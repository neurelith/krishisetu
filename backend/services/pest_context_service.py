"""Rule-based pest and product context used before RAG/LLM generation."""

from __future__ import annotations

from typing import Dict, Optional


PEST_PLAYBOOK = {
    "rice": {
        "fungal": "Watch for sheath blight and blast in humid weather. Avoid dense canopy moisture and consult an agronomist for fungicide timing.",
        "stem borer": "Check dead hearts and white ear heads. Early field scouting helps prevent spread.",
        "brown planthopper": "Inspect the lower plant stem. Avoid excess nitrogen and act before hopper burn patches widen.",
    },
    "cotton": {
        "bollworm": "Scout squares and bolls twice a week. Use threshold-based control and rotate modes of action.",
        "sucking pest": "Check jassid, aphid and whitefly on the underside of leaves, especially after dry spells.",
        "pink bollworm": "Use pheromone traps and destroy rosette flowers. Timely action protects boll quality.",
    },
    "wheat": {
        "rust": "Yellow rust and leaf rust spread fast in cool humid weather. Inspect leaves and treat early.",
        "fungal": "Humidity can increase foliar disease pressure. Keep scouting before heading stage.",
    },
    "maize": {
        "fall armyworm": "Check whorl damage and fresh frass. Early-stage control gives the best result.",
    },
}


def get_pest_context(crop: Optional[str], pest_threat: Optional[str], weather_risk: Optional[str]) -> Dict[str, str]:
    crop_key = str(crop or "").lower()
    threat_key = str(pest_threat or "").lower()
    crop_rules = PEST_PLAYBOOK.get(crop_key, {})

    advisory = ""
    for key, value in crop_rules.items():
        if key in threat_key:
            advisory = value
            break
    if not advisory and "fung" in threat_key:
        advisory = "Fungal risk rises with humidity and leaf wetness. Scout early and follow local label guidance."
    if not advisory:
        advisory = "Scout the field this week and act only when pest pressure is visible or locally reported."

    if weather_risk:
        advisory = f"{advisory} Current weather risk: {weather_risk}."

    return {
        "crop": crop or "crop",
        "pest_threat": pest_threat or "general crop stress",
        "weather_risk": weather_risk or "not specified",
        "advisory": advisory,
    }
