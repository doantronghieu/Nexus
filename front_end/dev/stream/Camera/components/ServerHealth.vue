<template>
  <div class="space-y-4">    
    <!-- Health Check Button -->
    <button
      @click="checkHealth"
      :disabled="isLoading || !serverStore.isConfigured"
      class="w-full sm:w-auto min-h-[44px] sm:min-h-0 px-6 py-3 sm:py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-base font-medium transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      :aria-busy="isLoading"
      aria-label="Check server health status"
    >
      <svg 
        v-if="isLoading"
        class="animate-spin h-5 w-5 text-white" 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24"
      >
        <circle 
          class="opacity-25" 
          cx="12" 
          cy="12" 
          r="10" 
          stroke="currentColor" 
          stroke-width="4"
        />
        <path 
          class="opacity-75" 
          fill="currentColor" 
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
      <span>{{ isLoading ? 'Checking...' : 'Check Server Health' }}</span>
    </button>

    <!-- Health Status Display -->
    <div v-if="healthStatus" class="animate-fadeIn">
      <div
        :class="[
          'p-4 rounded-lg border transition-colors duration-200',
          healthStatus.ok 
            ? 'bg-green-50 border-green-200 text-green-800' 
            : 'bg-red-50 border-red-200 text-red-800'
        ]"
      >
        <!-- Status Header -->
        <div class="flex items-center gap-3 mb-2">
          <div 
            :class="[
              'flex-shrink-0 w-4 h-4 rounded-full',
              healthStatus.ok ? 'bg-green-500' : 'bg-red-500'
            ]"
          />
          <h3 class="font-semibold">
            Status: {{ healthStatus.ok ? 'Healthy' : 'Unhealthy' }}
          </h3>
        </div>

        <!-- Status Message -->
        <div v-if="healthStatus.message" class="mt-2 text-sm sm:text-base">
          {{ healthStatus.message }}
        </div>

        <!-- Last Check Time -->
        <div class="mt-2 text-xs text-gray-600">
          Last checked: {{ lastCheckTime }}
        </div>
      </div>
    </div>

    <!-- Not Configured Warning -->
    <div 
      v-if="!serverStore.isConfigured" 
      class="text-sm text-gray-600 italic"
    >
      Please configure server connection first
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useServerStore } from '@/stores/server'

interface HealthStatus {
  ok: boolean
  message: string
}

const serverStore = useServerStore()
const isLoading = ref(false)
const healthStatus = ref<HealthStatus | null>(null)
const lastCheckTimestamp = ref<number | null>(null)

// Format the last check time
const lastCheckTime = computed(() => {
  if (!lastCheckTimestamp.value) return ''
  
  const date = new Date(lastCheckTimestamp.value)
  return date.toLocaleTimeString(undefined, { 
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
})

const checkHealth = async () => {
  if (!serverStore.isConfigured) {
    healthStatus.value = {
      ok: false,
      message: 'Please apply server configuration first'
    }
    return { ok: false, message: 'Server not configured' }
  }

  healthStatus.value = null
  isLoading.value = true
  
  try {
    const response = await fetch(`${serverStore.getHttpUrl}/health`, {
      headers: {
        'Accept': 'application/json',
        'ngrok-skip-browser-warning': 'true'
      }
    })
    
    const contentType = response.headers.get('content-type')
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Server returned non-JSON response')
    }
    
    const data = await response.json()
    
    const result = {
      ok: response.ok && data.status === 'healthy',
      message: data.status === 'healthy' 
        ? 'Server is responding normally' 
        : 'Server returned unexpected status'
    }
    
    healthStatus.value = result
    lastCheckTimestamp.value = Date.now()
    return result

  } catch (error) {
    const result = {
      ok: false,
      message: error instanceof Error ? error.message : 'Unknown error occurred'
    }
    healthStatus.value = result
    return result
  } finally {
    isLoading.value = false
  }
}

// Expose the checkHealth function and health status to parent components
defineExpose({ 
  checkHealth,
  healthStatus: computed(() => healthStatus.value)
})
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile touch improvements */
@media (max-width: 640px) {
  button {
    -webkit-tap-highlight-color: transparent;
  }
}
</style>