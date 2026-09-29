import { ref } from 'vue'
import { upsertFarmer, fetchFarmerProfile, API_BASE_URL } from '../api'

const channel = new BroadcastChannel('krishisetu-realtime-channel')

const activeFarmerName = ref(localStorage.getItem('farmer_name') || 'Ram Singh')
const activeFarmerLanguage = ref(localStorage.getItem('farmer_language') || 'Hindi')
const activeFarmerCrop = ref(localStorage.getItem('farmer_crop') || 'Wheat')
const activeFarmerLocation = ref(localStorage.getItem('farmer_location') || 'Uttar Pradesh · Agra')
const activeFarmerSize = ref(localStorage.getItem('farmer_size') || '2–5 acres')
const activeFarmerGrowerId = ref(localStorage.getItem('farmer_grower_id') || 'GRW_CURRENT_DEMO')

// WebSocket state and configuration
let ws = null
let reconnectDelay = 1000
const maxReconnectDelay = 16000
let isConnecting = false

const mapStringToSize = (str) => {
  if (!str) return 3.5
  if (typeof str === 'number') return str
  const clean = str.toLowerCase()
  if (clean.includes('under 2')) return 1.5
  if (clean.includes('2–5') || clean.includes('2-5')) return 3.5
  if (clean.includes('5–10') || clean.includes('5-10')) return 7.5
  if (clean.includes('10+')) return 12.0
  const parsed = parseFloat(str)
  return isNaN(parsed) ? 3.5 : parsed
}

const mapSizeToString = (size) => {
  if (size === undefined || size === null) return '2–5 acres'
  const val = parseFloat(size)
  if (isNaN(val)) return size
  if (val < 2) return 'Under 2 acres'
  if (val <= 5) return '2–5 acres'
  if (val <= 10) return '5–10 acres'
  return '10+ acres'
}

const mapCropToEmoji = (crop) => {
  if (!crop) return 'Wheat'
  const cleanCrop = crop.replace(/[^a-zA-Z\s]/g, '').trim().toLowerCase()
  if (cleanCrop === 'wheat') return 'Wheat'
  if (cleanCrop === 'maize') return 'Maize'
  if (cleanCrop === 'mustard') return 'Mustard'
  if (cleanCrop === 'potato') return 'Potato'
  return crop
}

// Event listener pools (shared across instances)
const campaignListeners = new Set()
const farmerUpdateListeners = new Set()
const interactionListeners = new Set()

// Utility to dispatch local callbacks
const triggerCallbacks = (type, data) => {
  if (type === 'campaign-generated') {
    campaignListeners.forEach(cb => cb(data))
  } else if (type === 'active-farmer-updated' || type === 'farmer-updated') {
    reloadActiveFarmer()
    farmerUpdateListeners.forEach(cb => cb(data))
  } else if (type === 'farmer-interaction') {
    interactionListeners.forEach(cb => cb(data))
  }
}

// Broadcast channel fallback listener
channel.addEventListener('message', (event) => {
  // If WebSocket is open and active, we ignore BroadcastChannel to avoid double triggers
  if (ws && ws.readyState === WebSocket.OPEN) return
  const { type, data } = event.data || {}
  triggerCallbacks(type, data)
})

function connectWebSocket() {
  if (ws || isConnecting) return
  isConnecting = true

  console.log('Connecting to Realtime WebSocket server...')
  const wsUrl = `${API_BASE_URL.replace(/^http/, 'ws')}/api/ws`
  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('WebSocket connection established.')
    isConnecting = false
    reconnectDelay = 1000
  }

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      const { type, data } = msg
      console.log('Received WebSocket message:', type, data)
      
      // Update local storage if active farmer is updated from another client
      if (type === 'active-farmer-updated' || type === 'farmer-updated') {
        if (data && data.grower_id) {
          if (data.name !== undefined) localStorage.setItem('farmer_name', data.name || 'Kisan')
          if (data.language !== undefined) localStorage.setItem('farmer_language', data.language)
          
          const cropVal = data.crop !== undefined ? data.crop : (data.main_crop !== undefined ? data.main_crop : data.campaign_crop)
          if (cropVal !== undefined) {
            localStorage.setItem('farmer_crop', mapCropToEmoji(cropVal))
          }
          
          if (data.state && data.district) {
            localStorage.setItem('farmer_location', `${data.state} · ${data.district}`)
          } else if (data.location) {
            localStorage.setItem('farmer_location', data.location)
          }
          
          const sizeVal = data.farm_size !== undefined ? data.farm_size : (data.grower_farm_size !== undefined ? data.grower_farm_size : data.size)
          if (sizeVal !== undefined) {
            localStorage.setItem('farmer_size', mapSizeToString(sizeVal))
          }
          
          if (data.grower_id !== undefined) localStorage.setItem('farmer_grower_id', data.grower_id)
        }
      }
      
      // Trigger callbacks reactively
      triggerCallbacks(type, data)
    } catch (err) {
      console.error('Error parsing WebSocket message:', err)
    }
  }

  ws.onerror = (err) => {
    console.warn('WebSocket error:', err)
    ws.close()
  }

  ws.onclose = () => {
    console.log('WebSocket connection closed. Reconnecting...')
    ws = null
    isConnecting = false
    setTimeout(() => {
      reconnectDelay = Math.min(reconnectDelay * 2, maxReconnectDelay)
      connectWebSocket()
    }, reconnectDelay)
  }
}

// Initialize WebSocket connection on load
if (typeof window !== 'undefined') {
  connectWebSocket()
}

const reloadActiveFarmer = () => {
  activeFarmerName.value = localStorage.getItem('farmer_name') || 'Ram Singh'
  activeFarmerLanguage.value = localStorage.getItem('farmer_language') || 'Hindi'
  activeFarmerCrop.value = localStorage.getItem('farmer_crop') || '🌾 Wheat'
  activeFarmerLocation.value = localStorage.getItem('farmer_location') || 'Uttar Pradesh · Agra'
  activeFarmerSize.value = localStorage.getItem('farmer_size') || '2–5 acres'
  activeFarmerGrowerId.value = localStorage.getItem('farmer_grower_id') || 'GRW_CURRENT_DEMO'
}

export function useRealtimeSync() {
  const localListeners = []

  const onCampaignReceived = (callback) => {
    campaignListeners.add(callback)
    localListeners.push({ set: campaignListeners, cb: callback })
    return () => {
      campaignListeners.delete(callback)
    }
  }

  const onFarmerUpdated = (callback) => {
    farmerUpdateListeners.add(callback)
    localListeners.push({ set: farmerUpdateListeners, cb: callback })
    return () => {
      farmerUpdateListeners.delete(callback)
    }
  }

  const onInteractionReceived = (callback) => {
    interactionListeners.add(callback)
    localListeners.push({ set: interactionListeners, cb: callback })
    return () => {
      interactionListeners.delete(callback)
    }
  }

  const updateActiveFarmer = async (profile) => {
    let mergedProfile = { ...profile }
    let shouldUpsert = profile.name !== undefined || profile.crop !== undefined || profile.location !== undefined || profile.size !== undefined

    // If grower_id is specified but other fields are missing, fetch from database to populate
    if (profile.grower_id && (!profile.name || !profile.crop || !profile.location || !profile.size)) {
      try {
        const dbProfile = await fetchFarmerProfile(profile.grower_id)
        if (dbProfile) {
          mergedProfile = {
            grower_id: dbProfile.grower_id,
            name: dbProfile.name || profile.name || 'Ram Singh',
            language: dbProfile.language || profile.language || 'Hindi',
            crop: dbProfile.crop ? mapCropToEmoji(dbProfile.crop) : (profile.crop || '🌾 Wheat'),
            location: dbProfile.state && dbProfile.district 
              ? `${dbProfile.state} · ${dbProfile.district}` 
              : (profile.location || 'Uttar Pradesh · Agra'),
            size: dbProfile.farm_size !== undefined 
              ? mapSizeToString(dbProfile.farm_size) 
              : (profile.size || '2–5 acres')
          }
        }
      } catch (err) {
        console.warn('Failed to fetch full farmer profile from database, using defaults:', err)
      }
    }

    if (mergedProfile.name !== undefined) localStorage.setItem('farmer_name', mergedProfile.name)
    if (mergedProfile.language !== undefined) localStorage.setItem('farmer_language', mergedProfile.language)
    if (mergedProfile.crop !== undefined) localStorage.setItem('farmer_crop', mergedProfile.crop)
    if (mergedProfile.location !== undefined) localStorage.setItem('farmer_location', mergedProfile.location)
    if (mergedProfile.size !== undefined) localStorage.setItem('farmer_size', mergedProfile.size)
    if (mergedProfile.grower_id !== undefined) localStorage.setItem('farmer_grower_id', mergedProfile.grower_id)
    
    reloadActiveFarmer()
    
    if (shouldUpsert) {
      // Map to backend properties & upsert
      let cropVal = mergedProfile.crop
      let mainCrop = cropVal ? cropVal.replace(/[^a-zA-Z\s]/g, '').trim() : undefined

      let stateVal = undefined
      let districtVal = undefined
      if (mergedProfile.location) {
        const parts = mergedProfile.location.split('·')
        stateVal = parts[0] ? parts[0].trim() : undefined
        districtVal = parts[1] ? parts[1].trim() : undefined
      }

      let farmSizeVal = mergedProfile.size ? mapStringToSize(mergedProfile.size) : undefined

      const backendProfile = {
        grower_id: mergedProfile.grower_id,
        name: mergedProfile.name,
        state: stateVal,
        district: districtVal,
        language: mergedProfile.language,
        grower_farm_size: farmSizeVal,
        main_crop: mainCrop
      }

      try {
        await upsertFarmer(backendProfile)
      } catch (err) {
        console.error('Failed to upsert active farmer to database:', err)
      }
    }
    
    const msg = { type: 'active-farmer-updated', data: mergedProfile }
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(msg))
    }
    channel.postMessage(msg)
  }

  const broadcastCampaign = (campaign) => {
    const msg = { type: 'campaign-generated', data: campaign }
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(msg))
    }
    channel.postMessage(msg)
  }

  const broadcastInteraction = (interaction) => {
    const msg = { type: 'farmer-interaction', data: interaction }
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(msg))
    }
    channel.postMessage(msg)
  }

  const destroy = () => {
    localListeners.forEach(({ set, cb }) => {
      set.delete(cb)
    })
  }

  return {
    activeFarmerName,
    activeFarmerLanguage,
    activeFarmerCrop,
    activeFarmerLocation,
    activeFarmerSize,
    activeFarmerGrowerId,
    broadcastCampaign,
    broadcastInteraction,
    onCampaignReceived,
    onFarmerUpdated,
    onInteractionReceived,
    updateActiveFarmer,
    reloadActiveFarmer,
    destroy
  }
}
