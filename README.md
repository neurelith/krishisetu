<div align="center">

<img src="docs/assets/hero-banner.svg" alt="KrishiSetu Hero Banner" width="100%" />

<br/>

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Vue 3](https://img.shields.io/badge/Vue.js-3.4-4FC08D.svg?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Standard](https://img.shields.io/badge/DPG_Standard-in.gov.dpg.farmcontext.v1-2563EB.svg)](https://github.com/neurelith/krishisetu)
[![Sentinel-2](https://img.shields.io/badge/ESA-Sentinel--2_L2A-blue.svg?logo=googleearth&logoColor=white)](https://sentinels.copernicus.eu/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<h3>Interoperable Digital Public Good for Multi-Source Agronomic Intelligence</h3>

<p>Harmonizing disparate state agricultural registries into a sovereign, open canonical data standard with multimodal pathology vision, Sentinel-2 spectral indices, ICAR-CRRI clinical RAG, and federated cross-border outbreak defense.</p>

<table>
  <tr>
    <td align="right"><b>🚀 Start</b></td>
    <td align="center"><a href="#-quickstart-guide">⚡ Quickstart</a></td>
    <td align="center"><a href="#-system-architecture">🏛 Architecture</a></td>
    <td align="center"><a href="#-verification--automated-testing">🧪 Verification</a></td>
  </tr>
  <tr>
    <td align="right"><b>💡 Discover</b></td>
    <td align="center"><a href="#-core-capabilities-bento-matrix">🧩 Capabilities</a></td>
    <td align="center"><a href="#-interactive-agronomic-infographics">📊 Infographics</a></td>
    <td align="center"><a href="#-legacy-state-silos-vs-krishisetu-dpg">⚖️ State Comparison</a></td>
  </tr>
  <tr>
    <td align="right"><b>📋 Standard</b></td>
    <td align="center"><a href="#-data-standard-reference-ingovdpgfarmcontextv1">📜 DPG Schema</a></td>
    <td align="center"><a href="docs/PURPOSE_AND_CONTEXT_ARCHITECTURE.md">📖 Context Guide</a></td>
    <td align="center"><a href="#-license">📄 License</a></td>
  </tr>
</table>

</div>

---

## 🏛 System Architecture

KrishiSetu is structured into five distinct operational stages: Heterogeneous State Registry Ingestion $\rightarrow$ Canonical DPG Normalization $\rightarrow$ Grounded Dual-Core AI Reasoners $\rightarrow$ Triaged Ergonomic Consoles $\rightarrow$ Federated Regional Defense.

<div align="center">
  <img src="docs/assets/architecture-diagram.svg" alt="KrishiSetu End-to-End System Architecture" width="100%" />
</div>

<br/>

### Data Flow Overview

```mermaid
flowchart TD
    subgraph Ingestion [1. Heterogeneous State Ingestion]
        WB[West Bengal: Matir Katha]
        BR[Bihar: DBT Agriculture]
        OD[Odisha: Krushak Odisha]
        PB[Punjab: Declarative Dynamic Adapter]
    end

    subgraph Standard [2. DPG Normalization Engine]
        NORM[Canonical Standard: in.gov.dpg.farmcontext.v1]
    end

    subgraph Core_AI [3. Dual-Core AI Diagnostics & Remote Sensing]
        GEMINI[Gemini 2.5 Multimodal Vision\nLeaf Pathology Diagnostic Core]
        RAG[ICAR-CRRI Vector RAG\nClinical Agronomy & Soil Protocols]
        SAT[Sentinel-2 L2A Telemetry\nNDVI = B8 - B4 / B8 + B4]
    end

    subgraph Consoles [4. Triaged Ergonomic Frontend Surfaces]
        SATHI[Kisan Sathi: Farmer Diagnostic PWA]
        SETU[Kisan Setu: Interop Registry & Rule Studio]
        RAKSHAK[Kisan Rakshak: Regional Outbreak Center]
    end

    subgraph Defense [5. Federated Outbreak Defense]
        CORRIDOR[Malda WB to Katihar BR Transmission Alerts]
    end

    WB --> NORM
    BR --> NORM
    OD --> NORM
    PB --> NORM

    NORM --> GEMINI
    NORM --> RAG
    NORM --> SAT

    GEMINI --> SATHI
    RAG --> SATHI
    NORM --> SETU
    SAT --> RAKSHAK
    GEMINI --> CORRIDOR
    CORRIDOR --> RAKSHAK
```

---

## 🧩 Core Capabilities: Bento Matrix

<div align="center">
  <img src="docs/assets/features-bento.svg" alt="KrishiSetu Core Capability Matrix" width="100%" />
</div>

<br/>

### 1. Multimodal Leaf Pathology Vision
- **Diagnostic Core:** Upload field leaf photographs to receive instant diagnostic assessment powered by Gemini Multimodal Vision.
- **Calibrated Confidence:** Yields structured probabilities, distinguishing Rice Blast (*Magnaporthe oryzae*), Brown Plant Hopper (*Nilaparvata lugens*), and Sheath Blight (*Rhizoctonia solani*).
- **Symptom Attribution:** Outlines microscopic visual indicators including chlorotic rings, elliptical diamond lesions, and leaf sheath necrosis.

### 2. Sentinel-2 Level-2A Spectral Telemetry
- **Scientific Formulation:** Computes Normalized Difference Vegetation Index directly from ESA Sentinel-2 MultiSpectral Instrument (MSI) surface reflectance bands:
  $$\text{NDVI} = \frac{\text{B8}_{\text{NIR}} - \text{B4}_{\text{Red}}}{\text{B8}_{\text{NIR}} + \text{B4}_{\text{Red}}}$$
- **Full Granule Provenance:** Exposes granule identifiers (e.g. `S2A_MSIL2A_20260924_T45QXE_R061`), acquisition timestamps, and radiometric quality flags.

### 3. Federated Cross-Border Outbreak Defense
- **Transmission Corridor Tracking:** Tracks biological vectors moving along agricultural ecological belts. When outbreak intensity spikes in border districts like Malda (West Bengal), proactive early warnings are dispatched to adjacent regions like Katihar and Kishanganj (Bihar).
- **48-Hour Advantage:** Provides extension officers with lead time to mobilize prophylactic bio-control agents prior to catastrophic crop damage.

### 4. Low-Literacy & Sensory Inclusion
- **Vernacular Audio Synthesis:** Automatically converts clinical advisory directives into spoken Hindi (`hi`) and Bengali (`bn`) audio using `gTTS`.
- **Field-Ready PWA:** Engineered with Workbox service workers to cache advisory cards, diagnostic roadmaps, and offline schemas for zero-connectivity field conditions.

---

## 📊 Interactive Agronomic Infographics

### 1. Diagnostic Telemetry Radar
Multi-axis field telemetry visualization comparing farmer soil metrics, atmospheric moisture, and satellite canopy indices against safe ICAR baselines:

<div align="center">
  <img src="docs/assets/infographic-radar.svg" alt="Agronomic Telemetry Radar" width="100%" />
</div>

<br/>

### 2. Chronological ICAR Treatment Roadmap
A structured 4-phase clinical intervention timeline tailored to minimize yield impact and regenerate soil biology:

<div align="center">
  <img src="docs/assets/infographic-roadmap.svg" alt="4-Stage ICAR Treatment Roadmap" width="100%" />
</div>

---

## ⚖️ Legacy State Silos vs. KrishiSetu DPG

| Architectural Dimension | Traditional State Silos (Matir Katha / DBT) | KrishiSetu Digital Public Good |
|---|---|---|
| **Data Interoperability** | Fragmented field keys (`krisak_naam` vs `kisan_nam`) | Unified `in.gov.dpg.farmcontext.v1` schema |
| **New State Onboarding** | Months of custom backend API re-architecture | Zero-code Declarative Dynamic JSON Mapper |
| **Pathology Diagnostics**| Manual visual inspection by busy field officers | Automated Gemini Vision with calibrated confidence |
| **Clinical Grounding** | Generic manufacturer-driven pesticide ads | ICAR-CRRI verified biological & chemical protocols |
| **Remote Sensing** | Expensive private satellite data subscriptions | Verified open Sentinel-2 Level-2A spectral indices |
| **Cross-Border Defense** | Data blind at state boundaries | Federated corridor early warning (WB ↔ Bihar) |
| **Field Inclusion** | Dense English/regional PDF reports | Vernacular voice synthesis (Hindi/Bengali) & offline PWA |

---

## 🌉 Supported State Adapters

| State | Source Registry | Native Naming Conventions | Adapter Status |
|---|---|---|:---:|
| **West Bengal** | *Matir Katha (মাটির কথা)* | `krisak_naam`, `jela`, `mouza`, `fasaler_jaat` | **Verified** |
| **Bihar** | *DBT Agriculture (प्रत्यक्ष लाभ अंतरण)* | `kisan_nam`, `zila`, `fasal`, `mitti_ph` | **Verified** |
| **Odisha** | *Krushak Odisha (କୃଷକ ଓଡ଼ିଶା)* | `chasa_nam`, `jilla`, `fasala`, `panji_id` | **Verified** |
| **Punjab / Extensible** | *Custom JSON / Department Portals* | Dynamic declarative rules via `/api/interop/normalize` | **Verified** |

---

## 📜 Data Standard Reference (`in.gov.dpg.farmcontext.v1`)

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

## ⚡ Quickstart Guide

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

Interactive OpenAPI docs: `http://127.0.0.1:8000/docs`.

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

Run the end-to-end integration and verification suite:

```bash
python backend/verify_krishisetu.py
```

### Verified Test Suite Output

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

## 📄 License

This project is licensed under the [MIT License](LICENSE).
