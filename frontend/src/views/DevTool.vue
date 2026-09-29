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

      <div class="control-divider" aria-hidden="true"></div>

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
        <div v-if="normalizedResponse" class="output-wrapper" :class="{ 'anim-highlight': isHighlighting }">
          <pre class="code-preview"><code>{{ formattedNormalizedJson }}</code></pre>
        </div>

        <!-- Standby Blueprint when not yet normalized -->
        <div v-else class="output-standby-guide">
          <div class="standby-schema-preview">
            <span class="preview-tag">CANONICAL TARGET ARCHITECTURE</span>
            <h4>in.gov.dpg.farmcontext.v1</h4>
            <p class="preview-sub">
              Transforms heterogeneous, regional state registry dialects into an immutable, verifiable Digital Public Good payload format.
            </p>
            <div class="schema-tree">
              <div class="tree-node"><span>├── farmer:</span> <small>{ name, preferred_language, id }</small></div>
              <div class="tree-node"><span>├── location:</span> <small>{ state, district, lat, lon }</small></div>
              <div class="tree-node"><span>├── crop:</span> <small>{ name, variety, season, stage }</small></div>
              <div class="tree-node"><span>├── soil_health:</span> <small>{ ph, n_kg_ha, p_kg_ha, k_kg_ha }</small></div>
              <div class="tree-node"><span>├── weather:</span> <small>{ temp_c, humidity_pct, rainfall }</small></div>
              <div class="tree-node"><span>└── satellite:</span> <small>{ ndvi, sentinel2_granule }</small></div>
            </div>
            <div class="standby-callout">
              <span>Ready for translation · Click "Normalize into Common DPG Contract" above.</span>
            </div>
          </div>
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
import '../styles/devtool.css'
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
