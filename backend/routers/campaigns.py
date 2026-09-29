"""routers/campaigns.py — Campaign generation and history endpoints."""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import get_db

router = APIRouter(prefix="/api/campaigns", tags=["Campaigns"])


# ---------------------------------------------------------------------------
# Request / response schemas (campaign-specific)
# ---------------------------------------------------------------------------

class CampaignCreate(BaseModel):
    grower_ids:       List[str]
    product:          str
    campaign_crop:    Optional[str] = None
    pest_threat:      Optional[str] = None
    weather_risk:     Optional[str] = None
    urgency:          Optional[str] = "normal"   # normal | high | low
    farmer_name:      Optional[str] = "Kisan"


class CampaignResult(BaseModel):
    grower_id:             str
    segment:               str
    engagement_probability: float
    channel:               str
    message:               str
    priority_score:        int


class CampaignResponse(BaseModel):
    total_targeted:   int
    total_skipped:    int
    results:          List[CampaignResult]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/", response_model=CampaignResponse, summary="Generate campaign for multiple farmers")
async def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    """
    Run predictions for a list of grower_ids and return ranked campaign plan.
    Only farmers already in the database are processed; others are skipped.
    """
    from routers.predict import _get_predictor, _season_context
    from services.pest_context_service import get_pest_context

    predictor, recommender, generator, rag_service, vernacular_service, urgency_service, audio_service = _get_predictor()

    results:  List[CampaignResult] = []
    skipped = 0
    broadcast_payloads = []

    for grower_id in payload.grower_ids:
        farmer = db.query(models.Farmer).filter(
            models.Farmer.grower_id == grower_id
        ).first()

        if not farmer:
            skipped += 1
            continue

        farmer_dict = {
            "grower_id":   farmer.grower_id,
            "state":       farmer.state,
            "district":    farmer.district,
            "tehsil_block": farmer.tehsil_block,
            "village":     farmer.village,
            "language":    farmer.language,
            "device_type": farmer.device_type,
            "connectivity": farmer.connectivity,
            "literacy_level": farmer.literacy_level,
            "gender":      farmer.gender,
            "grower_age":  farmer.age,
            "grower_farm_size":           farmer.farm_size,
            "grower_crop_calendar":       farmer.crop_calendar_json,
            "main_crop":                  farmer.crop,
            "product_scan":               farmer.product_scan,
            "offline_campaign_attended":  farmer.offline_campaign_attended,
            "campaign_crop":              payload.campaign_crop or farmer.crop,
            "campaign_product":           payload.product,
            "pest_threat":                payload.pest_threat,
            "weather_risk":               payload.weather_risk,
            "high_value_farmer":           farmer.high_value_farmer,
        }

        try:
            pred    = predictor.predict(farmer_dict)
            season_context = _season_context(farmer_dict)
            vernacular = vernacular_service.infer(farmer_dict)
            rag = rag_service.retrieve(farmer_dict)
            pest_context = get_pest_context(
                farmer_dict.get("main_crop") or farmer_dict.get("campaign_crop"),
                payload.pest_threat,
                payload.weather_risk,
            )
            urgency = urgency_service.score(farmer_dict, pred, season_context)
            channel = recommender.recommend(
                segment     = pred["segment"],
                device_type = farmer_dict.get("device_type"),
                language    = vernacular["language"],
                season_phase = season_context["season_phase"],
                literacy_level = farmer_dict.get("literacy_level"),
                connectivity = farmer_dict.get("connectivity"),
                high_value_farmer = bool(farmer_dict.get("high_value_farmer")),
            )

            content = generator.generate(
                farmer_name      = farmer.name or payload.farmer_name,
                segment          = pred["segment"],
                growth_stage     = season_context["estimated_growth_stage"],
                crop             = farmer.crop,
                campaign_product = payload.product,
                district         = farmer.district,
                days_until_harvest = season_context["days_until_harvest"],
                language         = vernacular["language"],
                channel          = channel["primary_channel"],
                vernacular       = vernacular,
                rag_context      = rag,
                pest_context     = pest_context,
                urgency          = urgency,
            )
            content["audio_file"] = audio_service.generate(
                content["voice_script"],
                vernacular["language"],
                farmer.grower_id,
            )

            # Persist campaign record
            campaign_row = models.Campaign(
                farmer_id       = farmer.id,
                product         = payload.product,
                campaign_crop   = payload.campaign_crop or farmer.crop,
                channel         = channel["primary_channel"],
                message         = content["primary_message"],
                sms_message     = content["sms"],
                whatsapp_message = content["whatsapp"],
                voice_script    = content["voice_script"],
                rag_summary     = rag["advisory_summary"],
                predicted_score = pred["engagement_probability"],
                segment         = pred["segment"],
                sent_at         = datetime.utcnow(),
            )
            db.add(campaign_row)

            results.append(CampaignResult(
                grower_id              = grower_id,
                segment                = pred["segment"],
                engagement_probability = pred["engagement_probability"],
                channel                = channel["primary_channel"],
                message                = content["primary_message"],
                priority_score         = channel["priority_score"],
            ))

            broadcast_payloads.append({
                "grower_id": grower_id,
                "prediction": pred,
                "channel": channel,
                "vernacular": vernacular,
                "urgency": urgency,
                "rag": rag,
                "content": content,
                "pest_threat": payload.pest_threat,
            })

        except Exception as exc:
            skipped += 1
            continue

    db.commit()

    # Broadcast generated campaigns after successful DB commit
    from routers.realtime import manager
    for payload_data in broadcast_payloads:
        try:
            await manager.broadcast({
                "type": "campaign-generated",
                "data": payload_data
            })
        except Exception as exc:
            import logging
            logging.getLogger("syngenta.api").warning(f"Could not broadcast campaign-generated event: {exc}")

    # Sort by priority (highest first)
    results.sort(key=lambda r: r.priority_score, reverse=True)

    return CampaignResponse(
        total_targeted = len(results),
        total_skipped  = skipped,
        results        = results,
    )


@router.get("/history", summary="Get campaign history")
def campaign_history(
    limit:  int = 50,
    skip:   int = 0,
    grower_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Return recent campaign records ordered by creation time, optionally filtered by grower_id."""
    query = db.query(models.Campaign)
    if grower_id:
        query = query.join(models.Farmer).filter(models.Farmer.grower_id == grower_id)
    
    rows = (
        query
        .order_by(models.Campaign.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "id":              r.id,
            "farmer_id":       r.farmer_id,
            "product":         r.product,
            "campaign_crop":   r.campaign_crop,
            "channel":         r.channel,
            "segment":         r.segment,
            "predicted_score": r.predicted_score,
            "actual_clicked":  r.actual_clicked,
            "message":         r.message,
            "sms_message":     r.sms_message,
            "whatsapp_message": r.whatsapp_message,
            "voice_script":    r.voice_script,
            "rag_summary":     r.rag_summary,
            "audio_file":      r.audio_file,
            "sent_at":         r.sent_at.isoformat() if r.sent_at else None,
            "created_at":      r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@router.get("/metrics", summary="Campaign efficiency metrics")
def campaign_metrics(db: Session = Depends(get_db)):
    rows = db.query(models.Campaign).all()
    total = len(rows)
    clicked = sum(1 for row in rows if row.actual_clicked is True)
    by_channel = {}
    by_segment = {}
    for row in rows:
        by_channel[row.channel or "unknown"] = by_channel.get(row.channel or "unknown", 0) + 1
        by_segment[row.segment or "unknown"] = by_segment.get(row.segment or "unknown", 0) + 1
    avg_score = sum((row.predicted_score or 0) for row in rows) / total if total else 0
    return {
        "total_campaigns": total,
        "recorded_clicks": clicked,
        "observed_ctr": clicked / total if total else 0,
        "average_predicted_engagement": avg_score,
        "by_channel": by_channel,
        "by_segment": by_segment,
    }


@router.patch("/{campaign_id}/clicked", summary="Record actual click outcome")
async def record_click(campaign_id: int, clicked: bool, db: Session = Depends(get_db)):
    """Update the actual_clicked flag for a campaign (for feedback loop tracking)."""
    row = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Campaign not found")
    row.actual_clicked = clicked
    db.commit()

    # Broadcast interaction to WebSockets
    try:
        from routers.realtime import manager
        await manager.broadcast({
            "type": "farmer-interaction",
            "data": {
                "campaign_id": campaign_id,
                "actual_clicked": clicked
            }
        })
    except Exception as exc:
        import logging
        logging.getLogger("syngenta.api").warning(f"Could not broadcast farmer-interaction event: {exc}")

    return {"campaign_id": campaign_id, "actual_clicked": clicked}
