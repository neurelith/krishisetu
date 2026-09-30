"""Agronomic insights endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from schemas import AgronomicInsightsRequest, AgronomicInsightsResponse
from services.gemini_service import get_gemini_service

router = APIRouter(prefix="/api/agronomy", tags=["Agronomic Insights"])


@router.post("/insights", response_model=AgronomicInsightsResponse)
def get_agronomic_insights(context: AgronomicInsightsRequest):
    """Synthesize supplied crop, weather, and satellite context without soil-test claims."""
    return get_gemini_service().generate_agronomic_insights(context)
