"""
Crop and leaf disease diagnostics router powered by Google Gemini Multimodal Vision.
"""

from __future__ import annotations

import logging
from typing import Optional

import asyncio

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import ValidationError
from schemas import DiagnosisResult, FarmContext
from services.gemini_service import get_gemini_service

logger = logging.getLogger("krishisetu.diagnose")

router = APIRouter(prefix="/api", tags=["Leaf Diagnostics"])


@router.post("/diagnose", response_model=DiagnosisResult, summary="Diagnose crop/leaf disease using Gemini Multimodal Vision")
async def diagnose_leaf_image(
    image: UploadFile = File(..., description="Crop/leaf photograph"),
    crop_hint: Optional[str] = Form("Rice", description="Crop name hint (e.g. Rice, Wheat, Cotton)"),
    farm_context: Optional[str] = Form(None, description="Existing FarmContext JSON used to contextualize diagnosis"),
):
    """
    Analyzes an uploaded leaf image using Google Gemini Multimodal Vision.
    Returns structured pathology assessment including condition, confidence, symptoms, and immediate bio-action.
    """
    try:
        context = FarmContext.model_validate_json(farm_context) if farm_context else None
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail="Invalid FarmContext payload.") from exc

    try:
        image_bytes = await image.read(10 * 1024 * 1024 + 1)
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Uploaded image file is empty.")
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller.")

        mime_type = image.content_type or "image/jpeg"
        if mime_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise HTTPException(status_code=415, detail="Upload a JPEG, PNG, or WebP image.")

        service = get_gemini_service()
        # Gemini call + gTTS are blocking (sync SDK) — keep them off the event loop.
        result = await asyncio.to_thread(
            service.diagnose_crop_disease,
            image_bytes=image_bytes,
            mime_type=mime_type,
            crop_hint=crop_hint,
            farm_context=context,
        )
        return result
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Error during leaf diagnosis: %s", exc)
        raise HTTPException(status_code=500, detail=f"Diagnostic analysis error: {str(exc)}")
