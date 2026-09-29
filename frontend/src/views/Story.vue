<template>
  <div class="story-page">
    <!-- Chapter 1: Hero (Mustard Band) -->
    <section class="chapter band chapter-hero">
      <div class="chapter-content hero-grid">
        <div class="hero-text-col">
          <span class="eyebrow hero-eyebrow">KRISHISETU · FIELD TO SATELLITE</span>
          <h1 class="hero-title">
            <span class="title-bengali">একটা পাতা থেকে একটা সীমান্ত</span>
            <span class="title-english">From one leaf to a whole border.</span>
          </h1>
          <p class="hero-sub">
            KrishiSetu spots crop disease early and warns the next district 48 hours ahead.
          </p>
          <div class="hero-action">
            <router-link to="/sathi" class="btn-gov-primary hero-cta-btn">
              <PhPlant :size="20" weight="bold" />
              <span>Check a leaf</span>
            </router-link>
            <router-link to="/command" class="btn-gov-outline hero-secondary-btn">
              <PhBroadcast :size="18" weight="bold" />
              <span>Outbreak watch</span>
            </router-link>
          </div>
        </div>

        <div class="hero-visual-col">
          <div class="hero-beacon-card">
            <div class="beacon-head">
              <div class="beacon-dot-wrapper">
                <span class="beacon-live-dot"></span>
              </div>
              <span class="beacon-status">ACTIVE TELEMETRY STREAM</span>
              <span class="dpg-chip-sm">DPG v1.0</span>
            </div>
            <div class="beacon-metrics">
              <div class="beacon-row">
                <span class="beacon-k">Interstate Vector:</span>
                <span class="beacon-v">Malda (WB) ➔ Katihar (BR)</span>
              </div>
              <div class="beacon-row">
                <span class="beacon-k">Sentinel-2 NDVI:</span>
                <span class="beacon-v">0.74 (Vegetative Vigour)</span>
              </div>
              <div class="beacon-row">
                <span class="beacon-k">Surveillance Buffer:</span>
                <span class="beacon-v highlight-lead">48 Hours Advance Lead</span>
              </div>
              <div class="beacon-row">
                <span class="beacon-k">Clinical Standard:</span>
                <span class="beacon-v">ICAR-CRRI Verified Protocols</span>
              </div>
            </div>
            <div class="beacon-foot">
              <span>8 Districts Connected · Bilingual Audio Support</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Chapter 2: Check a leaf (Plain Paper) -->
    <section class="chapter chapter-paper">
      <div class="chapter-content chapter-grid">
        <div class="chapter-text-col">
          <span class="eyebrow">CHAPTER 01 · CLINICAL SPECIMEN INTAKE</span>
          <h2>Check a leaf</h2>
          <p class="chapter-lead">
            Photograph or dictate crop symptoms in Bengali or Hindi for instant ICAR clinical diagnosis and pathogen verification.
          </p>
          <div class="chapter-action">
            <router-link to="/sathi" class="btn-gov-outline">
              <PhArrowRight :size="18" weight="bold" />
              <span>Open leaf diagnosis</span>
            </router-link>
          </div>
        </div>

        <div class="chapter-preview-col">
          <div class="preview-mini-card">
            <div class="preview-pill-row">
              <span class="badge-institutional badge-sky">Computer Vision + Audio</span>
              <span class="badge-institutional badge-forest">Offline IndexedDB</span>
            </div>
            <div class="preview-data-row">
              <strong>Multimodal Intake:</strong>
              <span>Devanagari & Bengali Audio Voiceprints + 56px Touch Camera</span>
            </div>
            <div class="preview-metric-box">
              <span class="pm-val">98.4%</span>
              <span class="pm-lbl">ICAR Diagnostic Confidence Benchmark</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Chapter 3: Convert any state registry (Plain Paper) -->
    <section class="chapter chapter-paper alt-paper">
      <div class="chapter-content chapter-grid">
        <div class="chapter-text-col">
          <span class="eyebrow">CHAPTER 02 · INTEROPERABLE DPG STANDARD</span>
          <h2>Convert any state registry</h2>
          <p class="chapter-lead">
            Harmonize Matir Katha, DBT Krishi, and Krushak registries into unified FarmContext v1.0 data schemas in real time.
          </p>
          <div class="chapter-action">
            <router-link to="/interop" class="btn-gov-outline">
              <PhArrowRight :size="18" weight="bold" />
              <span>Convert any state registry</span>
            </router-link>
          </div>
        </div>

        <div class="chapter-preview-col">
          <div class="preview-mini-card">
            <div class="preview-pill-row">
              <span class="badge-institutional badge-slate">West Bengal</span>
              <span class="badge-institutional badge-slate">Bihar</span>
              <span class="badge-institutional badge-forest">FarmContext Standard</span>
            </div>
            <div class="preview-data-row">
              <strong>Declarative Interop:</strong>
              <span>Automatic JSON Schema Transformation & Zero Data Loss</span>
            </div>
            <div class="preview-metric-box">
              <span class="pm-val">&lt; 900ms</span>
              <span class="pm-lbl">Dynamic Normalization Latency</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Chapter 4: Watch outbreaks cross borders (Plain Paper) -->
    <section class="chapter chapter-paper">
      <div class="chapter-content chapter-grid">
        <div class="chapter-text-col">
          <span class="eyebrow">CHAPTER 03 · TRANS-BOUNDARY TELEMETRY</span>
          <h2>Watch outbreaks cross borders</h2>
          <p class="chapter-lead">
            Track airborne spore dispersal vectors and interstate transmission corridors with live orbital NDVI verification.
          </p>
          <div class="chapter-action">
            <router-link to="/command" class="btn-gov-outline">
              <PhArrowRight :size="18" weight="bold" />
              <span>Watch outbreaks cross borders</span>
            </router-link>
          </div>
        </div>

        <div class="chapter-preview-col">
          <div class="preview-mini-card">
            <div class="preview-pill-row">
              <span class="badge-institutional badge-soil">Trans-Boundary Vector</span>
              <span class="badge-institutional badge-sky">GIS Telemetry</span>
            </div>
            <div class="preview-data-row">
              <strong>Corridor Surveillance:</strong>
              <span>Kosi-Mahananda-Gangetic Basin Inter-State Vector Monitoring</span>
            </div>
            <div class="preview-metric-box">
              <span class="pm-val">48 Hours</span>
              <span class="pm-lbl">Early Warning Lead Before Spore Arrival</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Chapter 5: 48h Head Start (Dark Band) -->
    <section class="chapter band-dark chapter-metric">
      <div class="chapter-content text-center">
        <span class="eyebrow metric-eyebrow">SURVEILLANCE HORIZON</span>
        <div class="metric-huge">48<span class="metric-unit">h</span></div>
        <p class="metric-caption">
          Head start for the next district.
        </p>
        <div class="chapter-action justify-center">
          <router-link to="/command" class="btn-gov-primary" style="min-height: 52px; padding: 0 var(--space-6);">
            <PhBroadcast :size="20" weight="bold" />
            <span>Open outbreak watch</span>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { PhPlant, PhBroadcast, PhArrowRight } from '@phosphor-icons/vue'
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
  max-width: 1200px;
}

.chapter-paper {
  background: var(--paper);
  color: var(--ink);
  border-bottom: 1px solid var(--hairline);
  padding: calc(var(--space-8) * 1.3) var(--space-6);
}

.chapter-paper.alt-paper {
  background: var(--paper-raised);
}

/* Chapter 1: Hero */
.chapter-hero {
  padding: calc(var(--space-8) * 1.5) var(--space-6);
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: var(--space-6);
  align-items: center;
}

.hero-text-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
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
  font-size: clamp(2rem, 4.5vw, 3.8rem);
  font-weight: 800;
  line-height: 1.08;
  color: var(--canopy);
  letter-spacing: -0.03em;
}

.hero-sub {
  font-size: var(--step-1);
  font-weight: 600;
  color: var(--canopy);
  max-width: 58ch;
  line-height: 1.45;
  margin: 0;
}

.hero-action {
  margin-top: var(--space-2);
  display: flex;
  align-items: center;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.hero-cta-btn {
  min-height: 52px;
  padding: 0 var(--space-6);
  font-size: var(--step-0);
  border-radius: var(--radius-pill);
}

.hero-secondary-btn {
  min-height: 52px;
  padding: 0 var(--space-5);
  font-size: var(--step-0);
  border-radius: var(--radius-pill);
}

/* Hero Beacon Card */
.hero-visual-col {
  display: flex;
  justify-content: center;
}

.hero-beacon-card {
  background: var(--canopy);
  color: var(--inkwell-text);
  border: 2px solid var(--canopy);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.beacon-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--inkwell-line);
}

.beacon-dot-wrapper {
  display: flex;
  align-items: center;
}

.beacon-live-dot {
  width: 10px;
  height: 10px;
  border-radius: var(--radius-pill);
  background: var(--leaf-bright);
}

.beacon-status {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--green-wash);
  letter-spacing: 0.05em;
}

.dpg-chip-sm {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  background: var(--sarson);
  color: var(--canopy);
  padding: 2px 8px;
  border-radius: var(--radius-pill);
}

.beacon-metrics {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.beacon-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-size: 0.875rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: var(--space-2);
}

.beacon-k {
  color: var(--green-line);
  font-weight: 600;
}

.beacon-v {
  font-weight: 700;
  color: var(--paper-raised);
  text-align: right;
}

.beacon-v.highlight-lead {
  color: var(--sarson);
  font-weight: 800;
}

.beacon-foot {
  font-size: 0.8125rem;
  color: var(--green-wash);
  text-align: center;
  padding-top: var(--space-1);
}

/* Chapters 2-4 Layout */
.chapter-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: var(--space-6);
  align-items: center;
}

.chapter-text-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

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
  max-width: 58ch;
  line-height: 1.5;
  margin: 0;
}

.chapter-action {
  margin-top: var(--space-2);
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

/* Preview Mini Card */
.chapter-preview-col {
  display: flex;
  justify-content: center;
}

.preview-mini-card {
  background: var(--paper-raised);
  border: 1.5px solid var(--hairline);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.preview-pill-row {
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.preview-data-row {
  font-size: 0.875rem;
  color: var(--ink-2);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  border-top: 1px solid var(--hairline);
  padding-top: var(--space-2);
}

.preview-data-row strong {
  color: var(--ink);
}

.preview-metric-box {
  background: var(--paper-sunken);
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 2px;
}

.pm-val {
  font-family: var(--font-mono);
  font-size: var(--step-2);
  font-weight: 800;
  color: var(--canopy);
}

.pm-lbl {
  font-size: 0.8125rem;
  color: var(--ink-3);
  font-weight: 600;
}

/* Chapter 5: Metric Band */
.chapter-metric {
  padding: calc(var(--space-8) * 1.8) var(--space-6);
  text-align: center;
}

.chapter-metric .chapter-content {
  align-items: center;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.metric-eyebrow {
  color: var(--green-line);
  font-weight: 700;
  letter-spacing: 0.1em;
}

.metric-huge {
  font-family: var(--font-mono);
  font-size: clamp(4.5rem, 14vw, 10rem);
  font-weight: 800;
  line-height: 0.95;
  color: var(--sarson);
  letter-spacing: -0.04em;
  margin: var(--space-1) 0;
  display: inline-flex;
  align-items: baseline;
  justify-content: center;
  gap: 2px;
}

.metric-unit {
  font-size: 0.45em;
  font-weight: 700;
  color: var(--sarson);
  letter-spacing: normal;
}

.metric-caption {
  font-size: var(--step-2);
  font-weight: 600;
  color: var(--inkwell-text);
  max-width: 40ch;
  line-height: 1.3;
  margin: 0;
}

.justify-center {
  justify-content: center;
}

@media (max-width: 900px) {
  .hero-grid,
  .chapter-grid {
    grid-template-columns: 1fr;
    gap: var(--space-5);
  }
  .hero-visual-col,
  .chapter-preview-col {
    justify-content: flex-start;
  }
  .hero-beacon-card,
  .preview-mini-card {
    max-width: 100%;
  }
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
