"""
preprocessing.py
----------------
Utility functions that mirror the EXACT feature engineering steps from the
Colab notebook (Syngenta_Track1_FINAL_NO_LEAKAGE.ipynb).

All functions are pure / stateless so they can be imported freely by the
predictor and any other service.
"""

import json
import math
from datetime import datetime
from typing import Any, Optional, Tuple

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Crop-calendar parsing
# ---------------------------------------------------------------------------

def parse_crop_calendar(
    calendar_json: Any,
) -> Tuple[Optional[str], Any, Any, Any, Any, Any]:
    """
    Parse grower_crop_calendar JSON into (crop, sowing_start, sowing_end,
    harvest_start, harvest_end, stages).

    Mirrors Colab: def parse_crop_calendar(calendar_json)
    """
    if calendar_json is None:
        return None, None, None, None, None, None
    try:
        if isinstance(calendar_json, float) and math.isnan(calendar_json):
            return None, None, None, None, None, None
    except (TypeError, ValueError):
        pass

    try:
        data = json.loads(calendar_json) if isinstance(calendar_json, str) else calendar_json
        crop = data.get("crop")

        sowing_start = sowing_end = None
        if "sowing" in data and isinstance(data["sowing"], dict):
            raw = data["sowing"].get("start")
            sowing_start = pd.to_datetime(raw, errors="coerce") if raw else None
            raw = data["sowing"].get("end")
            sowing_end = pd.to_datetime(raw, errors="coerce") if raw else None

        harvest_start = harvest_end = None
        if "harvest" in data and isinstance(data["harvest"], dict):
            raw = data["harvest"].get("start")
            harvest_start = pd.to_datetime(raw, errors="coerce") if raw else None
            raw = data["harvest"].get("end")
            harvest_end = pd.to_datetime(raw, errors="coerce") if raw else None

        stages = data.get("stages")
        return crop, sowing_start, sowing_end, harvest_start, harvest_end, stages

    except Exception:
        return None, None, None, None, None, None


# ---------------------------------------------------------------------------
# 2. Time / seasonal features
# ---------------------------------------------------------------------------

def calculate_time_features(
    sowing_start:   Optional[Any],
    harvest_start:  Optional[Any],
    reference_date: Optional[Any] = None,
) -> dict:
    """
    Calculate time-based features from crop calendar dates.

    Mirrors Colab cells:
        growers['days_since_sowing_start'] = (ref - sowing_start).dt.days
        growers['days_until_harvest']      = (harvest_start - ref).dt.days
        growers['estimated_growth_stage']  = ...
        growers['near_harvest']            = days_until_harvest <= 30
        growers['season_phase']            = ...
    """
    if reference_date is None:
        reference_date = pd.Timestamp(datetime.utcnow())
    else:
        reference_date = pd.Timestamp(reference_date)

    sowing_ts  = pd.Timestamp(sowing_start)  if sowing_start  is not None else pd.NaT
    harvest_ts = pd.Timestamp(harvest_start) if harvest_start is not None else pd.NaT

    days_since_sowing: Optional[float] = (
        (reference_date - sowing_ts).days if not pd.isna(sowing_ts) else None
    )
    days_until_harvest: Optional[float] = (
        (harvest_ts - reference_date).days if not pd.isna(harvest_ts) else None
    )

    growth_stage = estimate_growth_stage(days_since_sowing)
    near_harv    = (
        int(0 <= days_until_harvest <= 30)
        if days_until_harvest is not None else 0
    )
    season_ph = get_season_phase(days_since_sowing, days_until_harvest)

    return {
        "days_since_sowing_start": days_since_sowing if days_since_sowing is not None else np.nan,
        "days_until_harvest":      days_until_harvest if days_until_harvest is not None else np.nan,
        "estimated_growth_stage":  growth_stage,
        "near_harvest":            near_harv,
        "season_phase":            season_ph,
    }


def estimate_growth_stage(days: Optional[float]) -> str:
    """
    Mirrors Colab: def estimate_growth_stage(days)
    """
    if days is None or (isinstance(days, float) and math.isnan(days)):
        return "unknown"
    if days < 0:
        return "pre_sowing"
    elif days < 30:
        return "germination"
    elif days < 60:
        return "vegetative"
    elif days < 90:
        return "reproductive"
    elif days < 120:
        return "maturity"
    else:
        return "post_harvest"


def get_season_phase(
    days_sowing:  Optional[float],
    days_harvest: Optional[float],
) -> str:
    """
    Mirrors Colab: def get_season_phase(days_sowing, days_harvest)
    """
    if days_sowing is None or days_harvest is None:
        return "unknown"
    if isinstance(days_sowing, float) and math.isnan(days_sowing):
        return "unknown"
    if isinstance(days_harvest, float) and math.isnan(days_harvest):
        return "unknown"

    if days_sowing < 0:
        return "pre_season"
    elif days_harvest > 60:
        return "early_season"
    elif days_harvest > 30:
        return "mid_season"
    elif days_harvest > 0:
        return "late_season"
    else:
        return "post_season"


# ---------------------------------------------------------------------------
# 3. Demographic / behavioural features
# ---------------------------------------------------------------------------

def create_demographic_features(
    age: Optional[float],
    farm_size: Optional[float],
) -> dict:
    """
    Mirrors Colab:
        growers['age_group']          = pd.cut(grower_age, bins=[0,30,40,50,60,100], ...)
        growers['farm_size_category'] = pd.cut(grower_farm_size, bins=[0,2,5,10,inf], ...)
    """
    if age is None or (isinstance(age, float) and math.isnan(age)):
        age_group = "unknown"
    elif age <= 30:
        age_group = "age_under_30"
    elif age <= 40:
        age_group = "age_30_40"
    elif age <= 50:
        age_group = "age_40_50"
    elif age <= 60:
        age_group = "age_50_60"
    else:
        age_group = "age_over_60"

    if farm_size is None or (isinstance(farm_size, float) and math.isnan(farm_size)):
        farm_size_category = "unknown"
    elif farm_size <= 2:
        farm_size_category = "marginal"
    elif farm_size <= 5:
        farm_size_category = "small"
    elif farm_size <= 10:
        farm_size_category = "medium"
    else:
        farm_size_category = "large"

    return {"age_group": age_group, "farm_size_category": farm_size_category}


# ---------------------------------------------------------------------------
# 4. Crop-product relevance
# ---------------------------------------------------------------------------

def check_crop_match(
    main_crop:     Optional[str],
    campaign_crop: Optional[str],
) -> str:
    """
    Mirrors Colab: def check_crop_match(row)
    Returns 'exact_match', 'similar_match', 'no_match', or 'unknown'.
    """
    crop  = str(main_crop   or "").strip().lower()
    ccrop = str(campaign_crop or "").strip().lower()

    if not crop or crop in ("none", "nan") or not ccrop or ccrop in ("none", "nan"):
        return "unknown"
    if crop == ccrop:
        return "exact_match"

    similar = {
        "wheat":    ["barley"],
        "mustard":  ["safflower"],
        "chickpea": ["lentil"],
    }
    if crop in similar and ccrop in similar[crop]:
        return "similar_match"

    return "no_match"


# ---------------------------------------------------------------------------
# 5. Interaction / composite features
# ---------------------------------------------------------------------------

def build_interaction_features(
    main_crop:          Optional[str],
    season_phase:       Optional[str],
    age_group:          Optional[str],
    farm_size_category: Optional[str],
    device_type:        Optional[str],
    language:           Optional[str],
) -> dict:
    """
    Mirrors Colab:
        campaign_df['crop_season_interaction'] = main_crop + '_' + season_phase
        campaign_df['age_farm_interaction']    = age_group + '_' + farm_size_category
        growers['device_language_combo']       = device_type + '_' + language
    """
    def _s(v: Optional[str]) -> str:
        return str(v).strip() if v and str(v).strip() not in ("", "None", "nan") else "unknown"

    return {
        "crop_season_interaction": f"{_s(main_crop)}_{_s(season_phase)}",
        "age_farm_interaction":    f"{_s(age_group)}_{_s(farm_size_category)}",
        "device_language_combo":   f"{_s(device_type)}_{_s(language)}",
    }


# ---------------------------------------------------------------------------
# 6. Temporal campaign features
# ---------------------------------------------------------------------------

def get_campaign_temporal_features(
    message_sent_date: Optional[Any] = None,
    season_start_date: Optional[Any] = None,
) -> dict:
    """
    Mirrors Colab:
        campaign_df['day_of_week']    = message_sent_date.dt.dayofweek
        campaign_df['is_weekend']     = day_of_week.isin([5, 6]).astype(int)
        campaign_df['week_of_season'] = (message_sent_date - min_date).dt.days // 7
    """
    ts = pd.Timestamp(message_sent_date) if message_sent_date is not None else pd.Timestamp(datetime.utcnow())
    day_of_week = ts.dayofweek
    is_weekend  = int(day_of_week in (5, 6))

    season_start = (
        pd.Timestamp(season_start_date)
        if season_start_date is not None
        else pd.Timestamp(f"{ts.year}-01-01")
    )
    week_of_season = max(0, (ts - season_start).days // 7)

    return {
        "day_of_week":    day_of_week,
        "is_weekend":     is_weekend,
        "week_of_season": week_of_season,
    }
