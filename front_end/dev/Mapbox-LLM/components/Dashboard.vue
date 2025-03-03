<template>
  <div id="dashboard" class="panel" role="complementary" aria-label="Route controls">
    <!-- Navigation Controls Section -->
    <div class="control-group">
      <div class="section-header">
        <svg xmlns="http://www.w3.org/2000/svg" class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
        </svg>
        <h2>Navigation Controls</h2>
      </div>

      <div class="navigation-controls">
        <!-- Current Location Controls -->
        <div class="location-group">
          <div class="group-label">
            <svg xmlns="http://www.w3.org/2000/svg" class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            <span>Current Location</span>
          </div>
          <div class="button-group">
            <button 
              @click="setCurrentLocation" 
              class="button-primary"
              :disabled="loading"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="button-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              </svg>
              {{ loading ? 'Getting location...' : 'Use GPS' }}
            </button>
            <button @click="setLocationFromMap" class="button-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" class="button-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5"/>
              </svg>
              Set on Map
            </button>
          </div>
        </div>

        <!-- Destination Controls -->
        <div class="location-group">
          <div class="group-label">
            <svg xmlns="http://www.w3.org/2000/svg" class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
            </svg>
            <span>Destination</span>
          </div>
          <div class="button-group">
            <button @click="setDestinationFromMap" class="button-primary">
              <svg xmlns="http://www.w3.org/2000/svg" class="button-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v10.764a1 1 0 01-1.447.894L15 18"/>
              </svg>
              Set Destination
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Map Style Section -->
    <div class="control-group">
      <div class="section-header">
        <svg xmlns="http://www.w3.org/2000/svg" class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
        </svg>
        <h2>Map Style</h2>
      </div>
      <div class="select-wrapper">
        <select 
          id="map-style" 
          v-model="selectedMapStyle"
          @change="$emit('style-changed', selectedMapStyle)"
        >
          <option value="mapbox://styles/mapbox/streets-v12">Streets</option>
          <option value="mapbox://styles/mapbox/outdoors-v12">Outdoors</option>
          <option value="mapbox://styles/mapbox/light-v11">Light</option>
          <option value="mapbox://styles/mapbox/dark-v11">Dark</option>
          <option value="mapbox://styles/mapbox/satellite-v9">Satellite</option>
        </select>
        <svg xmlns="http://www.w3.org/2000/svg" class="select-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </div>
    </div>

    <!-- Travel Mode Section -->
    <div class="control-group">
      <div class="section-header">
        <svg xmlns="http://www.w3.org/2000/svg" class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0"/>
        </svg>
        <h2>Travel Mode</h2>
      </div>
      <div class="travel-mode-buttons">
        <button 
          v-for="mode in travelModes" 
          :key="mode.value"
          @click="selectTravelMode(mode.value)"
          :class="['mode-button', { active: selectedProfile === mode.value }]"
        >
          <span class="mode-icon" v-html="mode.icon"></span>
          {{ mode.label }}
        </button>
      </div>
    </div>

    <!-- Clear Route Button -->
    <div class="control-group">
      <button 
        class="button-danger"
        @click="$emit('clear-route')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="button-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
        Clear Route
      </button>
    </div>

    <!-- Auto Update Section -->
    <div class="control-group">
      <div class="section-header">
        <svg xmlns="http://www.w3.org/2000/svg" class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        <h2>Auto Update</h2>
      </div>
      <div class="auto-update-controls">
        <label class="toggle-label">
          <input 
            type="checkbox" 
            v-model="autoUpdate"
            @change="handleAutoUpdateChange"
          >
          <span class="toggle-switch"></span>
          <span class="toggle-text">Auto update route</span>
        </label>
        
        <div class="duration-control" v-if="autoUpdate">
          <label for="update-interval">Update interval (seconds)</label>
          <div class="duration-input">
            <input 
              type="number" 
              id="update-interval"
              v-model="updateInterval"
              min="5"
              max="300"
              @change="handleIntervalChange"
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMap } from '@/composables/useMap'
import mapboxgl from 'mapbox-gl'

const props = defineProps({
  mapRef: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  'style-changed',
  'profile-changed',
  'clear-route',
  'location-selected',
  'destination-selected',
  'auto-update-changed',
  'update-interval-changed'
])

const {
  map, updateCurrentLocationMarker, updateDestinationMarker,
  getCurrentLocation, setManualLocation
} = useMap()

const selectedMapStyle = ref('mapbox://styles/mapbox/streets-v12')
const selectedProfile = ref('driving')
const isSettingLocation = ref(false)
const isSettingDestination = ref(false)
const autoUpdate = ref(true)
const updateInterval = ref(30)
const currentMarker = ref(null)
const isLocationOverridden = ref(false)
const manualLocation = ref(null)
const loading = ref(false)

const travelModes = [
  {
    value: 'driving',
    label: 'Driving',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"/>
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0"/>
    </svg>`
  },
  {
    value: 'cycling',
    label: 'Cycling',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <circle cx="5.5" cy="17.5" r="3.5"/>
      <circle cx="18.5" cy="17.5" r="3.5"/>
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 6a1 1 0 100-2 1 1 0 000 2zm-3 11.5v-7l-3-3 4-3 2 3h2"/>
    </svg>`
  },
  {
    value: 'walking',
    label: 'Walking',
    icon: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <circle cx="13" cy="4" r="2"/>
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 21v-4.5L12 15l1-4.5L9 9v3l2.5 2.5V21M9 21v-3l-2-2"/>
    </svg>`
  }
]

async function setCurrentLocation() {
  try {
    loading.value = true
    const location = await getCurrentLocation()
    if (!location) {
      throw new Error('Failed to get location')
    }

    const mapInstance = props.mapRef?.map
    if (!mapInstance) {
      throw new Error('Map not initialized')
    }

    if (currentMarker.value) {
      currentMarker.value.remove()
    }
    
    currentMarker.value = new mapboxgl.Marker({
      color: '#3887be',
      scale: 1.2,
      draggable: true
    })
    .setLngLat([location.lng, location.lat])
    .addTo(mapInstance)

    currentMarker.value.on('dragend', async () => {
      const lngLat = currentMarker.value.getLngLat()
      manualLocation.value = { lng: lngLat.lng, lat: lngLat.lat }
      isLocationOverridden.value = true
      showNotification('Location manually set', 'success')
      emit('location-selected', manualLocation.value)
    })

    mapInstance.flyTo({
      center: [location.lng, location.lat],
      zoom: 15
    })

    showNotification('Using current location', 'success')
    emit('location-selected', location)
  } catch (error) {
    console.error('Error setting current location:', error)
    showNotification('Failed to set current location', 'error')
  } finally {
    loading.value = false
  }
}

function setLocationFromMap() {
  if (props.mapRef) {
    props.mapRef.enableLocationSelection()
  }
}

function setDestinationFromMap() {
  if (props.mapRef) {
    props.mapRef.enableDestinationSelection()
  }
}

function selectTravelMode(mode) {
  selectedProfile.value = mode
  emit('profile-changed', mode)
}

function handleAutoUpdateChange() {
  emit('auto-update-changed', {
    enabled: autoUpdate.value,
    interval: updateInterval.value
  })
}

function handleIntervalChange() {
  if (updateInterval.value < 5) updateInterval.value = 5
  if (updateInterval.value > 300) updateInterval.value = 300

  emit('auto-update-changed', {
    enabled: autoUpdate.value,
    interval: updateInterval.value
  })
}

function showNotification(message, type = 'info') {
  const notification = document.createElement('div')
  notification.className = `notification ${type}`
  notification.textContent = message
  notification.style.position = 'fixed'
  notification.style.top = '20px'
  notification.style.left = '50%'
  notification.style.transform = 'translateX(-50%)'
  notification.style.padding = '12px 24px'
  notification.style.borderRadius = '8px'
  notification.style.background = 'var(--panel-background)'
  notification.style.border = '1px solid var(--border-color)'
  notification.style.zIndex = '1000'
  notification.style.animation = 'fadeIn 0.3s ease'

  document.body.appendChild(notification)
  
  setTimeout(() => {
    notification.style.animation = 'fadeOut 0.3s ease'
    setTimeout(() => {
      document.body.removeChild(notification)
    }, 300)
  }, 3000)
}
</script>

<style scoped>
#dashboard {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 340px;
  z-index: 1;
  transition: all 0.3s ease;
}

.control-group {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
}

.navigation-controls {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.location-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: rgba(37, 99, 235, 0.05);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.group-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-color);
  font-size: 14px;
  font-weight: 500;
}

.label-icon {
  width: 16px;
  height: 16px;
  color: var(--primary-color);
}

.button-group {
  display: flex;
  gap: 8px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-icon {
  width: 20px;
  height: 20px;
  color: var(--primary-color);
}

h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
}

.button-primary,
.button-secondary,
.button-danger {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  height: 36px;
}

.button-primary {
  background: var(--primary-color);
  color: white;
  border: none;
}

.button-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.button-primary:disabled:hover {
  transform: none;
}

.button-primary:hover {
  background: var(--hover-color);
  transform: translateY(-1px);
}

.button-secondary {
  background: var(--background-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
}

.button-secondary:hover {
  background: rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

.button-danger {
  background: var(--error-color);
  color: white;
  border: none;
  width: 100%;
}

.button-danger:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.button-icon {
  width: 14px;
  height: 14px;
}

.select-wrapper {
  position: relative;
}

select {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 14px;
  background: var(--background-color);
  color: var(--text-color);
  appearance: none;
  cursor: pointer;
}

.select-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
  pointer-events: none;
}

.travel-mode-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.mode-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--background-color);
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.mode-button.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.mode-button:hover {
  transform: translateY(-1px);
}

.mode-icon {
  width: 20px;
  height: 20px;
}

.mode-icon svg {
  width: 20px;
  height: 20px;
}

.auto-update-controls {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
  background: var(--border-color);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.toggle-switch::after {
  content: '';
  position: absolute;
  left: 2px;
  top: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: all 0.2s ease;
}

input[type="checkbox"]:checked + .toggle-switch {
  background: var(--primary-color);
}

input[type="checkbox"]:checked + .toggle-switch::after {
  left: 22px;
}

input[type="checkbox"] {
  display: none;
}

.toggle-text {
  font-size: 14px;
  color: var(--text-color);
}

.duration-control {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.duration-control label {
  font-size: 14px;
  color: var(--text-secondary);
}

.duration-input input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-color);
}

@media (max-width: 768px) {
  #dashboard {
    width: calc(100% - 20px);
    margin: 10px;
    bottom: 10px;
    top: auto;
    right: 0;
  }

  .button-group {
    flex-direction: row;
  }

  .button-group .button-primary,
  .button-group .button-secondary {
    font-size: 12px;
    padding: 8px;
  }

  .travel-mode-buttons {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (prefers-color-scheme: dark) {
  .location-group {
    background: rgba(255, 255, 255, 0.05);
  }

  .mode-button:not(.active) {
    background: rgba(255, 255, 255, 0.05);
  }

  .select-wrapper select {
    background: rgba(255, 255, 255, 0.05);
  }

  .button-secondary {
    background: rgba(255, 255, 255, 0.05);
  }
}

@media (prefers-reduced-motion: reduce) {
  .button-primary,
  .button-secondary,
  .mode-button,
  .toggle-switch,
  .toggle-switch::after {
    transition: none;
  }
}
</style>