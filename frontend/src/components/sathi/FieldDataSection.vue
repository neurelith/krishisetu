<template>
  <section class="telemetry-operations-matrix unboxed">
    <div class="matrix-head">
      <div class="matrix-title">
        <PhPlant :size="24" weight="bold" class="text-forest" />
        <h2>Your field today</h2>
      </div>
      <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
        <div class="matrix-sync-tag">
          <span class="meta">Multi-Stream Fusion Active · 10m Ground Resolution</span>
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
          <span class="station-provenance">Agro-Meteorology · Bethuadahari Station</span>
          <h3>Atmospheric Microclimate</h3>
          <span class="source-tag">Open-Meteo High-Resolution Station</span>
        </div>

        <!-- Humidity Visual Warning Range Meter (Computed against 82% threshold) -->
        <div class="telemetry-gauge-card">
          <div class="gauge-header">
            <span class="gauge-label">Relative Humidity & Pathogen Risk</span>
            <span class="gauge-value" :class="isHighRisk ? 'alert' : 'safe'">
              {{ context.weather.relative_humidity_pct }}% ({{ humidityLabel }})
            </span>
          </div>
          <div class="gauge-track-container">
            <div class="gauge-bar-track">
              <div 
                class="gauge-fill-bar" 
                :class="isHighRisk ? 'gauge-fill-alert' : 'gauge-fill-safe'"
                :style="{ width: context.weather.relative_humidity_pct + '%' }"
              ></div>
              <div class="gauge-threshold-marker marker-rh-82" title="Fungal Sporulation Threshold (82%)"></div>
            </div>
            <div class="gauge-ticks-row">
              <span>0% Safe</span>
              <span class="threshold-label">82% Threshold</span>
              <span>100% Saturation</span>
            </div>
          </div>
        </div>

        <!-- Tabular Dual Metrics -->
        <div class="metrics-tabular">
          <div class="metric-row">
            <span class="metric-key">Ambient Temperature</span>
            <span class="metric-val">{{ context.weather.temperature_c }}°C</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">7-Day Rainfall Forecast</span>
            <span class="metric-val">{{ context.weather.rainfall_forecast_7d_mm }} mm</span>
          </div>
          <div class="metric-row">
            <span class="metric-key">24-Hour Precipitation</span>
            <span class="metric-val">{{ context.weather.rainfall_last_24h_mm }} mm</span>
          </div>
        </div>

        <div class="stream-risk-note">
          <span class="gauge-label">Microclimate Diagnostic:</span>
          <p class="font-editorial-italic" v-text="context.weather.microclimate_risk"></p>
        </div>
      </div>

      <!-- Stream 2: Soil Health Card (GOI SHC) -->
      <div class="matrix-column border-left-divider">
        <div class="column-header">
          <span class="station-provenance">Pedological Testing Lab · ICAR-NBSS</span>
          <h3>Soil Fertility Matrix (SHC)</h3>
          <span class="source-tag">Official Soil Health Card #<span v-text="context.soil_health.card_id"></span></span>
        </div>

        <!-- Soil Reaction pH Range Gauge -->
        <div class="telemetry-gauge-card">
          <div class="gauge-header">
            <span class="gauge-label">Soil Reaction (pH Balance)</span>
            <span class="gauge-value alert">{{ context.soil_health.ph }} (Acidic)</span>
          </div>
          <div class="gauge-track-container">
            <div class="gauge-bar-track">
              <div class="gauge-fill-bar gauge-fill-alert" :style="{ width: ((context.soil_health.ph / 14) * 100) + '%' }"></div>
              <div class="gauge-threshold-marker marker-rh-82" style="left: 50%;" title="Neutral Target (pH 7.0)"></div>
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
            <span class="metric-key">Potassium (K)</span>
            <span class="metric-val text-forest">{{ context.soil_health.potassium_kg_ha }} kg/ha (Moderate)</span>
          </div>
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px;">
          <span v-for="(def, idx) in context.soil_health.deficiencies" :key="idx" class="badge-institutional badge-soil">
            {{ def }}
          </span>
        </div>

        <div class="stream-risk-note">
          <span class="gauge-label">Pedological Assessment:</span>
          <p class="font-editorial-italic">"Acidic soil matrix reduces bio-available phosphate; organic carbon depletion requires organic matter restitution."</p>
        </div>
      </div>

      <!-- Stream 3: Satellite NDVI (Copernicus Sentinel-2) -->
      <div class="matrix-column border-left-divider">
        <div class="column-header">
          <span class="station-provenance">Copernicus Sentinel-2 MSI · Level-2A</span>
          <h3>Orbital Spectral Telemetry</h3>
          <span class="source-tag">ESA Copernicus 10m Resolution</span>
        </div>

        <!-- Vegetative Vigor Chlorophyll Spectrum Gauge -->
        <div class="telemetry-gauge-card">
          <div class="gauge-header">
            <span class="gauge-label">Canopy Vegetative Vigor (NDVI)</span>
            <span class="gauge-value text-forest">{{ context.satellite.ndvi }} (Dense Canopy)</span>
          </div>
          <div class="gauge-track-container">
            <div class="gauge-bar-track">
              <div class="gauge-fill-bar gauge-fill-safe" :style="{ width: (context.satellite.ndvi * 100) + '%' }"></div>
            </div>
            <div class="gauge-ticks-row">
              <span>0.0 Fallow</span>
              <span>0.5 Emergence</span>
              <span>1.0 Full Canopy</span>
            </div>
          </div>
        </div>

        <div class="metrics-tabular">
          <div class="metric-row">
            <span class="metric-key">Surface Soil Moisture Index</span>
            <span class="metric-val" v-text="context.satellite.soil_moisture_index"></span>
          </div>
          <div class="metric-row">
            <span class="metric-key">Cloud Cover Mask</span>
            <span class="metric-val">{{ context.satellite.cloud_cover_pct }}%</span>
          </div>
        </div>

        <div class="stream-risk-note">
          <span class="gauge-label">Spectral Provenance:</span>
          <p class="font-mono meta" v-text="context.satellite.spectral_formula || 'NDVI = (B08_NIR - B04_Red) / (B08_NIR + B04_Red)'"></p>
          <p class="font-mono meta" v-text="'Granule: ' + (context.satellite.tile_reference || 'S2A_MSIL2A_20260924_T45QXE_R061')"></p>
        </div>
      </div>
    </div>

    <!-- Atmospheric & Spray Drift Infographic Deck -->
    <InfographicTelemetryRadar />
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { PhPlant, PhArrowsClockwise } from '@phosphor-icons/vue'
import InfographicTelemetryRadar from '../InfographicTelemetryRadar.vue'

const props = defineProps({
  context: { type: Object, required: true },
  loadingTelemetry: { type: Boolean, default: false }
})

defineEmits(['refresh-telemetry'])

const isHighRisk = computed(() => {
  const rh = props.context?.weather?.relative_humidity_pct
  return typeof rh === 'number' && rh >= 82
})

const humidityLabel = computed(() => (isHighRisk.value ? 'High risk' : 'Safe'))
</script>
