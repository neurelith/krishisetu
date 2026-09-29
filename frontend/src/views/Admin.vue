<template>
  <div class="command-shell">
    <!-- Header -->
    <header class="command-header card-solid">
      <div class="header-left">
        <div class="command-badge-icon">
          <PhBroadcast :size="24" weight="bold" class="badge-icon-elem" />
        </div>
        <div>
          <div class="title-row">
            <h1>Outbreak watch</h1>
            <span class="badge-institutional badge-forest">Extension Officer & KVK Network</span>
          </div>
          <p class="subtitle">
            Federated real-time pest and disease telemetry monitoring cross-border agricultural corridors across West Bengal and Bihar.
          </p>
        </div>
      </div>

      <div class="header-right">
        <button type="button" @click="showSimModal = true" class="btn-gov-primary">
          <PhWarningCircle :size="18" weight="bold" />
          <span>Simulate an outbreak</span>
        </button>
      </div>
    </header>

    <!-- Operational KPI Matrix -->
    <section class="kpi-grid">
      <div class="kpi-card card-solid">
        <div class="kpi-icon-box">
          <PhUsers :size="20" weight="bold" class="kpi-icon-elem text-forest" />
        </div>
        <div>
          <span class="kpi-number">{{ smallholdersKpi }}</span>
          <span class="kpi-label">Registered Smallholders <span class="meta-tag">(Sample data)</span></span>
        </div>
      </div>

      <div class="kpi-card card-solid">
        <div class="kpi-icon-box">
          <PhMapTrifold :size="20" weight="bold" class="kpi-icon-elem text-sky" />
        </div>
        <div>
          <span class="kpi-number">8 Districts</span>
          <span class="kpi-label">Interstate Corridor (WB - Bihar)</span>
        </div>
      </div>

      <div class="kpi-card card-solid">
        <div class="kpi-icon-box">
          <PhBug :size="20" weight="bold" class="kpi-icon-elem text-soil" />
        </div>
        <div>
          <span class="kpi-number">{{ alerts.length }} Vectors</span>
          <span class="kpi-label">Active Monitored Outbreaks</span>
        </div>
      </div>

      <div class="kpi-card card-solid">
        <div class="kpi-icon-box">
          <PhClock :size="20" weight="bold" class="kpi-icon-elem text-forest" />
        </div>
        <div>
          <span class="kpi-number">48 Hours</span>
          <span class="kpi-label">Advance Swarm Warning Lead</span>
        </div>
      </div>
    </section>

    <!-- Main Command Workspace -->
    <div class="command-workspace">
      
      <!-- Left Column: Active Outbreak Corridors & Alerts -->
      <section class="corridor-section card-solid">
        <div class="section-head">
          <div>
            <h2>Outbreaks crossing borders</h2>
            <span class="section-sub">Cross-state pest progression tracking</span>
          </div>
          <button type="button" @click="refreshTelemetry" class="btn-gov-outline btn-compact" :disabled="loadingAlerts">
            <PhArrowsClockwise :size="16" weight="bold" :class="{ 'spin': loadingAlerts }" />
            <span>Refresh</span>
          </button>
        </div>

        <div class="alerts-list">
          <div 
            v-for="alert in alerts" 
            :key="alert.alert_id" 
            class="alert-card"
            :class="{ 'alert-card-severe': alert.severity_level === 'Severe' }"
          >
            <div class="alert-top">
              <span class="alert-id" v-text="alert.alert_id"></span>
              <span class="badge-institutional" :class="alert.severity_level === 'Severe' ? 'badge-soil' : 'badge-slate'">
                Level: <span v-text="alert.severity_level"></span>
              </span>
            </div>

            <div class="pest-title-block">
              <h3 class="pest-name" v-text="alert.pest_disease_name"></h3>
              <span v-if="getBinomial(alert.pest_disease_name)" class="pest-binomial font-editorial-italic" v-text="getBinomial(alert.pest_disease_name)"></span>
            </div>
            <div class="pest-details">
              <span>Crop: <strong v-text="alert.affected_crop"></strong></span>
              <span>Origin: <strong><span v-text="alert.origin_district"></span> (<span v-text="alert.origin_state"></span>)</strong></span>
            </div>

            <div class="corridor-box">
              <span class="corridor-label">Transmission Corridor:</span>
              <div class="corridor-path">
                <span v-text="alert.transmission_corridor"></span>
                <span class="dist-badge">~<span v-text="alert.distance_to_border_km"></span> km to border</span>
              </div>
            </div>

            <div class="threatened-row">
              <strong>Threatened Districts:</strong>
              <div class="threat-tags">
                <span v-for="(td, idx) in alert.threatened_neighboring_districts" :key="idx" class="badge-institutional badge-slate" v-text="td"></span>
              </div>
            </div>

            <div class="quarantine-box">
              <strong>Action Mandate:</strong>
              <p v-text="alert.recommended_quarantine_action"></p>
            </div>

            <div class="alert-actions">
              <button type="button" @click="broadcastAdvisory(alert)" class="btn-gov-outline w-full justify-center">
                <PhPaperPlaneTilt :size="16" weight="bold" />
                <span>Broadcast Early Warning to <span v-text="alert.threatened_neighboring_districts[0]"></span></span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Right Column: Regional Geographic Map Visualizer -->
      <section class="map-section band-dark">
        <div class="section-head map-head">
          <div>
            <h2>Border map</h2>
            <span class="section-sub map-sub">Kosi-Mahananda-Gangetic Convergence Corridor</span>
          </div>
          <span class="badge-institutional badge-forest">GIS Telemetry</span>
        </div>

        <!-- Stylized Interactive GIS SVG Corridor Map -->
        <div class="map-container">
          <svg viewBox="0 0 540 420" class="regional-map-svg" role="img" aria-label="Kosi-Mahananda-Gangetic Agro-Ecological Corridor Map">
            <!-- Background base -->
            <rect width="540" height="420" class="map-bg" rx="10"/>

            <!-- State Region: Bihar (West) -->
            <path d="M 20,40 L 260,30 L 250,220 L 210,380 L 30,360 Z" class="map-region-bihar"/>
            <text x="70" y="80" class="map-state-label">BIHAR STATE</text>

            <!-- State Region: West Bengal (East) -->
            <path d="M 260,30 L 510,40 L 490,370 L 250,380 L 250,220 Z" class="map-region-wb"/>
            <text x="340" y="80" class="map-state-label-wb">WEST BENGAL</text>

            <!-- Interstate Border Line (Dashed) -->
            <line x1="255" y1="30" x2="250" y2="380" class="map-border-line"/>
            <text x="260" y="200" class="map-border-text" transform="rotate(90 260 200)">INTERSTATE BORDER (280 km)</text>

            <!-- Major Agricultural Hub Points -->
            <!-- Purnia (Bihar) -->
            <circle cx="170" cy="180" r="7" class="node-selected" />
            <text x="110" y="185" class="map-node-label">Purnia Hub</text>

            <!-- Katihar (Bihar) -->
            <circle cx="210" cy="220" r="7" class="node-selected" />
            <text x="145" y="235" class="map-node-label">Katihar</text>

            <!-- Dynamic Active Outbreak Hub (Derived from Alerts) -->
            <circle cx="310" cy="230" r="9" class="node-outbreak" />
            <text x="330" y="235" class="map-label-bold">{{ activeOutbreakHub }}</text>

            <!-- Nadia (WB) -->
            <circle cx="370" cy="330" r="7" class="node-safe" />
            <text x="390" y="335" class="map-node-label">Nadia (Bethuadahari)</text>

            <!-- Transmission Corridor Vector Arrow (Malda to Katihar) -->
            <path d="M 290,225 Q 255,210 220,220" class="corridor-vector"/>
            <polygon points="220,220 230,214 228,225" class="corridor-arrow"/>

            <!-- Transmission Corridor Vector Arrow (Nadia to Murshidabad) -->
            <path d="M 365,315 Q 345,280 325,250" class="corridor-vector-secondary"/>

            <!-- Map Legend Box -->
            <g transform="translate(20, 300)">
              <rect width="200" height="98" class="legend-bg" rx="6"/>
              <text x="12" y="22" class="legend-title">VECTOR SURVEILLANCE</text>
              <circle cx="20" cy="42" r="5" class="node-outbreak"/>
              <text x="32" y="46" class="legend-text">Active Outbreak Origin</text>
              <circle cx="20" cy="62" r="5" class="node-selected"/>
              <text x="32" y="66" class="legend-text">Threatened Border Node</text>
              <line x1="12" y1="82" x2="28" y2="82" class="corridor-vector-sample"/>
              <text x="32" y="86" class="legend-text">Pathogen Flight Vector</text>
            </g>
          </svg>
        </div>

        <div class="gis-metrics-card">
          <h3>Kosi-Mahananda-Gangetic Basin Corridor Status</h3>
          <ul class="gis-field-notes">
            <li class="font-editorial-italic">"Active trans-boundary biological vector detected at Katihar-Malda corridor."</li>
            <li class="font-editorial-italic">"Brown Plant Hopper microclimate threshold: RH &gt; 85% with night ambient temp 26°C."</li>
            <li class="font-editorial-italic">"Synchronized biological advisory dispatched to 14,200 border smallholders across block boundaries."</li>
          </ul>
        </div>
      </section>

    </div>

    <!-- Outbreak Simulation Modal -->
    <div v-if="showSimModal" class="modal-backdrop" @click="showSimModal = false">
      <div class="modal-card" @click.stop>
        <div class="modal-head">
          <h2>Simulate an outbreak</h2>
          <button type="button" @click="showSimModal = false" class="btn-close" aria-label="Close Simulation Modal">
            <PhX :size="20" weight="bold" />
          </button>
        </div>
        <div class="modal-body">
          <p class="modal-desc">
            Trigger a real-time pest flare-up along the West Bengal - Bihar agricultural frontier to evaluate cross-state early-warning propagation.
          </p>

          <form @submit.prevent="submitSimulation">
            <div class="form-group">
              <label for="sim-pest-name">Pest or Disease Name:</label>
              <input id="sim-pest-name" aria-label="Pest or Disease Name" v-model="simForm.pest_name" type="text" class="form-input" required />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="sim-origin-state">Origin State:</label>
                <select id="sim-origin-state" aria-label="Origin State" v-model="simForm.origin_state" class="form-input">
                  <option value="West Bengal">West Bengal</option>
                  <option value="Bihar">Bihar</option>
                  <option value="Odisha">Odisha</option>
                </select>
              </div>

              <div class="form-group">
                <label for="sim-origin-district">Origin District:</label>
                <input id="sim-origin-district" aria-label="Origin District" v-model="simForm.origin_district" type="text" class="form-input" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="sim-affected-crop">Affected Crop:</label>
                <input id="sim-affected-crop" aria-label="Affected Crop" v-model="simForm.affected_crop" type="text" class="form-input" required />
              </div>

              <div class="form-group">
                <label for="sim-severity">Severity Level:</label>
                <select id="sim-severity" aria-label="Severity Level" v-model="simForm.severity" class="form-input">
                  <option value="Elevated">Elevated</option>
                  <option value="High">High</option>
                  <option value="Severe">Severe</option>
                </select>
              </div>
            </div>

            <div class="modal-foot">
              <button type="button" @click="showSimModal = false" class="btn-gov-outline">Cancel</button>
              <button type="submit" class="btn-gov-primary" :disabled="isSimulating">
                <PhArrowsClockwise v-if="isSimulating" :size="18" weight="bold" class="spin" />
                <span>Broadcast Federated Alert</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div v-if="toastMessage" class="toast-notification" v-text="toastMessage"></div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import {
  PhBroadcast,
  PhWarningCircle,
  PhUsers,
  PhMapTrifold,
  PhBug,
  PhClock,
  PhArrowsClockwise,
  PhX,
  PhPaperPlaneTilt
} from '@phosphor-icons/vue'
import { fetchOutbreakTelemetry, simulateOutbreak } from '../api'

const alerts = ref([])
const loadingAlerts = ref(false)
const showSimModal = ref(false)
const isSimulating = ref(false)
const toastMessage = ref('')
const smallholdersKpi = ref('24,580')

const activeOutbreakHub = computed(() => {
  const severeAlert = alerts.value.find(a => a.severity_level === 'Severe') || alerts.value[0]
  if (severeAlert && severeAlert.origin_district) {
    return `${severeAlert.origin_district} Hub (Active Outbreak)`
  }
  return 'Regional Hub (Active Outbreak)'
})

const simForm = reactive({
  pest_name: 'Yellow Stem Borer (Scirpophaga incertulas)',
  origin_state: 'West Bengal',
  origin_district: 'Malda',
  affected_crop: 'Rice (Aman Paddy)',
  severity: 'Severe'
})

onMounted(() => {
  loadTelemetry()
})

async function loadTelemetry() {
  loadingAlerts.value = true
  try {
    const data = await fetchOutbreakTelemetry()
    alerts.value = data
  } catch (err) {
    console.error('Failed to load outbreak telemetry:', err)
  } finally {
    loadingAlerts.value = false
  }
}

async function refreshTelemetry() {
  await loadTelemetry()
  showToast('Telemetry refreshed from state extension nodes.')
}

async function submitSimulation() {
  isSimulating.value = true
  try {
    const newAlert = await simulateOutbreak(
      simForm.pest_name,
      simForm.origin_state,
      simForm.origin_district,
      simForm.affected_crop,
      simForm.severity
    )
    alerts.value.unshift(newAlert)
    showSimModal.value = false
    showToast(`Alert ${newAlert.alert_id} broadcast to neighboring state border nodes!`)
  } catch (err) {
    console.error('Simulation failed:', err)
    alert('Simulation error: ' + err.message)
  } finally {
    isSimulating.value = false
  }
}

function broadcastAdvisory(alert) {
  showToast(`Emergency biological protocol dispatched to extension officers in ${alert.threatened_neighboring_districts[0]}.`)
}

function showToast(msg) {
  toastMessage.value = msg
  setTimeout(() => {
    toastMessage.value = ''
  }, 4000)
}

function getBinomial(name) {
  if (!name) return ''
  const lower = name.toLowerCase()
  if (lower.includes('stem borer')) return 'Scirpophaga incertulas'
  if (lower.includes('plant hopper') || lower.includes('bph')) return 'Nilaparvata lugens'
  if (lower.includes('blast')) return 'Magnaporthe oryzae'
  if (lower.includes('sheath')) return 'Rhizoctonia solani'
  if (lower.includes('armyworm')) return 'Spodoptera frugiperda'
  if (lower.includes('blight')) return 'Xanthomonas oryzae'
  if (lower.includes('aphid')) return 'Rhopalosiphum padi'
  if (lower.includes('rust')) return 'Puccinia graminis'
  return ''
}
</script>

<style scoped>
.command-shell {
  padding: var(--space-6) var(--space-5);
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* Header */
.command-header {
  padding: var(--space-5) var(--space-6);
  border-radius: var(--radius-md);
  border: 1px solid var(--hairline);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.command-badge-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  background: var(--sarson);
  color: var(--canopy);
  border: 1.5px solid var(--canopy);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.badge-icon-elem {
  color: var(--canopy);
}

.title-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.title-row h1 {
  font-size: var(--step-2);
  font-weight: 800;
  color: var(--ink);
  letter-spacing: -0.01em;
  margin: 0;
}

.subtitle {
  margin-top: var(--space-1);
  font-size: var(--step-0);
  color: var(--ink-2);
  line-height: 1.5;
  max-width: 70ch;
}

/* KPI Matrix */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

.kpi-card {
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-md);
  border: 1px solid var(--hairline);
  display: flex;
  align-items: center;
  gap: var(--space-3);
  transition: transform 120ms, border-color 120ms;
}

.kpi-card:hover {
  transform: translateY(-1px);
  border-color: var(--hairline-strong);
}

.kpi-icon-box {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  background: var(--paper-sunken);
  border: 1px solid var(--hairline-strong);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-number {
  font-family: var(--font-mono);
  font-size: var(--step-2);
  font-weight: 800;
  color: var(--ink);
  display: block;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.kpi-label {
  font-size: 0.8125rem;
  color: var(--ink-3);
  font-weight: 600;
  margin-top: var(--space-1);
  display: block;
}

.meta-tag {
  color: var(--ink-3);
  font-size: 0.8125rem;
}

.text-forest { color: var(--green); }
.text-sky { color: var(--leaf-bright); }
.text-soil { color: var(--brick); }

/* Command Workspace */
.command-workspace {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
  align-items: start;
}

.corridor-section {
  border-radius: var(--radius-md);
  border: 1px solid var(--hairline);
  overflow: hidden;
}

.map-section {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--inkwell-line);
}

.section-head {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--hairline);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--paper-sunken);
}

.section-head.map-head {
  background: var(--inkwell-2);
  border-bottom: 1px solid var(--inkwell-line);
}

.section-head h2 {
  font-size: var(--step-1);
  font-weight: 800;
  color: var(--ink);
  margin: 0 0 var(--space-1) 0;
}

.map-head h2 {
  color: var(--inkwell-text);
}

.section-sub {
  font-size: 0.8125rem;
  color: var(--ink-3);
}

.map-sub {
  color: var(--green-line);
}

.btn-compact {
  min-height: 38px;
  padding: 0 var(--space-3);
  font-size: 0.8125rem;
  border-radius: var(--radius-pill);
}

/* Alerts List */
.alerts-list {
  padding: var(--space-4) var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  max-height: 720px;
  overflow-y: auto;
}

.alert-card {
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-4) var(--space-4);
  background: var(--paper-raised);
  transition: transform 120ms, border-color 120ms;
}

.alert-card:hover {
  border-color: var(--hairline-strong);
  transform: translateY(-1px);
}

.alert-card-severe {
  border-left: 4px solid var(--alert-text);
}

.alert-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.alert-id {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink-2);
  font-variant-numeric: tabular-nums;
}

.pest-title-block {
  margin-bottom: var(--space-2);
}

.pest-name {
  font-size: var(--step-1);
  font-weight: 800;
  color: var(--ink);
  margin: 0 0 var(--space-1) 0;
}

.pest-binomial {
  font-family: var(--font-sans);
  font-style: italic;
  font-size: 0.875rem;
  color: var(--ink-3);
  display: block;
}

.pest-details {
  display: flex;
  gap: var(--space-4);
  font-size: 0.875rem;
  color: var(--ink-2);
  margin-bottom: var(--space-3);
}

.corridor-box {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-2) var(--space-3);
  font-size: 0.8125rem;
  margin-bottom: var(--space-3);
}

.corridor-label {
  font-weight: 700;
  color: var(--ink-2);
  display: block;
  margin-bottom: var(--space-1);
}

.corridor-path {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--ink);
}

.dist-badge {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--alert-text);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.threatened-row {
  font-size: 0.8125rem;
  color: var(--ink-2);
  margin-bottom: var(--space-3);
}

.threat-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-top: var(--space-1);
}

.quarantine-box {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-2) var(--space-3);
  font-size: 0.8125rem;
  margin-bottom: var(--space-4);
}

.quarantine-box strong {
  color: var(--ink);
}

.quarantine-box p {
  margin: var(--space-1) 0 0 0;
  color: var(--ink-2);
  line-height: 1.5;
}

.w-full { width: 100%; }
.justify-center { justify-content: center; }

/* Map Section (band-dark) */
.map-container {
  padding: var(--space-4);
}

.regional-map-svg {
  width: 100%;
  border-radius: var(--radius-sm);
  border: 1px solid var(--inkwell-line);
  display: block;
}

.map-bg {
  fill: var(--inkwell);
}

.map-region-bihar {
  fill: var(--inkwell-2);
  stroke: var(--inkwell-line);
  stroke-width: 1.5;
}

.map-region-wb {
  fill: var(--canopy);
  stroke: var(--leaf);
  stroke-width: 1.5;
}

.map-state-label {
  fill: var(--green-line);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
}

.map-state-label-wb {
  fill: var(--green-wash);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
}

.map-border-line {
  stroke: var(--sarson);
  stroke-width: 2;
  stroke-dasharray: 6,4;
}

.map-border-text {
  fill: var(--sarson);
  font-size: 12px;
  font-weight: 700;
}

.node-selected {
  fill: var(--sarson);
}

.node-outbreak {
  fill: var(--alert-lite);
  stroke: var(--paper-raised);
  stroke-width: 2;
}

.node-safe {
  fill: var(--leaf-bright);
}

.map-node-label {
  fill: var(--inkwell-text);
  font-size: 12px;
  font-weight: 600;
}

.map-label-bold {
  fill: var(--paper-raised);
  font-size: 13px;
  font-weight: 700;
}

.corridor-vector {
  fill: none;
  stroke: var(--alert-lite);
  stroke-width: 3;
  stroke-dasharray: 5,3;
}

.corridor-arrow {
  fill: var(--alert-lite);
}

.corridor-vector-secondary {
  fill: none;
  stroke: var(--sarson);
  stroke-width: 2;
  stroke-dasharray: 4,3;
}

.legend-bg {
  fill: var(--inkwell-2);
  stroke: var(--inkwell-line);
  stroke-width: 1;
}

.legend-title {
  fill: var(--paper-raised);
  font-size: 12px;
  font-weight: 700;
}

.legend-text {
  fill: var(--green-wash);
  font-size: 12px;
}

.corridor-vector-sample {
  stroke: var(--alert-lite);
  stroke-width: 2;
  stroke-dasharray: 3,2;
}

.gis-metrics-card {
  margin: 0 var(--space-4) var(--space-4);
  background: var(--inkwell-2);
  border: 1px solid var(--inkwell-line);
  border-radius: var(--radius-sm);
  padding: var(--space-3) var(--space-4);
  font-size: 0.8125rem;
}

.gis-metrics-card h3 {
  font-size: var(--step-0);
  font-weight: 700;
  color: var(--sarson);
  margin: 0 0 var(--space-2) 0;
}

.gis-metrics-card ul, .gis-field-notes {
  margin: 0;
  padding-left: var(--space-4);
  color: var(--inkwell-text);
  line-height: 1.6;
  font-style: italic;
  font-size: 0.8125rem;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 47, 34, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: var(--space-5);
}

.modal-card {
  background: var(--paper-raised);
  border-radius: var(--radius-md);
  border: 1px solid var(--hairline-strong);
  width: 100%;
  max-width: 600px;
  overflow: hidden;
}

.modal-head {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--hairline);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--paper);
}

.modal-head h2 {
  font-size: var(--step-1);
  font-weight: 800;
  color: var(--ink);
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--ink-2);
  transition: background-color 120ms, color 120ms;
}

.btn-close:hover {
  background: var(--paper-sunken);
  color: var(--ink);
}

.modal-body {
  padding: var(--space-5);
}

.modal-desc {
  font-size: var(--step-0);
  color: var(--ink-2);
  margin: 0 0 var(--space-4) 0;
  line-height: 1.5;
}

.form-group {
  margin-bottom: var(--space-3);
}

.form-group label {
  display: block;
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink-2);
  margin-bottom: var(--space-1);
}

.form-input {
  width: 100%;
  border: 1.5px solid var(--hairline-strong);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  font-size: var(--step-0);
  color: var(--ink);
  background: var(--paper-raised);
  box-sizing: border-box;
  transition: border-color 120ms;
}

.form-input:focus-visible {
  border-color: var(--canopy);
  outline: 3px solid var(--canopy);
  outline-offset: 2px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

.modal-foot {
  margin-top: var(--space-4);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
}

/* Toast */
.toast-notification {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  background: var(--canopy);
  color: var(--paper-raised);
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-pill);
  font-size: var(--step-0);
  font-weight: 600;
  border: 1.5px solid var(--hairline-strong);
  z-index: 3000;
}

.spin {
  display: inline-block;
  animation: spinAnim 0.75s infinite linear;
}

@keyframes spinAnim {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 1000px) {
  .command-workspace {
    grid-template-columns: 1fr;
  }
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
