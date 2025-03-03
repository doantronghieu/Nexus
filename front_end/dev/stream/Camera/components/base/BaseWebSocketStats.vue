<template>
  <div class="space-y-4">
    <!-- Header Section -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <h3 class="text-lg font-medium">{{ title }}</h3>
      <button
        @click="togglePolling"
        :disabled="!isConfigured"
        class="inline-flex items-center justify-center min-h-[44px] sm:min-h-0 px-4 py-2 rounded-lg text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        :class="[
          isPolling
            ? 'bg-red-100 text-red-700 hover:bg-red-200 focus:ring-red-500'
            : 'bg-green-100 text-green-700 hover:bg-green-200 focus:ring-green-500',
          !isConfigured && 'opacity-50 cursor-not-allowed'
        ]"
      >
        {{ isPolling ? 'Stop Auto-Refresh' : 'Start Auto-Refresh' }}
      </button>
    </div>

    <!-- Error State -->
    <div 
      v-if="error" 
      class="p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 text-sm sm:text-base"
    >
      {{ error }}
    </div>

    <!-- Loading State -->
    <div 
      v-else-if="isLoading && !stats" 
      class="p-4 text-gray-500 text-center animate-pulse"
    >
      <svg 
        class="animate-spin h-6 w-6 text-gray-400 mx-auto mb-2" 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24"
      >
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
      </svg>
      Loading statistics...
    </div>

    <!-- Stats Content -->
    <div v-else-if="stats" class="space-y-6">
      <!-- Summary Stats -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <!-- Primary Stat Card -->
        <div class="p-4 bg-blue-50 rounded-lg border border-blue-100">
          <div class="text-sm text-blue-600 font-medium mb-1">{{ primaryStatLabel }}</div>
          <div class="text-3xl font-bold text-blue-700">
            {{ stats[primaryStatKey] }}
          </div>
        </div>
        
        <!-- Secondary Stat Card -->
        <div class="p-4 bg-purple-50 rounded-lg border border-purple-100">
          <div class="text-sm text-purple-600 font-medium mb-1">Server Uptime</div>
          <div class="text-3xl font-bold text-purple-700">
            {{ formatDuration(stats.uptime_seconds) }}
          </div>
        </div>
      </div>

      <!-- Custom Stats Section -->
      <slot 
        name="custom-stats" 
        :stats="stats"
        :formatDuration="formatDuration"
      ></slot>

      <!-- Clients Table -->
      <div v-if="hasClients" class="overflow-hidden">
        <h4 class="text-sm font-medium text-gray-700 mb-3">{{ clientsTableTitle }}</h4>
        <div class="border rounded-lg overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th 
                  v-for="header in clientTableHeaders"
                  :key="header.key"
                  class="px-4 sm:px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap"
                >
                  {{ header.label }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="client in clientsList" :key="client.id">
                <td 
                  v-for="header in clientTableHeaders"
                  :key="header.key"
                  class="px-4 sm:px-6 py-4 text-sm"
                  :class="header.class"
                >
                  <slot 
                    :name="`client-${header.key}`" 
                    :client="client"
                    :formatDuration="formatDuration"
                  >
                    {{ header.format ? header.format(client[header.key]) : client[header.key] }}
                  </slot>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- No Clients State -->
      <div 
        v-else
        class="text-center py-6 text-gray-500 bg-gray-50 rounded-lg border border-gray-100"
      >
        <svg 
          class="mx-auto h-8 w-8 text-gray-400 mb-2" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
          />
        </svg>
        {{ noClientsMessage }}
      </div>
    </div>

    <!-- No Stats State -->
    <div 
      v-else 
      class="text-center py-6 text-gray-500 bg-gray-50 rounded-lg border border-gray-100"
    >
      <svg 
        class="mx-auto h-8 w-8 text-gray-400 mb-2" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          stroke-width="2" 
          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
        />
      </svg>
      No statistics available
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface ClientTableHeader {
  key: string
  label: string
  class?: string
  format?: (value: any) => string
}

interface Props {
  title: string
  stats: any | null
  error: string | null
  isLoading: boolean
  isPolling: boolean
  isConfigured: boolean
  clientsTableTitle?: string
  primaryStatLabel?: string
  primaryStatKey?: string
  noClientsMessage?: string
  clientTableHeaders: ClientTableHeader[]
  startPolling: () => void
  stopPolling: () => void
}

const props = withDefaults(defineProps<Props>(), {
  clientsTableTitle: 'Connected Clients',
  primaryStatLabel: 'Active Clients',
  primaryStatKey: 'active_connections',
  noClientsMessage: 'No active clients'
})

const emit = defineEmits<{
  (e: 'update:isPolling', value: boolean): void
}>()

// Computed properties
const clientsList = computed(() => props.stats?.clients || [])
const hasClients = computed(() => clientsList.value.length > 0)

// Format duration helper
const formatDuration = (seconds: number): string => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const remainingSeconds = Math.floor(seconds % 60)

  const parts = []
  if (hours > 0) parts.push(`${hours}h`)
  if (minutes > 0) parts.push(`${minutes}m`)
  parts.push(`${remainingSeconds}s`)

  return parts.join(' ')
}

// Toggle polling
const togglePolling = () => {
  if (props.isPolling) {
    props.stopPolling()
  } else {
    props.startPolling()
  }
  emit('update:isPolling', !props.isPolling)
}

// Expose formatDuration for parent components
defineExpose({ formatDuration })
</script>

<style scoped>
/* Custom scrollbar for table overflow */
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

/* Improve touch targets on mobile */
@media (max-width: 640px) {
  .table th,
  .table td {
    padding-top: 12px;
    padding-bottom: 12px;
  }

  button {
    -webkit-tap-highlight-color: transparent;
  }
}

/* Fade animation */
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

.animate-fadeIn {
  animation: fadeIn 0.2s ease-in-out;
}
</style>