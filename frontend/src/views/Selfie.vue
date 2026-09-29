<template>
  <div class="web-page-wrapper selfie-page-container">
    <!-- Dynamic Background Blobs -->
    <div class="bg-blob-container">
      <div class="bg-blob blob-1"></div>
      <div class="bg-blob blob-2"></div>
      <div class="bg-blob blob-3"></div>
    </div>
    <!-- Header Nav -->
    <header class="selfie-header">
      <router-link to="/home" class="back-btn">
        <ArrowLeft :size="20" />
        <span>Back to Home</span>
      </router-link>
      <h2 class="header-title">Grower Pride</h2>
      <div class="header-spacer"></div>
    </header>

    <div class="selfie-main">
      <!-- Input Panel -->
      <section class="selfie-form-panel card glass-card hover-lift animate-fade-in-up">
        <div class="intro">
          <div class="badge badge-success mb-2">📸 AI Grower Studio</div>
          <h3 class="form-title">Show Your Pride!</h3>
          <p class="form-subtitle">Create and share your personalized harvest poster with the community.</p>
        </div>

        <div class="form-group">
          <label for="crop-select">I AM PROUDLY GROWING</label>
          <select id="crop-select" v-model="crop" @change="drawCanvas" class="premium-select">
            <option value="🌾 Wheat">🌾 Wheat (गेहूं)</option>
            <option value="🌽 Maize">🌽 Maize (मक्का)</option>
            <option value="🌼 Mustard">🌼 Mustard (सरसों)</option>
            <option value="🥔 Potato">🥔 Potato (आलू)</option>
          </select>
        </div>

        <div class="form-group">
          <label for="brand-select">MY TRUSTED BRAND</label>
          <select id="brand-select" v-model="brand" @change="drawCanvas" class="premium-select">
            <option value="Topik 15 WP">Topik 15 WP (Fungicide)</option>
            <option value="Amistar Top">Amistar Top (Fungicide)</option>
            <option value="Actara 25 WG">Actara 25 WG (Insecticide)</option>
            <option value="Score 250 EC">Score 250 EC (Fungicide)</option>
            <option value="Ampligo">Ampligo (Insecticide)</option>
            <option value="Revus">Revus (Fungicide)</option>
          </select>
        </div>

        <div v-if="!imageLoaded" class="upload-area" @click="$refs.fileInput.click()">
          <div class="upload-icon-circle">
            <Camera :size="32" />
          </div>
          <p class="upload-text">Tap to take a selfie or upload crop photo</p>
          <span class="upload-subtext">Supports PNG, JPG, JPEG</span>
          <input type="file" ref="fileInput" accept="image/*" style="display: none;" @change="handleFileUpload" />
        </div>

        <div v-else class="upload-meta-info">
          <div class="success-upload-indicator">
            <span class="indicator-dot"></span>
            <span>Image uploaded successfully</span>
          </div>
          <button class="btn btn-secondary btn-full" @click="resetImage">
            <RefreshCw :size="16" />
            <span>Upload Different Photo</span>
          </button>
        </div>
      </section>

      <!-- Preview Canvas Panel -->
      <section class="selfie-preview-panel card glass-card hover-lift animate-fade-in-up delay-1">
        <h4 class="preview-title">Live Poster Preview</h4>
        
        <div class="canvas-wrapper viewfinder-container">
          <div class="viewfinder-corners" v-if="imageLoaded"></div>
          <div class="viewfinder-corners-bottom" v-if="imageLoaded"></div>
          <div class="rec-indicator" v-if="imageLoaded">
            <span class="rec-dot"></span>
            <span>REC</span>
          </div>
          <div class="camera-grid-lines" v-if="imageLoaded"></div>
          
          <canvas ref="canvasEl" width="1080" height="1080" class="canvas-element"></canvas>
          <div v-if="!imageLoaded" class="canvas-placeholder">
            <Camera :size="48" class="placeholder-icon" />
            <p>Upload a photo to preview your poster</p>
          </div>
        </div>

        <div class="preview-actions" v-if="imageLoaded">
          <button class="btn btn-primary btn-share" @click="shareImage">
            <Share2 :size="18" />
            <span>Share with Friends</span>
          </button>
          <button class="btn btn-secondary btn-download" @click="downloadImageDirect" title="Download Image">
            <Download :size="18" />
            <span>Download</span>
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ArrowLeft, Camera, Share2, Download, RefreshCw } from 'lucide-vue-next'
import { useRealtimeSync } from '../composables/useRealtimeSync'

const fileInput = ref(null)
const canvasEl = ref(null)
const imageLoaded = ref(false)
const userImage = ref(null)

const sync = useRealtimeSync()

const crop = ref(localStorage.getItem('farmer_crop') || '🌾 Wheat')

const brandMap = {
  '🌾 Wheat': 'Topik 15 WP',
  '🌽 Maize': 'Ampligo',
  '🌼 Mustard': 'Actara 25 WG',
  '🥔 Potato': 'Revus'
}

const brand = ref(brandMap[crop.value] || 'Topik 15 WP')

let cleanupFarmerSync = null

onMounted(() => {
  drawCanvas()
  
  cleanupFarmerSync = sync.onFarmerUpdated(() => {
    if (sync.activeFarmerCrop.value && sync.activeFarmerCrop.value !== crop.value) {
      crop.value = sync.activeFarmerCrop.value
    }
    drawCanvas()
  })
})

onUnmounted(() => {
  if (cleanupFarmerSync) cleanupFarmerSync()
  sync.destroy()
})

watch(crop, (newCrop) => {
  if (brandMap[newCrop]) {
    brand.value = brandMap[newCrop]
  }
  if (newCrop !== sync.activeFarmerCrop.value) {
    sync.updateActiveFarmer({
      grower_id: sync.activeFarmerGrowerId.value,
      crop: newCrop
    })
  }
  drawCanvas()
})

watch(brand, () => {
  drawCanvas()
})

watch(() => sync.activeFarmerGrowerId.value, (newGrowerId) => {
  if (sync.activeFarmerCrop.value && sync.activeFarmerCrop.value !== crop.value) {
    crop.value = sync.activeFarmerCrop.value
  }
  drawCanvas()
})

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    const img = new Image()
    img.onload = () => {
      userImage.value = img
      imageLoaded.value = true
      drawCanvas()
    }
    img.src = e.target.result
  }
  reader.readAsDataURL(file)
}

function resetImage() {
  imageLoaded.value = false
  userImage.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// Canvas rendering with premium typography and Syngenta branding layout
function drawCanvas() {
  if (!userImage.value || !canvasEl.value) return

  const canvas = canvasEl.value
  const ctx = canvas.getContext('2d')

  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Draw user image with cover style (centered crop)
  const size = canvas.width
  const scale = Math.max(size / userImage.value.width, size / userImage.value.height)
  const x = (size / 2) - (userImage.value.width / 2) * scale
  const y = (size / 2) - (userImage.value.height / 2) * scale
  
  ctx.drawImage(userImage.value, x, y, userImage.value.width * scale, userImage.value.height * scale)

  // Draw modern dark gradient overlay at the bottom 45% of the canvas
  const gradient = ctx.createLinearGradient(0, size * 0.55, 0, size)
  gradient.addColorStop(0, 'rgba(15, 23, 42, 0)') // Slate-900 transparent
  gradient.addColorStop(0.5, 'rgba(6, 78, 59, 0.65)') // Syngenta emerald-900 deep tint
  gradient.addColorStop(1, 'rgba(2, 8, 23, 0.95)') // Dark slate base
  ctx.fillStyle = gradient
  ctx.fillRect(0, size * 0.55, size, size * 0.45)

  // Draw Syngenta Emerald Stripe Accent
  ctx.fillStyle = '#059669' // Syngenta Emerald Green
  ctx.fillRect(60, size - 310, 8, 230) // Vertical green line bar

  // Draw Eyebrow (PROUD SYNGENTA GROWER)
  ctx.fillStyle = '#10b981' // emerald-400
  ctx.font = 'bold 32px Inter, sans-serif'
  ctx.fillText('PROUD SYNGENTA GROWER', 90, size - 265)

  // Draw main Crop Text
  const cropClean = crop.value.replace(/[^a-zA-Z\s]/g, '').trim()
  ctx.fillStyle = '#ffffff'
  ctx.font = '800 82px Inter, sans-serif'
  ctx.fillText(`Growing ${cropClean}`, 90, size - 170)
  
  // Draw Brand / Protection Badge Text
  ctx.fillStyle = '#cbd5e1' // slate-300
  ctx.font = '600 40px Inter, sans-serif'
  ctx.fillText(`Protected by: ${brand.value}`, 90, size - 105)

  // Draw Syngenta Brandmark logo in bottom right
  ctx.fillStyle = '#10b981' // emerald-400
  ctx.font = 'bold 44px Inter, sans-serif'
  ctx.fillText('Syngenta', size - 280, size - 170)

  ctx.fillStyle = '#ffffff'
  ctx.font = '500 24px Inter, sans-serif'
  ctx.fillText('TERRAPLUS AI', size - 280, size - 130)
}

// Web Share integration with WhatsApp and download fallbacks
function shareImage() {
  if (!canvasEl.value) return
  
  canvasEl.value.toBlob(async (blob) => {
    if (!blob) return
    
    const cropClean = crop.value.replace(/[^a-zA-Z\s]/g, '').trim()
    const shareText = `I am proud to share my harvest! Growing ${cropClean} using Syngenta's ${brand.value}. Created via TerraPlus AI. #Syngenta #GrowerPride`
    const file = new File([blob], 'my_syngenta_harvest.jpg', { type: 'image/jpeg' })

    // Check for native share support of files
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      try {
        await navigator.share({
          files: [file],
          title: 'My Syngenta Harvest',
          text: shareText
        })
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Error sharing image natively:', err)
          fallbackShare(blob, shareText)
        }
      }
    } else {
      // Fallback
      fallbackShare(blob, shareText)
    }
  }, 'image/jpeg', 0.9)
}

function fallbackShare(blob, text) {
  // Trigger file download
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.download = 'my_syngenta_harvest.jpg'
  link.href = url
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)

  // Trigger WhatsApp Web share message fallback
  const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(text + '\n\n[Attach the downloaded my_syngenta_harvest.jpg image]')}`
  window.open(whatsappUrl, '_blank')

  alert('Your custom Grower Pride poster was downloaded! Directing you to WhatsApp to share the message. Attach your downloaded photo to complete the share.')
}

function downloadImageDirect() {
  if (!canvasEl.value) return
  const dataUrl = canvasEl.value.toDataURL('image/jpeg', 0.95)
  const link = document.createElement('a')
  link.download = 'my_syngenta_harvest.jpg'
  link.href = dataUrl
  link.click()
}
</script>

<style scoped>
.selfie-page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--slate-50);
}

/* Header styling */
.selfie-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: white;
  border-bottom: 1px solid var(--color-border);
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--slate-600);
  font-weight: 600;
  font-size: 14px;
  transition: color 0.15s ease;
}

.back-btn:hover {
  color: var(--color-primary);
}

.header-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--slate-900);
  text-align: center;
}

.header-spacer {
  width: 120px;
}

@media (max-width: 640px) {
  .header-spacer {
    display: none;
  }
}

/* Main Layout Grid */
.selfie-main {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 24px;
  max-width: 1200px;
  width: 100%;
  margin: 32px auto;
  padding: 0 24px;
  align-items: start;
}

@media (max-width: 900px) {
  .selfie-main {
    grid-template-columns: 1fr;
    margin: 16px auto;
    padding: 0 16px;
    gap: 16px;
  }
}

/* Forms */
.selfie-form-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.intro {
  margin-bottom: 8px;
}

.mb-2 {
  margin-bottom: 8px;
}

.form-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--slate-900);
  margin-bottom: 4px;
}

.form-subtitle {
  font-size: 13px;
  color: var(--slate-500);
  line-height: 1.4;
}

.premium-select {
  background-color: var(--slate-50);
  border: 1px solid var(--color-border);
  font-weight: 600;
}

.upload-area {
  border: 2px dashed var(--color-primary);
  background-color: var(--color-primary-light);
  border-radius: var(--radius-md);
  padding: 32px 16px;
  text-align: center;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  transition: all 0.2s ease;
}

.upload-area:hover {
  background-color: var(--emerald-100);
}

.upload-icon-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: white;
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.upload-text {
  font-size: 14px;
  font-weight: 700;
  color: var(--emerald-800);
}

.upload-subtext {
  font-size: 11px;
  color: var(--slate-500);
}

.upload-meta-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.success-upload-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--emerald-800);
  font-weight: 600;
  background-color: var(--color-primary-light);
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--emerald-200);
}

.indicator-dot {
  width: 6px;
  height: 6px;
  background-color: var(--color-primary);
  border-radius: 50%;
}

.btn-full {
  width: 100%;
}

/* Preview Canvas Panel */
.selfie-preview-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preview-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--slate-700);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.canvas-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  background-color: var(--slate-100);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.canvas-element {
  width: 100%;
  height: 100%;
  display: block;
}

.canvas-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--slate-400);
  padding: 24px;
  text-align: center;
  gap: 12px;
}

.placeholder-icon {
  opacity: 0.4;
}

.canvas-placeholder p {
  font-size: 14px;
  font-weight: 600;
}

.preview-actions {
  display: flex;
  gap: 12px;
}

.btn-share {
  flex: 1.8;
}

.btn-download {
  flex: 1;
}

@media (max-width: 480px) {
  .preview-actions {
    flex-direction: column;
  }
}
</style>
