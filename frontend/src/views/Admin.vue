<template>
  <div class="command-shell">
    <!-- Header Sky Strip following alerts risk -->
    <header class="sky sky-strip command-header" :data-risk="alertsRisk">
      <div class="sky-strip-inner">
        <div class="header-left">
          <div class="command-badge-icon">
            <PhBroadcast :size="24" weight="bold" class="badge-icon-elem" />
          </div>
          <div>
            <div class="title-row">
              <h1>Outbreak watch</h1>
              <span class="badge-institutional badge-forest">Extension Officer & KVK Network</span>
            </div>
            <p class="sky-status-line">
              {{ alertsStatusLine }}
            </p>
          </div>
        </div>

        <div class="header-right">
          <button type="button" @click="showSimModal = true" class="btn-gov-primary">
            <PhWarningCircle :size="18" weight="bold" />
            <span>Simulate an outbreak</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Desk of White Cards -->
    <div class="desk">

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
              <button type="button" @click="broadcastAdvisory(alert)" class="btn-gov-outline justify-center" style="flex: 1;">
                <PhPaperPlaneTilt :size="16" weight="bold" />
                <span>Broadcast Early Warning to <span v-text="alert.threatened_neighboring_districts[0]"></span></span>
              </button>
              <button type="button" @click="shareAlertCard(alert)" class="btn-gov-outline justify-center" title="Export Share Card PNG">
                <PhShareNetwork :size="16" weight="bold" />
                <span>Share card</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Right Column: Regional Geographic Map Visualizer -->
      <section class="map-section card-solid card-float">
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
    </div> <!-- .desk -->

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

    <!-- Hidden Share Card for Export -->
    <ShareCard 
      ref="shareCardRef"
      :title="activeShareAlert.title"
      :headline-local="activeShareAlert.headlineLocal"
      :district="activeShareAlert.district"
      :state="activeShareAlert.state"
      :risk-level="activeShareAlert.riskLevel"
      :next-step="activeShareAlert.nextStep"
      :crop="activeShareAlert.crop"
    />

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import '../styles/admin.css'
import ShareCard from '../components/ShareCard.vue'
import {
  PhBroadcast,
  PhWarningCircle,
  PhUsers,
  PhMapTrifold,
  PhBug,
  PhClock,
  PhArrowsClockwise,
  PhX,
  PhPaperPlaneTilt,
  PhShareNetwork
} from '@phosphor-icons/vue'
import { fetchOutbreakTelemetry, simulateOutbreak } from '../api'

const alerts = ref([])
const loadingAlerts = ref(false)
const showSimModal = ref(false)
const isSimulating = ref(false)
const toastMessage = ref('')
const smallholdersKpi = ref('24,580')
const shareCardRef = ref(null)

const activeShareAlert = ref({
  title: 'Outbreak Warning',
  headlineLocal: '',
  district: 'Malda',
  state: 'West Bengal',
  riskLevel: 'Severe',
  nextStep: 'Immediate border quarantine inspection and containment protocol.',
  crop: 'Rice (Paddy)'
})

const activeOutbreakHub = computed(() => {
  const wbAlert = alerts.value.find(a => a.origin_state === 'West Bengal' && (a.severity_level === 'Severe' || a.severity_level === 'High')) || alerts.value.find(a => a.origin_state === 'West Bengal') || alerts.value[0]
  if (wbAlert && wbAlert.origin_district) {
    return `${wbAlert.origin_district} Hub (Active Outbreak)`
  }
  return 'Malda Extension Hub'
})

const alertsRisk = computed(() => {
  if (alerts.value.some(a => a.severity_level === 'Severe' || a.severity_level === 'High' || a.severity === 'Severe' || a.severity === 'High')) {
    return 'storm'
  }
  if (alerts.value.length > 0) {
    return 'watch'
  }
  return 'clear'
})

const alertsStatusLine = computed(() => {
  const total = alerts.value.length
  if (total === 0) return 'No active cross-border disease outbreaks detected.'
  const crossing = alerts.value.filter(a => a.transmission_vector?.includes('➔') || a.severity_level === 'Severe').length || 1
  return `${total} outbreak${total > 1 ? 's' : ''} active. ${crossing} cross${crossing === 1 ? 'es' : ''} a border.`
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
    showToast('Simulation failed: ' + err.message)
  } finally {
    isSimulating.value = false
  }
}

function broadcastAdvisory(alert) {
  showToast(`Emergency biological protocol dispatched to extension officers in ${alert.threatened_neighboring_districts[0]}.`)
}

async function shareAlertCard(alert) {
  activeShareAlert.value = {
    title: alert.pest_disease_name,
    headlineLocal: '',
    district: alert.origin_district,
    state: alert.origin_state,
    riskLevel: alert.severity_level,
    nextStep: alert.recommended_quarantine_action,
    crop: alert.affected_crop
  }
  await nextTick()
  if (shareCardRef.value) {
    const ok = await shareCardRef.value.exportCardPng(`krishisetu-outbreak-${alert.alert_id}.png`)
    if (ok) {
      showToast(`Share card for alert ${alert.alert_id} exported!`)
    }
  }
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
