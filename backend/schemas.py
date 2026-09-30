"""
Pydantic schemas for the KrishiSetu (कृषि-सेतु) Interoperable Digital Agriculture Platform.
Defines contracts for Multimodal Leaf Diagnostics, Grounded Regenerative Advisories,
Environmental Telemetry (Weather, Soil Health Card, Sentinel-2 NDVI), and Cross-State Interoperability.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# 1. Digital Public Good: Standard FarmContext Schema (v1.0)
# ============================================================================

class FarmerIdentity(BaseModel):
    farmer_id: Optional[str] = Field("IN-WB-NAD-0042", description="Unique farmer ID")
    name: Optional[str] = Field("Subhash Mondal", description="Farmer full name")
    phone: Optional[str] = Field("+919876543210", description="Contact phone")
    preferred_language: str = Field("bn", description="Preferred Indic language: 'bn', 'hi', 'en', 'te', 'mr'")
    literacy_profile: str = Field("audio_preferred", description="'text_preferred', 'audio_preferred'")


class GeoLocation(BaseModel):
    state: str = Field("West Bengal", description="State name")
    district: str = Field("Nadia", description="District name")
    block_tehsil: Optional[str] = Field("Nakashipara", description="Block / Tehsil / Mandal")
    village: Optional[str] = Field("Bethuadahari", description="Village name")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")


class CropDetails(BaseModel):
    name: str = Field("Rice (Paddy)", description="Crop name (e.g. Rice, Wheat, Cotton, Maize)")
    variety: Optional[str] = Field("Swarna-Sub1", description="Crop cultivar / variety")
    season: Optional[str] = Field("Kharif", description="Kharif, Rabi, Zaid")
    crop_stage: str = Field("Tillering to Panicle Initiation", description="Active physiological growth stage")
    sowing_date: Optional[str] = Field("2026-07-12", description="Sowing date (YYYY-MM-DD)")
    days_since_sowing: Optional[int] = Field(78, description="Days elapsed since sowing")


class SoilHealthCard(BaseModel):
    source: str = Field("Government of India Soil Health Card (SHC)", description="Origin registry")
    card_id: Optional[str] = Field("SHC-WB-2026-8819", description="Soil health card identifier")
    lab_test_cert: str = Field("ICAR-NBSS-LUP/2026/WB-089", description="Accredited lab certificate ref")
    nitrogen_kg_ha: float = Field(185.0, description="Available Nitrogen (N) in kg/ha")
    phosphorus_kg_ha: float = Field(14.2, description="Available Phosphorus (P) in kg/ha")
    potassium_kg_ha: float = Field(160.0, description="Available Potassium (K) in kg/ha")
    organic_carbon_pct: float = Field(0.42, description="Organic Carbon percentage (OC %)")
    ph: float = Field(5.8, description="Soil pH level (acidic < 6.5, alkaline > 7.5)")
    electrical_conductivity_ds_m: Optional[float] = Field(0.35, description="Electrical Conductivity (dS/m)")
    deficiencies: List[str] = Field(
        default_factory=lambda: ["Nitrogen Deficient (<280 kg/ha)", "Low Organic Carbon (<0.5%)", "Mildly Acidic pH"],
        description="Identified soil deficiencies"
    )


class WeatherContext(BaseModel):
    source: str = Field("Open-Meteo Agro-Meteorology API", description="Weather data provider")
    temperature_c: float = Field(31.8, description="Current ambient temperature in Celsius")
    relative_humidity_pct: float = Field(86.0, description="Relative humidity percentage")
    rainfall_last_24h_mm: float = Field(18.5, description="Rainfall in the last 24 hours (mm)")
    rainfall_forecast_7d_mm: float = Field(54.0, description="Projected 7-day cumulative precipitation (mm)")
    wind_speed_kmh: float = Field(14.2, description="Wind speed (km/h)")
    weather_condition: str = Field("Humid / Frequent Showers", description="Meteorological overview")
    microclimate_risk: str = Field("High fungal sporulation risk due to RH > 85% and cloudy conditions", description="Microclimate disease risk")


class SatelliteContext(BaseModel):
    available: bool = Field(False, description="Whether a usable satellite observation is available")
    source: str = Field("Google Earth Engine / Sentinel-2", description="Satellite imagery provider")
    observation_date: Optional[str] = Field(None, description="Acquisition date of the selected Sentinel-2 image")
    latitude: Optional[float] = Field(None, description="Farm latitude used for the observation")
    longitude: Optional[float] = Field(None, description="Farm longitude used for the observation")
    ndvi: Optional[float] = Field(None, description="Cloud-masked Normalized Difference Vegetation Index")
    b4_reflectance: Optional[float] = Field(None, description="Mean Sentinel-2 B4 surface reflectance")
    b8_reflectance: Optional[float] = Field(None, description="Mean Sentinel-2 B8 surface reflectance")
    scene_cloud_cover_pct: Optional[float] = Field(None, description="Scene-level Sentinel-2 cloud cover metadata")
    clear_pixel_pct: Optional[float] = Field(None, description="Clear Sentinel-2 pixels within the sampled farm area")
    clear_pixel_threshold: Optional[float] = Field(None, description="Cloud Score+ clear-pixel threshold")
    vegetation_status: Optional[str] = Field(None, description="Transparent NDVI-threshold interpretation")
    is_fresh: Optional[bool] = Field(None, description="Whether the observation is within the freshness window")
    thumbnail_url: Optional[str] = Field(None, description="Earth Engine RGB thumbnail URL")
    reason: Optional[str] = Field(None, description="Explanation when no usable observation is available")


class DiagnosisResult(BaseModel):
    diagnosis_status: Literal["complete", "uncertain", "unavailable"] = Field("complete", description="Whether image analysis produced a usable result")
    is_valid_crop_image: bool = Field(True, description="False if image is non-agricultural, animal, face, or invalid")
    rejection_reason: Optional[str] = Field(None, description="Explanation if image is not a recognized plant/crop")
    condition_detected: str = Field("Rice Sheath Blight (Rhizoctonia solani)", description="Pathology or pest name")
    scientific_name: Optional[str] = Field("Rhizoctonia solani Kühn", description="Pathogen taxonomic binomial")
    confidence: float = Field(0.94, ge=0.0, le=1.0, description="Diagnostic model confidence (0.0 - 1.0)")
    severity: str = Field("Moderate (Early Tillering Lesions)", description="'Low', 'Moderate', 'Severe', 'Critical'")
    symptoms: List[str] = Field(
        default_factory=lambda: [
            "Oval greenish-grey water-soaked lesions near water line",
            "Irregular brown margins forming on leaf sheaths",
            "Band-like sclerotial spots spreading upward"
        ],
        description="Observed visual pathology markers"
    )
    affected_part: str = Field("Leaf sheath and lower canopy", description="Anatomical location of disease")
    immediate_bio_action: str = Field(
        "Drain excess standing water from paddy field for 48 hours to reduce relative humidity at canopy base.",
        description="Immediate emergency agronomic step"
    )
    clinical_disclaimer: str = Field(
        "Assistive decision-support system grounded in ICAR regenerative guidelines. Consult your local Block Agricultural Officer (BAO) before chemical application.",
        description="Legal and agronomic clinical disclaimer"
    )
    model_used: str = Field("gemini-2.5-flash", description="AI diagnosis model")


class FarmContext(BaseModel):
    standard_version: str = Field("in.gov.dpg.farmcontext.v1", description="Digital Public Good contract version")
    farmer: FarmerIdentity = Field(default_factory=FarmerIdentity)
    location: GeoLocation = Field(default_factory=GeoLocation)
    crop: CropDetails = Field(default_factory=CropDetails)
    soil_health: SoilHealthCard = Field(default_factory=SoilHealthCard)
    weather: WeatherContext = Field(default_factory=WeatherContext)
    satellite: SatelliteContext = Field(default_factory=SatelliteContext)
    diagnosis: Optional[DiagnosisResult] = None
    connectivity_mode: str = Field("online", description="'online', 'low_bandwidth', 'offline_cached'")


# ============================================================================
# 2. Advisory & Explainability Schemas
# ============================================================================

class RegenerativeAction(BaseModel):
    category: str = Field("Bio-Control", description="'Bio-Control', 'Soil Health', 'Water Management', 'Cultural'")
    title: str = Field("Foliar application of Trichoderma viride", description="Action title")
    description: str = Field("Spray 2.5 kg/ha of bio-agent Trichoderma viride dissolved in 500L water in late afternoon.", description="Detailed protocol")
    urgency: str = Field("Within 48 hours", description="'Immediate', 'Within 48 hours', 'Next 7 days'")
    cost_level: str = Field("Low (₹180 - ₹250 / acre)", description="Estimated farmer cost")
    expected_outcome: str = Field("Inhibits Rhizoctonia mycelial growth without chemical toxicity.", description="Target result")


class ExplainabilityEvidence(BaseModel):
    factor: str = Field(..., description="Factor name, e.g. 'Weather', 'Soil pH', 'Visual Symptoms'")
    observation: str = Field(..., description="Observed parameter")
    impact_on_decision: str = Field(..., description="How this influenced the advisory")


class AdvisoryResponse(BaseModel):
    status: str = "success"
    advisory_id: str = Field(..., description="Unique advisory reference")
    generated_at: str = Field(..., description="Timestamp")
    crop_name: str
    stage: str
    condition_assessed: str
    severity: str
    summary_advisory: str = Field(..., description="Primary actionable guidance in preferred language")
    summary_advisory_en: str = Field(..., description="English summary translation")
    actions: List[RegenerativeAction] = Field(default_factory=list)
    soil_conditioning_steps: List[str] = Field(default_factory=list)
    preventive_cultural_practices: List[str] = Field(default_factory=list)
    explainability: List[ExplainabilityEvidence] = Field(default_factory=list)
    rag_sources: List[Dict[str, Any]] = Field(default_factory=list)
    audio_url: Optional[str] = None
    language: str = "bn"
    cached_in_indexeddb: bool = False


# ============================================================================
# 3. Cross-State Interoperability & Outbreak Schemas
# ============================================================================

class StateNormalizationRequest(BaseModel):
    state_origin: str = Field("west_bengal", description="'west_bengal', 'bihar', 'odisha', or custom state name")
    raw_payload: Dict[str, Any] = Field(..., description="Raw state-specific JSON payload")
    custom_rules: Optional[Dict[str, str]] = Field(None, description="Optional declarative mapping rules for custom state onboarding")


class StateNormalizationResponse(BaseModel):
    state_origin: str
    source_schema_detected: str
    normalized_context: FarmContext
    field_mappings_applied: Dict[str, str]
    transformation_notes: List[str]


class OutbreakAlert(BaseModel):
    alert_id: str
    pest_disease_name: str
    origin_state: str
    origin_district: str
    affected_crop: str
    severity_level: str  # 'Elevated', 'High', 'Severe'
    transmission_corridor: str
    threatened_neighboring_districts: List[str]
    distance_to_border_km: float
    recommended_quarantine_action: str
    reported_at: str


# ============================================================================
# 4. Legacy Compatibility Schemas (Preserved for existing endpoints)
# ============================================================================

class FarmerProfile(BaseModel):
    """Raw farmer, geography, crop, device, and campaign attributes for legacy endpoints."""
    grower_id: Optional[str] = Field(None, description="Unique grower identifier")
    name: Optional[str] = Field(None, description="Farmer display name")
    state: Optional[str] = None
    district: Optional[str] = None
    tehsil_block: Optional[str] = None
    village: Optional[str] = None
    language: Optional[str] = Field(None, description="Preferred language")
    device_type: Optional[str] = "smartphone"
    connectivity: Optional[str] = "good"
    literacy_level: Optional[str] = "medium"
    gender: Optional[str] = None
    grower_age: Optional[float] = None
    grower_farm_size: Optional[float] = None
    high_value_farmer: Optional[bool] = False
    grower_crop_calendar: Optional[str] = None
    main_crop: Optional[str] = None
    crop_stage: Optional[str] = None
    sowing_start: Optional[str] = None
    harvest_start: Optional[str] = None
    season: Optional[str] = None
    pest_threat: Optional[str] = None
    pest_risk_level: Optional[str] = None
    weather_risk: Optional[str] = None
    product_scan: Optional[bool] = False
    offline_campaign_attended: Optional[bool] = False
    campaign_crop: Optional[str] = None
    campaign_product: Optional[str] = None
    message_sent_date: Optional[str] = None
    hist_open_rate: Optional[float] = 0.0
    hist_click_rate: Optional[float] = 0.0
    message_count_history: Optional[int] = 0
    days_since_last_message: Optional[float] = 999.0
    message_frequency: Optional[float] = 0.0

    @field_validator("grower_age", "grower_farm_size", mode="before")
    @classmethod
    def coerce_numeric(cls, v: Any) -> Optional[float]:
        if v is None or v == "":
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None


class PredictionRequest(BaseModel):
    farmer_name: Optional[str] = None
    farmer: FarmerProfile
    features_override: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None


class EngagementPrediction(BaseModel):
    engagement_probability: float
    segment: str
    confidence: float
    percentile_in_district: Optional[float] = None
    model_version: str
    feature_contributions: Optional[Dict[str, float]] = None


class ChannelRecommendation(BaseModel):
    primary_channel: str
    fallback_channel: Optional[str] = None
    best_time_window: str
    frequency_per_month: int
    rationale: str
    priority_score: float


class VernacularProfile(BaseModel):
    language: str
    regional_style: str
    complexity_level: str
    sms_safe: bool
    voice_accent: Optional[str] = None


class RAGContext(BaseModel):
    advisory_summary: str
    sources: List[Dict[str, Any]]
    retrieval_mode: str
    matched_crop: Optional[str] = None
    matched_pest: Optional[str] = None


class ContentRecommendation(BaseModel):
    sms: str
    whatsapp: str
    voice_script: str
    cta: str
    media_url: Optional[str] = None
    audio_url: Optional[str] = None
    generation_mode: str


class UrgencyRecommendation(BaseModel):
    urgency_level: str
    urgency_score: float
    factors: List[str]
    days_until_action_needed: int
    seasonal_risk: str


class PredictionResponse(BaseModel):
    farmer_name: str
    prediction: EngagementPrediction
    channel: ChannelRecommendation
    vernacular: VernacularProfile
    rag: RAGContext
    content: ContentRecommendation
    urgency: UrgencyRecommendation
    request_timestamp: str
    metadata: Dict[str, Any]


class BatchPredictionRequest(BaseModel):
    farmers: List[FarmerProfile]
    batch_name: Optional[str] = None


class BatchPredictionResponse(BaseModel):
    batch_id: str
    processed_count: int
    results: List[PredictionResponse]
    summary_by_segment: Dict[str, int]
    summary_by_channel: Dict[str, int]
