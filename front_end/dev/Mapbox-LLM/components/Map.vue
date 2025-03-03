<template>
  <div class="app-container">
    <MapBox
      ref="mapRef"
      :map-style="mapStyle"
      @destination-selected="handleDestinationSelected"
      @step-clicked="handleStepClicked"
    />
    
    <Dashboard
      v-if="mapRef"
      :mapRef="mapRef"
      :distance="routeStats.distance"
      :duration="routeStats.duration"
      @style-changed="handleStyleChanged"
      @profile-changed="handleProfileChanged"
      @clear-route="handleClearRoute"
      @location-selected="handleLocationSelected"
      @destination-selected="handleDestinationSelected"
      @auto-update-changed="handleAutoUpdateChanged"
    />
    
    <RouteInstructions
      :show="!!routeData"
      :route-data="routeData"
      :error="routeError"
      @step-selected="handleStepSelected"
      @step-hover="handleStepHover"
    />
    
    <div class="loading-indicator" :class="{ active: loading }" role="alert" aria-live="polite">
      <div class="loading-spinner"></div>
      <span>Loading...</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useMap } from '@/composables/useMap'
import mapboxgl from 'mapbox-gl'
import MapBox from '@/components/MapBox.vue'
import Dashboard from '@/components/Dashboard.vue'
import RouteInstructions from '@/components/RouteInstructions.vue'

const mapRef = ref(null)
const { api } = useMap()

const loading = ref(false)
const mapStyle = ref('mapbox://styles/mapbox/streets-v12')
const routeProfile = ref('driving')
const routeData = ref(null)
const routeError = ref(false)
const routeStats = ref({
  distance: 0,
  duration: 0
})
const isAutoUpdateEnabled = ref(true)
const updateInterval = ref(30)

let checkCacheInterval
let lastPlacesCache = null
let lastDirectionsCache = null
let directionUpdateInterval

// Event handlers
const handleStyleChanged = (style) => {
  mapStyle.value = style
  showNotification('Map style updated', 'success')
}

const handleProfileChanged = async (profile) => {
  routeProfile.value = profile
  if (routeData.value) {
    await updateRoute()
    showNotification('Travel mode updated', 'success')
  }
}

const handleDestinationSelected = async (coordinates) => {
  try {
    loading.value = true
    // Update the destination marker
    mapRef.value?.updateDestinationMarker({
      lng: coordinates.longitude,
      lat: coordinates.latitude
    })
    // Update the route
    await updateRoute(coordinates)
    showNotification('Route updated', 'success')
  } catch (error) {
    console.error('Error updating route:', error)
    showNotification('Failed to update route', 'error')
    routeError.value = true
  } finally {
    loading.value = false
  }
}

const handleClearRoute = () => {
  routeData.value = null
  routeError.value = false
  routeStats.value = { distance: 0, duration: 0 }
  if (mapRef.value) {
    mapRef.value.clearRoute()
  }
  showNotification('Route cleared', 'success')
}

const handleStepSelected = ({ index, step }) => {
  if (!mapRef.value?.map?.value || !step.maneuver?.location) return;
  
  const mapInstance = mapRef.value.map.value;
  
  // Only proceed if we have a valid map instance
  if (mapInstance && typeof mapInstance.flyTo === 'function') {
    mapInstance.flyTo({
      center: step.maneuver.location,
      zoom: 16,
      duration: 1000
    });
  }

  // Also check if highlightStepMarker exists before calling
  if (mapRef.value?.highlightStepMarker) {
    mapRef.value.highlightStepMarker(index);
  }
};

const handleStepHover = (index) => {
  if (mapRef.value?.highlightStepMarker) {
    mapRef.value.highlightStepMarker(index)
  }
}

const handleStepClicked = ({ index, step }) => {
  if (!mapRef.value?.map?.value || !step.maneuver?.location) return;
  
  const mapInstance = mapRef.value.map.value;
  
  if (mapInstance && typeof mapInstance.flyTo === 'function') {
    mapInstance.flyTo({
      center: step.maneuver.location,
      zoom: 16,
      duration: 1000
    });
  }
};

// Route handling
async function updateRoute(destination) {
  if (!destination) return
  
  try {
    loading.value = true
    const currentLocation = mapRef.value?.getCurrentLocation()
    if (!currentLocation) {
      throw new Error('Current location not available')
    }

    const response = await api.directions.getRoute({
      start_lng: String(currentLocation.lng),
      start_lat: String(currentLocation.lat),
      end_lng: String(destination.longitude),
      end_lat: String(destination.latitude),
      profile: routeProfile.value
    })

    routeData.value = response
    routeStats.value = {
      distance: response.routes[0].distance,
      duration: response.routes[0].duration
    }
    routeError.value = false

    // Update map route and markers
    if (mapRef.value) {
      mapRef.value.drawRoute(response.routes[0].geometry, response)
    }
  } catch (error) {
    console.error('Error getting directions:', error)
    routeError.value = true
    throw error
  } finally {
    loading.value = false
  }
}

async function visualizeCachedDirections(directions) {
  if (!mapRef.value || !directions?.routes?.[0]) return
  
  try {
    loading.value = true
    const route = directions.routes[0]
    
    // Check if route has valid data
    if (!route.legs?.[0]?.steps?.length) {
      console.warn('Invalid route data structure')
      return
    }
    
    // Create end marker from the last step of the first leg
    const lastStep = route.legs[0].steps[route.legs[0].steps.length - 1]
    if (lastStep?.maneuver?.location) {
      const [lng, lat] = lastStep.maneuver.location
      mapRef.value.updateDestinationMarker({
        lng,
        lat
      })
    }
    
    // Update route visualization if geometry exists
    if (route.geometry) {
      mapRef.value.drawRoute(route.geometry)
    }
    
    // Update route data and stats
    routeData.value = directions
    routeStats.value = {
      distance: route.distance || 0,
      duration: route.duration || 0
    }
    
    // Fit map to show the entire route
    if (route.geometry?.coordinates?.length) {
      const bounds = new mapboxgl.LngLatBounds()
      route.geometry.coordinates.forEach(coord => bounds.extend(coord))
      
      // Check if map instance exists before fitting bounds
      const mapInstance = mapRef.value?.map?.value
      if (mapInstance && typeof mapInstance.fitBounds === 'function') {
        mapInstance.fitBounds(bounds, {
          padding: 50,
          duration: 1000
        })
      }
    }
    
    showNotification('Cached route loaded', 'success')
  } catch (error) {
    console.error('Error visualizing cached directions:', error)
    showNotification('Failed to load cached route', 'error')
  } finally {
    loading.value = false
  }
}

// Auto-update handling
const handleAutoUpdateChanged = ({ enabled, interval }) => {
  isAutoUpdateEnabled.value = enabled
  updateInterval.value = interval

  if (directionUpdateInterval) {
    clearInterval(directionUpdateInterval)
    directionUpdateInterval = null
  }

  if (enabled) {
    directionUpdateInterval = setInterval(async () => {
      await autoUpdateRoute()
    }, interval * 1000)
  }
}

async function autoUpdateRoute() {
  if (!isAutoUpdateEnabled.value) return

  if (!routeData.value || !mapRef.value) return

  try {
    const currentLocation = mapRef.value.getCurrentLocation()
    if (!currentLocation) return

    const lastDestination = routeData.value.waypoints?.[1]?.location
    if (!lastDestination) return

    const response = await api.directions.getRoute({
      start_lng: String(currentLocation.lng),
      start_lat: String(currentLocation.lat),
      end_lng: String(lastDestination[0]),
      end_lat: String(lastDestination[1]),
      profile: routeProfile.value
    })

    routeData.value = response
    routeStats.value = {
      distance: response.routes[0].distance,
      duration: response.routes[0].duration
    }

    if (mapRef.value) {
      mapRef.value.drawRoute(response.routes[0].geometry, response)
    }

    showNotification('Route updated', 'info')
  } catch (error) {
    console.error('Error auto-updating route:', error)
  }
}

const handleLocationSelected = async (location) => {
  if (mapRef.value) {
    mapRef.value.updateCurrentLocationMarker(location)
    
    // If we have an existing route, update it with the new start location
    if (routeData.value?.waypoints?.[1]?.location) {
      try {
        loading.value = true
        const destination = routeData.value.waypoints[1].location
        
        const response = await api.directions.getRoute({
          start_lng: String(location.lng),
          start_lat: String(location.lat),
          end_lng: String(destination[0]),
          end_lat: String(destination[1]),
          profile: routeProfile.value
        })

        routeData.value = response
        routeStats.value = {
          distance: response.routes[0].distance,
          duration: response.routes[0].duration
        }
        routeError.value = false

        // Update map route and markers
        if (mapRef.value) {
          mapRef.value.drawRoute(response.routes[0].geometry, response)
        }
        
        showNotification('Route updated with new starting point', 'success')
      } catch (error) {
        console.error('Error updating route:', error)
        showNotification('Failed to update route', 'error')
        routeError.value = true
      } finally {
        loading.value = false
      }
    }
  }
}

// Cache checking
async function checkCachedData() {
  if (!mapRef.value) return

  try {
    const placesResponse = await api.places.getStoredPlaces()
    if (placesResponse?.places && 
        JSON.stringify(placesResponse.places) !== JSON.stringify(lastPlacesCache)) {
      lastPlacesCache = placesResponse.places
      if (placesResponse.places.length > 0) {
        showNotification('New places available', 'info')
      }
    }

    const directionsResponse = await api.directions.getStoredDirections()
    if (directionsResponse?.success && directionsResponse.directions &&
        JSON.stringify(directionsResponse.directions) !== JSON.stringify(lastDirectionsCache)) {
      lastDirectionsCache = directionsResponse.directions
      await visualizeCachedDirections(directionsResponse.directions)
    }
  } catch (error) {
    console.error('Error checking cached data:', error)
  }
}

// Notifications
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

// Lifecycle
onMounted(async () => {
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  checkCacheInterval = setInterval(async () => {
    await checkCachedData()
  }, 3000)

  directionUpdateInterval = setInterval(async () => {
    await autoUpdateRoute()
  }, updateInterval.value * 1000)
})

onUnmounted(() => {
  if (checkCacheInterval) {
    clearInterval(checkCacheInterval)
  }
  if (directionUpdateInterval) {
    clearInterval(directionUpdateInterval)
  }
})
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
  position: relative;
}

.loading-indicator {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--panel-background);
  padding: 20px 40px;
  border-radius: 12px;
  box-shadow: var(--panel-shadow);
  display: none;
  z-index: 1000;
  border: 1px solid var(--border-color);
  color: var(--text-color);
}

.loading-indicator.active {
  display: flex;
  align-items: center;
  gap: 12px;
  animation: fadeIn 0.3s ease;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}
</style>