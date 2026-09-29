import { ref } from 'vue'

// Module-singleton toast queue so any component can emit without prop drilling.
const toasts = ref([])
let nextId = 1

function push(message, { type = 'info', timeout = 4000 } = {}) {
  const id = nextId++
  toasts.value.push({ id, message, type })
  if (timeout > 0) {
    setTimeout(() => dismiss(id), timeout)
  }
  return id
}

function dismiss(id) {
  const idx = toasts.value.findIndex((t) => t.id === id)
  if (idx !== -1) toasts.value.splice(idx, 1)
}

export function useToast() {
  return {
    toasts,
    dismiss,
    success: (msg, opts) => push(msg, { ...opts, type: 'success' }),
    error: (msg, opts) => push(msg, { ...opts, type: 'error', timeout: opts?.timeout ?? 6000 }),
    info: (msg, opts) => push(msg, { ...opts, type: 'info' })
  }
}
