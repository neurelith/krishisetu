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
              <PhShieldCheck :size="18" weight="bold" class="text-forest" />
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
              <PhFlask :size="18" weight="bold" class="text-sky" />
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
import { PhShieldCheck, PhFlask } from '@phosphor-icons/vue'

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
    biologicalTarget: 'Reinforce host plant epidermal cell walls with silica and potassium ions to double mechanical resistance against hyphal penetration pegs.',
    formulation: 'Soluble Potassium Silicate (K2SiO3, 18% Si, 12% K2O)',
    dosingRate: '2.5 ml / L water via fine foliar mist',
    costLevel: 'Economical (₹310 / acre)',
    applicationRules: [
      'Ensure complete canopy coverage; silica polymerization forms a hard microscopic barrier across leaf surfaces within 12 hours.',
      'Avoid tank mixing with highly acidic compounds or foliar fertilizers containing heavy metals.',
      'Best applied late afternoon (04:30 - 06:30 PM) as air temperatures cool down.'
    ]
  },
  {
    stepNumber: '03',
    timeWindow: 'Day 05 - 07',
    shortTitle: 'Systemic Resistance Induction',
    title: 'Systemic Acquired Resistance (SAR) Booster',
    priority: 'STANDARD',
    badgeClass: 'badge-slate',
    biologicalTarget: 'Activate salicylic acid defense pathways in uninfected neighboring tillers and foliar tissue.',
    formulation: 'Pseudomonas fluorescens (1% WP, 1x10^8 CFU/g)',
    dosingRate: '10.0 g / L water',
    costLevel: 'Very Low (₹260 / acre)',
    applicationRules: [
      'Spray broad perimeter buffer zone (15m radius around initial outbreak foci).',
      'Encourages competitive colonization of the rhizosphere and phyllosphere, generating natural siderophores.'
    ]
  },
  {
    stepNumber: '04',
    timeWindow: 'Day 10 - 14',
    shortTitle: 'Canopy Biomass Restoration',
    title: 'Photosynthetic Recovery & Micronutrient Feed',
    priority: 'RECOVERY',
    badgeClass: 'badge-forest',
    biologicalTarget: 'Restore chlorophyll density and stimulate vegetative tillering in recovering crop zones.',
    formulation: 'Liquid Seaweed Extract (Ascophyllum nodosum) + Chelated Zinc (12% Zn-EDTA)',
    dosingRate: '2.0 ml Seaweed + 1.0 g Zn-EDTA / L water',
    costLevel: 'Moderate (₹540 / acre)',
    applicationRules: [
      'Administer early morning after morning dew has evaporated from the canopy.',
      'Verify zero active necrotic sporulation rings before applying foliar nutrients.'
    ]
  }
]

const activePhase = computed(() => phases[activePhaseIdx.value])
</script>

<style scoped>
.treatment-roadmap-container {
  padding: var(--space-4) var(--space-5);
  background: var(--paper-raised);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md);
  margin-top: var(--space-4);
}

.roadmap-head-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  border-bottom: 1px solid var(--hairline);
  padding-bottom: var(--space-3);
  margin-bottom: var(--space-4);
  flex-wrap: wrap;
}

.sub-label {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--ink-3);
  letter-spacing: 0.05em;
  display: block;
}

.roadmap-title {
  font-size: var(--step-0);
  font-weight: 700;
  color: var(--ink);
  margin: var(--space-1) 0 0 0;
}

.timeline-segmented-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-2);
  background: var(--paper-sunken);
  padding: var(--space-1);
  border-radius: var(--radius-md);
  border: 1px solid var(--hairline);
  margin-bottom: var(--space-4);
}

.timeline-segment-btn {
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  padding: var(--space-2) var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  text-align: left;
  cursor: pointer;
  transition: background-color 120ms, border-color 120ms;
}

.timeline-segment-btn:focus-visible {
  outline: 3px solid var(--canopy);
  outline-offset: 2px;
}

.timeline-segment-btn:hover {
  background: var(--paper);
}

.timeline-segment-btn.is-active-segment {
  background: var(--paper-raised);
  border-color: var(--hairline-strong);
}

.segment-step-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.segment-number {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink-3);
  text-transform: uppercase;
}

.timeline-segment-btn.is-active-segment .segment-number {
  color: var(--canopy);
}

.segment-priority-pip {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.segment-time-label {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--ink-2);
}

.segment-title-label {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Active Protocol Deck */
.active-protocol-deck {
  background: var(--paper-raised);
  border: 1px solid var(--hairline-strong);
  border-radius: var(--radius-sm);
  padding: var(--space-4) var(--space-4);
}

.deck-masthead {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--hairline);
  padding-bottom: var(--space-3);
  margin-bottom: var(--space-4);
  gap: var(--space-3);
  flex-wrap: wrap;
}

.masthead-left {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.deck-phase-stamp {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.time-window-callout {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--ink-2);
}

.active-deck-title {
  font-size: var(--step-1);
  font-weight: 800;
  color: var(--ink);
  margin: 0;
  letter-spacing: -0.015em;
}

.priority-flag-pill {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--radius-xs);
  letter-spacing: 0.05em;
}

.badge-alert {
  background: var(--brick-wash);
  color: var(--brick);
  border: 1px solid var(--brick-line);
}

.badge-soil {
  background: var(--ochre-wash);
  color: var(--ochre);
  border: 1px solid var(--ochre-line);
}

.badge-slate {
  background: var(--paper-sunken);
  color: var(--ink-2);
  border: 1px solid var(--hairline-strong);
}

.badge-forest {
  background: var(--green-wash);
  color: var(--canopy);
  border: 1px solid var(--green-line);
}

/* Asymmetrical Deck Layout (60% / 40%) */
.deck-grid-asym {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: var(--space-4);
  align-items: stretch;
}

.deck-execution-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.biological-target-panel {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-left: 3px solid var(--leaf);
  border-radius: var(--radius-xs);
  padding: var(--space-3) var(--space-4);
}

.panel-header-mini {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-1);
}

.panel-kicker {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--ink-3);
  letter-spacing: 0.05em;
}

.target-narrative {
  margin: 0;
  font-size: 0.875rem;
  color: var(--ink);
  line-height: 1.55;
}

.application-rules-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.numbered-rules-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.rule-row {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: var(--paper-raised);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-xs);
}

.rule-index {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--canopy);
  color: var(--paper-raised);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
}

.rule-text {
  font-size: 0.8125rem;
  color: var(--ink-2);
  line-height: 1.5;
}

/* Right Specs Column */
.deck-specs-col {
  display: flex;
}

.specs-card-inner {
  width: 100%;
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-3) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.specs-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  border-bottom: 1px solid var(--hairline);
  padding-bottom: var(--space-2);
}

.formulation-highlight-box {
  background: var(--paper-raised);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-xs);
  padding: var(--space-2) var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.formulation-label {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  text-transform: uppercase;
  color: var(--ink-3);
  font-weight: 600;
}

.formulation-name {
  font-size: 0.875rem;
  font-weight: 800;
  color: var(--ink);
  line-height: 1.35;
}

.specs-data-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.spec-data-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: var(--space-1) var(--space-2);
  background: var(--paper-raised);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-xs);
}

.data-key {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  color: var(--ink-3);
  text-transform: uppercase;
}

.data-val {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink);
}

.text-sky { color: var(--leaf-bright); }
.text-forest { color: var(--leaf); }
.text-alert { color: var(--alert-text); }

@media (max-width: 900px) {
  .timeline-segmented-bar {
    grid-template-columns: repeat(2, 1fr);
  }
  .deck-grid-asym {
    grid-template-columns: 1fr;
  }
}
</style>
