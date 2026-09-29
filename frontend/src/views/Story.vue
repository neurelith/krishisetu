<template>
  <div class="story-page">
    <!-- Chapter 1: Hero (Mustard Band) -->
    <section class="chapter band chapter-hero">
      <div class="chapter-content">
        <span class="eyebrow hero-eyebrow">KRISHISETU · FIELD TO SATELLITE</span>
        <h1 class="hero-title">
          <span class="title-bengali">একটা পাতা থেকে একটা সীমান্ত</span>
          <span class="title-english">From one leaf to a whole border.</span>
        </h1>
        <p class="hero-sub">
          KrishiSetu spots crop disease early and warns the next district 48 hours ahead.
        </p>
        <div class="hero-action">
          <router-link to="/sathi" class="btn-gov-primary">
            Check a leaf
          </router-link>
        </div>
      </div>
    </section>

    <!-- Chapter 2: Check a leaf (Plain Paper) -->
    <section class="chapter chapter-paper">
      <div class="chapter-content">
        <span class="eyebrow">CHAPTER 01 · CLINICAL SPECIMEN INTAKE</span>
        <h2>Check a leaf</h2>
        <p class="chapter-lead">
          Photograph or dictate crop symptoms in Bengali or Hindi for instant ICAR clinical diagnosis and pathogen verification.
        </p>
        <div class="chapter-action">
          <router-link to="/sathi" class="btn-gov-outline">
            Open leaf diagnosis
          </router-link>
        </div>
      </div>
    </section>

    <!-- Chapter 3: Convert any state registry (Plain Paper) -->
    <section class="chapter chapter-paper alt-paper">
      <div class="chapter-content">
        <span class="eyebrow">CHAPTER 02 · INTEROPERABLE DPG STANDARD</span>
        <h2>Convert any state registry</h2>
        <p class="chapter-lead">
          Harmonize Matir Katha, DBT Krishi, and Krushak registries into unified FarmContext v1.0 data schemas in real time.
        </p>
        <div class="chapter-action">
          <router-link to="/interop" class="btn-gov-outline">
            Convert any state registry
          </router-link>
        </div>
      </div>
    </section>

    <!-- Chapter 4: Watch outbreaks cross borders (Plain Paper) -->
    <section class="chapter chapter-paper">
      <div class="chapter-content">
        <span class="eyebrow">CHAPTER 03 · TRANS-BOUNDARY TELEMETRY</span>
        <h2>Watch outbreaks cross borders</h2>
        <p class="chapter-lead">
          Track airborne spore dispersal vectors and interstate transmission corridors with live orbital NDVI verification.
        </p>
        <div class="chapter-action">
          <router-link to="/command" class="btn-gov-outline">
            Watch outbreaks cross borders
          </router-link>
        </div>
      </div>
    </section>

    <!-- Chapter 5: 48h Head Start (Dark Band) -->
    <section class="chapter band-dark chapter-metric">
      <div class="chapter-content text-center">
        <span class="eyebrow metric-eyebrow">SURVEILLANCE HORIZON</span>
        <div class="metric-huge">48 h</div>
        <p class="metric-caption">
          Head start for the next district.
        </p>
        <div class="chapter-action">
          <router-link to="/command" class="btn-gov-primary">
            Open outbreak watch
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// Phase 2: Static story view. Motion/scroll animations isolated from this phase.
</script>

<style scoped>
.story-page {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.chapter {
  width: 100%;
  padding: var(--space-8) var(--space-6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.chapter-content {
  width: 100%;
  max-width: 960px;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.chapter-paper {
  background: var(--paper);
  color: var(--ink);
  border-bottom: 1px solid var(--hairline);
  padding: calc(var(--space-8) * 1.5) var(--space-6);
}

.chapter-paper.alt-paper {
  background: var(--paper-raised);
}

/* Chapter 1: Hero */
.chapter-hero {
  padding: calc(var(--space-8) * 1.6) var(--space-6);
}

.hero-eyebrow {
  color: var(--canopy);
  font-weight: 700;
  letter-spacing: 0.08em;
}

.hero-title {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin: 0;
}

.title-bengali {
  font-family: "Anek Bangla", var(--font-display);
  font-size: var(--step-hero);
  font-weight: 800;
  line-height: 1.05;
  color: var(--canopy);
  letter-spacing: -0.02em;
}

.title-english {
  font-family: var(--font-display);
  font-size: clamp(2rem, 5vw, 4.2rem);
  font-weight: 800;
  line-height: 1.05;
  color: var(--canopy);
  letter-spacing: -0.03em;
}

.hero-sub {
  font-size: var(--step-1);
  font-weight: 600;
  color: var(--canopy);
  max-width: 60ch;
  line-height: 1.4;
  margin: 0;
}

.hero-action,
.chapter-action {
  margin-top: var(--space-3);
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

/* Chapters 2-4 Typography */
.chapter-paper h2 {
  font-size: var(--step-3);
  font-weight: 800;
  color: var(--ink);
  margin: 0;
  letter-spacing: -0.02em;
}

.chapter-lead {
  font-size: var(--step-1);
  color: var(--ink-2);
  max-width: 62ch;
  line-height: 1.5;
  margin: 0;
}

/* Chapter 5: Metric Band */
.chapter-metric {
  padding: calc(var(--space-8) * 2) var(--space-6);
  text-align: center;
}

.chapter-metric .chapter-content {
  align-items: center;
  text-align: center;
}

.metric-eyebrow {
  color: var(--green-line);
  font-weight: 700;
  letter-spacing: 0.1em;
}

.metric-huge {
  font-family: var(--font-mono);
  font-size: clamp(5rem, 16vw, 12rem);
  font-weight: 700;
  line-height: 0.95;
  color: var(--sarson);
  letter-spacing: -0.04em;
  margin: var(--space-2) 0;
}

.metric-caption {
  font-size: var(--step-2);
  font-weight: 600;
  color: var(--inkwell-text);
  max-width: 40ch;
  line-height: 1.3;
  margin: 0 0 var(--space-3) 0;
}

@media (max-width: 768px) {
  .chapter {
    padding: var(--space-6) var(--space-4);
  }
  .chapter-paper {
    padding: var(--space-8) var(--space-4);
  }
}
</style>
