import { ref, computed } from 'vue'

// Demo credentials — no backend auth, pure client-side for hackathon demo
const DEMO_USERS = {
  farmer: { username: 'farmer', password: 'farmer123', role: 'farmer', displayName: 'Subhash Mondal' },
  admin: { username: 'admin', password: 'admin123', role: 'admin', displayName: 'Dr. Ananya Roy (BAO)' }
}

const currentUser = ref(JSON.parse(localStorage.getItem('krishisetu_user') || 'null'))

export function useAuth() {
  const isLoggedIn = computed(() => !!currentUser.value)
  const isAdmin = computed(() => currentUser.value?.role === 'admin')
  const isFarmer = computed(() => currentUser.value?.role === 'farmer')
  const displayName = computed(() => currentUser.value?.displayName || '')
  const userRole = computed(() => currentUser.value?.role || '')

  function login(username, password) {
    const trimUser = username.trim().toLowerCase()
    const match = Object.values(DEMO_USERS).find(
      u => u.username === trimUser && u.password === password
    )
    if (!match) {
      return { success: false, error: 'Invalid credentials. Try farmer/farmer123 or admin/admin123.' }
    }
    const userData = { username: match.username, role: match.role, displayName: match.displayName }
    currentUser.value = userData
    localStorage.setItem('krishisetu_user', JSON.stringify(userData))
    return { success: true, user: userData }
  }

  function logout() {
    currentUser.value = null
    localStorage.removeItem('krishisetu_user')
  }

  return {
    currentUser,
    isLoggedIn,
    isAdmin,
    isFarmer,
    displayName,
    userRole,
    login,
    logout
  }
}
