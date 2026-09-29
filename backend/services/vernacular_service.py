"""Hyperlocal language and communication-complexity inference."""

from __future__ import annotations

from typing import Any, Dict, Optional


STATE_LANGUAGE_MAP = {
    "bihar": ("Hindi", "Maithili/Bhojpuri-influenced Hindi", "Devanagari"),
    "uttar pradesh": ("Hindi", "simple Hindi", "Devanagari"),
    "rajasthan": ("Hindi", "Hindi with rural Rajasthan phrasing", "Devanagari"),
    "madhya pradesh": ("Hindi", "simple Hindi", "Devanagari"),
    "telangana": ("Telugu", "Telangana Telugu", "Telugu"),
    "andhra pradesh": ("Telugu", "coastal/rayalaseema Telugu", "Telugu"),
    "tamil nadu": ("Tamil", "Tamil Nadu farmer Tamil", "Tamil"),
    "maharashtra": ("Marathi", "rural Marathi", "Devanagari"),
    "punjab": ("Punjabi", "Punjabi with Hindi fallback", "Gurmukhi"),
    "haryana": ("Hindi", "Haryanvi-influenced Hindi", "Devanagari"),
    "karnataka": ("Kannada", "rural Kannada", "Kannada"),
    "gujarat": ("Gujarati", "rural Gujarati", "Gujarati"),
    "west bengal": ("Bengali", "rural Bengali", "Bengali"),
}

SUPPORTED = {"Hindi", "Tamil", "Telugu", "Marathi", "English", "Punjabi"}


class VernacularService:
    """Infers the best farmer-facing language and message format."""

    def infer(self, farmer: Dict[str, Any]) -> Dict[str, Any]:
        state = _clean(farmer.get("state"))
        preferred = farmer.get("language")
        inferred, style, script = STATE_LANGUAGE_MAP.get(state, ("Hindi", "simple Indian farmer Hindi", "Devanagari"))

        language = _normalise_language(preferred) or inferred
        if language not in SUPPORTED:
            language = inferred if inferred in SUPPORTED else "Hindi"

        device = _clean(farmer.get("device_type"))
        literacy = _clean(farmer.get("literacy_level"))
        connectivity = _clean(farmer.get("connectivity"))

        keypad = device in {"keypad_phone", "feature_phone", "basic_phone"}
        low_literacy = literacy in {"low", "limited", "illiterate"}
        weak_network = connectivity in {"weak", "low", "offline", "2g"}

        complexity = "simple"
        if not low_literacy and not keypad and not weak_network:
            complexity = "moderate"
        if language == "English":
            complexity = "moderate"

        return {
            "language": language,
            "fallback_language": "Hindi" if language != "Hindi" else "English",
            "script": _script_for(language, script),
            "region_style": style,
            "complexity_level": complexity,
            "voice_first": bool(keypad or low_literacy),
            "sms_safe": bool(keypad or weak_network),
        }


def _clean(value: Optional[str]) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _normalise_language(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    lookup = {
        "hindi": "Hindi",
        "maithili": "Hindi",
        "bhojpuri": "Hindi",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "marathi": "Marathi",
        "english": "English",
        "punjabi": "Punjabi",
    }
    return lookup.get(_clean(value))


def _script_for(language: str, fallback: str) -> str:
    return {
        "Hindi": "Devanagari",
        "Tamil": "Tamil",
        "Telugu": "Telugu",
        "Marathi": "Devanagari",
        "Punjabi": "Gurmukhi",
        "English": "Latin",
    }.get(language, fallback)
