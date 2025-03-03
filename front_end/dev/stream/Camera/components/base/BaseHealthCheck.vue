<template>
  <div class="space-y-4">    
    <!-- Health Check Button -->
    <button
      @click="checkHealth"
      :disabled="isLoading || !isConfigured"
      class="w-full sm:w-auto min-h-[44px] sm:min-h-0 px-6 py-3 sm:py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-base font-medium transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      :aria-busy="isLoading"
      :aria-label="`Check ${serverType} health status`"
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
      <span>{{ isLoading ? `Checking ${serverType}...` : `Check ${serverType} Health` }}</span>
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
            {{ serverType }} Status: {{ healthStatus.ok ? 'Healthy' : 'Unhealthy' }}
          </h3>
        </div>

        <!-- Status Message -->
        <div v-if="healthStatus.message" class="mt-2 text-sm sm:text-base">
          {{ healthStatus.message }}
        </div>

        <!-- Extra Stats Slot -->
        <slot name="stats"></slot>

        <!-- Last Check Time -->
        <div class="mt-2 text-xs text-gray-600">
          Last checked: {{ lastCheckTime }}
        </div>
      </div>
    </div>

    <!-- Not Configured Warning -->
    <div 
      v-if="!isConfigured" 
      class="text-sm text-gray-600 italic"
    >
      Please configure {{ serverType.toLowerCase() }} connection first
    </div>

    <!-- Error Slot -->
    <slot name="error"></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  serverType: string
  isConfigured: boolean
  checkFn: () => Promise<{ ok: boolean, message: string }>
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'health-checked'): void
}>()

const isLoading = ref(false)
const healthStatus = ref<{ ok: boolean, message: string } | null>(null)
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
  if (!props.isConfigured) {
    healthStatus.value = {
      ok: false,
      message: `Please apply ${props.serverType.toLowerCase()} configuration first`
    }
    return
  }

  healthStatus.value = null
  isLoading.value = true
  
  try {
    healthStatus.value = await props.checkFn()
    emit('health-checked')
  } catch (error) {
    healthStatus.value = {
      ok: false,
      message: error instanceof Error ? error.message : 'Unknown error occurred'
    }
  } finally {
    isLoading.value = false
    lastCheckTimestamp.value = Date.now()
  }
}

// Expose the checkHealth function to parent components
defineExpose({ checkHealth })
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