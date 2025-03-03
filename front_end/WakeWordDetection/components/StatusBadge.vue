<template>
  <div class="inline-flex items-center px-3 py-1 rounded-full text-sm" :class="badgeClass">
    <div class="w-2 h-2 mr-2 rounded-full" :class="indicatorClass"></div>
    <span>{{ label }}: {{ displayStatus }}</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  status: boolean | string;
  label: string;
  type?: 'boolean' | 'string';
}

const props = withDefaults(defineProps<Props>(), {
  type: 'string'
})

const displayStatus = computed(() => {
  if (props.type === 'boolean') {
    return props.status ? 'Connected' : 'Disconnected'
  }
  return props.status
})

const badgeClass = computed(() => {
  if (props.type === 'boolean') {
    return props.status
      ? 'bg-green-100 text-green-800'
      : 'bg-red-100 text-red-800'
  }
  
  switch (props.status) {
    case 'healthy':
      return 'bg-green-100 text-green-800'
    case 'error':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
})

const indicatorClass = computed(() => {
  if (props.type === 'boolean') {
    return props.status
      ? 'bg-green-500'
      : 'bg-red-500'
  }
  
  switch (props.status) {
    case 'healthy':
      return 'bg-green-500'
    case 'error':
      return 'bg-red-500'
    default:
      return 'bg-gray-500'
  }
})
</script>