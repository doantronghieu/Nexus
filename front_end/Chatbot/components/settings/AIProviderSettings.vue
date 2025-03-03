<template>
  <div class="bg-gray-700 p-4 rounded-lg space-y-3">
    <h5 class="text-white font-medium">{{ title }}</h5>
    
    <!-- Provider Selection -->
    <div class="flex items-center justify-between">
      <span class="text-gray-300">Provider</span>
      <select 
        :value="modelValue.provider"
        class="bg-gray-800 text-white rounded px-3 py-1 border border-gray-600"
        @change="updateProvider($event.target.value)"
      >
        <option 
          v-for="provider in availableProviders" 
          :key="provider.id" 
          :value="provider.id"
        >
          {{ provider.name }}
        </option>
      </select>
    </div>

    <!-- Dynamic Provider Options -->
    <template v-if="currentProvider && Object.keys(currentProvider.options).length > 0">
      <div class="space-y-3">
        <div 
          v-for="(config, key) in currentProvider.options" 
          :key="key"
          class="flex items-center justify-between"
        >
          <span class="text-gray-300">{{ config.label }}</span>
          
          <!-- Select Input -->
          <select
            v-if="config.type === 'select'"
            :value="modelValue.options[key]"
            class="bg-gray-800 text-white rounded px-3 py-1 border border-gray-600"
            @change="updateOption(key, $event.target.value)"
          >
            <option
              v-for="choice in config.choices"
              :key="choice.value"
              :value="choice.value"
            >
              {{ choice.label }}
            </option>
          </select>

          <!-- Range Input -->
          <div v-else-if="config.type === 'range'" class="flex items-center space-x-2">
            <input
              type="range"
              :min="config.min"
              :max="config.max"
              :step="config.step"
              :value="modelValue.options[key]"
              @input="updateOption(key, parseFloat($event.target.value))"
              class="w-32"
            />
            <span class="text-gray-300 ml-2 w-12">
              {{ modelValue.options[key] }}
            </span>
          </div>

          <!-- Number Input -->
          <input
            v-else-if="config.type === 'number'"
            type="number"
            :min="config.min"
            :max="config.max"
            :value="modelValue.options[key]"
            @change="updateOption(key, parseInt($event.target.value))"
            class="bg-gray-800 text-white rounded px-3 py-1 border border-gray-600 w-24"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { AI_PROVIDERS, getProviderConfig } from '~/configs/aiProviders'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  serviceType: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const availableProviders = computed(() => {
  return AI_PROVIDERS[props.serviceType]?.providers || []
})

const currentProvider = computed(() => {
  return getProviderConfig(props.serviceType, props.modelValue.provider)
})

const updateProvider = (providerId) => {
  const provider = getProviderConfig(props.serviceType, providerId)
  const defaultOptions = {}
  
  // Set default options for the new provider
  if (provider && provider.options) {
    Object.entries(provider.options).forEach(([key, config]) => {
      defaultOptions[key] = config.default
    })
  }

  emit('update:modelValue', {
    provider: providerId,
    options: defaultOptions
  })
}

const updateOption = (key, value) => {
  const newModelValue = {
    provider: props.modelValue.provider,
    options: {
      ...props.modelValue.options,
      [key]: value
    }
  }
  emit('update:modelValue', newModelValue)
}
</script>