import { computed, reactive, watch } from 'vue'

const STORAGE_KEY = 'krishisetu:lastFarmer'

const REQUIRED_FIELDS = [
  ['state', 'State is required'],
  ['district', 'District is required'],
  ['main_crop', 'Crop is required'],
  ['pest_threat', 'Pest or disease threat is required']
]

function emptyState() {
  return {
    farmer_name: '',
    farmer: {
      grower_id: '',
      state: '',
      district: '',
      tehsil_block: '',
      season: '',
      language: '',
      main_crop: '',
      campaign_crop: '',
      campaign_product: '',
      pest_threat: '',
      weather_risk: '',
      device_type: 'smartphone',
      connectivity: 'good',
      literacy_level: 'medium',
      grower_age: null,
      grower_farm_size: null,
      high_value_farmer: false,
      hist_open_rate: 0,
      hist_click_rate: 0,
      message_count_history: 0
    }
  }
}

function loadInitial() {
  if (typeof window === 'undefined') return emptyState()
  try {
    const raw = window.localStorage?.getItem(STORAGE_KEY)
    if (!raw) return emptyState()
    const parsed = JSON.parse(raw)
    const base = emptyState()
    return {
      farmer_name: parsed.farmer_name ?? '',
      farmer: { ...base.farmer, ...(parsed.farmer || {}) }
    }
  } catch {
    return emptyState()
  }
}

export function useFarmerForm() {
  const state = reactive(loadInitial())
  const errors = reactive({})

  watch(
    state,
    (value) => {
      try {
        window.localStorage?.setItem(STORAGE_KEY, JSON.stringify(value))
      } catch {
        // ignore
      }
    },
    { deep: true }
  )

  const isValid = computed(() => {
    return REQUIRED_FIELDS.every(([key]) => {
      const val = state.farmer[key]
      return typeof val === 'string' ? val.trim().length > 0 : Boolean(val)
    })
  })

  function validate() {
    Object.keys(errors).forEach((k) => delete errors[k])
    for (const [key, message] of REQUIRED_FIELDS) {
      const val = state.farmer[key]
      const empty = typeof val === 'string' ? val.trim().length === 0 : !val
      if (empty) errors[key] = message
    }
    return Object.keys(errors).length === 0
  }

  function clearError(key) {
    if (errors[key]) delete errors[key]
  }

  function loadSample(sample) {
    state.farmer_name = sample.farmer_name || ''
    Object.assign(state.farmer, emptyState().farmer, sample.farmer || {})
    Object.keys(errors).forEach((k) => delete errors[k])
  }

  function reset() {
    const fresh = emptyState()
    state.farmer_name = fresh.farmer_name
    Object.assign(state.farmer, fresh.farmer)
    Object.keys(errors).forEach((k) => delete errors[k])
  }

  function payload() {
    // Strip empty strings so backend Optional fields stay None and validators
    // don't get tripped up by "" coerced to numeric.
    const cleaned = Object.fromEntries(
      Object.entries(state.farmer).filter(
        ([, v]) => v !== '' && v !== null && v !== undefined
      )
    )
    cleaned.campaign_crop = cleaned.campaign_crop || cleaned.main_crop
    return {
      farmer_name: state.farmer_name?.trim() || 'Kisan bhai',
      farmer: cleaned
    }
  }

  return { state, errors, isValid, validate, clearError, loadSample, reset, payload }
}
