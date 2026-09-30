<template>
  <div class="share-card-exporter">
    <!-- Off-screen 1080x1350 Card for HTML-to-Image Export -->
    <div ref="cardRef" class="share-card-canvas">
      <!-- Background & Band -->
      <div class="card-band">
        <div class="card-brand-row">
          <div class="brand-badge-box">
            <PhPlant :size="48" weight="bold" class="card-brand-icon" />
          </div>
          <div>
            <h1 class="brand-name">KrishiSetu · কৃষি-সেতু</h1>
            <span class="brand-kicker">ICAR / GOI Digital Public Good · Interoperable Agriculture Network</span>
          </div>
        </div>
        <span class="dpg-chip">DPG Standard v1.0</span>
      </div>

      <!-- Main Alert Content -->
      <div class="card-body">
        <!-- District & Crop Line -->
        <div class="card-meta-row">
          <div class="card-location">
            <PhMapPin :size="32" weight="bold" />
            <span>{{ district }}, {{ state }}</span>
          </div>
          <div class="card-risk-pill" :class="riskBadgeClass">
            <PhWarning :size="28" weight="bold" />
            <span>RISK LEVEL: {{ (riskLevel || 'HIGH').toUpperCase() }}</span>
          </div>
        </div>

        <!-- Big Local-Language Headline -->
        <div class="card-headline-box">
          <span class="eyebrow-card">ALERT & ADVISORY · সতর্কবার্তা</span>
          <h2 class="headline-local">{{ displayLocalHeadline }}</h2>
          <h3 class="headline-en">{{ title }}</h3>
          <p v-if="crop" class="crop-info">Affected Crop: <strong>{{ crop }}</strong></p>
        </div>

        <!-- Next Action / Immediate Steps -->
        <div class="card-action-box">
          <div class="action-header">
            <PhShieldCheck :size="36" weight="bold" />
            <span>IMMEDIATE BIOLOGICAL ACTION MANDATE · করণীয় পদক্ষেপ</span>
          </div>
          <p class="action-text">{{ nextStep }}</p>
        </div>

        <!-- Footer -->
        <div class="card-footer">
          <div class="footer-left">
            <PhBroadcast :size="28" weight="bold" />
            <span>Harmonized Interstate Corridor Early Warning</span>
          </div>
          <div class="footer-right">
            <span class="app-url-text">{{ appUrl }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { toPng } from 'html-to-image'
import { PhPlant, PhMapPin, PhWarning, PhShieldCheck, PhBroadcast } from '@phosphor-icons/vue'

const props = defineProps({
  title: { type: String, default: 'Crop Disease Alert' },
  headlineLocal: { type: String, default: '' },
  district: { type: String, default: 'Nadia' },
  state: { type: String, default: 'West Bengal' },
  riskLevel: { type: String, default: 'High' },
  nextStep: { type: String, default: 'Apply Trichoderma harzianum @ 5g/L water along crop base.' },
  crop: { type: String, default: 'Rice (Paddy)' },
  appUrl: { type: String, default: 'krishisetu.gov.in' }
})

const cardRef = ref(null)

const riskBadgeClass = computed(() => {
  const r = (props.riskLevel || '').toLowerCase()
  if (r.includes('severe') || r.includes('critical')) return 'risk-severe'
  if (r.includes('high')) return 'risk-high'
  return 'risk-elevated'
})

const displayLocalHeadline = computed(() => {
  if (props.headlineLocal) return props.headlineLocal
  if (props.title.toLowerCase().includes('sheath blight')) {
    return 'ধানে খোল পোড়া (Sheath Blight) রোগের প্রাদুর্ভাব'
  }
  if (props.title.toLowerCase().includes('rust')) {
    return 'গমের হলুদ মরিচা (Yellow Rust) রোগের প্রাদুর্ভাব'
  }
  if (props.title.toLowerCase().includes('bollworm')) {
    return 'তুলার গোলাপি শুঁয়োপোকার (Pink Bollworm) আক্রমণ'
  }
  return `সতর্কতা: ${props.title}`
})

async function exportCardPng(customName) {
  if (!cardRef.value) return
  try {
    // Bengali/Hindi glyphs render as tofu boxes if fonts aren't loaded yet.
    await document.fonts.ready
    const dataUrl = await toPng(cardRef.value, {
      pixelRatio: 1,
      cacheBust: true
    })
    const link = document.createElement('a')
    link.download = customName || `krishisetu-alert-${Date.now()}.png`
    link.href = dataUrl
    link.click()
    return true
  } catch (err) {
    console.error('Failed to export share card PNG:', err)
    return false
  }
}

defineExpose({
  exportCardPng
})
</script>

<style scoped>
.share-card-exporter {
  position: absolute;
  left: -9999px;
  top: 0;
  pointer-events: none;
  overflow: hidden;
}

/* 1080 x 1350 High-Res Instagram Portrait Canvas */
.share-card-canvas {
  width: 1080px;
  height: 1350px;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--font-sans);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.card-band {
  background: var(--sarson);
  color: var(--canopy);
  padding: 48px 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 4px solid var(--canopy);
}

.card-brand-row {
  display: flex;
  align-items: center;
  gap: 24px;
}

.brand-badge-box {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-md);
  background: var(--canopy);
  color: var(--sarson);
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-brand-icon {
  color: var(--sarson);
}

.brand-name {
  font-size: 40px;
  font-weight: 800;
  color: var(--canopy);
  margin: 0;
  letter-spacing: -0.02em;
}

.brand-kicker {
  font-size: 20px;
  font-weight: 600;
  color: var(--canopy);
  margin-top: 4px;
  display: block;
}

.dpg-chip {
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 700;
  background: var(--canopy);
  color: var(--paper-raised);
  padding: 10px 24px;
  border-radius: var(--radius-pill);
}

.card-body {
  padding: 56px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-location {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 32px;
  font-weight: 700;
  color: var(--ink-2);
}

.card-risk-pill {
  display: flex;
  align-items: center;
  gap: 14px;
  font-family: var(--font-mono);
  font-size: 24px;
  font-weight: 800;
  padding: 12px 28px;
  border-radius: var(--radius-pill);
}

.risk-severe {
  background: var(--brick-wash);
  color: var(--brick);
  border: 3px solid var(--brick-line);
}

.risk-high {
  background: var(--ochre-wash);
  color: var(--ochre);
  border: 3px solid var(--ochre-line);
}

.risk-elevated {
  background: var(--green-wash);
  color: var(--canopy);
  border: 3px solid var(--green-line);
}

.card-headline-box {
  background: var(--paper-raised);
  border: 3px solid var(--hairline-strong);
  border-radius: var(--radius-md);
  padding: 48px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.eyebrow-card {
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 700;
  color: var(--alert-text);
  letter-spacing: 0.08em;
}

.headline-local {
  font-family: "Anek Bangla", "Anek Devanagari", var(--font-display);
  font-size: 56px;
  font-weight: 800;
  line-height: 1.15;
  color: var(--canopy);
  margin: 0;
}

.headline-en {
  font-size: 36px;
  font-weight: 700;
  color: var(--ink-2);
  margin: 0;
}

.crop-info {
  font-size: 26px;
  color: var(--ink-3);
  margin: 8px 0 0 0;
}

.card-action-box {
  background: var(--green-wash);
  border: 3px solid var(--canopy);
  border-radius: var(--radius-md);
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.action-header {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 26px;
  font-weight: 800;
  color: var(--canopy);
  letter-spacing: 0.02em;
}

.action-text {
  font-size: 32px;
  font-weight: 600;
  line-height: 1.45;
  color: var(--canopy);
  margin: 0;
}

.card-footer {
  border-top: 3px solid var(--hairline-strong);
  padding-top: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 24px;
  color: var(--ink-3);
  font-weight: 600;
}

.app-url-text {
  font-family: var(--font-mono);
  font-size: 28px;
  font-weight: 700;
  color: var(--leaf);
}
</style>
