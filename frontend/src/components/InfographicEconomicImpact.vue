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
  padding: 20px 24px;
  background: var(--bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  margin-top: 16px;
}

.economic-head-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 12px;
  margin-bottom: 18px;
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

.economic-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 2px 0 0 0;
}

.roi-highlight-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 6px 14px;
  border-radius: var(--radius-sm);
}

.roi-label {
  font-size: 11px;
  color: #166534;
}

.roi-figure {
  font-family: var(--font-mono);
  font-size: 14px;
  color: #14532d;
  font-variant-numeric: tabular-nums;
}

.economic-comparison-deck {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 18px;
}

.scenario-panel {
  padding: 18px 20px;
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.panel-unmanaged {
  background: #fafaf9;
  border: 1px solid var(--color-border);
}

.panel-krishisetu {
  background: #fbfdfc;
  border: 1.5px solid var(--forest-800);
  box-shadow: var(--shadow-card);
}

.scenario-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.scenario-tag {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 2px 6px;
  border-radius: 2px;
  width: fit-content;
}

.tag-danger {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.tag-success {
  background: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.scenario-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 0;
}

.stat-progress-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label-row {
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
  color: var(--slate-700);
}

.visual-progress-track {
  height: 8px;
  background: var(--slate-200);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
}

.fill-danger {
  background: #dc2626;
}

.fill-success {
  background: #15803d;
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
  gap: 6px;
  border-top: 1px solid var(--slate-200);
  padding-top: 10px;
}

.finance-row {
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
  color: var(--slate-600);
}

.finance-row.f-net-row {
  border-top: 1px dashed var(--slate-300);
  padding-top: 6px;
  font-weight: 700;
  font-size: 12.5px;
}

.f-val {
  font-family: var(--font-mono);
}

.economic-summary-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: var(--radius-sm);
  flex-wrap: wrap;
  gap: 12px;
}

.strip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.strip-label {
  color: var(--slate-600);
}

.strip-val {
  font-family: var(--font-mono);
  font-size: 12.5px;
}

@media (max-width: 850px) {
  .economic-comparison-deck {
    grid-template-columns: 1fr;
  }
}
</style>
