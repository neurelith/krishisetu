<template>
  <div class="app-shell">
    <header class="site-nav" :class="{ 'site-nav-hero': isLanding }">
      <div class="nav-inner">
        <router-link to="/" class="brand-link" aria-label="KrishiSetu home">
          <span class="brand-mark"><PhPlant :size="20" weight="bold" /></span>
          <span class="brand-copy">
            <strong>KrishiSetu</strong>
            <span>field intelligence</span>
          </span>
        </router-link>

        <nav v-if="isLoggedIn" class="nav-cluster" aria-label="Workspace navigation">
          <router-link v-if="isFarmer" to="/sathi" class="nav-pill">
            <PhPlant :size="17" weight="bold" />
            <span>Check a leaf</span>
          </router-link>
          <template v-else>
            <router-link to="/command" class="nav-pill">
              <PhBroadcast :size="17" weight="bold" />
              <span>Outbreak watch</span>
            </router-link>
            <router-link to="/interop" class="nav-pill">
              <PhArrowsLeftRight :size="17" weight="bold" />
              <span>Registry converter</span>
            </router-link>
          </template>
        </nav>

        <div class="nav-right">
          <router-link v-if="!isLoggedIn" to="/" class="nav-sign-in">Sign in</router-link>
          <button v-else type="button" class="status-chip" :class="{ 'chip-off': !isOnline }" @click="toggleOfflineSimulation">
            <span class="status-dot" :class="{ 'dot-off': !isOnline }"></span>
            <span>{{ isOnline ? 'Online' : 'Offline' }}</span>
          </button>
          <div v-if="isLoggedIn" class="user-cluster">
            <div class="user-avatar"><PhUserCircle :size="19" weight="regular" /></div>
            <div class="user-info">
              <strong>{{ displayName }}</strong>
              <span>{{ isAdmin ? 'Extension officer' : 'Farmer' }}</span>
            </div>
            <button type="button" class="sign-out-btn" aria-label="Sign out" title="Sign out" @click="handleLogout">
              <PhSignOut :size="18" weight="bold" />
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="main-outlet"><router-view /></main>

    <footer class="app-footer">
      <div class="footer-inner">
        <div class="footer-brand"><span class="footer-dot"></span><strong>KrishiSetu</strong><span>Digital public good for field decisions</span></div>
        <div class="footer-links">
          <button type="button" @click="modal = 'tos'">Terms</button>
          <button type="button" @click="modal = 'privacy'">Privacy</button>
          <button type="button" @click="modal = 'standards'">Schema</button>
        </div>
      </div>
    </footer>

    <div v-if="modal" class="modal-overlay" @click="modal = null">
      <section class="modal-panel" role="dialog" aria-modal="true" @click.stop>
        <div class="modal-head">
          <div><span class="modal-kicker">KrishiSetu reference</span><h2>{{ modalTitle }}</h2></div>
          <button type="button" class="modal-close" aria-label="Close" @click="modal = null"><PhX :size="20" weight="bold" /></button>
        </div>
        <div class="modal-content">
          <template v-if="modal === 'tos'">
            <h3>Open Digital Public Good Framework</h3>
            <p>KrishiSetu provides assistive agronomic decision support and an open FarmContext data contract. Verify interventions with a local Block Agricultural Officer or Krishi Vigyan Kendra scientist.</p>
            <h3>Cross-state interoperability</h3>
            <p>Participating state registries retain ownership of their records. Normalization keeps the source dialect visible while producing one common contract.</p>
          </template>
          <template v-else-if="modal === 'privacy'">
            <h3>Data minimization</h3>
            <p>Farmer records and offline advisories stay on the device for this demo. Images are sent only when a diagnosis is requested and are not used for advertising.</p>
            <h3>Your control</h3>
            <p>Sign out to remove the active demo session. Clear local site data to remove saved field reports and cached advice.</p>
          </template>
          <template v-else>
            <h3>in.gov.dpg.farmcontext.v1</h3>
            <p>The shared contract connects farmer identity, location, crop, soil, weather and satellite observations across state registries.</p>
            <pre class="schema-block"><code>{
  "farmer": { "name": "string", "preferred_language": "bn | hi | en" },
  "location": { "state": "string", "district": "string" },
  "crop": { "name": "string", "variety": "string" },
  "satellite": { "ndvi": "number | null" }
}</code></pre>
          </template>
        </div>
        <div class="modal-foot"><button type="button" class="btn-gov-primary" @click="modal = null">Close reference</button></div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PhPlant, PhArrowsLeftRight, PhBroadcast, PhX, PhUserCircle, PhSignOut } from '@phosphor-icons/vue'
import { useOfflineStorage } from './composables/useOfflineStorage'
import { useAuth } from './composables/useAuth'

const route = useRoute()
const router = useRouter()
const { isOnline, isOfflineSimulation, setOfflineSimulation } = useOfflineStorage()
const { isLoggedIn, isAdmin, isFarmer, displayName, logout } = useAuth()
const modal = ref(null)
const isLanding = computed(() => route.name === 'story' || route.path === '/')
const modalTitle = computed(() => ({ tos: 'Terms of use', privacy: 'Privacy note', standards: 'FarmContext schema' }[modal.value] || 'Reference'))

function toggleOfflineSimulation() {
  setOfflineSimulation(!isOfflineSimulation.value)
}

function handleLogout() {
  logout()
  router.push('/')
}
</script>

<style scoped>
.app-shell { min-height: 100vh; min-height: 100dvh; display: flex; flex-direction: column; background: var(--color-cloud-white); }
.site-nav { position: sticky; top: 0; z-index: 20; background: var(--color-canopy); border-bottom: 1px solid var(--color-canopy-hover); }
.site-nav-hero { position: absolute; top: 0; left: 0; right: 0; background: transparent; border-bottom-color: var(--color-haze); }
.nav-inner { width: min(100% - 48px, 1240px); min-height: 74px; margin: 0 auto; display: flex; align-items: center; gap: 28px; }
.brand-link { display: inline-flex; align-items: center; gap: 10px; color: var(--color-cloud-white); text-decoration: none; flex-shrink: 0; }
.brand-mark { width: 38px; height: 38px; display: grid; place-items: center; border: 1px solid var(--color-haze); border-radius: 13px; color: var(--color-cloud-white); }
.brand-copy { display: grid; gap: 1px; }
.brand-copy strong { font-family: var(--font-display); font-size: 25px; font-weight: 500; line-height: 1; }
.brand-copy span { color: var(--color-haze); font-size: var(--text-caption); letter-spacing: 0.05em; text-transform: uppercase; }
.nav-cluster { display: flex; align-items: center; gap: 6px; margin-right: auto; }
.nav-pill, .nav-sign-in { min-height: 44px; display: inline-flex; align-items: center; gap: 8px; padding: 0 14px; border: 1px solid transparent; border-radius: var(--radius-buttons); color: var(--color-cloud-white); text-decoration: none; font-size: var(--text-body-sm); font-weight: 500; }
.nav-pill:hover, .nav-pill.router-link-exact-active { border-color: var(--color-haze); background: var(--color-deep-monsoon); }
.nav-right { display: flex; align-items: center; gap: 14px; margin-left: auto; }
.nav-sign-in { border-color: var(--color-haze); }
.status-chip { min-height: 36px; display: inline-flex; align-items: center; gap: 8px; padding: 0 12px; border: 1px solid var(--color-haze); border-radius: var(--radius-buttons); color: var(--color-cloud-white); background: transparent; font: inherit; cursor: pointer; }
.status-chip:hover { background: var(--color-deep-monsoon); }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--color-leaf); }
.status-dot.dot-off { background: var(--color-chilli); }
.user-cluster { display: flex; align-items: center; gap: 9px; color: var(--color-cloud-white); }
.user-avatar { width: 34px; height: 34px; display: grid; place-items: center; border: 1px solid var(--color-haze); border-radius: 50%; }
.user-info { display: grid; gap: 1px; min-width: 0; }
.user-info strong { max-width: 170px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: var(--text-caption); }
.user-info span { color: var(--color-haze); font-size: var(--text-caption); }
.sign-out-btn { width: 38px; height: 38px; display: grid; place-items: center; border: 1px solid transparent; border-radius: 50%; color: var(--color-haze); background: transparent; cursor: pointer; }
.sign-out-btn:hover { border-color: var(--color-haze); color: var(--color-cloud-white); }
.main-outlet { flex: 1; display: flex; flex-direction: column; }
.app-footer { padding: 28px 24px; border-top: 1px solid var(--color-fog); color: var(--color-stone); background: var(--color-cloud-white); }
.footer-inner { width: min(100%, var(--page-max-width)); margin: 0 auto; display: flex; justify-content: space-between; gap: 20px; flex-wrap: wrap; }
.footer-brand, .footer-links { display: flex; align-items: center; gap: 10px; font-size: var(--text-caption); }
.footer-brand strong { color: var(--color-ink); }
.footer-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--color-chilli); }
.footer-links button { padding: 4px 0; border: 0; color: var(--color-deep-monsoon); background: transparent; font: inherit; cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
.modal-overlay { position: fixed; inset: 0; z-index: 50; display: grid; place-items: center; padding: 24px; background: var(--color-night-soil); }
.modal-panel { width: min(100%, 620px); max-height: 86vh; display: flex; flex-direction: column; overflow: hidden; border-radius: var(--radius-modals); background: var(--color-cloud-white); box-shadow: var(--shadow-lift); }
.modal-head, .modal-foot { padding: 20px 24px; display: flex; align-items: center; justify-content: space-between; gap: 16px; border-bottom: 1px solid var(--color-fog); }
.modal-foot { justify-content: flex-end; border-top: 1px solid var(--color-fog); border-bottom: 0; }
.modal-kicker { color: var(--color-chilli); font-size: var(--text-caption); font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
.modal-head h2 { margin-top: 4px; font-size: var(--text-subheading); }
.modal-close { width: 42px; height: 42px; display: grid; place-items: center; border: 1px solid var(--color-fog); border-radius: 50%; color: var(--color-graphite); background: var(--color-cloud-white); cursor: pointer; }
.modal-content { padding: 24px; overflow-y: auto; }
.modal-content h3 { margin: 0 0 8px; color: var(--color-ink); }
.modal-content h3:not(:first-child) { margin-top: 24px; }
.modal-content p { color: var(--color-graphite); }
.schema-block { margin: 16px 0 0; padding: 16px; overflow: auto; border-radius: var(--radius-inputs); background: var(--inkwell); color: var(--inkwell-text); font-size: var(--text-caption); line-height: 1.6; }
@media (max-width: 900px) { .nav-inner { width: min(100% - 32px, 1240px); gap: 14px; } .nav-cluster { order: 3; width: 100%; overflow-x: auto; } .site-nav:not(.site-nav-hero) .nav-inner { flex-wrap: wrap; padding: 10px 0; } }
@media (max-width: 560px) { .brand-copy span, .user-info { display: none; } .nav-right { margin-left: auto; } .nav-inner { min-height: 68px; } .site-nav:not(.site-nav-hero) .nav-inner { padding-bottom: 8px; } .nav-pill { white-space: nowrap; } }
</style>
