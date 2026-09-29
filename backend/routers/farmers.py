"""routers/farmers.py — CRUD endpoints for farmer profiles."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import FarmerProfile

router = APIRouter(prefix="/api/farmers", tags=["Farmers"])


@router.get("/", summary="List all farmers")
def list_farmers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Return a paginated list of all farmers in the database."""
    farmers = db.query(models.Farmer).offset(skip).limit(limit).all()
    return [_farmer_to_dict(f) for f in farmers]


@router.get("/{grower_id}", summary="Get farmer by grower_id")
def get_farmer(grower_id: str, db: Session = Depends(get_db)):
    """Return a single farmer's profile by their grower_id."""
    farmer = db.query(models.Farmer).filter(models.Farmer.grower_id == grower_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail=f"Farmer '{grower_id}' not found")
    return _farmer_to_dict(farmer)


@router.post("/", summary="Create or update a farmer profile", status_code=201)
async def upsert_farmer(profile: FarmerProfile, db: Session = Depends(get_db)):
    """
    Create a new farmer or update an existing one (matched on grower_id).
    """
    if not profile.grower_id:
        raise HTTPException(status_code=422, detail="grower_id is required")

    farmer = db.query(models.Farmer).filter(
        models.Farmer.grower_id == profile.grower_id
    ).first()

    if farmer is None:
        farmer = models.Farmer(grower_id=profile.grower_id)
        db.add(farmer)

    farmer.state        = profile.state
    farmer.district     = profile.district
    farmer.name         = profile.name
    farmer.tehsil_block = profile.tehsil_block
    farmer.village      = profile.village
    farmer.language     = profile.language
    farmer.device_type  = profile.device_type
    farmer.connectivity = profile.connectivity
    farmer.literacy_level = profile.literacy_level
    farmer.gender       = profile.gender
    farmer.age          = profile.grower_age
    farmer.farm_size    = profile.grower_farm_size
    farmer.crop         = profile.main_crop
    farmer.high_value_farmer = profile.high_value_farmer or False
    farmer.crop_calendar_json = profile.grower_crop_calendar
    farmer.product_scan              = profile.product_scan or False
    farmer.offline_campaign_attended = profile.offline_campaign_attended or False

    db.commit()
    db.refresh(farmer)

    # Broadcast active farmer update to WebSockets
    try:
        from routers.realtime import manager
        await manager.broadcast({
            "type": "active-farmer-updated",
            "data": _farmer_to_dict(farmer)
        })
    except Exception as exc:
        import logging
        logging.getLogger("syngenta.api").warning(f"Could not broadcast active-farmer-updated event: {exc}")

    return _farmer_to_dict(farmer)


# ---------------------------------------------------------------------------
def _farmer_to_dict(f: models.Farmer) -> dict:
    return {
        "id":          f.id,
        "grower_id":   f.grower_id,
        "name":        f.name,
        "age":         f.age,
        "farm_size":   f.farm_size,
        "state":       f.state,
        "district":    f.district,
        "tehsil_block": f.tehsil_block,
        "village":     f.village,
        "language":    f.language,
        "device_type": f.device_type,
        "connectivity": f.connectivity,
        "literacy_level": f.literacy_level,
        "gender":      f.gender,
        "crop":        f.crop,
        "high_value_farmer": f.high_value_farmer,
        "product_scan":              f.product_scan,
        "offline_campaign_attended": f.offline_campaign_attended,
        "created_at":  f.created_at.isoformat() if f.created_at else None,
    }
