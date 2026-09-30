<template>
  <section class="telemetry-operations-matrix unboxed">
    <div class="matrix-head">
      <div class="matrix-title">
        <PhPlant :size="24" weight="bold" class="text-forest" />
        <h2>Your field today</h2>
      </div>
      <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
        <div class="matrix-sync-tag">
          <span class="meta">{{ loadingTelemetry ? 'Refreshing field data…' : 'Live field data · updated from weather, soil and satellite' }}</span>
        </div>
        <button
          type="button"
          @click="$emit('refresh-telemetry')"
          class="btn-gov-outline"
          :disabled="loadingTelemetry"
          style="min-height: 48px;"
        >
          <PhArrowsClockwise :size="18" weight="bold" :class="{ 'spin': loadingTelemetry }" />
          <span>Refresh field data</span>
        </button>
      </div>
    </div>

    <div class="matrix-grid card-solid">
      <!-- Stream 1: Agro-Weather (Open-Meteo) -->
      <div class="matrix-column">
        <div class="column-header">
          <span class="station-provenance">Weather · Bethuadahari station</span>
          <h3>Weather now</h3>
          <span class="source-tag">Open-Meteo station data</span>
        </div>

        <!-- Humidity gauge with 82% fungal threshold marker -->
        <div class="telemetry-gauge-card">
          <div class="gauge-header">
            <span class="gauge-label">Humidity and disease risk</span>
            <span class="gauge-value" :class="isHighRisk ? 'alert' : 'safe'">
              {{ context.weather.relative_humidity_pct }}% ({{ humidityLabel }})
            </span>
          </div>
          <div class="gauge-track-container">
            <div class="gauge-bar-track">
              <div
                class="gauge-fill-bar"
                :class="isHighRisk ? 'gauge-fill-alert' : 'gauge-fill-safe'"
                :style="{ width: gaugeWidth(context.weather.relative_humidity_pct, 0, 100) + '%' }"
              ></div>
              <div class="gauge-threshold-marker marker-rh-82" title="Fungal risk starts at 82% humidity"></div>
            </div>
            <div class="gauge-ticks-row">
              <span>0% Safe</span>
              <span class="threshold-label">82% Risk</span>
              <span>100% Saturated</span>
            </div>
          </div>
        </div>

        <!-- Tabular Dual Metrics -->
        <div class="metrics-tabular">
          <div class="metric-row">
            <span class="metric-key">Temperature</span>
            <span class="metric-val">{{ context.weather.temperature_c }}°C</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Rain expected this week</span>
            <span class="metric-val">{{ context.weather.rainfall_forecast_7d_mm }} mm</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Rain in last 24 hours</span>
            <span class="metric-val">{{ context.weather.rainfall_last_24h_mm }} mm</span>
          </div>
        </div>

        <div class="stream-risk-note">
          <span class="gauge-label">What this means:</span>
          <p class="font-editorial-italic" v-text="context.weather.microclimate_risk"></p>
        </div>
      </div>

      <!-- Stream 2: Soil Health Card (GOI SHC) -->
      <div class="matrix-column border-left-divider">
        <div class="column-header">
          <span class="station-provenance">Soil lab · Government Soil Health Card</span>
          <h3>Soil health</h3>
          <span class="source-tag">Card #<span v-text="context.soil_health.card_id"></span></span>
        </div>

        <!-- Soil Reaction pH Range Gauge -->
        <div class="telemetry-gauge-card">
          <div class="gauge-header">
            <span class="gauge-label">Soil pH (acidity)</span>
            <span class="gauge-value" :class="phIsAcidic ? 'alert' : 'safe'">{{ context.soil_health.ph }} ({{ phLabel }})</span>
          </div>
          <div class="gauge-track-container">
            <div class="gauge-bar-track">
              <div class="gauge-fill-bar gauge-fill-alert" :style="{ width: gaugeWidth(context.soil_health.ph, 0, 14) + '%' }"></div>
              <div class="gauge-threshold-marker marker-rh-82" style="left: 50%;" title="Neutral target (pH 7.0)"></div>
            </div>
            <div class="gauge-ticks-row">
              <span>0 Acidic</span>
              <span class="threshold-label">7.0 Neutral</span>
              <span>14 Alkaline</span>
            </div>
          </div>
        </div>

        <!-- N-P-K Nutrient Status -->
        <div class="metrics-tabular">
          <div class="metric-row">
            <span class="metric-key">Nitrogen (N)</span>
            <span class="metric-val text-alert">{{ context.soil_health.nitrogen_kg_ha }} kg/ha (Low)</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Phosphorus (P)</span>
            <span class="metric-val text-alert">{{ context.soil_health.phosphorus_kg_ha }} kg/ha (Low)</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Potash (K)</span>
            <span class="metric-val text-forest">{{ context.soil_health.potassium_kg_ha }} kg/ha (Moderate)</span>
          </div>
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px;">
          <span v-for="(def, idx) in context.soil_health.deficiencies" :key="idx" class="badge-institutional badge-soil">
            {{ def }}
          </span>
        </div>

        <div class="stream-risk-note">
          <span class="gauge-label">What this means:</span>
          <p class="font-editorial-italic">"Acidic soil locks up phosphate; adding compost and lime restores fertility."</p>
        </div>
      </div>

      <!-- Stream 3: Satellite NDVI (Copernicus Sentinel-2) -->
      <div class="matrix-column border-left-divider">
        <div class="column-header">
          <span class="station-provenance">Satellite · Sentinel-2</span>
          <h3>Satellite view</h3>
          <span class="source-tag">ESA Copernicus, 10m detail</span>
        </div>

        <!-- Vegetative Vigor Chlorophyll Spectrum Gauge -->
        <div class="telemetry-gauge-card">
          <div class="gauge-header">
            <span class="gauge-label">Crop greenness (NDVI)</span>
            <span class="gauge-value text-forest">{{ context.satellite.ndvi }} ({{ ndviLabel }})</span>
          </div>
          <div class="gauge-track-container">
            <div class="gauge-bar-track">
              <div class="gauge-fill-bar gauge-fill-safe" :style="{ width: gaugeWidth(context.satellite.ndvi, 0, 1) + '%' }"></div>
            </div>
            <div class="gauge-ticks-row">
              <span>0.0 Bare</span>
              <span>0.5 Growing</span>
              <span>1.0 Dense</span>
            </div>
          </div>
        </div>

        <div class="metrics-tabular">
          <div class="metric-row">
            <span class="metric-key">Soil moisture index</span>
            <span class="metric-val" v-text="context.satellite.soil_moisture_index"></span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Cloud cover</span>
            <span class="metric-val">{{ context.satellite.cloud_cover_pct }}%</span>
          </div>
        </div>

        <!-- Granule/mono details on demand -->
        <DetailDisclosure show-label="Satellite image details" hide-label="Hide satellite details">
          <div class="stream-risk-note">
            <span class="gauge-label">Image provenance:</span>
            <p class="font-mono meta" v-text="context.satellite.spectral_formula || 'NDVI = (B08_NIR - B04_Red) / (B08_NIR + B04_Red)'"></p>
            <p class="font-mono meta" v-text="'Granule: ' + (context.satellite.tile_reference || 'S2A_MSIL2A_20260924_T45QXE_R061')"></p>
          </div>
        </DetailDisclosure>
      </div>
    </div>

    <!-- Spray-timing science: available on demand, not in the way -->
    <DetailDisclosure show-label="Best spray times and disease pressure" hide-label="Hide spray guide">
      <InfographicTelemetryRadar />
    </DetailDisclosure>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { PhPlant, PhArrowsClockwise } from '@phosphor-icons/vue'
import InfographicTelemetryRadar from '../InfographicTelemetryRadar.vue'
import DetailDisclosure from './DetailDisclosure.vue'

const props = defineProps({
  context: { type: Object, required: true },
  loadingTelemetry: { type: Boolean, default: false }
})

defineEmits(['refresh-telemetry'])

// Clamp helper: keeps gauges inside 0-100% even when data goes out of range
// (e.g. NDVI can be negative over water/clouds, humidity could exceed 100).
function gaugeWidth(value, min, max) {
  const n = Number(value)
  if (!Number.isFinite(n)) return 0
  return Math.min(100, Math.max(0, ((n - min) / (max - min)) * 100))
}

// Same 82% fungal threshold as the backend's microclimate risk and Home's sky state.
const FUNGAL_RH_THRESHOLD = 82

const isHighRisk = computed(() => {
  const rh = props.context?.weather?.relative_humidity_pct
  return typeof rh === 'number' && rh >= FUNGAL_RH_THRESHOLD
})

const humidityLabel = computed(() => (isHighRisk.value ? 'High risk' : 'Safe'))

const phIsAcidic = computed(() => {
  const ph = Number(props.context?.soil_health?.ph)
  return Number.isFinite(ph) && ph < 6.5
})

const phLabel = computed(() => {
  const ph = Number(props.context?.soil_health?.ph)
  if (!Number.isFinite(ph)) return ''
  if (ph < 5.5) return 'Very acidic'
  if (ph < 6.5) return 'Acidic'
  if (ph <= 7.5) return 'Neutral'
  return 'Alkaline'
})

const ndviLabel = computed(() => {
  const v = Number(props.context?.satellite?.ndvi)
  if (!Number.isFinite(v)) return ''
  if (v >= 0.6) return 'Dense canopy'
  if (v >= 0.3) return 'Growing'
  return 'Sparse'
})
</script>