<template>
  <div class="app-container">
    <!-- KrishiSetu Global Header Navigation -->
    <header class="krishi-nav">
      <div class="nav-left">
        <router-link to="/" class="brand-link">
          <!-- Institutional Brand Logo Frame -->
          <div class="brand-logo-frame">
            <PhPlant :size="24" weight="bold" class="brand-icon" />
          </div>
          <div class="brand-text">
            <div class="brand-title-row">
              <span class="brand-title">KrishiSetu</span>
              <span class="brand-subtitle">कृषि-सेतु</span>
            </div>
            <span class="brand-caption">Interoperable Digital Public Good · ICAR/GOI Standard</span>
          </div>
        </router-link>
      </div>

      <nav class="nav-links">
        <router-link to="/sathi" class="nav-item">
          <PhPlant :size="18" weight="bold" class="nav-icon" />
          <span>Check a leaf</span>
        </router-link>

        <router-link to="/interop" class="nav-item">
          <PhArrowsLeftRight :size="18" weight="bold" class="nav-icon" />
          <span>Registry converter</span>
        </router-link>

        <router-link to="/command" class="nav-item">
          <PhBroadcast :size="18" weight="bold" class="nav-icon" />
          <span>Outbreak watch</span>
        </router-link>
      </nav>

      <div class="nav-right">
        <!-- Resilient Offline Network Simulation Switch -->
        <button 
          type="button"
          @click="toggleOfflineSimulation" 
          class="offline-toggle-btn" 
          :class="{ 'is-offline': !isOnline }"
          aria-label="Toggle network simulation to test IndexedDB offline resilience"
        >
          <span class="status-marker" :class="{ 'marker-offline': !isOnline }"></span>
          <span class="status-label">{{ isOnline ? 'Network: Online' : 'Network: Offline (IndexedDB Active)' }}</span>
          <span class="status-mode-tag">{{ isOfflineSimulation ? 'SIMULATION' : 'REAL' }}</span>
        </button>
      </div>
    </header>

    <!-- Main View Outlet -->
    <main class="main-viewport">
      <router-view />
    </main>

    <!-- Institutional Footer with Public Good Terms of Service & Privacy Policy -->
    <footer class="site-footer">
      <div class="footer-content">
        <div class="footer-left">
          <span class="badge-institutional badge-forest">DPG Standard v1.0</span>
          <span>KrishiSetu is an open-source Digital Public Good under ICAR & Ministry of Agriculture and Farmers Welfare specifications.</span>
        </div>
        <div class="footer-links">
          <button type="button" @click="activeModal = 'tos'" class="footer-link-btn">Terms of Service (DPG License)</button>
          <span>·</span>
          <button type="button" @click="activeModal = 'privacy'" class="footer-link-btn">Farmer Privacy Policy (DPDP Act 2023)</button>
          <span>·</span>
          <button type="button" @click="activeModal = 'standards'" class="footer-link-btn">DPG Schema Spec</button>
        </div>
      </div>
    </footer>

    <!-- Governance Modal Dialog -->
    <div v-if="activeModal" class="modal-backdrop" @click="activeModal = null">
      <div class="modal-card" @click.stop>
        <div class="modal-header">
          <div class="modal-title-row">
            <span class="badge-institutional badge-slate">Compliance & Governance</span>
            <h3>{{ modalTitle }}</h3>
          </div>
          <button type="button" @click="activeModal = null" class="btn-modal-close" aria-label="Close dialog">
            <PhX :size="20" weight="bold" />
          </button>
        </div>

        <div class="modal-body">
          <!-- Terms of Service Content -->
          <div v-if="activeModal === 'tos'" class="legal-text-block">
            <h4>1. Open Digital Public Good Framework</h4>
            <p>
              KrishiSetu is released as a Digital Public Good adhering to the Digital Public Goods Standard. All core data schemas (<code>in.gov.dpg.farmcontext.v1</code>) and cross-state adapters are licensed under the Apache 2.0 and Creative Commons Attribution 4.0 International license.
            </p>
            <h4>2. Clinical Agronomic Decision Support Disclaimer</h4>
            <p>
              The diagnostic outputs, satellite spectral indices, and generative advisory summaries provided by KrishiSetu represent assistive decision support grounded in ICAR and FAO research monographs. Recommendations are intended to aid smallholder farmers and extension officers. Always verify chemical or cultural interventions with local Block Agricultural Officers (BAO) or Krishi Vigyan Kendra (KVK) scientists before large-scale application.
            </p>
            <h4>3. Cross-State Interoperability Principles</h4>
            <p>
              Participating state registries (e.g., West Bengal Matir Katha, Bihar DBT Krishi, Odisha Krushak) retain sovereign ownership over their agricultural databases. KrishiSetu executes client-side and federated normalization without centralizing proprietary farmer land titles.
            </p>
          </div>

          <!-- Privacy Policy Content -->
          <div v-else-if="activeModal === 'privacy'" class="legal-text-block">
            <h4>1. Compliance with Digital Personal Data Protection (DPDP) Act, 2023</h4>
            <p>
              KrishiSetu is engineered around the principle of strict data minimization. Farmer personal identifiers (such as Aadhaar or direct biometric records) are never stored on public cloud servers. All local records are indexed locally within the client browser using IndexedDB.
            </p>
            <h4>2. Audio and Image Processing Telemetry</h4>
            <p>
              Photographs of crop leaves submitted for multimodal pathology diagnosis are processed via zero-retention enterprise inference endpoints. Voice transcripts recorded in regional languages (Bengali, Hindi) are converted into structured diagnostic query parameters and are not utilized for advertising profiling or commercial monetization.
            </p>
            <h4>3. Right to Erasure & Offline Autonomy</h4>
            <p>
              Farmers and extension officers may purge all cached telemetry, diagnoses, and offline advisories at any point via the IndexedDB storage panel.
            </p>
          </div>

          <!-- DPG Specification Content -->
          <div v-else-if="activeModal === 'standards'" class="legal-text-block">
            <h4>Digital Public Good Schema: in.gov.dpg.farmcontext.v1</h4>
            <p>
              The standard interoperability contract ensures that heterogeneous regional state registries ingest into a unified canonical JSON schema:
            </p>
            <pre class="schema-code-box"><code>{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "FarmContext",
  "standard": "in.gov.dpg.farmcontext.v1",
  "contract": {
    "farmer": { "farmer_id": "string", "name": "string", "language": "bn|hi|en" },
    "location": { "state": "string", "district": "string", "coordinates": { "lat": "number", "lon": "number" } },
    "soil_health": { "nitrogen_kg_ha": "number", "ph": "number", "organic_carbon_pct": "number" },
    "satellite": { "tile_reference": "string", "spectral_formula": "string", "ndvi": "number" }
  }
}</code></pre>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" @click="activeModal = null" class="btn-gov-primary">Acknowledge</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { PhPlant, PhArrowsLeftRight, PhBroadcast, PhX } from '@phosphor-icons/vue'
import { useOfflineStorage } from './composables/useOfflineStorage'

const { isOnline, isOfflineSimulation, setOfflineSimulation } = useOfflineStorage()

const activeModal = ref(null)

const modalTitle = computed(() => {
  if (activeModal.value === 'tos') return 'Terms of Service (Digital Public Good Charter)'
  if (activeModal.value === 'privacy') return 'Farmer Data Sovereignty & Privacy Policy'
  if (activeModal.value === 'standards') return 'DPG Canonical Architecture Specification'
  return ''
})

function toggleOfflineSimulation() {
  setOfflineSimulation(!isOfflineSimulation.value)
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-canvas);
  font-family: var(--font-sans);
}

/* Institutional Navigation Header */
.krishi-nav {
  min-height: 64px;
  background: var(--inkwell);
  border-bottom: 1px solid var(--inkwell-line);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-6);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.brand-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  text-decoration: none;
}

.brand-logo-frame {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background: var(--sarson);
  color: var(--canopy);
  border: 1.5px solid var(--canopy);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-icon {
  color: var(--canopy);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title-row {
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
}

.brand-title {
  color: var(--paper-raised);
  font-size: var(--step-1);
  font-weight: 800;
  letter-spacing: -0.02em;
}

.brand-subtitle {
  color: var(--sarson);
  font-size: var(--step-0);
  font-weight: 700;
}

.brand-caption {
  color: var(--green-line);
  font-size: var(--step-0);
  letter-spacing: 0.01em;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: var(--inkwell-2);
  border: 1px solid var(--inkwell-line);
  border-radius: var(--radius-pill);
  padding: var(--space-1);
}

.nav-item {
  color: var(--inkwell-text);
  text-decoration: none;
  font-size: var(--step-0);
  font-weight: 600;
  padding: 8px 18px;
  border-radius: var(--radius-pill);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  transition: background-color 120ms, color 120ms, transform 120ms;
  border: 1px solid transparent;
}

.nav-item:hover {
  color: var(--paper-raised);
  background: var(--inkwell-line);
}

.nav-item:active {
  transform: translateY(1px);
}

.nav-item:focus-visible {
  outline: 3px solid var(--sarson);
  outline-offset: 2px;
}

.nav-item.router-link-exact-active {
  color: var(--canopy);
  background: var(--sarson);
  border-color: var(--canopy);
  font-weight: 700;
}

.nav-right {
  display: flex;
  align-items: center;
}

.offline-toggle-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: var(--inkwell-2);
  color: var(--inkwell-text);
  border: 1.5px solid var(--inkwell-line);
  border-radius: var(--radius-pill);
  padding: 8px 16px;
  font-size: var(--step-0);
  font-weight: 600;
  cursor: pointer;
  transition: background-color 120ms, border-color 120ms, transform 120ms;
}

.offline-toggle-btn:hover {
  background: var(--inkwell-line);
}

.offline-toggle-btn:active {
  transform: translateY(1px);
}

.offline-toggle-btn:focus-visible {
  outline: 3px solid var(--sarson);
  outline-offset: 2px;
}

.status-marker {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-pill);
  background: var(--leaf-bright);
}

.status-marker.marker-offline {
  background: var(--alert);
}

.status-mode-tag {
  font-family: var(--font-mono);
  font-size: var(--step-0);
  background: var(--canopy);
  border: 1px solid var(--inkwell-line);
  color: var(--sarson);
  padding: 2px 6px;
  border-radius: var(--radius-xs);
}

.offline-toggle-btn.is-offline {
  background: var(--brick);
  border-color: var(--brick-line);
  color: var(--paper-raised);
}

.main-viewport {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Modal Dialog */
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
  border: 1px solid var(--hairline-strong);
  border-radius: var(--radius-md);
  width: 100%;
  max-width: 680px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--hairline);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--paper);
}

.modal-title-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.btn-modal-close {
  background: none;
  border: none;
  padding: var(--space-1);
  cursor: pointer;
  color: var(--ink-2);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: color 120ms, background-color 120ms;
}

.btn-modal-close:hover {
  color: var(--ink);
  background: var(--paper-sunken);
}

.modal-body {
  padding: var(--space-5);
  overflow-y: auto;
  font-size: var(--step-0);
  line-height: 1.6;
}

.legal-text-block h4 {
  font-size: var(--step-1);
  font-weight: 700;
  color: var(--ink);
  margin: var(--space-4) 0 var(--space-2) 0;
}

.legal-text-block h4:first-child {
  margin-top: 0;
}

.legal-text-block p {
  margin-bottom: var(--space-3);
  color: var(--ink-2);
}

.schema-code-box {
  background: var(--inkwell);
  color: var(--green-wash);
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  border: 1px solid var(--inkwell-line);
  font-size: var(--step-0);
  overflow-x: auto;
}

.modal-footer {
  padding: var(--space-3) var(--space-5);
  border-top: 1px solid var(--hairline);
  display: flex;
  justify-content: flex-end;
  background: var(--paper);
}

@media (max-width: 900px) {
  .krishi-nav {
    min-height: auto;
    padding: var(--space-3) var(--space-4);
    flex-wrap: wrap;
    gap: var(--space-3);
  }
  .nav-links {
    order: 3;
    width: 100%;
    overflow-x: auto;
  }
}
</style>
