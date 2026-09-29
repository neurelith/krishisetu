<template>
  <section class="profile-ribbon-slim">
    <div class="profile-left">
      <div class="profile-badge-frame">
        <PhUser :size="20" weight="bold" />
      </div>
      <div>
        <div class="farmer-title-row">
          <h1><span v-text="context.farmer.name"></span></h1>
          <span class="badge-institutional badge-forest">
            <span v-text="context.location.district"></span>, <span v-text="context.location.state"></span>
          </span>
          <span class="badge-institutional badge-slate">ID: <span v-text="context.farmer.farmer_id"></span></span>
        </div>
        <p class="farmer-meta-line">
          Crop: <strong v-text="context.crop.name"></strong> (<span v-text="context.crop.variety"></span>) · Growth Stage: <em><span v-text="context.crop.crop_stage"></span></em> · Day <span v-text="context.crop.days_since_sowing"></span> Post-Sowing
        </p>
      </div>
    </div>

    <div class="profile-actions">
      <!-- Language Selector -->
      <div class="lang-selector-group">
        <PhGlobe :size="18" weight="bold" />
        <label for="farmer-preferred-lang" class="selector-label">Language:</label>
        <select 
          id="farmer-preferred-lang" 
          aria-label="Advisory Language" 
          v-model="context.farmer.preferred_language" 
          @change="$emit('language-change')" 
          class="lang-dropdown"
        >
          <option value="bn">Bengali (বাংলা)</option>
          <option value="hi">Hindi (हिन्दी)</option>
          <option value="en">English (Global)</option>
        </select>
      </div>
    </div>
  </section>
</template>

<script setup>
import { PhUser, PhGlobe } from '@phosphor-icons/vue'

defineProps({
  context: {
    type: Object,
    required: true
  }
})

defineEmits(['language-change'])
</script>
