/**
 * IndexedDB Offline Storage Composable for KrishiSetu (कृषि-সেতু).
 * Ensures smallholders can access diagnostics, regenerative advisories,
 * and audio guidance even during total rural connectivity blackouts.
 */

import { ref } from 'vue'

const DB_NAME = 'KrishiSetuOfflineDB'
const DB_VERSION = 1
const STORE_NAME = 'offline_store'

let dbInstance = null

// Module-singleton state: every component calling useOfflineStorage() shares the
// same isOnline/isOfflineSimulation refs, so the nav toggle drives every banner.
const isOnlineGlobal = ref(typeof navigator !== 'undefined' ? navigator.onLine : true)
const isOfflineSimulationGlobal = ref(false)
const lastSyncTimeGlobal = ref(null)

function openDatabase() {
  return new Promise((resolve, reject) => {
    if (dbInstance) return resolve(dbInstance)
    if (typeof window === 'undefined' || !window.indexedDB) {
      return reject(new Error('IndexedDB not supported in this environment.'))
    }

    const request = indexedDB.open(DB_NAME, DB_VERSION)

    request.onupgradeneeded = (event) => {
      const db = event.target.result
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: 'key' })
      }
    }

    request.onsuccess = (event) => {
      dbInstance = event.target.result
      resolve(dbInstance)
    }

    request.onerror = (event) => {
      reject(event.target.error)
    }
  })
}

export function useOfflineStorage() {
  // Singleton refs (module scope) — every consumer shares one truth.
  const isOnline = isOnlineGlobal
  const isOfflineSimulation = isOfflineSimulationGlobal
  const lastSyncTime = lastSyncTimeGlobal

  const updateOnlineStatus = () => {
    isOnline.value = navigator.onLine && !isOfflineSimulation.value
  }

  // Window listeners are registered once at module level; per-component
  // onMounted/onUnmounted registration would create duplicate closures.
  if (typeof window !== 'undefined' && !window.__krishisetu_online_listeners) {
    window.__krishisetu_online_listeners = true
    window.addEventListener('online', updateOnlineStatus)
    window.addEventListener('offline', updateOnlineStatus)
    updateOnlineStatus()
  }

  const setOfflineSimulation = (val) => {
    isOfflineSimulation.value = val
    updateOnlineStatus()
  }

  const saveOfflineItem = async (key, value) => {
    try {
      const db = await openDatabase()
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite')
        const store = tx.objectStore(STORE_NAME)
        const request = store.put({
          key,
          value,
          updated_at: new Date().toISOString()
        })
        request.onsuccess = () => {
          lastSyncTime.value = new Date().toLocaleTimeString()
          resolve(true)
        }
        request.onerror = (e) => reject(e.target.error)
      })
    } catch (err) {
      console.warn('Failed to save to IndexedDB:', err)
      // LocalStorage fallback
      try {
        localStorage.setItem(`krishisetu_${key}`, JSON.stringify(value))
      } catch (e) {}
    }
  }

  const getOfflineItem = async (key) => {
    try {
      const db = await openDatabase()
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readonly')
        const store = tx.objectStore(STORE_NAME)
        const request = store.get(key)
        request.onsuccess = () => {
          resolve(request.result ? request.result.value : null)
        }
        request.onerror = (e) => reject(e.target.error)
      })
    } catch (err) {
      console.warn('Failed to read from IndexedDB, trying localStorage:', err)
      try {
        const item = localStorage.getItem(`krishisetu_${key}`)
        return item ? JSON.parse(item) : null
      } catch (e) {
        return null
      }
    }
  }

  return {
    isOnline,
    isOfflineSimulation,
    setOfflineSimulation,
    lastSyncTime,
    saveOfflineItem,
    getOfflineItem
  }
}
