<template>
  <div class="detail-disclosure">
    <button
      type="button"
      class="detail-disclosure-toggle btn-gov-outline btn-compact"
      :aria-expanded="open ? 'true' : 'false'"
      @click="open = !open"
    >
      <PhCaretDown :size="16" weight="bold" :class="['disclosure-caret', { 'caret-open': open }]" />
      <span>{{ open ? hideLabel : showLabel }}</span>
    </button>
    <div v-show="open" class="detail-disclosure-body">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { PhCaretDown } from '@phosphor-icons/vue'

defineProps({
  showLabel: { type: String, default: 'Show more detail' },
  hideLabel: { type: String, default: 'Hide detail' }
})

const open = ref(false)
</script>

<style scoped>
.detail-disclosure {
  margin-top: var(--space-4);
}

.detail-disclosure-toggle {
  min-height: 48px;
}

.disclosure-caret {
  transition: transform 150ms;
}

.caret-open {
  transform: rotate(180deg);
}

.detail-disclosure-body {
  margin-top: var(--space-4);
}
</style>
