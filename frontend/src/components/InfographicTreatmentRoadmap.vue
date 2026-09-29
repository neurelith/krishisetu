<template>
  <div class="treatment-roadmap-container">
    <div class="roadmap-head-bar">
      <div>
        <span class="sub-label">Regenerative Chronology & Dosing Plan</span>
        <h4 class="roadmap-title">Phased Agronomic Bio-Intervention Roadmap</h4>
      </div>
      <span class="badge-institutional badge-forest">4-Stage Chronological Protocol</span>
    </div>

    <!-- Apple-Grade Segmented Chronological Phase Selector -->
    <div class="timeline-segmented-bar" role="tablist" aria-label="Chronological Treatment Stages">
      <button 
        v-for="(phase, pIdx) in phases" 
        :key="pIdx"
        type="button"
        role="tab"
        :aria-selected="activePhaseIdx === pIdx"
        :aria-controls="'phase-panel-' + pIdx"
        class="timeline-segment-btn"
        :class="{ 'is-active-segment': activePhaseIdx === pIdx }"
        @click="activePhaseIdx = pIdx"
      >
        <div class="segment-step-row">
          <span class="segment-number">Stage {{ phase.stepNumber }}</span>
          <span class="segment-priority-pip" :class="phase.badgeClass"></span>
        </div>
        <span class="segment-time-label" v-text="phase.timeWindow"></span>
        <span class="segment-title-label" v-text="phase.shortTitle"></span>
      </button>
    </div>

    <!-- Active Protocol Execution Deck (Asymmetrical Spec Sheet) -->
    <div 
      :id="'phase-panel-' + activePhaseIdx" 
      class="active-protocol-deck"
      role="tabpanel"
    >
      <!-- Deck Masthead -->
      <div class="deck-masthead">
        <div class="masthead-left">
          <div class="deck-phase-stamp">
            <span class="badge-institutional badge-slate">STAGE {{ activePhase.stepNumber }} OF 4</span>
            <span class="time-window-callout" v-text="activePhase.timeWindow"></span>
          </div>
          <h5 class="active-deck-title" v-text="activePhase.title"></h5>
        </div>
        <div class="priority-flag-pill" :class="activePhase.badgeClass">
          <span v-text="activePhase.priority"></span> ACTION
        </div>
      </div>

      <!-- Asymmetrical 2-Column Deck Grid: 60% Execution / 40% Spec Sheet -->
      <div class="deck-grid-asym">
        
        <!-- Left Column: Biological Mechanism & Step-by-Step Protocol -->
        <div class="deck-execution-col">
          <!-- Biological Target Callout -->
          <div class="biological-target-panel">
            <div class="panel-header-mini">
              <svg class="svg-icon-sm text-forest" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
                <circle cx="12" cy="12" r="9" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v8m-4-4h8" />
              </svg>
              <span class="panel-kicker">Biological Mode of Action</span>
            </div>
            <p class="target-narrative font-editorial-italic">
              "<span v-text="activePhase.biologicalTarget"></span>"
            </p>
          </div>

          <!-- Application Protocol & Rules -->
          <div class="application-rules-panel">
            <span class="panel-kicker">Field Application Protocol & Rules</span>
            <div class="numbered-rules-list">
              <div 
                v-for="(rule, rIdx) in activePhase.applicationRules" 
                :key="rIdx" 
                class="rule-row"
              >
                <span class="rule-index">{{ rIdx + 1 }}</span>
                <span class="rule-text" v-text="rule"></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Prescribed Formulation & Operational Specs -->
        <div class="deck-specs-col">
          <div class="specs-card-inner">
            <div class="specs-header">
              <svg class="svg-icon-sm text-sky" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3" />
              </svg>
              <span class="panel-kicker">Prescribed Input Specification</span>
            </div>

            <div class="formulation-highlight-box">
              <span class="formulation-label">Active Formulation</span>
              <strong class="formulation-name" v-text="activePhase.formulation"></strong>
            </div>

            <div class="specs-data-grid">
              <div class="spec-data-item">
                <span class="data-key">Application Rate</span>
                <span class="data-val text-sky" v-text="activePhase.dosingRate"></span>
              </div>

              <div class="spec-data-item">
                <span class="data-key">Input Cost Estimate</span>
                <span class="data-val text-forest" v-text="activePhase.costLevel"></span>
              </div>

              <div class="spec-data-item">
                <span class="data-key">Chemical Compatibility</span>
                <span class="data-val text-alert">Do NOT mix with copper/synthetic fungicides</span>
              </div>

              <div class="spec-data-item">
                <span class="data-key">Ecological Residue</span>
                <span class="data-val text-forest">0 days (100% Organic & Bio-Safe)</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activePhaseIdx = ref(0)

const phases = [
  {
    stepNumber: '01',
    timeWindow: 'Hour 00:00 - 24:00',
    shortTitle: 'Bio-Shield Inoculation',
    title: 'Immediate Bio-Shield Inoculation',
    priority: 'CRITICAL',
    badgeClass: 'badge-alert',
    biologicalTarget: 'Halt active zoospore motility and occupy leaf phyllosphere before stomatal cuticular breach occurs.',
    formulation: 'Trichoderma harzianum (2x10^9 CFU/g) + Bio-Surfactant',
    dosingRate: '5.0 g / L water (Knapsack sprayer with hollow-cone nozzle)',
    costLevel: 'Low (₹420 / acre)',
    applicationRules: [
      'Apply strictly during morning calm window (06:30 - 09:30 AM) when stomata are receptive.',
      'Target leaf undersides where microclimate humidity accumulates and sporangia emerge.',
      'Keep nozzle pressure at 2.5 bar for uniform droplet distribution without leaf runoff.'
    ]
  },
  {
    stepNumber: '02',
    timeWindow: 'Day 02 - 03',
    shortTitle: 'Epidermal Hardening',
    title: 'Epidermal Hardening & Foliar Potassium',
    priority: 'HIGH PRIORITY',
    badgeClass: 'badge-soil',
    biologicalTarget: 'Reinforce leaf epidermal cell walls with soluble potassium and silica to prevent secondary mycelial spread.',
    formulation: 'Potassium Sulfate (0-0-50 SOP) + Azadirachtin (1500 ppm)',
    dosingRate: '3.0 g / L Potassium Sulfate + 2.5 ml / L Neem extract',
    costLevel: 'Moderate (₹680 / acre)',
    applicationRules: [
      'Ensure soil has minimum moisture before foliar nutrition mist to avoid osmotic shock.',
      'Neem provides secondary anti-feedant barrier against leaf-puncturing insect vectors.',
      'Verify spray solution pH is buffered between 6.0 and 6.5 for optimal cellular uptake.'
    ]
  },
  {
    stepNumber: '03',
    timeWindow: 'Day 05 - 07',
    shortTitle: 'Canopy Audit',
    title: 'Canopy Audit & Sporulation Clearance',
    priority: 'VERIFICATION',
    badgeClass: 'badge-slate',
    biologicalTarget: 'Inspect lesion margins; verify white velvety downy ring has dried out into non-sporulating brown necrotic crust.',
    formulation: 'Botanical Fermented Bio-Wash (Dashaparni Arka / Cow urine extract)',
    dosingRate: '20 ml / L clean water',
    costLevel: 'Minimal (₹180 / acre)',
    applicationRules: [
      'Physically prune severely blighted lower senescent leaves into sealed biodegradable bags.',
      'Never compost blighted crop debris near active irrigation canals or field perimeters.',
      'Re-check microclimate humidity; if ambient RH remains above 85%, repeat Bio-Shield application.'
    ]
  },
  {
    stepNumber: '04',
    timeWindow: 'Day 10+',
    shortTitle: 'Rhizosphere Healing',
    title: 'Rhizosphere Inoculation & Drip Calibration',
    priority: 'RECOVERY',
    badgeClass: 'badge-forest',
    biologicalTarget: 'Replenish beneficial root mycorrhizae and aerate soil to prevent root asphyxiation from excess saturation.',
    formulation: 'VAM (Vesicular Arbuscular Mycorrhizae) + Humic Bio-Extract',
    dosingRate: '2.0 kg / acre mixed with vermicompost or delivered via drip',
    costLevel: 'Moderate (₹750 / acre)',
    applicationRules: [
      'Reduce irrigation duration by 20% to drain excess pore water and restore aerobic balance.',
      'Deep root mycorrhizal colonization unlocks fixed soil phosphorus pools naturally.',
      'Ensures vigorous canopy recovery without triggering excessive synthetic nitrate surge.'
    ]
  }
]

const activePhase = computed(() => phases[activePhaseIdx.value])
</script>

<style scoped>
.treatment-roadmap-container {
  padding: 20px 24px;
  background: var(--bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  margin-top: 20px;
}

.roadmap-head-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.sub-label {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--slate-500);
  letter-spacing: 0.05em;
  display: block;
}

.roadmap-title {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 2px 0 0 0;
}

/* Apple-Style Segmented Stepper Bar */
.timeline-segmented-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  background: var(--slate-100);
  padding: 5px;
  border-radius: var(--radius-md);
  border: 1px solid var(--slate-200);
  margin-bottom: 16px;
}

.timeline-segment-btn {
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

.timeline-segment-btn:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

.timeline-segment-btn:hover {
  background: rgba(255, 255, 255, 0.6);
}

.timeline-segment-btn.is-active-segment {
  background: #ffffff;
  border-color: rgba(15, 23, 42, 0.15);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.segment-step-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.segment-number {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  color: var(--slate-500);
  text-transform: uppercase;
}

.timeline-segment-btn.is-active-segment .segment-number {
  color: var(--forest-800);
}

.segment-priority-pip {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.segment-time-label {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--slate-600);
}

.segment-title-label {
  font-size: 11.5px;
  font-weight: 700;
  color: var(--slate-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Active Protocol Deck */
.active-protocol-deck {
  background: #ffffff;
  border: 1px solid var(--slate-300);
  border-radius: var(--radius-sm);
  padding: 18px 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

.deck-masthead {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--slate-200);
  padding-bottom: 12px;
  margin-bottom: 16px;
  gap: 12px;
  flex-wrap: wrap;
}

.masthead-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.deck-phase-stamp {
  display: flex;
  align-items: center;
  gap: 8px;
}

.time-window-callout {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--slate-600);
}

.active-deck-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--slate-950);
  margin: 0;
  letter-spacing: -0.015em;
}

.priority-flag-pill {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--radius-xs);
  letter-spacing: 0.05em;
}

.badge-alert {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.badge-soil {
  background: #fffbeb;
  color: #92400e;
  border: 1px solid #fde68a;
}

.badge-slate {
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #cbd5e1;
}

.badge-forest {
  background: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
}

/* Asymmetrical Deck Layout (60% / 40%) */
.deck-grid-asym {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 20px;
  align-items: stretch;
}

.deck-execution-col {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.biological-target-panel {
  background: #f8fafc;
  border: 1px solid var(--slate-200);
  border-left: 3px solid var(--forest-600);
  border-radius: var(--radius-xs);
  padding: 12px 14px;
}

.panel-header-mini {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.svg-icon-sm {
  width: 14px;
  height: 14px;
}

.panel-kicker {
  font-family: var(--font-mono);
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--slate-500);
  letter-spacing: 0.05em;
}

.target-narrative {
  margin: 0;
  font-size: 13px;
  color: var(--slate-800);
  line-height: 1.55;
}

.application-rules-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.numbered-rules-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rule-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 10px;
  background: #ffffff;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xs);
}

.rule-index {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--slate-800);
  color: #ffffff;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
}

.rule-text {
  font-size: 12px;
  color: var(--slate-700);
  line-height: 1.5;
}

/* Right Specs Column */
.deck-specs-col {
  display: flex;
}

.specs-card-inner {
  width: 100%;
  background: #f8fafc;
  border: 1px solid var(--slate-300);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.specs-header {
  display: flex;
  align-items: center;
  gap: 6px;
  border-bottom: 1px solid var(--slate-200);
  padding-bottom: 8px;
}

.formulation-highlight-box {
  background: #ffffff;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xs);
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.formulation-label {
  font-family: var(--font-mono);
  font-size: 9px;
  text-transform: uppercase;
  color: var(--slate-500);
  font-weight: 600;
}

.formulation-name {
  font-size: 13px;
  font-weight: 800;
  color: var(--slate-950);
  line-height: 1.35;
}

.specs-data-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.spec-data-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 6px 8px;
  background: #ffffff;
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-xs);
}

.data-key {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--slate-500);
  text-transform: uppercase;
}

.data-val {
  font-size: 11.5px;
  font-weight: 700;
  color: var(--slate-800);
}

@media (max-width: 900px) {
  .timeline-segmented-bar {
    grid-template-columns: repeat(2, 1fr);
  }
  .deck-grid-asym {
    grid-template-columns: 1fr;
  }
}
</style>
