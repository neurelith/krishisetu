<template>
  <div class="app-container">
    <!-- KrishiSetu Global Header Navigation -->
    <header class="krishi-nav">
      <div class="nav-left">
        <router-link to="/" class="brand-link">
          <!-- Institutional SVG Logo -->
          <div class="brand-logo-frame">
            <svg class="brand-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" role="img" aria-label="KrishiSetu ICAR Emblem">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v18M12 3c-4.5 0-7 3.5-7 8 0 4 3 7 7 10M12 3c4.5 0 7 3.5 7 8 0 4-3 7-7 10" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9c2-1.5 4-1.5 6 0M6 13c2-1.5 4-1.5 6 0" />
            </svg>
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
        <router-link to="/" class="nav-item">
          <svg class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
          </svg>
          <span>Kisan Sathi (Farmer Advisory)</span>
        </router-link>

        <router-link to="/interop" class="nav-item">
          <svg class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21L3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
          </svg>
          <span>Kisan Setu (Cross-State Registry)</span>
        </router-link>

        <router-link to="/command" class="nav-item">
          <svg class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <circle cx="12" cy="12" r="9" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3a9 9 0 0 1 9 9m-9 9a9 9 0 0 1-9-9" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 12l4-4" />
          </svg>
          <span>Kisan Rakshak (Corridor Telemetry)</span>
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
            <svg class="close-svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
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
    "location": { "state": "string", "district": "string", "coordinates": { "lat": "number|null", "lon": "number|null" } },
    "soil_health": { "nitrogen_kg_ha": "number", "ph": "number", "organic_carbon_pct": "number" },
    "satellite": { "available": "boolean", "source": "string", "observation_date": "string|null", "ndvi": "number|null", "vegetation_status": "string|null", "clear_pixel_pct": "number|null", "reason": "string|null" }
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
  font-family: var(--font-swiss);
}

/* Institutional Navigation Header */
.krishi-nav {
  height: 64px;
  background: #0f172a;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.brand-logo-frame {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--forest-900);
  border: 1px solid var(--forest-700);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #86efac;
  flex-shrink: 0;
}

.brand-svg {
  width: 22px;
  height: 22px;
  stroke-width: 1.8;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.brand-title {
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.brand-subtitle {
  color: #86efac;
  font-size: 11px;
  font-weight: 600;
}

.brand-caption {
  color: #94a3b8;
  font-size: 10.5px;
  letter-spacing: 0.01em;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 9999px;
  padding: 4px;
}

.nav-item {
  color: #94a3b8;
  text-decoration: none;
  font-size: 12.5px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.15s ease, border-color 0.15s ease;
  border: 1px solid transparent;
}

.nav-item:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.06);
}

.nav-item:active {
  transform: scale(0.97);
}

.nav-item:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

.nav-item.router-link-exact-active {
  color: #ffffff;
  background: #0f172a;
  border-color: rgba(255, 255, 255, 0.18);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
  font-weight: 600;
}

.nav-right {
  display: flex;
  align-items: center;
}

.offline-toggle-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #1e293b;
  color: #e2e8f0;
  border: 1px solid #334155;
  border-radius: 9999px;
  padding: 6px 14px;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s ease, transform 0.15s ease;
}

.offline-toggle-btn:hover {
  background: #273549;
}

.offline-toggle-btn:active {
  transform: scale(0.97);
}

.offline-toggle-btn:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

.status-marker {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
}

.status-marker.marker-offline {
  background: #f97316;
}

.status-mode-tag {
  font-family: var(--font-mono);
  font-size: 9.5px;
  background: #0f172a;
  border: 1px solid #334155;
  color: #94a3b8;
  padding: 1px 5px;
  border-radius: var(--radius-xs);
}

.offline-toggle-btn.is-offline {
  background: #3a1a08;
  border-color: #78350f;
  color: #fed7aa;
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
  background: rgba(15, 23, 42, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-card {
  background: #ffffff;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  width: 100%;
  max-width: 680px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 14px 20px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-canvas);
}

.modal-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-modal-close {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: var(--slate-500);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: color 0.15s ease, background-color 0.15s ease;
}

.btn-modal-close:hover {
  color: var(--slate-800);
  background: var(--slate-100);
}

.close-svg-icon {
  width: 16px;
  height: 16px;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  font-size: 13px;
  line-height: 1.6;
}

.legal-text-block h4 {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 14px 0 6px 0;
}

.legal-text-block h4:first-child {
  margin-top: 0;
}

.legal-text-block p {
  margin-bottom: 12px;
  color: var(--slate-700);
}

.schema-code-box {
  background: #0f172a;
  color: #93c5fd;
  padding: 12px;
  border-radius: var(--radius-sm);
  font-size: 11.5px;
  overflow-x: auto;
}

.modal-footer {
  padding: 12px 20px;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
  background: var(--bg-canvas);
}

@media (max-width: 900px) {
  .krishi-nav {
    height: auto;
    padding: 10px 16px;
    flex-wrap: wrap;
    gap: 10px;
  }
  .nav-links {
    order: 3;
    width: 100%;
    overflow-x: auto;
  }
}
</style>
