import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DevTool from '../views/DevTool.vue'
import Admin from '../views/Admin.vue'

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
    }
  ]
})

export default router
