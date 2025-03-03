<template>
  <div class="map-widget-container">
    <div id="map"></div>

    <!-- Toggle Button -->
    <button class="panel-toggle" @click="isPanelOpen = !isPanelOpen">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path v-if="isPanelOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>
    
    <!-- Control Panel -->
    <div class="control-panel" :class="{ 'panel-closed': !isPanelOpen }">
      <div class="panel-header">
        <h2>Navigation Controls</h2>
      </div>
      
      <!-- Search Box -->
      <div class="search-group">
        <div class="group-label">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <span>Search Location</span>
        </div>
        <div class="search-box" v-click-outside="closeSearchResults">
          <input
            type="text"
            v-model="searchQuery"
            @input="handleSearch"
            @focus="showResults = true"
            placeholder="Search for a location..."
            class="search-input"
          />
          <div v-if="searchResults.length && showResults" class="search-results">
            <div
              v-for="result in searchResults"
              :key="result.id"
              class="search-result"
              @click="selectSearchResult(result)"
            >
              <div class="search-result-content">
                <div class="search-result-name">{{ result.name }}</div>
                <div class="search-result-address">{{ result.address }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Location Controls -->
      <div class="location-group">
        <div class="group-label">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          <span>Current Location</span>
        </div>
        <div class="button-group">
          <button @click="setCurrentLocation" class="btn btn-primary" :disabled="loading">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
            </svg>
            {{ loading ? 'Getting location...' : 'Use GPS' }}
          </button>
          <button @click="setLocationFromMap" class="btn btn-secondary">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5"/>
            </svg>
            Set on Map
          </button>
        </div>
      </div>

      <!-- Destination Controls -->
      <div class="location-group">
        <div class="group-label">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
          </svg>
          <span>Destination</span>
        </div>
        <button @click="setDestinationFromMap" class="btn btn-primary" :disabled="!currentMarker">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v10.764a1 1 0 01-1.447.894L15 18"/>
          </svg>
          Set Destination
        </button>
      </div>

      <!-- Map Style -->
      <div class="style-group">
        <div class="group-label">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
          </svg>
          <span>Map Style</span>
        </div>
        <select v-model="mapStyle" @change="handleStyleChange" class="style-select">
          <option value="mapbox://styles/mapbox/streets-v12">Streets</option>
          <option value="mapbox://styles/mapbox/outdoors-v12">Outdoors</option>
          <option value="mapbox://styles/mapbox/light-v11">Light</option>
          <option value="mapbox://styles/mapbox/dark-v11">Dark</option>
          <option value="mapbox://styles/mapbox/satellite-v9">Satellite</option>
        </select>
      </div>

      <!-- Clear Route -->
      <button 
        v-if="routeShown"
        @click="clearRoute" 
        class="btn btn-danger"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
        Clear Route
      </button>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="loading-spinner">Loading...</div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
      <button @click="errorMessage = ''" class="error-close">×</button>
    </div>

    <!-- Map Selection Indicator -->
    <div v-if="isSelectingDestination || isSelectingLocation" class="map-selection-indicator" :class="{ 'indicator-location': isSelectingLocation }">
      <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
      </svg>
      {{ isSelectingLocation ? 'Click anywhere on the map to set your current location' : 'Click anywhere on the map to set your destination' }}
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import mapboxgl from 'mapbox-gl'
import { useRuntimeConfig } from '#app'
import { isEqual } from 'lodash'
import services from '@/configs/services_info.json'

const config = useRuntimeConfig()
const map = ref(null)
const mapStyle = ref('mapbox://styles/mapbox/streets-v12')
const isPanelOpen = ref(true)
const loading = ref(false)
const currentMarker = ref(null)
const destinationMarker = ref(null)
const errorMessage = ref('')
const isSelectingDestination = ref(false)
const isSelectingLocation = ref(false)

const MAPBOX_SERVICE_URL = services['svc-mapbox'].url

// Local state management
const localState = reactive({
  places: [],
  directions: null,
  lastUpdate: null,
  currentLocation: null,
  destinationLocation: null
})

// Polling control
const pollInterval = ref(null)
const pollError = ref(null)
const consecutiveErrors = ref(0)
const maxRetries = 3
const basePollingInterval = 3000
const maxPollingInterval = 10000

// Search state
const searchQuery = ref('')
const searchResults = ref([])
const searchDebounceTimeout = ref(null)
const routeShown = ref(false)
const showResults = ref(false)

const defaultLocation = { lat: 21.0285, lng: 105.8542 } // Hanoi

// Click outside directive
const vClickOutside = {
  mounted(el, binding) {
    el._clickOutside = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) {
    document.removeEventListener('click', el._clickOutside)
  }
}

// Function to deep compare objects
const hasStateChanged = (newData, currentData) => {
  return !isEqual(newData, currentData)
}

const closeSearchResults = () => {
  showResults.value = false
}

const handleSearch = () => {
  if (searchDebounceTimeout.value) {
    clearTimeout(searchDebounceTimeout.value)
  }

  if (!searchQuery.value) {
    searchResults.value = []
    return
  }

  searchDebounceTimeout.value = setTimeout(async () => {
    try {
      const response = await fetch(
        `${MAPBOX_SERVICE_URL}/api/search/?query=${encodeURIComponent(searchQuery.value)}&limit=5&country=vn`
      )
      if (!response.ok) throw new Error('Search request failed')
      const data = await response.json()
      
      const newResults = data.suggestions.map(suggestion => ({
        id: suggestion.mapbox_id,
        name: suggestion.name,
        address: suggestion.full_address,
        display_text: `${suggestion.name} - ${suggestion.full_address}`,
        coordinates: {
          lng: suggestion.coordinates ? suggestion.coordinates.longitude : null,
          lat: suggestion.coordinates ? suggestion.coordinates.latitude : null
        }
      }))

      // Only update if results have changed
      if (hasStateChanged(newResults, searchResults.value)) {
        searchResults.value = newResults
      }
    } catch (error) {
      console.error('Search error:', error)
      showError('Search failed. Please try again.')
    }
  }, 300)
}

const addDestinationMarker = (coords) => {
  // Only update if position has changed
  const currentCoords = destinationMarker.value?.getLngLat()
  if (currentCoords && 
      currentCoords.lng === coords.lng && 
      currentCoords.lat === coords.lat) {
    return
  }

  if (destinationMarker.value) {
    destinationMarker.value.remove()
  }
  
  destinationMarker.value = new mapboxgl.Marker({
    color: '#f30',
    scale: 1.2
  })
  .setLngLat([coords.lng, coords.lat])
  .addTo(map.value)

  localState.destinationLocation = coords

  // Update route if we have both markers
  if (currentMarker.value) {
    updateRoute()
  }
}

const selectSearchResult = async (result) => {
  try {
    searchQuery.value = result.display_text
    searchResults.value = []
    showResults.value = false

    if (result.coordinates.lng && result.coordinates.lat) {
      addDestinationMarker(result.coordinates)
    } else {
      const response = await fetch(`${MAPBOX_SERVICE_URL}/api/retrieve/${result.id}`)
      if (!response.ok) throw new Error('Failed to get location details')
      const data = await response.json()
      
      const feature = data.features[0]
      if (feature && feature.properties.coordinates) {
        addDestinationMarker({
          lng: feature.properties.coordinates.longitude,
          lat: feature.properties.coordinates.latitude
        })
      } else {
        throw new Error('Location coordinates not found')
      }
    }
  } catch (error) {
    console.error('Error getting location details:', error)
    showError('Failed to set location. Please try again.')
  }
}

const showError = (message) => {
  errorMessage.value = message
  setTimeout(() => {
    errorMessage.value = ''
  }, 5000)
}

const initializeMap = async (coords) => {
  try {
    const accessToken = config.public.mapboxAccessToken
    if (!accessToken) {
      throw new Error('Mapbox access token is missing')
    }

    mapboxgl.accessToken = accessToken
    
    map.value = new mapboxgl.Map({
      container: 'map',
      style: mapStyle.value,
      center: [coords.lng, coords.lat],
      zoom: 13
    })

    map.value.addControl(new mapboxgl.NavigationControl(), 'top-right')
    map.value.addControl(new mapboxgl.ScaleControl({ maxWidth: 6.25, unit: 'metric' }))

    addCurrentLocationMarker(coords)
  } catch (error) {
    console.error('Map initialization error:', error)
    showError('Failed to initialize map. Please check your access token.')
  }
}

const getCurrentLocation = async (retryCount = 0) => {
  try {
    loading.value = true

    if (!navigator.geolocation) {
      throw new Error('Geolocation is not supported by your browser')
    }

    const position = await new Promise((resolve, reject) => {
      const geoOptions = {
        enableHighAccuracy: false,
        timeout: 5000,
        maximumAge: retryCount === 0 ? 30000 : 0
      }

      navigator.geolocation.getCurrentPosition(resolve, reject, geoOptions)
    })

    const coords = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    }

    localState.currentLocation = coords
    return coords
  } catch (error) {
    console.error('Location error:', error)
    if (error instanceof GeolocationPositionError) {
        switch (error.code) {
          case 1:
            showError('Please allow location access in your browser to use GPS.')
            return defaultLocation
          case 2:
            if (retryCount < 2) {
              await new Promise(resolve => setTimeout(resolve, 1000))
              return getCurrentLocation(retryCount + 1)
            }
            showError('Could not detect your location. Please check your GPS settings.')
            break
          case 3:
            if (retryCount < 2) {
              return getCurrentLocation(retryCount + 1)
            }
            showError('Location request timed out. Please try again.')
            break
          default:
            showError('Could not get your location. Please try again.')
        }
      } else {
        showError('Could not get your location. Please try again.')
      }
      return defaultLocation
    } finally {
      loading.value = false
    }
  }
  
  const setCurrentLocation = async () => {
    try {
      loading.value = true
      const coords = await getCurrentLocation()
      addCurrentLocationMarker(coords)
    } catch (error) {
      console.error('Error setting location:', error)
      showError('Failed to set current location')
    } finally {
      loading.value = false
    }
  }
  
  const addCurrentLocationMarker = (coords) => {
    // Only update if position has changed
    const currentCoords = currentMarker.value?.getLngLat()
    if (currentCoords && 
        currentCoords.lng === coords.lng && 
        currentCoords.lat === coords.lat) {
      return
    }
  
    if (currentMarker.value) {
      currentMarker.value.remove()
    }
    
    currentMarker.value = new mapboxgl.Marker({
      color: '#3887be',
      scale: 1.2,
      draggable: true
    })
    .setLngLat([coords.lng, coords.lat])
    .addTo(map.value)
  
    // Add drag end event listener
    currentMarker.value.on('dragend', () => {
      const newCoords = currentMarker.value.getLngLat()
      localState.currentLocation = {
        lng: newCoords.lng,
        lat: newCoords.lat
      }
      if (destinationMarker.value) {
        updateRoute()
      }
    })
  
    localState.currentLocation = coords
  
    // Update route if destination exists
    if (destinationMarker.value) {
      updateRoute()
    }
  }
  
  const setLocationFromMap = () => {
      if (!map.value) return
      
      isSelectingLocation.value = true
      map.value.getCanvas().style.cursor = 'crosshair'
      const onClick = (e) => {
        addCurrentLocationMarker({
          lng: e.lngLat.lng,
          lat: e.lngLat.lat
        })
        map.value.getCanvas().style.cursor = ''
        map.value.off('click', onClick)
        isSelectingLocation.value = false
      }
      map.value.on('click', onClick)
  }
  
  const setDestinationFromMap = () => {
      if (!map.value) return
      
      isSelectingDestination.value = true
      map.value.getCanvas().style.cursor = 'crosshair'
      
      const onClick = (e) => {
        const coords = {
          lng: e.lngLat.lng,
          lat: e.lngLat.lat
        }
        
        addDestinationMarker(coords)
        map.value.getCanvas().style.cursor = ''
        map.value.off('click', onClick)
        isSelectingDestination.value = false
      }
      map.value.on('click', onClick)
  }
  
  const updateRoute = async () => {
    if (!map.value || !currentMarker.value || !destinationMarker.value) return
  
    try {
      loading.value = true
      const start = currentMarker.value.getLngLat()
      const end = destinationMarker.value.getLngLat()
  
      const directions = await getDirections(start, end)
      
      // Only update if route has changed
      if (hasStateChanged(directions, localState.directions)) {
        localState.directions = directions
        await updateRouteVisualization(directions)
      }
    } catch (error) {
      console.error('Error getting directions:', error)
      showError('Could not calculate route')
    } finally {
      loading.value = false
    }
  }
  
  const updateRouteVisualization = async (directions) => {
    if (!directions.routes || !directions.routes[0]) return
  
    const route = {
      type: 'Feature',
      properties: {},
      geometry: directions.routes[0].geometry
    }
  
    const currentRouteSource = map.value.getSource('route')
    if (currentRouteSource) {
      const currentData = currentRouteSource.serialize()
      if (!isEqual(currentData.data, route)) {
        currentRouteSource.setData(route)
      }
    } else {
      // Initial route setup
      if (map.value.getSource('route')) {
        map.value.removeLayer('route')
        map.value.removeSource('route')
      }
  
      map.value.addSource('route', {
        type: 'geojson',
        data: route
      })
  
      map.value.addLayer({
        id: 'route',
        type: 'line',
        source: 'route',
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
  
    routeShown.value = true
  
    // Only adjust bounds if significant time has passed
    if (!localState.lastUpdate || 
        Date.now() - localState.lastUpdate > 5000) {
      const bounds = new mapboxgl.LngLatBounds()
      route.geometry.coordinates.forEach(coord => bounds.extend(coord))
      map.value.fitBounds(bounds, { padding: { top: 3.125, bottom: 3.125, left: 3.125, right: 3.125 } })
      localState.lastUpdate = Date.now()
    }
  }
  
  const getDirections = async (start, end) => {
    const accessToken = config.public.mapboxAccessToken
    const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${start.lng},${start.lat};${end.lng},${end.lat}?steps=true&geometries=geojson&access_token=${accessToken}`
  
    const response = await fetch(url)
    if (!response.ok) throw new Error('Network response was not ok')
    return response.json()
  }
  
  const clearRoute = () => {
    if (destinationMarker.value) {
      destinationMarker.value.remove()
      destinationMarker.value = null
    }
  
    if (map.value.getLayer('route')) {
      map.value.removeLayer('route')
    }
    if (map.value.getSource('route')) {
      map.value.removeSource('route')
    }
  
    localState.directions = null
    localState.destinationLocation = null
    routeShown.value = false
  }
  
  const handleStyleChange = () => {
    if (!map.value) return
    const style = mapStyle.value
    
    // Store current state
    const currentState = {
      currentLocation: localState.currentLocation,
      destinationLocation: localState.destinationLocation,
      directions: localState.directions
    }
    
    map.value.once('style.load', () => {
      // Restore markers
      if (currentState.currentLocation) {
        addCurrentLocationMarker(currentState.currentLocation)
      }
      
      if (currentState.destinationLocation) {
        addDestinationMarker(currentState.destinationLocation)
      }
      
      // Restore route if both markers exist
      if (currentState.directions && currentState.currentLocation && currentState.destinationLocation) {
        updateRouteVisualization(currentState.directions)
      }
    })
    
    map.value.setStyle(style)
  }
  
  // Enhanced Redis polling with exponential backoff
  const pollRedisChanges = async () => {
    try {
      // Check stored places
      const placesResponse = await fetch(`${MAPBOX_SERVICE_URL}/api/stored-places`)
      if (!placesResponse.ok) throw new Error('Failed to fetch stored places')
      const placesData = await placesResponse.json()
      
      if (placesData.success) {
        const newPlaces = placesData.places.map(place => ({
          id: place.mapbox_id,
          name: place.name,
          address: place.full_address,
          display_text: `${place.name} - ${place.full_address}`,
          coordinates: {
            lng: place.coordinates?.longitude,
            lat: place.coordinates?.latitude
          }
        }))
  
        // Only update if places have changed
        if (hasStateChanged(newPlaces, localState.places)) {
          localState.places = newPlaces
          
          if (newPlaces.length > 0) {
            searchResults.value = newPlaces
            showResults.value = true
            
            if (newPlaces.length === 1) {
              await selectSearchResult(newPlaces[0])
              searchResults.value = []
              showResults.value = false
            }
          } else {
            searchResults.value = []
            showResults.value = false
          }
        }
      }
  
      // Check stored directions
      const directionsResponse = await fetch(`${MAPBOX_SERVICE_URL}/api/stored-directions`)
      if (!directionsResponse.ok) throw new Error('Failed to fetch stored directions')
      const directionsData = await directionsResponse.json()
  
      if (directionsData.success && directionsData.directions) {
        // Only update if directions have changed
        if (hasStateChanged(directionsData.directions, localState.directions)) {
          localState.directions = directionsData.directions
          await updateRouteFromDirections(directionsData.directions)
        }
      }
  
      // Reset error counters on successful poll
      consecutiveErrors.value = 0
      pollError.value = null
      
      // Reset to base polling interval after successful request
      if (pollInterval.value) {
        clearInterval(pollInterval.value)
        pollInterval.value = setInterval(pollRedisChanges, basePollingInterval)
      }
  
    } catch (error) {
      console.error('Error polling Redis:', error)
      pollError.value = error
      
      // Implement exponential backoff
      consecutiveErrors.value++
      if (consecutiveErrors.value > maxRetries) {
        const newInterval = Math.min(
          basePollingInterval * Math.pow(2, consecutiveErrors.value - maxRetries),
          maxPollingInterval
        )
        
        if (pollInterval.value) {
          clearInterval(pollInterval.value)
          pollInterval.value = setInterval(pollRedisChanges, newInterval)
        }
      }
    }
  }
  
  const updateRouteFromDirections = async (directions) => {
    if (!map.value || !directions.routes || !directions.routes[0]) return
    
    try {
      const route = directions.routes[0]
      const endLeg = route.legs[0]
      if (!endLeg || !endLeg.steps.length) return

      // Get coordinates
      const lastStep = endLeg.steps[endLeg.steps.length - 1]
      const endCoords = lastStep.maneuver.location
      const firstStep = endLeg.steps[0]
      const startCoords = firstStep.maneuver.location

      // Update markers only if positions have changed
      const currentStartCoords = currentMarker.value?.getLngLat()
      const currentEndCoords = destinationMarker.value?.getLngLat()

      if (!currentStartCoords || 
          currentStartCoords.lng !== startCoords[0] || 
          currentStartCoords.lat !== startCoords[1]) {
        addCurrentLocationMarker({
          lng: startCoords[0],
          lat: startCoords[1]
        })
      }

      if (!currentEndCoords || 
          currentEndCoords.lng !== endCoords[0] || 
          currentEndCoords.lat !== endCoords[1]) {
        if (destinationMarker.value) destinationMarker.value.remove()
        destinationMarker.value = new mapboxgl.Marker({
          color: '#f30',
          scale: 1.2
        })
        .setLngLat(endCoords)
        .addTo(map.value)
      }

      // Update route visualization
      const geojson = {
        type: 'Feature',
        properties: {},
        geometry: route.geometry
      }

      // Check if route layer exists
      const currentRouteSource = map.value.getSource('route')
      if (currentRouteSource) {
        const currentData = currentRouteSource.serialize()
        if (!isEqual(currentData.data, geojson)) {
          currentRouteSource.setData(geojson)
        }
      } else {
        // Initial route setup
        map.value.addSource('route', {
          type: 'geojson',
          data: geojson
        })

        map.value.addLayer({
          id: 'route',
          type: 'line',
          source: 'route',
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

      routeShown.value = true

      // Only adjust bounds if significant time has passed
      if (!localState.lastUpdate || 
          Date.now() - localState.lastUpdate > 5000) {
        const bounds = new mapboxgl.LngLatBounds()
        geojson.geometry.coordinates.forEach(coord => bounds.extend(coord))
        map.value.fitBounds(bounds, { padding: { top: 3.125, bottom: 3.125, left: 3.125, right: 3.125 } })
        localState.lastUpdate = Date.now()
      }

    } catch (error) {
      console.error('Error updating route from directions:', error)
      showError('Failed to update route visualization')
    }
  }

  // Watch for errors to show notifications
  watch(pollError, (error) => {
    if (error) {
      showError(`Connection error: ${error.message}. Retrying...`)
    }
  })
  
  // Start polling on mount
  onMounted(async () => {
    const initialCoords = await getCurrentLocation()
    await initializeMap(initialCoords)
    
    // Initial poll and start interval
    await pollRedisChanges()
    pollInterval.value = setInterval(pollRedisChanges, basePollingInterval)
  })
  
  // Clean up on unmount
  onUnmounted(() => {
    if (pollInterval.value) {
      clearInterval(pollInterval.value)
    }
  })
</script>

<style>
.map-widget-container {
  position: relative;
  width: 100%;
  height: 100vh;
}

#map {
  width: 100%;
  height: 100%;
}

.control-panel {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  width: 100%;
  max-width: 20rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 0.75rem;
  box-shadow: 0 0.125rem 0.625rem rgba(0, 0, 0, 0.1);
  padding: 1rem;
  backdrop-filter: blur(0.625rem);
  border: 1px solid rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.panel-header {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.panel-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.location-group,
.style-group,
.search-group {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 0.5rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.group-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
  color: #4b5563;
}

.icon {
  width: 1.25rem;
  height: 1.25rem;
}

.button-group {
  display: flex;
  gap: 0.5rem;
}

.btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  justify-content: center;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  border: none;
}

.btn-primary:not(:disabled):hover {
  background: #2563eb;
}

.btn-secondary {
  background: white;
  color: #4b5563;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  background: #f3f4f6;
}

.btn-danger {
  background: #dc2626;
  color: white;
  border: none;
  margin-top: 0.5rem;
}

.btn-danger:hover {
  background: #b91c1c;
}

.style-select {
  width: 100%;
  padding: 0.5rem;
  border-radius: 0.375rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: white;
  color: #4b5563;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236B7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.loading-spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.625rem rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(0.25rem);
  z-index: 1100;
}

.search-box {
  position: relative;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 0.875rem;
  background: white;
  color: #4b5563;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.125rem rgba(59, 130, 246, 0.1);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border-radius: 0.375rem;
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
  margin-top: 0.25rem;
  max-height: 40vh;
  overflow-y: auto;
  z-index: 1000;
}

.search-result {
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.search-result:hover {
  background: #f3f4f6;
}

.search-result-content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.search-result-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1f2937;
}

.search-result-address {
  font-size: 0.75rem;
  color: #6b7280;
}

.error-message {
  position: fixed;
  bottom: 1.25rem;
  left: 50%;
  transform: translateX(-50%);
  background: #fee2e2;
  color: #dc2626;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: 0 0.125rem 0.625rem rgba(0, 0, 0, 0.1);
  animation: slideUp 0.3s ease;
  z-index: 1200;
}

.error-close {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.125rem;
  color: #dc2626;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
}

/* Custom scrollbar for search results */
.search-results::-webkit-scrollbar {
  width: 0.5rem;
}

.search-results::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 0.25rem;
}

.search-results::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 0.25rem;
}

.search-results::-webkit-scrollbar-thumb:hover {
  background: #666;
}

@keyframes slideUp {
  from {
    transform: translate(-50%, 100%);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}
  
/* Map Selection Indicator */
.map-selection-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(59, 130, 246, 0.9);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 0.125rem 0.625rem rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease;
  z-index: 1000;
  transition: background-color 0.3s ease;
}
  
.indicator-location {
  background: rgba(34, 197, 94, 0.9); /* Green color for location selection */
}
  
.map-selection-indicator .icon {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}
  
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, -40%);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%);
  }
}
  
/* Responsive styles */
@media (max-width: 640px) {
  .control-panel {
    top: auto;
    bottom: 1.25rem;
    right: 0.625rem;
    left: 0.625rem;
    width: auto;
    max-width: calc(100% - 1.25rem);
  }

  .button-group {
    flex-direction: column;
  }

  .error-message {
    width: calc(100% - 2.5rem);
    left: 1.25rem;
    transform: none;
  }

  .search-results {
    max-height: 25vh;
  }
}

/* Panel toggle button */
.panel-toggle {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  z-index: 1001;
  background: white;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  box-shadow: 0 0.125rem 0.625rem rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.panel-toggle:hover {
  background: #f3f4f6;
}

.panel-toggle .icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #4b5563;
}

/* Panel animation */
.control-panel {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.panel-closed {
  transform: translateX(calc(100% + 1.25rem));
  opacity: 0;
  pointer-events: none;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .panel-toggle {
    background: rgba(31, 41, 55, 0.95);
  }

  .panel-toggle:hover {
    background: rgba(55, 65, 81, 0.95);
  }

  .panel-toggle .icon {
    color: #e5e7eb;
  }

  .control-panel {
    background: rgba(31, 41, 55, 0.95);
    border-color: rgba(255, 255, 255, 0.1);
  }

  .panel-header h2 {
    color: #e5e7eb;
  }

  .location-group,
  .style-group,
  .search-group {
    background: rgba(31, 41, 55, 0.5);
    border-color: rgba(255, 255, 255, 0.1);
  }

  .group-label {
    color: #d1d5db;
  }

  .btn-secondary {
    background: rgba(31, 41, 55, 0.8);
    color: #e5e7eb;
    border-color: rgba(255, 255, 255, 0.1);
  }

  .btn-secondary:hover {
    background: rgba(55, 65, 81, 0.8);
  }

  .search-input,
  .style-select {
    background-color: rgba(31, 41, 55, 0.8);
    color: #e5e7eb;
    border-color: rgba(255, 255, 255, 0.1);
  }

  .search-results {
    background: rgba(31, 41, 55, 0.95);
  }

  .search-result:hover {
    background: rgba(55, 65, 81, 0.8);
  }

  .search-result-name {
    color: #e5e7eb;
  }

  .search-result-address {
    color: #9ca3af;
  }
}
</style>