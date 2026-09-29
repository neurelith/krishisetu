<template>
  <div class="interop-shell">
    <!-- Header -->
    <header class="interop-header card-solid">
      <div class="header-left">
        <div class="dpg-badge-icon">
          <svg class="svg-icon-lg text-forest" viewBox="0 0 24 24" stroke="currentColor" fill="none" role="img" aria-label="Interoperability Transfer Icon">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
          </svg>
        </div>
        <div>
          <div class="title-row">
            <h1>Kisan Setu: cross-state interoperability console</h1>
            <span class="badge-institutional badge-forest">Digital Public Good (DPG)</span>
          </div>
          <p class="subtitle">
            Harmonizing disparate state agricultural registries (West Bengal <em>Matir Katha</em>, Bihar <em>DBT Krishi</em>, Odisha <em>Krushak</em>) into the unified <code>in.gov.dpg.farmcontext.v1</code> schema.
          </p>
        </div>
      </div>

      <div class="header-right">
        <button type="button" @click="showSchemaModal = true" class="btn-gov-outline">
          <svg class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>
          <span>View DPG JSON Schema</span>
        </button>
      </div>
    </header>

    <!-- State Switcher & Payload Inspection Bar -->
    <section class="state-control-bar card-solid">
      <div class="state-pills">
        <span class="control-label">Ingested State Registry:</span>
        <button 
          type="button"
          @click="selectState('west_bengal')" 
          class="state-tab-btn" 
          :class="{ active: selectedState === 'west_bengal' }"
        >
          <span class="state-tag">[WB]</span>
          <span>West Bengal (Matir Katha)</span>
        </button>
        <button 
          type="button"
          @click="selectState('bihar')" 
          class="state-tab-btn" 
          :class="{ active: selectedState === 'bihar' }"
        >
          <span class="state-tag">[BR]</span>
          <span>Bihar (DBT Krishi)</span>
        </button>
        <button 
          type="button"
          @click="selectState('odisha')" 
          class="state-tab-btn" 
          :class="{ active: selectedState === 'odisha' }"
        >
          <span class="state-tag">[OD]</span>
          <span>Odisha (Krushak Odisha)</span>
        </button>
        <button 
          type="button"
          @click="selectState('custom')" 
          class="state-tab-btn" 
          :class="{ active: selectedState === 'custom' }"
        >
          <span class="state-tag">[CUSTOM]</span>
          <span>Custom State (Dynamic Rules)</span>
        </button>
      </div>

      <div class="action-buttons">
        <button type="button" @click="loadSample" class="btn-gov-outline" :disabled="isLoading">
          <svg class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          <span>Reset Sample Payload</span>
        </button>
        <button type="button" @click="runNormalization" class="btn-gov-primary" :disabled="isLoading">
          <svg v-if="isLoading" class="svg-icon spin" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          <svg v-else class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
          </svg>
          <span>Normalize into Common DPG Contract</span>
        </button>
      </div>
    </section>

    <!-- Dual Split View: Raw Input vs Normalized DPG Standard -->
    <div class="split-workspace">
      
      <!-- Left Column: Raw State Payload -->
      <section class="panel-left card-solid">
        <div class="panel-head">
          <div>
            <h2>1. Heterogeneous state-specific payload</h2>
            <span class="portal-badge" v-text="rawPayload.source_portal || 'State Registry'"></span>
          </div>
          <span class="badge-institutional badge-slate">Source Schema</span>
        </div>

        <!-- Custom State Input Name when Custom State is selected -->
        <div v-if="selectedState === 'custom'" class="custom-state-config">
          <div class="custom-field-row">
            <label for="custom-target-state-input" class="custom-label">Target State / FPO Registry Name:</label>
            <input 
              id="custom-target-state-input"
              aria-label="Target State or FPO Registry Name"
              v-model="customStateName" 
              type="text" 
              class="custom-name-input" 
              placeholder="e.g. Punjab (PGRKAM) or Karnataka (FRUITS)" 
            />
          </div>
        </div>

        <div class="editor-wrapper">
          <textarea 
            id="raw-state-payload-editor"
            aria-label="Raw State Payload JSON"
            v-model="rawPayloadString" 
            class="code-editor" 
            spellcheck="false"
            :rows="selectedState === 'custom' ? 14 : 22"
          ></textarea>
        </div>

        <!-- Custom Declarative Mapping Rules Panel -->
        <div v-if="selectedState === 'custom'" class="custom-rules-panel">
          <div class="rules-header">
            <div class="rules-title">
              <h3>Declarative Schema Mapping Rules</h3>
            </div>
            <span class="badge-institutional badge-forest">Dynamic Adapter Engine</span>
          </div>
          <p class="rules-hint">
            Map arbitrary regional keys to canonical <code>FarmContext v1.0</code> paths without modifying backend code:
          </p>
          <textarea 
            id="custom-mapping-rules-editor"
            aria-label="Declarative Schema Mapping Rules JSON"
            v-model="customRulesString" 
            class="code-editor rules-editor" 
            spellcheck="false" 
            rows="9"
          ></textarea>
        </div>

        <div class="schema-hint-box">
          <strong class="hint-title">State Dialect Characteristics:</strong>
          <p v-if="selectedState === 'west_bengal'" class="hint-text font-editorial-italic">
            Uses Bengali phonetics: <code>krisak_naam</code>, <code>jela</code> (district), <code>mouza_gram</code>, <code>sar_n/p/k</code> (fertilizers), <code>jaiba_carbon</code>, <code>abohawa_ardrata</code> (humidity).
          </p>
          <p v-else-if="selectedState === 'bihar'" class="hint-text font-editorial-italic">
            Uses Bihar Hindi nomenclature: <code>kisan_ka_naam</code>, <code>jila</code>, <code>prakhand</code> (block), <code>mitti_ph</code>, <code>nitrogen_matra</code>, <code>nami_pratishat</code> (humidity).
          </p>
          <p v-else-if="selectedState === 'odisha'" class="hint-text font-editorial-italic">
            Uses Odia nomenclature: <code>chasa_nama</code>, <code>zilla</code>, <code>dhan_kism</code>, <code>mrutika_ph</code>, <code>sar_n</code>, <code>ardrata</code>.
          </p>
          <p v-else class="hint-text font-editorial-italic">
            Dynamic Declarative Adapter: Onboard any Indian State or FPO in under 60 seconds by modifying the JSON mapping rules above.
          </p>
        </div>
      </section>

      <!-- Right Column: Normalized DPG Output & Mapping Audit -->
      <section class="panel-right card-solid">
        <div class="panel-head">
          <div>
            <h2>2. Standardized FarmContext v1.0</h2>
            <span class="standard-badge">Canonical: in.gov.dpg.farmcontext.v1</span>
          </div>
          <span class="badge-institutional badge-forest">Validated Contract</span>
        </div>

        <!-- Mapping Transformation Table -->
        <div v-if="normalizedResponse" class="mapping-table-container">
          <h3>Canonical field mapping rules</h3>
          <table class="mapping-table">
            <thead>
              <tr>
                <th>Source State Key</th>
                <th>DPG Canonical Path</th>
                <th>Transformation Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(target, src) in normalizedResponse.field_mappings_applied" :key="src">
                <td><code>{{ src }}</code></td>
                <td><strong class="target-field">{{ target }}</strong></td>
                <td><span class="badge-institutional badge-forest">[Normalized]</span></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Normalized JSON Inspector -->
        <div class="output-wrapper">
          <pre class="code-preview"><code>{{ formattedNormalizedJson }}</code></pre>
        </div>

        <!-- Audit Transformation Notes -->
        <div v-if="normalizedResponse && normalizedResponse.transformation_notes" class="audit-notes-box">
          <h3>Interoperability engine audit log</h3>
          <ul class="audit-list">
            <li v-for="(note, nIdx) in normalizedResponse.transformation_notes" :key="nIdx" class="font-editorial-italic">
              {{ note }}
            </li>
          </ul>
        </div>
      </section>

    </div>

    <!-- Schema Modal -->
    <div v-if="showSchemaModal" class="modal-backdrop" @click="showSchemaModal = false">
      <div class="modal-card" @click.stop>
        <div class="modal-head">
          <h2>Digital public good schema: FarmContext v1.0</h2>
          <button type="button" @click="showSchemaModal = false" class="btn-close" aria-label="Close DPG Schema Modal">
            <svg class="close-svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p class="modal-desc">
            This open specification enables any Indian State (e.g. Odisha, Punjab, Karnataka) or research institute to publish and consume interoperable agricultural intelligence.
          </p>
          <pre class="schema-code"><code>{{ schemaJsonString }}</code></pre>
        </div>
        <div class="modal-foot">
          <button type="button" @click="copySchema" class="btn-gov-primary">
            <span>{{ copySuccess ? 'Copied to Clipboard' : 'Copy JSON Schema' }}</span>
          </button>
          <button type="button" @click="showSchemaModal = false" class="btn-gov-outline">Close</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { normalizeStatePayload, fetchSampleStatePayload } from '../api'

const selectedState = ref('west_bengal')
const customStateName = ref('Punjab (PGRKAM)')
const customRulesString = ref(JSON.stringify({
  "kisan_nam": "farmer.name",
  "zila": "location.district",
  "fasal": "crop.name",
  "fasal_kism": "crop.variety",
  "mitti_ph": "soil_health.ph",
  "nitrogen": "soil_health.nitrogen_kg_ha",
  "carbon": "soil_health.organic_carbon_pct",
  "ardrata": "weather.relative_humidity_pct"
}, null, 2))

const rawPayload = ref({})
const rawPayloadString = ref('{}')
const normalizedResponse = ref(null)
const isLoading = ref(false)
const showSchemaModal = ref(false)
const copySuccess = ref(false)

const formattedNormalizedJson = computed(() => {
  if (!normalizedResponse.value?.normalized_context) {
    return '// Click "Normalize into Common DPG Contract" to inspect output...'
  }
  return JSON.stringify(normalizedResponse.value.normalized_context, null, 2)
})

const schemaJsonString = computed(() => {
  return JSON.stringify({
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "FarmContext",
    "version": "1.0.0",
    "standard": "in.gov.dpg.farmcontext.v1",
    "type": "object",
    "required": ["farmer", "location", "crop", "soil_health", "weather", "satellite"],
    "properties": {
      "farmer": {
        "type": "object",
        "properties": {
          "farmer_id": { "type": "string" },
          "name": { "type": "string" },
          "preferred_language": { "type": "string", "enum": ["bn", "hi", "en", "te", "mr", "pa", "or"] }
        }
      },
      "location": {
        "type": "object",
        "properties": {
          "state": { "type": "string" },
          "district": { "type": "string" },
          "coordinates": {
            "type": "object",
            "properties": {
              "latitude": { "type": "number" },
              "longitude": { "type": "number" }
            }
          }
        }
      },
      "crop": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "variety": { "type": "string" },
          "crop_stage": { "type": "string" }
        }
      },
      "soil_health": {
        "type": "object",
        "properties": {
          "nitrogen_kg_ha": { "type": "number" },
          "phosphorus_kg_ha": { "type": "number" },
          "potassium_kg_ha": { "type": "number" },
          "organic_carbon_pct": { "type": "number" },
          "ph": { "type": "number" }
        }
      },
      "weather": {
        "type": "object",
        "properties": {
          "temperature_c": { "type": "number" },
          "relative_humidity_pct": { "type": "number" },
          "rainfall_forecast_7d_mm": { "type": "number" }
        }
      },
      "satellite": {
        "type": "object",
        "properties": {
          "ndvi": { "type": "number" },
          "soil_moisture_index": { "type": "number" }
        }
      }
    }
  }, null, 2)
})

onMounted(() => {
  loadSample()
})

async function selectState(stateKey) {
  selectedState.value = stateKey
  await loadSample()
}

async function loadSample() {
  isLoading.value = true
  try {
    if (selectedState.value === 'custom') {
      const customData = {
        "source_portal": "Punjab Kisan Portal (PGRKAM) - Dept of Agriculture",
        "kisan_nam": "Gurmeet Singh",
        "zila": "Ludhiana",
        "fasal": "Wheat (Kanak)",
        "fasal_kism": "HD-3086",
        "mitti_ph": 7.4,
        "nitrogen": 210.0,
        "carbon": 0.55,
        "ardrata": 72.0
      }
      rawPayload.value = customData
      rawPayloadString.value = JSON.stringify(customData, null, 2)
    } else {
      const data = await fetchSampleStatePayload(selectedState.value)
      rawPayload.value = data
      rawPayloadString.value = JSON.stringify(data, null, 2)
    }
    await runNormalization()
  } catch (err) {
    console.error('Error loading sample payload:', err)
  } finally {
    isLoading.value = false
  }
}

async function runNormalization() {
  isLoading.value = true
  try {
    let parsed
    try {
      parsed = JSON.parse(rawPayloadString.value)
    } catch (e) {
      alert('Invalid JSON in payload editor: ' + e.message)
      return
    }

    let customRules = null
    if (selectedState.value === 'custom') {
      try {
        customRules = JSON.parse(customRulesString.value)
      } catch (e) {
        alert('Invalid JSON in Declarative Schema Mapping Rules: ' + e.message)
        return
      }
    }

    const stateName = selectedState.value === 'custom' 
      ? (customStateName.value.trim() || 'Custom State') 
      : selectedState.value

    const res = await normalizeStatePayload(stateName, parsed, customRules)
    normalizedResponse.value = res
  } catch (err) {
    console.error('Normalization failed:', err)
  } finally {
    isLoading.value = false
  }
}

function copySchema() {
  navigator.clipboard.writeText(schemaJsonString.value)
  copySuccess.value = true
  setTimeout(() => { copySuccess.value = false }, 2000)
}
</script>

<style scoped>
.interop-shell {
  padding: 32px 28px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

/* Header */
.interop-header {
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

.dpg-badge-icon {
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

.subtitle code {
  background: var(--slate-100);
  padding: 2px 6px;
  border-radius: var(--radius-xs);
  color: var(--slate-800);
  font-family: var(--font-mono);
  font-size: 12px;
}

/* State Control Bar */
.state-control-bar {
  padding: 16px 20px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.state-pills {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.control-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--slate-700);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-right: 4px;
}

.state-tab-btn {
  background: var(--slate-100);
  border: 1px solid var(--color-border);
  color: var(--slate-700);
  font-size: 12px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.18s ease, border-color 0.18s ease, transform 0.18s ease, color 0.18s ease;
  font-variant-numeric: tabular-nums;
}

.state-tab-btn:hover {
  background: var(--slate-200);
  border-color: var(--slate-400);
  transform: translateY(-1px);
}

.state-tab-btn:active {
  transform: scale(0.98);
}

.state-tab-btn:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

.state-tab-btn.active {
  background: var(--forest-900);
  color: #ffffff;
  border-color: var(--forest-900);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.state-tag {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  font-variant-numeric: tabular-nums;
}

.state-tab-btn.active .state-tag {
  color: #86efac;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* Dual Split View */
.split-workspace {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.panel-left, .panel-right {
  padding: 22px 24px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.panel-head h2 {
  font-size: 14.5px;
  font-weight: 800;
  color: var(--slate-900);
  margin: 0 0 4px 0;
}

.portal-badge {
  font-size: 11.5px;
  color: var(--sky-700);
  font-weight: 600;
}

.standard-badge {
  font-size: 11.5px;
  color: var(--forest-800);
  font-weight: 600;
}

/* Custom State & Declarative Rules Editor */
.custom-state-config {
  margin-bottom: 14px;
}

.custom-field-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.custom-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--slate-700);
}

.custom-name-input {
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-strong);
  font-size: 12.5px;
  color: var(--slate-900);
  background: var(--bg-surface);
  transition: border-color 0.15s ease;
}

.custom-name-input:focus {
  border-color: var(--forest-600);
}

.custom-name-input:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 2px;
}

.custom-rules-panel {
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 14px;
  margin-bottom: 16px;
}

.rules-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.rules-title h3 {
  font-size: 13px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 0;
}

.rules-hint {
  margin: 0 0 10px 0;
  font-size: 11.5px;
  color: var(--slate-600);
  line-height: 1.45;
}

.rules-hint code {
  background: var(--slate-200);
  padding: 1px 5px;
  border-radius: var(--radius-xs);
  color: var(--slate-800);
  font-family: var(--font-mono);
}

/* Editor & Output */
.editor-wrapper, .output-wrapper {
  margin-bottom: 16px;
  flex: 1;
}

.code-editor {
  width: 100%;
  background: #0f172a;
  color: #e2e8f0;
  font-family: var(--font-mono);
  font-size: 12px;
  font-variant-numeric: tabular-nums;
  line-height: 1.6;
  padding: 14px;
  border-radius: var(--radius-sm);
  border: 1px solid #1e293b;
  resize: vertical;
  box-sizing: border-box;
}

.code-editor:focus {
  border-color: #3b82f6;
}

.code-editor:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.code-preview {
  margin: 0;
  background: #022c22;
  color: #86efac;
  font-family: var(--font-mono);
  font-size: 12px;
  font-variant-numeric: tabular-nums;
  line-height: 1.6;
  padding: 14px;
  border-radius: var(--radius-sm);
  border: 1px solid #064e3b;
  max-height: 380px;
  overflow: auto;
  box-sizing: border-box;
}

.schema-hint-box {
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  font-size: 12px;
  color: var(--slate-700);
  line-height: 1.5;
}

.hint-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--slate-800);
  display: block;
  margin-bottom: 4px;
}

.hint-text {
  margin: 0;
  font-family: var(--font-editorial);
  font-style: italic;
  font-size: 13px;
  color: var(--slate-700);
  line-height: 1.5;
}

.schema-hint-box code {
  background: var(--slate-200);
  padding: 1px 5px;
  border-radius: var(--radius-xs);
  color: var(--slate-900);
  font-style: normal;
  font-family: var(--font-mono);
}

/* Mapping Table */
.mapping-table-container {
  margin-bottom: 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.mapping-table-container h3 {
  padding: 10px 14px;
  background: var(--slate-50);
  border-bottom: 1px solid var(--color-border);
  font-size: 12.5px;
  font-weight: 700;
  color: var(--slate-800);
  margin: 0;
}

.mapping-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.mapping-table th, .mapping-table td {
  padding: 8px 14px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.mapping-table th {
  background: var(--bg-surface);
  color: var(--slate-500);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.mapping-table tr:last-child td {
  border-bottom: none;
}

.target-field {
  color: var(--forest-800);
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}

.audit-notes-box {
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  font-size: 12px;
}

.audit-notes-box h3 {
  font-size: 12px;
  font-weight: 700;
  color: var(--slate-800);
  margin: 0 0 6px 0;
}

.audit-list {
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
  background: rgba(15, 23, 42, 0.7);
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
  max-width: 720px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
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

.modal-head h2 {
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
  transition: background-color 0.15s ease, color 0.15s ease;
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
  overflow-y: auto;
}

.modal-desc {
  font-size: 13px;
  color: var(--slate-700);
  margin: 0 0 14px 0;
  line-height: 1.5;
}

.schema-code {
  background: #0f172a;
  color: #93c5fd;
  padding: 14px;
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-variant-numeric: tabular-nums;
  line-height: 1.55;
  max-height: 380px;
  overflow: auto;
  margin: 0;
}

.modal-foot {
  padding: 14px 22px;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: var(--slate-50);
}

@media (max-width: 1000px) {
  .split-workspace {
    grid-template-columns: 1fr;
  }
}
</style>
