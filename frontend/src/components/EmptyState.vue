<template>
  <article class="panel empty-state">
    <div class="empty-icon" aria-hidden="true">
      <Sparkles :size="28" />
    </div>
    <h2>Generate your first campaign</h2>
    <p>
      Fill the farmer context on the left, or pick a sample persona to see how
      device, literacy, and connectivity reshape the recommended channel and
      hyperlocal copy.
    </p>
    <div class="sample-grid">
      <button
        v-for="s in samples"
        :key="s.id"
        type="button"
        class="sample-card"
        @click="$emit('pick', s)"
      >
        <strong>{{ s.label }}</strong>
        <span>{{ s.description }}</span>
      </button>
    </div>
  </article>
</template>

<script setup>
import { Sparkles } from 'lucide-vue-next'

defineProps({
  samples: { type: Array, default: () => [] }
})
defineEmits(['pick'])
</script>
