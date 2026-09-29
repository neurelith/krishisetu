# 🌾 KrishiSetu (कृषि-सेतु)
### Interoperable Digital Public Good for Multi-Source Agronomic Intelligence

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Vue 3](https://img.shields.io/badge/Vue.js-3.4-4FC08D.svg?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Standard](https://img.shields.io/badge/DPG_Standard-in.gov.dpg.farmcontext.v1-2563EB.svg)](https://github.com/neurelith/krishisetu)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

KrishiSetu is an open-source **Digital Public Good (DPG)** engineered to solve agricultural data fragmentation across India's disparate state registries. By harmonizing state portals into a unified canonical standard (`in.gov.dpg.farmcontext.v1`), KrishiSetu combines **multimodal leaf pathology diagnostics**, **ICAR-CRRI grounded agro-advisory RAG**, **Sentinel-2 Level-2A satellite telemetry**, and **cross-border trans-district outbreak defense** into a single cohesive, accessible system.

---

## 🏛 System Architecture

```mermaid
flowchart TD
    subgraph State_Portals [State Agricultural Portals]
        WB[West Bengal: Matir Katha]
        BR[Bihar: DBT Agriculture]
        OD[Odisha: Krushak Odisha]
        PB[Punjab / Others: Declarative Schema]
    end

    subgraph Interop_Layer [Interoperability & Normalization Layer]
        WB_ADPT[Matir Katha Adapter]
        BR_ADPT[DBT Agriculture Adapter]
        OD_ADPT[Krushak Odisha Adapter]
        DEC_MAP[Dynamic Declarative Mapper]
        CANONICAL[Canonical Standard: in.gov.dpg.farmcontext.v1]
    end

    subgraph Intelligence_Core [Multimodal Agronomic Intelligence Core]
        GEMINI[Gemini Multimodal Vision\nLeaf Pathology Assessment]
        RAG[ICAR / CRRI Vector RAG\nClinical Treatment Protocols]
        SAT[Sentinel-2 L2A Provenance\nNDVI & Thermal Reflectance]
        OUTBREAK[Federated Outbreak Engine\nTrans-Border Corridor Defense]
        AUDIO[Vernacular TTS Engine\nHindi & Bengali Synthesis]
    end

    subgraph Swiss_UI [Swiss Ergonomic Frontend (PWA)]
        SATHI[Kisan Sathi: Farmer Diagnostic Hub]
        SETU[Kisan Setu: Interop Registry & Normalizer]
        RAKSHAK[Kisan Rakshak: Outbreak Command Center]
    end

    WB --> WB_ADPT
    BR --> BR_ADPT
    OD --> OD_ADPT
    PB --> DEC_MAP

    WB_ADPT --> CANONICAL
    BR_ADPT --> CANONICAL
    OD_ADPT --> CANONICAL
    DEC_MAP --> CANONICAL

    CANONICAL --> GEMINI
    CANONICAL --> RAG
    CANONICAL --> SAT

    GEMINI --> OUTBREAK
    RAG --> AUDIO

    CANONICAL --> SETU
    GEMINI --> SATHI
    RAG --> SATHI
    AUDIO --> SATHI
    OUTBREAK --> RAKSHAK
    SAT --> RAKSHAK
```

---

## 🚀 Key Modules

### 1. Unified DPG Standard (`in.gov.dpg.farmcontext.v1`)
Eliminates structural vendor lock-in and state silo walls by mapping disparate naming conventions (e.g., Bengali `krisak_naam`, Hindi `kisan_nam`, Odia `chasa_nam`) into a strictly validated, strongly typed schema:
- **`farmer`**: Sovereign UID, vernacular language preference, literacy profile (audio-first vs. text).
- **`location`**: Lat/Long coordinate precision, state, district, block/tehsil, village.
- **`crop`**: Variety, current physiological stage, sowing date, cumulative GDD (Growing Degree Days).
- **`soil_health`**: Soil Health Card parameters ($\text{pH}$, Nitrogen, Organic Carbon %, Electrical Conductivity).
- **`weather` & `satellite`**: Real-time humidity, temperature, precipitation risk, and Sentinel-2 surface reflectance ($\text{B8 NIR}$, $\text{B4 Red}$, $\text{NDVI}$).

### 2. Multimodal Leaf Diagnostics & Clinical Fusion
- **Visual Pathology**: Uses Gemini Multimodal Vision to inspect uploaded crop imagery, identifying pathogen lesions, chlorosis patterns, and blast/blight markers with calibrated confidence scores.
- **ICAR-CRRI Grounded Advisories**: Cross-references visual diagnoses against verified Central Rice Research Institute (CRRI) and Indian Council of Agricultural Research (ICAR) clinical advisories.
- **Explainability**: Every recommendation includes a deterministic evidence breakdown explaining *why* a specific dosage or biological control (e.g., *Pseudomonas fluorescens* vs. Tricyclazole) was selected given the farmer's specific soil $\text{pH}$ and weather conditions.
- **Vernacular Audio Synthesis**: Synthesizes clinical advisory text into natural audio clips in Hindi (`hi`) and Bengali (`bn`) for low-literacy field accessibility.

### 3. Sentinel-2 Spectral Provenance
Calculates Normalized Difference Vegetation Index (NDVI) directly from ESA Sentinel-2 MSI Level-2A surface reflectance bands:
$$\text{NDVI} = \frac{\text{B8}_{\text{NIR}} - \text{B4}_{\text{Red}}}{\text{B8}_{\text{NIR}} + \text{B4}_{\text{Red}}}$$
Exposes full granule provenance (e.g., `S2A_MSIL2A_20260924_T45QXE_R061`), surface reflectance metrics, and cloud cover probability.

### 4. Federated Outbreak Corridor Engine
Monitors disease spread across regional boundaries. For example, when Brown Plant Hopper or Yellow Stem Borer density spikes in Malda (West Bengal), the engine identifies geographic transmission vectors and issues proactive early-warning telemetry to adjacent border districts such as Katihar and Kishanganj (Bihar).

### 5. Interactive SVG Infographics
- **`InfographicTelemetryRadar.vue`**: Multi-axis telemetry radar comparing current field metrics against safe ICAR baselines.
- **`InfographicTreatmentRoadmap.vue`**: Chronological 4-stage intervention timeline (Immediate Containment $\rightarrow$ Curative Intervention $\rightarrow$ Soil Remediation $\rightarrow$ Harvest Recovery).
- **`InfographicEconomicImpact.vue`**: Yield loss mitigation, direct input cost breakdown, and net profit preservation calculations.
- **`InfographicPathogenCycle.vue`**: Pathogen incubation, sporulation, and containment visual tracker.

---

## 💻 Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend Framework** | Vue 3 (Composition API, `<script setup>`), Vue Router 4 |
| **Build & PWA** | Vite 5, `vite-plugin-pwa`, Workbox offline caching |
| **Typography & Styling**| Vanilla CSS3, IBM Plex Mono & Plus Jakarta Sans, Lucide Icons |
| **Backend API** | FastAPI 0.111, Pydantic v2, Uvicorn, Python 3.11 |
| **Knowledge Engine** | SQLite, LangChain, FAISS Vector Index, ICAR Knowledge Base |
| **AI / Multimodal** | Google Gemini Multimodal Vision, gTTS Speech Synthesis |
| **Remote Sensing** | Sentinel-2 Level-2A Spectral Index Engine |

---

## 🛠 Quickstart Guide

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** and `npm`

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Export Gemini API Key for live vision diagnostics
export GEMINI_API_KEY="your-gemini-api-key"

# Start the API server
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

The interactive OpenAPI documentation will be accessible at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🧪 Verification & Automated Testing

KrishiSetu includes an end-to-end integration and interoperability test suite validating route availability, declarative adapters, Sentinel-2 spectral integrity, and outbreak simulation:

```bash
python backend/verify_krishisetu.py
```

### Test Suite Summary

```
=== 1. Verifying Frontend Routes (http://localhost:5173) ===
  [PASS] Frontend route / -> HTTP 200
  [PASS] Frontend route /interop -> HTTP 200
  [PASS] Frontend route /command -> HTTP 200

=== 2. Verifying Backend State Sample Payloads (http://127.0.0.1:8000) ===
  [PASS] Sample for west_bengal: source='Matir Katha (মাটির কথা)'
  [PASS] Sample for bihar: source='DBT Agriculture (प्रत्यक्ष लाभ अंतरण)'
  [PASS] Sample for odisha: source='Krushak Odisha (କୃଷକ ଓଡ଼ିଶା)'

=== 3. Verifying Dynamic Declarative Schema Mapping ===
  [PASS] Declarative Adapter Source: Declarative Dynamic Adapter (Punjab)
  [PASS] Farmer Name mapped: Gurmeet Singh
  [PASS] Location District mapped: Ludhiana
  [PASS] Crop Name mapped: Wheat
  [PASS] Soil pH mapped: 7.4
  [PASS] Soil Nitrogen mapped: 210.0 kg/ha
  [PASS] Mappings applied count: 8

=== 4. Verifying Sentinel-2 Spectral Provenance & Outbreak Corridor ===
  [PASS] Active Regional Alerts: 4 corridor warning(s) active
  [PASS] Sentinel-2 Provenance: Granule=S2A_MSIL2A_20260924_T45QXE_R061
         NDVI=0.64 | Formula=NDVI = (B8_NIR - B4_Red) / (B8_NIR + B4_Red)

=== 5. Testing Simulated Cross-Border Outbreak Injection ===
  [PASS] Injected Outbreak: ALT-1EDBEC for Yellow Stem Borer
         Corridor: Malda (West Bengal) -> Border -> Katihar (Bihar)

ALL VERIFICATION CHECKS PASSED 100%!
```

---

## 📋 Data Standard Reference (`in.gov.dpg.farmcontext.v1`)

```json
{
  "schema_version": "in.gov.dpg.farmcontext.v1",
  "farmer": {
    "farmer_id": "IN-WB-NAD-0042",
    "name": "Subhash Mondal",
    "phone": "+919876543210",
    "preferred_language": "bn",
    "literacy_profile": "audio_preferred"
  },
  "location": {
    "state": "West Bengal",
    "district": "Nadia",
    "block_tehsil": "Nakashipara",
    "village": "Bethuadahari",
    "latitude": 23.47,
    "longitude": 88.55
  },
  "crop": {
    "name": "Rice (Paddy)",
    "variety": "Swarna-Sub1",
    "season": "Kharif",
    "crop_stage": "Tillering to Panicle Initiation",
    "sowing_date": "2026-07-12",
    "days_since_sowing": 78
  },
  "soil_health": {
    "ph": 6.2,
    "nitrogen_kg_ha": 185.0,
    "phosphorus_kg_ha": 14.5,
    "potassium_kg_ha": 140.0,
    "organic_carbon_pct": 0.48,
    "electrical_conductivity_ds_m": 0.35
  },
  "weather": {
    "temperature_c": 29.5,
    "relative_humidity_pct": 84.0,
    "rainfall_last_7d_mm": 62.0,
    "forecast_summary": "High humidity with scattered evening thunderstorms."
  },
  "satellite": {
    "tile_reference": "S2A_MSIL2A_20260924_T45QXE_R061",
    "ndvi": 0.64,
    "spectral_formula": "NDVI = (B8_NIR - B4_Red) / (B8_NIR + B4_Red)",
    "nir_band_reflectance": 0.78,
    "red_band_reflectance": 0.17
  }
}
```

---

## 📄 License

This project is licensed under the MIT License.
