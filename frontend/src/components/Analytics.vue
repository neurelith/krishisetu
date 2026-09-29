<template>
  <article class="panel analytics">
    <div class="panel-head">
      <BarChart3 :size="20" aria-hidden="true" />
      <h2>Campaign analytics</h2>
      <span class="panel-meta">{{ history.length }} logs</span>
    </div>

    <div v-if="loading" class="chart-skeleton">
      <Skeleton height="180px" radius="8px" />
    </div>
    <canvas v-else ref="chartEl" height="180" aria-label="Segment distribution chart" />

    <div class="metric-grid">
      <div>
        <strong>{{ history.length }}</strong>
        <span>campaign logs</span>
      </div>
      <div>
        <strong>{{ avgEngagement }}</strong>
        <span>avg engagement</span>
      </div>
      <div>
        <strong>{{ topChannel }}</strong>
        <span>top channel</span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { BarChart3 } from 'lucide-vue-next'
import Chart from 'chart.js/auto'
import Skeleton from './Skeleton.vue'

const props = defineProps({
  stats: { type: Array, default: () => [] },
  history: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  theme: { type: String, default: 'light' }
})

const chartEl = ref(null)
let chart = null

const avgEngagement = computed(() => {
  if (!props.history.length) return '—'
  const total = props.history.reduce((acc, h) => acc + (Number(h.predicted_score) || 0), 0)
  return `${((total / props.history.length) * 100).toFixed(1)}%`
})

const topChannel = computed(() => {
  if (!props.history.length) return '—'
  const counts = {}
  for (const h of props.history) {
    const c = h.channel || 'unknown'
    counts[c] = (counts[c] || 0) + 1
  }
  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1])
  return (entries[0]?.[0] || '—').replaceAll('_', ' ')
})

function paletteFor(theme) {
  return theme === 'dark'
    ? ['#7ed7a8', '#f6c34a', '#6aa9ff', '#3aa365']
    : ['#7ca982', '#f2c14e', '#2f80ed', '#1f7a4d']
}

function gridColor(theme) {
  return theme === 'dark' ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)'
}

function tickColor(theme) {
  return theme === 'dark' ? '#c8d6cc' : '#405348'
}

async function render() {
  await nextTick()
  if (!chartEl.value) return
  const rows = (props.stats || []).map((row) => ({
    label: row.segment || row.label || 'unknown',
    value: Number(row.count ?? row.value ?? 0)
  }))
  chart?.destroy()
  chart = new Chart(chartEl.value, {
    type: 'bar',
    data: {
      labels: rows.map((r) => r.label),
      datasets: [
        {
          label: 'Farmers',
          data: rows.map((r) => r.value),
          backgroundColor: paletteFor(props.theme),
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: tickColor(props.theme) }, grid: { display: false } },
        y: {
          beginAtZero: true,
          ticks: { color: tickColor(props.theme) },
          grid: { color: gridColor(props.theme) }
        }
      }
    }
  })
}

watch(() => [props.stats, props.theme, props.loading], render, { deep: true, immediate: true })

onBeforeUnmount(() => chart?.destroy())
</script>
