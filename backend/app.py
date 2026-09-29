"""FastAPI entrypoint for KrishiSetu (कृषि-सेतु) Digital Public Good."""

from __future__ import annotations

import json
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

sys.path.insert(0, str(Path(__file__).parent))

from database import init_db
from routers import advisory, campaigns, diagnose, farmers, interop, predict, realtime, telemetry

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
logger = logging.getLogger("krishisetu.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting KrishiSetu (कृषि-सेतु) Cooperative Digital Agriculture API.")
    init_db()
    audio_path = Path(__file__).parent / "audio"
    audio_path.mkdir(parents=True, exist_ok=True)
    try:
        predict._get_predictor()
        logger.info("Core ML, RAG and Gemini services pre-warmed.")
    except Exception as exc:
        logger.warning("Could not pre-warm services: %s", exc)
    yield
    logger.info("KrishiSetu API shutting down.")


app = FastAPI(
    title="KrishiSetu (कृषि-सेतु) Cooperative Digital Agriculture API",
    description=(
        "Digital Public Good for Multimodal Crop Disease Diagnostics, "
        "Grounded Regenerative Agro-Advisories, Environmental Telemetry, and Cross-State Agricultural Interoperability."
    ),
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# KrishiSetu Core Digital Public Good Endpoints
app.include_router(diagnose.router)
app.include_router(advisory.router)
app.include_router(interop.router)
app.include_router(telemetry.router)

# Legacy & Extension Endpoints
app.include_router(farmers.router)
app.include_router(predict.router)
app.include_router(campaigns.router)
app.include_router(realtime.router)

audio_dir = Path(__file__).parent / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")


@app.get("/health", tags=["System"], summary="Health check")
def health():
    from routers.predict import _predictor

    model_ok = _predictor is not None
    return {
        "status": "ok",
        "model_loaded": model_ok,
        "n_features": len(_predictor.feature_columns) if model_ok else 0,
        "roc_auc": _predictor.metadata.get("roc_auc", 0) if model_ok else 0,
    }


@app.get("/api/segments/stats", tags=["Analytics"], summary="Segment statistics")
def segment_stats():
    path = Path(__file__).parent / "data" / "segment_stats.json"
    if not path.exists():
        raise HTTPException(404, "Segment stats file not found.")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@app.get("/api/model/info", tags=["System"], summary="Model metadata")
def model_info():
    from routers.predict import _predictor

    if _predictor is None:
        raise HTTPException(503, "Model not loaded.")
    return {
        **_predictor.metadata,
        "feature_columns": _predictor.feature_columns,
        "n_label_encoders": len(_predictor.label_encoders),
    }


@app.get("/api/dashboard/stats", tags=["Analytics"], summary="Dashboard KPIs from database")
def dashboard_stats():
    """Return live KPIs for the Admin Command Center, sourced entirely from the database."""
    from database import SessionLocal
    import models

    db = SessionLocal()
    try:
        total_farmers = db.query(models.Farmer).count()
        total_campaigns = db.query(models.Campaign).count()
        total_clicked = db.query(models.Campaign).filter(models.Campaign.actual_clicked == True).count()
        observed_ctr = total_clicked / total_campaigns if total_campaigns else 0

        # Channel breakdown
        campaigns_all = db.query(models.Campaign).all()
        by_channel = {}
        by_segment = {}
        for c in campaigns_all:
            ch = (c.channel or "unknown").lower()
            by_channel[ch] = by_channel.get(ch, 0) + 1
            seg = c.segment or "unknown"
            by_segment[seg] = by_segment.get(seg, 0) + 1

        # Recent dispatches (last 10 campaigns with farmer info)
        recent = (
            db.query(models.Campaign, models.Farmer)
            .join(models.Farmer)
            .order_by(models.Campaign.created_at.desc())
            .limit(10)
            .all()
        )
        dispatches = []
        for campaign, farmer in recent:
            dispatches.append({
                "id": campaign.id,
                "farmer_name": farmer.name or f"Farmer {farmer.grower_id}",
                "grower_id": farmer.grower_id,
                "location": f"{farmer.state or ''}, {farmer.district or ''}".strip(", "),
                "channel": campaign.channel,
                "product": campaign.product,
                "crop": campaign.campaign_crop,
                "segment": campaign.segment,
                "predicted_score": campaign.predicted_score,
                "actual_clicked": campaign.actual_clicked,
                "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
            })

        # Farmer list for reference
        farmers_list = db.query(models.Farmer).order_by(models.Farmer.created_at.desc()).limit(20).all()
        farmer_records = [
            {
                "grower_id": f.grower_id,
                "name": f.name,
                "state": f.state,
                "district": f.district,
                "crop": f.crop,
                "language": f.language,
                "device_type": f.device_type,
                "created_at": f.created_at.isoformat() if f.created_at else None,
            }
            for f in farmers_list
        ]

        return {
            "total_farmers": total_farmers,
            "total_campaigns": total_campaigns,
            "total_clicked": total_clicked,
            "observed_ctr": round(observed_ctr, 4),
            "by_channel": by_channel,
            "by_segment": by_segment,
            "recent_dispatches": dispatches,
            "farmers": farmer_records,
        }
    finally:
        db.close()
