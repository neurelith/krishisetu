<template>
  <section class="score-band" aria-label="Campaign scorecard">
    <article class="score-card score-card-primary">
      <p class="eyebrow">Engagement probability</p>
      <strong class="score-value">{{ engagement }}</strong>
      <span>{{ result.prediction.segment }} segment</span>
      <div class="score-progress" aria-hidden="true">
        <span :style="{ width: progressWidth }" />
      </div>
    </article>

    <article class="score-card">
      <p class="eyebrow">Best channel</p>
      <strong>
        <component :is="channelIcon" :size="20" aria-hidden="true" />
        {{ pretty(result.channel.primary_channel) }}
      </strong>
      <span>{{ result.vernacular.language }} · {{ result.vernacular.complexity_level }}</span>
    </article>

    <article class="score-card">
      <p class="eyebrow">Priority</p>
      <strong>{{ result.channel.priority_score }}</strong>
      <span>{{ result.channel.frequency_per_month }} touch / month</span>
    </article>

    <article class="score-card" :class="urgencyClass">
      <p class="eyebrow">Urgency</p>
      <strong>{{ result.urgency.urgency_score }}</strong>
      <span>{{ result.urgency.urgency_level }}</span>
    </article>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { MessageSquare, Phone, Smartphone, Radio } from 'lucide-vue-next'

const props = defineProps({
  result: { type: Object, required: true }
})

const engagement = computed(() => {
  const v = props.result.prediction?.engagement_probability ?? 0
  return `${(v * 100).toFixed(1)}%`
})
const progressWidth = computed(() => {
  const v = Math.max(0, Math.min(1, props.result.prediction?.engagement_probability ?? 0))
  // Boost visibility for the typically-low probabilities (cap at 100%).
  return `${Math.min(100, v * 400).toFixed(1)}%`
})

const channelIcon = computed(() => {
  const c = props.result.channel?.primary_channel
  if (c === 'whatsapp') return MessageSquare
  if (c === 'voice_call') return Phone
  if (c === 'sms') return Smartphone
  return Radio
})

const urgencyClass = computed(() => {
  const lvl = (props.result.urgency?.urgency_level || '').toLowerCase()
  if (lvl.includes('high') || lvl.includes('critical')) return 'urgency-high'
  if (lvl.includes('medium') || lvl.includes('moderate')) return 'urgency-medium'
  return 'urgency-low'
})

function pretty(value) {
  return String(value || '').replaceAll('_', ' ')
}
</script>
