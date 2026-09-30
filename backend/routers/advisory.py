"""
Contextual Regenerative Advisory router powered by Google Gemini and ICAR RAG.
"""

from __future__ import annotations

import logging
from fastapi import APIRouter
from schemas import AdvisoryResponse, FarmContext
from services.gemini_service import get_gemini_service
from services.rag_service import RagService

logger = logging.getLogger("krishisetu.advisory")

router = APIRouter(prefix="/api", tags=["Regenerative Advisory"])
_rag_service = None


def _get_rag():
    global _rag_service
    if _rag_service is None:
        _rag_service = RagService()
    return _rag_service


@router.post("/advisory", response_model=AdvisoryResponse, summary="Generate multi-factor contextual regenerative agro-advisory")
async def generate_advisory(context: FarmContext):
    """
    Fuses unified farm context (Leaf Diagnosis + Weather + Soil Health + Satellite NDVI)
    with retrieved ICAR/FAO agronomic guidance using Google Gemini to produce an actionable,
    regenerative advisory with transparent explainability and Indic audio playback.
    """
    try:
        rag = _get_rag()
        rag_result = rag.retrieve(context, k=3)
        sources = rag_result.get("sources", [])

        gemini = get_gemini_service()
        advisory = gemini.generate_contextual_advisory(context, sources)
        return advisory
    except Exception as exc:
        logger.error("Error generating contextual advisory: %s", exc)
        return get_gemini_service().unavailable_contextual_advisory(context)
