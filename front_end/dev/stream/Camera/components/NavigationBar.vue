<template>
  <nav class="bg-gray-800 text-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Mobile Nav Container -->
      <div class="relative flex items-center justify-between h-16">
        <!-- Logo/Brand - Always visible -->
        <div class="flex-shrink-0 flex items-center">
          <span class="text-xl font-bold">Camera Stream</span>
        </div>
        
        <!-- Navigation Links - Responsive -->
        <div class="hidden sm:flex sm:space-x-4">
          <NuxtLink
            v-for="item in navigation"
            :key="item.path"
            :to="item.path"
            :class="[
              'px-3 py-2 rounded-md text-sm font-medium transition-colors',
              isCurrentPath(item.path)
                ? 'bg-gray-900 text-white'
                : 'text-gray-300 hover:bg-gray-700 hover:text-white'
            ]"
          >
            <span>{{ item.name }}</span>
            <span 
              v-if="item.path === '/view-streams' && streamsStore.streamingClientsCount > 0"
              class="ml-2 px-2 py-0.5 text-xs bg-green-500 rounded-full"
              aria-label="Active streams count"
            >
              {{ streamsStore.streamingClientsCount }}
            </span>
          </NuxtLink>
        </div>

        <!-- Mobile Menu Button -->
        <div class="sm:hidden">
          <button
            @click="toggleMobileMenu"
            type="button"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            :aria-expanded="isMobileMenuOpen"
            aria-controls="mobile-menu"
          >
            <span class="sr-only">{{ isMobileMenuOpen ? 'Close menu' : 'Open menu' }}</span>
            <!-- Icon when menu is closed -->
            <svg
              v-show="!isMobileMenuOpen"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <!-- Icon when menu is open -->
            <svg
              v-show="isMobileMenuOpen"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div
        id="mobile-menu"
        v-show="isMobileMenuOpen"
        class="sm:hidden"
        @click.self="isMobileMenuOpen = false"
      >
        <div class="px-2 pt-2 pb-3 space-y-1">
          <NuxtLink
            v-for="item in navigation"
            :key="item.path"
            :to="item.path"
            @click="isMobileMenuOpen = false"
            :class="[
              'flex items-center justify-between w-full px-3 py-3 rounded-md text-base font-medium transition-colors min-h-[44px]',
              isCurrentPath(item.path)
                ? 'bg-gray-900 text-white'
                : 'text-gray-300 hover:bg-gray-700 hover:text-white'
            ]"
          >
            <span>{{ item.name }}</span>
            <span 
              v-if="item.path === '/view-streams' && streamsStore.streamingClientsCount > 0"
              class="px-2 py-0.5 text-xs bg-green-500 rounded-full"
              aria-label="Active streams count"
            >
              {{ streamsStore.streamingClientsCount }}
            </span>
          </NuxtLink>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStreamsStore } from '@/stores/streams'

const route = useRoute()
const streamsStore = useStreamsStore()
const isMobileMenuOpen = ref(false)

const navigation = [
  { name: 'Server Setup', path: '/server-setup' },
  { name: 'Camera Stream', path: '/camera-stream' },
  { name: 'View Streams', path: '/view-streams' },
  { name: 'Processed Streams', path: '/view-processed-streams' }
]

const isCurrentPath = (path) => {
  return route.path === path
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// Close mobile menu on route change
watch(() => route.path, () => {
  isMobileMenuOpen.value = false
})

// Handle escape key to close mobile menu
const handleEscKey = (event) => {
  if (event.key === 'Escape' && isMobileMenuOpen.value) {
    isMobileMenuOpen.value = false
  }
}

// Close menu when clicking outside
const handleClickOutside = (event) => {
  const mobileMenu = document.getElementById('mobile-menu')
  const menuButton = event.target.closest('button')
  if (isMobileMenuOpen.value && !menuButton && !mobileMenu?.contains(event.target)) {
    isMobileMenuOpen.value = false
  }
}

// Handle device orientation change
const handleOrientationChange = () => {
  if (window.innerWidth >= 640) { // sm breakpoint
    isMobileMenuOpen.value = false
  }
}

// Setup and cleanup event listeners
onMounted(() => {
  document.addEventListener('keydown', handleEscKey)
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleOrientationChange)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscKey)
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleOrientationChange)
})
</script>

<style scoped>
/* Transition for mobile menu */
#mobile-menu {
  transform-origin: top;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    transform: scaleY(0);
    opacity: 0;
  }
  to {
    transform: scaleY(1);
    opacity: 1;
  }
}

/* Remove tap highlight on mobile */
@media (max-width: 640px) {
  a, button {
    -webkit-tap-highlight-color: transparent;
  }
}

/* Safe area insets for notched devices */
@supports (padding: max(0px)) {
  nav {
    padding-top: max(16px, env(safe-area-inset-top));
    padding-left: max(16px, env(safe-area-inset-left));
    padding-right: max(16px, env(safe-area-inset-right));
  }

  #mobile-menu {
    padding-bottom: max(16px, env(safe-area-inset-bottom));
  }
}
</style>
