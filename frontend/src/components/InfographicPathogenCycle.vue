<template>
  <div class="pathogen-cycle-infographic">
    <div class="cycle-head-bar">
      <div>
        <span class="sub-label">Biological Mode-of-Action Monograph</span>
        <h4 class="cycle-title">Pathogen etiology and bio-fungicidal interception cycle</h4>
      </div>
      <div class="stage-stepper-pills">
        <button 
          v-for="(st, idx) in stages" 
          :key="idx" 
          class="step-pill" 
          :class="{ 'step-active': activeStageIndex === idx }"
          @click="activeStageIndex = idx"
          type="button"
        >
          Phase {{ idx + 1 }}: {{ st.shortTitle }}
        </button>
      </div>
    </div>

    <!-- Main Biological Cross-Section Visualizer (SVG) -->
    <div class="anatomy-svg-wrapper">
      <svg class="leaf-anatomy-svg" viewBox="0 0 760 260" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Plant Tissue Anatomy and Pathogen Infection Cycle Diagram">
        <!-- Botanical Leaf Tissue Layers -->
        <!-- Upper Cuticle / Epidermis -->
        <rect x="20" y="70" width="720" height="24" rx="2" fill="#d1fae5" stroke="#059669" stroke-width="1.5" />
        <text x="32" y="86" class="layer-label-text">Waxy Cuticle & Upper Epidermis (Adaxial Surface)</text>

        <!-- Palisade Mesophyll Layer (Chloroplast Cells) -->
        <g v-for="i in 18" :key="'palisade-' + i">
          <rect :x="32 + (i - 1) * 39" y="102" width="34" height="60" rx="4" fill="#ecfdf5" stroke="#10b981" stroke-width="1" />
          <circle :cx="40 + (i - 1) * 39" cy="116" r="3" fill="#059669" opacity="0.6" />
          <circle :cx="58 + (i - 1) * 39" cy="130" r="3" fill="#059669" opacity="0.6" />
          <circle :cx="48 + (i - 1) * 39" cy="148" r="3" fill="#059669" opacity="0.6" />
        </g>
        <text x="32" y="136" class="layer-sub-text">Palisade Mesophyll (Chloroplast Engine)</text>

        <!-- Spongy Mesophyll & Air Spaces -->
        <rect x="20" y="170" width="720" height="40" fill="#f0fdf4" stroke="#a7f3d0" stroke-width="1" />
        <circle cx="120" cy="190" r="12" fill="#ffffff" stroke="#6ee7b7" stroke-width="1" />
        <circle cx="260" cy="190" r="14" fill="#ffffff" stroke="#6ee7b7" stroke-width="1" />
        <circle cx="440" cy="190" r="11" fill="#ffffff" stroke="#6ee7b7" stroke-width="1" />
        <circle cx="600" cy="190" r="13" fill="#ffffff" stroke="#6ee7b7" stroke-width="1" />
        <text x="32" y="195" class="layer-sub-text">Spongy Parenchyma & Vascular Bundle</text>

        <!-- Lower Epidermis & Stomata (Abaxial Surface) -->
        <rect x="20" y="218" width="720" height="22" rx="2" fill="#d1fae5" stroke="#059669" stroke-width="1.5" />
        <text x="32" y="233" class="layer-label-text">Lower Epidermis & Stomata (Primary Infection Gateway)</text>

        <!-- Phase 1: Zoospore Droplet on Cuticle -->
        <g class="infection-vector" :class="{ 'vector-highlight': activeStageIndex === 0 }">
          <ellipse cx="140" cy="58" rx="28" ry="14" fill="rgba(56, 189, 248, 0.25)" stroke="#0284c7" stroke-width="1.5" />
          <circle cx="132" cy="56" r="4.5" fill="#c2410c" />
          <circle cx="148" cy="58" r="4.5" fill="#c2410c" />
          <!-- Zoospore flagella -->
          <path d="M 132 52 Q 130 42 125 40" fill="none" stroke="#ea580c" stroke-width="1.5" />
          <path d="M 148 54 Q 154 44 158 42" fill="none" stroke="#ea580c" stroke-width="1.5" />
          <text x="140" y="28" text-anchor="middle" class="vector-title">Phase 1: Free Water Zoospores</text>
          <text x="140" y="40" text-anchor="middle" class="vector-sub">RH 86% triggers germination</text>
        </g>

        <!-- Phase 2: Appressorium & Cuticular Penetration -->
        <g class="infection-vector" :class="{ 'vector-highlight': activeStageIndex === 1 }">
          <circle cx="320" cy="62" r="7" fill="#b91c1c" />
          <!-- Penetration peg piercing cuticle -->
          <path d="M 320 69 L 320 102" fill="none" stroke="#b91c1c" stroke-width="2.5" />
          <polygon points="316,98 320,106 324,98" fill="#b91c1c" />
          <text x="320" y="28" text-anchor="middle" class="vector-title">Phase 2: Enzymatic Peg</text>
          <text x="320" y="40" text-anchor="middle" class="vector-sub">Cutinase dissolves epidermis</text>
        </g>

        <!-- Phase 3: Intercellular Mycelial Colonization -->
        <g class="infection-vector" :class="{ 'vector-highlight': activeStageIndex === 2 }">
          <!-- Branching hyphae between mesophyll cells -->
          <path d="M 480 94 Q 495 120 485 145 T 510 175" fill="none" stroke="#b91c1c" stroke-width="2.5" />
          <path d="M 490 125 Q 515 130 520 148" fill="none" stroke="#b91c1c" stroke-width="2" />
          <!-- Haustoria (nutrient siphons) -->
          <circle cx="475" cy="130" r="3.5" fill="#7f1d1d" />
          <circle cx="510" cy="142" r="3.5" fill="#7f1d1d" />
          <text x="500" y="28" text-anchor="middle" class="vector-title">Phase 3: Hyphal Siphoning</text>
          <text x="500" y="40" text-anchor="middle" class="vector-sub">Chloroplast lysis & brown rot</text>
        </g>

        <!-- Phase 4: Sporangiophore Eruption (Underside Sporulation) -->
        <g class="infection-vector" :class="{ 'vector-highlight': activeStageIndex === 3 }">
          <!-- Emergence through stoma -->
          <path d="M 660 216 L 660 248 Q 675 258 685 244" fill="none" stroke="#b91c1c" stroke-width="2.5" />
          <circle cx="660" cy="254" r="5" fill="#b91c1c" />
          <circle cx="685" cy="244" r="4.5" fill="#b91c1c" />
          <circle cx="674" cy="258" r="4" fill="#b91c1c" />
          <text x="660" y="28" text-anchor="middle" class="vector-title">Phase 4: Active Sporulation</text>
          <text x="660" y="40" text-anchor="middle" class="vector-sub">White mildew downy ring</text>
        </g>

        <!-- Biocontrol Interception Overlay (Trichoderma Mycoparasitism) -->
        <g class="biocontrol-shield">
          <rect x="290" y="4" width="220" height="20" rx="3" fill="#1e3a8a" />
          <text x="400" y="18" text-anchor="middle" class="shield-label-text">
            KRISHISETU BIO-SHIELD: TRICHODERMA ANTAGONISM
          </text>
          <!-- Coiling antagonistic hyphae wrapping pathogen -->
          <path d="M 330 62 Q 338 54 345 66 T 352 56" fill="none" stroke="#2563eb" stroke-width="2" stroke-dasharray="3, 2" />
        </g>
      </svg>
    </div>

    <!-- Active Stage Explainer Card -->
    <div class="active-stage-card">
      <div class="stage-info-meta">
        <span class="badge-institutional badge-forest">Biological Phase {{ activeStageIndex + 1 }}</span>
        <span class="pathogen-taxa">Pathogen: <em>Phytophthora infestans</em> (Oomycota)</span>
      </div>
      <h5 class="active-stage-heading">{{ currentStage.title }}</h5>
      <p class="active-stage-desc">{{ currentStage.description }}</p>
      
      <div class="stage-biocontrol-box">
        <span class="biocontrol-tag">Prescribed Biological Countermeasure:</span>
        <span class="biocontrol-text font-editorial-italic">{{ currentStage.countermeasure }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeStageIndex = ref(0)

const stages = [
  {
    shortTitle: 'Spore Attachment',
    title: 'Phase 1: Zoospore Encystment & Free Water Mobility',
    description: 'Biflagellate zoospores emerge from sporangia in free water films. When microclimate relative humidity exceeds 82% and leaf wetness persists over 6 hours, zoospores encyst onto the adaxial waxy cuticle, preparing germ tubes.',
    countermeasure: 'Pre-emptive foliar spray of Trichoderma harzianum (5g/L) occupies adhesion sites on the phyllosphere, physically outcompeting pathogen spore encystment.'
  },
  {
    shortTitle: 'Stomatal Breach',
    title: 'Phase 2: Enzymatic Appressorium & Cuticular Penetration',
    description: 'The germ tube forms an appressorium that secretes cutinases, pectinases, and cellulases, dissolving the wax and cell wall matrix. In potatoes and tomatoes, it commonly breaches directly through open stomata.',
    countermeasure: 'Foliar application of Potassium Silicate / Potassium Sulfate thickens plant epidermal cell walls, doubling mechanical resistance to penetration pegs.'
  },
  {
    shortTitle: 'Mycelial Colonization',
    title: 'Phase 3: Intercellular Hyphal Expansion & Chloroplast Lysis',
    description: 'Mycelium traverses intercellular air spaces in the spongy mesophyll. Specialized bulbous haustoria penetrate host cell walls to siphon sucrose and amino acids, causing chlorophyll degradation, cellular collapse, and brown necrotic lesions.',
    countermeasure: 'Trichoderma secretes extracellular enzymes (chitinase and beta-1,3-glucanase) that digest and dissolve oomycete cell walls, halting hyphal expansion.'
  },
  {
    shortTitle: 'Sporulation & Spread',
    title: 'Phase 4: Conidiophore Eruption & Secondary Dispersal',
    description: 'Branching sporangiophores emerge through stomata on the underside of leaves, producing the characteristic white velvety mildew halo. Millions of airborne sporangia are shed by rain splash and convective wind currents.',
    countermeasure: 'Immediate morning sanitization with botanical bio-fungicide halts spore discharge; infected canopy leaf prunings must be sealed and removed from field perimeter.'
  }
]

const currentStage = computed(() => stages[activeStageIndex.value])
</script>

<style scoped>
.pathogen-cycle-infographic {
  padding: 20px 24px;
  background: var(--bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  margin-top: 16px;
}

.cycle-head-bar {
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

.cycle-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 2px 0 0 0;
}

.stage-stepper-pills {
  display: inline-flex;
  background: var(--slate-100);
  padding: 3px;
  border-radius: var(--radius-md);
  border: 1px solid var(--slate-200);
  gap: 3px;
  flex-wrap: wrap;
}

.step-pill {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  padding: 5px 12px;
  border-radius: var(--radius-sm);
  background: transparent;
  border: none;
  color: var(--slate-600);
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, box-shadow 0.15s ease;
}

.step-pill:hover {
  color: var(--slate-900);
}

.step-pill:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

.step-pill.step-active {
  background: #ffffff;
  color: var(--slate-900);
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* SVG Leaf Anatomy */
.anatomy-svg-wrapper {
  background: #fafaf9;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px 12px;
  overflow-x: auto;
}

.leaf-anatomy-svg {
  width: 100%;
  min-width: 600px;
  height: auto;
  display: block;
}

.layer-label-text {
  font-family: var(--font-mono);
  font-size: 9.5px;
  font-weight: 700;
  fill: #065f46;
}

.layer-sub-text {
  font-family: var(--font-mono);
  font-size: 9px;
  fill: #047857;
  opacity: 0.85;
}

.vector-title {
  font-family: var(--font-mono);
  font-size: 9.5px;
  font-weight: 700;
  fill: #991b1b;
}

.vector-sub {
  font-family: var(--font-mono);
  font-size: 8.5px;
  fill: #78350f;
}

.shield-label-text {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 700;
  fill: #ffffff;
}

.infection-vector {
  opacity: 0.45;
  transition: opacity 0.2s ease;
}

.infection-vector.vector-highlight {
  opacity: 1;
}

/* Active Stage Card */
.active-stage-card {
  margin-top: 14px;
  padding: 12px 16px;
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stage-info-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pathogen-taxa {
  font-size: 11px;
  color: var(--slate-600);
}

.active-stage-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 0;
}

.active-stage-desc {
  font-size: 12px;
  color: var(--slate-700);
  line-height: 1.5;
  margin: 0;
}

.stage-biocontrol-box {
  margin-top: 4px;
  padding: 8px 12px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: var(--radius-sm);
  font-size: 11.5px;
  color: #14532d;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.biocontrol-tag {
  font-weight: 700;
}

.biocontrol-text {
  color: #166534;
}
</style>
