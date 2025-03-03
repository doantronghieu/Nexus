<template>
  <div class="bg-gray-800 bg-opacity-50 backdrop-blur-md p-2 rounded-lg flex justify-end items-center">
    <button @click="$emit('open-settings')" class="toolbar-btn group" title="Settings">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
      <span class="tooltip group-hover:scale-100">Settings</span>
    </button>
  </div>
</template>

<style scoped>
.toolbar-btn {
  @apply text-gray-300 hover:text-white p-2 rounded-full transition-colors duration-200 relative;
}

.tooltip {
  @apply absolute -top-10 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs py-1 px-2 rounded opacity-0 transition-all duration-200 scale-0 whitespace-nowrap;
}

.toolbar-btn:hover .tooltip {
  @apply opacity-100 scale-100;
}
</style>