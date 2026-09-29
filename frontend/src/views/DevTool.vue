<template>
  <div class="interop-shell">
    <!-- Header -->
    <header class="interop-header card-solid">
      <div class="header-left">
        <div class="dpg-badge-icon">
          <PhArrowsLeftRight :size="24" weight="bold" class="badge-icon-elem" />
        </div>
        <div>
          <div class="title-row">
            <h1>Registry converter</h1>
            <span class="badge-institutional badge-forest">Digital Public Good (DPG)</span>
          </div>
          <p class="subtitle">
            Harmonizing disparate state agricultural registries (West Bengal <em>Matir Katha</em>, Bihar <em>DBT Krishi</em>, Odisha <em>Krushak</em>) into the unified <code>in.gov.dpg.farmcontext.v1</code> schema.
          </p>
        </div>
      </div>

      <div class="header-right">
        <button type="button" @click="showSchemaModal = true" class="btn-gov-outline" style="min-height: 48px;">
          <PhFileCode :size="18" weight="bold" />
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
        <button type="button" @click="loadSample" class="btn-gov-outline" :disabled="isLoading" style="min-height: 48px;">
          <PhArrowsClockwise :size="18" weight="bold" />
          <span>Reset Sample Payload</span>
        </button>
        <button type="button" @click="runNormalization" class="btn-gov-primary" :disabled="isLoading" style="min-height: 48px;">
          <PhArrowsClockwise v-if="isLoading" :size="18" weight="bold" class="spin" />
          <PhArrowsLeftRight v-else :size="18" weight="bold" />
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
            <h2>State registry data</h2>
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

        <div class="editor-wrapper" :class="{ 'anim-highlight': isHighlighting }">
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
            <h2>Standard FarmContext</h2>
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
              <tr 
                v-for="(target, src) in normalizedResponse.field_mappings_applied" 
                :key="src"
                :class="{ 'anim-highlight': isHighlighting }"
              >
                <td><code>{{ src }}</code></td>
                <td><strong class="target-field">{{ target }}</strong></td>
                <td><span class="badge-institutional badge-forest">[Normalized]</span></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Normalized JSON Inspector -->
        <div class="output-wrapper" :class="{ 'anim-highlight': isHighlighting }">
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
            <PhX :size="20" weight="bold" />
          </button>
        </div>
        <div class="modal-body">
          <p class="modal-desc">
            This open specification enables any Indian State (e.g. Odisha, Punjab, Karnataka) or research institute to publish and consume interoperable agricultural intelligence.
          </p>
          <pre class="schema-code"><code>{{ schemaJsonString }}</code></pre>
        </div>
        <div class="modal-foot">
          <button type="button" @click="copySchema" class="btn-gov-primary" style="min-height: 48px;">
            <span>{{ copySuccess ? 'Copied to Clipboard' : 'Copy JSON Schema' }}</span>
          </button>
          <button type="button" @click="showSchemaModal = false" class="btn-gov-outline" style="min-height: 48px;">Close</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { PhArrowsLeftRight, PhFileCode, PhArrowsClockwise, PhX } from '@phosphor-icons/vue'
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
const isHighlighting = ref(false)
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
          "ph": { "type": "number" }
        }
      },
      "weather": {
        "type": "object",
        "properties": {
          "temperature_c": { "type": "number" },
          "relative_humidity_pct": { "type": "number" }
        }
      },
      "satellite": {
        "type": "object",
        "properties": {
          "ndvi": { "type": "number" },
          "tile_reference": { "type": "string" }
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
  normalizedResponse.value = null
  try {
    const data = await fetchSampleStatePayload(selectedState.value)
    rawPayload.value = data
    rawPayloadString.value = JSON.stringify(data, null, 2)
  } catch (err) {
    console.error('Failed to load sample state payload:', err)
  } finally {
    isLoading.value = false
  }
}

async function runNormalization() {
  isLoading.value = true
  isHighlighting.value = true
  try {
    let payloadToNormalize = {}
    try {
      payloadToNormalize = JSON.parse(rawPayloadString.value)
    } catch {
      alert('Invalid JSON in State Payload Editor')
      isLoading.value = false
      isHighlighting.value = false
      return
    }

    let customRules = null
    if (selectedState.value === 'custom') {
      try {
        customRules = JSON.parse(customRulesString.value)
      } catch {
        alert('Invalid JSON in Custom Declarative Rules Editor')
        isLoading.value = false
        isHighlighting.value = false
        return
      }
    }

    const res = await normalizeStatePayload(
      selectedState.value, 
      payloadToNormalize, 
      selectedState.value === 'custom' ? customStateName.value : null,
      customRules
    )
    normalizedResponse.value = res
  } catch (err) {
    console.error('Normalization failed:', err)
    alert('Normalization error: ' + err.message)
  } finally {
    isLoading.value = false
    setTimeout(() => {
      isHighlighting.value = false
    }, 900)
  }
}

function copySchema() {
  navigator.clipboard.writeText(schemaJsonString.value)
  copySuccess.value = true
  setTimeout(() => {
    copySuccess.value = false
  }, 3000)
}
</script>

<style scoped>
.interop-shell {
  padding: var(--space-6) var(--space-5);
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* Header */
.interop-header {
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

.dpg-badge-icon {
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
  max-width: 75ch;
}

.subtitle code {
  background: var(--paper-sunken);
  padding: 2px 6px;
  border-radius: var(--radius-xs);
  color: var(--ink);
  font-family: var(--font-mono);
  font-size: 0.8125rem;
}

/* State Control Bar */
.state-control-bar {
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-md);
  border: 1px solid var(--hairline);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.state-pills {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.control-label {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink-2);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-right: 4px;
}

/* State tabs are large pills (min 48px) */
.state-tab-btn {
  background: var(--paper-sunken);
  border: 1.5px solid var(--hairline);
  color: var(--ink-2);
  font-size: 0.8125rem;
  font-weight: 700;
  min-height: 48px;
  padding: 0 var(--space-4);
  border-radius: var(--radius-pill);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  transition: background-color 120ms, border-color 120ms, transform 120ms, color 120ms;
}

.state-tab-btn:hover {
  background: var(--paper);
  border-color: var(--hairline-strong);
  transform: translateY(-1px);
}

.state-tab-btn:active {
  transform: translateY(1px);
}

.state-tab-btn:focus-visible {
  outline: 3px solid var(--canopy);
  outline-offset: 2px;
}

.state-tab-btn.active {
  background: var(--sarson);
  color: var(--canopy);
  border-color: var(--canopy);
}

.state-tag {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink-3);
}

.state-tab-btn.active .state-tag {
  color: var(--canopy);
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

/* Dual Split View */
.split-workspace {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
}

.panel-left, .panel-right {
  padding: var(--space-5);
  border-radius: var(--radius-md);
  border: 1px solid var(--hairline);
  display: flex;
  flex-direction: column;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--hairline);
}

.panel-head h2 {
  font-size: var(--step-1);
  font-weight: 800;
  color: var(--ink);
  margin: 0 0 var(--space-1) 0;
}

.portal-badge {
  font-size: 0.8125rem;
  color: var(--leaf);
  font-weight: 600;
}

.standard-badge {
  font-size: 0.8125rem;
  color: var(--canopy);
  font-weight: 600;
}

/* Custom State & Declarative Rules Editor */
.custom-state-config {
  margin-bottom: var(--space-3);
}

.custom-field-row {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.custom-label {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink-2);
}

.custom-name-input {
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--hairline-strong);
  font-size: var(--step-0);
  color: var(--ink);
  background: var(--paper-raised);
  transition: border-color 120ms;
}

.custom-name-input:focus-visible {
  outline: 3px solid var(--canopy);
  outline-offset: 2px;
}

.custom-rules-panel {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  margin-bottom: var(--space-4);
}

.rules-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.rules-title h3 {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--ink);
  margin: 0;
}

.rules-hint {
  margin: 0 0 var(--space-2) 0;
  font-size: 0.8125rem;
  color: var(--ink-2);
  line-height: 1.45;
}

.rules-hint code {
  background: var(--paper-raised);
  padding: 2px 6px;
  border-radius: var(--radius-xs);
  color: var(--ink);
  font-family: var(--font-mono);
}

/* Editor & Output */
.editor-wrapper, .output-wrapper {
  margin-bottom: var(--space-4);
  flex: 1;
}

.code-editor {
  width: 100%;
  background: var(--inkwell);
  color: var(--paper-raised);
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-variant-numeric: tabular-nums;
  line-height: 1.6;
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  border: 1px solid var(--inkwell-line);
  resize: vertical;
  box-sizing: border-box;
}

.code-editor:focus-visible {
  outline: 3px solid var(--sarson);
  outline-offset: 2px;
}

.code-preview {
  margin: 0;
  background: var(--inkwell-2);
  color: var(--green-wash);
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-variant-numeric: tabular-nums;
  line-height: 1.6;
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  border: 1px solid var(--inkwell-line);
  max-height: 380px;
  overflow: auto;
  box-sizing: border-box;
}

/* 900ms transform and opacity animation for conversion highlight */
@keyframes convertTransfer {
  0% {
    opacity: 0.3;
    transform: translateY(6px);
  }
  50% {
    opacity: 1;
    transform: translateY(-2px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.anim-highlight {
  animation: convertTransfer 850ms ease-out forwards;
}

@media (prefers-reduced-motion: reduce) {
  .anim-highlight {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
}

.schema-hint-box {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  font-size: 0.8125rem;
  color: var(--ink-2);
  line-height: 1.5;
}

.hint-title {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink);
  display: block;
  margin-bottom: 4px;
}

.hint-text {
  margin: 0;
  font-style: italic;
  font-size: 0.8125rem;
  color: var(--ink-2);
  line-height: 1.5;
}

.schema-hint-box code {
  background: var(--paper-raised);
  padding: 1px 5px;
  border-radius: var(--radius-xs);
  color: var(--ink);
  font-style: normal;
  font-family: var(--font-mono);
}

/* Mapping Table */
.mapping-table-container {
  margin-bottom: var(--space-4);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.mapping-table-container h3 {
  padding: var(--space-2) var(--space-3);
  background: var(--paper-sunken);
  border-bottom: 1px solid var(--hairline);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink);
  margin: 0;
}

.mapping-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8125rem;
}

.mapping-table th, .mapping-table td {
  padding: var(--space-2) var(--space-3);
  text-align: left;
  border-bottom: 1px solid var(--hairline);
}

.mapping-table th {
  background: var(--paper);
  color: var(--ink-3);
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.mapping-table tr:last-child td {
  border-bottom: none;
}

.target-field {
  color: var(--canopy);
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
}

.audit-notes-box {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  font-size: 0.8125rem;
}

.audit-notes-box h3 {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 var(--space-1) 0;
}

.audit-list {
  margin: 0;
  padding-left: var(--space-4);
  color: var(--ink-2);
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
  background: rgba(10, 47, 34, 0.7);
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
  max-width: 720px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
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
  overflow-y: auto;
}

.modal-desc {
  font-size: var(--step-0);
  color: var(--ink-2);
  margin: 0 0 var(--space-3) 0;
  line-height: 1.5;
}

.schema-code {
  background: var(--inkwell);
  color: var(--green-wash);
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-variant-numeric: tabular-nums;
  line-height: 1.55;
  max-height: 380px;
  overflow: auto;
  margin: 0;
}

.modal-foot {
  padding: var(--space-3) var(--space-5);
  border-top: 1px solid var(--hairline);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  background: var(--paper);
}

@media (max-width: 1000px) {
  .split-workspace {
    grid-template-columns: 1fr;
  }
}
</style>
