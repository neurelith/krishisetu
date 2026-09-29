import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DevTool from '../views/DevTool.vue'
import Admin from '../views/Admin.vue'
import Onboarding from '../views/Onboarding.vue'
import Inbox from '../views/Inbox.vue'
import Selfie from '../views/Selfie.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'kisan-sathi',
      component: Home
    },
    {
      path: '/home',
      redirect: '/'
    },
    {
      path: '/interop',
      name: 'kisan-setu',
      component: DevTool
    },
    {
      path: '/dev-tool',
      redirect: '/interop'
    },
    {
      path: '/command',
      name: 'kisan-rakshak',
      component: Admin
    },
    {
      path: '/admin',
      redirect: '/command'
    },
    {
      path: '/onboarding',
      redirect: '/'
    },
    {
      path: '/inbox',
      redirect: '/'
    },
    {
      path: '/selfie',
      redirect: '/'
    }
  ]
})

export default router
