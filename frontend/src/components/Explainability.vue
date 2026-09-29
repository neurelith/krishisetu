<template>
  <article class="panel">
    <div class="panel-head">
      <RadioTower :size="20" aria-hidden="true" />
      <h2>Why this recommendation</h2>
    </div>

    <div class="reason-groups">
      <section v-if="result.engagement_reasoning?.length">
        <h3>Engagement signal</h3>
        <ul>
          <li v-for="item in result.engagement_reasoning" :key="`eng-${item}`">{{ item }}</li>
        </ul>
      </section>

      <section v-if="result.channel?.rationale?.length">
        <h3>Channel choice</h3>
        <ul>
          <li v-for="item in result.channel.rationale" :key="`ch-${item}`">{{ item }}</li>
        </ul>
      </section>

      <section v-if="result.urgency?.urgency_reasons?.length">
        <h3>Urgency</h3>
        <ul>
          <li v-for="item in result.urgency.urgency_reasons" :key="`urg-${item}`">{{ item }}</li>
        </ul>
      </section>

      <section v-if="result.rag?.advisory_summary">
        <h3>Agronomy advisory</h3>
        <p class="advisory">{{ result.rag.advisory_summary }}</p>
        <div v-if="result.rag.sources?.length" class="sources">
          <span v-for="(source, i) in result.rag.sources" :key="`src-${i}`">
            {{ source.crop ? `${source.crop} · ` : '' }}{{ source.topic || source.title || 'source' }}
          </span>
        </div>
      </section>
    </div>
  </article>
</template>

<script setup>
import { RadioTower } from 'lucide-vue-next'

defineProps({
  result: { type: Object, required: true }
})
</script>
