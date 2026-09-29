<template>
  <div class="infographic-radar-container">
    <div class="infographic-head-row">
      <div class="head-title-block">
        <span class="sub-label">Atmospheric & Canopy Sensor Fusion</span>
        <h4 class="infographic-title">Microclimate pathogen vector and spray drift window</h4>
      </div>
      <div class="risk-composite-badge">
        <span class="pulse-indicator"></span>
        <span class="risk-score-text">Pathogen Pressure Index: <strong>89/100</strong> (Critical)</span>
      </div>
    </div>

    <div class="radar-split-layout">
      <!-- 5-Axis Radar Chart Area -->
      <div class="radar-chart-column">
        <svg class="radar-svg" viewBox="0 0 380 310" preserveAspectRatio="xMidYMid meet" role="img" aria-label="5-Axis Microclimate Pathogen Vector Radar Chart">
          <!-- Concentric Pentagonal Grids (20%, 40%, 60%, 80%, 100%) -->
          <polygon :points="gridPentagon(0.2)" class="radar-grid-ring" />
          <polygon :points="gridPentagon(0.4)" class="radar-grid-ring" />
          <polygon :points="gridPentagon(0.6)" class="radar-grid-ring" />
          <polygon :points="gridPentagon(0.8)" class="radar-grid-ring" />
          <polygon :points="gridPentagon(1.0)" class="radar-grid-boundary" />

          <!-- Danger Threshold Ring (80% Zone) -->
          <polygon :points="gridPentagon(0.8)" class="radar-danger-threshold" />

          <!-- Axis Lines -->
          <line v-for="(pt, idx) in outerVertices" :key="'axis-' + idx" 
            :x1="center.x" :y1="center.y" :x2="pt.x" :y2="pt.y" 
            class="radar-axis-line" 
          />

          <!-- Actual Pathogen Data Polygon -->
          <polygon :points="dataPolygonPoints" class="radar-data-polygon" />

          <!-- Data Points on Axes -->
          <circle v-for="(pt, idx) in dataVertices" :key="'dot-' + idx"
            :cx="pt.x" :cy="pt.y" r="4.5" class="radar-data-point"
          />

          <!-- Axis Labels and Values -->
          <text :x="labelPositions[0].x" :y="labelPositions[0].y" text-anchor="middle" class="axis-label-text">
            <tspan :x="labelPositions[0].x" dy="-4">Rel. Humidity</tspan>
            <tspan :x="labelPositions[0].x" dy="14" class="axis-val-alert">86% (Critical)</tspan>
          </text>

          <text :x="labelPositions[1].x" :y="labelPositions[1].y" text-anchor="start" class="axis-label-text">
            <tspan :x="labelPositions[1].x" dy="-2">Leaf Wetness</tspan>
            <tspan :x="labelPositions[1].x" dy="14" class="axis-val-alert">9.4 hrs (&gt;6h risk)</tspan>
          </text>

          <text :x="labelPositions[2].x" :y="labelPositions[2].y" text-anchor="middle" class="axis-label-text">
            <tspan :x="labelPositions[2].x" dy="-2">Rain Splash</tspan>
            <tspan :x="labelPositions[2].x" dy="14" class="axis-val-warn">34 mm / 24h</tspan>
          </text>

          <text :x="labelPositions[3].x" :y="labelPositions[3].y" text-anchor="end" class="axis-label-text">
            <tspan :x="labelPositions[3].x" dy="-2">Canopy Density</tspan>
            <tspan :x="labelPositions[3].x" dy="14" class="axis-val-info">0.68 NDVI</tspan>
          </text>

          <text :x="labelPositions[4].x" :y="labelPositions[4].y" text-anchor="end" class="axis-label-text">
            <tspan :x="labelPositions[4].x" dy="-2">Incubation Temp</tspan>
            <tspan :x="labelPositions[4].x" dy="14" class="axis-val-alert">22.4°C (Favorable)</tspan>
          </text>
        </svg>

        <div class="radar-legend-row">
          <div class="legend-item">
            <span class="legend-box legend-danger-box"></span>
            <span>Threshold Boundary (80%)</span>
          </div>
          <div class="legend-item">
            <span class="legend-box legend-data-box"></span>
            <span>Current Canopy Vector</span>
          </div>
        </div>
      </div>

      <!-- 24-Hour Spray & Thermal Drift Timeline Column -->
      <div class="drift-window-column">
        <div class="drift-header">
          <span class="drift-sub">Micro-Meteorological Advisory</span>
          <h5>Field Spray & Thermal Inversion Guide</h5>
          <p class="drift-note font-editorial-italic">
            "High humidity coupled with calm morning air provides a narrow biocontrol uptake window before midday thermal convective currents trigger high droplet drift."
          </p>
        </div>

        <!-- 24-Hour Bar Visualizer -->
        <div class="timeline-bar-wrapper">
          <div class="timeline-hours-labels">
            <span>00:00</span>
            <span>06:00</span>
            <span>09:30</span>
            <span>12:00</span>
            <span>16:30</span>
            <span>20:00</span>
            <span>24:00</span>
          </div>

          <div class="timeline-segments-track">
            <!-- 00:00 - 06:00 Night Dew -->
            <div class="time-segment segment-night seg-w-25" title="Night Hours: Heavy Dew Formation">
              <span class="segment-code">NIGHT</span>
            </div>

            <!-- 06:00 - 09:30 Optimal Window -->
            <div class="time-segment segment-optimal seg-w-optimal" title="OPTIMAL WINDOW: High Stomatal Absorption, Zero Drift">
              <span class="segment-code">OPTIMAL</span>
            </div>

            <!-- 09:30 - 16:30 Prohibited Thermal Hazard -->
            <div class="time-segment segment-prohibited seg-w-prohibited" title="PROHIBITED: Convective Evaporation & 60% Drift Loss">
              <span class="segment-code">DRIFT HAZARD</span>
            </div>

            <!-- 16:30 - 19:30 Secondary Window -->
            <div class="time-segment segment-secondary seg-w-secondary" title="SECONDARY WINDOW: Cooling Canopy, Low Wind">
              <span class="segment-code">SECONDARY</span>
            </div>

            <!-- 19:30 - 24:00 Night Inversion -->
            <div class="time-segment segment-night seg-w-night-late" title="Night Hours: Darkness & Evaporation Halt">
              <span class="segment-code">NIGHT</span>
            </div>

            <!-- Current Time Indicator Needle (e.g. 07:45 AM) -->
            <div class="current-time-marker marker-pos-now" title="Current Field Time: 07:45 AM">
              <span class="marker-flag">NOW (07:45)</span>
              <span class="marker-line"></span>
            </div>
          </div>
        </div>

        <!-- Operational Drift Rule Matrix -->
        <div class="drift-metrics-grid">
          <div class="drift-metric-card">
            <span class="dm-label">Anemometer Wind Speed</span>
            <span class="dm-val text-forest">4.8 km/h NW</span>
            <span class="dm-status">Optimal (&lt; 10 km/h)</span>
          </div>

          <div class="drift-metric-card">
            <span class="dm-label">Droplet Evaporation Risk</span>
            <span class="dm-val text-alert">High Midday (&gt; 28°C)</span>
            <span class="dm-status">Lockout at 10:00 AM</span>
          </div>

          <div class="drift-metric-card">
            <span class="dm-label">Foliar Stomatal Conductance</span>
            <span class="dm-val text-forest">Peak at 07:30 AM</span>
            <span class="dm-status">Max Bio-Penetration</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const center = { x: 190, y: 155 }
const radius = 92

// 5 Axes angles in radians (starting from top, clockwise: -90°, -18°, 54°, 126°, 198°)
const angles = [
  -Math.PI / 2,
  -Math.PI / 2 + (2 * Math.PI) / 5,
  -Math.PI / 2 + (4 * Math.PI) / 5,
  -Math.PI / 2 + (6 * Math.PI) / 5,
  -Math.PI / 2 + (8 * Math.PI) / 5
]

// Current normalized pathogen vector weights (0.0 to 1.0)
const axisValues = [0.86, 0.78, 0.68, 0.68, 0.82]

function getPoint(angle, r) {
  return {
    x: center.x + r * Math.cos(angle),
    y: center.y + r * Math.sin(angle)
  }
}

function gridPentagon(scaleFactor) {
  const r = radius * scaleFactor
  return angles.map(a => {
    const pt = getPoint(a, r)
    return `${pt.x.toFixed(1)},${pt.y.toFixed(1)}`
  }).join(' ')
}

const outerVertices = computed(() => {
  return angles.map(a => getPoint(a, radius))
})

const dataVertices = computed(() => {
  return angles.map((a, i) => getPoint(a, radius * axisValues[i]))
})

const dataPolygonPoints = computed(() => {
  return dataVertices.value.map(pt => `${pt.x.toFixed(1)},${pt.y.toFixed(1)}`).join(' ')
})

const labelPositions = [
  { x: 190, y: 26 },
  { x: 312, y: 125 },
  { x: 265, y: 280 },
  { x: 115, y: 280 },
  { x: 68, y: 125 }
]
</script>

<style scoped>
.infographic-radar-container {
  padding: var(--space-4) var(--space-5);
  background: var(--paper-raised);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md);
  margin-top: var(--space-4);
}

.infographic-head-row {
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

.infographic-title {
  font-size: var(--step-0);
  font-weight: 700;
  color: var(--ink);
  margin: var(--space-1) 0 0 0;
}

.risk-composite-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: 6px 14px;
  background: var(--brick-wash);
  border: 1px solid var(--brick-line);
  border-radius: var(--radius-sm);
}

.pulse-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--alert);
}

.risk-score-text {
  font-size: 0.8125rem;
  font-family: var(--font-mono);
  color: var(--brick);
}

.risk-score-text strong {
  font-size: 0.875rem;
}

.radar-split-layout {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: var(--space-5);
  align-items: start;
}

/* Radar Chart Styling */
.radar-chart-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-3) var(--space-2);
}

.radar-svg {
  width: 100%;
  max-width: 320px;
  height: auto;
  overflow: visible;
}

.radar-grid-ring {
  fill: none;
  stroke: var(--hairline);
  stroke-width: 1;
}

.radar-grid-boundary {
  fill: none;
  stroke: var(--hairline-strong);
  stroke-width: 1.5;
}

.radar-danger-threshold {
  fill: none;
  stroke: var(--alert);
  stroke-width: 1.5;
  stroke-dasharray: 4, 3;
}

.radar-axis-line {
  stroke: var(--hairline-strong);
  stroke-width: 1;
  stroke-dasharray: 2, 2;
}

.radar-data-polygon {
  fill: var(--brick-wash);
  stroke: var(--brick);
  stroke-width: 2;
}

.radar-data-point {
  fill: var(--brick);
  stroke: var(--paper-raised);
  stroke-width: 1.5;
}

.axis-label-text {
  font-family: var(--font-mono);
  font-size: 12px;
  fill: var(--ink-2);
}

.axis-val-alert {
  font-weight: 700;
  fill: var(--alert-text);
  font-size: 12px;
}

.axis-val-warn {
  font-weight: 700;
  fill: var(--ochre);
  font-size: 12px;
}

.axis-val-info {
  font-weight: 700;
  fill: var(--canopy);
  font-size: 12px;
}

.radar-legend-row {
  display: flex;
  gap: var(--space-3);
  font-size: 0.8125rem;
  font-family: var(--font-mono);
  color: var(--ink-2);
  margin-top: var(--space-2);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.legend-box {
  width: 12px;
  height: 8px;
  border-radius: 1px;
}

.legend-danger-box {
  border: 1px dashed var(--alert);
  background: transparent;
}

.legend-data-box {
  background: var(--brick-wash);
  border: 1px solid var(--brick);
}

/* Drift Window Column */
.drift-window-column {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.drift-header h5 {
  font-size: var(--step-0);
  font-weight: 700;
  color: var(--ink);
  margin: var(--space-1) 0 var(--space-1) 0;
}

.drift-sub {
  font-family: var(--font-mono);
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--ink-3);
  text-transform: uppercase;
}

.drift-note {
  font-size: 0.8125rem;
  color: var(--ink-2);
  line-height: 1.45;
  margin: 0;
}

/* Timeline Horizontal Track */
.timeline-bar-wrapper {
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: var(--space-3) var(--space-3) var(--space-4) var(--space-3);
}

.timeline-hours-labels {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--ink-3);
  margin-bottom: var(--space-1);
}

.timeline-segments-track {
  position: relative;
  height: 28px;
  display: flex;
  border-radius: 6px;
  overflow: visible;
  border: 1px solid var(--hairline-strong);
}

.time-segment {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--paper-raised);
}

.segment-night {
  background: var(--ink-3);
}

.segment-optimal {
  background: var(--leaf);
}

.segment-prohibited {
  background: var(--brick);
}

.segment-secondary {
  background: var(--leaf-bright);
}

.seg-w-25 { width: 25%; }
.seg-w-optimal { width: 14.6%; }
.seg-w-prohibited { width: 29.2%; }
.seg-w-secondary { width: 12.5%; }
.seg-w-night-late { width: 18.7%; }
.marker-pos-now { left: 32.3%; }

.current-time-marker {
  position: absolute;
  top: -8px;
  bottom: -6px;
  width: 2px;
  z-index: 5;
}

.marker-flag {
  position: absolute;
  top: -16px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--canopy);
  color: var(--paper-raised);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: var(--radius-xs);
  white-space: nowrap;
}

.marker-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 2px;
  background: var(--canopy);
}

/* Drift Metrics Grid */
.drift-metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--space-2);
}

.drift-metric-card {
  padding: var(--space-2) var(--space-3);
  background: var(--paper-sunken);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.dm-label {
  font-size: 0.8125rem;
  color: var(--ink-3);
  font-weight: 600;
}

.dm-val {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  font-weight: 700;
}

.dm-status {
  font-size: 0.8125rem;
  color: var(--ink-2);
}

.text-forest { color: var(--leaf); }
.text-alert { color: var(--alert-text); }

@media (max-width: 900px) {
  .radar-split-layout {
    grid-template-columns: 1fr;
  }
}
</style>
