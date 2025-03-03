<template>
  <div class="search-container panel" :class="{ 'is-searching': isSearching }">
    <div class="search-wrapper">
      <div class="search-input-group">
        <!-- Search Icon -->
        <svg 
          class="search-icon"
          xmlns="http://www.w3.org/2000/svg" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>

        <!-- Search Input -->
        <input 
          v-model="searchQuery" 
          type="text" 
          class="search-box" 
          :class="{ 'has-value': searchQuery.length > 0 }"
          placeholder="Search for a location..." 
          @input="handleSearchInput"
          @focus="isSearching = true"
          @blur="handleSearchBlur"
        >

        <!-- Clear Button -->
        <button 
          v-if="searchQuery.length > 0"
          class="clear-button"
          @click="clearSearch"
          aria-label="Clear search"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Saved Places Button -->
        <button 
          class="saved-places-button" 
          :class="{ 'has-saved': cachedPlaces.length > 0 }"
          @click="toggleCacheDropdown"
          aria-label="Show saved places"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
          </svg>
          <span v-if="cachedPlaces.length > 0" class="cache-count">{{ cachedPlaces.length }}</span>
        </button>
      </div>

      <!-- Search Results -->
      <div 
        v-show="showSearchResults && searchResults.length > 0" 
        class="search-results"
        role="listbox"
      >
        <div class="results-header">
          <span>Search Results</span>
          <small>{{ searchResults.length }} locations found</small>
        </div>

        <div class="results-list">
          <button
            v-for="result in searchResults" 
            :key="result.mapbox_id"
            class="search-result-item"
            @click="selectSearchResult(result)"
            role="option"
          >
            <div class="result-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <div class="result-content">
              <div class="result-name">{{ result.name }}</div>
              <div class="result-address">{{ result.full_address }}</div>
              <div class="result-distance">{{ formatDistance(result.distance) }}</div>
            </div>
          </button>
        </div>
      </div>

      <!-- No Results Message -->
      <div 
        v-if="showSearchResults && searchQuery.length >= 3 && searchResults.length === 0" 
        class="no-results"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 20a8 8 0 100-16 8 8 0 000 16z" />
        </svg>
        <p>No locations found for "{{ searchQuery }}"</p>
      </div>

      <!-- Saved Places Dropdown -->
      <div 
        v-show="showCacheDropdown" 
        class="cache-dropdown"
        role="listbox"
      >
        <div class="cache-header">
          <span>Saved Places</span>
          <small>{{ cachedPlaces.length }} locations saved</small>
        </div>

        <div class="cache-list">
          <button
            v-for="place in cachedPlaces" 
            :key="place.mapbox_id"
            class="cache-item"
            @click="selectCachedPlace(place)"
            role="option"
          >
            <div class="place-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
              </svg>
            </div>
            <div class="place-content">
              <div class="place-name">{{ place.name }}</div>
              <div class="place-address">{{ place.place_formatted }}</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMap } from '@/composables/useMap'

const emit = defineEmits(['location-selected'])

const { api, getCurrentLocation } = useMap()

const searchQuery = ref('')
const searchResults = ref([])
const showSearchResults = ref(false)
const cachedPlaces = ref([])
const showCacheDropdown = ref(false)
const isSearching = ref(false)

let searchTimeout

// Search handling
function clearSearch() {
  searchQuery.value = ''
  searchResults.value = []
  showSearchResults.value = false
}

function handleSearchBlur() {
  setTimeout(() => {
    isSearching.value = false
  }, 200)
}

async function handleSearchInput() {
  showCacheDropdown.value = false
  
  clearTimeout(searchTimeout)
  const query = searchQuery.value.trim()
  
  if (query.length < 3) {
    showSearchResults.value = false
    return
  }

  searchTimeout = setTimeout(() => performSearch(query), 300)
}

async function performSearch(query) {
  try {
    const currentLoc = await getCurrentLocation()
    const params = {
      query,
      language: 'en',
      limit: '5',
      country: 'vn',
      proximity_lng: String(currentLoc.lng),
      proximity_lat: String(currentLoc.lat)
    }

    const data = await api.places.search(params)
    searchResults.value = data.suggestions.sort((a, b) => a.distance - b.distance)
    showSearchResults.value = true
  } catch (error) {
    console.error('Search error:', error)
    showNotification('Failed to search locations', 'error')
  }
}

async function selectSearchResult(result) {
  try {
    const data = await api.places.getDetails(result.mapbox_id)
    const feature = data.features[0]
    const coordinates = feature.properties.coordinates
    
    emit('location-selected', coordinates)
    clearSearch()
  } catch (error) {
    console.error('Error selecting location:', error)
    showNotification('Failed to select location', 'error')
  }
}

// Cache handling
function toggleCacheDropdown(event) {
  event.stopPropagation()
  showCacheDropdown.value = !showCacheDropdown.value
  showSearchResults.value = false
}

async function checkCachedPlaces() {
  try {
    const data = await api.places.getStoredPlaces()
    if (data.places && data.places.length > 0) {
      cachedPlaces.value = data.places
    }
  } catch (error) {
    console.error('Error checking cached places:', error)
  }
}

function selectCachedPlace(place) {
  showCacheDropdown.value = false
  selectSearchResult({
    ...place,
    mapbox_id: place.mapbox_id,
    distance: 0,
    full_address: place.place_formatted
  })
}

// Utilities
function formatDistance(meters) {
  if (!meters) return ''
  if (meters < 1000) return `${Math.round(meters)}m away`
  return `${(meters/1000).toFixed(1)}km away`
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

// Initialize
checkCachedPlaces()
</script>

<style scoped>
.search-container {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 400px;
  z-index: 1;
  padding: 16px;
  transition: all 0.3s ease;
}

.search-container.is-searching {
  width: 480px;
}

.search-wrapper {
  position: relative;
  width: 100%;
}

.search-input-group {
  position: relative;
  display: flex;
  align-items: center;
  background: var(--background-color);
  border: 2px solid var(--border-color);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.search-input-group:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
}

.search-icon {
  width: 20px;
  height: 20px;
  color: var(--text-secondary);
  margin: 0 12px;
  flex-shrink: 0;
}

.search-box {
  flex: 1;
  padding: 14px 0;
  border: none;
  font-size: 15px;
  background: transparent;
  color: var(--text-color);
  outline: none;
}

.search-box::placeholder {
  color: var(--text-secondary);
  opacity: 0.7;
}

.clear-button,
.saved-places-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  margin: 0 6px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-button svg,
.saved-places-button svg {
  width: 18px;
  height: 18px;
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.clear-button:hover,
.saved-places-button:hover {
  background: rgba(0, 0, 0, 0.05);
}

.clear-button:hover svg,
.saved-places-button:hover svg {
  color: var(--text-color);
}

.saved-places-button {
  position: relative;
  margin-right: 8px;
}

.saved-places-button.has-saved svg {
  color: var(--primary-color);
}

.cache-count {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--error-color);
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 10px;
  font-weight: 600;
}

.search-results,
.cache-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: var(--panel-background);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: var(--panel-shadow);
  overflow: hidden;
  animation: slideDown 0.2s ease;
}

.results-header,
.cache-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
}

.results-header span,
.cache-header span {
  font-weight: 600;
  color: var(--text-color);
}

.results-header small,
.cache-header small {
  color: var(--text-secondary);
  font-size: 12px;
}

.results-list,
.cache-list {
  max-height: 320px;
  overflow-y: auto;
}

.search-result-item,
.cache-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 12px 16px;
  border: none;
  background: transparent;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
  border-bottom: 1px solid var(--border-color);
}

.search-result-item:last-child,
.cache-item:last-child {
  border-bottom: none;
}

.result-icon,
.place-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--primary-color);
  border-radius: 8px;
  margin-right: 12px;
  flex-shrink: 0;
}

.result-icon svg,
.place-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.result-content,
.place-content {
  flex: 1;
  min-width: 0;
}

.result-name,
.place-name {
  font-weight: 500;
  color: var(--text-color);
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-address,
.place-address {
  font-size: 13px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-distance {
  font-size: 12px;
  color: var(--primary-color);
  margin-top: 2px;
}

.search-result-item:hover,
.cache-item:hover {
  background: rgba(37, 99, 235, 0.05);
  transform: translateX(4px);
}

.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 32px 16px;
  text-align: center;
  color: var(--text-secondary);
}

.no-results svg {
  width: 32px;
  height: 32px;
  color: var(--text-secondary);
  opacity: 0.5;
}

.no-results p {
  margin: 0;
  font-size: 14px;
}

/* Animations */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .search-container {
    width: calc(100% - 32px);
    margin: 16px;
    left: 0;
    transform: none;
  }

  .search-container.is-searching {
    width: calc(100% - 32px);
  }

  .search-input-group {
    border-width: 1px;
  }

  .search-box {
    font-size: 14px;
    padding: 12px 0;
  }

  .clear-button,
  .saved-places-button {
    width: 32px;
    height: 32px;
  }

  .results-list,
  .cache-list {
    max-height: 260px;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .search-input-group {
    background: rgba(255, 255, 255, 0.05);
  }

  .clear-button:hover,
  .saved-places-button:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .search-result-item:hover,
  .cache-item:hover {
    background: rgba(255, 255, 255, 0.05);
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .search-container,
  .search-input-group,
  .search-result-item,
  .cache-item {
    transition: none;
  }
}
</style>