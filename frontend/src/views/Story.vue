<template>
  <div class="story-page">
    <!-- Chapter 1: Sky Hero -->
    <section class="sky sky-hero" data-risk="clear">
      <div class="hero-container">
        <h1 class="display hero-headline">
          <span class="hero-line-bengali">একটা পাতা থেকে একটা সীমান্ত</span>
          <span class="hero-line-english">From one leaf to a whole border.</span>
        </h1>
        <p class="hero-sub">
          KrishiSetu spots crop disease early and warns the next district 48 hours ahead.
        </p>
        <div class="hero-actions">
          <router-link to="/sathi" class="btn-gov-primary">
            <span>Check a leaf</span>
            <PhArrowRight :size="18" weight="bold" />
          </router-link>
          <router-link to="/command" class="btn-gov-outline">
            <span>See outbreaks</span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Chapter 2: Quiet white section with 3 cards -->
    <section class="quiet">
      <div class="cards-row">
        <div class="card-solid feature-card">
          <h2>Check a leaf</h2>
          <p>Photograph a leaf or speak. Get the disease and what to do today.</p>
          <div class="card-action">
            <router-link to="/sathi" class="btn-gov-outline">
              <span>Open Sathi</span>
              <PhArrowRight :size="16" weight="bold" />
            </router-link>
          </div>
        </div>

        <div class="card-solid feature-card">
          <h2>Convert any registry</h2>
          <p>Bring state records into one standard format.</p>
          <div class="card-action">
            <router-link to="/interop" class="btn-gov-outline">
              <span>Open converter</span>
              <PhArrowRight :size="16" weight="bold" />
            </router-link>
          </div>
        </div>

        <div class="card-solid feature-card">
          <h2>Watch outbreaks</h2>
          <p>See disease cross district borders before it reaches your field.</p>
          <div class="card-action">
            <router-link to="/command" class="btn-gov-outline">
              <span>Open watch</span>
              <PhArrowRight :size="16" weight="bold" />
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Chapter 3: Storm sky 48 hours lead -->
    <section class="sky storm-band" data-risk="storm">
      <div class="storm-container">
        <div class="display storm-number">48 hours</div>
        <p class="storm-caption">Head start for the next district.</p>
        <div class="storm-action">
          <router-link to="/command" class="btn-gov-primary">
            <span>Open outbreak watch</span>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { PhArrowRight } from '@phosphor-icons/vue'
</script>

<style scoped>
.story-page {
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* Sky Hero */
.sky-hero {
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: calc(var(--spacing-64) + 64px) var(--spacing-24) var(--spacing-64);
  text-align: center;
}

.hero-container {
  max-width: var(--page-max-width);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-24);
}

.hero-headline {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-8);
  color: var(--color-cloud-white);
}

.hero-line-bengali {
  font-family: var(--font-display);
  font-size: clamp(2.2rem, 5.5vw, 4.2rem);
  font-weight: 400;
  line-height: 1.35;
}

.hero-line-english {
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 6vw, 4.6rem);
  font-weight: 300;
  line-height: 1.1;
  letter-spacing: -0.01em;
}

.hero-sub {
  font-family: var(--font-sans);
  font-size: 1.125rem; /* 18px */
  color: var(--color-cloud-white);
  max-width: 54ch;
  line-height: 1.5;
  margin: 0;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-16);
  flex-wrap: wrap;
  justify-content: center;
  margin-top: var(--spacing-8);
}

/* Quiet Section with 3 Cards */
.quiet {
  background: var(--color-cloud-white);
  padding: var(--section-gap) var(--spacing-24);
}

.cards-row {
  max-width: var(--page-max-width);
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-24);
}

.feature-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-16);
  padding: var(--card-padding);
}

.feature-card h2 {
  font-family: var(--font-display);
  font-size: var(--text-subheading);
  font-weight: 500;
  color: var(--color-ink);
  line-height: 1.2;
}

.feature-card p {
  font-family: var(--font-sans);
  font-size: var(--text-body);
  color: var(--color-graphite);
  line-height: 1.5;
  flex: 1;
}

.card-action {
  margin-top: auto;
  padding-top: var(--spacing-8);
}

/* Storm Band */
.storm-band {
  padding: calc(var(--spacing-64) * 1.5) var(--spacing-24);
  text-align: center;
}

.storm-container {
  max-width: var(--page-max-width);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-16);
}

.storm-number {
  font-family: var(--font-display);
  font-size: var(--text-display);
  font-weight: 300;
  color: var(--color-cloud-white);
  line-height: 1.05;
}

.storm-caption {
  font-family: var(--font-sans);
  font-size: 1.125rem; /* 18px */
  color: var(--color-cloud-white);
  margin: 0;
}

.storm-action {
  margin-top: var(--spacing-12);
}

@media (max-width: 900px) {
  .cards-row {
    grid-template-columns: 1fr;
    gap: var(--spacing-20);
  }
}
</style>
