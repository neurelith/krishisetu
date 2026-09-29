"""Prediction and campaign-intelligence endpoints."""

from __future__ import annotations

from datetime import datetime
import json
import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import models
from database import get_db
from schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    ChannelRecommendation,
    ContentRecommendation,
    EngagementPrediction,
    PredictionRequest,
    PredictionResponse,
    RAGContext,
    UrgencyRecommendation,
    VernacularProfile,
)

router = APIRouter(prefix="/api", tags=["Prediction"])

_predictor = None
_recommender = None
_generator = None
_rag = None
_vernacular = None
_urgency = None
_audio = None


def _get_services():
    from services.audio_service import AudioService
    from services.channel_recommender import ChannelRecommender
    from services.content_generator import ContentGenerator
    from services.predictor import EngagementPredictor
    from services.rag_service import RagService
    from services.urgency_service import UrgencyService
    from services.vernacular_service import VernacularService

    return EngagementPredictor, ChannelRecommender, ContentGenerator, RagService, VernacularService, UrgencyService, AudioService


def _get_predictor():
    global _predictor, _recommender, _generator, _rag, _vernacular, _urgency, _audio
    if _predictor is None:
        EP, CR, CG, RS, VS, US, AS = _get_services()
        _predictor = EP()
        _recommender = CR()
        _generator = CG()
        _rag = RS()
        _vernacular = VS()
        _urgency = US()
        _audio = AS()
    return _predictor, _recommender, _generator, _rag, _vernacular, _urgency, _audio


@router.post("/predict", response_model=PredictionResponse, summary="Predict and generate adaptive campaign")
async def predict(request: PredictionRequest, db: Session = Depends(get_db)):
    predictor, recommender, generator, rag_service, vernacular_service, urgency_service, audio_service = _get_predictor()
    farmer_dict = {k: v for k, v in request.farmer.model_dump().items() if v is not None}

    try:
        pred = predictor.predict(farmer_dict)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction error: {exc}")

    season_context = _season_context(farmer_dict)
    vernacular = vernacular_service.infer(farmer_dict)
    rag = rag_service.retrieve(farmer_dict)

    from services.pest_context_service import get_pest_context

    pest_context = get_pest_context(
        farmer_dict.get("main_crop") or farmer_dict.get("campaign_crop"),
        farmer_dict.get("pest_threat"),
        farmer_dict.get("weather_risk"),
    )
    urgency = urgency_service.score(farmer_dict, pred, season_context)
    channel = recommender.recommend(
        segment=pred["segment"],
        device_type=farmer_dict.get("device_type"),
        season_phase=season_context["season_phase"],
        language=vernacular["language"],
        hist_open_rate=float(farmer_dict.get("hist_open_rate", 0.0)),
        hist_click_rate=float(farmer_dict.get("hist_click_rate", 0.0)),
        message_count_history=int(farmer_dict.get("message_count_history", 0)),
        literacy_level=farmer_dict.get("literacy_level"),
        connectivity=farmer_dict.get("connectivity"),
        high_value_farmer=bool(farmer_dict.get("high_value_farmer", False)),
    )
    content = generator.generate(
        farmer_name=request.farmer_name or "Kisan",
        segment=pred["segment"],
        growth_stage=farmer_dict.get("crop_stage") or season_context["estimated_growth_stage"],
        crop=farmer_dict.get("main_crop") or farmer_dict.get("campaign_crop"),
        campaign_product=farmer_dict.get("campaign_product"),
        district=farmer_dict.get("district"),
        days_until_harvest=season_context.get("days_until_harvest"),
        language=vernacular["language"],
        channel=channel["primary_channel"],
        vernacular=vernacular,
        rag_context=rag,
        pest_context=pest_context,
        urgency=urgency,
    )
    content["audio_file"] = audio_service.generate(
        content["voice_script"],
        vernacular["language"],
        farmer_dict.get("grower_id"),
    )

    _persist_prediction(db, farmer_dict, pred, channel, content, rag)
    reasoning = _engagement_reasoning(farmer_dict, pred, channel, urgency, rag)

    response_data = PredictionResponse(
        grower_id=farmer_dict.get("grower_id"),
        prediction=EngagementPrediction(**pred),
        channel=ChannelRecommendation(**channel),
        vernacular=VernacularProfile(**vernacular),
        urgency=UrgencyRecommendation(**urgency),
        engagement_reasoning=reasoning,
        rag=RAGContext(**rag),
        content=ContentRecommendation(**content),
    )

    # Broadcast campaign to WebSockets
    try:
        from routers.realtime import manager
        await manager.broadcast({
            "type": "campaign-generated",
            "data": response_data.model_dump()
        })
    except Exception as exc:
        # Fallback if broadcast fails so API call succeeds
        import logging
        logging.getLogger("syngenta.api").warning(f"Could not broadcast campaign-generated event: {exc}")

    return response_data


@router.post("/predict/batch", response_model=BatchPredictionResponse, summary="Batch farmer predictions")
async def batch_predict(request: BatchPredictionRequest, db: Session = Depends(get_db)):
    results = [
        await predict(PredictionRequest(farmer=farmer, farmer_name="Kisan"), db)
        for farmer in request.farmers
    ]
    return BatchPredictionResponse(total=len(results), results=results)


def _season_context(farmer_dict: dict) -> dict:
    from utils.preprocessing import calculate_time_features, parse_crop_calendar

    sowing = farmer_dict.get("sowing_start")
    harvest = farmer_dict.get("harvest_start")
    if not sowing and farmer_dict.get("grower_crop_calendar"):
        _, sowing, _, harvest, _, _ = parse_crop_calendar(farmer_dict["grower_crop_calendar"])
    tf = calculate_time_features(sowing, harvest, farmer_dict.get("message_sent_date"))
    return {
        **tf,
        "days_until_harvest": None if str(tf["days_until_harvest"]) == "nan" else tf["days_until_harvest"],
    }


def _persist_prediction(db: Session, farmer_dict: dict, pred: dict, channel: dict, content: dict, rag: dict) -> None:
    try:
        grower_id = farmer_dict.get("grower_id")
        if not grower_id:
            return
        farmer = db.query(models.Farmer).filter(models.Farmer.grower_id == grower_id).first()
        if not farmer:
            farmer = models.Farmer(grower_id=grower_id)
            db.add(farmer)
            db.flush()
        farmer.state = farmer_dict.get("state")
        farmer.district = farmer_dict.get("district")
        farmer.tehsil_block = farmer_dict.get("tehsil_block")
        farmer.village = farmer_dict.get("village")
        farmer.language = farmer_dict.get("language")
        farmer.device_type = farmer_dict.get("device_type")
        farmer.connectivity = farmer_dict.get("connectivity")
        farmer.literacy_level = farmer_dict.get("literacy_level")
        farmer.crop = farmer_dict.get("main_crop")
        farmer.high_value_farmer = bool(farmer_dict.get("high_value_farmer", False))

        db.add(models.Prediction(
            farmer_id=farmer.id,
            engagement_probability=pred["engagement_probability"],
            segment=pred["segment"],
            confidence=pred["confidence"],
            campaign_product=farmer_dict.get("campaign_product"),
            campaign_crop=farmer_dict.get("campaign_crop"),
            primary_channel=channel["primary_channel"],
            primary_message=content["primary_message"],
            rag_summary=rag.get("advisory_summary"),
            model_version=pred["model_version"],
        ))
        db.add(models.Advisory(
            farmer_id=farmer.id,
            crop=farmer_dict.get("main_crop") or farmer_dict.get("campaign_crop"),
            pest_threat=farmer_dict.get("pest_threat"),
            language=farmer_dict.get("language"),
            channel=channel["primary_channel"],
            sms=content["sms"],
            whatsapp=content["whatsapp"],
            voice_script=content["voice_script"],
            audio_file=content.get("audio_file"),
            rag_sources_json=json.dumps(rag.get("sources", []), ensure_ascii=False),
        ))
        db.add(models.Campaign(
            farmer_id=farmer.id,
            product=farmer_dict.get("campaign_product"),
            campaign_crop=farmer_dict.get("campaign_crop") or farmer_dict.get("main_crop"),
            channel=channel["primary_channel"],
            message=content["primary_message"],
            sms_message=content["sms"],
            whatsapp_message=content["whatsapp"],
            voice_script=content["voice_script"],
            rag_summary=rag.get("advisory_summary"),
            predicted_score=pred["engagement_probability"],
            segment=pred["segment"],
            audio_file=content.get("audio_file"),
            sent_at=datetime.utcnow(),
        ))
        db.commit()
    except Exception:
        db.rollback()


def _engagement_reasoning(farmer: dict, pred: dict, channel: dict, urgency: dict, rag: dict) -> list[str]:
    reasons = []
    crop = farmer.get("main_crop") or farmer.get("campaign_crop")
    pest = farmer.get("pest_threat")
    if crop:
        reasons.append(f"Campaign is crop-specific for {crop}.")
    if pest:
        reasons.append(f"Current advisory is driven by {pest} risk.")
    if pred.get("segment") in {"High", "Very High"}:
        reasons.append(f"{pred['segment']} receptivity segment based on model probability.")
    else:
        reasons.append(f"{pred['segment']} receptivity segment, so message frequency is capped.")
    if channel.get("primary_channel"):
        reasons.append(f"{channel['primary_channel']} selected from device, literacy and connectivity rules.")
    if urgency.get("urgency_level") == "high":
        reasons.append("High urgency due to pest, weather, or season timing.")
    if rag.get("sources"):
        top = rag["sources"][0]
        reasons.append(f"Top agronomy source matched {top.get('crop')} / {top.get('topic')}.")
    return reasons
