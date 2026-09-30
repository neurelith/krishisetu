<template>
  <section class="diagnostic-intake-card card-solid">
    <div class="section-header-row">
      <div>
        <h2>Check a leaf</h2>
        <p class="section-sub">Photo or voice note — get today's diagnosis</p>
      </div>
      <span class="badge-institutional badge-forest">Field intake</span>
    </div>

    <!-- Sample picker (try a real case without a camera) -->
    <div class="specimen-selector-bar">
      <span class="selector-subheading">Or try a sample case:</span>
      <div class="segmented-specimen-group">
        <button 
          @click="$emit('select-sample', 'rice')" 
          class="specimen-tab-btn" 
          :class="{ active: selectedSample === 'rice' }"
          type="button"
        >
          <span class="crop-indicator indicator-rice"></span>
          <span>Rice: Sheath Blight</span>
        </button>
        <button 
          @click="$emit('select-sample', 'wheat')" 
          class="specimen-tab-btn" 
          :class="{ active: selectedSample === 'wheat' }"
          type="button"
        >
          <span class="crop-indicator indicator-wheat"></span>
          <span>Wheat: Yellow Rust</span>
        </button>
        <button 
          @click="$emit('select-sample', 'cotton')" 
          class="specimen-tab-btn" 
          :class="{ active: selectedSample === 'cotton' }"
          type="button"
        >
          <span class="crop-indicator indicator-cotton"></span>
          <span>Cotton: Bollworm</span>
        </button>
        <button 
          @click="$emit('select-sample', 'invalid_dog')" 
          class="specimen-tab-btn btn-guardrail" 
          :class="{ active: selectedSample === 'invalid_dog' }"
          type="button"
        >
          <span class="crop-indicator indicator-guardrail"></span>
          <span>Guardrail: Non-Crop</span>
        </button>
      </div>
    </div>

    <!-- Specimen Inspection Viewfinder Stage with Precision Optical Reticles -->
    <div class="specimen-stage-frame">
      <div class="specimen-viewfinder" @click="triggerFileInput">
        <input 
          type="file" 
          ref="fileInputRef" 
          @change="onFileSelected" 
          accept="image/*" 
          class="hidden-input-element" 
          aria-label="Specimen leaf photo upload"
          tabindex="-1"
        />
        <!-- Corner Optical Reticles -->
        <div class="reticle-corner reticle-tl"></div>
        <div class="reticle-corner reticle-tr"></div>
        <div class="reticle-corner reticle-bl"></div>
        <div class="reticle-corner reticle-br"></div>

        <img :src="previewImage" alt="Leaf Sample" width="480" height="320" class="specimen-rendered-image" />
        <div class="viewfinder-overlay">
          <div class="viewfinder-tag">
            <span class="tag-dot"></span>
            <span>{{ selectedFileName || 'Specimen Photo' }}</span>
          </div>
          <button @click.stop="triggerFileInput" class="btn-change-photo" type="button">
            <PhUploadSimple :size="16" weight="bold" />
            <span>Upload Photo</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Farmer Voice Observation Console (56px touch target) -->
    <div class="voice-intake-card">
      <div class="voice-intake-header">
        <span class="voice-intake-title">Say what you see (voice note)</span>
        <span class="badge-institutional badge-slate"><span v-text="langName"></span></span>
      </div>
      <div class="voice-action-row">
        <button 
          @click.stop="$emit('toggle-voice')" 
          class="btn-voice-record" 
          :class="{ 'is-active-recording': isRecording }" 
          type="button"
        >
          <PhMicrophone :size="20" weight="bold" />
          <span>{{ isRecording ? 'Listening (Speak observation)...' : 'Record Voice Observation' }}</span>
        </button>
        <button 
          v-if="voiceTranscript" 
          @click="$emit('clear-voice')" 
          class="btn-gov-outline btn-compact" 
          type="button"
        >
          Clear
        </button>
      </div>
      <div v-if="voiceTranscript" class="transcript-box">
        <span class="transcript-lead">Recorded Clinical Transcript:</span>
        <p class="transcript-quote font-editorial-italic">"{{ voiceTranscript }}"</p>
      </div>
      <p v-else class="voice-hint font-editorial-italic">
        "Spoken farmer queries in Bengali or Hindi are transcribed locally and fused into Gemini's multi-source diagnostic reasoning."
      </p>
    </div>

    <!-- Action Execution Button (56px primary touch target) -->
    <div class="diagnose-actions">
      <button 
        @click="$emit('run-diagnosis')" 
        class="btn-gov-primary btn-execute-diagnosis" 
        :disabled="isDiagnosing || !previewImage"
        type="button"
      >
        <PhArrowsClockwise v-if="isDiagnosing" :size="20" weight="bold" class="spin" />
        <PhSparkle v-else :size="20" weight="bold" />
        <span>{{ isDiagnosing ? 'Checking your leaf…' : 'Check my leaf' }}</span>
      </button>
    </div>

    <!-- Specimen Technical Metadata -->
    <div class="specimen-tech-bar">
      <span>AI check · photo deleted after analysis (DPDP Act 2023)</span>
      <span>Zero-Retention DPDP Act 2023 Compliant</span>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { PhUploadSimple, PhMicrophone, PhArrowsClockwise, PhSparkle } from '@phosphor-icons/vue'

const props = defineProps({
  selectedSample: { type: String, default: 'rice' },
  previewImage: { type: String, default: '' },
  selectedFileName: { type: String, default: '' },
  isRecording: { type: Boolean, default: false },
  voiceTranscript: { type: String, default: '' },
  isDiagnosing: { type: Boolean, default: false },
  preferredLanguage: { type: String, default: 'bn' }
})

const emit = defineEmits([
  'select-sample',
  'file-selected',
  'toggle-voice',
  'clear-voice',
  'run-diagnosis'
])

const fileInputRef = ref(null)

const langName = computed(() => {
  if (props.preferredLanguage === 'bn') return 'Bengali'
  if (props.preferredLanguage === 'hi') return 'Hindi'
  return 'English'
})

function triggerFileInput() {
  fileInputRef.value?.click()
}

function onFileSelected(event) {
  const file = event.target.files?.[0]
  if (file) {
    emit('file-selected', file)
  }
}
</script>
