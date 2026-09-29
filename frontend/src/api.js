import axios from 'axios'

const getApiBaseUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) return import.meta.env.VITE_API_BASE_URL
  if (typeof window !== 'undefined') {
    const host = window.location.hostname === 'localhost' ? '127.0.0.1' : window.location.hostname
    return `${window.location.protocol}//${host}:8000`
  }
  return 'http://127.0.0.1:8000'
}

export const API_BASE_URL = getApiBaseUrl()

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000
})

function describeError(err, fallback) {
  if (err?.response?.data?.detail) {
    const detail = err.response.data.detail
    return typeof detail === 'string' ? detail : JSON.stringify(detail)
  }
  if (err?.code === 'ERR_NETWORK') {
    return `Cannot reach backend at ${API_BASE_URL}. Is uvicorn running?`
  }
  if (err?.code === 'ECONNABORTED') {
    return 'Backend timed out. The service may be cold-starting; try again.'
  }
  return err?.message || fallback
}

// ============================================================================
// KrishiSetu Core Digital Public Good API Functions
// ============================================================================

/**
 * Upload a leaf image to Google Gemini Multimodal Vision for disease diagnostics.
 */
export async function diagnoseCropDisease(fileOrBlob, cropHint = 'Rice') {
  try {
    const formData = new FormData()
    formData.append('image', fileOrBlob)
    formData.append('crop_hint', cropHint)

    const { data } = await api.post('/api/diagnose', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    console.log('KrishiSetu /api/diagnose response:', data)
    return data
  } catch (err) {
    throw new Error(describeError(err, 'Leaf diagnosis failed'))
  }
}

/**
 * Fuses farm context, leaf diagnosis, weather, soil, and satellite data with ICAR RAG
 * using Google Gemini to generate a contextual regenerative advisory with audio.
 */
export async function generateRegenerativeAdvisory(farmContext) {
  try {
    const { data } = await api.post('/api/advisory', farmContext)
    console.log('KrishiSetu /api/advisory response:', data)
    return data
  } catch (err) {
    throw new Error(describeError(err, 'Advisory generation failed'))
  }
}

/**
 * Normalizes raw state portal payloads (e.g. West Bengal Matir Katha vs Bihar DBT Krishi)
 * into the open DPG FarmContext v1.0 standard.
 */
export async function normalizeStatePayload(stateOrigin, rawPayload, customRules = null) {
  try {
    const body = {
      state_origin: stateOrigin,
      raw_payload: rawPayload
    }
    if (customRules) {
      body.custom_rules = customRules
    }
    const { data } = await api.post('/api/interop/normalize', body)
    console.log('KrishiSetu /api/interop/normalize response:', data)
    return data
  } catch (err) {
    throw new Error(describeError(err, 'State payload normalization failed'))
  }
}

/**
 * Fetches sample raw state payloads for instant live UI testing.
 */
export async function fetchSampleStatePayload(state) {
  try {
    const { data } = await api.get(`/api/interop/sample-payload/${state}`)
    return data
  } catch (err) {
    throw new Error(describeError(err, `Failed to load sample payload for ${state}`))
  }
}

/**
 * Fetches regional pest outbreak alerts and cross-border corridor telemetry.
 */
export async function fetchOutbreakTelemetry() {
  try {
    const { data } = await api.get('/api/interop/telemetry')
    return Array.isArray(data) ? data : []
  } catch (err) {
    throw new Error(describeError(err, 'Failed to load outbreak telemetry'))
  }
}

/**
 * Injects a simulated pest outbreak in a border district to demonstrate live cross-state alerting.
 */
export async function simulateOutbreakEvent(pestName, originState, originDistrict, affectedCrop, severity) {
  try {
    const { data } = await api.post('/api/interop/simulate-outbreak', null, {
      params: {
        pest_name: pestName,
        origin_state: originState,
        origin_district: originDistrict,
        affected_crop: affectedCrop,
        severity: severity
      }
    })
    return data
  } catch (err) {
    throw new Error(describeError(err, 'Outbreak simulation failed'))
  }
}

/**
 * Fetches Open-Meteo agro-weather telemetry.
 */
export async function fetchAgroWeather(lat = 23.47, lon = 88.55, label = 'Nadia, West Bengal') {
  try {
    const { data } = await api.get('/api/telemetry/weather', {
      params: { lat, lon, location_label: label }
    })
    return data
  } catch (err) {
    console.warn('Weather fetch fallback:', err)
    return null
  }
}

/**
 * Fetches Soil Health Card 12-parameter data.
 */
export async function fetchSoilHealth(state = 'West Bengal', district = 'Nadia') {
  try {
    const { data } = await api.get('/api/telemetry/soil', {
      params: { state, district }
    })
    return data
  } catch (err) {
    console.warn('Soil health fetch fallback:', err)
    return null
  }
}

/**
 * Fetches Copernicus Sentinel-2 NDVI metrics.
 */
export async function fetchSatelliteNDVI(lat = 23.47, lon = 88.55) {
  try {
    const { data } = await api.get('/api/telemetry/satellite', {
      params: { lat, lon }
    })
    return data
  } catch (err) {
    console.warn('Satellite fetch fallback:', err)
    return null
  }
}

export const simulateOutbreak = simulateOutbreakEvent

export function resolveMediaUrl(path) {
  if (!path) return ''
  if (/^https?:\/\//i.test(path)) return path
  let cleanPath = path
  if (!cleanPath.startsWith('/')) {
    cleanPath = `/audio/${cleanPath}`
  }
  return `${API_BASE_URL}${cleanPath}`
}

// ============================================================================
// Legacy compatibility functions
// ============================================================================

export async function predictCampaign(payload) {
  try {
    const { data } = await api.post('/api/predict', payload)
    return data
  } catch (err) {
    throw new Error(describeError(err, 'Prediction failed'))
  }
}

export async function fetchSegmentStats() {
  try {
    const { data } = await api.get('/api/segments/stats')
    return Array.isArray(data) ? data : []
  } catch (err) {
    throw new Error(describeError(err, 'Failed to load segment stats'))
  }
}

export async function fetchCampaignHistory(limit = 20, grower_id = null) {
  try {
    const params = { limit }
    if (grower_id) params.grower_id = grower_id
    const { data } = await api.get('/api/campaigns/history', { params })
    return Array.isArray(data) ? data : []
  } catch (err) {
    throw new Error(describeError(err, 'Failed to load campaign history'))
  }
}

export async function upsertFarmer(profile) {
  try {
    const { data } = await api.post('/api/farmers', profile)
    return data
  } catch (err) {
    throw new Error(describeError(err, 'Failed to register farmer profile'))
  }
}

export async function fetchFarmerProfile(growerId) {
  try {
    const { data } = await api.get(`/api/farmers/${growerId}`)
    return data
  } catch (err) {
    return null
  }
}

export async function fetchCampaignMetrics() {
  try {
    const { data } = await api.get('/api/campaigns/metrics')
    return data
  } catch (err) {
    return {}
  }
}

export async function recordCampaignClick(campaignId, clicked = true) {
  try {
    const { data } = await api.patch(`/api/campaigns/${campaignId}/clicked`, null, {
      params: { clicked }
    })
    return data
  } catch (err) {
    return null
  }
}
