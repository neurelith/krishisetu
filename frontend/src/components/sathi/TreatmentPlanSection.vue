<template>
  <section v-if="advisoryResult" class="treatment-dossier-section unboxed">
    <div class="dossier-masthead card-solid" style="margin-bottom: 20px;">
      <div>
        <h2>Your treatment plan</h2>
        <span class="meta">Step-by-step plan · checked against ICAR advisories</span>
      </div>
      <div style="display: flex; align-items: center; gap: 8px;">
        <span class="badge-institutional badge-forest">
          {{ advisoryResult.language === 'bn' ? 'বাংলা সংস্করণ' : (advisoryResult.language === 'hi' ? 'हिन्दी संस्करण' : 'English Edition') }}
        </span>
        <button
          v-if="advisoryResult.summary_advisory_en"
          @click="showEn = !showEn"
          type="button"
          class="btn-gov-outline btn-compact"
        >
          {{ showEn ? 'Show local language advice' : 'Show English translation' }}
        </button>
      </div>
    </div>

    <!-- Summary Advisory Lead -->
    <div class="summary-advisory-card card-solid" style="margin-bottom: 20px;">
      <p class="summary-advisory-lead">
        {{ showEn && advisoryResult.summary_advisory_en ? advisoryResult.summary_advisory_en : advisoryResult.summary_advisory }}
      </p>
    </div>

    <!-- Structured Action Plan Grid -->
    <div class="actions-tri-grid" style="margin-bottom: 24px;">
      <div
        v-for="(action, aIdx) in advisoryResult.actions"
        :key="aIdx"
        class="action-card card-solid"
      >
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span class="badge-institutional badge-slate">{{ action.category }}</span>
          <span class="badge-institutional" :class="action.urgency?.toLowerCase().includes('critical') || action.urgency?.toLowerCase().includes('immediate') ? 'badge-soil' : 'badge-forest'">
            {{ action.urgency }}
          </span>
        </div>
        <h5>{{ action.title }}</h5>
        <p class="action-desc">{{ action.description }}</p>
        <div style="margin-top: auto; display: flex; justify-content: space-between; font-size: 0.8125rem;">
          <span class="meta">{{ action.cost_level }}</span>
          <span class="action-outcome">{{ action.expected_outcome }}</span>
        </div>
      </div>
    </div>

    <!-- Roadmap and economics: on demand -->
    <DetailDisclosure show-label="See the full week-by-week plan" hide-label="Hide the week-by-week plan">
      <InfographicTreatmentRoadmap />
      <InfographicEconomicImpact />
    </DetailDisclosure>

    <!-- Why this advice (evidence): on demand -->
    <DetailDisclosure show-label="Why this advice? See the evidence" hide-label="Hide the evidence">
      <div v-if="advisoryResult.explainability && advisoryResult.explainability.length" class="explainability-block card-solid">
        <div class="explainability-header">
          <h4>Why the plan looks like this</h4>
        </div>
        <table class="explainability-table">
          <thead>
            <tr>
              <th>Field factor</th>
              <th>What we saw</th>
              <th>How it shaped the plan</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(ev, eIdx) in advisoryResult.explainability" :key="eIdx">
              <td><strong>{{ ev.factor }}</strong></td>
              <td>{{ ev.observation }}</td>
              <td class="font-editorial-italic">"{{ ev.impact_on_decision }}"</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="advisoryResult.rag_sources && advisoryResult.rag_sources.length" style="margin-top: 16px; padding: 16px;" class="card-solid">
        <span class="meta" style="font-weight: 700; display: block; margin-bottom: 8px;">Source research (ICAR):</span>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          <span v-for="src in advisoryResult.rag_sources" :key="src.id" class="badge-institutional badge-slate">
            {{ src.topic }} ({{ src.region || 'National' }})
          </span>
        </div>
      </div>
    </DetailDisclosure>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import InfographicTreatmentRoadmap from '../InfographicTreatmentRoadmap.vue'
import InfographicEconomicImpact from '../InfographicEconomicImpact.vue'
import DetailDisclosure from './DetailDisclosure.vue'

defineProps({
  advisoryResult: { type: Object, default: null }
})

const showEn = ref(false)
</script>