<template>
  <div class="sathi-shell">
    <!-- Toast host: error/success feedback the farmer can actually see -->
    <div class="toast-region" aria-live="polite">
      <div v-for="t in toasts" :key="t.id" class="toast-notification" :class="'toast-' + t.type">
        <span class="toast-msg" v-text="t.message"></span>
        <button type="button" class="toast-close" aria-label="Dismiss message" @click="dismiss(t.id)">
          <PhX :size="14" weight="bold" />
        </button>
      </div>
    </div>

    <!-- Offline Resiliency Notice (shared state with App.vue) -->
    <div class="sathi-topline">
      <div v-if="!isOnline" class="offline-banner">
        <div class="banner-marker"></div>
        <div class="banner-body">
          <strong>You are offline:</strong>
          <span>Your last field report and advice are saved on this phone. Everything still works without internet.</span>
        </div>
        <span class="badge-institutional badge-slate">Saved on this phone</span>
      </div>
    </div>

    <!-- Sky Strip: The Sky carries the status based on humidity risk -->
    <header class="sky sky-strip sathi-header" :data-risk="humidityRisk">
      <div class="sky-strip-inner">
        <div class="sky-strip-left">
          <div class="sathi-badge-icon">
            <PhPlant :size="24" weight="bold" class="sathi-badge-icon-elem" />
          </div>
          <div>
            <div class="farmer-title-row">
              <h1>{{ currentContext.farmer.name }}</h1>
              <span class="badge-institutional badge-forest">
                {{ currentContext.location.district }}, {{ currentContext.location.state }}
              </span>
              <span class="badge-institutional badge-slate">
                {{ currentContext.crop.name }} ({{ currentContext.crop.variety }})
              </span>
              <span class="badge-institutional badge-gold" title="Demo profile loaded on this device">Demo farm</span>
            </div>
            <p class="sky-status-line">
              {{ humidityStatusLine }}
            </p>
          </div>
        </div>

        <div class="sky-strip-right">
          <!-- Language Selector -->
          <div class="lang-selector-group">
            <label for="farmer-preferred-lang" class="selector-label">Language:</label>
            <select
              id="farmer-preferred-lang"
              aria-label="Advisory Language"
              v-model="currentContext.farmer.preferred_language"
              @change="onLanguageChange"
              class="lang-dropdown"
            >
              <option value="bn">Bengali (বাংলা)</option>
              <option value="hi">Hindi (हिन्दी)</option>
              <option value="en">English (Global)</option>
            </select>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Desk of White Cards -->
    <div class="desk">
      <!-- Main Diagnostic Lab Grid: (1) Check a leaf & (2) What it is and what to do now -->
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
          @share-card="exportDiagnosisShareCard"
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

    <!-- Hidden Share Card for Export -->
    <ShareCard
      ref="diagnosisShareCardRef"
      :title="diagnosisResult?.condition_detected || 'Crop Disease Alert'"
      :district="currentContext.location.district"
      :state="currentContext.location.state"
      :risk-level="diagnosisResult?.confidence > 0.8 ? 'High' : 'Elevated'"
      :next-step="diagnosisResult?.immediate_bio_action || 'Consult local Krishi Vigyan Kendra.'"
      :crop="currentContext.crop.name"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { PhX } from '@phosphor-icons/vue'
import '../styles/sathi.css'
import ShareCard from '../components/ShareCard.vue'
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
import { useToast } from '../composables/useToast'
import { SAMPLE_BENCHMARKS } from '../data/sampleBenchmarks'

const { isOnline, saveOfflineItem, getOfflineItem } = useOfflineStorage()
const { toasts, dismiss, success, error } = useToast()

// Current Farm Context State (demo farm profile — flagged as "Demo farm" in the UI)
const currentContext = reactive({
  standard_version: 'in.gov.dpg.farmcontext.v1',
  farmer: {
    farmer_id: 'IN-WB-NAD-0042',
    name: 'Subhash Mondal',
    phone: '+919****3210',
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

onMounted(() => {
  document.documentElement.lang = currentContext.farmer.preferred_language || 'bn'
})

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

// Stop the mic if the farmer leaves the page mid-recording
onUnmounted(() => {
  try { recognition?.abort?.() } catch { /* already stopped */ }
  recognition = null
  isRecording.value = false
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
    .catch(() => {
      selectedFileBlob.value = null
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
    error('Voice notes need Chrome or Edge on this device.')
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
    error('Could not hear you clearly. Try again in a quiet spot.')
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
  if (!selectedFileBlob.value) {
    error('Choose a leaf photo first, then tap Check.')
    return
  }

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
    error('Could not check the leaf. Check your internet and try again.')
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
    error('The advice plan could not be prepared. You can still see the leaf result above.')
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
    if (w) Object.assign(currentContext.weather, w)
    if (s) Object.assign(currentContext.soil_health, s)
    if (sat) Object.assign(currentContext.satellite, sat)
    if (!w && !s && !sat) {
      error('Field data could not refresh. Using the last saved values.')
    }
    await saveOfflineItem('latest_context', JSON.parse(JSON.stringify(currentContext)))
  } catch (err) {
    console.error('Failed to sync telemetry:', err)
    error('Field data could not refresh. Using the last saved values.')
  } finally {
    loadingTelemetry.value = false
  }
}

const diagnosisShareCardRef = ref(null)

async function exportDiagnosisShareCard() {
  if (!diagnosisResult.value || !diagnosisShareCardRef.value) return
  const ok = await diagnosisShareCardRef.value.exportCardPng(`krishisetu-diagnosis-${Date.now()}.png`)
  if (ok) {
    success('Share card image downloaded.')
  } else {
    error('Could not make the share card image. Try again.')
  }
}

function onLanguageChange() {
  const lang = currentContext.farmer.preferred_language || 'bn'
  document.documentElement.lang = lang
  if (advisoryResult.value) {
    generateAdvisoryPlan()
  }
}

// Sky risk states (DESIGN.md: the sky carries the status):
// RH >= 82% = storm — the backend's fungal sporulation threshold ("RH > 82%"),
// also used by FieldDataSection's "High risk" gauge. 70-81% = watch.
const HUMIDITY_RISK = { watch: 70, storm: 82 }

const humidityRisk = computed(() => {
  const h = currentContext.weather?.relative_humidity_pct || 0
  if (h >= HUMIDITY_RISK.storm) return 'storm'
  if (h >= HUMIDITY_RISK.watch) return 'watch'
  return 'clear'
})

const humidityStatusLine = computed(() => {
  const h = currentContext.weather?.relative_humidity_pct || 0
  if (h >= HUMIDITY_RISK.storm) {
    return `Humidity is very high (${h}%). Check the lower leaves today.`
  }
  if (h >= HUMIDITY_RISK.watch) {
    return `Humidity is high (${h}%). Monitor morning dew and canopy moisture.`
  }
  return `Field conditions are stable. Humidity is safe at ${h}%.`
})
</script>
