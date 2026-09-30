"""
Google Gemini Multimodal AI & Contextual Reasoning Service for KrishiSetu.
Handles:
1. Multimodal Leaf Pathology Diagnostics using Gemini 2.5/Flash Vision.
2. Contextual Regenerative Advisory Synthesis (fusing Leaf Pathology + Soil Health Card + Weather + Satellite NDVI + ICAR RAG).
3. Transparent Explainability Generation ("Why this recommendation?").
4. Vernacular Audio Speech Synthesis (gTTS).
Includes robust deterministic clinical protocols as a zero-crash safety net.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from gtts import gTTS
from schemas import (
    AdvisoryResponse,
    DiagnosisResult,
    ExplainabilityEvidence,
    FarmContext,
    RegenerativeAction,
)

logger = logging.getLogger("krishisetu.gemini")

AUDIO_DIR = Path(__file__).resolve().parent.parent / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


class GeminiAgriService:
    """Manages Google Gemini Multimodal Vision and Contextual Reasoning."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Google GenAI client initialized successfully.")
            except Exception as exc:
                logger.warning("Failed to initialize Google GenAI client: %s", exc)

    def diagnose_crop_disease(
        self,
        image_bytes: bytes,
        mime_type: str = "image/jpeg",
        crop_hint: Optional[str] = "Rice",
        farm_context: Optional[FarmContext] = None,
    ) -> DiagnosisResult:
        """
        Analyzes a crop/leaf image using Gemini Multimodal Vision.
        Extracts structured pathology assessment with confidence, symptoms, and severity.
        """
        if not self.client:
            return self._unavailable_diagnosis("Gemini is not configured. Add GEMINI_API_KEY to enable image diagnosis.")

        try:
            from google.genai import types

            context_details = "No additional farm context provided."
            if farm_context:
                context_details = (
                    f"Crop: {farm_context.crop.name}; variety: {farm_context.crop.variety or 'not provided'}; "
                    f"growth stage: {farm_context.crop.crop_stage}; "
                    f"location: {farm_context.location.district}, {farm_context.location.state}; "
                    f"preferred language: {farm_context.farmer.preferred_language}."
                )

            prompt = (
                "You are an agricultural image assessment assistant. Do not claim ICAR affiliation.\n"
                f"Inspect this image. Farmer-provided context: {context_details}\n"
                f"Crop hint: {crop_hint or 'not provided'}. Use context only to narrow possibilities; do not assume a disease from the crop.\n"
                "If the image is not a plant/crop, set is_valid_crop_image=false and provide a rejection_reason. "
                "If it is a plant but the image or evidence is insufficient, set diagnosis_status='uncertain', describe only visible observations, "
                "and do not name a disease or recommend treatment. Only use diagnosis_status='complete' when a disease/condition is visibly supported.\n"
                "Respond ONLY with JSON containing diagnosis_status ('complete' or 'uncertain'), is_valid_crop_image, rejection_reason, "
                "condition_detected, scientific_name, confidence (0 to 1), severity, symptoms (array), affected_part, "
                "and immediate_bio_action. Use an empty symptoms array and no treatment recommendation when uncertain."
            )

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )

            if not response or not response.text:
                return self._unavailable_diagnosis("Gemini returned no analyzable result. Try a clearer crop photo.")

            parsed = json.loads(response.text)
            is_valid = parsed.get("is_valid_crop_image")
            if not isinstance(is_valid, bool):
                raise ValueError("Gemini response omitted image validity.")

            if not is_valid:
                return DiagnosisResult(
                    diagnosis_status="complete",
                    is_valid_crop_image=False,
                    rejection_reason=parsed.get("rejection_reason") or "This image does not appear to show a crop or plant. Please try a clear crop photo.",
                    condition_detected="Non-Crop Image Detected",
                    scientific_name=None,
                    confidence=0.0,
                    severity="Unknown",
                    symptoms=[],
                    affected_part="N/A",
                    immediate_bio_action="Upload a clear crop image to request an assessment.",
                    model_used="gemini-2.5-flash",
                )

            required_fields = ("condition_detected", "confidence", "severity", "symptoms", "affected_part", "immediate_bio_action")
            if any(field not in parsed for field in required_fields):
                raise ValueError("Gemini response was missing diagnosis fields.")

            status = parsed.get("diagnosis_status", "complete")
            if status not in {"complete", "uncertain"}:
                raise ValueError("Gemini returned an unsupported diagnosis status.")
            confidence = float(parsed["confidence"])

            if status == "uncertain" or confidence < 0.5:
                return DiagnosisResult(
                    diagnosis_status="uncertain",
                    is_valid_crop_image=True,
                    rejection_reason="The image does not provide enough visual evidence for a reliable diagnosis.",
                    condition_detected="Uncertain diagnosis",
                    scientific_name=None,
                    confidence=confidence,
                    severity="Unknown",
                    symptoms=parsed["symptoms"] if isinstance(parsed["symptoms"], list) else [],
                    affected_part=str(parsed["affected_part"] or "Unclear"),
                    immediate_bio_action="No treatment recommendation is available. Retake a clear image and consult a local agricultural expert.",
                    model_used="gemini-2.5-flash",
                )

            return DiagnosisResult(
                diagnosis_status="complete",
                is_valid_crop_image=True,
                rejection_reason=None,
                condition_detected=str(parsed["condition_detected"]),
                scientific_name=parsed.get("scientific_name"),
                confidence=confidence,
                severity=str(parsed["severity"]),
                symptoms=parsed["symptoms"],
                affected_part=str(parsed["affected_part"]),
                immediate_bio_action=str(parsed["immediate_bio_action"]),
                model_used="gemini-2.5-flash",
            )
        except Exception as exc:
            logger.warning("Gemini multimodal diagnosis failed: %s", exc)
            return self._unavailable_diagnosis("Gemini could not analyze this image. Check the connection or try a clearer crop photo.")

    @staticmethod
    def _unavailable_diagnosis(message: str) -> DiagnosisResult:
        return DiagnosisResult(
            diagnosis_status="unavailable",
            is_valid_crop_image=False,
            rejection_reason=message,
            condition_detected="Diagnosis unavailable",
            scientific_name=None,
            confidence=0.0,
            severity="Unknown",
            symptoms=[],
            affected_part="Unknown",
            immediate_bio_action="No disease diagnosis or treatment recommendation is available.",
            model_used="unavailable",
        )

    def generate_contextual_advisory(
        self,
        context: FarmContext,
        rag_sources: List[Dict[str, Any]],
    ) -> AdvisoryResponse:
        """
        Synthesizes a multi-factor regenerative advisory by fusing:
        - Diagnosis
        - Soil Health Card metrics
        - Weather telemetry
        - Satellite NDVI
        - ICAR/FAO RAG knowledge
        """
        advisory_id = f"ADV-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        preferred_lang = context.farmer.preferred_language or "bn"
        crop_name = context.crop.name
        condition = context.diagnosis.condition_detected if context.diagnosis else "Preventive Health Monitoring"
        severity = context.diagnosis.severity if context.diagnosis else "Low"
        if context.satellite.available:
            satellite_summary = (
                f"available from {context.satellite.source} on {context.satellite.observation_date}: "
                f"NDVI={context.satellite.ndvi} ({context.satellite.vegetation_status}); "
                f"clear pixels={context.satellite.clear_pixel_pct}%"
            )
        else:
            satellite_summary = f"unavailable: {context.satellite.reason or 'no usable observation'}"

        if not self.client:
            return self.unavailable_contextual_advisory(context)

        try:
            rag_summary = "\n".join([f"- [{s.get('topic')}]: {s.get('text')}" for s in rag_sources[:3]])
            prompt = (
                f"You are an agricultural advisory assistant. Do not claim government or institutional affiliation.\n"
                f"Synthesize a localized advisory based on this farm context:\n\n"
                f"FARMER: {context.farmer.name} | District: {context.location.district}, {context.location.state}\n"
                f"CROP: {crop_name} ({context.crop.variety}) | Stage: {context.crop.crop_stage}\n"
                f"DIAGNOSIS: {condition} ({severity})\n"
                f"SOIL DATA (source: {context.soil_health.source}): N={context.soil_health.nitrogen_kg_ha} kg/ha, P={context.soil_health.phosphorus_kg_ha} kg/ha, "
                f"K={context.soil_health.potassium_kg_ha} kg/ha, Organic Carbon={context.soil_health.organic_carbon_pct}%, pH={context.soil_health.ph}\n"
                f"WEATHER (source: {context.weather.source}): Temp={context.weather.temperature_c}°C, Relative Humidity={context.weather.relative_humidity_pct}%, "
                f"7-Day Rain Forecast={context.weather.rainfall_forecast_7d_mm}mm, Risk={context.weather.microclimate_risk}\n"
                f"SATELLITE DATA: {satellite_summary}. Do not use unavailable satellite data as evidence. NDVI is vegetation reflectance, not soil moisture.\n"
                "Treat any soil or weather source marked as a sample baseline as unavailable.\n"
                f"RETRIEVED KNOWLEDGE:\n{rag_summary}\n\n"
                f"TARGET LANGUAGE: {preferred_lang}.\n"
                "Return status='uncertain' with no recommendations if the context does not support safe, specific advice. "
                "Otherwise return status='success' and recommendations supported by the diagnosis and retrieved knowledge. "
                "Do not invent measurements, sources, or crop-specific treatment details.\n"
                "Output ONLY JSON with status ('success' or 'uncertain'), non-empty summary_advisory, non-empty summary_advisory_en, "
                "actions (non-empty array with category, title, description, urgency, cost_level, expected_outcome), "
                "soil_conditioning_steps (array), preventive_cultural_practices (array), and explainability "
                "(non-empty array with factor, observation, impact_on_decision)."
            )

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json", "temperature": 0.25},
            )
            if not response or not response.text:
                raise ValueError("Gemini returned no advisory content.")

            parsed = json.loads(response.text)
            if not isinstance(parsed, dict):
                raise ValueError("Gemini advisory response was not a JSON object.")
            status = parsed.get("status", "success")
            if status == "uncertain":
                return self.unavailable_contextual_advisory(context, status="uncertain")
            if status != "success":
                raise ValueError("Gemini returned an unsupported advisory status.")

            required_fields = (
                "summary_advisory",
                "summary_advisory_en",
                "actions",
                "soil_conditioning_steps",
                "preventive_cultural_practices",
                "explainability",
            )
            if any(field not in parsed for field in required_fields):
                raise ValueError("Gemini advisory response omitted required fields.")
            if not isinstance(parsed["summary_advisory"], str) or not parsed["summary_advisory"].strip():
                raise ValueError("Gemini advisory summary was empty.")
            if not isinstance(parsed["summary_advisory_en"], str) or not parsed["summary_advisory_en"].strip():
                raise ValueError("Gemini English advisory summary was empty.")
            if not isinstance(parsed["actions"], list) or not parsed["actions"]:
                raise ValueError("Gemini advisory did not contain actionable recommendations.")
            if not isinstance(parsed["explainability"], list) or not parsed["explainability"]:
                raise ValueError("Gemini advisory did not contain supporting evidence.")
            for steps_field in ("soil_conditioning_steps", "preventive_cultural_practices"):
                if not isinstance(parsed[steps_field], list):
                    raise ValueError(f"Gemini advisory field {steps_field} was not an array.")
            action_fields = {"category", "title", "description", "urgency", "cost_level", "expected_outcome"}
            if any(not isinstance(action, dict) or not action_fields.issubset(action) for action in parsed["actions"]):
                raise ValueError("Gemini advisory contained an incomplete action.")

            actions = [RegenerativeAction(**action) for action in parsed["actions"]]
            explain = [ExplainabilityEvidence(**evidence) for evidence in parsed["explainability"]]
            audio_file = self.synthesize_speech(
                parsed["summary_advisory"],
                lang=preferred_lang,
                advisory_id=advisory_id,
            )

            return AdvisoryResponse(
                status="success",
                advisory_id=advisory_id,
                generated_at=timestamp,
                crop_name=crop_name,
                stage=context.crop.crop_stage,
                condition_assessed=condition,
                severity=severity,
                summary_advisory=parsed["summary_advisory"],
                summary_advisory_en=parsed["summary_advisory_en"],
                actions=actions,
                soil_conditioning_steps=parsed["soil_conditioning_steps"],
                preventive_cultural_practices=parsed["preventive_cultural_practices"],
                explainability=explain,
                rag_sources=rag_sources[:3],
                audio_url=f"/audio/{audio_file}" if audio_file else None,
                language=preferred_lang,
            )
        except Exception as exc:
            logger.warning("Gemini contextual advisory failed: %s", exc)
            return self.unavailable_contextual_advisory(context)

    @staticmethod
    def unavailable_contextual_advisory(
        context: FarmContext,
        status: str = "unavailable",
    ) -> AdvisoryResponse:
        preferred_lang = context.farmer.preferred_language or "bn"
        if status == "uncertain":
            messages = {
                "bn": "প্রদত্ত তথ্য থেকে নির্ভরযোগ্য পরামর্শ তৈরি করা যায়নি। কোনো চিকিৎসা সুপারিশ দেওয়া হচ্ছে না।",
                "hi": "दी गई जानकारी से विश्वसनीय सलाह नहीं बन सकी। कोई उपचार सुझाव नहीं दिया जा रहा है।",
                "en": "The available context is insufficient for reliable advice. No treatment recommendations are available.",
            }
        else:
            status = "unavailable"
            messages = {
                "bn": "পরামর্শ পরিষেবা এই মুহূর্তে উপলভ্য নয়। কোনো চিকিৎসা সুপারিশ দেওয়া হচ্ছে না।",
                "hi": "सलाह सेवा इस समय उपलब्ध नहीं है। कोई उपचार सुझाव नहीं दिया जा रहा है।",
                "en": "The advisory service is unavailable. No treatment recommendations are available.",
            }
        message = messages.get(preferred_lang, messages["en"])
        return AdvisoryResponse(
            status=status,
            advisory_id=f"ADV-{uuid.uuid4().hex[:8].upper()}",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            crop_name=context.crop.name,
            stage=context.crop.crop_stage,
            condition_assessed=context.diagnosis.condition_detected if context.diagnosis else "Unable to assess",
            severity=context.diagnosis.severity if context.diagnosis else "Unknown",
            summary_advisory=message,
            summary_advisory_en="No treatment recommendations are available.",
            actions=[],
            soil_conditioning_steps=[],
            preventive_cultural_practices=[],
            explainability=[],
            rag_sources=[],
            audio_url=None,
            language=preferred_lang,
        )

    def synthesize_speech(self, text: str, lang: str = "bn", advisory_id: str = "adv") -> Optional[str]:
        """Synthesizes text to regional Indic voice audio using gTTS."""
        if not text:
            return None
        try:
            filename = f"advisory_{advisory_id}_{lang}.mp3"
            filepath = AUDIO_DIR / filename
            if not filepath.exists():
                gtts_lang = "bn" if lang == "bn" else ("hi" if lang == "hi" else "en")
                tts = gTTS(text=text[:350], lang=gtts_lang, slow=False)
                tts.save(str(filepath))
            return filename
        except Exception as exc:
            logger.warning("gTTS speech synthesis failed: %s", exc)
            return None

_service_instance = None


def get_gemini_service() -> GeminiAgriService:
    global _service_instance
    if _service_instance is None:
        _service_instance = GeminiAgriService()
    return _service_instance
