"""Urgency scoring for time-sensitive campaign prioritization."""

from __future__ import annotations

from typing import Any, Dict


SEVERE_PEST_TERMS = {
    "pink bollworm": 30,
    "bollworm": 24,
    "fungal": 20,
    "blast": 24,
    "blight": 24,
    "rust": 22,
    "fall armyworm": 30,
    "outbreak": 28,
}

WEATHER_TERMS = {
    "humidity": 18,
    "rain": 16,
    "heavy rain": 20,
    "cloudy": 10,
    "dry": 10,
    "heat": 12,
}


class UrgencyService:
    def score(self, farmer: Dict[str, Any], prediction: Dict[str, Any], season_context: Dict[str, Any]) -> Dict[str, Any]:
        score = int(float(prediction.get("engagement_probability", 0)) * 25)
        pest = str(farmer.get("pest_threat") or "").lower()
        weather = str(farmer.get("weather_risk") or "").lower()

        reasons = []
        for term, points in SEVERE_PEST_TERMS.items():
            if term in pest:
                score += points
                reasons.append(f"Pest risk matched: {term}")
                break
        for term, points in WEATHER_TERMS.items():
            if term in weather:
                score += points
                reasons.append(f"Weather risk matched: {term}")
                break

        phase = season_context.get("season_phase")
        stage = season_context.get("estimated_growth_stage")
        if phase in {"mid_season", "late_season"}:
            score += 18
            reasons.append(f"Season timing is sensitive: {phase}")
        if stage in {"reproductive", "maturity"}:
            score += 12
            reasons.append(f"Crop stage is time-sensitive: {stage}")
        if prediction.get("segment") in {"High", "Very High"}:
            score += 12
            reasons.append("Farmer is likely to respond to a timely campaign")

        score = max(0, min(100, score))
        if score >= 70:
            level = "high"
        elif score >= 40:
            level = "medium"
        else:
            level = "low"
        return {"urgency_score": score, "urgency_level": level, "urgency_reasons": reasons}
