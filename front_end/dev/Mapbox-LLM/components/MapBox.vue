<template>
  <div class="map-container">
    <div id="map" ref="mapContainer" role="application" aria-label="Interactive map"></div>
    
    <SearchBox @location-selected="handleSearchLocationSelected" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import mapboxgl from 'mapbox-gl'
import { useMap } from '@/composables/useMap'
import SearchBox from './SearchBox.vue'

const props = defineProps({
  mapStyle: {
    type: String,
    default: 'mapbox://styles/mapbox/streets-v12'
  }
})

const emit = defineEmits([
  'destination-selected',
  'location-selected',
  'step-clicked'
])

const { map, initializeMap, getCurrentLocation, api } = useMap()

const mapContainer = ref(null)
const currentMarker = ref(null)
const destinationMarker = ref(null)
const isSettingLocation = ref(false)
const isSettingDestination = ref(false)
const loading = ref(false)
const stepMarkers = ref([])

const getCustomIcon = (type, instruction, isStart, isEnd) => {
  // Base styles for all icons
  const baseStyle = `
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #2196F3;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  `;

  // Determine icon based on specific instruction text
  const instructionLower = instruction?.toLowerCase() || '';

  // Check for specific maneuver types
  if (instructionLower.includes('drive north') || instructionLower.includes('drive south')) {
    return `
      <div style="${baseStyle}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
          <path d="M12 4v16M12 4l-4 4m4-4l4 4" stroke="white" stroke-width="2"/>
        </svg>
      </div>
    `;
  }

  if (instructionLower.includes('turn left')) {
    return `
      <div style="${baseStyle}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
          <path d="M15 19l-7-7 7-7" stroke="white" stroke-width="2"/>
        </svg>
      </div>
    `;
  }

  if (instructionLower.includes('turn right')) {
    return `
      <div style="${baseStyle}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
          <path d="M9 5l7 7-7 7" stroke="white" stroke-width="2"/>
        </svg>
      </div>
    `;
  }

  if (instructionLower.includes('enter') && instructionLower.includes('roundabout')) {
    return `
      <div style="${baseStyle}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white">
          <circle cx="12" cy="12" r="6" stroke-width="2"/>
          <path d="M12 6v6l4-4" stroke-width="2"/>
        </svg>
      </div>
    `;
  }

  if (instructionLower.includes('exit') && instructionLower.includes('roundabout')) {
    return `
      <div style="${baseStyle}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white">
          <circle cx="12" cy="12" r="6" stroke-width="2"/>
          <path d="M12 12l4-4" stroke-width="2"/>
        </svg>
      </div>
    `;
  }

  // Default straight icon for any unmatched instructions
  return `
    <div style="${baseStyle}">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
        <path d="M12 4v16M12 4l-4 4m4-4l4 4" stroke="white" stroke-width="2"/>
      </svg>
    </div>
  `;
};

const visualizeRouteSteps = (routeData) => {
  clearStepMarkers();
  
  if (!routeData?.routes?.[0]?.legs?.[0]?.steps) return;
  
  const steps = routeData.routes[0].legs[0].steps;
  
  steps.forEach((step, index) => {
    if (!step.maneuver?.location) return;
    
    // Create marker element
    const el = document.createElement('div');
    el.className = 'step-marker';
    
    // Get icon based only on maneuver instruction
    const icon = getCustomIcon(step.maneuver.type, step.maneuver.instruction);
    el.innerHTML = icon;
    
    // Create popup
    const popup = new mapboxgl.Popup({
      offset: 25,
      closeButton: false,
      className: 'step-popup'
    })
    .setHTML(`
      <div class="step-instruction">
        <p>${step.maneuver.instruction}</p>
        ${step.distance ? `<small>${formatDistance(step.distance)}</small>` : ''}
      </div>
    `);
    
    // Create marker
    const marker = new mapboxgl.Marker({
      element: el,
      anchor: 'center'
    })
    .setLngLat(step.maneuver.location)
    .setPopup(popup)
    .addTo(map.value);
    
    stepMarkers.value.push(marker);
  });
};

const clearStepMarkers = () => {
  stepMarkers.value.forEach(marker => marker.remove())
  stepMarkers.value = []
}

const highlightStepMarker = (index) => {
  stepMarkers.value.forEach((marker, i) => {
    const el = marker.getElement()
    if (i === index) {
      el.classList.add('highlighted')
      marker.getPopup().addTo(map.value)
    } else {
      el.classList.remove('highlighted')
      marker.getPopup().remove()
    }
  })
}

onMounted(async () => {
  const currentLocation = await getCurrentLocation()
  if (currentLocation && mapContainer.value) {
    const mapInstance = await initializeMap('map', currentLocation)
    map.value = await initializeMap('map', currentLocation)

    currentMarker.value = new mapboxgl.Marker({
      color: '#3887be',
      scale: 1.2,
      draggable: true
    })
    .setLngLat([currentLocation.lng, currentLocation.lat])
    .addTo(map.value)
  }

  // Map click handlers
  map.value?.on('click', (e) => {
    if (isSettingLocation.value) {
      handleLocationClick(e)
    }

    if (isSettingDestination.value) {
      handleDestinationClick(e)
    }
  })
})

function handleLocationClick(e) {
  const coords = {
    lng: e.lngLat.lng,
    lat: e.lngLat.lat
  }
  
  if (currentMarker.value) {
    currentMarker.value.remove()
  }
  
  currentMarker.value = new mapboxgl.Marker({
    color: '#3887be',
    scale: 1.2,
    draggable: true
  })
  .setLngLat(coords)
  .addTo(map.value)

  currentMarker.value.on('dragend', () => {
    const lngLat = currentMarker.value.getLngLat()
    emit('location-selected', {
      lng: lngLat.lng,
      lat: lngLat.lat
    })
  })

  isSettingLocation.value = false
  map.value.getCanvas().style.cursor = ''
  showNotification('Location set from map', 'success')
  emit('location-selected', coords)
}

function handleDestinationClick(e) {
  const coords = {
    longitude: e.lngLat.lng,
    latitude: e.lngLat.lat
  }
  
  if (destinationMarker.value) {
    destinationMarker.value.setLngLat([coords.longitude, coords.latitude])
  } else {
    destinationMarker.value = new mapboxgl.Marker({
      color: '#f30',
      scale: 1.2
    })
    .setLngLat([coords.longitude, coords.latitude])
    .addTo(map.value)
  }

  isSettingDestination.value = false
  map.value.getCanvas().style.cursor = ''
  showNotification('Destination set from map', 'success')
  emit('destination-selected', coords)
}

const handleSearchLocationSelected = (coordinates) => {
  try {
    if (destinationMarker.value) {
      destinationMarker.value.remove()
    }
    destinationMarker.value = new mapboxgl.Marker({
      color: '#f30',
      scale: 1.2
    })
    .setLngLat([coordinates.longitude, coordinates.latitude])
    .addTo(map.value)
    
    emit('destination-selected', coordinates)
    
    if (map.value) {
      map.value.flyTo({
        center: [coordinates.longitude, coordinates.latitude],
        zoom: 15,
        essential: true
      })
    }
  } catch (error) {
    console.error('Error selecting location:', error)
    showNotification('Failed to select location', 'error')
  }
}

function formatDistance(meters) {
  if (!meters) return ''
  if (meters < 1000) return `${Math.round(meters)}m away`
  return `${(meters/1000).toFixed(1)}km away`
}

function enableLocationSelection() {
  isSettingLocation.value = true
  if (map.value) {
    map.value.getCanvas().style.cursor = 'crosshair'
    showNotification('Click on the map to set your location', 'info')
  }
}

function enableDestinationSelection() {
  isSettingDestination.value = true
  if (map.value) {
    map.value.getCanvas().style.cursor = 'crosshair'
    showNotification('Click on the map to set destination', 'info')
  }
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

// Expose methods for parent component
defineExpose({
  getCurrentLocation: () => {
    if (!currentMarker.value) return null
    const lngLat = currentMarker.value.getLngLat()
    return { lng: lngLat.lng, lat: lngLat.lat }
  },
  updateCurrentLocationMarker: (location) => {
    if (currentMarker.value) {
      currentMarker.value.remove()
    }
    currentMarker.value = new mapboxgl.Marker({
      color: '#3887be',
      scale: 1.2,
      draggable: true
    })
    .setLngLat([location.lng, location.lat])
    .addTo(map.value)
  },
  updateDestinationMarker: (location) => {
    if (destinationMarker.value) {
      destinationMarker.value.remove()
    }
    destinationMarker.value = new mapboxgl.Marker({
      color: '#f30',
      scale: 1.2
    })
    .setLngLat([location.lng ?? location.longitude, location.lat ?? location.latitude])
    .addTo(map.value)

    return destinationMarker.value
  },
  clearRoute: () => {
    if (destinationMarker.value) {
      destinationMarker.value.remove()
      destinationMarker.value = null
    }
    clearStepMarkers()
    if (map.value?.getLayer('route')) {
      map.value.removeLayer('route')
    }
    if (map.value?.getSource('route')) {
      map.value.removeSource('route')
    }
  },
  drawRoute: (geometry, routeData) => {
    const geojson = {
      type: 'Feature',
      properties: {},
      geometry
    }

    if (map.value?.getSource('route')) {
      map.value.getSource('route').setData(geojson)
    } else {
      map.value?.addLayer({
        id: 'route',
        type: 'line',
        source: {
          type: 'geojson',
          data: geojson
        },
        layout: {
          'line-join': 'round',
          'line-cap': 'round'
        },
        paint: {
          'line-color': '#3887be',
          'line-width': 5,
          'line-opacity': 0.75
        }
      })
    }

    if (routeData) {
      visualizeRouteSteps(routeData)
    }
  },
  enableLocationSelection,
  enableDestinationSelection,
  highlightStepMarker,
  map: computed(() => map.value),
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
  position: relative;
}

#map {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 100%;
}

/* Route visualization styles */
.step-marker {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.step-marker:hover {
  transform: scale(1.1);
}

.step-marker.highlighted {
  transform: scale(1.2);
  z-index: 2;
}

.step-popup {
  max-width: 250px;
}

.step-popup .mapboxgl-popup-content {
  padding: 12px;
  border-radius: 8px;
  font-family: var(--font-primary);
}

.step-instruction {
  font-family: var(--font-primary);
}

.step-instruction p {
  margin: 0 0 4px 0;
  font-size: 13px;
  color: var(--text-color);
}

.step-instruction small {
  color: var(--text-secondary);
  font-size: 12px;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {  
  .step-marker {
    border-color: rgba(0, 0, 0, 0.25);
  }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .step-marker {
    width: 24px;
    height: 24px;
  }
  
  .step-number {
    font-size: 12px;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .step-marker {
    transition: none;
  }
}
</style>