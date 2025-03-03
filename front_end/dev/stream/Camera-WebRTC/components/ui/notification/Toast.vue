// components/ui/notification/Toast.vue
<template>
  <div 
    v-show="visible"
    class="flex items-center w-full gap-x-4 p-4 rounded-lg shadow-lg transition-all duration-300"
    :class="typeClasses"
  >
    <!-- Icon -->
    <div v-if="icon" class="flex-shrink-0">
      <component 
        :is="icon" 
        class="h-5 w-5 text-white"
      />
    </div>

    <!-- Content -->
    <div class="flex-1 text-sm font-semibold text-white">
      {{ message }}
    </div>
    
    <!-- Close button -->
    <button
      v-if="dismissible"
      @click="dismiss"
      class="flex-shrink-0 rounded-lg p-1 transition-colors duration-200 hover:bg-white/20"
    >
      <X class="h-4 w-4 text-white" />
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { CheckCircle, AlertCircle, Info, AlertTriangle, X } from 'lucide-vue-next'

const props = defineProps({
  id: {
    type: [Number, String],
    required: true
  },
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'info', 'warning'].includes(value)
  },
  duration: {
    type: Number,
    default: 3000
  },
  dismissible: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['dismiss'])

const visible = ref(false)
let timeout = null

// Compute icon based on type
const icon = computed(() => {
  switch (props.type) {
    case 'success':
      return CheckCircle
    case 'error':
      return AlertCircle
    case 'info':
      return Info
    case 'warning':
      return AlertTriangle
    default:
      return null
  }
})

// Compute classes based on type
const typeClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-green-600'
    case 'error':
      return 'bg-red-600'
    case 'info':
      return 'bg-blue-600'
    case 'warning':
      return 'bg-yellow-600'
    default:
      return 'bg-gray-600'
  }
})

const dismiss = () => {
  visible.value = false
  emit('dismiss', props.id)
}

onMounted(() => {
  visible.value = true
  
  if (props.duration > 0) {
    timeout = setTimeout(() => {
      dismiss()
    }, props.duration)
  }
})

onUnmounted(() => {
  if (timeout) {
    clearTimeout(timeout)
  }
})
</script>