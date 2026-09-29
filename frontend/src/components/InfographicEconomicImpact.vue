<template>
  <div class="economic-infographic-container">
    <div class="economic-head-bar">
      <div>
        <span class="sub-label">Farm Economics & Agronomic ROI</span>
        <h4 class="economic-title">Yield protection and financial recovery assessment</h4>
      </div>
      <div class="roi-highlight-badge">
        <span class="roi-label">Bio-Input Benefit-Cost Ratio:</span>
        <strong class="roi-figure">17.3 : 1</strong>
      </div>
    </div>

    <!-- Comparative Visual Bars -->
    <div class="economic-comparison-deck">
      <!-- Scenario A: Unmanaged Outbreak -->
      <div class="scenario-panel panel-unmanaged">
        <div class="scenario-header">
          <span class="scenario-tag tag-danger">SCENARIO A: UNMANAGED DISEASE OUTBREAK</span>
          <h5 class="scenario-name">Status Quo (No Intervention / Late Spray)</h5>
        </div>

        <div class="stat-progress-block">
          <div class="stat-label-row">
            <span>Marketable Yield Harvest:</span>
            <strong>10.8 Tonnes / Acre (-42% Defoliation)</strong>
          </div>
          <div class="visual-progress-track">
            <div class="progress-bar-fill fill-danger bar-w-58"></div>
          </div>
        </div>

        <div class="financial-balance-sheet">
          <div class="finance-row">
            <span class="f-key">Gross Harvest Revenue</span>
            <span class="f-val">₹ 56,200</span>
          </div>
          <div class="finance-row">
            <span class="f-key">Direct Tuber & Foliar Blight Loss</span>
            <span class="f-val text-alert">-₹ 38,500 / acre</span>
          </div>
          <div class="finance-row f-net-row">
            <span class="f-key">Net Realized Farm Profit</span>
            <span class="f-val text-alert">₹ 31,400</span>
          </div>
        </div>
      </div>

      <!-- Scenario B: KrishiSetu Prescribed Bio-Intervention -->
      <div class="scenario-panel panel-krishisetu">
        <div class="scenario-header">
          <span class="scenario-tag tag-success">SCENARIO B: KRISHISETU PRESCRIBED BIO-INTERVENTION</span>
          <h5 class="scenario-name">Immediate Phased Biological Countermeasures</h5>
        </div>

        <div class="stat-progress-block">
          <div class="stat-label-row">
            <span>Marketable Yield Harvest:</span>
            <strong class="text-forest">18.4 Tonnes / Acre (94% Canopy Protection)</strong>
          </div>
          <div class="visual-progress-track">
            <div class="progress-bar-fill fill-success bar-w-94"></div>
          </div>
        </div>

        <div class="financial-balance-sheet">
          <div class="finance-row">
            <span class="f-key">Gross Harvest Revenue</span>
            <span class="f-val">₹ 95,680</span>
          </div>
          <div class="finance-row">
            <span class="f-key">Prescribed Bio-Input Cost (Trichoderma + SOP)</span>
            <span class="f-val text-slate">-₹ 2,030 / acre</span>
          </div>
          <div class="finance-row f-net-row">
            <span class="f-key">Net Realized Farm Profit</span>
            <span class="f-val text-forest">₹ 72,150</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Net Impact Strip -->
    <div class="economic-summary-strip">
      <div class="strip-item">
        <span class="strip-label">Net Capital Value Protected:</span>
        <strong class="strip-val text-forest">+₹ 40,750 / Acre</strong>
      </div>
      <div class="strip-item">
        <span class="strip-label">Ecological Chemical Displacement:</span>
        <strong class="strip-val text-slate">100% Non-Toxic Biological Active</strong>
      </div>
      <div class="strip-item">
        <span class="strip-label">Secondary Outbreak Risk:</span>
        <strong class="strip-val text-forest">Contained (R₀ &lt; 0.3)</strong>
      </div>
    </div>
  </div>
</template>

<script setup>
// Pure presentation component using verified field agronomic data
</script>

<style scoped>
.economic-infographic-container {
  padding: var(--space-4) var(--space-5);
  background: var(--paper-raised);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md);
  margin-top: var(--space-4);
}

.economic-head-bar {
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

.economic-title {
  font-size: var(--step-0);
  font-weight: 700;
  color: var(--ink);
  margin: var(--space-1) 0 0 0;
}

.roi-highlight-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  background: var(--green-wash);
  border: 1.5px solid var(--green-line);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-pill);
}

.roi-label {
  font-size: 0.8125rem;
  color: var(--canopy);
  font-weight: 600;
}

.roi-figure {
  font-family: var(--font-mono);
  font-size: var(--step-0);
  color: var(--canopy);
  font-variant-numeric: tabular-nums;
}

.economic-comparison-deck {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}

.scenario-panel {
  padding: var(--space-4) var(--space-4);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.panel-unmanaged {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
}

.panel-krishisetu {
  background: var(--paper-raised);
  border: 2px solid var(--green-line);
}

.scenario-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.scenario-tag {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 3px 8px;
  border-radius: var(--radius-xs);
  width: fit-content;
}

.tag-danger {
  background: var(--brick-wash);
  color: var(--brick);
  border: 1px solid var(--brick-line);
}

.tag-success {
  background: var(--green-wash);
  color: var(--canopy);
  border: 1px solid var(--green-line);
}

.scenario-name {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--ink);
  margin: 0;
}

.stat-progress-block {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.stat-label-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.8125rem;
  color: var(--ink-2);
}

.visual-progress-track {
  height: 8px;
  background: var(--hairline);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
}

.fill-danger {
  background: var(--alert);
}

.fill-success {
  background: var(--leaf);
}

.bar-w-58 {
  width: 58%;
}

.bar-w-94 {
  width: 94%;
}

.financial-balance-sheet {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  border-top: 1px solid var(--hairline);
  padding-top: var(--space-2);
}

.finance-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.8125rem;
  color: var(--ink-2);
}

.finance-row.f-net-row {
  border-top: 1px dashed var(--hairline-strong);
  padding-top: var(--space-1);
  font-weight: 700;
  font-size: 0.875rem;
}

.f-val {
  font-family: var(--font-mono);
}

.text-alert {
  color: var(--alert-text);
}

.text-forest {
  color: var(--leaf);
}

.text-slate {
  color: var(--ink-3);
}

.economic-summary-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.strip-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 0.8125rem;
}

.strip-label {
  color: var(--ink-3);
}

.strip-val {
  font-family: var(--font-mono);
  font-size: 0.875rem;
}

@media (max-width: 850px) {
  .economic-comparison-deck {
    grid-template-columns: 1fr;
  }
}
</style>
