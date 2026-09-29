<template>
  <form class="panel form" novalidate @submit.prevent="onSubmit">
    <div class="panel-head">
      <Sprout :size="20" aria-hidden="true" />
      <h2>Farmer context</h2>
      <button
        type="button"
        class="link-btn"
        :disabled="loading"
        @click="$emit('reset')"
      >
        Reset
      </button>
    </div>

    <!-- Sync Toggle Option -->
    <div class="sync-option-wrapper">
      <label class="premium-toggle">
        <input type="checkbox" v-model="targetActiveFarmer" />
        <span class="toggle-slider"></span>
        <span class="toggle-label">Link to active onboarding farmer profile</span>
      </label>
      <div v-if="targetActiveFarmer" class="connected-badge animate-fade-in">
        📡 Linked: <strong>{{ activeFarmerName }}</strong> ({{ activeFarmerId }})
      </div>
    </div>

    <div class="grid two">
      <label>
        <span>Farmer name</span>
        <input v-model="state.farmer_name" autocomplete="off" />
      </label>
      <label>
        <span>Grower ID</span>
        <input v-model="state.farmer.grower_id" autocomplete="off" />
      </label>

      <label :class="{ invalid: errors.state }">
        <span>State <em aria-hidden="true">*</em></span>
        <input
          v-model="state.farmer.state"
          required
          :aria-invalid="!!errors.state"
          @input="clearError('state')"
        />
        <small v-if="errors.state" class="field-error">{{ errors.state }}</small>
      </label>
      <label :class="{ invalid: errors.district }">
        <span>District <em aria-hidden="true">*</em></span>
        <input
          v-model="state.farmer.district"
          required
          :aria-invalid="!!errors.district"
          @input="clearError('district')"
        />
        <small v-if="errors.district" class="field-error">{{ errors.district }}</small>
      </label>

      <label>
        <span>Tehsil / block</span>
        <input v-model="state.farmer.tehsil_block" />
      </label>
      <label>
        <span>Season</span>
        <input v-model="state.farmer.season" placeholder="Kharif / Rabi / Zaid" />
      </label>

      <label>
        <span>Language</span>
        <select v-model="state.farmer.language">
          <option value="">Infer from region</option>
          <option>Hindi</option>
          <option>Tamil</option>
          <option>Telugu</option>
          <option>Marathi</option>
          <option>Punjabi</option>
          <option>Gujarati</option>
          <option>Kannada</option>
          <option>English</option>
        </select>
      </label>
      <label :class="{ invalid: errors.main_crop }">
        <span>Crop <em aria-hidden="true">*</em></span>
        <input
          v-model="state.farmer.main_crop"
          required
          :aria-invalid="!!errors.main_crop"
          @input="clearError('main_crop')"
        />
        <small v-if="errors.main_crop" class="field-error">{{ errors.main_crop }}</small>
      </label>

      <label>
        <span>Product</span>
        <input v-model="state.farmer.campaign_product" placeholder="e.g. Tilt 250 EC" />
      </label>
      <label :class="{ invalid: errors.pest_threat }">
        <span>Pest / disease <em aria-hidden="true">*</em></span>
        <input
          v-model="state.farmer.pest_threat"
          required
          :aria-invalid="!!errors.pest_threat"
          @input="clearError('pest_threat')"
        />
        <small v-if="errors.pest_threat" class="field-error">{{ errors.pest_threat }}</small>
      </label>

      <label>
        <span>Weather risk</span>
        <input v-model="state.farmer.weather_risk" placeholder="rain, dry spell, humidity" />
      </label>
      <label>
        <span>Farm size (acres)</span>
        <input
          v-model.number="state.farmer.grower_farm_size"
          type="number"
          min="0"
          step="0.1"
        />
      </label>

      <label>
        <span>Device</span>
        <select v-model="state.farmer.device_type">
          <option value="smartphone">Smartphone</option>
          <option value="keypad_phone">Keypad phone</option>
          <option value="feature_phone">Feature phone</option>
        </select>
      </label>
      <label>
        <span>Connectivity</span>
        <select v-model="state.farmer.connectivity">
          <option value="good">Good</option>
          <option value="weak">Weak</option>
          <option value="offline">Offline</option>
        </select>
      </label>

      <label>
        <span>Literacy</span>
        <select v-model="state.farmer.literacy_level">
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </label>
      <label class="check">
        <input
          v-model="state.farmer.high_value_farmer"
          type="checkbox"
        />
        <span>High-value farmer · add voice follow-up</span>
      </label>
    </div>

    <button class="primary" :disabled="loading">
      <Send :size="18" aria-hidden="true" />
      <span>{{ loading ? 'Generating campaign…' : 'Generate campaign' }}</span>
    </button>
  </form>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { Sprout, Send } from 'lucide-vue-next'
import { useRealtimeSync } from '../composables/useRealtimeSync'

const props = defineProps({
  state: { type: Object, required: true },
  errors: { type: Object, required: true },
  loading: { type: Boolean, default: false }
})
const emit = defineEmits(['submit', 'reset', 'clear-error'])

const sync = useRealtimeSync()
const targetActiveFarmer = ref(false)

const activeFarmerName = sync.activeFarmerName
const activeFarmerId = sync.activeFarmerGrowerId

function clearError(key) {
  emit('clear-error', key)
}
function onSubmit() {
  emit('submit')
}

const fillFromActiveFarmer = () => {
  if (!targetActiveFarmer.value) return
  
  const cropRaw = sync.activeFarmerCrop.value || ''
  const cropClean = cropRaw.replace(/[^a-zA-Z\s]/g, '').trim()

  const locRaw = sync.activeFarmerLocation.value || ''
  const parts = locRaw.split('·')
  const stateVal = parts[0]?.trim() || ''
  const distVal = parts[1]?.trim() || ''

  let sizeVal = null
  const sizeRaw = sync.activeFarmerSize.value || ''
  if (sizeRaw.includes('Under 2')) sizeVal = 1.5
  else if (sizeRaw.includes('2–5')) sizeVal = 3.5
  else if (sizeRaw.includes('5–10')) sizeVal = 7.5
  else if (sizeRaw.includes('10+')) sizeVal = 12.0

  props.state.farmer_name = sync.activeFarmerName.value
  props.state.farmer.grower_id = sync.activeFarmerGrowerId.value
  props.state.farmer.state = stateVal
  props.state.farmer.district = distVal
  props.state.farmer.main_crop = cropClean
  props.state.farmer.grower_farm_size = sizeVal
  props.state.farmer.language = sync.activeFarmerLanguage.value

  if (!props.state.farmer.pest_threat) {
    if (cropClean.toLowerCase() === 'wheat') props.state.farmer.pest_threat = 'Powdery Mildew'
    else if (cropClean.toLowerCase() === 'maize') props.state.farmer.pest_threat = 'Fall Armyworm'
    else if (cropClean.toLowerCase() === 'mustard') props.state.farmer.pest_threat = 'Aphids'
    else if (cropClean.toLowerCase() === 'potato') props.state.farmer.pest_threat = 'Late Blight'
    else props.state.farmer.pest_threat = 'Pest threat'
  }
  
  if (!props.state.farmer.campaign_product) {
    if (cropClean.toLowerCase() === 'wheat') props.state.farmer.campaign_product = 'Topik 15 WP'
    else if (cropClean.toLowerCase() === 'maize') props.state.farmer.campaign_product = 'Ampligo'
    else if (cropClean.toLowerCase() === 'mustard') props.state.farmer.campaign_product = 'Actara 25 WG'
    else if (cropClean.toLowerCase() === 'potato') props.state.farmer.campaign_product = 'Revus'
  }
  
  clearError('state')
  clearError('district')
  clearError('main_crop')
  clearError('pest_threat')
}

watch(targetActiveFarmer, (val) => {
  if (val) {
    fillFromActiveFarmer()
  }
})

watch(
  [sync.activeFarmerName, sync.activeFarmerLanguage, sync.activeFarmerCrop, sync.activeFarmerLocation, sync.activeFarmerSize, sync.activeFarmerGrowerId],
  () => {
    if (targetActiveFarmer.value) {
      fillFromActiveFarmer()
    }
  }
)

onUnmounted(() => {
  sync.destroy()
})
</script>

<style scoped>
.sync-option-wrapper {
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.premium-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: var(--slate-700);
  user-select: none;
}
.premium-toggle input {
  display: none;
}
.toggle-slider {
  position: relative;
  width: 36px;
  height: 20px;
  background-color: var(--slate-300);
  border-radius: 20px;
  transition: background-color 0.3s;
}
.toggle-slider::before {
  content: '';
  position: absolute;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background-color: white;
  top: 3px;
  left: 3px;
  transition: transform 0.3s;
}
.premium-toggle input:checked + .toggle-slider {
  background-color: var(--emerald-600);
}
.premium-toggle input:checked + .toggle-slider::before {
  transform: translateX(16px);
}
.connected-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--emerald-800);
  background-color: var(--emerald-50);
  border: 1px solid var(--emerald-100);
  padding: 4px 10px;
  border-radius: 6px;
  align-self: flex-start;
  font-weight: 500;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.2s ease forwards;
}
</style>
