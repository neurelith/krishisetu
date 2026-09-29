<template>
  <div class="command-shell">
    <!-- Header -->
    <header class="command-header card-solid">
      <div class="header-left">
        <div class="command-badge-icon">
          <svg class="svg-icon-lg text-forest" viewBox="0 0 24 24" stroke="currentColor" fill="none" role="img" aria-label="Command Center Outbreak Radar">
            <circle cx="12" cy="12" r="9" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3a9 9 0 0 1 9 9m-9 9a9 9 0 0 1-9-9" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12l4-4" />
          </svg>
        </div>
        <div>
          <div class="title-row">
            <h1>Kisan Rakshak: regional outbreak command center</h1>
            <span class="badge-institutional badge-forest">Extension Officer & KVK Network</span>
          </div>
          <p class="subtitle">
            Federated real-time pest and disease telemetry monitoring cross-border agricultural corridors across West Bengal and Bihar.
          </p>
        </div>
      </div>

      <div class="header-right">
        <button type="button" @click="showSimModal = true" class="btn-gov-primary">
          <svg class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
          </svg>
          <span>Simulate Cross-Border Outbreak</span>
        </button>
      </div>
    </header>

    <!-- Operational KPI Matrix -->
    <section class="kpi-grid">
      <div class="kpi-card card-solid">
        <div class="kpi-icon-box">
          <svg class="svg-icon text-forest" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
          </svg>
        </div>
        <div>
          <span class="kpi-number">24,580</span>
          <span class="kpi-label">Registered Smallholders</span>
        </div>
      </div>

      <div class="kpi-card card-solid">
        <div class="kpi-icon-box">
          <svg class="svg-icon text-sky" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.284a1.875 1.875 0 00-1.006 0L3.623 5.72A1.125 1.125 0 003 6.726v11.928c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z" />
          </svg>
        </div>
        <div>
          <span class="kpi-number">8 Districts</span>
          <span class="kpi-label">Interstate Corridor (WB - Bihar)</span>
        </div>
      </div>

      <div class="kpi-card card-solid">
        <div class="kpi-icon-box">
          <svg class="svg-icon text-soil" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
          </svg>
        </div>
        <div>
          <span class="kpi-number">{{ alerts.length }} Vectors</span>
          <span class="kpi-label">Active Monitored Outbreaks</span>
        </div>
      </div>

      <div class="kpi-card card-solid">
        <div class="kpi-icon-box">
          <svg class="svg-icon text-forest" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
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
            <h2>Active trans-boundary outbreak vectors</h2>
            <span class="section-sub">Cross-state pest progression tracking</span>
          </div>
          <button type="button" @click="refreshTelemetry" class="btn-gov-outline btn-compact" :disabled="loadingAlerts">
            <svg class="svg-icon" :class="{ 'spin': loadingAlerts }" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            <span>Refresh</span>
          </button>
        </div>

        <div class="alerts-list">
          <div 
            v-for="alert in alerts" 
            :key="alert.alert_id" 
            class="alert-card"
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
                <span>Broadcast Early Warning to <span v-text="alert.threatened_neighboring_districts[0]"></span></span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Right Column: Regional Geographic Map Visualizer -->
      <section class="map-section card-solid">
        <div class="section-head">
          <div>
            <h2>Agro-ecological interstate map</h2>
            <span class="section-sub">Kosi-Mahananda-Gangetic Convergence Corridor</span>
          </div>
          <span class="badge-institutional badge-sky">GIS Telemetry</span>
        </div>

        <!-- Stylized Interactive GIS SVG Corridor Map -->
        <div class="map-container">
          <svg viewBox="0 0 540 420" class="regional-map-svg" role="img" aria-label="Kosi-Mahananda-Gangetic Agro-Ecological Corridor Map">
            <!-- Background base -->
            <rect width="540" height="420" fill="#0f172a" rx="6"/>

            <!-- State Region: Bihar (West) -->
            <path d="M 20,40 L 260,30 L 250,220 L 210,380 L 30,360 Z" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
            <text x="70" y="80" fill="#94a3b8" font-size="14" font-weight="700" letter-spacing="1">BIHAR STATE</text>

            <!-- State Region: West Bengal (East) -->
            <path d="M 260,30 L 510,40 L 490,370 L 250,380 L 250,220 Z" fill="#064e3b" stroke="#059669" stroke-width="1.5"/>
            <text x="340" y="80" fill="#86efac" font-size="14" font-weight="700" letter-spacing="1">WEST BENGAL</text>

            <!-- Interstate Border Line (Dashed) -->
            <line x1="255" y1="30" x2="250" y2="380" stroke="#f59e0b" stroke-width="2" stroke-dasharray="6,4"/>
            <text x="260" y="200" fill="#f59e0b" font-size="10" font-weight="700" transform="rotate(90 260 200)">INTERSTATE BORDER (280 km)</text>

            <!-- Major Agricultural Hub Points -->
            <!-- Purnia (Bihar) -->
            <circle cx="170" cy="180" r="7" fill="#f59e0b" />
            <text x="110" y="185" fill="#f8fafc" font-size="11" font-weight="600">Purnia Hub</text>

            <!-- Katihar (Bihar) -->
            <circle cx="210" cy="220" r="7" fill="#f59e0b" />
            <text x="145" y="235" fill="#f8fafc" font-size="11" font-weight="600">Katihar</text>

            <!-- Malda (WB) -->
            <circle cx="310" cy="230" r="9" fill="#ef4444" stroke="#ffffff" stroke-width="2"/>
            <text x="330" y="235" fill="#ffffff" font-size="12" font-weight="bold">Malda Hub (Active Outbreak)</text>

            <!-- Nadia (WB) -->
            <circle cx="370" cy="330" r="7" fill="#22c55e" />
            <text x="390" y="335" fill="#f8fafc" font-size="11" font-weight="600">Nadia (Bethuadahari)</text>

            <!-- Transmission Corridor Vector Arrow (Malda to Katihar) -->
            <path d="M 290,225 Q 255,210 220,220" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="5,3"/>
            <polygon points="220,220 230,214 228,225" fill="#ef4444"/>

            <!-- Transmission Corridor Vector Arrow (Nadia to Murshidabad) -->
            <path d="M 365,315 Q 345,280 325,250" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,3"/>

            <!-- Map Legend Box -->
            <g transform="translate(20, 310)">
              <rect width="180" height="90" fill="#020817" rx="4" stroke="#334155" stroke-width="1"/>
              <text x="12" y="20" fill="#f8fafc" font-size="11" font-weight="700">VECTOR SURVEILLANCE</text>
              <circle cx="20" cy="38" r="5" fill="#ef4444"/>
              <text x="32" y="42" fill="#94a3b8" font-size="10">Active Outbreak Origin</text>
              <circle cx="20" cy="56" r="5" fill="#f59e0b"/>
              <text x="32" y="60" fill="#94a3b8" font-size="10">Threatened Border Node</text>
              <line x1="12" y1="74" x2="28" y2="74" stroke="#ef4444" stroke-width="2" stroke-dasharray="3,2"/>
              <text x="32" y="77" fill="#94a3b8" font-size="10">Pathogen Flight Vector</text>
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
          <h2>Inject simulated outbreak event</h2>
          <button type="button" @click="showSimModal = false" class="btn-close" aria-label="Close Simulation Modal">
            <svg class="close-svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
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
                <svg v-if="isSimulating" class="svg-icon spin" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                </svg>
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
import { ref, reactive, onMounted } from 'vue'
import { fetchOutbreakTelemetry, simulateOutbreak } from '../api'

const alerts = ref([])
const loadingAlerts = ref(false)
const showSimModal = ref(false)
const isSimulating = ref(false)
const toastMessage = ref('')

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
  padding: 32px 28px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* Header */
.command-header {
  padding: 22px 24px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.command-badge-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  background: var(--forest-50);
  border: 1px solid var(--forest-200);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.title-row h1 {
  font-size: 19px;
  font-weight: 800;
  color: var(--slate-900);
  letter-spacing: -0.01em;
  margin: 0;
}

.subtitle {
  margin-top: 6px;
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

/* KPI Matrix */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.kpi-card {
  padding: 18px 20px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  gap: 14px;
  transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}

.kpi-card:hover {
  transform: translateY(-1px);
  border-color: var(--slate-300);
}

.kpi-icon-box {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background: var(--slate-100);
  border: 1px solid var(--slate-300);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-number {
  font-family: var(--font-mono);
  font-size: 20px;
  font-weight: 800;
  color: var(--slate-900);
  display: block;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.kpi-label {
  font-size: 11.5px;
  color: var(--slate-500);
  font-weight: 600;
  margin-top: 2px;
  display: block;
}

.text-forest { color: var(--forest-800); }
.text-sky { color: var(--sky-700); }
.text-soil { color: var(--soil-700); }

/* Command Workspace */
.command-workspace {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: start;
}

.corridor-section, .map-section {
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.section-head {
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--slate-50);
}

.section-head h2,
.section-head h3 {
  font-size: 14.5px;
  font-weight: 800;
  color: var(--slate-900);
  margin: 0 0 2px 0;
}

.section-sub {
  font-size: 11.5px;
  color: var(--slate-500);
}

.btn-compact {
  padding: 6px 12px;
  font-size: 12px;
  border-radius: var(--radius-sm);
}

/* Alerts List */
.alerts-list {
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 720px;
  overflow-y: auto;
}

.alert-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 16px 18px;
  background: var(--bg-surface);
  transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}

.alert-card:hover {
  border-color: var(--slate-300);
  transform: translateY(-1px);
}

.alert-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.alert-id {
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-weight: 700;
  color: var(--slate-600);
  font-variant-numeric: tabular-nums;
}

.pest-title-block {
  margin-bottom: 8px;
}

.pest-name {
  font-size: 15px;
  font-weight: 800;
  color: var(--slate-900);
  margin: 0 0 3px 0;
}

.pest-binomial {
  font-family: var(--font-editorial);
  font-style: italic;
  font-size: 13px;
  color: var(--slate-600);
  display: block;
}

.pest-details {
  display: flex;
  gap: 16px;
  font-size: 12.5px;
  color: var(--slate-600);
  margin-bottom: 12px;
}

.corridor-box {
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 12px;
  margin-bottom: 12px;
}

.corridor-label {
  font-weight: 700;
  color: var(--slate-700);
  display: block;
  margin-bottom: 4px;
}

.corridor-path {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--slate-900);
}

.dist-badge {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--soil-700);
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.threatened-row {
  font-size: 12px;
  color: var(--slate-700);
  margin-bottom: 12px;
}

.threat-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}

.quarantine-box {
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 12px;
  margin-bottom: 14px;
}

.quarantine-box strong {
  color: var(--slate-800);
}

.quarantine-box p {
  margin: 4px 0 0 0;
  color: var(--slate-700);
  line-height: 1.5;
}

.w-full { width: 100%; }
.justify-center { justify-content: center; }

/* Map Section */
.map-container {
  padding: 20px;
}

.regional-map-svg {
  width: 100%;
  border-radius: var(--radius-sm);
  border: 1px solid #1e293b;
  display: block;
}

.gis-metrics-card {
  margin: 0 20px 20px;
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  font-size: 12px;
}

.gis-metrics-card h3,
.gis-metrics-card h4 {
  font-size: 12.5px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 0 0 8px 0;
}

.gis-metrics-card ul, .gis-field-notes {
  margin: 0;
  padding-left: 20px;
  color: var(--slate-700);
  line-height: 1.6;
  font-family: var(--font-editorial);
  font-style: italic;
  font-size: 12.5px;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 24px;
}

.modal-card {
  background: #ffffff;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 600px;
  overflow: hidden;
}

.modal-head {
  padding: 16px 22px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--slate-50);
}

.modal-head h2,
.modal-head h3 {
  font-size: 15px;
  font-weight: 800;
  color: var(--slate-900);
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--slate-500);
  transition: transform 0.15s ease, opacity 0.15s ease, background-color 0.15s ease;
}

.btn-close:hover {
  background: var(--slate-200);
  color: var(--slate-800);
}

.close-svg-icon {
  width: 18px;
  height: 18px;
}

.modal-body {
  padding: 20px 22px;
}

.modal-desc {
  font-size: 12.5px;
  color: var(--slate-600);
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.form-group {
  margin-bottom: 14px;
}

.form-group label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: var(--slate-700);
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  font-size: 12.5px;
  color: var(--slate-900);
  background: var(--bg-surface);
  box-sizing: border-box;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.form-input:focus-visible {
  border-color: var(--forest-600);
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.modal-foot {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Toast */
.toast-notification {
  position: fixed;
  bottom: 28px;
  right: 28px;
  background: #0f172a;
  color: #ffffff;
  padding: 12px 20px;
  border-radius: var(--radius-pill);
  font-size: 12.5px;
  font-weight: 600;
  border: 1px solid #334155;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
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
