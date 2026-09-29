<template>
  <header class="topbar">
    <div class="topbar-brand">
      <div class="brand-mark" aria-hidden="true">
        <Leaf :size="22" />
      </div>
      <div>
        <p class="eyebrow">Terrapulse · Track 1</p>
        <h1>Adaptive Agricultural Campaign Intelligence</h1>
      </div>
    </div>
    <div class="topbar-actions">
      <span class="api-pill" :class="`api-${apiStatus}`" :title="`Backend: ${apiStatus}`">
        <span class="api-dot" aria-hidden="true" />
        {{ apiStatus }}
      </span>
      <button class="ghost icon-btn" :aria-label="themeLabel" :title="themeLabel" @click="$emit('toggle-theme')">
        <component :is="theme === 'dark' ? Sun : Moon" :size="18" />
      </button>
      <button class="ghost" :disabled="loadingAnalytics" @click="$emit('refresh')">
        <RefreshCw :size="16" :class="{ spinning: loadingAnalytics }" />
        <span>Refresh metrics</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { Leaf, Moon, Sun, RefreshCw } from 'lucide-vue-next'

const props = defineProps({
  apiStatus: { type: String, default: 'unknown' },
  loadingAnalytics: { type: Boolean, default: false },
  theme: { type: String, default: 'light' }
})
defineEmits(['refresh', 'toggle-theme'])

const themeLabel = computed(() =>
  props.theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
)
</script>
