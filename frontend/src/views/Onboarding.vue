<template>
  <div class="web-page-wrapper onboarding-page">
    <!-- Dynamic Background Blobs -->
    <div class="bg-blob-container">
      <div class="bg-blob blob-1"></div>
      <div class="bg-blob blob-2"></div>
      <div class="bg-blob blob-3"></div>
    </div>
    <div class="onboarding-container">
      
      <!-- Left Hero Banner Panel (visible on desktop/tablet) -->
      <div class="hero-panel">
        <div class="hero-content">
          <div class="brand animate-fade-in-up">
            <span class="brand-icon">🌱</span>
            <span class="brand-name">Terrapulse</span>
          </div>
          <h1 class="hero-title animate-fade-in-up delay-1">AI-Powered Personalized Agri-Intelligence</h1>
          <p class="hero-subtitle animate-fade-in-up delay-2">
            Get real-time agronomic advisories, localized pest alerts, and direct physical support tailored specifically for your farm.
          </p>
          
          <div class="benefits-list">
            <div class="benefit-item animate-fade-in-up delay-3">
              <div class="benefit-icon">
                <Sprout :size="20" />
              </div>
              <div class="benefit-text">
                <strong>Crop-Specific Advisory</strong>
                <p>Personalized timelines and chemical dosage guides for Wheat, Maize, Mustard, and Potato.</p>
              </div>
            </div>
            
            <div class="benefit-item animate-fade-in-up delay-4">
              <div class="benefit-icon">
                <ShieldAlert :size="20" />
              </div>
              <div class="benefit-text">
                <strong>Localized Pest Alerts</strong>
                <p>Early warnings based on regional weather, humidity, and disease risk factors.</p>
              </div>
            </div>

            <div class="benefit-item animate-fade-in-up delay-5">
              <div class="benefit-icon">
                <Globe :size="20" />
              </div>
              <div class="benefit-text">
                <strong>Vernacular First</strong>
                <p>Access all advisories and AI dialogs in your preferred regional language.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="hero-footer animate-fade-in-up delay-5">
          <span>Syngenta Hackathon 2026</span>
          <span>Personalization at Scale</span>
        </div>
      </div>

      <!-- Right Form Panel -->
      <div class="form-panel">
        <div class="form-scroll-container">
          <div class="mobile-logo-header animate-fade-in-up">
            <span class="brand-icon">🌱</span>
            <span class="brand-name">Terrapulse</span>
          </div>

          <div class="welcome-header animate-fade-in-up">
            <h2>Welcome to Terrapulse</h2>
            <p>Setup your profile to receive personalized crop advice and alerts.</p>
          </div>

          <div class="form-sections">
            <!-- 0. Farmer Name -->
            <div class="form-group animate-fade-in-up">
              <label class="section-label" for="farmer-name-input"><User :size="16" /> ENTER YOUR NAME</label>
              <input 
                id="farmer-name-input"
                type="text"
                v-model="selectedName"
                class="premium-input hover-lift"
                placeholder="Enter your name (e.g. Ramesh Kumar)"
              />
            </div>

            <!-- 1. Language -->
            <div class="form-group animate-fade-in-up delay-1">
              <label class="section-label"><Globe :size="16" /> CHOOSE YOUR LANGUAGE</label>
              <div class="lang-grid">
                <button 
                  v-for="lang in languages" 
                  :key="lang.code"
                  type="button" 
                  class="lang-card-btn hover-lift active-scale"
                  :class="{ active: selectedLanguage === lang.name }"
                  @click="selectedLanguage = lang.name"
                >
                  <span class="lang-native">{{ lang.native }}</span>
                  <span class="lang-english">{{ lang.name }}</span>
                  <span class="active-badge" v-if="selectedLanguage === lang.name">✓</span>
                </button>
              </div>
            </div>

            <!-- 2. Main Crop -->
            <div class="form-group animate-fade-in-up delay-2">
              <label class="section-label"><Sprout :size="16" /> YOUR MAIN CROP</label>
              <div class="crop-grid">
                <button 
                  v-for="c in crops" 
                  :key="c.name"
                  type="button"
                  class="crop-card-btn hover-lift active-scale"
                  :class="{ active: selectedCrop === c.value }"
                  @click="selectedCrop = c.value"
                >
                  <span class="crop-emoji">{{ c.emoji }}</span>
                  <span class="crop-name">{{ c.name }}</span>
                  <span class="crop-desc">{{ c.desc }}</span>
                  <span class="active-badge" v-if="selectedCrop === c.value">✓</span>
                </button>
              </div>
            </div>

            <!-- 3. State & District -->
            <div class="form-group animate-fade-in-up delay-3">
              <label class="section-label" for="location-select"><MapPin :size="16" /> STATE / DISTRICT</label>
              <select id="location-select" v-model="selectedLocation" class="premium-select hover-lift">
                <option value="Uttar Pradesh · Agra">Uttar Pradesh · Agra (High Humidity Region)</option>
                <option value="Punjab · Ludhiana">Punjab · Ludhiana (Irrigation Intensive Region)</option>
                <option value="Bihar · Patna">Bihar · Patna (Moderate Humidity Region)</option>
              </select>
            </div>

            <!-- 4. Farm Size -->
            <div class="form-group animate-fade-in-up delay-4">
              <label class="section-label"><Smartphone :size="16" /> FARM SIZE</label>
              <div class="segmented-control">
                <button 
                  v-for="size in farmSizes" 
                  :key="size"
                  type="button"
                  class="segment-btn active-scale"
                  :class="{ active: selectedFarmSize === size }"
                  @click="selectedFarmSize = size"
                >
                  {{ size }}
                </button>
              </div>
            </div>

            <!-- Submit -->
            <div class="form-actions animate-fade-in-up delay-5">
              <button @click="saveAndProceed" :disabled="isSubmitting" class="btn btn-primary btn-submit hover-lift active-scale">
                <span v-if="isSubmitting">Saving profile...</span>
                <span v-else>Configure Profile & Get Started</span>
                <ArrowRight v-if="!isSubmitting" :size="18" class="arrow-icon" />
              </button>
              <p class="terms-note">By proceeding, you agree to receive personalized automated campaign messages via WhatsApp, Voice, and SMS.</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Globe, 
  Sprout, 
  MapPin, 
  Smartphone, 
  ArrowRight, 
  ShieldAlert,
  User
} from 'lucide-vue-next'
import { useRealtimeSync } from '../composables/useRealtimeSync'
import { upsertFarmer } from '../api'
import { useToast } from '../composables/useToast'

const router = useRouter()
const sync = useRealtimeSync()
const toast = useToast()
const isSubmitting = ref(false)

// Load pre-existing state if available
const selectedName = ref(localStorage.getItem('farmer_name') || '')
const selectedLanguage = ref(localStorage.getItem('farmer_language') || 'Hindi')
const selectedCrop = ref(localStorage.getItem('farmer_crop') || '🌾 Wheat')
const selectedLocation = ref(localStorage.getItem('farmer_location') || 'Uttar Pradesh · Agra')
const selectedFarmSize = ref(localStorage.getItem('farmer_size') || '2–5 acres')

const languages = [
  { code: 'hi', native: 'हिंदी', name: 'Hindi' },
  { code: 'pa', native: 'ਪੰਜਾਬੀ', name: 'Punjabi' },
  { code: 'mr', native: 'मराठी', name: 'Marathi' },
  { code: 'gu', native: 'ગુજરાતી', name: 'Gujarati' },
  { code: 'bn', native: 'বাংলা', name: 'Bengali' },
  { code: 'kn', native: 'ಕನ್ನಡ', name: 'Kannada' }
]

const crops = [
  { value: '🌾 Wheat', name: 'Wheat (गेहूं)', emoji: '🌾', desc: 'Rabi · 120-130 days' },
  { value: '🌽 Maize', name: 'Maize (मक्का)', emoji: '🌽', desc: 'Kharif/Rabi · 100 days' },
  { value: '🌼 Mustard', name: 'Mustard (सरसों)', emoji: '🌼', desc: 'Rabi · 110 days' },
  { value: '🥔 Potato', name: 'Potato (आलू)', emoji: '🥔', desc: 'Rabi · 90-100 days' }
]

const farmSizes = ['Under 2 acres', '2–5 acres', '5–10 acres', '10+ acres']

const updateLocalFields = () => {
  selectedName.value = sync.activeFarmerName.value
  selectedLanguage.value = sync.activeFarmerLanguage.value
  selectedCrop.value = sync.activeFarmerCrop.value
  selectedLocation.value = sync.activeFarmerLocation.value
  selectedFarmSize.value = sync.activeFarmerSize.value
}

let cleanupFarmerSync = null

onMounted(() => {
  cleanupFarmerSync = sync.onFarmerUpdated(() => {
    updateLocalFields()
  })
})

onUnmounted(() => {
  if (cleanupFarmerSync) {
    cleanupFarmerSync()
  }
  sync.destroy()
})

watch(sync.activeFarmerGrowerId, () => {
  updateLocalFields()
})

const saveAndProceed = async () => {
  if (isSubmitting.value) return
  isSubmitting.value = true

  const name = selectedName.value.trim() || 'Ramesh Kumar'
  const existingId = localStorage.getItem('farmer_grower_id')
  const growerId = existingId || ('GRW_' + Math.random().toString(36).substring(2, 9).toUpperCase())

  // Parse location into state + district
  const [state, district] = (selectedLocation.value || '').split(' · ')

  // Extract clean crop name (remove emoji prefix)
  const cropClean = (selectedCrop.value || '').replace(/^[^\w]+/, '').trim().toLowerCase()

  // Map farm size text to numeric acres
  const sizeMap = { 'Under 2 acres': 1.5, '2–5 acres': 3.5, '5–10 acres': 7, '10+ acres': 12 }
  const farmSizeNum = sizeMap[selectedFarmSize.value] || 3.5

  // Device heuristic: check screen width
  const deviceType = window.innerWidth <= 480 ? 'feature_phone' : 'smartphone'

  // Build the FarmerProfile payload matching the backend schema
  const profile = {
    grower_id: growerId,
    name: name,
    state: state?.trim() || null,
    district: district?.trim() || null,
    language: selectedLanguage.value,
    main_crop: cropClean,
    grower_farm_size: farmSizeNum,
    device_type: deviceType,
    connectivity: 'good',
    literacy_level: 'medium',
  }

  try {
    // Persist to backend DB
    await upsertFarmer(profile)
    toast.success(`✅ Profile registered for ${name}!`)
  } catch (err) {
    console.warn('Backend persist failed, continuing with local-only:', err)
    toast.info('Profile saved locally (backend unreachable)')
  }

  // Sync to other tabs via BroadcastChannel / WebSocket
  sync.updateActiveFarmer({
    name,
    language: selectedLanguage.value,
    crop: selectedCrop.value,
    location: selectedLocation.value,
    size: selectedFarmSize.value,
    grower_id: growerId
  })

  localStorage.setItem('farmer_registered', 'true')
  isSubmitting.value = false
  router.push('/home')
}
</script>

<style scoped>
.onboarding-page {
  min-height: 100vh;
  overflow: hidden;
  background-color: var(--slate-900);
}

.onboarding-container {
  display: flex;
  height: 100vh;
  width: 100%;
}

/* Left Hero Panel Styling with flow animations */
@keyframes gradientFlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes floatShape {
  0% { transform: translateY(0px) rotate(0deg); }
  100% { transform: translateY(-30px) rotate(8deg); }
}

.hero-panel {
  flex: 1.2;
  background: linear-gradient(-45deg, var(--slate-950) 0%, var(--emerald-950) 50%, var(--slate-900) 100%);
  background-size: 200% 200%;
  animation: gradientFlow 15s ease infinite;
  color: white;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-right: 1px solid var(--slate-800);
  position: relative;
  overflow: hidden;
}

.hero-panel::before {
  content: '';
  position: absolute;
  top: -10%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(16,185,129,0.08) 0%, transparent 70%);
  z-index: 1;
  pointer-events: none;
  animation: floatShape 12s infinite alternate ease-in-out;
}

.hero-panel::after {
  content: '';
  position: absolute;
  bottom: -15%;
  left: -15%;
  width: 450px;
  height: 450px;
  background: radial-gradient(circle, rgba(16,185,129,0.05) 0%, transparent 60%);
  z-index: 1;
  pointer-events: none;
  animation: floatShape 18s infinite alternate-reverse ease-in-out;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 40px;
}

.brand-icon {
  font-size: 32px;
}

.brand-name {
  font-size: 24px;
  font-weight: 800;
  color: var(--emerald-400);
  letter-spacing: -0.025em;
  text-shadow: 0 0 10px rgba(16, 185, 129, 0.15);
}

.hero-content {
  max-width: 560px;
  z-index: 2;
  margin-top: auto;
  margin-bottom: auto;
}

.hero-title {
  font-size: 40px;
  font-weight: 800;
  line-height: 1.15;
  color: white;
  margin-bottom: 20px;
  letter-spacing: -0.03em;
}

.hero-subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--slate-300);
  margin-bottom: 40px;
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.benefit-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.benefit-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background-color: rgba(16, 185, 129, 0.15);
  color: var(--emerald-400);
  flex-shrink: 0;
  box-shadow: 0 0 15px rgba(16, 185, 129, 0.1);
}

.benefit-text strong {
  display: block;
  font-size: 15px;
  color: white;
  margin-bottom: 4px;
}

.benefit-text p {
  font-size: 13px;
  color: var(--slate-300);
  margin: 0;
  line-height: 1.4;
}

.hero-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--slate-500);
  font-weight: 600;
}

/* Right Form Panel Styling */
.form-panel {
  flex: 1;
  background: #ffffff;
  border-left: 1px solid var(--slate-200);
  padding: 60px 48px;
  overflow-y: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-scroll-container {
  max-width: 520px;
  width: 100%;
}

.mobile-logo-header {
  display: none;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}

.mobile-logo-header .brand-name {
  font-size: 20px;
  font-weight: 800;
  color: var(--emerald-600);
}

.welcome-header {
  margin-bottom: 32px;
}

.welcome-header h2 {
  font-size: 28px;
  font-weight: 800;
  color: var(--slate-900);
  letter-spacing: -0.025em;
  margin-bottom: 8px;
}

.welcome-header p {
  color: var(--slate-900);
  font-size: 14px;
  font-weight: 500;
}

.form-sections {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 700;
  color: var(--slate-900);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

/* Grids with glass overlay style */
.lang-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.lang-card-btn {
  background: #ffffff;
  border: 1px solid var(--slate-300) !important;
  border-radius: var(--radius-md);
  padding: 14px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  position: relative;
  min-height: auto;
}

.lang-card-btn:hover, .crop-card-btn:hover {
  border-color: var(--emerald-400) !important;
}

.lang-card-btn.active {
  border-color: var(--emerald-500) !important;
  background: var(--emerald-50) !important;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.1);
}

.lang-native {
  font-size: 16px;
  font-weight: 700;
  color: var(--slate-900);
  margin-bottom: 2px;
}

.lang-card-btn.active .lang-native {
  color: var(--emerald-800);
}

.lang-english {
  font-size: 11px;
  color: var(--slate-800);
  font-weight: 500;
}

.active-badge {
  position: absolute;
  top: 6px;
  right: 8px;
  width: 16px;
  height: 16px;
  background-color: var(--emerald-600);
  color: white;
  border-radius: 50%;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Crop Selection */
.crop-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.crop-card-btn {
  background: #ffffff;
  border: 1px solid var(--slate-300) !important;
  border-radius: var(--radius-md);
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  cursor: pointer;
  position: relative;
  text-align: left;
  min-height: auto;
}

.crop-card-btn.active {
  border-color: var(--emerald-500) !important;
  background: var(--emerald-50) !important;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.1);
}

.crop-emoji {
  font-size: 28px;
  margin-bottom: 8px;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.crop-card-btn:hover .crop-emoji {
  transform: scale(1.15) rotate(5deg);
}

.crop-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--slate-900);
  margin-bottom: 4px;
}

.crop-card-btn.active .crop-name {
  color: var(--emerald-800);
}

.crop-desc {
  font-size: 11px;
  color: var(--slate-800);
  font-weight: 500;
}

/* Premium Select & Input */
.premium-select, .premium-input {
  width: 100%;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--slate-300);
  background-color: var(--slate-50);
  font-size: 14px;
  font-weight: 600;
  color: var(--slate-900);
  transition: all 0.2s ease;
}

.premium-select {
  cursor: pointer;
}

.premium-input::placeholder {
  color: var(--slate-400);
  font-weight: 500;
}

.premium-input:focus, .premium-select:focus {
  outline: none;
  border-color: var(--emerald-500);
  background-color: white;
  box-shadow: 0 0 0 3px var(--emerald-100);
}

/* Segmented Control */
.segmented-control {
  display: flex;
  background-color: var(--slate-100);
  padding: 4px;
  border-radius: var(--radius-md);
  border: 1px solid var(--slate-300);
}

.segment-btn {
  flex: 1;
  border: 0;
  background: transparent;
  color: var(--slate-900);
  font-size: 13px;
  font-weight: 600;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: auto;
}

.segment-btn.active {
  background-color: white;
  color: var(--slate-900);
  box-shadow: var(--shadow-sm);
}

/* Submit Actions and Hover animation */
.form-actions {
  margin-top: 12px;
}

.btn-submit {
  width: 100%;
  padding: 14px;
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 700;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  background-color: var(--emerald-700) !important;
  color: white !important;
}

.arrow-icon {
  transition: transform 0.2s ease;
}

.btn-submit:hover {
  background-color: var(--emerald-800) !important;
}

.btn-submit:hover .arrow-icon {
  transform: translateX(4px);
}

.terms-note {
  font-size: 11px;
  color: var(--slate-800);
  text-align: center;
  margin-top: 14px;
  line-height: 1.4;
  font-weight: 500;
}

/* Responsive Breakpoints */
@media (max-width: 1024px) {
  .hero-panel {
    display: none;
  }
  .form-panel {
    padding: 40px 20px;
  }
  .mobile-logo-header {
    display: flex;
  }
}

@media (max-width: 640px) {
  .lang-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
