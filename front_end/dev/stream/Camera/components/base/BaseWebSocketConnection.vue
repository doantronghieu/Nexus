<template>
  <div class="w-full space-y-4">
    <!-- Connection Setup Section -->
    <div v-if="!isConnected" class="space-y-6">
      <!-- Name Selection Options -->
      <div v-if="showNameSelection" class="space-y-4">
        <!-- Server Name Option -->
        <label class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
          <input
            type="radio"
            id="useServerName"
            value="server"
            v-model="nameSelectionMode"
            class="w-5 h-5 text-blue-500 focus:ring-2 focus:ring-blue-500"
          />
          <span class="text-gray-700">Use server-generated name</span>
        </label>

        <!-- Preset Name Option -->
        <div class="space-y-3">
          <label class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
            <input
              type="radio"
              id="usePresetName"
              value="preset"
              v-model="nameSelectionMode"
              class="w-5 h-5 text-blue-500 focus:ring-2 focus:ring-blue-500"
            />
            <span class="text-gray-700">Select from predefined names</span>
          </label>
          
          <div v-if="nameSelectionMode === 'preset'" class="ml-8">
            <select
              v-model="selectedPresetName"
              class="w-full min-h-[44px] px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              :class="{'border-red-500': showValidation && nameSelectionMode === 'preset' && !selectedPresetName}"
            >
              <option value="">Select a name</option>
              <option v-for="name in predefinedNames" :key="name" :value="name">
                {{ name }}
              </option>
            </select>
            <p v-if="showValidation && nameSelectionMode === 'preset' && !selectedPresetName" class="mt-2 text-sm text-red-500">
              Please select a name
            </p>
          </div>
        </div>

        <!-- Custom Name Option -->
        <div class="space-y-3">
          <label class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
            <input
              type="radio"
              id="useCustomName"
              value="custom"
              v-model="nameSelectionMode"
              class="w-5 h-5 text-blue-500 focus:ring-2 focus:ring-blue-500"
            />
            <span class="text-gray-700">Enter custom name</span>
          </label>
          
          <div v-if="nameSelectionMode === 'custom'" class="ml-8">
            <input
              v-model="customName"
              type="text"
              :placeholder="`Enter ${connectionType} name`"
              class="w-full min-h-[44px] px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{'border-red-500': showValidation && nameSelectionMode === 'custom' && !customName.trim()}"
            />
            <p v-if="showValidation && nameSelectionMode === 'custom' && !customName.trim()" class="mt-2 text-sm text-red-500">
              Please enter a name
            </p>
          </div>
        </div>
      </div>

      <!-- Additional Setup Options Slot -->
      <slot name="setup-options"></slot>

      <!-- Connect Button -->
      <div class="flex justify-end">
        <button
          @click="onConnect"
          class="w-full sm:w-auto min-h-[44px] px-6 py-3 sm:py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-base font-medium transition-colors"
          :disabled="isLoading"
        >
          <template v-if="isLoading">
            <span class="flex items-center gap-2">
              <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Connecting...
            </span>
          </template>
          <template v-else>
            Connect
          </template>
        </button>
      </div>
    </div>

    <!-- Connected State -->
    <div v-else class="space-y-4">
      <!-- Connection Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 bg-gray-50 rounded-lg">
        <div class="flex items-center gap-2">
          <div class="h-2.5 w-2.5 rounded-full bg-green-500"></div>
          <span class="text-gray-600">Connected as {{ displayName }}</span>
        </div>
        <button
          @click="onDisconnect"
          class="w-full sm:w-auto min-h-[44px] sm:min-h-0 px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 text-sm font-medium transition-colors"
        >
          Disconnect
        </button>
      </div>

      <!-- Custom Connected Content -->
      <slot 
        name="connected-content"
        :handle-disconnect="onDisconnect"
        :display-name="displayName"
      ></slot>

      <!-- Error Display -->
      <div 
        v-if="error"
        class="p-3 text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg"
      >
        {{ error }}
        <button
          @click="onResetError"
          class="ml-2 text-red-500 hover:text-red-700"
        >
          Dismiss
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { NameSelectionMode } from '@/composables/types'

interface Props {
  connectionType: string
  isConnected: boolean
  displayName: string
  error: string | null
  showNameSelection?: boolean
  isLoading?: boolean
  predefinedNames?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  showNameSelection: true,
  isLoading: false,
  predefinedNames: () => [
    'Client_1',
    'Client_2',
    'Guest_A',
    'Guest_B',
    'User_X',
    'User_Y'
  ]
})

const emit = defineEmits<{
  (e: 'connect', name?: string): void
  (e: 'disconnect'): void
  (e: 'reset-error'): void
}>()

// Connection preferences
const nameSelectionMode = ref<NameSelectionMode>('server')
const selectedPresetName = ref('')
const customName = ref('')
const showValidation = ref(false)

const getSelectedName = () => {
  switch (nameSelectionMode.value) {
    case 'preset':
      return selectedPresetName.value || null
    case 'custom':
      return customName.value.trim() || null
    case 'server':
    default:
      return null
  }
}

const validateInput = () => {
  if (!props.showNameSelection) return true
  
  showValidation.value = true
  if (nameSelectionMode.value === 'custom' && !customName.value.trim()) {
    return false
  }
  if (nameSelectionMode.value === 'preset' && !selectedPresetName.value) {
    return false
  }
  return true
}

const resetValidation = () => {
  showValidation.value = false
}

const resetPreferences = () => {
  nameSelectionMode.value = 'server'
  selectedPresetName.value = ''
  customName.value = ''
  showValidation.value = false
}

const onConnect = () => {
  if (!validateInput()) return
  const nameToUse = getSelectedName()
  emit('connect', nameToUse)
}

const onDisconnect = () => {
  emit('disconnect')
  resetPreferences()
}

const onResetError = () => {
  emit('reset-error')
}

// Reset validation when changing mode
watch(nameSelectionMode, () => {
  if (showValidation.value) {
    resetValidation()
  }
})

// Clean up on unmount (when leaving the app)
onUnmounted(() => {
  if (process.client && window.navigator.userAgent.includes('Firefox')) {
    onDisconnect()
  }
})
</script>

<style scoped>
/* Improve touch targets on mobile */
@media (max-width: 640px) {
  input[type="radio"] {
    min-width: 20px;
    min-height: 20px;
  }

  button {
    -webkit-tap-highlight-color: transparent;
  }

  .hover\:bg-gray-50:hover {
    background-color: transparent;
  }
}

/* Transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>