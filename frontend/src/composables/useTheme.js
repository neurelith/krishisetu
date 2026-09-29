import { ref, watch } from 'vue'

const STORAGE_KEY = 'krishisetu:theme'

function preferredTheme() {
  if (typeof window === 'undefined') return 'light'
  const stored = window.localStorage?.getItem(STORAGE_KEY)
  if (stored === 'light' || stored === 'dark') return stored
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const theme = ref(preferredTheme())

function applyTheme(value) {
  if (typeof document === 'undefined') return
  document.documentElement.dataset.theme = value
}

applyTheme(theme.value)

watch(theme, (value) => {
  applyTheme(value)
  try {
    window.localStorage?.setItem(STORAGE_KEY, value)
  } catch {
    // ignore quota / privacy mode errors
  }
})

export function useTheme() {
  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }
  return { theme, toggle }
}
