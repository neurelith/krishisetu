<template>
  <div class="story-page">
    <section class="story-hero sky sky-hero" data-risk="clear">
      <div class="hero-layout">
        <div class="hero-copy">
          <div class="hero-kicker"><span class="kicker-line"></span><span>Open field intelligence</span></div>
          <h1 class="display">From one leaf,<br /><em>to every field.</em></h1>
          <p class="hero-lede">KrishiSetu helps farmers act early, while giving extension officers a clear view of disease moving across districts.</p>
          <div class="hero-proof-row">
            <span><PhTranslate :size="18" weight="bold" /> Bengali, Hindi and English</span>
            <span><PhMicrophone :size="18" weight="bold" /> Voice-ready</span>
          </div>
          <div class="hero-stats" aria-label="KrishiSetu capabilities">
            <div><strong>48h</strong><span>border warning lead</span></div>
            <div><strong>10m</strong><span>satellite field detail</span></div>
            <div><strong>1</strong><span>common farm contract</span></div>
          </div>
        </div>

        <div class="hero-side">
          <div v-if="!isLoggedIn" class="auth-card">
            <div class="auth-topline"><span class="auth-icon"><PhPlant :size="22" weight="bold" /></span><span>Private field workspace</span></div>
            <h2>Start with your role</h2>
            <p class="auth-intro">Sign in to see only the tools made for your work.</p>
            <form class="auth-form" @submit.prevent="handleLogin">
              <label for="uid">Username</label>
              <div class="input-wrap"><PhUser :size="18" /><input id="uid" v-model="uid" type="text" placeholder="farmer or admin" autocomplete="username" required /></div>
              <label for="pwd">Password</label>
              <div class="input-wrap"><PhLock :size="18" /><input id="pwd" v-model="pwd" :type="showPwd ? 'text' : 'password'" placeholder="Enter password" autocomplete="current-password" required /><button type="button" class="password-toggle" :aria-label="showPwd ? 'Hide password' : 'Show password'" @click="showPwd = !showPwd"><PhEyeSlash v-if="showPwd" :size="18" /><PhEye v-else :size="18" /></button></div>
              <p v-if="errMsg" class="auth-error" role="alert">{{ errMsg }}</p>
              <button type="submit" class="btn-gov-primary btn-xl auth-submit" :disabled="busy"><PhCircleNotch v-if="busy" class="spin" :size="19" weight="bold" /><span>{{ busy ? 'Opening workspace' : 'Sign in securely' }}</span><PhArrowRight v-if="!busy" :size="18" weight="bold" /></button>
            </form>
            <div class="demo-access">
              <span>Demo access</span>
              <button type="button" @click="fill('farmer')"><PhPlant :size="16" weight="bold" /> Farmer</button>
              <button type="button" @click="fill('admin')"><PhShieldCheck :size="16" weight="bold" /> Officer</button>
            </div>
          </div>

          <div v-else class="welcome-card">
            <div class="welcome-orbit"><PhUserCircle :size="40" weight="thin" /></div>
            <span class="welcome-kicker">Workspace ready</span>
            <h2>{{ displayName }}</h2>
            <p>{{ isAdmin ? 'Extension officer tools are ready.' : 'Your field check is ready.' }}</p>
            <router-link :to="isAdmin ? '/command' : '/sathi'" class="btn-gov-primary btn-xl"><span>{{ isAdmin ? 'Open outbreak watch' : 'Check a leaf' }}</span><PhArrowRight :size="18" weight="bold" /></router-link>
            <button type="button" class="text-action" @click="handleLogout"><PhSignOut :size="17" weight="bold" /> Sign out</button>
          </div>

          <div class="hero-visual" aria-hidden="true">
            <div class="visual-label"><span class="live-dot"></span> Live field signal</div>
            <div class="signal-ring ring-one"></div><div class="signal-ring ring-two"></div>
            <div class="signal-node"><PhPlant :size="30" weight="bold" /></div>
            <div class="signal-caption"><strong>Leaf &rarr; satellite &rarr; district</strong><span>One connected view of crop health</span></div>
          </div>
        </div>
      </div>
      <div class="hero-footer-line"><span>Built for bright fields, low bandwidth and local language decisions.</span><span>in.gov.dpg.farmcontext.v1</span></div>
    </section>

    <section class="workspace-preview quiet">
      <div class="section-intro"><span class="section-kicker">Two workspaces, one bridge</span><h2>Less noise. Faster decisions.</h2><p>Farmers get a simple path from observation to action. Officers get the signals needed to protect the next district.</p></div>
      <div class="feature-grid">
        <article v-for="feature in visibleFeatures" :key="feature.title" class="feature-tile" :class="feature.tone">
          <div class="feature-icon"><component :is="feature.icon" :size="23" weight="bold" /></div>
          <span class="feature-index">0{{ feature.index }}</span>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.desc }}</p>
          <router-link :to="feature.to" class="feature-link">{{ feature.cta }} <PhArrowUpRight :size="17" weight="bold" /></router-link>
        </article>
      </div>
    </section>

    <section class="ml-section quiet">
      <div class="ml-heading"><span class="section-kicker">The field loop</span><h2>How the machine learning works</h2><p>A clear chain of evidence, translated into a decision a farmer can use today.</p></div>
      <div class="ml-track">
        <article v-for="step in steps" :key="step.number" class="ml-step"><div class="step-number">{{ step.number }}</div><div class="step-icon"><component :is="step.icon" :size="22" weight="bold" /></div><h3>{{ step.title }}</h3><p>{{ step.copy }}</p></article>
      </div>
    </section>

    <section class="story-close sky" data-risk="storm"><div><span class="close-kicker">When the border matters</span><strong>48<span>h</span></strong><h2>Head start for the next district.</h2><p>Detect the signal here. Give the next field time to respond.</p></div><router-link :to="isAdmin ? '/command' : '/sathi'" class="btn-gov-primary btn-xl"><span>{{ isAdmin ? 'Open outbreak watch' : 'Check a leaf' }}</span><PhArrowRight :size="18" weight="bold" /></router-link></section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { PhPlant, PhUser, PhLock, PhEye, PhEyeSlash, PhCircleNotch, PhShieldCheck, PhUserCircle, PhArrowRight, PhArrowUpRight, PhSignOut, PhArrowsLeftRight, PhTranslate, PhMicrophone, PhCamera, PhCpu, PhBroadcast } from '@phosphor-icons/vue'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const { isLoggedIn, isAdmin, displayName, login, logout } = useAuth()
const uid = ref('')
const pwd = ref('')
const errMsg = ref('')
const showPwd = ref(false)
const busy = ref(false)

const features = [
  { index: 1, role: 'farmer', icon: PhPlant, tone: 'tone-leaf', title: 'Check a leaf', desc: 'Photograph a leaf or speak in your language. Get the disease and what to do today.', cta: 'Open field check', to: '/sathi' },
  { index: 2, role: 'admin', icon: PhBroadcast, tone: 'tone-alert', title: 'Watch outbreaks', desc: 'See disease cross district borders before it reaches the next field.', cta: 'Open outbreak watch', to: '/command' },
  { index: 3, role: 'admin', icon: PhArrowsLeftRight, tone: 'tone-sky', title: 'Convert registries', desc: 'Bring state farmer records into one standard FarmContext contract.', cta: 'Open registry converter', to: '/interop' }
]
const visibleFeatures = computed(() => !isLoggedIn.value ? features : features.filter(feature => feature.role === (isAdmin.value ? 'admin' : 'farmer')))
const steps = [
  { number: '01', icon: PhCamera, title: 'Capture', copy: 'A leaf photo or voice note becomes a structured field observation.' },
  { number: '02', icon: PhCpu, title: 'Match', copy: 'Vision signals meet crop context, soil, weather and satellite evidence.' },
  { number: '03', icon: PhBroadcast, title: 'Act', copy: 'The next step reaches the farmer, and a border signal reaches officers.' }
]

function fill(type) {
  uid.value = type
  pwd.value = type === 'farmer' ? 'farmer123' : 'admin123'
  errMsg.value = ''
}

async function handleLogin() {
  errMsg.value = ''
  busy.value = true
  await new Promise(resolve => setTimeout(resolve, 280))
  const result = login(uid.value, pwd.value)
  busy.value = false
  if (!result.success) {
    errMsg.value = result.error
    return
  }
  router.push(result.user.role === 'admin' ? '/command' : '/sathi')
}

function handleLogout() {
  logout()
  uid.value = ''
  pwd.value = ''
}
</script>

<style scoped>
.story-page { width: 100%; overflow: hidden; }
.story-hero { min-height: 780px; display: flex; flex-direction: column; justify-content: center; padding: 122px 32px 32px; }
.hero-layout { width: min(100%, 1180px); margin: 0 auto; display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(360px, 0.7fr); gap: clamp(48px, 8vw, 124px); align-items: center; }
.hero-copy { max-width: 690px; }
.hero-kicker, .section-kicker, .close-kicker, .welcome-kicker { display: inline-flex; align-items: center; gap: 9px; color: var(--color-haze); font-size: var(--text-caption); font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; }
.kicker-line { width: 26px; height: 1px; background: var(--color-haze); }
.hero-copy h1 { margin: 24px 0 22px; color: var(--color-cloud-white); font-size: clamp(58px, 8vw, 108px); letter-spacing: -0.045em; line-height: 0.92; }
.hero-copy h1 em { color: var(--color-haze); font-style: normal; }
.hero-lede { max-width: 50ch; color: var(--color-cloud-white); font-size: clamp(18px, 2vw, 22px); line-height: 1.55; }
.hero-proof-row { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 28px; color: var(--color-cloud-white); font-size: var(--text-body-sm); }
.hero-proof-row span { display: inline-flex; align-items: center; gap: 8px; }
.hero-stats { display: flex; flex-wrap: wrap; gap: 1px; margin-top: 56px; border-top: 1px solid var(--color-haze); border-bottom: 1px solid var(--color-haze); }
.hero-stats div { min-width: 140px; padding: 17px 22px 17px 0; display: grid; gap: 4px; }
.hero-stats strong { color: var(--color-cloud-white); font-family: var(--font-display); font-size: 34px; font-weight: 500; line-height: 1; }
.hero-stats span { color: var(--color-haze); font-size: var(--text-caption); }
.hero-side { position: relative; }
.auth-card, .welcome-card { position: relative; z-index: 2; padding: 28px; border: 1px solid var(--color-fog); border-radius: 20px; background: var(--color-cloud-white); box-shadow: var(--shadow-lift); color: var(--color-ink); }
.auth-topline { display: flex; align-items: center; gap: 10px; color: var(--color-stone); font-size: var(--text-caption); font-weight: 600; }
.auth-icon { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 12px; color: var(--color-cloud-white); background: var(--color-canopy); }
.auth-card h2, .welcome-card h2 { margin: 24px 0 6px; font-size: 30px; }
.auth-intro, .welcome-card p { color: var(--color-graphite); font-size: var(--text-body-sm); }
.auth-form { display: grid; gap: 8px; margin-top: 24px; }
.auth-form label { color: var(--color-graphite); font-size: var(--text-caption); font-weight: 600; }
.input-wrap { position: relative; display: flex; align-items: center; width: 100%; }
.input-wrap > svg { position: absolute; left: 14px; color: var(--color-stone); pointer-events: none; z-index: 2; }
.input-wrap input {
  width: 100%;
  height: 50px;
  min-height: 50px;
  box-sizing: border-box;
  padding: 12px 46px 12px 42px;
  font-size: var(--text-body);
  font-family: inherit;
  border: 1.5px solid var(--color-line-strong);
  border-radius: var(--radius-inputs);
  background: var(--color-cloud-white);
  color: var(--color-ink);
  transition: border-color var(--dur-fast), box-shadow var(--dur-fast);
}
.input-wrap input:focus {
  border-color: var(--color-deep-monsoon);
}
.password-toggle { position: absolute; right: 6px; width: 40px; height: 40px; display: grid; place-items: center; border: 0; border-radius: 50%; color: var(--color-stone); background: transparent; cursor: pointer; z-index: 2; }
.password-toggle:hover { color: var(--color-ink); background: var(--color-paddy-mist); }
.auth-submit { width: 100%; margin-top: 12px; }
.auth-error { padding: 10px 12px; border: 1px solid var(--brick-line); border-radius: var(--radius-inputs); color: var(--color-chilli); background: var(--brick-wash); font-size: var(--text-caption); }
.demo-access { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: 20px; padding-top: 16px; border-top: 1px solid var(--color-fog); color: var(--color-stone); font-size: var(--text-caption); }
.demo-access button { display: inline-flex; align-items: center; gap: 6px; min-height: 36px; padding: 0 10px; border: 1px solid var(--color-fog); border-radius: var(--radius-buttons); color: var(--color-deep-monsoon); background: var(--color-cloud-white); cursor: pointer; font: inherit; }
.demo-access button:hover { border-color: var(--color-deep-monsoon); background: var(--color-paddy-mist); }
.welcome-card { display: grid; justify-items: center; text-align: center; gap: 8px; }
.welcome-orbit { width: 74px; height: 74px; display: grid; place-items: center; border: 1px solid var(--color-deep-monsoon); border-radius: 50%; color: var(--color-deep-monsoon); }
.welcome-card h2 { margin-top: 8px; }
.welcome-card .btn-gov-primary { width: 100%; margin-top: 14px; }
.text-action { display: inline-flex; align-items: center; gap: 7px; border: 0; color: var(--color-deep-monsoon); background: transparent; cursor: pointer; font: inherit; font-size: var(--text-body-sm); }
.hero-visual { position: absolute; right: -48px; bottom: -102px; width: 260px; height: 260px; display: grid; place-items: center; border: 1px solid var(--color-haze); border-radius: 50%; color: var(--color-cloud-white); }
.visual-label { position: absolute; top: 20px; right: -8px; display: inline-flex; align-items: center; gap: 7px; padding: 7px 11px; border: 1px solid var(--color-haze); border-radius: var(--radius-buttons); color: var(--color-cloud-white); background: var(--color-storm); font-size: var(--text-caption); }
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--color-straw-fill); }
.signal-ring { position: absolute; border: 1px solid var(--color-haze); border-radius: 50%; }
.ring-one { inset: 28px; }.ring-two { inset: 64px; border-style: dashed; }
.signal-node { width: 76px; height: 76px; display: grid; place-items: center; border-radius: 24px; color: var(--color-canopy); background: var(--color-haze); }
.signal-caption { position: absolute; right: -26px; bottom: 6px; display: grid; gap: 3px; width: 180px; padding: 12px; border-left: 2px solid var(--color-chilli); color: var(--color-cloud-white); background: var(--color-storm); font-size: var(--text-caption); }
.signal-caption span { color: var(--color-haze); }
.hero-footer-line { width: min(100%, 1180px); margin: 100px auto 0; padding-top: 16px; display: flex; justify-content: space-between; gap: 16px; border-top: 1px solid var(--color-haze); color: var(--color-cloud-white); font-size: var(--text-caption); }
.workspace-preview, .ml-section { padding: 104px 32px; }
.section-intro, .ml-heading { width: min(100%, 720px); margin: 0 auto 48px; text-align: center; }
.section-intro h2, .ml-heading h2 { margin: 14px 0 10px; font-size: clamp(38px, 5vw, 64px); letter-spacing: -0.035em; }
.section-intro p, .ml-heading p { margin: 0 auto; color: var(--color-graphite); }
.section-kicker { color: var(--color-chilli); }
.feature-grid { width: min(100%, 1180px); margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.feature-tile { position: relative; min-height: 300px; padding: 28px; border-top: 3px solid var(--color-deep-monsoon); background: var(--color-paddy-mist); }
.feature-tile.tone-alert { border-top-color: var(--color-chilli); background: var(--brick-wash); }.feature-tile.tone-sky { border-top-color: var(--color-monsoon-sky); background: var(--sky-50); }
.feature-icon { width: 48px; height: 48px; display: grid; place-items: center; margin-bottom: 42px; border-radius: 15px; color: var(--color-cloud-white); background: var(--color-canopy); }.tone-alert .feature-icon { background: var(--color-chilli); }.tone-sky .feature-icon { background: var(--color-deep-monsoon); }
.feature-index { position: absolute; top: 28px; right: 28px; color: var(--color-stone); font-family: var(--font-mono); font-size: var(--text-caption); }
.feature-tile h3 { margin-bottom: 10px; font-family: var(--font-display); font-size: 30px; font-weight: 500; }.feature-tile p { min-height: 76px; color: var(--color-graphite); font-size: var(--text-body-sm); }.feature-link { display: inline-flex; align-items: center; gap: 8px; margin-top: 18px; color: var(--color-deep-monsoon); font-size: var(--text-body-sm); font-weight: 600; text-decoration: none; }.feature-link:hover { color: var(--color-chilli); }
.ml-section { background: var(--color-paddy-mist); }.ml-track { width: min(100%, 1180px); margin: 0 auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; border-top: 1px solid var(--color-fog); border-bottom: 1px solid var(--color-fog); }.ml-step { min-height: 260px; padding: 28px; border-right: 1px solid var(--color-fog); }.ml-step:last-child { border-right: 0; }.step-number { color: var(--color-chilli); font-family: var(--font-mono); font-size: var(--text-caption); }.step-icon { width: 46px; height: 46px; display: grid; place-items: center; margin: 28px 0 22px; border: 1px solid var(--color-deep-monsoon); border-radius: 50%; color: var(--color-deep-monsoon); }.ml-step h3 { margin-bottom: 10px; font-family: var(--font-display); font-size: 30px; font-weight: 500; }.ml-step p { color: var(--color-graphite); font-size: var(--text-body-sm); }
.story-close { padding: 92px 32px; display: flex; align-items: center; justify-content: space-between; gap: 32px; }.story-close > div { width: min(100%, 620px); }.close-kicker { color: var(--color-haze); }.story-close strong { display: block; margin: 12px 0 0; color: var(--color-cloud-white); font-family: var(--font-display); font-size: clamp(92px, 15vw, 180px); font-weight: 300; letter-spacing: -0.08em; line-height: 0.78; }.story-close strong span { margin-left: 8px; font-size: 0.42em; letter-spacing: 0; }.story-close h2 { margin: 22px 0 8px; color: var(--color-cloud-white); font-size: clamp(30px, 4vw, 48px); }.story-close p { color: var(--color-cloud-white); }.story-close .btn-gov-primary { background: var(--color-cloud-white); color: var(--color-canopy); }.story-close .btn-gov-primary:hover { background: var(--color-haze); }
@media (max-width: 860px) { .story-hero { min-height: auto; padding-top: 120px; }.hero-layout { grid-template-columns: 1fr; }.hero-side { max-width: 540px; width: 100%; margin: 0 auto; }.hero-visual { display: none; }.hero-footer-line { margin-top: 64px; }.feature-grid, .ml-track { grid-template-columns: 1fr; }.ml-step { border-right: 0; border-bottom: 1px solid var(--color-fog); }.ml-step:last-child { border-bottom: 0; }.story-close { align-items: flex-start; flex-direction: column; } }
@media (max-width: 560px) { .story-hero, .workspace-preview, .ml-section, .story-close { padding-left: 16px; padding-right: 16px; }.hero-copy h1 { font-size: 58px; }.hero-stats div { min-width: 0; flex: 1; padding-right: 12px; }.hero-footer-line { flex-direction: column; }.auth-card, .welcome-card { padding: 22px; } }
</style>
