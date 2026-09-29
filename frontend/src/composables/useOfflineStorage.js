/**
 * IndexedDB Offline Storage Composable for KrishiSetu (कृषि-সেতু).
 * Ensures smallholders can access diagnostics, regenerative advisories,
 * and audio guidance even during total rural connectivity blackouts.
 */

import { ref, onMounted, onUnmounted } from 'vue'

const DB_NAME = 'KrishiSetuOfflineDB'
const DB_VERSION = 1
const STORE_NAME = 'offline_store'

let dbInstance = null

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
  const isOnline = ref(typeof navigator !== 'undefined' ? navigator.onLine : true)
  const isOfflineSimulation = ref(false)
  const lastSyncTime = ref(null)

  const updateOnlineStatus = () => {
    isOnline.value = navigator.onLine && !isOfflineSimulation.value
  }

  onMounted(() => {
    if (typeof window !== 'undefined') {
      window.addEventListener('online', updateOnlineStatus)
      window.addEventListener('offline', updateOnlineStatus)
      updateOnlineStatus()
    }
  })

  onUnmounted(() => {
    if (typeof window !== 'undefined') {
      window.removeEventListener('online', updateOnlineStatus)
      window.removeEventListener('offline', updateOnlineStatus)
    }
  })

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
