<template>
  <article class="panel preview-card">
    <div class="panel-head">
      <Image :size="20" aria-hidden="true" />
      <h2>Channel preview</h2>
      <span class="panel-meta">{{ pretty(channel) }}</span>
    </div>

    <!-- WhatsApp: chat bubble in a phone shell. -->
    <div v-if="channel === 'whatsapp'" class="phone-shell whatsapp">
      <div class="phone-header">
        <span class="phone-dot" />
        <span>{{ farmerName || 'Farmer' }}</span>
      </div>
      <div v-if="media" class="chat-bubble bubble-media">
        <div class="media-tile">
          <span>{{ media.type || 'infographic' }}</span>
          <strong>{{ media.topic || 'crop advisory' }}</strong>
        </div>
        <p v-if="media.caption">{{ media.caption }}</p>
        <small v-if="media.video_script">{{ media.video_script }}</small>
      </div>
      <div v-if="message" class="chat-bubble">{{ message }}</div>
    </div>

    <!-- SMS: minimal bubble in a feature-phone shell. -->
    <div v-else-if="channel === 'sms'" class="phone-shell sms">
      <div class="phone-header">
        <span class="phone-dot" />
        <span>SMS · {{ farmerName || 'Farmer' }}</span>
      </div>
      <div class="sms-bubble">{{ message || '—' }}</div>
      <p class="phone-meta">{{ smsLength }} chars · {{ smsLength > 160 ? 'multi-part' : 'single SMS' }}</p>
    </div>

    <!-- Voice: waveform mock + transcript. -->
    <div v-else class="voice-shell">
      <div class="waveform" aria-hidden="true">
        <span v-for="n in 36" :key="n" :style="{ height: barHeight(n) }" />
      </div>
      <div class="voice-transcript">
        <p class="phone-meta">Voice script · {{ language }}</p>
        <p>{{ message || '—' }}</p>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { Image } from 'lucide-vue-next'

const props = defineProps({
  result: { type: Object, required: true },
  farmerName: { type: String, default: '' }
})

const channel = computed(() => {
  const c = props.result.channel?.primary_channel
  if (c === 'whatsapp') return 'whatsapp'
  if (c === 'voice_call') return 'voice'
  return 'sms'
})

const media = computed(() => props.result.content?.recommended_media || null)
const language = computed(() => props.result.vernacular?.language || 'English')

const message = computed(() => {
  const c = props.result.content || {}
  if (channel.value === 'whatsapp') return c.whatsapp || ''
  if (channel.value === 'voice') return c.voice_script || ''
  return c.sms || ''
})

const smsLength = computed(() => (props.result.content?.sms || '').length)

function barHeight(n) {
  // Pseudo-random but stable per index so the waveform doesn't shimmer on re-render.
  const seed = Math.sin(n * 12.9898) * 43758.5453
  const f = seed - Math.floor(seed)
  return `${20 + Math.round(f * 70)}%`
}

function pretty(value) {
  return String(value || '').replaceAll('_', ' ')
}
</script>
