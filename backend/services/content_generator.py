"""OpenAI-backed content generation with language-pure local fallback."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from services.language_engine import LanguageEngine, compress_sms


class ContentGenerator:
    """Generates SMS, WhatsApp, voice script, and rich-media recommendations."""

    def __init__(self) -> None:
        self.language_engine = LanguageEngine()

    def generate(
        self,
        farmer_name: str = "Kisan",
        segment: str = "Medium",
        growth_stage: Optional[str] = None,
        crop: Optional[str] = None,
        campaign_product: Optional[str] = None,
        district: Optional[str] = None,
        days_until_harvest: Optional[float] = None,
        language: Optional[str] = None,
        channel: Optional[str] = None,
        vernacular: Optional[Dict[str, Any]] = None,
        rag_context: Optional[Dict[str, Any]] = None,
        pest_context: Optional[Dict[str, Any]] = None,
        urgency: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        vernacular = vernacular or {"language": language or "Hindi", "sms_safe": True}
        rag_context = rag_context or {"advisory_summary": ""}
        pest_context = pest_context or {}
        urgency = urgency or {"urgency_level": "medium"}

        if os.getenv("OPENAI_API_KEY"):
            generated = self._generate_with_openai(
                farmer_name, segment, growth_stage, crop, campaign_product, district,
                channel, vernacular, rag_context, pest_context, urgency
            )
            if generated:
                return generated

        return self._generate_local(
            farmer_name, segment, growth_stage, crop, campaign_product, district,
            channel, vernacular, rag_context, pest_context, urgency
        )

    def _generate_with_openai(
        self,
        farmer_name: str,
        segment: str,
        growth_stage: Optional[str],
        crop: Optional[str],
        product: Optional[str],
        district: Optional[str],
        channel: Optional[str],
        vernacular: Dict[str, Any],
        rag_context: Dict[str, Any],
        pest_context: Dict[str, Any],
        urgency: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        try:
            from openai import OpenAI
        except Exception:
            return None

        language = vernacular.get("language", "Hindi")
        prompt = f"""
Return strict JSON with keys: sms, whatsapp, voice_script, subject_line, cta_text,
recommended_media: {{type, topic, caption, video_script}}.
Use ONLY {language}. Do not mix Hindi, English, or transliterated filler unless {language} is English.
Use natural farmer phrasing for {vernacular.get('region_style')}.
Keep SMS under 160 characters. Voice script must be simple and spoken.
Farmer: {farmer_name}
District: {district}
Crop: {crop}
Growth stage: {growth_stage}
Pest: {pest_context.get('pest_threat')}
Weather: {pest_context.get('weather_risk')}
Product: {product}
Segment: {segment}
Channel: {channel}
Urgency: {urgency}
Agronomy evidence: {rag_context.get('advisory_summary')}
No dosage claims. Recommend local label-approved advice.
"""
        try:
            import json

            client = OpenAI()
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You write safe, language-pure agricultural campaign copy."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.35,
            )
            data = json.loads(response.choices[0].message.content)
            return self._shape_response(data, segment, vernacular, "openai")
        except Exception:
            return None

    def _generate_local(
        self,
        farmer_name: str,
        segment: str,
        growth_stage: Optional[str],
        crop: Optional[str],
        product: Optional[str],
        district: Optional[str],
        channel: Optional[str],
        vernacular: Dict[str, Any],
        rag_context: Dict[str, Any],
        pest_context: Dict[str, Any],
        urgency: Dict[str, Any],
    ) -> Dict[str, Any]:
        language = vernacular.get("language", "Hindi")
        messages = self.language_engine.build_messages(
            language=language,
            name=farmer_name or "Kisan",
            crop=crop or pest_context.get("crop"),
            pest=pest_context.get("pest_threat"),
            district=district,
            weather=pest_context.get("weather_risk"),
            product=product,
            sms_safe=bool(vernacular.get("sms_safe")),
        )
        crop_local = self.language_engine.localize_crop(language, crop)
        pest_local = self.language_engine.localize_term(language, pest_context.get("pest_threat"))
        media = self._media_recommendation(language, crop_local, pest_local, urgency.get("urgency_level"))

        data = {
            **messages,
            "subject_line": self._subject(language, crop_local, pest_local, urgency.get("urgency_level")),
            "recommended_media": media,
        }
        return self._shape_response(data, segment, vernacular, "local-language-engine")

    def _shape_response(self, data: Dict[str, Any], segment: str, vernacular: Dict[str, Any], mode: str) -> Dict[str, Any]:
        sms = compress_sms(data.get("sms") or data.get("whatsapp") or "", 160)
        whatsapp = data.get("whatsapp") or sms
        voice = data.get("voice_script") or whatsapp
        return {
            "primary_message": sms if vernacular.get("sms_safe") else whatsapp,
            "alternative_message": voice if vernacular.get("voice_first") else sms,
            "subject_line": data.get("subject_line") or "Crop advisory",
            "cta_text": data.get("cta_text") or "",
            "content_tips": [
                "SMS keeps one action for low-bandwidth users.",
                "WhatsApp includes richer advisory formatting for smartphone users.",
                "Voice script is generated for keypad or low-literacy farmers.",
            ],
            "language_note": f"{vernacular.get('language')} | {vernacular.get('region_style')}",
            "personalisation_level": {"Very High": "deep", "High": "high", "Medium": "moderate"}.get(segment, "basic"),
            "sms": sms,
            "whatsapp": whatsapp,
            "voice_script": voice,
            "generation_mode": mode,
            "recommended_media": data.get("recommended_media"),
            "audio_file": None,
        }

    def _media_recommendation(self, language: str, crop: str, pest: str, urgency: Optional[str]) -> Dict[str, str]:
        if language == "Telugu":
            caption = f"{crop} పంటను {pest} నుంచి కాపాడండి"
            video = f"{crop} పొలంలో {pest} లక్షణాలను ఎలా చూడాలో 20 సెకన్ల చిన్న వీడియో."
        elif language == "Tamil":
            caption = f"{crop} பயிரை {pest} அபாயத்திலிருந்து பாதுகாக்குங்கள்"
            video = f"{crop} வயலில் {pest} அறிகுறிகளை காணும் 20 விநாடி வீடியோ."
        elif language == "Marathi":
            caption = f"{crop} पिकाचे {pest} पासून संरक्षण करा"
            video = f"{crop} शेतात {pest} लक्षणे पाहण्याचा 20 सेकंदाचा व्हिडिओ."
        elif language == "English":
            caption = f"Protect {crop} from {pest}"
            video = f"20-second field video showing how to spot {pest} in {crop}."
        else:
            caption = f"{crop} को {pest} से बचाएं"
            video = f"{crop} खेत में {pest} के लक्षण पहचानने का 20 सेकंड वीडियो."
        return {
            "type": "infographic" if urgency != "high" else "short_video",
            "topic": f"{crop}_{pest}_prevention".replace(" ", "_").lower(),
            "caption": caption,
            "video_script": video,
        }

    def _subject(self, language: str, crop: str, pest: str, urgency: Optional[str]) -> str:
        if language == "English":
            return f"{crop}: {pest} advisory"
        if language == "Telugu":
            return f"{crop}: {pest} సలహా"
        if language == "Tamil":
            return f"{crop}: {pest} ஆலோசனை"
        if language == "Marathi":
            return f"{crop}: {pest} सल्ला"
        return f"{crop}: {pest} सलाह"
