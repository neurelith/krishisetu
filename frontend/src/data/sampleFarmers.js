// Three contrasting farmer personas used by the empty state to seed the form.
// They cover the device/literacy/connectivity matrix so the demo immediately
// shows different channel + content recommendations.

export const sampleFarmers = [
  {
    id: 'priya-smartphone',
    label: 'Priya · smartphone, high value',
    description: 'WhatsApp-ready, English/Hindi bilingual, large farm.',
    farmer_name: 'Priya Sharma',
    farmer: {
      grower_id: 'GRW_DEMO_01',
      state: 'Punjab',
      district: 'Patiala',
      tehsil_block: 'Rajpura',
      language: 'Punjabi',
      main_crop: 'wheat',
      campaign_product: 'Tilt 250 EC',
      pest_threat: 'rust',
      weather_risk: 'humidity',
      device_type: 'smartphone',
      connectivity: 'good',
      literacy_level: 'high',
      grower_farm_size: 6.5,
      high_value_farmer: true
    }
  },
  {
    id: 'rajesh-keypad',
    label: 'Rajesh · keypad phone, low literacy',
    description: 'Voice-first follow-up, Hindi, weak connectivity.',
    farmer_name: 'Rajesh Yadav',
    farmer: {
      grower_id: 'GRW_DEMO_02',
      state: 'Uttar Pradesh',
      district: 'Kanpur Nagar',
      tehsil_block: 'Bilhaur',
      language: 'Hindi',
      main_crop: 'mustard',
      campaign_product: 'Score 250 EC',
      pest_threat: 'aphids',
      weather_risk: 'dry spell',
      device_type: 'keypad_phone',
      connectivity: 'weak',
      literacy_level: 'low',
      grower_farm_size: 1.2,
      high_value_farmer: false
    }
  },
  {
    id: 'lakshmi-feature',
    label: 'Lakshmi · feature phone, medium farm',
    description: 'SMS-safe Tamil, mid literacy, moderate value.',
    farmer_name: 'Lakshmi Iyer',
    farmer: {
      grower_id: 'GRW_DEMO_03',
      state: 'Tamil Nadu',
      district: 'Thanjavur',
      tehsil_block: 'Kumbakonam',
      language: 'Tamil',
      main_crop: 'rice',
      campaign_product: 'Amistar 250 SC',
      pest_threat: 'blast',
      weather_risk: 'rain',
      device_type: 'feature_phone',
      connectivity: 'good',
      literacy_level: 'medium',
      grower_farm_size: 2.8,
      high_value_farmer: false
    }
  }
]
