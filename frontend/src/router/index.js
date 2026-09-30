import { createRouter, createWebHistory } from 'vue-router'
import Story from '../views/Story.vue'
import Home from '../views/Home.vue'
import DevTool from '../views/DevTool.vue'
import Admin from '../views/Admin.vue'
import { useAuth } from '../composables/useAuth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'story',
      component: Story
    },
    {
      path: '/sathi',
      name: 'kisan-sathi',
      component: Home,
      meta: { requiresAuth: true, roles: ['farmer'] }
    },
    {
      path: '/home',
      redirect: '/sathi'
    },
    {
      path: '/interop',
      name: 'kisan-setu',
      component: DevTool,
      meta: { requiresAuth: true, roles: ['admin'] }
    },
    {
      path: '/dev-tool',
      redirect: '/interop'
    },
    {
      path: '/command',
      name: 'kisan-rakshak',
      component: Admin,
      meta: { requiresAuth: true, roles: ['admin'] }
    },
    {
      path: '/admin',
      redirect: '/command'
    }
  ]
})

router.beforeEach((to, from, next) => {
  const { isLoggedIn, userRole } = useAuth()

  if (to.meta.requiresAuth) {
    if (!isLoggedIn.value) {
      return next({ path: '/', query: { redirect: to.fullPath, reason: 'login_required' } })
    }
    if (to.meta.roles && !to.meta.roles.includes(userRole.value)) {
      if (userRole.value === 'farmer') {
        return next({ path: '/sathi', query: { restricted: 'admin_only' } })
      }
      if (userRole.value === 'admin') {
        return next({ path: '/command', query: { restricted: 'farmer_only' } })
      }
      return next({ path: '/' })
    }
  }
  next()
})

export default router

