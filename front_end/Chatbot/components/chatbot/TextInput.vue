<template>
  <div class="relative group">
    <!-- Main input container -->
    <div 
      class="relative flex items-center overflow-hidden rounded-xl border-2 transition-all duration-300 bg-opacity-20"
      :class="[
        disabled ? 'border-gray-600 bg-gray-800' : 'border-blue-500 bg-gray-800 hover:border-blue-400',
        focused ? 'ring-2 ring-blue-500 ring-opacity-50' : ''
      ]"
    >
      <!-- Animated background gradient -->
      <div 
        class="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20 animate-gradient"
        :class="{ 'opacity-50': !focused, 'opacity-100': focused }"
      ></div>

      <!-- Input field -->
      <input
        v-model="inputText"
        @keyup.enter="sendMessage"
        @focus="handleFocus"
        @blur="handleBlur"
        type="text"
        :placeholder="disabled ? 'Please wait...' : 'Type your message...'"
        :disabled="disabled"
        class="w-full bg-transparent px-4 py-3 text-white placeholder-blue-300/70 focus:outline-none relative z-10"
        :class="{ 'opacity-50 cursor-not-allowed': disabled }"
      />

      <!-- Character counter -->
      <div 
        v-if="inputText.length > 0"
        class="absolute right-16 top-1/2 -translate-y-1/2 text-xs text-blue-300/70 px-2 py-1 rounded-full bg-blue-500/10"
      >
        {{ inputText.length }}/2000
      </div>

      <!-- Send button -->
      <button
        @click="sendMessage"
        :disabled="!canSend"
        class="relative z-10 p-3 transition-all duration-300 rounded-r-xl group"
        :class="[
          canSend ? 'text-white hover:bg-blue-500/30' : 'text-gray-500 cursor-not-allowed'
        ]"
      >
        <!-- Button background pulse effect -->
        <div 
          v-if="canSend"
          class="absolute inset-0 bg-blue-500/20 rounded-r-xl transform scale-0 group-hover:scale-100 transition-transform duration-300"
        ></div>

        <!-- Send icon -->
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          class="h-6 w-6 transform transition-transform duration-300 group-hover:rotate-12"
          :class="{ 'group-hover:text-blue-300': canSend }"
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" 
          />
        </svg>

        <!-- Hover tooltip -->
        <div class="absolute bottom-full right-0 mb-2 hidden group-hover:block">
          <div class="bg-gray-800 text-white text-xs px-2 py-1 rounded">
            Send message
          </div>
        </div>
      </button>
    </div>

    <!-- Character limit warning -->
    <div 
      v-if="inputText.length > 1900"
      class="absolute -bottom-6 left-0 text-xs text-yellow-400"
    >
      Approaching character limit
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['send-message'])
const inputText = ref('')
const focused = ref(false)

const canSend = computed(() => {
  return !props.disabled && inputText.value.trim().length > 0 && inputText.value.length <= 2000
})

const handleFocus = () => {
  focused.value = true
}

const handleBlur = () => {
  focused.value = false
}

const sendMessage = () => {
  if (canSend.value) {
    emit('send-message', inputText.value)
    inputText.value = ''
  }
}
</script>

<style scoped>
@keyframes gradient {
  0% { background-position: 0% 50% }
  50% { background-position: 100% 50% }
  100% { background-position: 0% 50% }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 8s ease infinite;
}

/* Smooth transition for input field */
input {
  transition: all 0.3s ease;
}

/* Custom placeholder style */
input::placeholder {
  transition: opacity 0.3s ease;
}

input:focus::placeholder {
  opacity: 0.5;
}

/* Disable default outline and add custom focus styles */
input:focus {
  outline: none;
}

/* Smooth transition for all interactive elements */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Hover effects */
.group:hover .border-blue-500 {
  border-color: rgba(59, 130, 246, 0.8);
}

/* Disabled state styling */
.cursor-not-allowed {
  cursor: not-allowed;
}

.opacity-50 {
  opacity: 0.5;
}
</style>