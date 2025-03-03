<template>
  <div class="weather-widget">
    <div class="weather-container" :class="{ 'has-data': weather }">
      <!-- Error Display -->
      <transition name="fade">
        <div v-if="error" class="error-message" role="alert">
          <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          {{ error }}
        </div>
      </transition>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-indicator">
          <div class="loading-ring">
            <div></div><div></div><div></div><div></div>
          </div>
          <span class="loading-text">{{ loadingMessage }}</span>
        </div>
      </div>

      <!-- Weather Display -->
      <transition name="fade">
        <div v-if="weather" class="weather-content">
          <!-- Location & Refresh -->
          <div class="header-row">
            <h2 class="location-name">{{ location }}</h2>
            <button @click="refreshWeather" class="refresh-button" aria-label="Refresh weather">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 12a9 9 0 11-9-9c2.52 0 4.85.99 6.57 2.57L21 8"/>
                <path d="M21 3v5h-5"/>
              </svg>
            </button>
          </div>

          <!-- Main Weather Info -->
          <div class="main-weather">
            <div class="temperature-display">
              <span class="current-temp">{{ Math.round(weather.temperature) }}°</span>
              <span class="weather-icon">{{ getWeatherIcon(weather.weathercode) }}</span>
            </div>
            <div class="weather-description">
              {{ getWeatherDescription(weather.weathercode) }}
              <span class="feels-like">Feels like {{ Math.round(weather.apparent_temperature) }}°</span>
            </div>
          </div>

          <!-- Weather Details -->
          <div class="weather-metrics">
            <div class="metric-item">
              <svg xmlns="http://www.w3.org/2000/svg" class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 3v18M8 6l8 0M8 10l8 0M8 14l8 0M8 18l8 0"/>
              </svg>
              <span>{{ Math.round(weather.relative_humidity) }}%</span>
            </div>
            <div class="metric-item">
              <svg xmlns="http://www.w3.org/2000/svg" class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2"/>
              </svg>
              <span>{{ formatWind(weather.wind_speed) }}</span>
            </div>
            <div class="metric-item">
              <svg xmlns="http://www.w3.org/2000/svg" class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 2v6M12 22v-6M4.93 4.93l4.24 4.24M14.83 14.83l4.24 4.24M2 12h6M16 12h6M4.93 19.07l4.24-4.24M14.83 9.17l4.24-4.24"/>
              </svg>
              <span>{{ formatPrecipitation(weather.precipitation) }}</span>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const location = ref(null)
const weather = ref(null)
const loading = ref(false)
const error = ref(null)
const loadingMessage = ref('Updating weather...')
const updateInterval = ref(null)
const isRetrying = ref(false)
const retryCount = ref(0)
const maxRetries = 3

const weatherCodes = {
  0: { description: 'Clear sky', icon: '☀️' },
  1: { description: 'Mainly clear', icon: '🌤️' },
  2: { description: 'Partly cloudy', icon: '⛅' },
  3: { description: 'Overcast', icon: '☁️' },
  45: { description: 'Foggy', icon: '🌫️' },
  48: { description: 'Depositing rime fog', icon: '🌫️' },
  51: { description: 'Light drizzle', icon: '🌦️' },
  53: { description: 'Moderate drizzle', icon: '🌦️' },
  55: { description: 'Dense drizzle', icon: '🌧️' },
  61: { description: 'Light rain', icon: '🌧️' },
  63: { description: 'Moderate rain', icon: '🌧️' },
  65: { description: 'Heavy rain', icon: '⛈️' },
  71: { description: 'Light snow', icon: '🌨️' },
  73: { description: 'Moderate snow', icon: '🌨️' },
  75: { description: 'Heavy snow', icon: '🌨️' },
  77: { description: 'Snow grains', icon: '❄️' },
  80: { description: 'Light rain showers', icon: '🌦️' },
  81: { description: 'Moderate rain showers', icon: '🌧️' },
  82: { description: 'Violent rain showers', icon: '⛈️' },
  95: { description: 'Thunderstorm', icon: '⚡' }
}

const getWeatherIcon = (code) => {
  return weatherCodes[code]?.icon || '❓'
}

const getWeatherDescription = (code) => {
  return weatherCodes[code]?.description || 'Unknown'
}

const formatWind = (speed) => {
  if (typeof speed !== 'number') return 'N/A'
  return `${Math.round(speed)} km/h`
}

const formatPrecipitation = (precip) => {
  if (typeof precip !== 'number') return 'N/A'
  return precip === 0 ? 'None' : `${precip.toFixed(1)} mm`
}

const getCurrentPosition = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported'))
      return
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve(position)
      },
      (err) => {
        reject(err)
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // 5 minutes
      }
    )
  })
}

const getWeatherData = async () => {
  try {
    loading.value = true
    error.value = null
    loadingMessage.value = 'Getting location...'

    const position = await getCurrentPosition()
    const { latitude, longitude } = position.coords

    // Get location name
    loadingMessage.value = 'Getting location details...'
    const locationResponse = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`,
      {
        headers: {
          'Accept-Language': 'en-US,en;q=0.9',
          'User-Agent': 'WeatherWidget/1.0'
        }
      }
    )

    if (!locationResponse.ok) {
      throw new Error(`Location service error: ${locationResponse.status}`)
    }

    const locationData = await locationResponse.json()
    location.value = locationData.address.city || 
                     locationData.address.town || 
                     locationData.address.village || 
                     locationData.display_name

    // Get weather data
    loadingMessage.value = 'Fetching weather data...'
    const weatherResponse = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m`
    )

    if (!weatherResponse.ok) {
      throw new Error(`Weather service error: ${weatherResponse.status}`)
    }

    const weatherData = await weatherResponse.json()

    if (!weatherData.current) {
      throw new Error('Invalid weather data received')
    }

    weather.value = {
      temperature: weatherData.current.temperature_2m,
      weathercode: weatherData.current.weather_code,
      wind_speed: weatherData.current.wind_speed_10m,
      relative_humidity: weatherData.current.relative_humidity_2m,
      apparent_temperature: weatherData.current.apparent_temperature,
      precipitation: weatherData.current.precipitation
    }

    retryCount.value = 0
    isRetrying.value = false
  } catch (err) {
    console.error('Weather error:', err)
    error.value = handleError(err)

    // Implement retry logic
    if (retryCount.value < maxRetries && !isRetrying.value) {
      isRetrying.value = true
      retryCount.value++
      setTimeout(() => {
        isRetrying.value = false
        getWeatherData()
      }, 3000)
    }
  } finally {
    loading.value = false
    loadingMessage.value = ''
  }
}

const handleError = (err) => {
  if (err.code === 1) {
    return 'Location access denied'
  } else if (err.code === 2) {
    return 'Location unavailable'
  } else if (err.code === 3 || err.message.includes('timeout')) {
    return 'Request timed out'
  } else if (err.message.includes('Location service')) {
    return 'Location service error'
  } else if (err.message.includes('Weather service')) {
    return 'Weather service error'
  }
  return 'Unable to update weather'
}

const refreshWeather = () => {
  weather.value = null
  location.value = null
  getWeatherData()
}

// Initialize weather updates
onMounted(() => {
  getWeatherData()
  // Update weather every 15 minutes
  updateInterval.value = setInterval(getWeatherData, 900000)
})

onUnmounted(() => {
  if (updateInterval.value) {
    clearInterval(updateInterval.value)
  }
})
</script>

<style scoped>
.weather-widget {
  height: 100%;
  padding: clamp(1rem, 5%, 2rem);
  max-width: 100vw;
}

.weather-container {
  min-height: 30vh;
  height: 100%;
  background: rgba(15, 23, 42, 0.95);
  border-radius: clamp(1rem, 3vw, 1.5rem);
  padding: clamp(1rem, 5%, 2rem);
  position: relative;
  backdrop-filter: blur(0.75rem);
  border: 1px solid rgba(51, 65, 85, 0.5);
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Error Message */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.75em;
  padding: 1em;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #f87171;
  border-radius: 0.75em;
  font-size: clamp(0.875rem, 2vw, 1rem);
  margin-bottom: 1em;
}

.error-icon {
  width: 1.5em;
  height: 1.5em;
  flex-shrink: 0;
}

/* Loading State */
.loading-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40vh;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1em;
}

.loading-text {
  color: #94a3b8;
  font-size: 0.875em;
}

.loading-ring {
  display: inline-block;
  position: relative;
  width: 3em;
  height: 3em;
}

.loading-ring div {
  box-sizing: border-box;
  display: block;
  position: absolute;
  width: 2.4em;
  height: 2.4em;
  margin: 0.3em;
  border: 0.2em solid #3b82f6;
  border-radius: 50%;
  animation: loading-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  border-color: #3b82f6 transparent transparent transparent;
}

.loading-ring div:nth-child(1) { animation-delay: -0.45s; }
.loading-ring div:nth-child(2) { animation-delay: -0.3s; }
.loading-ring div:nth-child(3) { animation-delay: -0.15s; }

/* Initial State */
.initial-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.5rem;
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border: 0.0625rem solid rgba(59, 130, 246, 0.2);
  border-radius: 0.75rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background: rgba(59, 130, 246, 0.15);
  transform: translateY(-0.0625rem);
}

.location-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Weather Content */
.weather-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.location-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.refresh-button {
  width: clamp(2.25rem, 8vw, 3rem);
  height: clamp(2.25rem, 8vw, 3rem);
  min-width: 2.25rem; /* Ensure minimum touch target size */
  min-height: 2.25rem;
  border: none;
  background: rgba(51, 65, 85, 0.5);
  color: #94a3b8;
  border-radius: 0.75em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.refresh-button:hover {
  background: rgba(71, 85, 105, 0.5);
  color: #e2e8f0;
  transform: translateY(-1px);
}

.refresh-button svg {
  width: clamp(1rem, 4vw, 1.25rem);
  height: clamp(1rem, 4vw, 1.25rem);
}

/* Main Weather Display */
.main-weather {
  text-align: center;
  padding: clamp(1rem, 5%, 2rem);
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1em;
  border: 1px solid rgba(51, 65, 85, 0.5);
}

.temperature-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(0.5rem, 3vw, 1rem);
}

.current-temp {
  font-size: clamp(2rem, 8vw, 3.5rem);
  font-weight: 700;
  color: #e2e8f0;
  line-height: 1;
}

.weather-icon {
  font-size: clamp(2rem, 8vw, 3.5rem);
  line-height: 1;
}

.weather-description {
  margin-top: 0.75em;
  color: #94a3b8;
  font-size: clamp(0.875rem, 2.5vw, 1rem);
  display: flex;
  flex-direction: column;
  gap: 0.25em;
}

.feels-like {
  font-size: clamp(0.75rem, 2vw, 0.875rem);
  color: #64748b;
}

/* Weather Metrics */
.weather-metrics {
  display: flex;
  justify-content: space-around;
  padding: clamp(0.75rem, 3%, 1.25rem);
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1em;
  border: 1px solid rgba(51, 65, 85, 0.5);
  gap: clamp(0.5rem, 2vw, 1rem);
}

.metric-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5em;
  color: #94a3b8;
  font-size: clamp(0.75rem, 2vw, 0.875rem);
  flex: 1;
  min-width: max-content;
  padding: clamp(0.25em, 1vw, 0.5em);
}

.metric-icon {
  width: clamp(1.25rem, 4vw, 1.5rem);
  height: clamp(1.25rem, 4vw, 1.5rem);
  color: #3b82f6;
}

/* Animations */
@keyframes loading-ring {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(0.625rem);
}

/* Light Mode Support */
@media (prefers-color-scheme: light) {
  .weather-container {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .location-name {
    color: #1e293b;
  }

  .main-weather {
    background: rgba(248, 250, 252, 0.8);
  }

  .current-temp {
    color: #1e293b;
  }

  .weather-metrics {
    background: rgba(248, 250, 252, 0.8);
  }
}

/* Touch Device Optimizations */
@media (hover: none) and (pointer: coarse) {
  .refresh-button {
    min-height: 2.75rem;
    min-width: 2.75rem;
  }

  .action-button {
    min-height: 2.75rem;
    padding: 0.75rem 1.5rem;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .weather-container {
    background: white;
    border: 0.125rem solid black;
  }

  .location-name {
    color: black;
  }

  .main-weather,
  .weather-metrics {
    background: white;
    border: 0.125rem solid black;
  }

  .current-temp {
    color: black;
  }

  .refresh-button {
    background: white;
    border: 0.125rem solid black;
    color: black;
  }
}
</style>