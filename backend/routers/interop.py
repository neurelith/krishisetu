"""
Cross-State Interoperability & Federated Outbreak Router for KrishiSetu.
Enables heterogeneous state portals (e.g. West Bengal Matir Katha vs Bihar DBT Krishi)
to normalize into the open DPG FarmContext standard and share trans-border pest alerts.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from schemas import (
    FarmContext,
    OutbreakAlert,
    StateNormalizationRequest,
    StateNormalizationResponse,
)
from services.state_adapters import (
    BiharAdapter,
    DynamicStateAdapter,
    WestBengalAdapter,
    get_outbreak_engine,
)

logger = logging.getLogger("krishisetu.interop")

router = APIRouter(prefix="/api/interop", tags=["Cross-State Interoperability"])


@router.post("/normalize", response_model=StateNormalizationResponse, summary="Normalize state-specific payload to DPG standard")
def normalize_state_payload(request: StateNormalizationRequest):
    """
    Accepts raw state-specific JSON (e.g. West Bengal Matir Katha Bengali schema, Bihar DBT Krishi Hindi schema,
    or custom third-party state with declarative mapping rules) and maps it into the standardized open FarmContext v1.0 contract.
    """
    state = request.state_origin.lower()
    raw = request.raw_payload

    if request.custom_rules:
        context, mappings, notes = DynamicStateAdapter.normalize(request.state_origin, raw, request.custom_rules)
        source = f"Declarative Dynamic Adapter ({request.state_origin})"
    elif "bengal" in state or "wb" in state:
        context, mappings, notes = WestBengalAdapter.normalize(raw)
        source = "West Bengal Department of Agriculture (Matir Katha)"
    elif "bihar" in state or "br" in state:
        context, mappings, notes = BiharAdapter.normalize(raw)
        source = "Bihar Department of Agriculture (DBT Kisan Panjikaran)"
    elif "odisha" in state or "or" in state:
        odisha_rules = {
            "chasa_nama": "farmer.name",
            "zilla": "location.district",
            "dhan_kism": "crop.variety",
            "mrutika_ph": "soil_health.ph",
            "sar_n": "soil_health.nitrogen_kg_ha",
            "ardrata": "weather.relative_humidity_pct",
        }
        context, mappings, notes = DynamicStateAdapter.normalize("Odisha", raw, odisha_rules)
        source = "Odisha Department of Agriculture (Krushak Odisha Portal)"
    else:
        context, mappings, notes = DynamicStateAdapter.normalize(request.state_origin, raw, {})
        source = f"Generic DPG Adapter ({request.state_origin})"

    return StateNormalizationResponse(
        state_origin=request.state_origin,
        source_schema_detected=source,
        normalized_context=context,
        field_mappings_applied=mappings,
        transformation_notes=notes,
    )


@router.get("/sample-payload/{state}", summary="Get sample raw state payload for testing")
def get_sample_state_payload(state: str) -> Dict[str, Any]:
    """Provides representative raw state payloads for live UI demonstration."""
    s = state.lower()
    if "bengal" in s or "wb" in s:
        return {
            "state_origin": "west_bengal",
            "source_portal": "Matir Katha (মাটির কথা) - Government of West Bengal",
            "krisak_id": "IN-WB-NAD-0042",
            "krisak_naam": "সুভাষ মন্ডল (Subhash Mondal)",
            "mobile_no": "+919876543210",
            "bhasa": "bn",
            "jela": "Nadia",
            "block": "Nakashipara",
            "mouza_gram": "Bethuadahari",
            "latitude": 23.47,
            "longitude": 88.55,
            "fasal": "Rice (Aman Dhan)",
            "fasaler_jaat": "Swarna-Sub1",
            "mousom": "Kharif",
            "fasaler_dhoron": "Tillering to Panicle Initiation",
            "bopon_tarikh": "2026-07-12",
            "bopon_din": 78,
            "matir_card_no": "WB-MK-2026-9041",
            "sar_n": 185.0,
            "sar_p": 14.2,
            "sar_k": 160.0,
            "jaiba_carbon": 0.42,
            "matir_p_h": 5.8,
            "torit_poribahita": 0.35,
            "abohawa_tapanmatra": 31.8,
            "abohawa_ardrata": 86.0,
            "bristi_24h": 18.5,
            "bristi_purbabhash_7d": 54.0,
            "bataser_goti": 14.2,
            "abohawar_obostha": "Humid / Active Showers",
        }
    elif "odisha" in s or "or" in s:
        return {
            "state_origin": "odisha",
            "source_portal": "Krushak Odisha (କୃଷକ ଓଡ଼ିଶା) - Department of Agriculture & FE",
            "chasa_id": "OD-BHD-2026-3391",
            "chasa_nama": "ବିଶ୍ୱନାଥ ଦାସ (Biswanath Das)",
            "zilla": "Bhadrak",
            "block_nama": "Dhamnagar",
            "latitude": 20.91,
            "longitude": 86.51,
            "mukhya_fasal": "Rice (Dhan)",
            "dhan_kism": "Pooja (CR-Dhan 300)",
            "mrutika_ph": 6.1,
            "sar_n": 178.0,
            "jaiba_angara_pct": 0.45,
            "ardrata": 83.0,
            "tapamatra": 31.2,
        }
    else:
        return {
            "state_origin": "bihar",
            "source_portal": "DBT Agriculture (प्रत्यक्ष लाभ अंतरण) - Government of Bihar",
            "kisan_panjikaran_sankhya": "BR-DBT-2026-7841",
            "kisan_ka_naam": "रामेश्वर प्रसाद यादव (Rameshwar Yadav)",
            "durkhas_sankhya": "+919431209876",
            "bhasha": "hi",
            "jila": "Purnia",
            "prakhand": "Kasba",
            "panchayat_gram": "Sabdalpur",
            "latitude": 25.77,
            "longitude": 87.47,
            "mukhya_fasal": "Rice (Dhan/Paddy)",
            "fasal_kism": "MTU-7029 (Swarna)",
            "mausam": "Kharif",
            "fasal_awastha": "Vegetative / Maximum Tillering",
            "buwai_tithi": "2026-07-08",
            "buwai_din": 82,
            "mrida_swasthya_card": "BR-SHC-2026-4402",
            "nitrogen_matra": 192.0,
            "phosphorus_matra": 16.5,
            "potash_matra": 175.0,
            "mitti_carbon_pct": 0.38,
            "mitti_ph": 7.4,
            "vidyut_chalakta": 0.40,
            "tapman": 32.4,
            "nami_pratishat": 84.0,
            "pichle_24_ghante_varsha": 12.0,
            "varsha_purvanuman_7d": 45.0,
            "hawa_ki_gati": 12.8,
            "mausam_sthiti": "Humid / Partly Cloudy",
        }


@router.get("/schema", summary="Export open Digital Public Good FarmContext schema")
def get_dpg_schema():
    """Returns JSON Schema specification for FarmContext v1.0."""
    return FarmContext.model_json_schema()


@router.get("/telemetry", response_model=List[OutbreakAlert], summary="Get regional outbreak telemetry and trans-border alerts")
def get_outbreak_telemetry():
    """Returns active regional pest and disease outbreak vectors across border corridors."""
    engine = get_outbreak_engine()
    return engine.get_all_alerts()


@router.post("/simulate-outbreak", response_model=OutbreakAlert, summary="Simulate dynamic cross-state outbreak event")
def simulate_outbreak_event(
    pest_name: str = "Brown Plant Hopper (Nilaparvata lugens)",
    origin_state: str = "Bihar",
    origin_district: str = "Katihar",
    affected_crop: str = "Rice (Paddy)",
    severity: str = "High Risk",
):
    """Simulates an outbreak in a border district and immediately broadcasts early-warning alert to neighboring state."""
    engine = get_outbreak_engine()
    alert = engine.inject_outbreak_report(pest_name, origin_state, origin_district, affected_crop, severity)
    return alert
