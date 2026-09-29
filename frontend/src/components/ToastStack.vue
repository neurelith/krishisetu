<template>
  <div class="toast-stack" role="region" aria-label="Notifications">
    <transition-group name="toast">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="toast"
        :class="`toast-${t.type}`"
        role="status"
        aria-live="polite"
      >
        <component :is="iconFor(t.type)" :size="18" aria-hidden="true" />
        <span class="toast-msg">{{ t.message }}</span>
        <button class="toast-close" :aria-label="`Dismiss notification`" @click="dismiss(t.id)">
          <X :size="14" aria-hidden="true" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { CheckCircle2, AlertTriangle, Info, X } from 'lucide-vue-next'
import { useToast } from '../composables/useToast'

const { toasts, dismiss } = useToast()

function iconFor(type) {
  if (type === 'success') return CheckCircle2
  if (type === 'error') return AlertTriangle
  return Info
}
</script>
