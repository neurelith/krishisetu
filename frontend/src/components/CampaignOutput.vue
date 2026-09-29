<template>
  <article class="panel output">
    <div class="panel-head">
      <Languages :size="20" aria-hidden="true" />
      <h2>Generated campaign</h2>
      <span class="panel-meta">{{ result.content.generation_mode }}</span>
    </div>

    <div class="message-tabs" role="tablist" aria-label="Channel preview">
      <button
        v-for="t in tabs"
        :key="t.key"
        type="button"
        role="tab"
        :aria-selected="active === t.key"
        :class="{ active: active === t.key }"
        @click="active = t.key"
      >
        <component :is="t.icon" :size="14" aria-hidden="true" />
        {{ t.label }}
      </button>
    </div>

    <div
      class="campaign-copy"
      :data-channel="active"
      role="tabpanel"
      aria-live="polite"
    >
      <p>{{ currentMessage || '—' }}</p>
      <button
        type="button"
        class="copy-btn"
        :aria-label="`Copy ${active} content`"
        :disabled="!currentMessage"
        @click="copy"
      >
        <component :is="copied ? Check : Copy" :size="14" aria-hidden="true" />
        {{ copied ? 'Copied' : 'Copy' }}
      </button>
    </div>

    <div class="facts">
      <span>{{ result.vernacular.region_style }}</span>
      <span>{{ result.vernacular.script }}</span>
      <span>{{ result.vernacular.sms_safe ? 'SMS safe' : 'Rich format' }}</span>
      <span v-if="result.vernacular.voice_first">Voice-first</span>
    </div>

    <div v-if="result.content.audio_file" class="audio-row">
      <Volume2 :size="16" aria-hidden="true" />
      <audio class="audio" controls :src="audioUrl" />
    </div>
  </article>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import {
  Languages,
  MessageSquare,
  Phone,
  Smartphone,
  Copy,
  Check,
  Volume2
} from 'lucide-vue-next'
import { resolveMediaUrl } from '../api'

const props = defineProps({
  result: { type: Object, required: true }
})

const tabs = [
  { key: 'sms', label: 'SMS', icon: Smartphone },
  { key: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
  { key: 'voice_script', label: 'Voice', icon: Phone }
]

const active = ref('sms')

watch(
  () => props.result?.channel?.primary_channel,
  (channel) => {
    if (channel === 'voice_call') active.value = 'voice_script'
    else if (channel === 'whatsapp') active.value = 'whatsapp'
    else active.value = 'sms'
  },
  { immediate: true }
)

const currentMessage = computed(() => {
  const c = props.result.content || {}
  if (active.value === 'sms') return c.sms || ''
  if (active.value === 'whatsapp') return c.whatsapp || ''
  return c.voice_script || ''
})

const audioUrl = computed(() => resolveMediaUrl(props.result.content?.audio_file))

const copied = ref(false)
async function copy() {
  if (!currentMessage.value) return
  try {
    await navigator.clipboard.writeText(currentMessage.value)
    copied.value = true
    setTimeout(() => (copied.value = false), 1500)
  } catch {
    // Clipboard API can be blocked in insecure contexts; fail silently.
  }
}
</script>
