<template>
  <div class="kisan-sathi-container">
    <!-- Offline Resiliency Notice -->
    <div v-if="!isOnline" class="offline-banner">
      <div class="banner-marker"></div>
      <div class="banner-body">
        <strong>Offline Resiliency Active:</strong>
        <span>Previously saved guidance may be available offline. New image diagnoses and advisories require a connection.</span>
      </div>
      <span class="badge-institutional badge-slate">IndexedDB Local Cache</span>
    </div>

    <!-- Farmer Identity & Agro-Ecological Node Header -->
    <section class="profile-ribbon card-solid">
      <div class="profile-left">
        <div class="profile-badge-frame">
          <svg class="svg-icon-lg" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
          </svg>
        </div>
        <div>
          <div class="farmer-title-row">
            <h1><span v-text="currentContext.farmer.name || 'Your farm'"></span></h1>
            <span class="badge-institutional badge-forest">{{ [currentContext.location.district, currentContext.location.state].filter(Boolean).join(', ') || 'Location not set' }}</span>
          </div>
          <p class="farmer-meta-line">
            Crop: <strong>{{ currentContext.crop.name || 'Not set' }}</strong><span v-if="currentContext.crop.variety"> ({{ currentContext.crop.variety }})</span> · Growth stage: <em>{{ currentContext.crop.crop_stage || 'Not set' }}</em>
          </p>
        </div>
      </div>

      <div class="profile-actions">
        <button type="button" @click="refreshTelemetry" class="btn-gov-outline" :disabled="loadingTelemetry || currentContext.location.latitude == null || currentContext.location.longitude == null">
          <svg class="svg-icon" :class="{ 'spin': loadingTelemetry }" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
          </svg>
          <span>Sync Environmental Telemetry</span>
        </button>
      </div>
    </section>

    <section class="farmer-context-card card-solid">
      <div class="context-heading">
        <div>
          <h2>Your crop and location</h2>
          <p>These details accompany your image and are used to tailor the advisory.</p>
        </div>
        <span class="badge-institutional badge-slate">Farm context</span>
      </div>
      <div class="farmer-context-grid">
        <label>
          <span>Crop</span>
          <input v-model="currentContext.crop.name" autocomplete="off" placeholder="e.g. Rice" @input="onFarmContextChanged" />
        </label>
        <label>
          <span>Variety (optional)</span>
          <input v-model="currentContext.crop.variety" autocomplete="off" placeholder="e.g. Swarna" @input="onFarmContextChanged" />
        </label>
        <label>
          <span>State</span>
          <input v-model="currentContext.location.state" autocomplete="address-level1" placeholder="Your state" @input="onFarmContextChanged" />
        </label>
        <label>
          <span>District</span>
          <input v-model="currentContext.location.district" autocomplete="address-level2" placeholder="Your district" @input="onFarmContextChanged" />
        </label>
        <label>
          <span>Growth stage</span>
          <input v-model="currentContext.crop.crop_stage" autocomplete="off" placeholder="e.g. Flowering" @input="onFarmContextChanged" />
        </label>
        <label>
          <span>Advisory language</span>
          <select v-model="currentContext.farmer.preferred_language" @change="onFarmContextChanged">
            <option value="bn">Bengali (বাংলা)</option>
            <option value="hi">Hindi (हिन्दी)</option>
            <option value="en">English</option>
          </select>
        </label>
      </div>
    </section>

    <!-- Unified Agro-Meteorological & Spectral Operations Matrix -->
    <section class="telemetry-operations-matrix card-solid">
      <div class="matrix-head">
        <div class="matrix-title">
          <svg class="svg-icon text-forest" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5" />
          </svg>
          <h2>Environmental telemetry</h2>
        </div>
        <div class="matrix-sync-tag">
          <span class="live-dot"></span>
          <span>Sample baselines · not linked to a farm record</span>
        </div>
      </div>

      <div class="matrix-grid">
        <!-- Stream 1: Agro-Weather (Open-Meteo) -->
        <div class="matrix-column">
          <div class="column-header">
            <span class="station-provenance">Agro-Meteorology · sample baseline</span>
            <h3>Atmospheric Microclimate</h3>
            <span class="source-tag">Sample values · refresh requires farm coordinates</span>
          </div>

          <!-- Humidity Visual Warning Range Meter -->
          <div class="telemetry-gauge-card highlight-gauge-alert">
            <div class="gauge-header">
              <span class="gauge-label">Relative Humidity & Pathogen Risk</span>
              <span class="gauge-value text-alert"><span v-text="currentContext.weather.relative_humidity_pct"></span>% (Elevated)</span>
            </div>
            <div class="gauge-track-container">
              <div class="gauge-bar-track">
                <div class="gauge-fill-bar gauge-fill-alert" :style="{ width: currentContext.weather.relative_humidity_pct + '%' }"></div>
                <div class="gauge-threshold-marker marker-rh-82" title="Fungal Sporulation Threshold (82%)"></div>
              </div>
              <div class="gauge-ticks-row">
                <span>0% Safe</span>
                <span class="threshold-label">82% Threshold</span>
                <span>100% Saturation</span>
              </div>
            </div>
          </div>

          <!-- Tabular Dual Metrics -->
          <div class="metrics-tabular">
            <div class="metric-row">
              <span class="metric-key">Ambient Temperature</span>
              <span class="metric-val"><span v-text="currentContext.weather.temperature_c"></span>°C</span>
            </div>
            <div class="metric-row">
              <span class="metric-key">7-Day Rainfall Forecast</span>
              <span class="metric-val"><span v-text="currentContext.weather.rainfall_forecast_7d_mm"></span> mm</span>
            </div>
            <div class="metric-row">
              <span class="metric-key">24-Hour Precipitation</span>
              <span class="metric-val"><span v-text="currentContext.weather.rainfall_last_24h_mm"></span> mm</span>
            </div>
          </div>

          <div class="stream-risk-note">
            <span class="risk-label">Microclimate Diagnostic:</span>
            <p class="font-editorial-italic" v-text="currentContext.weather.microclimate_risk"></p>
          </div>
        </div>

        <!-- Stream 2: Soil Health Card (GOI SHC) -->
        <div class="matrix-column border-left-divider">
          <div class="column-header">
            <span class="station-provenance">Soil metrics · sample baseline</span>
            <h3>Soil Fertility Matrix (SHC)</h3>
            <span class="source-tag">Sample soil values · not a farmer health card</span>
          </div>

          <!-- Soil Reaction pH Range Gauge -->
          <div class="telemetry-gauge-card">
            <div class="gauge-header">
              <span class="gauge-label">Soil Reaction (pH Balance)</span>
              <span class="gauge-value text-alert"><span v-text="currentContext.soil_health.ph"></span> (Acidic)</span>
            </div>
            <div class="gauge-track-container">
              <div class="gauge-bar-track">
                <div class="gauge-fill-bar gauge-fill-ph" :style="{ width: ((currentContext.soil_health.ph / 14) * 100) + '%' }"></div>
                <div class="gauge-threshold-marker marker-ph-neutral" title="Neutral Target (pH 7.0)"></div>
              </div>
              <div class="gauge-ticks-row">
                <span>0 Acidic</span>
                <span class="threshold-label">7.0 Neutral</span>
                <span>14 Alkaline</span>
              </div>
            </div>
          </div>

          <!-- N-P-K Nutrient Status Bars -->
          <div class="npk-tri-deck">
            <div class="npk-item">
              <div class="npk-head">
                <span class="npk-name">Nitrogen (N)</span>
                <span class="npk-val text-alert"><span v-text="currentContext.soil_health.nitrogen_kg_ha"></span> kg/ha (Low)</span>
              </div>
              <div class="npk-bar-track">
                <div class="npk-bar-fill fill-low fill-n-35"></div>
              </div>
            </div>
            <div class="npk-item">
              <div class="npk-head">
                <span class="npk-name">Phosphorus (P)</span>
                <span class="npk-val text-alert"><span v-text="currentContext.soil_health.phosphorus_kg_ha"></span> kg/ha (Low)</span>
              </div>
              <div class="npk-bar-track">
                <div class="npk-bar-fill fill-low fill-p-28"></div>
              </div>
            </div>
            <div class="npk-item">
              <div class="npk-head">
                <span class="npk-name">Potassium (K)</span>
                <span class="npk-val text-forest"><span v-text="currentContext.soil_health.potassium_kg_ha"></span> kg/ha (Moderate)</span>
              </div>
              <div class="npk-bar-track">
                <div class="npk-bar-fill fill-mod fill-k-62"></div>
              </div>
            </div>
          </div>

          <div class="deficiency-chips-row">
            <span v-for="(def, idx) in currentContext.soil_health.deficiencies" :key="idx" class="badge-institutional badge-soil">
              {{ def }}
            </span>
          </div>

          <div class="stream-risk-note">
            <span class="risk-label">Pedological Assessment:</span>
            <p class="font-editorial-italic">"Acidic soil matrix reduces bio-available phosphate; organic carbon depletion requires organic matter restitution."</p>
          </div>
        </div>

        <!-- Stream 3: Satellite NDVI (Copernicus Sentinel-2) -->
        <div class="matrix-column border-left-divider">
          <div class="column-header">
            <span class="station-provenance">Satellite metrics · sample baseline</span>
            <h3>Orbital Spectral Telemetry</h3>
            <span class="source-tag">Sample spectral values · no satellite fetch</span>
          </div>

          <!-- Vegetative Vigor Chlorophyll Spectrum Gauge -->
          <div class="telemetry-gauge-card highlight-gauge-forest">
            <div class="gauge-header">
              <span class="gauge-label">Canopy Vegetative Vigor (NDVI)</span>
              <span class="gauge-value text-forest font-bold">{{ currentContext.satellite.ndvi }} (Dense Canopy)</span>
            </div>
            <div class="gauge-track-container">
              <div class="gauge-bar-track spectrum-gradient-track">
                <div class="spectrum-pin" :style="{ left: (currentContext.satellite.ndvi * 100) + '%' }"></div>
              </div>
              <div class="gauge-ticks-row">
                <span>0.0 Fallow</span>
                <span>0.5 Emergence</span>
                <span>1.0 Full Canopy</span>
              </div>
            </div>
          </div>

          <div class="metrics-tabular">
            <div class="metric-row">
              <span class="metric-key">Surface Soil Moisture Index</span>
              <span class="metric-val" v-text="currentContext.satellite.soil_moisture_index"></span>
            </div>
            <div class="metric-row">
              <span class="metric-key">Cloud Cover Mask</span>
              <span class="metric-val"><span v-text="currentContext.satellite.cloud_cover_pct"></span>%</span>
            </div>
          </div>

          <!-- Mathematical Spectral Provenance Box -->
          <div class="provenance-technical-box">
            <div class="formula-technical-row">
              <code v-text="currentContext.satellite.spectral_formula || 'NDVI = (B08_NIR - B04_Red) / (B08_NIR + B04_Red)'"></code>
            </div>
            <div class="granule-technical-row">
              <span>Granule:</span>
              <code class="granule-code" v-text="currentContext.satellite.tile_reference || 'S2A_MSIL2A_20260924_T45QXE_R061'"></code>
            </div>
          </div>

          <div class="stream-risk-note">
            <span class="risk-label">Canopy Reflectance Assessment:</span>
            <p class="font-editorial-italic">"Sentinel-2 MSI Level-2A canopy reflectance indicates robust vegetative vigor across 10m grid cell."</p>
          </div>
        </div>
      </div>

      <!-- Integrated Atmospheric & Spray Drift Infographic Deck -->
      <InfographicTelemetryRadar />
    </section>

    <!-- Stage 3: Clinical Diagnostic Laboratory Stage (Balanced 2-Column Grid) -->
    <div class="diagnostic-lab-grid">
      
      <!-- Panel 1: Field Specimen Intake & Multi-Modal Console -->
      <section class="diagnostic-intake-card card-solid">
        <div class="section-header-row">
          <div>
            <h2>Specimen Intake & Observational Console</h2>
            <p class="section-sub">Multimodal Foliage Specimen + Indic Speech Transcription</p>
          </div>
          <span class="badge-institutional badge-forest">Field Intake</span>
        </div>

        <div class="benchmark-controls">
          <button type="button" class="btn-gov-outline" @click="showBenchmarks = !showBenchmarks">
            {{ showBenchmarks ? 'Hide Demo / Benchmark' : 'Demo / Benchmark' }}
          </button>
          <p v-if="showBenchmarks" class="benchmark-note">Sample images and prewritten outputs for demonstration only. They are not diagnoses of your crop.</p>
        </div>

        <!-- Explicit demo / benchmark selector -->
        <div v-if="showBenchmarks" class="specimen-selector-bar">
          <span class="selector-subheading">Choose a sample benchmark:</span>
          <div class="segmented-specimen-group">
            <button 
              @click="selectAndRunBenchmark('rice')" 
              class="specimen-tab-btn" 
              :class="{ active: selectedSample === 'rice' }"
              type="button"
            >
              <span class="crop-indicator indicator-rice"></span>
              <span>Rice: Sheath Blight</span>
            </button>
            <button 
              @click="selectAndRunBenchmark('wheat')" 
              class="specimen-tab-btn" 
              :class="{ active: selectedSample === 'wheat' }"
              type="button"
            >
              <span class="crop-indicator indicator-wheat"></span>
              <span>Wheat: Yellow Rust</span>
            </button>
            <button 
              @click="selectAndRunBenchmark('cotton')" 
              class="specimen-tab-btn" 
              :class="{ active: selectedSample === 'cotton' }"
              type="button"
            >
              <span class="crop-indicator indicator-cotton"></span>
              <span>Cotton: Bollworm</span>
            </button>
            <button 
              @click="selectAndRunBenchmark('invalid_dog')" 
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
              accept="image/jpeg,image/png,image/webp"
              capture="environment"
              class="hidden-input-element" 
              aria-label="Specimen leaf photo upload"
              tabindex="-1"
            />
            <!-- Corner Optical Reticles -->
            <div class="reticle-corner reticle-tl"></div>
            <div class="reticle-corner reticle-tr"></div>
            <div class="reticle-corner reticle-bl"></div>
            <div class="reticle-corner reticle-br"></div>
            <div class="reticle-crosshair"></div>

            <img v-if="previewImage" :src="previewImage" :alt="isDemoResult ? 'Sample benchmark image' : 'Selected crop image preview'" width="480" height="320" class="specimen-rendered-image" />
            <div v-else class="specimen-empty-state">
              <strong>Take or upload a crop photo</strong>
              <span>Tap here to open your camera or choose an image.</span>
            </div>
            <div class="viewfinder-overlay">
              <div class="viewfinder-tag">
                <span class="tag-dot"></span>
                <span>{{ selectedFileName || 'No image selected' }}</span>
                <span v-if="isDemoResult" class="reticle-telemetry">SAMPLE</span>
              </div>
              <button @click.stop="triggerFileInput" class="btn-change-photo" type="button">
                <svg class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
                </svg>
                <span>{{ previewImage ? 'Choose another photo' : 'Take or upload photo' }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Farmer Voice Observation Console with Audio Frequency Equalizer -->
        <div class="voice-intake-card">
          <div class="voice-intake-header">
            <span class="voice-intake-title">Farmer Spoken Observation (Indic STT)</span>
            <span class="badge-institutional badge-slate"><span v-text="getLangName(currentContext.farmer.preferred_language)"></span></span>
          </div>
          <div class="voice-action-row">
            <button @click.stop="toggleVoiceRecording" class="btn-voice-record" :class="{ 'is-active-recording': isRecording }" type="button">
              <svg class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15a3 3 0 01-3-3V4.5a3 3 0 116 0v7.5a3 3 0 01-3 3z" />
              </svg>
              <span>{{ isRecording ? 'Listening (Speak observation)...' : 'Record Voice Observation' }}</span>
              <div v-if="isRecording" class="audio-wave-visualizer">
                <span class="wave-bar bar-1"></span>
                <span class="wave-bar bar-2"></span>
                <span class="wave-bar bar-3"></span>
                <span class="wave-bar bar-4"></span>
                <span class="wave-bar bar-5"></span>
              </div>
            </button>
            <button v-if="voiceTranscript" @click="voiceTranscript = ''; currentContext.farmer.voice_observation = ''" class="btn-gov-outline btn-compact" type="button">
              Clear
            </button>
          </div>
          <div v-if="voiceTranscript" class="transcript-box">
            <span class="transcript-lead">Recorded Clinical Transcript:</span>
            <p class="transcript-quote font-editorial-italic">"{{ voiceTranscript }}"</p>
          </div>
          <p v-else class="voice-hint font-editorial-italic">
            Voice transcription is optional and is not currently included in the diagnosis request.
          </p>
        </div>

        <!-- Action Execution Button -->
        <div class="diagnose-actions">
          <button 
            @click="runDiagnosis" 
            class="btn-gov-primary btn-execute-diagnosis w-full justify-center" 
            :disabled="isDiagnosing || !selectedFileBlob || !isContextReady || isDemoResult || !isOnline"
            type="button"
          >
            <svg v-if="isDiagnosing" class="svg-icon spin" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
            <svg v-else class="svg-icon" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
            <span>{{ isDiagnosing ? 'Analyzing crop image...' : 'Diagnose crop image' }}</span>
          </button>
        </div>

        <!-- Specimen Technical Metadata -->
        <div class="specimen-tech-bar">
          <span>Image is sent to the KrishiSetu diagnosis API for analysis.</span>
          <span>Use the result as decision support, not a confirmed diagnosis.</span>
        </div>
      </section>

      <!-- Panel 2: Verified Diagnostic Pathology & Immediate Bio-Action (Peer to Intake Card) -->
      <section class="diagnostic-evaluation-card card-solid">
        <div class="section-header-row">
          <div>
            <h2>Image assessment and next steps</h2>
            <p class="section-sub">Model-generated result · review with a local agricultural expert</p>
          </div>
          <span class="badge-institutional badge-sky">Laboratory Output</span>
        </div>

        <div v-if="isDemoResult" class="benchmark-result-notice">
          Sample benchmark output. This is not a diagnosis of your image or farm.
        </div>
        <div v-if="diagnosisError" class="diagnosis-error-notice" role="alert">
          {{ diagnosisError }}
        </div>
        <div v-if="advisoryError" class="diagnosis-error-notice" role="alert">
          Advisory unavailable: {{ advisoryError }}
        </div>
        <div v-if="advisoryResult && !isDemoResult && advisoryResult.status !== 'success'" class="diagnosis-unavailable" role="status">
          <h3>{{ advisoryResult.status === 'uncertain' ? 'Advisory uncertain' : 'Advisory unavailable' }}</h3>
          <p>{{ advisoryResult.summary_advisory || 'No treatment recommendations are available.' }}</p>
        </div>

        <!-- Skeleton Loader for Loading State -->
        <div v-if="isDiagnosing" class="diagnostic-skeleton-card">
          <div class="skeleton-block skeleton-shimmer h-8 w-3-4 mb-3"></div>
          <div class="skeleton-block skeleton-shimmer h-4 w-1-2 mb-4"></div>
          <div class="skeleton-block skeleton-shimmer h-12 w-full mb-3"></div>
          <div class="skeleton-block skeleton-shimmer h-24 w-full mb-3"></div>
          <div class="skeleton-block skeleton-shimmer h-20 w-full"></div>
        </div>

        <div v-else-if="diagnosisResult && diagnosisResult.diagnosis_status === 'unavailable'" class="diagnosis-unavailable" role="status">
          <h3>Diagnosis unavailable</h3>
          <p>{{ diagnosisResult.rejection_reason || 'The image could not be analyzed. Check your connection and try again with a clear crop photo.' }}</p>
        </div>

        <div v-else-if="diagnosisResult && diagnosisResult.diagnosis_status === 'uncertain'" class="diagnosis-unavailable" role="status">
          <h3>Uncertain image assessment</h3>
          <p>No disease was identified with enough confidence to provide a diagnosis or advisory. Try a clear, close-up photo and consult a local agricultural expert.</p>
        </div>

        <!-- Guardrail Alert (Rejection of Non-Agricultural / Non-Crop Input) -->
        <div v-else-if="diagnosisResult && !diagnosisResult.is_valid_crop_image" class="guardrail-alert-box">
          <div class="alert-icon-frame">
            <svg class="svg-icon text-alert" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
            </svg>
          </div>
          <div>
            <h3 class="guardrail-title">This image could not be assessed as a crop</h3>
            <p v-text="diagnosisResult.rejection_reason"></p>
            <span class="guardrail-sub">Model: <span v-text="diagnosisResult.model_used"></span></span>
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
            <!-- Precision Certainty Gauge -->
            <div class="diag-match-badge">
              <div class="match-score-row">
                <span class="match-percentage">{{ Math.round(diagnosisResult.confidence * 100) }}%</span>
                <div class="certainty-segments" :title="`Model-reported confidence: ${Math.round(diagnosisResult.confidence * 100)}%`">
                  <span v-for="segment in 5" :key="segment" class="segment" :class="{ active: segment <= Math.round(diagnosisResult.confidence * 5) }"></span>
                </div>
              </div>
              <span class="match-label">Model-reported confidence</span>
            </div>
          </div>

          <div class="diag-attribute-strip">
            <span class="badge-institutional badge-soil">Severity: <span v-text="diagnosisResult.severity"></span></span>
            <span class="badge-institutional badge-slate">Tissue: <span v-text="diagnosisResult.affected_part"></span></span>
            <span class="badge-institutional badge-forest" v-text="diagnosisResult.model_used"></span>
          </div>

          <!-- Observed Pathology Markers in Clinical Table Checklist -->
          <div class="markers-block">
            <h4>Observed Clinical Symptoms:</h4>
            <div class="symptoms-clinical-grid">
              <div v-for="(sym, sIdx) in diagnosisResult.symptoms" :key="sIdx" class="symptom-tag-item">
                <span class="symptom-pip"></span>
                <span>{{ sym }}</span>
              </div>
            </div>
          </div>

          <!-- Immediate Emergency Bio-Control Action -->
          <div class="protective-step-box">
            <span class="step-title">Immediate Emergency Bio-Agronomic Action:</span>
            <p v-text="diagnosisResult.immediate_bio_action"></p>
          </div>

          <!-- Bottom Status Strip -->
          <div class="lab-provenance-strip">
            <span>Assessment: <strong>{{ isDemoResult ? 'Sample benchmark' : 'Gemini model output' }}</strong></span>
            <span>Confidence: <strong>Model-reported, not calibrated</strong></span>
          </div>
        </div>

        <!-- Fallback Ready State for Lab Stage -->
        <div v-else class="lab-readiness-state">
          <h3>Pathology Lab Engine Ready</h3>
          <p>Select a clinical specimen or upload foliage to evaluate cellular pathology markers.</p>
        </div>
      </section>

    </div>

    <!-- Integrated Biological Pathogen Etiology & Bio-Fungicidal Cycle Infographic -->
    <div v-if="isDemoResult && diagnosisResult && diagnosisResult.is_valid_crop_image" class="post-diagnosis-infographics">
      <InfographicPathogenCycle />
    </div>

    <!-- Stage 4: Comprehensive Regenerative Action Dossier (Full-Width Publication Grade) -->
    <section v-if="advisoryResult && (isDemoResult || advisoryResult.status === 'success') && diagnosisResult?.is_valid_crop_image && diagnosisResult?.diagnosis_status !== 'uncertain'" class="advisory-full-dossier card-solid">
      <!-- Dossier Masthead with Custom Voice Player -->
      <div class="dossier-masthead">
        <div class="masthead-left">
          <div class="dossier-badge-row">
            <span v-if="isDemoResult" class="badge-institutional badge-soil">SAMPLE BENCHMARK</span>
            <span class="badge-institutional badge-forest">Regenerative Advisory Plan</span>
            <span class="badge-institutional badge-slate">Generated from submitted farm context</span>
            <span class="timestamp-tag" v-text="advisoryResult.generated_at"></span>
          </div>
          <h2>Comprehensive agronomic management dossier</h2>
          <p class="section-sub">Multi-Source Synthesis: Gemini Multimodal Vision · ICAR Regenerative Protocols · Sentinel-2 Spectral Fusion</p>
        </div>

        <!-- Custom Indic Voice Broadcast Player Deck -->
        <div v-if="advisoryResult.audio_url" class="custom-audio-broadcast-deck">
          <button type="button" @click="toggleAudioPlayback" class="btn-audio-circle" :aria-label="isPlayingAudio ? 'Pause Voice Advisory' : 'Play Voice Advisory'">
            <svg v-if="!isPlayingAudio" class="audio-svg-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M8 5v14l11-7z" />
            </svg>
            <svg v-else class="audio-svg-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
            </svg>
          </button>
          <div class="audio-track-info">
            <div class="audio-track-top">
              <div class="broadcast-tag">
                <span class="broadcast-pulse" :class="{ 'is-pulsing': isPlayingAudio }"></span>
                <strong>Voice Advisory Broadcast (<span v-text="getLangName(advisoryResult.language)"></span>)</strong>
              </div>
              <span class="audio-time-stamp" v-text="audioTimeDisplay"></span>
            </div>
            <div class="audio-scrub-bar" @click="seekAudio">
              <div class="audio-scrub-fill" :style="{ width: audioProgressPct + '%' }"></div>
            </div>
          </div>
          <audio 
            ref="audioElementRef" 
            :src="resolveMediaUrl(advisoryResult.audio_url)" 
            @timeupdate="onAudioTimeUpdate" 
            @ended="onAudioEnded"
            class="hidden-audio-element"
            tabindex="-1"
          ></audio>
        </div>
      </div>

      <div class="dossier-body-container">
        <!-- Actionable Summary Monograph -->
        <div class="summary-monograph-card">
          <p class="summary-paragraph font-editorial-italic">"<span v-text="advisoryResult.summary_advisory"></span>"</p>
          
          <div v-if="advisoryResult.language !== 'en'" class="translation-drawer">
            <button @click="showEnTranslation = !showEnTranslation" class="btn-text-link" type="button">
              {{ showEnTranslation ? 'Hide English Reference' : 'Display English Translation Reference' }}
            </button>
            <p v-if="showEnTranslation" class="en-translation-text font-editorial-italic">
              "<span v-text="advisoryResult.summary_advisory_en"></span>"
            </p>
          </div>
        </div>

        <!-- The Golden Hero Prescription Anchor (Primary Visual Gravitational Anchor) -->
        <div v-if="isDemoResult" class="golden-prescription-anchor">
          <div class="prescription-masthead">
            <div class="prescription-tag-badge">
              <span class="live-pulse-dot" aria-hidden="true"></span>
              <span class="prescription-tag-text">CRITICAL IMMEDIATE INTERVENTION &bull; STAGE 01 (HOUR 00:00 - 24:00)</span>
            </div>
            <span class="prescription-priority-pill">MANDATORY PROTOCOL</span>
          </div>

          <div class="prescription-content-grid">
            <div class="prescription-main-col">
              <span class="prescription-eyebrow">Immediate Bio-Shield Inoculation</span>
              <h3 class="prescription-hero-title">
                <span v-text="diagnosisResult?.immediate_bio_action || 'Foliar spray of Trichoderma harzianum (2x10^9 CFU/g) @ 5g/L water'"></span>
              </h3>
              <p class="prescription-directive font-editorial-italic">
                Target leaf undersides and lower sheath where humidity accumulates. Apply during calm morning window to occupy leaf phyllosphere before stomatal cuticular breach occurs.
              </p>
              <div class="prescription-contraindication-banner">
                <svg class="contra-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                </svg>
                <span><strong>STRICT BIOLOGICAL COMPATIBILITY:</strong> Do NOT tank-mix with synthetic copper or Mancozeb. Maintain 72h chemical isolation window.</span>
              </div>
            </div>

            <div class="prescription-specs-deck">
              <div class="spec-tile">
                <span class="spec-tile-label">Optimal Application Window</span>
                <strong class="spec-tile-value text-accent-emerald">06:30 &ndash; 09:30 AM</strong>
                <span class="spec-tile-sub">Calm morning inversion &bull; Rel Humidity &gt; 80%</span>
              </div>
              <div class="spec-tile">
                <span class="spec-tile-label">Dispersal Method &amp; Nozzle</span>
                <strong class="spec-tile-value">Knapsack Sprayer</strong>
                <span class="spec-tile-sub">Hollow cone nozzle &bull; Target culm &amp; underside</span>
              </div>
              <div class="spec-tile">
                <span class="spec-tile-label">Direct Farm Input Cost</span>
                <strong class="spec-tile-value text-accent-gold">&sim; &#8377;140 &ndash; &#8377;420 / acre</strong>
                <span class="spec-tile-sub">Low-cost regenerative bio-shield</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Phased Chronological Treatment Roadmap Infographic -->
        <InfographicTreatmentRoadmap v-if="isDemoResult" />

        <!-- Prescribed Regenerative Interventions (Domain-Differentiated Grid) -->
        <div class="interventions-section">
          <div class="section-title-bar">
            <div>
              <h3>Prescribed regenerative interventions and bio-control sequence</h3>
              <span class="section-micro-sub">Categorized biological, pedological, and water microclimate interventions</span>
            </div>
            <span class="badge-institutional badge-slate">Phased Application Matrix</span>
          </div>

          <div class="interventions-differentiated-grid">
            <div 
              v-for="(act, aIdx) in advisoryResult.actions" 
              :key="aIdx" 
              class="action-domain-card"
              :class="getActionDomainClass(act.category, aIdx)"
            >
              <div class="domain-card-header">
                <div class="domain-badge-group">
                  <span class="domain-icon-dot" aria-hidden="true"></span>
                  <span class="domain-tag" v-text="act.category"></span>
                </div>
                <span class="priority-chip" :class="getPriorityClass(act.urgency)">
                  <span v-text="act.urgency"></span> Priority
                </span>
              </div>

              <div class="domain-card-body">
                <h4 class="action-card-title" v-text="act.title"></h4>
                <p class="action-card-detail" v-text="act.description"></p>
              </div>

              <div class="domain-card-specs">
                <div class="spec-pill">
                  <span class="pill-label">Input Cost</span>
                  <strong class="pill-val" v-text="act.cost_level"></strong>
                </div>
                <div class="spec-pill spec-pill-outcome">
                  <span class="pill-label">Target Biological Outcome</span>
                  <strong class="pill-val" v-text="act.expected_outcome"></strong>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Soil Conditioning & Cultural Protocols (Unified Field Protocol Matrix) -->
        <div class="protocols-field-matrix">
          <div class="protocol-column-card protocol-soil-card">
            <div class="protocol-card-header">
              <div class="protocol-header-icon-wrap bg-soil-tint">
                <svg class="protocol-svg-icon text-soil" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v18M12 3c-4.5 0-7 3.5-7 8 0 4 3 7 7 10M12 3c4.5 0 7 3.5 7 8 0 4-3 7-7 10" />
                </svg>
              </div>
              <div>
                <h4>Soil conditioning and pedological protocols</h4>
                <span class="protocol-header-sub">Root zone mycorrhizal &amp; microbial remediation</span>
              </div>
            </div>
            <div class="protocol-step-rows">
              <div 
                v-for="(step, stIdx) in advisoryResult.soil_conditioning_steps" 
                :key="stIdx" 
                class="protocol-step-item"
              >
                <span class="protocol-step-num">0{{ stIdx + 1 }}</span>
                <p class="protocol-step-text" v-text="step"></p>
              </div>
            </div>
          </div>

          <div class="protocol-column-card protocol-water-card">
            <div class="protocol-card-header">
              <div class="protocol-header-icon-wrap bg-sky-tint">
                <svg class="protocol-svg-icon text-sky" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z" />
                </svg>
              </div>
              <div>
                <h4>Cultural, water and microclimate protocols</h4>
                <span class="protocol-header-sub">Canopy aerification &amp; humidity mitigation</span>
              </div>
            </div>
            <div class="protocol-step-rows">
              <div 
                v-for="(pr, pIdx) in advisoryResult.preventive_cultural_practices" 
                :key="pIdx" 
                class="protocol-step-item"
              >
                <span class="protocol-step-num">0{{ pIdx + 1 }}</span>
                <p class="protocol-step-text" v-text="pr"></p>
              </div>
            </div>
          </div>
        </div>

        <!-- Yield Protection & Farm Economics Assessment Infographic -->
        <InfographicEconomicImpact v-if="isDemoResult" />

        <!-- Diagnostic Explainability & Multi-Source Reasoning Ledger (Full-Width Table) -->
        <div class="explainability-block">
          <div class="explainability-header">
            <svg class="svg-icon text-forest" viewBox="0 0 24 24" stroke="currentColor" fill="none" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
            <div>
              <h4>Diagnostic explainability and multi-source reasoning ledger</h4>
              <span>Evidence returned by retrieval and advisory generation</span>
            </div>
          </div>
          <div class="evidence-table-container">
            <table class="evidence-table">
              <thead>
                <tr>
                  <th style="width: 22%;">Factor</th>
                  <th style="width: 38%;">Observed Parameter</th>
                  <th style="width: 40%;">Impact on Agronomic Advisory</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(ev, eIdx) in advisoryResult.explainability" :key="eIdx">
                  <td><code v-text="ev.factor"></code></td>
                  <td v-text="ev.observation"></td>
                  <td class="font-editorial-italic explainability-impact">"<span v-text="ev.impact_on_decision"></span>"</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Unit Economics & Clinical Agronomic Notice -->
        <div class="economics-notice-strip">
          <div v-if="isDemoResult" class="economics-row">
            <span class="badge-institutional badge-slate">Unit Economics</span>
            <span>Gemini Flash Inference: ₹0.12 / query · Smallholder Input Savings: ₹1,550 / acre · Benefit-Cost Ratio: 14:1</span>
          </div>
          <p class="clinical-disclaimer">
            <strong>Decision-support notice:</strong> AI-generated guidance is not a confirmed diagnosis. Verify treatment recommendations with a local agricultural expert and follow product labels.
          </p>
        </div>

        <!-- Grounded ICAR Monographs -->
        <div v-if="advisoryResult.rag_sources && advisoryResult.rag_sources.length" class="monographs-box">
            <span class="monograph-title">Retrieved knowledge entries:</span>
          <div class="monograph-chips">
            <span v-for="src in advisoryResult.rag_sources" :key="src.id" class="badge-institutional badge-slate" :title="src.text">
              {{ src.topic }} ({{ src.region || 'General' }})
            </span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { 
  diagnoseCropDisease, 
  generateRegenerativeAdvisory, 
  fetchAgroWeather, 
  fetchSoilHealth, 
  fetchSatelliteNDVI,
  resolveMediaUrl 
} from '../api'
import { useOfflineStorage } from '../composables/useOfflineStorage'
import InfographicTelemetryRadar from '../components/InfographicTelemetryRadar.vue'
import InfographicPathogenCycle from '../components/InfographicPathogenCycle.vue'
import InfographicTreatmentRoadmap from '../components/InfographicTreatmentRoadmap.vue'
import InfographicEconomicImpact from '../components/InfographicEconomicImpact.vue'

const { isOnline, saveOfflineItem, getOfflineItem } = useOfflineStorage()

// Current Farm Context State
const currentContext = reactive({
  standard_version: 'in.gov.dpg.farmcontext.v1',
  farmer: {
    farmer_id: '',
    name: '',
    phone: '',
    preferred_language: 'en',
    literacy_profile: 'text_preferred',
    voice_observation: ''
  },
  location: {
    state: '',
    district: '',
    block_tehsil: '',
    village: '',
    latitude: null,
    longitude: null
  },
  crop: {
    name: '',
    variety: '',
    season: '',
    crop_stage: '',
    sowing_date: null,
    days_since_sowing: null
  },
  soil_health: {
    source: 'Sample baseline (not linked to a farmer soil test)',
    card_id: 'SHC-WB-2026-8819',
    lab_test_cert: 'ICAR-NBSS-LUP/2026/WB-089',
    nitrogen_kg_ha: 185.0,
    phosphorus_kg_ha: 14.2,
    potassium_kg_ha: 160.0,
    organic_carbon_pct: 0.42,
    ph: 5.8,
    deficiencies: ['Nitrogen Low (<280 kg/ha)', 'Low Organic Carbon (<0.5%)', 'Acidic Alluvial Soil']
  },
  weather: {
    source: 'Sample baseline (not linked to this location)',
    temperature_c: 31.8,
    relative_humidity_pct: 86.0,
    rainfall_last_24h_mm: 18.5,
    rainfall_forecast_7d_mm: 54.0,
    wind_speed_kmh: 14.2,
    microclimate_risk: 'Elevated fungal sporulation risk (RH > 82%)'
  },
  satellite: {
    source: 'Sample baseline (no satellite imagery fetched)',
    tile_reference: 'S2A_MSIL2A_20260924_T45QXE_R061',
    spectral_formula: 'NDVI = (B08_NIR - B04_Red) / (B08_NIR + B04_Red)',
    nir_band_reflectance: 0.78,
    red_band_reflectance: 0.17,
    ndvi: 0.64,
    ndvi_trend: 'slight_drop_anomaly',
    soil_moisture_index: 0.42,
    cloud_cover_pct: 20.0,
    vegetation_vigor: 'Moderate canopy vigor; localized chlorosis in sector B'
  },
  diagnosis: null
})

// UI & Reactive States
const loadingTelemetry = ref(false)
const isDiagnosing = ref(false)
const isGeneratingAdvisory = ref(false)
const previewImage = ref(null)
const selectedFileName = ref('')
const selectedSample = ref(null)
const fileInputRef = ref(null)
const selectedFileBlob = ref(null)
const diagnosisResult = ref(null)
const advisoryResult = ref(null)
const showEnTranslation = ref(false)
const showBenchmarks = ref(false)
const isDemoResult = ref(false)
const diagnosisError = ref('')
const advisoryError = ref('')
const isContextReady = computed(() => Boolean(
  currentContext.crop.name.trim() &&
  currentContext.location.state.trim() &&
  currentContext.location.district.trim() &&
  currentContext.crop.crop_stage.trim()
))

// Voice STT State
const isRecording = ref(false)
const voiceTranscript = ref('')
let recognition = null

// Sample benchmark base64 images and canonical clinical payloads
const SAMPLE_BENCHMARKS = {
  rice: {
    label: 'Rice Sheath Blight (Nadia, WB)',
    crop: 'Rice (Paddy)',
    is_valid: true,
    diagnosis: {
      condition_detected: 'Rice Sheath Blight',
      scientific_name: 'Rhizoctonia solani Kühn',
      confidence: 0.94,
      severity: 'High',
      affected_part: 'Leaf Sheath & Lower Culm',
      is_valid_crop_image: true,
      model_used: 'gemini-2.5-flash',
      rejection_reason: null,
      symptoms: [
        'Elliptical or oval water-soaked greenish-grey lesions on lower leaf sheaths near water line.',
        'Lesions coalesce with distinct irregular dark-brown margins creating banded appearance.',
        'Initial formation of tiny white globose mycelial sclerotial bodies.'
      ],
      immediate_bio_action: 'Apply foliar bio-spray of Trichoderma harzianum @ 5g/L or Pseudomonas fluorescens @ 10g/L along the base of the infected hill. Drain field to reduce canopy microclimate humidity.'
    },
    advisory: {
      language: 'bn',
      summary_advisory: 'আপনার ধানের জমিতে খোল পোড়া (Sheath Blight) রোগের লক্ষণ দেখা দিয়েছে। বাতাসের আর্দ্রতা ৮৬% হওয়ায় ছত্রাকের জীবাণু দ্রুত বিস্তার লাভ করতে পারে। রাসায়নিক প্রয়োগের পূর্বে জমিতে জমে থাকা অতিরিক্ত জল নিষ্কাশন করুন এবং ট্রাইকোডার্মা হারজিয়ানাম বা সিউডোমোনাস ফ্লুরোসেন্স স্প্রে করুন। মাটির পিএইচ ৫.৮ হওয়ায় ইউরিয়া অতিরিক্ত দেবেন না।',
      summary_advisory_en: 'Sheath Blight symptoms detected on your rice crop. High relative humidity (86%) accelerates fungal spread. Drain stagnant field water immediately and apply bio-fungicide foliar spray (Trichoderma harzianum or Pseudomonas fluorescens). Refrain from excess nitrogenous fertilizer as soil is acidic (pH 5.8).',
      generated_at: '2026-09-29 03:45 UTC',
      audio_url: null,
      actions: [
        {
          title: 'Field Microclimate Water Drainage',
          category: 'Cultural Interventions',
          urgency: 'Immediate (Within 24h)',
          description: 'Drain standing ponded water from the paddy field for 3-4 days to expose the lower sheath to sunlight and lower relative humidity below 80%.',
          cost_level: 'Zero Cost',
          expected_outcome: 'Halts secondary sclerotial germination'
        },
        {
          title: 'Bio-Fungicidal Foliar Application',
          category: 'Biological Protection',
          urgency: 'Critical',
          description: 'Foliar spray of Trichoderma harzianum (2x10^9 CFU/g) @ 5g/L water targeted at the base of the crop canopy during afternoon hours.',
          cost_level: 'Low (₹140 / acre)',
          expected_outcome: 'Suppresses Rhizoctonia mycelial growth by 75%'
        },
        {
          title: 'Potassium & Silicon Strengthening',
          category: 'Soil Remediation',
          urgency: 'Medium',
          description: 'Top-dress with Muriate of Potash (MOP) @ 15 kg/acre to strengthen culm epidermal cell walls against enzymatic penetration.',
          cost_level: 'Moderate (₹320 / acre)',
          expected_outcome: 'Enhances mechanical resistance of culm'
        }
      ],
      soil_conditioning_steps: [
        'Current soil pH is 5.8 (acidic); avoid lime during active pathogen sporulation.',
        'Incorporate decomposed farmyard manure (FYM) or bio-slurry @ 2 tonnes/ha post-harvest to restore organic carbon (currently 0.42%).'
      ],
      preventive_cultural_practices: [
        'Keep bunds clean of alternate weed hosts (Echinochloa colona, Cyperus difformis).',
        'Avoid excessive top-dressing of urea; split nitrogen into 3 equal doses.'
      ],
      explainability: [
        {
          factor: 'Atmospheric Humidity (86%)',
          observation: 'Relative humidity exceeds threshold (RH > 82%) with night ambient 26°C.',
          impact_on_decision: 'Mandates immediate field water drainage to inhibit fungal incubation.'
        },
        {
          factor: 'Soil Reaction (pH 5.8)',
          observation: 'Acidic alluvium limits bio-available phosphorus and systemic plant immunity.',
          impact_on_decision: 'Recommends MOP potassium strengthening rather than heavy chemical liming.'
        },
        {
          factor: 'Sentinel-2 NDVI (0.64)',
          observation: 'Canopy vigor index reflects dense tillering foliage, creating shaded microclimate.',
          impact_on_decision: 'Specifies targeted base spray instead of general aerial broadcast.'
        }
      ],
      rag_sources: [
        { id: 'rag-01', topic: 'Integrated Rice Sheath Blight Management', region: 'Gangetic Plains' },
        { id: 'rag-02', topic: 'Biological Control of Sclerotial Plant Pathogens', region: 'ICAR-CRRI' }
      ]
    },
    url: 'data:image/svg+xml;utf8,<svg role="img" aria-label="Rice Sheath Blight specimen" xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260"><rect width="400" height="260" fill="%232d5a27"/><path d="M50,180 Q200,20 350,160 Q200,240 50,180" fill="%23438a39"/><ellipse cx="160" cy="140" rx="35" ry="18" fill="%238a795d" stroke="%234a2e12" stroke-width="3"/><ellipse cx="230" cy="120" rx="45" ry="22" fill="%239c8969" stroke="%235c3b19" stroke-width="4"/><ellipse cx="280" cy="110" rx="25" ry="12" fill="%23806e50" stroke="%234a2e12" stroke-width="2"/><text x="110" y="240" fill="white" font-family="sans-serif" font-size="14" font-weight="bold">Rice Sheath Blight Lesion (Rhizoctonia)</text></svg>'
  },
  wheat: {
    label: 'Wheat Yellow Rust (Punjab)',
    crop: 'Wheat',
    is_valid: true,
    diagnosis: {
      condition_detected: 'Wheat Stripe (Yellow) Rust',
      scientific_name: 'Puccinia striiformis f. sp. tritici',
      confidence: 0.96,
      severity: 'Severe',
      affected_part: 'Foliar Lamina (Linear Uredinial Pustules)',
      is_valid_crop_image: true,
      model_used: 'gemini-2.5-flash',
      rejection_reason: null,
      symptoms: [
        'Linear parallel rows of bright yellow or orange uredinial pustules along leaf veins.',
        'Pustules break through epidermal layer releasing yellow powdery spore dust.',
        'Severe foliar chlorosis with accelerated senescence of photosynthetic leaf area.'
      ],
      immediate_bio_action: 'Spray bio-fungicidal formulation of Bacillus subtilis @ 10g/L or fermented garlic-chili foliar repellent. Establish border quarantine to retard wind-borne urediniospore drift.'
    },
    advisory: {
      language: 'bn',
      summary_advisory: 'গমের পাতায় হলুদ মরিচা (Stripe Rust) রোগের বিস্তার লক্ষ্য করা গেছে। পুসিনিয়া ছত্রাক বাতাসের মাধ্যমে দ্রুত ছড়ায়। অবিলম্বে আক্রান্ত সীমানায় জৈব ছত্রাকনাশক স্প্রে করুন এবং জমিতে অতিরিক্ত নাইট্রোজেন সার দেওয়া বন্ধ রাখুন।',
      summary_advisory_en: 'Yellow Stripe Rust confirmed on wheat foliage. Puccinia spores spread rapidly via wind currents. Spray Bacillus subtilis bio-formulation immediately and withhold supplementary urea fertilization.',
      generated_at: '2026-09-29 03:45 UTC',
      audio_url: null,
      actions: [
        {
          title: 'Biological Spore Suppression Spray',
          category: 'Biological Protection',
          urgency: 'Immediate (Within 12h)',
          description: 'Foliar spray of Bacillus subtilis (1x10^9 spores/g) @ 10g/L to antagonize rust fungal sporulation.',
          cost_level: 'Low (₹160 / acre)',
          expected_outcome: 'Inhibits urediniospore viability by 80%'
        },
        {
          title: 'Wind-Break Border Inspection',
          category: 'Cultural Interventions',
          urgency: 'High',
          description: 'Survey windward field borders; rogue out severely infected pioneer clumps to suppress aerodynamic inoculation.',
          cost_level: 'Zero Cost',
          expected_outcome: 'Prevents mass canopy infestation'
        }
      ],
      soil_conditioning_steps: [
        'Halt top-dressing of urea; excess vegetative succulence increases rust vulnerability.',
        'Apply foliar zinc sulfate @ 0.5% + urea 1% to mitigate localized chlorosis.'
      ],
      preventive_cultural_practices: [
        'Plant stripe-rust resistant cultivars (HD-2967, DBW-187) in subsequent sowing rotations.',
        'Synchronize sowing across village clusters to prevent staggered infection windows.'
      ],
      explainability: [
        {
          factor: 'Wind Speed & Ambient Temp',
          observation: 'Cool ambient temperature (16-22°C) with moderate breezes favors airborne dissemination.',
          impact_on_decision: 'Prioritizes windward containment spray.'
        },
        {
          factor: 'Leaf Nitrogen Status',
          observation: 'High foliage succulence accelerates pustule eruption.',
          impact_on_decision: 'Discontinues nitrogen top-dressing.'
        }
      ],
      rag_sources: [
        { id: 'rag-03', topic: 'Management of Wheat Rust Epidemics', region: 'Indo-Gangetic Plains' }
      ]
    },
    url: 'data:image/svg+xml;utf8,<svg role="img" aria-label="Wheat Yellow Rust specimen" xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260"><rect width="400" height="260" fill="%233e5c32"/><path d="M40,210 Q200,10 360,190" stroke="%23eab308" stroke-width="6" stroke-dasharray="10,5"/><path d="M60,225 Q210,35 340,200" stroke="%23facc15" stroke-width="8" stroke-dasharray="8,4"/><text x="100" y="245" fill="white" font-family="sans-serif" font-size="14" font-weight="bold">Wheat Yellow Rust Stripes (Puccinia)</text></svg>'
  },
  cotton: {
    label: 'Cotton Pink Bollworm (Maharashtra)',
    crop: 'Cotton',
    is_valid: true,
    diagnosis: {
      condition_detected: 'Pink Bollworm Infestation',
      scientific_name: 'Pectinophora gossypiella (Saunders)',
      confidence: 0.91,
      severity: 'High',
      affected_part: 'Developing Boll & Squares (Entry Borehole)',
      is_valid_crop_image: true,
      model_used: 'gemini-2.5-flash',
      rejection_reason: null,
      symptoms: [
        'Pin-hole entry boreholes on young developing bolls plugged with larval frass.',
        'Rosetted flower blossoms ("rosette flowers") failing to open normally.',
        'Internal burrowing through locules damaging lint fibers and seeds.'
      ],
      immediate_bio_action: 'Install Gossyplure sex pheromone delta traps @ 10 traps/acre; release egg parasitoid Trichogramma bactrae @ 50,000 wasps/acre.'
    },
    advisory: {
      language: 'bn',
      summary_advisory: 'তুলার গুটিতে গোলাপি শুঁয়োপোকার (Pink Bollworm) আক্রমণ শনাক্ত করা হয়েছে। অবিলম্বে ফেরোমোন ফাঁদ ব্যবহার করুন এবং ট্রাইকোগ্রামা পরজীবী ছাড়ুন।',
      summary_advisory_en: 'Pink Bollworm infestation confirmed in cotton bolls. Deploy Gossyplure pheromone traps and release Trichogramma bactrae parasitoids immediately.',
      generated_at: '2026-09-29 03:45 UTC',
      audio_url: null,
      actions: [
        {
          title: 'Mating Disruption with Pheromone Traps',
          category: 'Biological Protection',
          urgency: 'Critical',
          description: 'Deploy 8-10 Gossyplure delta traps per acre at canopy height to capture male moths.',
          cost_level: 'Low (₹220 / acre)',
          expected_outcome: 'Disrupts reproductive mating cycles by 65%'
        },
        {
          title: 'Parasitoid Bio-Release',
          category: 'Biological Control',
          urgency: 'High',
          description: 'Release Trichogramma bactrae parasitized egg cards during early morning hours.',
          cost_level: 'Low (₹150 / acre)',
          expected_outcome: 'Parasitizes bollworm eggs before larval emergence'
        }
      ],
      soil_conditioning_steps: [
        'Maintain deep soil aeration between rows; destroy fallen shed squares harboring diapausing larvae.'
      ],
      preventive_cultural_practices: [
        'Avoid extending ratoon crop beyond recommended seasonal duration.',
        'Install light traps on field perimeters to monitor nocturnal flight flushes.'
      ],
      explainability: [
        {
          factor: 'Crop Phenology (Flowering/Boll formation)',
          observation: 'Boll initiation stage coincides with second-generation moth emergence.',
          impact_on_decision: 'Triggers mass trapping and parasitoid release.'
        }
      ],
      rag_sources: [
        { id: 'rag-04', topic: 'Integrated Pest Management for Cotton Pink Bollworm', region: 'Central India' }
      ]
    },
    url: 'data:image/svg+xml;utf8,<svg role="img" aria-label="Cotton Pink Bollworm specimen" xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260"><rect width="400" height="260" fill="%231e3a1e"/><circle cx="200" cy="130" r="70" fill="%233f6212"/><circle cx="180" cy="115" r="10" fill="%231c1917"/><ellipse cx="215" cy="140" rx="14" ry="7" fill="%23fb7185" stroke="%23881337"/><text x="80" y="245" fill="white" font-family="sans-serif" font-size="14" font-weight="bold">Cotton Pink Bollworm Borehole (Pectinophora)</text></svg>'
  },
  invalid_dog: {
    label: 'Non-Crop Guardrail Validation (Canine Photo)',
    crop: 'Non-Crop',
    is_valid: false,
    diagnosis: {
      condition_detected: 'Non-Agricultural Specimen (Canine)',
      scientific_name: 'Canis lupus familiaris',
      confidence: 0.99,
      severity: 'N/A',
      affected_part: 'N/A',
      is_valid_crop_image: false,
      model_used: 'gemini-2.5-flash',
      rejection_reason: 'The submitted image depicts a domestic animal (canine), not a cultivated crop or plant foliage specimen. KrishiSetu has safely rejected diagnosis to prevent erroneous agrochemical recommendations and protect farmer capital.',
      symptoms: [],
      immediate_bio_action: ''
    },
    advisory: null,
    url: 'data:image/svg+xml;utf8,<svg role="img" aria-label="Non-Crop specimen" xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260"><rect width="400" height="260" fill="%23cbd5e1"/><ellipse cx="200" cy="130" rx="80" ry="60" fill="%23d97706"/><circle cx="160" cy="110" r="12" fill="%230f172a"/><circle cx="240" cy="110" r="12" fill="%230f172a"/><ellipse cx="200" cy="145" rx="16" ry="10" fill="%230f172a"/><path d="M140,80 Q110,30 130,120" fill="%2392400e"/><path d="M260,80 Q290,30 270,120" fill="%2392400e"/><text x="80" y="235" fill="%231e293b" font-family="sans-serif" font-size="14" font-weight="bold">Non-Crop Image (Triggers Guardrail Rejection)</text></svg>'
  }
}

onMounted(async () => {
  const savedContext = await getOfflineItem('farmer_context')
  if (savedContext) {
    Object.assign(currentContext.crop, savedContext.crop || {})
    Object.assign(currentContext.location, savedContext.location || {})
    Object.assign(currentContext.farmer, savedContext.farmer || {})
  }
})

function selectAndRunBenchmark(type) {
  loadSampleLeaf(type)
}

function loadSampleLeaf(type) {
  selectedSample.value = type
  const sample = SAMPLE_BENCHMARKS[type]
  if (!sample) return

  isDemoResult.value = true
  currentContext.diagnosis = null
  diagnosisError.value = ''
  advisoryError.value = ''
  if (fileInputRef.value) fileInputRef.value.value = ''
  previewImage.value = sample.url
  selectedFileName.value = sample.label
  selectedFileBlob.value = null
  diagnosisResult.value = sample.diagnosis
  advisoryResult.value = sample.advisory
}

function triggerFileInput() {
  fileInputRef.value?.click()
}

function onFileSelected(event) {
  const file = event.target.files?.[0]
  if (file) {
    isDemoResult.value = false
    selectedSample.value = null
    diagnosisResult.value = null
    advisoryResult.value = null
    currentContext.diagnosis = null
    diagnosisError.value = ''
    advisoryError.value = ''
    selectedFileBlob.value = file
    selectedFileName.value = file.name
    selectedSample.value = 'custom'
    const reader = new FileReader()
    reader.onload = (e) => {
      previewImage.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

function onFarmContextChanged() {
  if (isDemoResult.value) {
    previewImage.value = null
    selectedFileBlob.value = null
    selectedFileName.value = ''
    selectedSample.value = null
    if (fileInputRef.value) fileInputRef.value.value = ''
  }
  diagnosisResult.value = null
  advisoryResult.value = null
  currentContext.diagnosis = null
  isDemoResult.value = false
  diagnosisError.value = ''
  advisoryError.value = ''
  saveOfflineItem('farmer_context', {
    crop: {
      name: currentContext.crop.name,
      variety: currentContext.crop.variety,
      crop_stage: currentContext.crop.crop_stage
    },
    location: {
      state: currentContext.location.state,
      district: currentContext.location.district
    },
    farmer: { preferred_language: currentContext.farmer.preferred_language }
  })
}

function toggleVoiceRecording() {
  if (isRecording.value) {
    recognition?.stop()
    isRecording.value = false
    return
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SpeechRecognition) {
    alert('Speech recognition is not supported in this browser environment. Please test in Chrome or Edge.')
    return
  }

  recognition = new SpeechRecognition()
  const lang = currentContext.farmer.preferred_language
  recognition.lang = lang === 'bn' ? 'bn-IN' : (lang === 'hi' ? 'hi-IN' : 'en-IN')
  recognition.interimResults = false
  recognition.maxAlternatives = 1

  recognition.onstart = () => {
    isRecording.value = true
  }

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript
    voiceTranscript.value = transcript
    currentContext.farmer.voice_observation = transcript
  }

  recognition.onerror = (event) => {
    isRecording.value = false
  }

  recognition.onend = () => {
    isRecording.value = false
  }

  recognition.start()
}

async function runDiagnosis() {
  if (!selectedFileBlob.value || !isContextReady.value || isDemoResult.value) return

  isDiagnosing.value = true
  diagnosisResult.value = null
  advisoryResult.value = null
  diagnosisError.value = ''
  advisoryError.value = ''
  currentContext.diagnosis = null

  try {
    const contextPayload = JSON.parse(JSON.stringify(currentContext))
    const res = await diagnoseCropDisease(selectedFileBlob.value, contextPayload)
    diagnosisResult.value = res
    currentContext.diagnosis = res

    if (res.diagnosis_status === 'complete') {
      await saveOfflineItem('latest_diagnosis', res)
      await saveOfflineItem('latest_context', JSON.parse(JSON.stringify(currentContext)))
    }

    if (res.diagnosis_status === 'complete' && res.is_valid_crop_image) {
      await generateAdvisoryPlan()
    }
  } catch (err) {
    console.error('Diagnosis error:', err)
    diagnosisError.value = err.message || 'Diagnosis is unavailable. Please try again.'
  } finally {
    isDiagnosing.value = false
  }
}

async function generateAdvisoryPlan() {
  isGeneratingAdvisory.value = true
  advisoryError.value = ''
  try {
    const payload = JSON.parse(JSON.stringify(currentContext))
    const res = await generateRegenerativeAdvisory(payload)
    advisoryResult.value = res
    if (res.status === 'success') {
      await saveOfflineItem('latest_advisory', res)
    }
  } catch (err) {
    console.error('Advisory generation error:', err)
    advisoryError.value = err.message || 'Please try again.'
  } finally {
    isGeneratingAdvisory.value = false
  }
}

async function refreshTelemetry() {
  loadingTelemetry.value = true
  try {
    const [w, s, sat] = await Promise.all([
      fetchAgroWeather(currentContext.location.latitude, currentContext.location.longitude),
      fetchSoilHealth(currentContext.location.state, currentContext.location.district),
      fetchSatelliteNDVI(currentContext.location.latitude, currentContext.location.longitude)
    ])
    Object.assign(currentContext.weather, w)
    Object.assign(currentContext.soil_health, s)
    Object.assign(currentContext.satellite, sat)
    await saveOfflineItem('latest_context', JSON.parse(JSON.stringify(currentContext)))
  } catch (err) {
    console.error('Failed to sync telemetry:', err)
  } finally {
    loadingTelemetry.value = false
  }
}

function getLangName(code) {
  if (code === 'bn') return 'Bengali'
  if (code === 'hi') return 'Hindi'
  return 'English'
}

function getActionDomainClass(category, index) {
  const cat = (category || '').toLowerCase()
  if (cat.includes('bio') || cat.includes('fungicid')) return 'domain-biological'
  if (cat.includes('cultur') || cat.includes('water') || cat.includes('drain')) return 'domain-cultural'
  if (cat.includes('soil') || cat.includes('potassium') || cat.includes('remedi')) return 'domain-pedological'
  const fallback = ['domain-cultural', 'domain-biological', 'domain-pedological']
  return fallback[index % 3]
}

function getPriorityClass(urgency) {
  const u = (urgency || '').toLowerCase()
  if (u.includes('immediate') || u.includes('critical')) return 'priority-critical'
  if (u.includes('high')) return 'priority-high'
  return 'priority-medium'
}

// Custom Audio Player State & Controls
const audioElementRef = ref(null)
const isPlayingAudio = ref(false)
const audioCurrentTime = ref(0)
const audioDuration = ref(42)

function toggleAudioPlayback() {
  if (!audioElementRef.value) return
  if (isPlayingAudio.value) {
    audioElementRef.value.pause()
    isPlayingAudio.value = false
  } else {
    audioElementRef.value.play()
    isPlayingAudio.value = true
  }
}

function onAudioTimeUpdate() {
  if (!audioElementRef.value) return
  audioCurrentTime.value = audioElementRef.value.currentTime
  if (audioElementRef.value.duration && !isNaN(audioElementRef.value.duration)) {
    audioDuration.value = audioElementRef.value.duration
  }
}

function onAudioEnded() {
  isPlayingAudio.value = false
  audioCurrentTime.value = 0
}

function seekAudio(e) {
  if (!audioElementRef.value || !audioDuration.value) return
  const rect = e.currentTarget.getBoundingClientRect()
  const clickX = e.clientX - rect.left
  const pct = Math.max(0, Math.min(1, clickX / rect.width))
  audioElementRef.value.currentTime = pct * audioDuration.value
  audioCurrentTime.value = audioElementRef.value.currentTime
}

const audioProgressPct = computed(() => {
  if (!audioDuration.value) return 0
  return Math.min(100, (audioCurrentTime.value / audioDuration.value) * 100)
})

const audioTimeDisplay = computed(() => {
  const curM = Math.floor(audioCurrentTime.value / 60)
  const curS = Math.floor(audioCurrentTime.value % 60)
  const durM = Math.floor(audioDuration.value / 60)
  const durS = Math.floor(audioDuration.value % 60)
  return `${curM}:${curS < 10 ? '0' : ''}${curS} / ${durM}:${durS < 10 ? '0' : ''}${durS}`
})
</script>

<style scoped>
.kisan-sathi-container {
  padding: 32px 28px;
  max-width: 1440px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.offline-banner { order: 0; }
.profile-ribbon { order: 1; }
.farmer-context-card { order: 2; }
.diagnostic-lab-grid { order: 3; }
.telemetry-operations-matrix { order: 4; }
.post-diagnosis-infographics { order: 5; }
.advisory-full-dossier { order: 6; }

.farmer-context-card {
  padding: 18px 20px;
}

.context-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.context-heading p {
  margin: 3px 0 0;
  color: var(--slate-600);
  font-size: 12px;
}

.farmer-context-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.farmer-context-grid label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  min-width: 0;
  color: var(--slate-700);
  font-size: 12px;
  font-weight: 600;
}

.farmer-context-grid input,
.farmer-context-grid select {
  width: 100%;
  min-height: 42px;
  padding: 8px 10px;
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  color: var(--slate-900);
  font-size: 14px;
}

.farmer-context-grid input:focus-visible,
.farmer-context-grid select:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

.benchmark-controls {
  padding: 12px 18px;
  border-bottom: 1px solid var(--color-border);
}

.benchmark-note {
  margin: 8px 0 0;
  color: var(--soil-800);
  font-size: 12px;
}

.specimen-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 18px;
  color: #f8fafc;
  text-align: center;
}

.specimen-empty-state span {
  color: #cbd5e1;
  font-size: 12px;
}

.benchmark-result-notice,
.diagnosis-error-notice,
.diagnosis-unavailable {
  margin: 14px 18px 0;
  padding: 12px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--slate-50);
  color: var(--slate-800);
  font-size: 13px;
  line-height: 1.5;
}

.benchmark-result-notice {
  border-color: var(--soil-200);
  background: var(--soil-50);
  color: var(--soil-800);
  font-weight: 700;
}

.diagnosis-error-notice {
  border-color: var(--soil-200);
  background: var(--soil-50);
}

.diagnosis-unavailable h3 {
  margin: 0 0 4px;
  font-size: 14px;
}

.diagnosis-unavailable p {
  margin: 0;
}

/* Offline Notice Banner */
.offline-banner {
  background: var(--soil-50);
  border: 1px solid var(--soil-200);
  border-radius: var(--radius-sm);
  padding: 12px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 13px;
}

.banner-marker {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--soil-600);
  flex-shrink: 0;
}

.banner-body {
  flex: 1;
  color: var(--soil-800);
}

.banner-body strong {
  margin-right: 6px;
}

/* Farmer Profile Ribbon */
.profile-ribbon {
  padding: 20px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  border-radius: var(--radius-md);
}

.profile-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.profile-badge-frame {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: var(--slate-100);
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--slate-700);
  flex-shrink: 0;
}

.farmer-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.farmer-meta-line {
  margin-top: 5px;
  font-size: 13px;
  color: var(--color-text-secondary);
  line-height: 1.4;
}

.profile-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.lang-selector-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.selector-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--slate-700);
}

.lang-dropdown {
  height: 38px;
  padding: 0 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-strong);
  background: var(--bg-surface);
  font-size: 12.5px;
  color: var(--slate-900);
}

.lang-dropdown:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

/* Unified Telemetry Operations Matrix */
.telemetry-operations-matrix {
  overflow: hidden;
  border-radius: var(--radius-md);
}

.matrix-head {
  padding: 16px 24px;
  border-bottom: 1px solid var(--color-border);
  background: var(--slate-50);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.matrix-title {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--slate-900);
}

.matrix-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.matrix-column {
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.border-left-divider {
  border-left: 1px solid var(--color-border);
}

.column-header {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.stream-index {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  color: var(--slate-400);
  letter-spacing: 0.05em;
}

.column-header h3 {
  font-size: 14px;
  font-weight: 700;
  color: var(--slate-900);
}

.source-tag {
  font-size: 11.5px;
  color: var(--slate-500);
}

.metrics-tabular {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.metric-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-border);
  font-size: 12.5px;
  background: var(--bg-surface);
}

.metric-row:last-child {
  border-bottom: none;
}

.metric-row.highlight-alert {
  background: #fffbf5;
}

.metric-key {
  color: var(--slate-600);
}

.metric-val {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--slate-900);
  font-variant-numeric: tabular-nums;
}

.text-alert {
  color: var(--soil-700);
}

.text-forest {
  color: var(--forest-800);
}

.stream-risk-note {
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 8px 10px;
  font-size: 11.5px;
  line-height: 1.4;
}

.risk-label {
  font-weight: 700;
  color: var(--slate-700);
  display: block;
  margin-bottom: 2px;
}

.deficiency-chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.provenance-technical-box {
  background: #0f172a;
  border-radius: var(--radius-sm);
  padding: 10px;
  color: #e2e8f0;
  font-size: 11px;
}

.formula-technical-row code {
  color: #86efac;
  font-family: var(--font-mono);
  display: block;
  margin-bottom: 4px;
}

.granule-technical-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  color: #94a3b8;
}

.granule-code {
  color: #93c5fd;
  font-family: var(--font-mono);
}

/* Stage 3: Clinical Diagnostic Laboratory Stage (Balanced 2-Column Grid) */
.diagnostic-lab-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 20px;
  align-items: stretch;
  width: 100%;
}

.diagnostic-intake-card,
.diagnostic-evaluation-card {
  min-width: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.section-header-row {
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--slate-50);
  gap: 12px;
  flex-wrap: wrap;
}

.section-sub {
  font-size: 11.5px;
  color: var(--slate-500);
  margin-top: 2px;
}

/* Specimen Benchmark Selector (Segmented Tab Bar) */
.specimen-selector-bar {
  padding: 14px 18px 12px 18px;
  border-bottom: 1px solid var(--color-border);
  background: var(--slate-50);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.selector-subheading {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 700;
  color: var(--slate-500);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.segmented-specimen-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  background: var(--slate-200);
  padding: 4px;
  border-radius: var(--radius-sm);
}

.specimen-tab-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 7px 10px;
  border: 1px solid transparent;
  border-radius: var(--radius-xs);
  background: transparent;
  color: var(--slate-700);
  font-family: var(--font-swiss);
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.specimen-tab-btn:hover {
  background: rgba(255, 255, 255, 0.6);
  color: var(--slate-900);
}

.specimen-tab-btn:active {
  transform: scale(0.97);
}

.specimen-tab-btn:focus-visible {
  outline: 2px solid var(--forest-600);
  outline-offset: 1px;
}

.specimen-tab-btn.active {
  background: #ffffff;
  color: var(--slate-950);
  border-color: var(--slate-300);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  font-weight: 700;
}

.specimen-tab-btn.btn-guardrail {
  color: var(--soil-800);
}

.specimen-tab-btn.btn-guardrail.active {
  border-color: var(--soil-300);
  background: #ffffff;
  color: var(--soil-800);
}

.crop-indicator {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.indicator-rice { background: #22c55e; }
.indicator-wheat { background: #eab308; }
.indicator-cotton { background: #3b82f6; }
.indicator-guardrail { background: #f97316; }

/* Specimen Inspection Viewfinder Stage */
.specimen-stage-frame {
  padding: 16px 18px;
  background: #0f172a;
}

.specimen-viewfinder {
  position: relative;
  width: 100%;
  height: 220px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: #020617;
  border: 1px solid #334155;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.viewfinder-tag {
  min-width: 0;
  flex: 1;
}

.specimen-rendered-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.viewfinder-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px 12px;
  background: rgba(15, 23, 42, 0.88);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.viewfinder-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: #f1f5f9;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tag-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  flex-shrink: 0;
}

.btn-change-photo {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(30, 41, 59, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: var(--radius-xs);
  padding: 4px 8px;
  color: #ffffff;
  font-family: var(--font-swiss);
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.btn-change-photo:hover {
  background: rgba(255, 255, 255, 0.25);
}

.btn-change-photo .svg-icon {
  width: 13px;
  height: 13px;
}

/* Farmer Voice Observation Console */
.voice-intake-card {
  padding: 14px 18px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: var(--bg-surface);
}

.voice-intake-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.voice-intake-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--slate-800);
}

.voice-action-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-voice-record {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--slate-300);
  background: var(--slate-50);
  color: var(--slate-800);
  font-family: var(--font-swiss);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.btn-voice-record:hover {
  background: var(--slate-100);
  border-color: var(--slate-400);
}

.btn-voice-record.is-active-recording {
  background: #fef2f2;
  border-color: #f87171;
  color: #dc2626;
}

.live-mic-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #dc2626;
  animation: pulse-ring 0.75s infinite;
}

@keyframes pulse-ring {
  0% { transform: scale(0.9); opacity: 0.8; }
  50% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.8; }
}

.transcript-box {
  background: var(--slate-50);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xs);
  padding: 10px 12px;
}

.transcript-lead {
  display: block;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  color: var(--slate-500);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 4px;
}

.transcript-quote {
  margin: 0;
  font-family: var(--font-editorial);
  font-style: italic;
  font-size: 13.5px;
  color: var(--forest-900);
  line-height: 1.45;
}

.voice-hint {
  margin: 0;
  font-family: var(--font-editorial);
  font-style: italic;
  font-size: 12px;
  color: var(--slate-500);
  line-height: 1.4;
}

/* Action Execution Button */
.diagnose-actions {
  padding: 16px 18px 12px 18px;
}

.btn-execute-diagnosis {
  padding: 12px 16px;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.w-full {
  width: 100%;
}

.justify-center {
  justify-content: center;
}

.btn-compact {
  padding: 4px 10px;
  font-size: 11.5px;
}

/* Specimen Technical Metadata */
.specimen-tech-bar {
  padding: 10px 18px;
  border-top: 1px solid var(--color-border);
  background: var(--slate-50);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--slate-500);
  flex-wrap: wrap;
  gap: 6px;
}

.specimen-tech-bar code {
  color: var(--forest-800);
  font-weight: 600;
}

/* Skeleton Loading Utilities */
.diagnostic-skeleton-card, .advisory-skeleton-card {
  padding: 20px;
}

.h-4 { height: 16px; }
.h-6 { height: 24px; }
.h-12 { height: 48px; }
.h-20 { height: 80px; }
.h-24 { height: 96px; }
.h-32 { height: 128px; }
.w-1-2 { width: 50%; }
.w-3-4 { width: 75%; }
.mb-2 { margin-bottom: 8px; }
.mb-3 { margin-bottom: 12px; }
.mb-4 { margin-bottom: 16px; }

/* Guardrail Alert Box */
.guardrail-alert-box {
  margin: 20px;
  background: var(--soil-50);
  border: 1px solid var(--soil-200);
  border-radius: var(--radius-sm);
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.alert-icon-frame {
  margin-top: 2px;
  flex-shrink: 0;
}

.guardrail-alert-box h4 {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--soil-800);
  margin-bottom: 4px;
}

.guardrail-alert-box p {
  font-size: 12px;
  color: var(--soil-800);
  margin-bottom: 6px;
  line-height: 1.45;
}

.guardrail-sub {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--soil-600);
}

/* Laboratory Findings Body */
.lab-findings-body {
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  flex: 1;
}

.diag-header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 4px;
  gap: 12px;
  flex-wrap: wrap;
}

.diag-label {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--slate-500);
  text-transform: uppercase;
}

.diag-condition-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--slate-900);
  margin-top: 2px;
}

.diag-scientific-name {
  font-family: var(--font-editorial);
  font-style: italic;
  font-size: 14px;
  color: var(--slate-600);
  display: block;
  margin-top: 2px;
}

.diag-match-badge {
  text-align: right;
  flex-shrink: 0;
}

.match-percentage {
  font-family: var(--font-mono);
  font-size: 20px;
  font-weight: 800;
  color: var(--forest-800);
  display: block;
  line-height: 1.1;
}

.match-label {
  font-size: 10.5px;
  color: var(--slate-500);
}

.diag-attribute-strip {
  display: flex;
  gap: 6px;
  margin-bottom: 2px;
  flex-wrap: wrap;
}

.markers-block h4 {
  font-size: 12px;
  font-weight: 700;
  color: var(--slate-800);
  margin-bottom: 6px;
}

.markers-list {
  margin: 0;
  padding-left: 18px;
  font-size: 12px;
  color: var(--slate-700);
  line-height: 1.45;
}

.protective-step-box {
  background: var(--bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 12px;
}

.step-title {
  font-weight: 700;
  color: var(--slate-800);
  display: block;
  margin-bottom: 2px;
}

.protective-step-box p {
  margin: 0;
  color: var(--slate-700);
  line-height: 1.45;
}

.lab-provenance-strip {
  margin-top: auto;
  padding: 10px 18px;
  background: var(--slate-50);
  border-top: 1px solid var(--color-border);
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--slate-500);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.lab-provenance-strip strong {
  color: var(--forest-800);
}

.lab-readiness-state {
  padding: 48px 24px;
  text-align: center;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--slate-500);
}

.lab-readiness-state h4 {
  font-size: 14px;
  font-weight: 700;
  color: var(--slate-800);
}

.lab-readiness-state p {
  font-size: 12px;
  max-width: 340px;
}

/* Stage 4: Comprehensive Regenerative Action Dossier (Full-Width Publication Grade) */
.advisory-full-dossier {
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-sm);
}

.dossier-masthead {
  padding: 18px 24px;
  border-bottom: 1px solid var(--color-border);
  background: var(--slate-50);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.masthead-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.dossier-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.masthead-audio-player {
  display: flex;
  align-items: center;
  gap: 14px;
  background: #ffffff;
  border: 1px solid var(--color-border);
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  flex-wrap: wrap;
}

.audio-label-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.audio-label-group strong {
  font-size: 12px;
  color: var(--slate-900);
}

.audio-label-group .audio-sub {
  font-size: 10.5px;
  color: var(--slate-500);
}

.native-audio-player {
  height: 32px;
}

.dossier-body-container {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

/* Actionable Summary Monograph */
.summary-monograph-card {
  background: #fbfbfa;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 18px 22px;
}

.summary-paragraph {
  font-family: var(--font-editorial);
  font-style: italic;
  font-size: 16px;
  line-height: 1.65;
  color: var(--slate-900);
  margin: 0;
}

.translation-drawer {
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid var(--color-border);
}

.btn-text-link {
  background: none;
  border: none;
  padding: 0;
  color: var(--sky-700);
  cursor: pointer;
  font-size: 11.5px;
  font-weight: 600;
}

.en-translation-text {
  margin-top: 6px;
  font-size: 13.5px;
  color: var(--slate-700);
  font-family: var(--font-editorial);
  font-style: italic;
  line-height: 1.6;
}

/* The Golden Hero Prescription Anchor (Primary Visual Gravitational Anchor) */
.golden-prescription-anchor {
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: var(--radius-sm);
  padding: 24px 28px;
  color: #f8fafc;
  box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.35);
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.prescription-masthead {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  flex-wrap: wrap;
}

.prescription-tag-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #34d399;
}

.live-pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.8);
}

.prescription-priority-pill {
  background: rgba(239, 68, 68, 0.18);
  border: 1px solid rgba(239, 68, 68, 0.4);
  color: #fca5a5;
  font-size: 10.5px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 4px;
  letter-spacing: 0.05em;
}

.prescription-content-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 24px;
  align-items: start;
}

@media (max-width: 960px) {
  .prescription-content-grid {
    grid-template-columns: 1fr;
  }
}

.prescription-main-col {
  display: flex;
  flex-direction: column;
}

.prescription-eyebrow {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #94a3b8;
  font-weight: 700;
  display: block;
  margin-bottom: 6px;
}

.prescription-hero-title {
  font-size: 19px;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.35;
  margin: 0 0 10px 0;
  font-family: var(--font-swiss);
}

.prescription-directive {
  font-size: 13.5px;
  color: #cbd5e1;
  line-height: 1.6;
  margin: 0 0 16px 0;
}

.prescription-contraindication-banner {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 4px;
  padding: 10px 14px;
  font-size: 12px;
  color: #fef3c7;
  display: flex;
  align-items: center;
  gap: 10px;
  line-height: 1.45;
}

.contra-icon {
  width: 18px;
  height: 18px;
  color: #f59e0b;
  flex-shrink: 0;
}

.prescription-specs-deck {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.spec-tile {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.spec-tile-label {
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #94a3b8;
  font-weight: 600;
}

.spec-tile-value {
  font-size: 14.5px;
  font-weight: 700;
  color: #ffffff;
}

.text-accent-emerald {
  color: #34d399;
}

.text-accent-gold {
  color: #fbbf24;
}

.spec-tile-sub {
  font-size: 11px;
  color: #94a3b8;
}

/* Prescribed Interventions (Domain-Differentiated Grid) */
.interventions-section {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.section-title-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
}

.section-title-bar h3 {
  font-size: 14px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 0;
}

.section-micro-sub {
  font-size: 11.5px;
  color: var(--slate-500);
  display: block;
  margin-top: 2px;
}

.interventions-differentiated-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  width: 100%;
}

@media (max-width: 1024px) {
  .interventions-differentiated-grid {
    grid-template-columns: 1fr;
  }
}

.action-domain-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 18px 20px;
  background: var(--bg-surface);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 14px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.action-domain-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px -3px rgba(15, 23, 42, 0.08);
}

.action-domain-card.domain-biological {
  border-left: 4px solid var(--forest-600);
}

.action-domain-card.domain-biological .domain-icon-dot {
  background: var(--forest-600);
}

.action-domain-card.domain-biological .domain-tag {
  color: var(--forest-800);
  background: var(--forest-50);
  border: 1px solid var(--forest-200);
}

.action-domain-card.domain-cultural {
  border-left: 4px solid var(--sky-600);
}

.action-domain-card.domain-cultural .domain-icon-dot {
  background: var(--sky-600);
}

.action-domain-card.domain-cultural .domain-tag {
  color: var(--sky-800);
  background: var(--sky-50);
  border: 1px solid var(--sky-200);
}

.action-domain-card.domain-pedological {
  border-left: 4px solid var(--soil-700);
}

.action-domain-card.domain-pedological .domain-icon-dot {
  background: var(--soil-700);
}

.action-domain-card.domain-pedological .domain-tag {
  color: var(--soil-800);
  background: var(--soil-50);
  border: 1px solid var(--soil-200);
}

.domain-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}

.domain-badge-group {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.domain-icon-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.domain-tag {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  letter-spacing: 0.02em;
}

.priority-chip {
  font-size: 10.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
}

.priority-chip.priority-critical {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.priority-chip.priority-high {
  background: #fffbeb;
  color: #92400e;
  border: 1px solid #fde68a;
}

.priority-chip.priority-medium {
  background: #f1f5f9;
  color: #334155;
  border: 1px solid #cbd5e1;
}

.domain-card-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.action-card-title {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 0;
  font-family: var(--font-swiss);
  line-height: 1.35;
}

.action-card-detail {
  font-size: 12.5px;
  color: var(--slate-700);
  line-height: 1.55;
  margin: 0;
}

.domain-card-specs {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 10px;
  border-top: 1px solid var(--color-border);
  background: var(--slate-50);
  border-radius: 4px;
  padding: 10px 12px;
}

.spec-pill {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
  font-size: 11.5px;
}

.pill-label {
  color: var(--slate-500);
  font-weight: 600;
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.pill-val {
  color: var(--slate-900);
  font-weight: 700;
  text-align: right;
}

/* Soil Conditioning & Cultural Protocols (Unified Field Protocol Matrix) */
.protocols-field-matrix {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  width: 100%;
}

@media (max-width: 900px) {
  .protocols-field-matrix {
    grid-template-columns: 1fr;
  }
}

.protocol-column-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 20px 22px;
  background: var(--bg-surface);
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}

.protocol-column-card.protocol-soil-card {
  border-top: 3px solid var(--soil-700);
}

.protocol-column-card.protocol-water-card {
  border-top: 3px solid var(--sky-600);
}

.protocol-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.protocol-header-icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.protocol-header-icon-wrap.bg-soil-tint {
  background: var(--soil-100);
}

.protocol-header-icon-wrap.bg-sky-tint {
  background: var(--sky-100);
}

.protocol-svg-icon {
  width: 20px;
  height: 20px;
}

.protocol-card-header h4 {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--slate-900);
  margin: 0;
  font-family: var(--font-swiss);
}

.protocol-header-sub {
  font-size: 11px;
  color: var(--slate-500);
  display: block;
  margin-top: 2px;
}

.text-soil {
  color: var(--soil-700);
}

.text-sky {
  color: var(--sky-700);
}

.protocol-step-rows {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.protocol-step-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: var(--slate-50);
  border: 1px solid rgba(15, 23, 42, 0.06);
  border-radius: 6px;
  padding: 12px 14px;
}

.protocol-step-num {
  font-size: 11px;
  font-weight: 800;
  font-family: var(--font-swiss);
  color: var(--slate-700);
  background: #ffffff;
  border: 1px solid rgba(15, 23, 42, 0.12);
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.protocol-step-text {
  font-size: 12.5px;
  color: var(--slate-800);
  line-height: 1.55;
  margin: 0;
  flex: 1;
}

/* Explainability Ledger (Full-Width Table) */
.explainability-block {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
  width: 100%;
}

.explainability-header {
  padding: 12px 18px;
  background: var(--slate-50);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  gap: 10px;
}

.explainability-header h4 {
  font-size: 13px;
  font-weight: 700;
  color: var(--slate-900);
}

.explainability-header span {
  font-size: 11px;
  color: var(--slate-500);
  display: block;
}

.evidence-table-container {
  width: 100%;
  overflow-x: auto;
}

.evidence-table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  font-size: 12.5px;
}

.evidence-table th, .evidence-table td {
  padding: 10px 14px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
  word-break: break-word;
  overflow-wrap: break-word;
}

.evidence-table th {
  background: var(--slate-50);
  color: var(--slate-600);
  font-weight: 700;
  font-size: 11.5px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.evidence-table tr:last-child td {
  border-bottom: none;
}

.evidence-table code {
  color: var(--forest-800);
  font-weight: 600;
}

.explainability-impact {
  font-family: var(--font-editorial);
  font-style: italic;
  color: var(--forest-950);
  font-size: 13.5px;
  line-height: 1.45;
}

/* Unit Economics & Clinical Notice */
.economics-notice-strip {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  background: var(--slate-50);
  font-size: 12px;
}

.economics-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
  color: var(--slate-800);
  flex-wrap: wrap;
}

.clinical-disclaimer {
  color: var(--slate-600);
  line-height: 1.45;
  margin: 0;
}

.monographs-box {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  font-size: 11.5px;
}

.monograph-title {
  color: var(--slate-600);
  font-weight: 600;
}

.monograph-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

/* Telemetry Gauge Cards & Visual Meters */
.telemetry-gauge-card {
  margin-top: 10px;
  padding: 8px 10px;
  background: var(--slate-100);
  border-radius: var(--radius-sm);
  border: 1px solid var(--slate-200);
}

.gauge-bar-track {
  position: relative;
  height: 8px;
  background: var(--slate-200);
  border-radius: 4px;
  overflow: visible;
  margin-bottom: 4px;
}

.gauge-fill-alert {
  height: 100%;
  background: #c2410c;
  border-radius: 4px;
}

.gauge-threshold-marker {
  position: absolute;
  top: -3px;
  bottom: -3px;
  width: 2px;
  background: #0f172a;
  z-index: 2;
}

.gauge-ticks-row {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 9.5px;
  color: var(--slate-500);
}

.gauge-alert-text {
  color: #c2410c;
  font-weight: 700;
}

/* pH Meter Bar */
.ph-scale-track {
  position: relative;
  height: 8px;
  background: var(--slate-200);
  border-radius: 4px;
  margin-bottom: 4px;
}

.ph-range-ideal {
  position: absolute;
  top: 0;
  bottom: 0;
  background: rgba(22, 163, 74, 0.35);
  border-left: 1px solid rgba(22, 163, 74, 0.8);
  border-right: 1px solid rgba(22, 163, 74, 0.8);
}

.ph-indicator-pin {
  position: absolute;
  top: -4px;
  width: 3px;
  height: 16px;
  background: #0f172a;
  border-radius: 1.5px;
  transform: translateX(-50%);
  z-index: 3;
}

/* N-P-K Nutrient Bars */
.npk-tri-deck {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 10px;
}

.npk-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.npk-label {
  width: 72px;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  color: var(--slate-600);
}

.npk-bar-track {
  flex: 1;
  height: 6px;
  background: var(--slate-200);
  border-radius: 3px;
  overflow: hidden;
}

.npk-bar-fill {
  height: 100%;
  border-radius: 3px;
}

.npk-bar-fill.fill-low {
  background: #d97706;
}

.npk-bar-fill.fill-mod {
  background: #15803d;
}

.npk-status-val {
  width: 50px;
  text-align: right;
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--slate-600);
}

/* Sentinel-2 NDVI Reflectance Track */
.spectrum-gradient-track {
  position: relative;
  height: 8px;
  background: var(--slate-200);
  border-radius: 4px;
  margin-bottom: 4px;
}

.spectrum-pin {
  position: absolute;
  top: -4px;
  width: 3px;
  height: 16px;
  background: #0f172a;
  border-radius: 1.5px;
  transform: translateX(-50%);
  z-index: 2;
}

/* Optical Reticles for Specimen Viewfinder */
.reticle-corner {
  position: absolute;
  width: 14px;
  height: 14px;
  pointer-events: none;
  z-index: 4;
}

.reticle-tl {
  top: 12px;
  left: 12px;
  border-top: 2px solid rgba(255, 255, 255, 0.85);
  border-left: 2px solid rgba(255, 255, 255, 0.85);
}

.reticle-tr {
  top: 12px;
  right: 12px;
  border-top: 2px solid rgba(255, 255, 255, 0.85);
  border-right: 2px solid rgba(255, 255, 255, 0.85);
}

.reticle-bl {
  bottom: 12px;
  left: 12px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.85);
  border-left: 2px solid rgba(255, 255, 255, 0.85);
}

.reticle-br {
  bottom: 12px;
  right: 12px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.85);
  border-right: 2px solid rgba(255, 255, 255, 0.85);
}

.reticle-crosshair {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 24px;
  height: 24px;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 4;
}

.reticle-crosshair::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 1px;
  background: rgba(255, 255, 255, 0.4);
}

.reticle-crosshair::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  background: rgba(255, 255, 255, 0.4);
}

.reticle-telemetry {
  position: absolute;
  bottom: 10px;
  left: 12px;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  color: #38bdf8;
  letter-spacing: 0.05em;
  background: rgba(15, 23, 42, 0.85);
  padding: 2px 6px;
  border-radius: 2px;
  z-index: 4;
}

/* Audio STT Live Wave Visualizer */
.audio-wave-visualizer {
  display: inline-flex;
  align-items: center;
  gap: 2.5px;
  height: 12px;
  margin-left: 6px;
  vertical-align: middle;
}

.wave-bar {
  width: 2.5px;
  background: #dc2626;
  border-radius: 1px;
  animation: wavePulse 0.8s ease-in-out infinite alternate;
}

.wave-bar:nth-child(1) { height: 4px; animation-delay: 0.1s; }
.wave-bar:nth-child(2) { height: 10px; animation-delay: 0.25s; }
.wave-bar:nth-child(3) { height: 12px; animation-delay: 0.4s; }
.wave-bar:nth-child(4) { height: 8px; animation-delay: 0.15s; }
.wave-bar:nth-child(5) { height: 5px; animation-delay: 0.3s; }

@keyframes wavePulse {
  0% { transform: scaleY(0.4); }
  100% { transform: scaleY(1); }
}

/* 5-Segment Certainty Meter */
.match-score-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.certainty-segments {
  display: flex;
  align-items: center;
  gap: 2px;
}

.certainty-segments .segment {
  width: 6px;
  height: 10px;
  background: var(--slate-200);
  border-radius: 1px;
}

.certainty-segments .segment.active {
  background: #15803d;
}

/* Symptoms Clinical Grid */
.symptoms-clinical-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 6px;
}

.symptom-tag-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: var(--slate-100);
  border: 1px solid var(--slate-200);
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  color: var(--slate-700);
}

.symptom-pip {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #b91c1c;
}

/* Custom Audio Broadcast Player Deck */
.custom-audio-broadcast-deck {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 18px;
  background: var(--slate-900);
  border-radius: var(--radius-md);
  color: #ffffff;
  border: 1px solid var(--slate-800);
}

.btn-audio-circle {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: var(--forest-700);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
  transition: background 0.15s ease, transform 0.1s ease;
}

.btn-audio-circle:hover {
  background: var(--forest-800);
  transform: scale(1.04);
}

.audio-svg-icon {
  width: 18px;
  height: 18px;
}

.audio-deck-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.audio-title-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.audio-track-name {
  font-size: 12px;
  font-weight: 600;
  color: #f1f5f9;
  letter-spacing: 0.02em;
}

.broadcast-pulse {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #22c55e;
  margin-right: 6px;
  vertical-align: middle;
  animation: radioBlink 0.75s infinite;
}

@keyframes radioBlink {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.audio-timing-label {
  font-family: var(--font-mono);
  font-size: 11px;
  color: #94a3b8;
}

.audio-scrub-bar {
  width: 100%;
  height: 6px;
  background: #334155;
  border-radius: 3px;
  cursor: pointer;
  overflow: hidden;
  position: relative;
}

.audio-scrub-fill {
  height: 100%;
  background: #22c55e;
  border-radius: 3px;
}

.hidden-input-element,
.hidden-audio-element {
  display: none;
}

.marker-rh-82 {
  left: 82%;
}

.marker-ph-neutral {
  left: 50%;
}

.fill-n-35 {
  width: 35%;
}

.fill-p-28 {
  width: 28%;
}

.fill-k-62 {
  width: 62%;
}

/* Responsive Media Queries */
@media (max-width: 960px) {
  .diagnostic-lab-grid {
    grid-template-columns: 1fr;
  }
  .interventions-two-col-grid {
    grid-template-columns: 1fr;
  }
  .protocols-full-grid {
    grid-template-columns: 1fr;
  }
  .matrix-grid {
    grid-template-columns: 1fr;
  }
  .border-left-divider {
    border-left: none;
    border-top: 1px solid var(--color-border);
  }
}

@media (max-width: 640px) {
  .kisan-sathi-container {
    padding: 16px 12px;
    gap: 16px;
  }

  .farmer-context-card {
    padding: 14px;
  }

  .farmer-context-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 10px;
  }

  .profile-ribbon {
    padding: 14px;
    flex-wrap: wrap;
  }

  .profile-actions,
  .profile-actions > button {
    width: 100%;
  }

  .specimen-stage-frame {
    padding: 12px;
  }

  .specimen-viewfinder {
    height: min(58vw, 240px);
    min-height: 180px;
  }

  .benchmark-controls {
    padding: 12px;
  }

  .specimen-selector-bar {
    padding: 12px;
  }

  .segmented-specimen-group {
    grid-template-columns: minmax(0, 1fr);
  }

  .specimen-tab-btn {
    min-height: 40px;
    white-space: normal;
  }

  .btn-change-photo {
    flex-shrink: 0;
  }
}
</style>
