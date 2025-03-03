<template>
  <div class="relative group">
    <slot></slot>
    <div class="absolute z-10 px-3 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip group-hover:opacity-100 transition-opacity duration-300"
         :class="position">
      {{ text }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    required: true
  },
  position: {
    type: String,
    default: 'top'
  }
})
</script>

<style scoped>
.tooltip {
  white-space: nowrap;
}
.tooltip.top { bottom: 100%; left: 50%; transform: translateX(-50%) translateY(-8px); }
.tooltip.bottom { top: 100%; left: 50%; transform: translateX(-50%) translateY(8px); }
.tooltip.left { right: 100%; top: 50%; transform: translateY(-50%) translateX(-8px); }
.tooltip.right { left: 100%; top: 50%; transform: translateY(-50%) translateX(8px); }
</style>