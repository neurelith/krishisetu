<template>
  <section class="diagnostic-evaluation-card card-solid">
    <div class="section-header-row">
      <div>
        <h2>What it is and what to do now</h2>
        <p class="section-sub">Computer Vision Clinical Match · Spectral & Phenological Correlation</p>
      </div>
      <span class="badge-institutional badge-sky">Laboratory Output</span>
    </div>

    <!-- Skeleton Loader for Loading State -->
    <div v-if="isDiagnosing" class="diagnostic-skeleton-card">
      <div class="skeleton-block skeleton-shimmer" style="height: 32px; width: 75%; margin-bottom: 12px;"></div>
      <div class="skeleton-block skeleton-shimmer" style="height: 20px; width: 50%; margin-bottom: 16px;"></div>
      <div class="skeleton-block skeleton-shimmer" style="height: 48px; width: 100%; margin-bottom: 12px;"></div>
      <div class="skeleton-block skeleton-shimmer" style="height: 80px; width: 100%; margin-bottom: 12px;"></div>
      <div class="skeleton-block skeleton-shimmer" style="height: 60px; width: 100%;"></div>
    </div>

    <!-- Guardrail Alert (Rejection of Non-Agricultural / Non-Crop Input) -->
    <div v-else-if="diagnosisResult && !diagnosisResult.is_valid_crop_image" class="guardrail-alert-box">
      <div class="alert-icon-frame">
        <PhWarningCircle :size="24" weight="bold" class="text-alert" />
      </div>
      <div>
        <h3 class="guardrail-title">Image Validation Guardrail Activated</h3>
        <p v-text="diagnosisResult.rejection_reason"></p>
        <span class="guardrail-sub">Model: <span v-text="diagnosisResult.model_used"></span> · Zero-Misdiagnosis Protection Standard</span>
      </div>
    </div>

    <!-- Verified Diagnostic Findings Content -->
    <div v-else-if="diagnosisResult && diagnosisResult.is_valid_crop_image" class="lab-findings-body">
      <div class="diag-header-row">
        <div>
          <span class="diag-label">Identified Pathology Marker</span>
          <h3 class="diag-condition-title" v-text="diagnosisResult.condition_detected"></h3>
          <em class="diag-scientific-name font-editorial-italic" v-text="diagnosisResult.scientific_name"></em>
        </div>
        <div style="display: flex; align-items: center; gap: var(--space-3); flex-wrap: wrap;">
          <button type="button" @click="$emit('share-card')" class="btn-gov-outline" title="Export Share Card PNG" style="min-height: 44px; display: inline-flex; align-items: center; gap: var(--space-2);">
            <PhShareNetwork :size="18" weight="bold" />
            <span>Share card</span>
          </button>
          <!-- Precision Certainty Gauge -->
          <div class="diag-match-badge">
            <span class="match-percentage">{{ Math.round(diagnosisResult.confidence * 100) }}%</span>
            <span class="meta">Clinical Confidence</span>
          </div>
        </div>
      </div>

      <!-- Specific Morphological Symptoms List -->
      <div class="symptoms-panel">
        <h4>Observed Pathological Symptoms</h4>
        <ul class="symptoms-list">
          <li v-for="(symp, sIdx) in diagnosisResult.symptoms" :key="sIdx" v-text="symp"></li>
        </ul>
      </div>

      <!-- Immediate Bio-Action Protocol -->
      <div class="immediate-action-callout">
        <h4>Immediate Agronomic Prescription</h4>
        <p class="action-narrative" v-text="diagnosisResult.immediate_bio_action"></p>
      </div>

      <!-- Pathogen Cycle Infographic -->
      <InfographicPathogenCycle />
    </div>

    <div v-else class="empty-diagnosis-standby">
      <div class="standby-icon-frame">
        <PhPlant :size="36" weight="bold" class="standby-icon" />
      </div>
      <div class="standby-content">
        <span class="standby-chip">DIAGNOSTIC STANDBY</span>
        <h3 class="standby-title">Awaiting Clinical Specimen Intake</h3>
        <p class="standby-desc">
          Select a benchmark specimen on the left or upload a field photograph to trigger multimodal computer vision verification.
        </p>
        <div class="standby-steps-matrix">
          <div class="standby-step">
            <span class="step-num">1</span>
            <div>
              <strong>Sample Intake:</strong>
              <span>Capture leaf lesion in sunlight or choose benchmark specimen.</span>
            </div>
          </div>
          <div class="standby-step">
            <span class="step-num">2</span>
            <div>
              <strong>Audio Observation:</strong>
              <span>Speak symptoms in local dialect (Bengali/Hindi) for symptom triage.</span>
            </div>
          </div>
          <div class="standby-step">
            <span class="step-num">3</span>
            <div>
              <strong>ICAR Action Plan:</strong>
              <span>Receive immediate bio-control protocol and 1080x1350 WhatsApp share card.</span>
            </div>
          </div>
        </div>
      </div>
      <div class="standby-footer">
        <span class="badge-institutional badge-forest">DPG Validation Engine · ICAR-CRRI Standard</span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { PhWarningCircle, PhShareNetwork, PhPlant } from '@phosphor-icons/vue'
import InfographicPathogenCycle from '../InfographicPathogenCycle.vue'

defineProps({
  diagnosisResult: { type: Object, default: null },
  isDiagnosing: { type: Boolean, default: false }
})

defineEmits(['share-card'])
</script>
