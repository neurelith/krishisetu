<template>
  <div class="kisan-sathi-container">
    <!-- Offline Resiliency Notice -->
    <div v-if="!isOnline" class="offline-banner">
      <div class="banner-marker"></div>
      <div class="banner-body">
        <strong>Offline Resiliency Active:</strong>
        <span>Viewing intelligence cached in browser IndexedDB. All diagnostic guidelines and previous advisories remain operational without connectivity.</span>
      </div>
      <span class="badge-institutional badge-slate">IndexedDB Local Cache</span>
    </div>

    <!-- Farmer Identity & Agro-Ecological Node Header (Slim Line) -->
    <FarmerRibbon 
      :context="currentContext" 
      @language-change="onLanguageChange" 
    />

    <!-- Main Diagnostic Lab Grid: (1) Leaf Check & (2) Result -->
    <div class="diagnostic-lab-grid">
      <!-- (1) Check a leaf -->
      <LeafCheckSection 
        :selected-sample="selectedSample"
        :preview-image="previewImage"
        :selected-file-name="selectedFileName"
        :is-recording="isRecording"
        :voice-transcript="voiceTranscript"
        :is-diagnosing="isDiagnosing"
        :preferred-language="currentContext.farmer.preferred_language"
        @select-sample="selectAndRunBenchmark"
        @file-selected="onCustomFileSelected"
        @toggle-voice="toggleVoiceRecording"
        @clear-voice="clearVoiceObservation"
        @run-diagnosis="runDiagnosis"
      />

      <!-- (2) What it is and what to do now -->
      <DiagnosisResultSection 
        :diagnosis-result="diagnosisResult"
        :is-diagnosing="isDiagnosing"
      />
    </div>

    <!-- (3) Your field today -->
    <FieldDataSection 
      :context="currentContext"
      :loading-telemetry="loadingTelemetry"
      @refresh-telemetry="refreshTelemetry"
    />

    <!-- (4) Your treatment plan -->
    <TreatmentPlanSection 
      :advisory-result="advisoryResult" 
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import '../styles/sathi.css'
import FarmerRibbon from '../components/sathi/FarmerRibbon.vue'
import LeafCheckSection from '../components/sathi/LeafCheckSection.vue'
import DiagnosisResultSection from '../components/sathi/DiagnosisResultSection.vue'
import FieldDataSection from '../components/sathi/FieldDataSection.vue'
import TreatmentPlanSection from '../components/sathi/TreatmentPlanSection.vue'
import { 
  diagnoseCropDisease, 
  generateRegenerativeAdvisory, 
  fetchAgroWeather, 
  fetchSoilHealth, 
  fetchSatelliteNDVI 
} from '../api'
import { useOfflineStorage } from '../composables/useOfflineStorage'

const { isOnline, saveOfflineItem, getOfflineItem } = useOfflineStorage()

// Current Farm Context State
const currentContext = reactive({
  standard_version: 'in.gov.dpg.farmcontext.v1',
  farmer: {
    farmer_id: 'IN-WB-NAD-0042',
    name: 'Subhash Mondal',
    phone: '+919876543210',
    preferred_language: 'bn',
    literacy_profile: 'audio_preferred',
    voice_observation: ''
  },
  location: {
    state: 'West Bengal',
    district: 'Nadia',
    block_tehsil: 'Nakashipara',
    village: 'Bethuadahari',
    latitude: 23.47,
    longitude: 88.55
  },
  crop: {
    name: 'Rice (Paddy)',
    variety: 'Swarna-Sub1',
    season: 'Kharif',
    crop_stage: 'Tillering to Panicle Initiation',
    sowing_date: '2026-07-12',
    days_since_sowing: 78
  },
  soil_health: {
    source: 'Government of India Soil Health Card (SHC)',
    card_id: 'SHC-WB-2026-8819',
    lab_test_cert: 'ICAR-NBSS-LUP/2026/WB-089',
    nitrogen_kg_ha: 185.0,
    phosphorus_kg_ha: 14.2,
    potassium_kg_ha: 160.0,
    organic_carbon_pct: 0.42,
    ph: 5.8,
    deficiencies: ['Nitrogen Low (<280 kg/ha)', 'Low Organic Carbon (<0.5%)', 'Acidic Alluvial Soil']
  },
  weather: {
    source: 'Open-Meteo Agro-Meteorology API',
    temperature_c: 31.8,
    relative_humidity_pct: 86.0,
    rainfall_last_24h_mm: 18.5,
    rainfall_forecast_7d_mm: 54.0,
    wind_speed_kmh: 14.2,
    microclimate_risk: 'Elevated fungal sporulation risk (RH > 82%)'
  },
  satellite: {
    source: 'Copernicus Sentinel-2 Level-2A',
    tile_reference: 'S2A_MSIL2A_20260924_T45QXE_R061',
    spectral_formula: 'NDVI = (B08_NIR - B04_Red) / (B08_NIR + B04_Red)',
    nir_band_reflectance: 0.78,
    red_band_reflectance: 0.17,
    ndvi: 0.64,
    ndvi_trend: 'slight_drop_anomaly',
    soil_moisture_index: 0.42,
    cloud_cover_pct: 20.0,
    vegetation_vigor: 'Moderate canopy vigor; localized chlorosis in sector B'
  },
  diagnosis: null
})

// UI & Reactive States
const loadingTelemetry = ref(false)
const isDiagnosing = ref(false)
const isGeneratingAdvisory = ref(false)
const previewImage = ref(null)
const selectedFileName = ref('')
const selectedSample = ref('rice')
const selectedFileBlob = ref(null)
const diagnosisResult = ref(null)
const advisoryResult = ref(null)

// Voice STT State
const isRecording = ref(false)
const voiceTranscript = ref('')
let recognition = null

// Sample benchmark base64 images and canonical clinical payloads
const SAMPLE_BENCHMARKS = {
  rice: {
    label: 'Rice Sheath Blight (Nadia, WB)',
    crop: 'Rice (Paddy)',
    is_valid: true,
    diagnosis: {
      condition_detected: 'Rice Sheath Blight',
      scientific_name: 'Rhizoctonia solani Kühn',
      confidence: 0.94,
      severity: 'High',
      affected_part: 'Leaf Sheath & Lower Culm',
      is_valid_crop_image: true,
      model_used: 'gemini-2.5-flash',
      rejection_reason: null,
      symptoms: [
        'Elliptical or oval water-soaked greenish-grey lesions on lower leaf sheaths near water line.',
        'Lesions coalesce with distinct irregular dark-brown margins creating banded appearance.',
        'Initial formation of tiny white globose mycelial sclerotial bodies.'
      ],
      immediate_bio_action: 'Apply foliar bio-spray of Trichoderma harzianum @ 5g/L or Pseudomonas fluorescens @ 10g/L along the base of the infected hill. Drain field to reduce canopy microclimate humidity.'
    },
    advisory: {
      language: 'bn',
      summary_advisory: 'আপনার ধানের জমিতে খোল পোড়া (Sheath Blight) রোগের লক্ষণ দেখা দিয়েছে। বাতাসের আর্দ্রতা ৮৬% হওয়ায় ছত্রাকের জীবাণু দ্রুত বিস্তার লাভ করতে পারে। রাসায়নিক প্রয়োগের পূর্বে জমিতে জমে থাকা অতিরিক্ত জল নিষ্কাশন করুন এবং ট্রাইকোডার্মা হারজিয়ানাম বা সিউডোমোনাস ফ্লুরোসেন্স স্প্রে করুন। মাটির পিএইচ ৫.৮ হওয়ায় ইউরিয়া অতিরিক্ত দেবেন না।',
      summary_advisory_en: 'Sheath Blight symptoms detected on your rice crop. High relative humidity (86%) accelerates fungal spread. Drain stagnant field water immediately and apply bio-fungicide foliar spray (Trichoderma harzianum or Pseudomonas fluorescens). Refrain from excess nitrogenous fertilizer as soil is acidic (pH 5.8).',
      generated_at: '2026-09-29 03:45 UTC',
      audio_url: null,
      actions: [
        {
          title: 'Field Microclimate Water Drainage',
          category: 'Cultural Interventions',
          urgency: 'Immediate (Within 24h)',
          description: 'Drain standing ponded water from the paddy field for 3-4 days to expose the lower sheath to sunlight and lower relative humidity below 80%.',
          cost_level: 'Zero Cost',
          expected_outcome: 'Halts secondary sclerotial germination'
        },
        {
          title: 'Bio-Fungicide Inoculation',
          category: 'Biological Protection',
          urgency: 'High (Day 1-2)',
          description: 'Spray Trichoderma harzianum @ 5.0 g/L water targeting lower sheath level during morning calm hours.',
          cost_level: 'Low (₹420 / acre)',
          expected_outcome: 'Mycoparasitic destruction of Rhizoctonia hyphae'
        },
        {
          title: 'Potassium Soil Conditioning',
          category: 'Soil Fertility & Resilience',
          urgency: 'Standard (Day 3-5)',
          description: 'Apply Muriate of Potash (MOP) @ 20 kg/acre to strengthen culm cell walls against penetration pegs.',
          cost_level: 'Moderate (₹680 / acre)',
          expected_outcome: 'Enhances epidermal mechanical resistance by 40%'
        }
      ],
      explainability: [
        {
          factor: 'Microclimate Humidity (86%)',
          observation: 'Exceeds the 82% fungal sporulation threshold.',
          impact_on_decision: 'Mandates immediate water drainage before chemical intervention.'
        },
        {
          factor: 'Soil Reaction (pH 5.8)',
          observation: 'Acidic alluvial matrix restricts phosphorus availability.',
          impact_on_decision: 'Substitutes acidic chemical fertilizers with biological amendments.'
        }
      ],
      rag_sources: [
        { id: 'rag-01', topic: 'Epidemiology of Rhizoctonia solani in Lower Gangetic Plains', region: 'West Bengal' },
        { id: 'rag-02', topic: 'ICAR Integrated Sheath Blight Management in Kharif Rice', region: 'National' }
      ]
    },
    url: 'data:image/svg+xml;utf8,<svg role="img" aria-label="Rice Sheath Blight specimen" xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260"><rect width="400" height="260" fill="%232d4a22"/><path d="M50,240 Q180,40 320,180" stroke="%2384cc16" stroke-width="24" fill="none"/><ellipse cx="160" cy="140" rx="35" ry="16" fill="%23a3e635" stroke="%23713f12" stroke-width="3"/><ellipse cx="210" cy="165" rx="42" ry="18" fill="%23bef264" stroke="%23713f12" stroke-width="3"/><text x="80" y="240" fill="white" font-family="sans-serif" font-size="14" font-weight="bold">Rice Sheath Blight (Rhizoctonia)</text></svg>'
  },
  wheat: {
    label: 'Wheat Yellow Rust (Purnia, Bihar)',
    crop: 'Wheat',
    is_valid: true,
    diagnosis: {
      condition_detected: 'Wheat Stripe / Yellow Rust',
      scientific_name: 'Puccinia striiformis f. sp. tritici',
      confidence: 0.96,
      severity: 'Severe',
      affected_part: 'Foliar Lamina (Parallel Stripes)',
      is_valid_crop_image: true,
      model_used: 'gemini-2.5-flash',
      rejection_reason: null,
      symptoms: [
        'Linear yellow-orange uredinial pustules arranged in parallel stripes along leaf veins.',
        'Chlorotic striping followed by premature leaf desiccation.',
        'High sporulation shedding bright yellow powdery spore masses.'
      ],
      immediate_bio_action: 'Apply biological preventative barrier with Bacillus subtilis @ 10g/L. Alert neighboring districts in West Bengal border corridor.'
    },
    advisory: {
      language: 'bn',
      summary_advisory: 'গমের পাতায় হলুদ মরিচা (Yellow Rust) রোগের তীব্র আক্রমণ পরিলক্ষিত হয়েছে। দ্রুত জৈব ছত্রাকনাশক স্প্রে করুন এবং সংলগ্ন ব্লকে সতর্কবার্তা পাঠান।',
      summary_advisory_en: 'Wheat Yellow Rust pustules confirmed. Air currents favor interstate spore dispersal. Initiate immediate biocontrol perimeter barrier.',
      generated_at: '2026-09-29 03:45 UTC',
      audio_url: null,
      actions: [
        {
          title: 'Perimeter Barrier Bio-Spray',
          category: 'Biological Protection',
          urgency: 'Critical (Within 12h)',
          description: 'Spray Bacillus subtilis @ 10g/L along windward field border to prevent airborne spore dissemination.',
          cost_level: 'Low (₹380 / acre)',
          expected_outcome: 'Forms antimicrobial barrier on foliar surface'
        }
      ],
      explainability: [
        {
          factor: 'Wind Speed & Ambient Temp',
          observation: 'Cool ambient temperature (16-22°C) with moderate breezes favors airborne dissemination.',
          impact_on_decision: 'Prioritizes windward containment spray.'
        }
      ],
      rag_sources: [
        { id: 'rag-03', topic: 'Management of Wheat Rust Epidemics', region: 'Indo-Gangetic Plains' }
      ]
    },
    url: 'data:image/svg+xml;utf8,<svg role="img" aria-label="Wheat Yellow Rust specimen" xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260"><rect width="400" height="260" fill="%233e5c32"/><path d="M40,210 Q200,10 360,190" stroke="%23eab308" stroke-width="6" stroke-dasharray="10,5"/><path d="M60,225 Q210,35 340,200" stroke="%23facc15" stroke-width="8" stroke-dasharray="8,4"/><text x="100" y="245" fill="white" font-family="sans-serif" font-size="14" font-weight="bold">Wheat Yellow Rust Stripes (Puccinia)</text></svg>'
  },
  cotton: {
    label: 'Cotton Pink Bollworm (Maharashtra)',
    crop: 'Cotton',
    is_valid: true,
    diagnosis: {
      condition_detected: 'Pink Bollworm Infestation',
      scientific_name: 'Pectinophora gossypiella (Saunders)',
      confidence: 0.91,
      severity: 'High',
      affected_part: 'Developing Boll & Squares (Entry Borehole)',
      is_valid_crop_image: true,
      model_used: 'gemini-2.5-flash',
      rejection_reason: null,
      symptoms: [
        'Pin-hole entry boreholes on young developing bolls plugged with larval frass.',
        'Rosetted flower blossoms ("rosette flowers") failing to open normally.',
        'Internal burrowing through locules damaging lint fibers and seeds.'
      ],
      immediate_bio_action: 'Install Gossyplure sex pheromone delta traps @ 10 traps/acre; release egg parasitoid Trichogramma bactrae @ 50,000 wasps/acre.'
    },
    advisory: {
      language: 'bn',
      summary_advisory: 'তুলার গুটিতে গোলাপি শুঁয়োপোকার (Pink Bollworm) আক্রমণ শনাক্ত করা হয়েছে। অবিলম্বে ফেরোমোন ফাঁদ ব্যবহার করুন এবং ট্রাইকোগ্রামা পরজীবী ছাড়ুন।',
      summary_advisory_en: 'Pink Bollworm infestation confirmed in cotton bolls. Deploy Gossyplure pheromone traps and release Trichogramma bactrae parasitoids immediately.',
      generated_at: '2026-09-29 03:45 UTC',
      audio_url: null,
      actions: [
        {
          title: 'Mating Disruption with Pheromone Traps',
          category: 'Biological Protection',
          urgency: 'Critical',
          description: 'Deploy 8-10 Gossyplure delta traps per acre at canopy height to capture male moths.',
          cost_level: 'Low (₹220 / acre)',
          expected_outcome: 'Disrupts reproductive mating cycles by 65%'
        }
      ],
      explainability: [
        {
          factor: 'Crop Phenology (Flowering/Boll formation)',
          observation: 'Boll initiation stage coincides with second-generation moth emergence.',
          impact_on_decision: 'Triggers mass trapping and parasitoid release.'
        }
      ],
      rag_sources: [
        { id: 'rag-04', topic: 'Integrated Pest Management for Cotton Pink Bollworm', region: 'Central India' }
      ]
    },
    url: 'data:image/svg+xml;utf8,<svg role="img" aria-label="Cotton Pink Bollworm specimen" xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260"><rect width="400" height="260" fill="%231e3a1e"/><circle cx="200" cy="130" r="70" fill="%233f6212"/><circle cx="180" cy="115" r="10" fill="%231c1917"/><ellipse cx="215" cy="140" rx="14" ry="7" fill="%23fb7185" stroke="%23881337"/><text x="80" y="245" fill="white" font-family="sans-serif" font-size="14" font-weight="bold">Cotton Pink Bollworm Borehole (Pectinophora)</text></svg>'
  },
  invalid_dog: {
    label: 'Non-Crop Guardrail Validation (Canine Photo)',
    crop: 'Non-Crop',
    is_valid: false,
    diagnosis: {
      condition_detected: 'Non-Agricultural Specimen (Canine)',
      scientific_name: 'Canis lupus familiaris',
      confidence: 0.99,
      severity: 'N/A',
      affected_part: 'N/A',
      is_valid_crop_image: false,
      model_used: 'gemini-2.5-flash',
      rejection_reason: 'The submitted image depicts a domestic animal (canine), not a cultivated crop or plant foliage specimen. KrishiSetu has safely rejected diagnosis to prevent erroneous agrochemical recommendations and protect farmer capital.',
      symptoms: [],
      immediate_bio_action: ''
    },
    advisory: null,
    url: 'data:image/svg+xml;utf8,<svg role="img" aria-label="Non-Crop specimen" xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260"><rect width="400" height="260" fill="%23cbd5e1"/><ellipse cx="200" cy="130" rx="80" ry="60" fill="%23d97706"/><circle cx="160" cy="110" r="12" fill="%230f172a"/><circle cx="240" cy="110" r="12" fill="%230f172a"/><ellipse cx="200" cy="145" rx="16" ry="10" fill="%230f172a"/><path d="M140,80 Q110,30 130,120" fill="%2392400e"/><path d="M260,80 Q290,30 270,120" fill="%2392400e"/><text x="80" y="235" fill="%231e293b" font-family="sans-serif" font-size="14" font-weight="bold">Non-Crop Image (Triggers Guardrail Rejection)</text></svg>'
  }
}

onMounted(async () => {
  const cachedContext = await getOfflineItem('latest_context')
  if (cachedContext) {
    Object.assign(currentContext, cachedContext)
  }

  const cachedAdvisory = await getOfflineItem('latest_advisory')
  if (cachedAdvisory) {
    advisoryResult.value = cachedAdvisory
  }

  const cachedDiagnosis = await getOfflineItem('latest_diagnosis')
  if (cachedDiagnosis) {
    diagnosisResult.value = cachedDiagnosis
  }

  if (!diagnosisResult.value) {
    loadSampleLeaf('rice', true)
  } else {
    loadSampleLeaf('rice', false)
  }
})

function selectAndRunBenchmark(type) {
  loadSampleLeaf(type, true)
}

function loadSampleLeaf(type, autoApply = false) {
  selectedSample.value = type
  const sample = SAMPLE_BENCHMARKS[type]
  if (!sample) return

  previewImage.value = sample.url
  selectedFileName.value = sample.label
  currentContext.crop.name = sample.crop

  fetch(sample.url)
    .then(res => res.blob())
    .then(blob => {
      selectedFileBlob.value = blob
    })

  if (autoApply) {
    diagnosisResult.value = sample.diagnosis
    advisoryResult.value = sample.advisory
  }
}

function onCustomFileSelected(file) {
  selectedFileBlob.value = file
  selectedFileName.value = file.name
  selectedSample.value = 'custom'
  const reader = new FileReader()
  reader.onload = (e) => {
    previewImage.value = e.target.result
  }
  reader.readAsDataURL(file)
}

function toggleVoiceRecording() {
  if (isRecording.value) {
    recognition?.stop()
    isRecording.value = false
    return
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SpeechRecognition) {
    alert('Speech recognition is not supported in this browser environment. Please test in Chrome or Edge.')
    return
  }

  recognition = new SpeechRecognition()
  const lang = currentContext.farmer.preferred_language
  recognition.lang = lang === 'bn' ? 'bn-IN' : (lang === 'hi' ? 'hi-IN' : 'en-IN')
  recognition.interimResults = false
  recognition.maxAlternatives = 1

  recognition.onstart = () => {
    isRecording.value = true
  }

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript
    voiceTranscript.value = transcript
    currentContext.farmer.voice_observation = transcript
  }

  recognition.onerror = () => {
    isRecording.value = false
  }

  recognition.onend = () => {
    isRecording.value = false
  }

  recognition.start()
}

function clearVoiceObservation() {
  voiceTranscript.value = ''
  currentContext.farmer.voice_observation = ''
}

async function runDiagnosis() {
  if (!selectedFileBlob.value) return

  isDiagnosing.value = true
  diagnosisResult.value = null

  try {
    const res = await diagnoseCropDisease(selectedFileBlob.value, currentContext.crop.name)
    diagnosisResult.value = res
    currentContext.diagnosis = res

    await saveOfflineItem('latest_diagnosis', res)
    await saveOfflineItem('latest_context', JSON.parse(JSON.stringify(currentContext)))

    if (res.is_valid_crop_image) {
      await generateAdvisoryPlan()
    }
  } catch (err) {
    console.error('Diagnosis error:', err)
  } finally {
    isDiagnosing.value = false
  }
}

async function generateAdvisoryPlan() {
  isGeneratingAdvisory.value = true
  try {
    const payload = JSON.parse(JSON.stringify(currentContext))
    const res = await generateRegenerativeAdvisory(payload)
    advisoryResult.value = res
    await saveOfflineItem('latest_advisory', res)
  } catch (err) {
    console.error('Advisory generation error:', err)
  } finally {
    isGeneratingAdvisory.value = false
  }
}

async function refreshTelemetry() {
  loadingTelemetry.value = true
  try {
    const [w, s, sat] = await Promise.all([
      fetchAgroWeather(currentContext.location.latitude, currentContext.location.longitude),
      fetchSoilHealth(currentContext.location.state, currentContext.location.district),
      fetchSatelliteNDVI(currentContext.location.latitude, currentContext.location.longitude)
    ])
    Object.assign(currentContext.weather, w)
    Object.assign(currentContext.soil_health, s)
    Object.assign(currentContext.satellite, sat)
    await saveOfflineItem('latest_context', JSON.parse(JSON.stringify(currentContext)))
  } catch (err) {
    console.error('Failed to sync telemetry:', err)
  } finally {
    loadingTelemetry.value = false
  }
}

function onLanguageChange() {
  if (advisoryResult.value) {
    generateAdvisoryPlan()
  }
}
</script>
