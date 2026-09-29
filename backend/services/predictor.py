"""
predictor.py
------------
EngagementPredictor: loads the pre-trained LightGBM model and reconstructs
the exact 32 features used during training, following the same steps as the
Colab notebook (Syngenta_Track1_FINAL_NO_LEAKAGE.ipynb).
"""

import json
import logging
import pickle
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Fix Windows console encoding so logger doesn't choke on non-ASCII
# ---------------------------------------------------------------------------
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Lazy import of preprocessing utils (avoids circular-import issues)
# ---------------------------------------------------------------------------
def _get_preprocessing():
    # Ensure the backend/ root is on sys.path so `utils` is importable
    # regardless of whether we're running from backend/ or a parent directory
    _backend_root = str(Path(__file__).resolve().parent.parent)
    if _backend_root not in sys.path:
        sys.path.insert(0, _backend_root)

    from utils.preprocessing import (
        parse_crop_calendar,
        calculate_time_features,
        create_demographic_features,
        check_crop_match,
        build_interaction_features,
        get_campaign_temporal_features,
    )
    return (
        parse_crop_calendar,
        calculate_time_features,
        create_demographic_features,
        check_crop_match,
        build_interaction_features,
        get_campaign_temporal_features,
    )


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths - resolve relative to THIS file so CWD doesn't matter
# ---------------------------------------------------------------------------
_HERE       = Path(__file__).resolve().parent        # backend/services/
_MODELS_DIR = _HERE.parent / "models"                # backend/models/

_MODEL_PATH    = _MODELS_DIR / "model_no_leakage.pkl"
_ENCODERS_PATH = _MODELS_DIR / "label_encoders_clean.pkl"
_FEATURES_PATH = _MODELS_DIR / "feature_columns.json"
_METADATA_PATH = _MODELS_DIR / "model_metadata.json"

# ---------------------------------------------------------------------------
# Feature type sets (must match training)
# ---------------------------------------------------------------------------
_CATEGORICAL_COLS = {
    "state", "district", "language", "device_type", "gender",
    "age_group", "farm_size_category", "main_crop",
    "estimated_growth_stage", "season_phase",
    "campaign_crop", "campaign_product", "crop_product_relevance",
    "device_language_combo", "crop_season_interaction", "age_farm_interaction",
}

_BOOLEAN_COLS = {"product_scan", "offline_campaign_attended", "near_harvest", "is_weekend"}

# Safe fallback values for missing numerics (mirrors Colab median fills)
_NUMERICAL_DEFAULTS: Dict[str, float] = {
    "grower_age":              35.0,
    "grower_farm_size":         2.0,
    "days_since_sowing_start": 45.0,
    "days_until_harvest":      60.0,
    "engagement_score":         0.0,
    "hist_open_rate":           0.0,
    "hist_click_rate":          0.0,
    "message_count_history":    0.0,
    "days_since_last_message": 999.0,
    "message_frequency":        0.0,
    "day_of_week":              2.0,
    "week_of_season":           4.0,
    "is_weekend":               0.0,
    "near_harvest":             0.0,
    "product_scan":             0.0,
    "offline_campaign_attended": 0.0,
}


class EngagementPredictor:
    """
    Loads the pre-trained LightGBM model and predicts click-engagement
    probability for a farmer-campaign pair.

    Usage
    -----
    predictor = EngagementPredictor()
    result = predictor.predict({
        "state": "Rajasthan",
        "grower_age": 42,
        "grower_farm_size": 4.5,
        "campaign_crop": "wheat",
        ...
    })
    # -> {'engagement_probability': 0.078, 'segment': 'High', 'confidence': 'high', ...}
    """

    def __init__(self) -> None:
        self._load_artifacts()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _load_artifacts(self) -> None:
        """Load model, encoders, feature list and metadata from disk."""
        if not _MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {_MODEL_PATH}")
        with open(_MODEL_PATH, "rb") as fh:
            self.model = pickle.load(fh)
        logger.info("Model loaded from %s", _MODEL_PATH)

        if not _ENCODERS_PATH.exists():
            raise FileNotFoundError(f"Encoders not found: {_ENCODERS_PATH}")
        with open(_ENCODERS_PATH, "rb") as fh:
            self.label_encoders: Dict[str, Any] = pickle.load(fh)
        logger.info("%d label encoders loaded", len(self.label_encoders))

        if not _FEATURES_PATH.exists():
            raise FileNotFoundError(f"Feature columns not found: {_FEATURES_PATH}")
        with open(_FEATURES_PATH, "r") as fh:
            feature_data = json.load(fh)
        self.feature_columns: list = feature_data["features"]
        logger.info("Feature list loaded: %d features", len(self.feature_columns))

        self.metadata: Dict = {}
        if _METADATA_PATH.exists():
            with open(_METADATA_PATH, "r") as fh:
                self.metadata = json.load(fh)

        print(f"[Predictor] Model ready | features={len(self.feature_columns)} "
              f"| roc_auc={self.metadata.get('roc_auc', 0):.4f}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def predict(self, farmer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict engagement probability for a farmer-campaign pair.

        Parameters
        ----------
        farmer_data : dict
            Raw farmer and campaign attributes.

        Returns
        -------
        dict
            engagement_probability (float 0-1), segment (str),
            confidence (str), model_version (str), features_used (int)
        """
        try:
            feature_vector = self._prepare_features(farmer_data)
            prob = float(self.model.predict_proba([feature_vector])[0][1])
            segment = self._determine_segment(prob)
            return {
                "engagement_probability": round(prob, 6),
                "segment":    segment,
                "confidence": "high" if segment in ("High", "Very High")
                              else ("medium" if segment == "Medium" else "low"),
                "model_version": self.metadata.get("training_date", "unknown"),
                "features_used": len(self.feature_columns),
            }
        except Exception as exc:
            logger.exception("Prediction failed: %s", exc)
            raise

    # ------------------------------------------------------------------
    # Feature engineering (mirrors the Colab notebook exactly)
    # ------------------------------------------------------------------

    def _prepare_features(self, farmer_data: Dict[str, Any]) -> list:
        """Build the ordered 32-feature vector expected by the model."""
        features = self._engineer_all_features(farmer_data)
        vector: list = []

        for col in self.feature_columns:
            raw_val = features.get(col)

            if col in _CATEGORICAL_COLS:
                vector.append(self._encode_categorical(col, raw_val))

            elif col in _BOOLEAN_COLS:
                if raw_val is None:
                    vector.append(int(_NUMERICAL_DEFAULTS.get(col, 0)))
                else:
                    try:
                        vector.append(int(bool(raw_val)))
                    except (TypeError, ValueError):
                        vector.append(0)
            else:
                # Numerical
                if raw_val is None or (isinstance(raw_val, float) and np.isnan(raw_val)):
                    vector.append(float(_NUMERICAL_DEFAULTS.get(col, 0.0)))
                else:
                    try:
                        vector.append(float(raw_val))
                    except (TypeError, ValueError):
                        vector.append(float(_NUMERICAL_DEFAULTS.get(col, 0.0)))

        return vector

    def _engineer_all_features(self, fd: Dict[str, Any]) -> Dict[str, Any]:
        """Run the full feature-engineering pipeline on raw farmer_data."""
        (
            parse_crop_calendar,
            calculate_time_features,
            create_demographic_features,
            check_crop_match,
            build_interaction_features,
            get_campaign_temporal_features,
        ) = _get_preprocessing()

        feat: Dict[str, Any] = {}

        # 1. Direct demographics
        feat["state"]            = fd.get("state")       or "unknown"
        feat["district"]         = fd.get("district")    or "unknown"
        feat["language"]         = fd.get("language")    or "unknown"
        feat["device_type"]      = fd.get("device_type") or "unknown"
        feat["gender"]           = fd.get("gender")      or "unknown"
        feat["grower_age"]       = fd.get("grower_age")
        feat["grower_farm_size"] = fd.get("grower_farm_size")

        # 2. Derived demographic bins (age_group, farm_size_category)
        feat.update(create_demographic_features(feat["grower_age"], feat["grower_farm_size"]))

        # 3. Crop calendar -> main_crop + timing features
        main_crop     = fd.get("main_crop")
        sowing_start  = fd.get("sowing_start")
        harvest_start = fd.get("harvest_start")

        if not main_crop or not sowing_start:
            cal_json = fd.get("grower_crop_calendar")
            if cal_json:
                pc, ps, _, ph, _, _ = parse_crop_calendar(cal_json)
                main_crop     = main_crop     or pc
                sowing_start  = sowing_start  or ps
                harvest_start = harvest_start or ph

        feat["main_crop"] = main_crop or "unknown"

        # 4. Time features (days_since_sowing_start, days_until_harvest,
        #                   estimated_growth_stage, near_harvest, season_phase)
        ref_date = fd.get("message_sent_date") or datetime.utcnow()
        feat.update(calculate_time_features(sowing_start, harvest_start, ref_date))

        # 5. Static behavioural flags
        feat["product_scan"]              = int(bool(fd.get("product_scan", False)))
        feat["offline_campaign_attended"] = int(bool(fd.get("offline_campaign_attended", False)))
        feat["engagement_score"]          = feat["product_scan"] + feat["offline_campaign_attended"]

        # 6. Campaign characteristics
        feat["campaign_crop"]          = fd.get("campaign_crop")    or "unknown"
        feat["campaign_product"]       = fd.get("campaign_product") or "unknown"
        feat["crop_product_relevance"] = check_crop_match(feat["main_crop"], feat["campaign_crop"])

        # 7. Interaction features
        feat.update(build_interaction_features(
            main_crop          = feat["main_crop"],
            season_phase       = feat["season_phase"],
            age_group          = feat["age_group"],
            farm_size_category = feat["farm_size_category"],
            device_type        = feat["device_type"],
            language           = feat["language"],
        ))

        # 8. Temporal campaign features (day_of_week, is_weekend, week_of_season)
        feat.update(get_campaign_temporal_features(ref_date))

        # 9. Engagement history (caller-supplied or safe defaults)
        feat["hist_open_rate"]           = fd.get("hist_open_rate",          0.0)
        feat["hist_click_rate"]          = fd.get("hist_click_rate",         0.0)
        feat["message_count_history"]    = fd.get("message_count_history",   0.0)
        feat["days_since_last_message"]  = fd.get("days_since_last_message", 999.0)
        feat["message_frequency"]        = fd.get("message_frequency",       0.0)

        return feat

    # ------------------------------------------------------------------
    # Encoding helpers
    # ------------------------------------------------------------------

    def _encode_categorical(self, col: str, value: Any) -> int:
        """Apply the fitted LabelEncoder; unknown labels fall back to 0."""
        if col not in self.label_encoders:
            return 0

        le      = self.label_encoders[col]
        str_val = str(value).strip() if value is not None else "unknown"
        if str_val in ("", "None", "nan", "NaN"):
            str_val = "unknown"

        if str_val in le.classes_:
            return int(le.transform([str_val])[0])
        if "unknown" in le.classes_:
            return int(le.transform(["unknown"])[0])
        return 0

    # ------------------------------------------------------------------
    # Segment mapping (mirrors Colab pd.cut bins)
    # ------------------------------------------------------------------

    @staticmethod
    def _determine_segment(probability: float) -> str:
        """
        bins=[0, 0.03, 0.06, 0.10, 1.0]
        labels=['Low', 'Medium', 'High', 'Very High']
        """
        if probability >= 0.10:
            return "Very High"
        elif probability >= 0.06:
            return "High"
        elif probability >= 0.03:
            return "Medium"
        else:
            return "Low"