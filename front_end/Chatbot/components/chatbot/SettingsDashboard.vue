<template>
  <div v-if="isOpen" class="fixed inset-0 z-40">
    <!-- Animated backdrop with blur effect -->
    <div 
      class="absolute inset-0 backdrop-blur-lg bg-gradient-to-br from-gray-900/90 to-blue-900/90"
      @click="close"
    >
      <!-- Floating particles background -->
      <div v-for="i in 20" :key="i"
        class="particle absolute w-1 h-1 bg-blue-500/30 rounded-full"
        :style="{
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 3}s`
        }"
      ></div>
    </div>

    <!-- Main Settings Container -->
    <div class="relative h-full max-w-4xl mx-auto flex items-center px-4">
      <div class="w-full bg-gray-900/80 rounded-2xl shadow-2xl backdrop-blur-xl border border-blue-500/20 overflow-hidden">
        <!-- Header -->
        <div class="relative p-6 border-b border-blue-500/20">
          <div class="flex items-center space-x-4">
            <div class="relative">
              <!-- Animated ring around icon -->
              <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full animate-spin-slow"></div>
              <div class="relative bg-gray-900 p-3 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
            </div>
            <div>
              <h2 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                Settings Dashboard
              </h2>
              <p class="text-gray-400 mt-1">Customize your AI assistant experience</p>
            </div>
          </div>
          
          <!-- Close button -->
          <button 
            @click="close"
            class="absolute top-6 right-6 text-gray-400 hover:text-white transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Settings Content -->
        <div class="h-[calc(100vh-16rem)] overflow-y-auto">
          <div class="grid gap-6 p-6">
            <!-- Display Mode -->
            <section class="settings-section">
              <div class="flex items-center space-x-4 mb-6">
                <div class="p-3 rounded-xl bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-purple-500/20">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-xl font-semibold text-white">Display Mode</h3>
                  <p class="text-gray-400 text-sm">Choose how you want the chat window to appear</p>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <button 
                  @click="setWindowSize('full')"
                  class="display-option-button"
                  :class="{ 'active': isFullScreen }"
                >
                  <div class="flex items-center space-x-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                    </svg>
                    <span>Full Screen</span>
                  </div>
                  <div class="absolute -top-2 -right-2 transition-opacity" :class="{ 'opacity-100': isFullScreen, 'opacity-0': !isFullScreen }">
                    <div class="bg-blue-500 rounded-full p-1">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  </div>
                </button>

                <button 
                  @click="setWindowSize('minimized')"
                  class="display-option-button"
                  :class="{ 'active': !isFullScreen }"
                >
                  <div class="flex items-center space-x-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12V8m0 0l-4 4m4-4H8m0 12h8m-8 0l4-4m-4 4v-4" />
                    </svg>
                    <span>Floating Window</span>
                  </div>
                  <div class="absolute -top-2 -right-2 transition-opacity" :class="{ 'opacity-100': !isFullScreen, 'opacity-0': isFullScreen }">
                    <div class="bg-blue-500 rounded-full p-1">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  </div>
                </button>
              </div>
            </section>

            <!-- AI Services -->
            <section class="settings-section">
              <div class="flex items-center space-x-4 mb-6">
                <div class="p-3 rounded-xl bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-xl font-semibold text-white">AI Services</h3>
                  <p class="text-gray-400 text-sm">Configure your AI service providers</p>
                </div>
              </div>

              <div class="space-y-6">
                <AIProviderSettings
                  v-model="aiSettings.speechToText"
                  service-type="speechToText"
                  title="Speech to Text"
                  @update:model-value="(value) => updateAISettings('speechToText', value)"
                  class="settings-card"
                />
                <AIProviderSettings
                  v-model="aiSettings.textToSpeech"
                  service-type="textToSpeech"
                  title="Text to Speech"
                  @update:model-value="(value) => updateAISettings('textToSpeech', value)"
                  class="settings-card"
                />
                <AIProviderSettings
                  v-model="aiSettings.textGeneration"
                  service-type="textGeneration"
                  title="Text Generation"
                  @update:model-value="(value) => updateAISettings('textGeneration', value)"
                  class="settings-card"
                />
              </div>
            </section>

            <!-- Theme Settings -->
            <section class="settings-section">
              <div class="flex items-center space-x-4 mb-6">
                <div class="p-3 rounded-xl bg-gradient-to-br from-yellow-500/10 to-orange-500/10 border border-yellow-500/20">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-xl font-semibold text-white">Theme</h3>
                  <p class="text-gray-400 text-sm">Customize the appearance</p>
                </div>
              </div>

              <div class="theme-card">
                <div class="flex items-center justify-between">
                  <div class="space-y-1">
                    <span class="text-lg font-medium text-white">Dark Mode</span>
                    <p class="text-sm text-gray-400">Toggle between light and dark themes</p>
                  </div>
                  <button 
                    @click="toggleDarkMode"
                    class="relative w-14 h-7 rounded-full transition-colors duration-300"
                    :class="isDarkMode ? 'bg-blue-600' : 'bg-gray-600'"
                  >
                    <span 
                      class="absolute left-1 top-1 w-5 h-5 rounded-full bg-white transition-transform duration-300"
                      :class="isDarkMode ? 'translate-x-7' : 'translate-x-0'"
                    ></span>
                  </button>
                </div>
              </div>
            </section>

            <!-- Data Management -->
            <section class="settings-section">
              <div class="flex items-center space-x-4 mb-6">
                <div class="p-3 rounded-xl bg-gradient-to-br from-red-500/10 to-pink-500/10 border border-red-500/20">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-xl font-semibold text-white">Data Management</h3>
                  <p class="text-gray-400 text-sm">Manage your chat history and data</p>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <button 
                  @click="clearChat"
                  class="data-management-button group bg-gradient-to-br from-red-500/10 to-pink-500/10 hover:from-red-500/20 hover:to-pink-500/20"
                >
                  <div class="relative flex items-center justify-center space-x-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-400 group-hover:text-red-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    <span class="text-red-400 group-hover:text-red-300">Clear History</span>
                  </div>
                  <div class="absolute inset-0 rounded-xl transition-opacity opacity-0 group-hover:opacity-100">
                    <div class="absolute inset-0 bg-gradient-to-r from-red-500/20 to-pink-500/20 blur"></div>
                  </div>
                </button>

                <button 
                  @click="exportChat"
                  class="data-management-button group bg-gradient-to-br from-blue-500/10 to-cyan-500/10 hover:from-blue-500/20 hover:to-cyan-500/20"
                >
                  <div class="relative flex items-center justify-center space-x-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-400 group-hover:text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414A1 1 0 0119 9.586V17a2 2 0 01-2 2z" />
                    </svg>
                    <span class="text-blue-400 group-hover:text-blue-300">Export Chat</span>
                  </div>
                  <div class="absolute inset-0 rounded-xl transition-opacity opacity-0 group-hover:opacity-100">
                    <div class="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 blur"></div>
                  </div>
                </button>
              </div>
            </section>
          </div>
        </div>

        <!-- Footer -->
        <div class="p-6 border-t border-blue-500/20 backdrop-blur-xl">
          <div class="flex items-center justify-between">
            <div class="text-sm text-blue-400">
              <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span>Changes are saved automatically</span>
              </div>
            </div>
            <button 
              @click="close"
              class="px-6 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 text-white font-medium hover:from-blue-600 hover:to-purple-600 transition-all duration-300 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Notifications -->
    <NotificationToast />
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserPreferencesStore } from '~/stores/chatbot/userPreferences'
import { useNotificationsStore } from '~/stores/chatbot/notifications'
import { useMessagesStore } from '~/stores/chatbot/messages'
import NotificationToast from '../common/NotificationToast.vue'
import AIProviderSettings from '../settings/AIProviderSettings.vue'

const props = defineProps({
  isOpen: Boolean,
  isFullScreen: Boolean
})

const emit = defineEmits(['close', 'toggle-fullscreen'])

const userPreferencesStore = useUserPreferencesStore()
const notificationsStore = useNotificationsStore()
const messagesStore = useMessagesStore()

const { isDarkMode } = storeToRefs(userPreferencesStore)

const aiSettings = reactive({
  speechToText: { ...userPreferencesStore.getAISettings('speechToText') },
  textToSpeech: { ...userPreferencesStore.getAISettings('textToSpeech') },
  textGeneration: { ...userPreferencesStore.getAISettings('textGeneration') }
})

// Service names for notifications
const serviceNames = {
  speechToText: 'Speech to Text',
  textToSpeech: 'Text to Speech',
  textGeneration: 'Text Generation'
}

const updateAISettings = (service, settings) => {
  try {
    // Update local state
    aiSettings[service] = settings

    // Update store
    userPreferencesStore.updateAIProvider(service, settings.provider)
    userPreferencesStore.updateAIOptions(service, settings.options)

    notificationsStore.success(
      `${serviceNames[service]} settings updated successfully`
    )
  } catch (error) {
    notificationsStore.error(
      `Failed to update ${serviceNames[service]} settings: ${error.message}`
    )
  }
}

const close = () => {
  emit('close')
}

const setWindowSize = (size) => {
  emit('toggle-fullscreen', size === 'full')
  notificationsStore.success(`Window size set to ${size} mode`)
  close()
}

const toggleDarkMode = () => {
  userPreferencesStore.toggleDarkMode()
  notificationsStore.success(
    `Theme switched to ${userPreferencesStore.theme} mode`
  )
}

const clearChat = () => {
  if (confirm('Are you sure you want to clear all chat history? This action cannot be undone.')) {
    messagesStore.clearMessages()
    notificationsStore.success('Chat history cleared successfully')
    close()
  }
}

const exportChat = () => {
  try {
    const chatContent = messagesStore.messages
      .map(msg => `${msg.role}: ${msg.content}`)
      .join('\n\n')
    const blob = new Blob([chatContent], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'chat_export.txt'
    a.click()
    URL.revokeObjectURL(url)
    notificationsStore.success('Chat history exported successfully')
  } catch (error) {
    notificationsStore.error('Failed to export chat history')
  }
}

// Watch for store changes
watch(() => userPreferencesStore.getAllAISettings, (newSettings) => {
  Object.entries(newSettings).forEach(([service, settings]) => {
    aiSettings[service] = { ...settings }
  })
}, { deep: true })
</script>

<style scoped>
.settings-section {
  @apply bg-gray-800/50 rounded-2xl p-6 backdrop-blur-sm border border-blue-500/10;
}

.display-option-button {
  @apply relative p-4 rounded-xl border-2 transition-all duration-300 bg-gray-800/50 hover:bg-gray-800/80;
}

.display-option-button.active {
  @apply border-blue-500 bg-blue-500/10;
}

.display-option-button:not(.active) {
  @apply border-gray-700 text-gray-400 hover:border-gray-600;
}

.theme-card {
  @apply bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm border border-blue-500/10;
}

.data-management-button {
  @apply relative p-4 rounded-xl border border-transparent transition-all duration-300 overflow-hidden;
}

.settings-card {
  @apply bg-gray-800/50 rounded-xl backdrop-blur-sm border border-blue-500/10 transition-all duration-300 hover:border-blue-500/20;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

.particle {
  animation: float 3s infinite ease-in-out;
}

@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}

/* Custom scrollbar styling */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(59, 130, 246, 0.5) rgba(0, 0, 0, 0.1);
}

.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  @apply bg-gray-800/50 rounded-full;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  @apply bg-blue-500/50 rounded-full hover:bg-blue-500/70 transition-colors duration-300;
}

/* Transition animations */
.backdrop-blur-lg {
  transition: backdrop-filter 0.3s ease;
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>