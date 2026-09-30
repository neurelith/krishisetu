"""
Google Gemini Multimodal AI & Contextual Reasoning Service for KrishiSetu.
Handles:
1. Multimodal Leaf Pathology Diagnostics using Gemini 2.5/Flash Vision.
2. Contextual advisory and Agronomic Insights from available crop, weather, satellite, and retrieved context.
3. Transparent Explainability Generation ("Why this recommendation?").
4. Vernacular Audio Speech Synthesis (gTTS).
Includes robust deterministic clinical protocols as a zero-crash safety net.
"""

from __future__ import annotations

import base64
import json
import logging
import math
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from gtts import gTTS
from schemas import (
    AdvisoryResponse,
    AgronomicInsight,
    AgronomicInsightInputs,
    AgronomicInsightsRequest,
    AgronomicInsightsResponse,
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

    def generate_agronomic_insights(
        self,
        context: AgronomicInsightsRequest,
    ) -> AgronomicInsightsResponse:
        """Explain supplied farm/weather/satellite context without inferring soil test results."""
        location_parts = [
            part.strip()
            for part in (context.location.district, context.location.state)
            if part and part.strip()
        ]
        location = ", ".join(location_parts) or "Location not provided"
        crop_name = (context.crop.name or "").strip()
        season = (context.crop.season or "").strip() or None
        satellite = context.satellite
        satellite_available = bool(
            satellite.available
            and satellite.ndvi is not None
            and math.isfinite(satellite.ndvi)
            and satellite.observation_date
        )
        weather = context.weather
        weather_available = bool(
            weather.available
            and weather.source.startswith("Open-Meteo Agro Station")
            and any(
                value is not None and math.isfinite(value)
                for value in (
                    weather.temperature_c,
                    weather.relative_humidity_pct,
                    weather.recent_rain_mm,
                    weather.rainfall_forecast_7d_mm,
                    weather.wind_speed_kmh,
                )
            )
        )
        input_status = AgronomicInsightInputs(
            weather_available=weather_available,
            satellite_available=satellite_available,
            soil_test_available=context.soil_test_available,
        )

        def unavailable(reason: str) -> AgronomicInsightsResponse:
            return AgronomicInsightsResponse(
                available=False,
                location=location,
                crop=crop_name or "Not provided",
                season=season,
                inputs=input_status,
                reason=reason,
            )

        stage = (context.crop.crop_stage or "").strip()
        if not crop_name or not stage:
            return unavailable("Enter the crop and its current growth stage to request agronomic insights.")
        if not self.client:
            return unavailable("Agronomic insights are unavailable because Gemini is not configured.")

        weather_facts = {
            "source": weather.source if weather_available else None,
            "temperature_c": weather.temperature_c if weather_available else None,
            "relative_humidity_pct": weather.relative_humidity_pct if weather_available else None,
            "recent_rain_mm": weather.recent_rain_mm if weather_available else None,
            "rainfall_forecast_7d_mm": weather.rainfall_forecast_7d_mm if weather_available else None,
            "wind_speed_kmh": weather.wind_speed_kmh if weather_available else None,
        }
        satellite_facts = {
            "source": satellite.source if satellite_available else None,
            "observation_date": satellite.observation_date if satellite_available else None,
            "ndvi": satellite.ndvi if satellite_available else None,
            "vegetation_status": satellite.vegetation_status if satellite_available else None,
        }
        facts = {
            "location": location,
            "coordinates": (
                {
                    "latitude": context.location.latitude,
                    "longitude": context.location.longitude,
                }
                if context.location.latitude is not None and context.location.longitude is not None
                else None
            ),
            "crop": crop_name,
            "variety": (context.crop.variety or "").strip() or None,
            "growth_stage": stage,
            "season": season,
            "weather_available": weather_available,
            "weather": weather_facts,
            "satellite_available": satellite_available,
            "satellite": satellite_facts,
            "soil_test_available": context.soil_test_available,
        }

        prompt = (
            "You are a cautious agricultural assistant. Use the supplied JSON facts only. "
            "Return JSON with exactly two non-empty string fields: crop_cycle and field_management. "
            "Give short, practical, general guidance for the stated crop and growth stage; season may be considered only if supplied. "
            "Use weather or satellite values only if their availability flag is true, and do not repeat or alter measurements. "
            "Do not infer location-specific facts, soil properties, nutrient deficiencies, pest presence, or crop condition from missing inputs. "
            "Do not invent citations, authorities, sources, or crop-calendar rules. "
            "Do not give fertilizer/pesticide rates, quantities, doses, or precise prescriptions. "
            "Do not claim this guidance comes from a government or research institution. "
            "State uncertainty implicitly by keeping guidance broad. Do not include numbers in either field.\n"
            f"FACTS JSON:\n{json.dumps(facts, ensure_ascii=False)}"
        )

        try:
            models = (
                "gemini-3.8-flash",
                "gemini-3.7-flash",
                "gemini-3.6-flash",
                "gemini-3.5-flash-lite",
            )
            transient_failures = []
            response = None
            for model in models:
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config={"response_mime_type": "application/json", "temperature": 0.2},
                    )
                    break
                except Exception as exc:
                    status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
                    try:
                        status_code = int(status_code)
                    except (TypeError, ValueError):
                        status_code = None
                    if status_code not in (429, 503):
                        raise
                    transient_failures.append(f"{model} (HTTP {status_code})")
                    logger.warning(
                        "Gemini agronomic insights model %s returned transient HTTP %s; trying the next model.",
                        model,
                        status_code,
                    )
            if response is None and transient_failures:
                return unavailable(
                    "Gemini models were temporarily unavailable or rate-limited "
                    f"({', '.join(transient_failures)}). No recommendations were generated."
                )
            if not response or not response.text:
                return unavailable(
                    "Gemini returned no agronomic insight content. No recommendations were generated."
                )
            try:
                parsed = json.loads(response.text)
            except json.JSONDecodeError:
                logger.warning("Gemini agronomic insight response was not valid JSON.")
                return unavailable(
                    "Gemini returned an unstructured response. No recommendations were generated."
                )
            guidance_fields = ("crop_cycle", "field_management")
            if not isinstance(parsed, dict) or set(parsed) != set(guidance_fields):
                logger.warning("Gemini agronomic insight response did not match the required fields.")
                return unavailable(
                    "Gemini response did not match the required insight structure. No recommendations were generated."
                )
            if any(
                not isinstance(parsed.get(field), str) or not parsed[field].strip()
                for field in guidance_fields
            ):
                logger.warning("Gemini agronomic insight response contained empty guidance.")
                return unavailable(
                    "Gemini response did not include usable crop-stage guidance. No recommendations were generated."
                )

            guidance = [parsed[field].strip() for field in guidance_fields]
            prohibited = re.compile(
                r"\d|@|%|https?://|\b(?:ICAR|DES|SHC|Soil Health Card|Matir Katha|"
                r"government|Ministry|Department|official|authority|research|study|"
                r"source|citation|according to|as per|kg|grams?|millilit(?:er|re)s?|"
                r"lit(?:er|re)s?|acre|hectare)\b",
                re.IGNORECASE,
            )
            soil_claim = re.compile(
                r"\b(?:soil|nutrient|nitrogen|phosphorus|potassium)\b.{0,50}"
                r"\b(?:deficien\w*|low|high|acidic|alkaline|shortage|lacks?)\b|"
                r"\b(?:deficien\w*|shortage|acidic|alkaline)\b.{0,50}"
                r"\b(?:soil|nutrient|nitrogen|phosphorus|potassium)\b",
                re.IGNORECASE,
            )
            if any(prohibited.search(text) or soil_claim.search(text) for text in guidance):
                logger.warning(
                    "Gemini agronomic insight response was rejected by citation, prescription, or soil-claim safety validation."
                )
                return unavailable(
                    "Gemini draft was rejected by safety validation because it included a possible unsupported citation, numeric prescription, or soil-status claim. No recommendations were returned."
                )

            if satellite_available:
                crop_condition = (
                    f"Sentinel-2 observation on {satellite.observation_date}: NDVI "
                    f"{satellite.ndvi:.3f}"
                    + (
                        f" ({satellite.vegetation_status})"
                        if satellite.vegetation_status
                        else ""
                    )
                    + ". NDVI describes vegetation reflectance, not soil nutrients or soil moisture."
                )
            else:
                crop_condition = (
                    "No usable Sentinel-2 observation is available; current crop condition "
                    "cannot be assessed from satellite data."
                )

            if weather_available:
                observed_weather = []
                if weather.temperature_c is not None:
                    observed_weather.append(f"{weather.temperature_c:g}°C")
                if weather.relative_humidity_pct is not None:
                    observed_weather.append(f"{weather.relative_humidity_pct:g}% relative humidity")
                if weather.recent_rain_mm is not None:
                    observed_weather.append(f"{weather.recent_rain_mm:g} mm recent rain")
                if weather.rainfall_forecast_7d_mm is not None:
                    observed_weather.append(f"{weather.rainfall_forecast_7d_mm:g} mm forecast over 7 days")
                weather_text = (
                    f"Open-Meteo reports {', '.join(observed_weather)}. "
                    "Consider these conditions when planning field work and water management."
                )
            else:
                weather_text = (
                    "Current weather data is unavailable; no weather-specific field guidance is included."
                )

            return AgronomicInsightsResponse(
                available=True,
                generated_at=datetime.now().astimezone().isoformat(timespec="seconds"),
                location=location,
                crop=crop_name,
                season=season,
                inputs=input_status,
                insights=[
                    AgronomicInsight(
                        type="crop_condition",
                        title="Current field condition",
                        text=crop_condition,
                    ),
                    AgronomicInsight(
                        type="weather",
                        title="Weather consideration",
                        text=weather_text,
                    ),
                    AgronomicInsight(
                        type="crop_cycle",
                        title="Crop-cycle guidance",
                        text=guidance[0],
                    ),
                    AgronomicInsight(
                        type="field_management",
                        title="Field and water management",
                        text=guidance[1],
                    ),
                    AgronomicInsight(
                        type="nutrient",
                        title="Nutrient guidance",
                        text=(
                            "No farmer-specific soil test is available, so soil N, P, K, pH, "
                            "EC, and organic-carbon status are unknown. Nutrient guidance is "
                            "general; obtain a soil test before making fertilizer adjustments."
                        ),
                    ),
                ],
            )
        except Exception as exc:
            status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
            logger.warning(
                "Gemini agronomic insights provider request failed (%s, status=%s).",
                type(exc).__name__,
                status_code,
            )
            if status_code == 503:
                reason = "Gemini is temporarily unavailable or overloaded. No recommendations were generated."
            elif status_code in (401, 403):
                reason = "Gemini authorization failed. Check the existing server-side Gemini configuration."
            elif status_code == 404:
                reason = "The configured Gemini model is unavailable. No recommendations were generated."
            else:
                reason = "Gemini could not complete the agronomic insights request. No recommendations were generated."
            return unavailable(
                reason
            )

    def generate_contextual_advisory(
        self,
        context: FarmContext,
        rag_sources: List[Dict[str, Any]],
    ) -> AdvisoryResponse:
        """
        Synthesizes a multi-factor regenerative advisory by fusing:
        - Diagnosis
        - Soil-test status (no farmer-specific measurements by default)
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
        if context.weather.available and context.weather.source.startswith("Open-Meteo Agro Station"):
            weather_summary = (
                f"source: {context.weather.source}; temperature={context.weather.temperature_c}; "
                f"relative humidity={context.weather.relative_humidity_pct}; "
                f"recent rain={context.weather.recent_rain_mm}; "
                f"7-day rain forecast={context.weather.rainfall_forecast_7d_mm}; "
                f"condition={context.weather.weather_condition}"
            )
        else:
            weather_summary = "unavailable; no weather measurements may be inferred"

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
                "SOIL DATA: No farmer-specific soil-test measurements are available. "
                "Do not infer soil properties, nutrient status, or deficiencies.\n"
                f"WEATHER DATA: {weather_summary}\n"
                f"SATELLITE DATA: {satellite_summary}. Do not use unavailable satellite data as evidence. NDVI is vegetation reflectance, not soil moisture.\n"
                "No farmer-specific soil test is available. Do not infer soil conditions or provide soil-specific nutrient/fertilizer recommendations; advise soil testing before adjustments. "
                "Do not recommend a nutrient treatment or fertilizer dose without verified soil-test evidence.\n"
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
