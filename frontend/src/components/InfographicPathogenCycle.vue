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
        <rect x="20" y="70" width="720" height="24" rx="2" class="svg-cuticle" />
        <text x="32" y="86" class="layer-label-text">Waxy Cuticle & Upper Epidermis (Adaxial Surface)</text>

        <!-- Palisade Mesophyll Layer (Chloroplast Cells) -->
        <g v-for="i in 18" :key="'palisade-' + i">
          <rect :x="32 + (i - 1) * 39" y="102" width="34" height="60" rx="4" class="svg-mesophyll-cell" />
          <circle :cx="40 + (i - 1) * 39" cy="116" r="3" class="svg-chloroplast" />
          <circle :cx="58 + (i - 1) * 39" cy="130" r="3" class="svg-chloroplast" />
          <circle :cx="48 + (i - 1) * 39" cy="148" r="3" class="svg-chloroplast" />
        </g>
        <text x="32" y="136" class="layer-sub-text">Palisade Mesophyll (Chloroplast Engine)</text>

        <!-- Spongy Mesophyll & Air Spaces -->
        <rect x="20" y="170" width="720" height="40" class="svg-spongy" />
        <circle cx="120" cy="190" r="12" class="svg-air-space" />
        <circle cx="260" cy="190" r="14" class="svg-air-space" />
        <circle cx="440" cy="190" r="11" class="svg-air-space" />
        <circle cx="600" cy="190" r="13" class="svg-air-space" />
        <text x="32" y="195" class="layer-sub-text">Spongy Parenchyma & Vascular Bundle</text>

        <!-- Lower Epidermis & Stomata (Abaxial Surface) -->
        <rect x="20" y="218" width="720" height="22" rx="2" class="svg-cuticle" />
        <text x="32" y="233" class="layer-label-text">Lower Epidermis & Stomata (Primary Infection Gateway)</text>

        <!-- Phase 1: Zoospore Droplet on Cuticle -->
        <g class="infection-vector" :class="{ 'vector-highlight': activeStageIndex === 0 }">
          <ellipse cx="140" cy="58" rx="28" ry="14" class="svg-water-drop" />
          <circle cx="132" cy="56" r="4.5" class="svg-spore-node" />
          <circle cx="148" cy="58" r="4.5" class="svg-spore-node" />
          <!-- Zoospore flagella -->
          <path d="M 132 52 Q 130 42 125 40" class="svg-flagella" />
          <path d="M 148 54 Q 154 44 158 42" class="svg-flagella" />
          <!-- Phase labels positioned near the visual element (top-left area) -->
          <text x="140" y="18" text-anchor="middle" class="vector-title">Phase 1: Free Water Zoospores</text>
          <text x="140" y="34" text-anchor="middle" class="vector-sub">RH 86% triggers germination</text>
        </g>

        <!-- Phase 2: Appressorium & Cuticular Penetration -->
        <g class="infection-vector" :class="{ 'vector-highlight': activeStageIndex === 1 }">
          <circle cx="320" cy="62" r="7" class="svg-appressorium" />
          <!-- Penetration peg piercing cuticle -->
          <path d="M 320 69 L 320 102" class="svg-penetration-peg" />
          <polygon points="316,98 320,106 324,98" class="svg-appressorium" />
          <!-- Phase labels near this element (top-center area) -->
          <text x="320" y="18" text-anchor="middle" class="vector-title">Phase 2: Enzymatic Peg</text>
          <text x="320" y="34" text-anchor="middle" class="vector-sub">Cutinase dissolves epidermis</text>
        </g>

        <!-- Phase 3: Intercellular Mycelial Colonization -->
        <g class="infection-vector" :class="{ 'vector-highlight': activeStageIndex === 2 }">
          <!-- Branching hyphae between mesophyll cells -->
          <path d="M 480 94 Q 495 120 485 145 T 510 175" class="svg-penetration-peg" />
          <path d="M 490 125 Q 515 130 520 148" class="svg-hypha-branch" />
          <!-- Haustoria (nutrient siphons) -->
          <circle cx="475" cy="130" r="3.5" class="svg-haustoria" />
          <circle cx="510" cy="142" r="3.5" class="svg-haustoria" />
          <!-- Phase labels near this element (top-right area) -->
          <text x="500" y="18" text-anchor="middle" class="vector-title">Phase 3: Hyphal Siphoning</text>
          <text x="500" y="34" text-anchor="middle" class="vector-sub">Chloroplast lysis & brown rot</text>
        </g>

        <!-- Phase 4: Sporangiophore Eruption (Underside Sporulation) -->
        <g class="infection-vector" :class="{ 'vector-highlight': activeStageIndex === 3 }">
          <!-- Emergence through stoma -->
          <path d="M 660 216 L 660 248 Q 675 258 685 244" class="svg-penetration-peg" />
          <circle cx="660" cy="254" r="5" class="svg-appressorium" />
          <circle cx="685" cy="244" r="4.5" class="svg-appressorium" />
          <circle cx="674" cy="258" r="4" class="svg-appressorium" />
          <!-- Phase labels near this element (bottom-right area), moved up to avoid cutoff -->
          <text x="660" y="18" text-anchor="middle" class="vector-title">Phase 4: Active Sporulation</text>
          <text x="660" y="34" text-anchor="middle" class="vector-sub">White mildew downy ring</text>
        </g>

        <!-- Biocontrol Interception Overlay (Trichoderma Mycoparasitism) -->
        <g class="biocontrol-shield">
          <rect x="290" y="4" width="220" height="20" rx="3" class="svg-shield-rect" />
          <text x="400" y="18" text-anchor="middle" class="shield-label-text">
            KRISHISETU BIO-SHIELD: TRICHODERMA ANTAGONISM
          </text>
          <!-- Coiling antagonistic hyphae wrapping pathogen -->
          <path d="M 330 62 Q 338 54 345 66 T 352 56" class="svg-coiling-hypha" />
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
  padding: var(--space-4) var(--space-5);
  background: var(--paper-raised);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md);
  margin-top: var(--space-4);
}

.cycle-head-bar {
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

.cycle-title {
  font-size: var(--step-0);
  font-weight: 700;
  color: var(--ink);
  margin: var(--space-1) 0 0 0;
}

.stage-stepper-pills {
  display: inline-flex;
  background: var(--paper-sunken);
  padding: 3px;
  border-radius: var(--radius-md);
  border: 1px solid var(--hairline);
  gap: 3px;
  flex-wrap: wrap;
}

.step-pill {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 500;
  padding: 6px 14px;
  min-height: 48px;
  border-radius: var(--radius-sm);
  background: transparent;
  border: none;
  color: var(--ink-2);
  cursor: pointer;
  transition: background-color 120ms, color 120ms;
}

.step-pill:hover {
  color: var(--ink);
}

.step-pill:focus-visible {
  outline: 3px solid var(--canopy);
  outline-offset: 2px;
}

.step-pill.step-active {
  background: var(--sarson);
  color: var(--canopy);
  font-weight: 700;
}

/* SVG Leaf Anatomy */
.anatomy-svg-wrapper {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-3);
  overflow-x: auto;
}

.leaf-anatomy-svg {
  width: 100%;
  min-width: 600px;
  height: auto;
  display: block;
}

.svg-cuticle {
  fill: var(--green-wash);
  stroke: var(--leaf);
  stroke-width: 1.5;
}

.svg-mesophyll-cell {
  fill: var(--paper-raised);
  stroke: var(--green-line);
  stroke-width: 1;
}

.svg-chloroplast {
  fill: var(--leaf);
  opacity: 0.6;
}

.svg-spongy {
  fill: var(--green-wash);
  stroke: var(--green-line);
  stroke-width: 1;
}

.svg-air-space {
  fill: var(--paper-raised);
  stroke: var(--green-line);
  stroke-width: 1;
}

.svg-water-drop {
  fill: var(--green-wash);
  stroke: var(--leaf-bright);
  stroke-width: 1.5;
}

.svg-spore-node {
  fill: var(--alert);
}

.svg-flagella {
  fill: none;
  stroke: var(--alert);
  stroke-width: 1.5;
}

.svg-appressorium {
  fill: var(--brick);
}

.svg-penetration-peg {
  fill: none;
  stroke: var(--brick);
  stroke-width: 2.5;
}

.svg-hypha-branch {
  fill: none;
  stroke: var(--brick);
  stroke-width: 2;
}

.svg-haustoria {
  fill: var(--brick);
}

.svg-shield-rect {
  fill: var(--canopy);
}

.svg-coiling-hypha {
  fill: none;
  stroke: var(--sarson);
  stroke-width: 2;
  stroke-dasharray: 3, 2;
}

.layer-label-text {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  fill: var(--canopy);
}

.layer-sub-text {
  font-family: var(--font-mono);
  font-size: 12px;
  fill: var(--leaf);
  opacity: 0.9;
}

.vector-title {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  fill: var(--brick);
}

.vector-sub {
  font-family: var(--font-mono);
  font-size: 12px;
  fill: var(--soil);
}

.shield-label-text {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  fill: var(--paper-raised);
}

.infection-vector {
  opacity: 0.45;
  transition: opacity 120ms;
}

.infection-vector.vector-highlight {
  opacity: 1;
}

/* Active Stage Card */
.active-stage-card {
  margin-top: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.stage-info-meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.pathogen-taxa {
  font-size: 0.8125rem;
  color: var(--ink-2);
}

.active-stage-heading {
  font-size: var(--step-0);
  font-weight: 700;
  color: var(--ink);
  margin: 0;
}

.active-stage-desc {
  font-size: 0.875rem;
  color: var(--ink-2);
  line-height: 1.5;
  margin: 0;
}

.stage-biocontrol-box {
  margin-top: var(--space-1);
  padding: var(--space-2) var(--space-3);
  background: var(--green-wash);
  border: 1px solid var(--green-line);
  border-radius: var(--radius-sm);
  font-size: 0.8125rem;
  color: var(--canopy);
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.biocontrol-tag {
  font-weight: 700;
}

.biocontrol-text {
  color: var(--canopy);
}
</style>
