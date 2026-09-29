<template>
  <article class="panel history">
    <div class="panel-head">
      <History :size="20" aria-hidden="true" />
      <h2>Recent campaigns</h2>
      <span class="panel-meta">{{ items.length }}</span>
    </div>

    <ul v-if="items.length" class="history-list">
      <li
        v-for="(item, i) in items.slice(0, 8)"
        :key="item.id ?? i"
        class="history-item"
      >
        <div class="history-main">
          <strong>{{ item.product || `Farmer #${item.farmer_id}` }}</strong>
          <span class="history-meta">
            {{ pretty(item.channel) }}
            <template v-if="item.segment"> · {{ item.segment }}</template>
            <template v-if="typeof item.predicted_score === 'number'">
              · {{ (item.predicted_score * 100).toFixed(1) }}%
            </template>
          </span>
        </div>
        <span class="history-time">{{ formatTime(item.sent_at || item.created_at) }}</span>
      </li>
    </ul>

    <div v-else class="history-empty">
      <p>No campaign logs yet. Generate a campaign to start populating history.</p>
    </div>
  </article>
</template>

<script setup>
import { History } from 'lucide-vue-next'

defineProps({
  items: { type: Array, default: () => [] }
})

function pretty(value) {
  return String(value || 'unknown').replaceAll('_', ' ')
}

function formatTime(value) {
  if (!value) return ''
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return ''
  const diff = (Date.now() - d.getTime()) / 1000
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.round(diff / 60)}m ago`
  if (diff < 86400) return `${Math.round(diff / 3600)}h ago`
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}
</script>
