"""Telemetry router for Open-Meteo weather, soil-test availability, and satellite NDVI."""

from __future__ import annotations

import logging
import math
from typing import Optional

import httpx
from fastapi import APIRouter, Query
from schemas import SatelliteContext, SoilHealthCard, WeatherContext
from services.earth_engine_service import get_satellite_telemetry as query_satellite_telemetry

logger = logging.getLogger("krishisetu.telemetry")

router = APIRouter(prefix="/api/telemetry", tags=["Environmental Telemetry"])


@router.get("/weather", response_model=WeatherContext, summary="Fetch agro-weather telemetry")
async def get_weather(
    lat: float = 23.47,
    lon: float = 88.55,
    location_label: Optional[str] = "Nadia, West Bengal",
):
    """
    Fetches real-time agro-meteorological data from Open-Meteo.
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain,wind_speed_10m&"
            f"daily=precipitation_sum&timezone=Asia%2FKolkata"
        )
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                daily = data.get("daily", {})
                observations = {
                    "temperature_c": current.get("temperature_2m"),
                    "relative_humidity_pct": current.get("relative_humidity_2m"),
                    "recent_rain_mm": current.get("rain"),
                    "wind_speed_kmh": current.get("wind_speed_10m"),
                }
                forecast = daily.get("precipitation_sum")
                if any(
                    not isinstance(value, (int, float)) or not math.isfinite(value)
                    for value in observations.values()
                ) or not isinstance(forecast, list) or not forecast or any(
                    not isinstance(value, (int, float)) or not math.isfinite(value)
                    for value in forecast
                ):
                    raise ValueError("Open-Meteo response did not contain complete numeric observations.")
                forecast_rain = sum(forecast)
                temp = observations["temperature_c"]
                rh = observations["relative_humidity_pct"]
                recent_rain = observations["recent_rain_mm"]
                wind = observations["wind_speed_kmh"]

                risk = (
                    "High fungal sporulation risk (RH > 82%)"
                    if rh > 80
                    else "Moderate fungal risk"
                )

                return WeatherContext(
                    available=True,
                    source=f"Open-Meteo Agro Station ({location_label})",
                    temperature_c=round(temp, 1),
                    relative_humidity_pct=round(rh, 1),
                    recent_rain_mm=round(recent_rain, 1),
                    rainfall_forecast_7d_mm=round(forecast_rain, 1),
                    wind_speed_kmh=round(wind, 1),
                    weather_condition="Recent rain reported" if recent_rain > 0 else "No recent rain reported",
                    microclimate_risk=risk,
                )
            logger.warning("Open-Meteo returned HTTP %s for weather telemetry.", resp.status_code)
    except Exception:
        logger.exception("Open-Meteo weather telemetry request failed.")

    return WeatherContext(
        available=False,
        source="Open-Meteo Agro-Meteorology API",
        reason="Weather telemetry is unavailable; no current observations were returned.",
    )


@router.get("/soil", response_model=SoilHealthCard, summary="Report soil-test availability")
def get_soil_health(
    state: str = "West Bengal",
    district: str = "Nadia",
):
    """Return an explicit unavailable state until a verified farmer-linked soil source exists."""
    return SoilHealthCard(
        available=False,
        reason="No farmer-specific soil-test measurements are currently available.",
    )


@router.get("/satellite", response_model=SatelliteContext, summary="Fetch Google Earth Engine Sentinel-2 telemetry")
def get_satellite_telemetry(
    latitude: Optional[float] = Query(None, ge=-90, le=90),
    longitude: Optional[float] = Query(None, ge=-180, le=180),
):
    if latitude is None or longitude is None:
        return SatelliteContext(
            available=False,
            reason="Farm coordinates are required for satellite telemetry.",
        )
    return query_satellite_telemetry(latitude, longitude)
