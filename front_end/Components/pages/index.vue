<template>
  <div class="dashboard-container" :class="{ 'dark-mode': isDarkMode }">
    <!-- Tab Navigation -->
    <div class="tab-navigation">
      <div class="logo-container">
        <div class="logo">
        <img src="~/public/assets/logo-aic.png" alt="AI Vehicle Avatar" class="logo-image" />
        </div>
      </div>
      
      <div class="tabs-container">
        <div 
          v-for="(tab, index) in tabs" 
          :key="index"
          class="tab-item"
          :class="{ active: activeTab === index }"
          @click="setActiveTab(index)"
          :title="tab.name"
        >
          <div class="tab-icon" v-html="tab.icon"></div>
          <span class="tab-name">{{ tab.name }}</span>
          <div class="active-indicator"></div>
          <div class="glow-effect"></div>
        </div>
      </div>
      
      <!-- Settings Tab -->
      <div class="utilities-container">
        <div 
          class="tab-item theme-toggle"
          @click="toggleTheme"
          :title="isDarkMode ? 'Light Mode' : 'Dark Mode'"
        >
          <div class="tab-icon" v-html="isDarkMode ? lightModeIcon : darkModeIcon"></div>
          <span class="tab-name">{{ isDarkMode ? 'Light' : 'Dark' }}</span>
        </div>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Map & Weather Tab -->
      <div 
        class="tab-panel map-weather-panel" 
        :class="{ 'active': activeTab === 0, 'inactive': activeTab !== 0 }"
      >
        <div class="map-container">
          <Map />
        </div>
        <div class="weather-container">
          <Weather />
        </div>
      </div>

      <!-- Music & News Tab -->
      <div 
        class="tab-panel media-panel"
        :class="{ 'active': activeTab === 1, 'inactive': activeTab !== 1 }"
      >
        <div class="music-container">
          <Music />
        </div>
        <div class="news-container">
          <News />
        </div>
      </div>

      <!-- Face Recognition Tab -->
      <div 
        class="tab-panel face-panel"
        :class="{ 'active': activeTab === 2, 'inactive': activeTab !== 2 }"
      >
        <ClientOnly>
          <LazyFace />
          <template #fallback>
            <div class="face-loading-placeholder">
              <div class="loading-indicator">
                <div class="spinner"></div>
                <p>Initializing camera...</p>
              </div>
            </div>
          </template>
        </ClientOnly>
      </div>
    </div>

    <!-- Fixed Bottom Area -->
    <div class="bottom-panel">
      <div class="agent-container">
        <AgentNexus ref="agentNexus" />
      </div>
      <div class="input-container">
        <MultiModalInput @messageSent="handleMessageSent" />
      </div>
    </div>

    <!-- Tab Transition Overlay -->
    <div v-if="isTransitioning" class="transition-overlay" :style="transitionStyle">
      <div class="transition-circle"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, defineAsyncComponent, watch } from 'vue'
import AgentNexus from '@/components/vehicle/AgentNexus.vue'
// Use defineAsyncComponent to lazy-load the Face component
// Nuxt will automatically prefix with "Lazy" when using ClientOnly
import Map from '@/components/Map.vue'
import MultiModalInput from '@/components/MultiModalInput.vue'
import Music from '@/components/Music.vue'
import News from '@/components/News.vue'
import Weather from '@/components/Weather.vue'

// Regular import - Nuxt will handle with Lazy prefix
import Face from '@/components/Face.vue'

// State
const activeTab = ref(0)
const isDarkMode = ref(true)
const isTransitioning = ref(false)
const transitionStyle = ref({})

// Handle message sent from MultiModalInput
const agentNexus = ref(null)
const handleMessageSent = () => {
  if (agentNexus.value) {
    agentNexus.value.clearMessage()
  }
}

// Agent-to-tab mapping
const agentTabMapping = {
  'agent_navigation': 0, // Navigation tab index
  'agent_music': 1,      // Entertainment tab index
  // Add more agent-to-tab mappings as needed
}

// Also set up a watcher for the currentAgent value
const setupAgentWatcher = () => {
  const checkForChanges = () => {
    if (agentNexus.value) {
      // Use a Vue watcher to react to currentAgent changes
      watch(() => agentNexus.value.currentAgent, (newAgent, oldAgent) => {
        console.log(`Agent changed from ${oldAgent} to ${newAgent}`)
        if (newAgent && agentTabMapping[newAgent] !== undefined) {
          console.log(`Switching to tab ${agentTabMapping[newAgent]}`)
          setActiveTab(agentTabMapping[newAgent], true)
        }
      })
      return true
    }
    return false
  }
  
  // Try to set up the watcher immediately
  if (!checkForChanges()) {
    // If agentNexus isn't ready yet, use a short interval to check again
    const watcherSetupInterval = setInterval(() => {
      if (checkForChanges()) {
        clearInterval(watcherSetupInterval)
      }
    }, 100)
    
    // Clean up the setup interval after a reasonable timeout (5 seconds)
    setTimeout(() => {
      clearInterval(watcherSetupInterval)
    }, 5000)
  }
}

// Tab definitions with SVG icons
const tabs = [
  {
    name: 'Navigation',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>'
  },
  {
    name: 'Entertainment',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>'
  },
  {
    name: 'Profile',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'
  }
]

// Theme toggle icons
const darkModeIcon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>'
const lightModeIcon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'

// Methods
const setActiveTab = (index, isAutoSwitch = false) => {
  // If already on this tab, do nothing
  if (activeTab.value === index) return
  
  // Create a high-tech transition effect
  if (!isAutoSwitch) {
    // Only do the fancy transition for user-initiated switches
    createTransition()
  }
  
  // Update the active tab
  activeTab.value = index
}

// Create a high-tech transition effect 
const createTransition = () => {
  isTransitioning.value = true
  
  // Generate a random position for the transition effect
  const x = Math.floor(Math.random() * window.innerWidth)
  const y = Math.floor(Math.random() * window.innerHeight)
  
  transitionStyle.value = {
    '--origin-x': `${x}px`,
    '--origin-y': `${y}px`,
  }
  
  // Reset the transition after animation completes
  setTimeout(() => {
    isTransitioning.value = false
  }, 2500)
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
}

// This handles key navigation for tabs
const handleKeyNavigation = (e) => {
  if (e.key === 'ArrowDown' && activeTab.value < tabs.length - 1) {
    setActiveTab(activeTab.value + 1)
  } else if (e.key === 'ArrowUp' && activeTab.value > 0) {
    setActiveTab(activeTab.value - 1)
  }
}

// Lifecycle hooks
onMounted(() => {
  if (process.client) {
    // Check system preference - only run on client
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    isDarkMode.value = prefersDark
    
    window.addEventListener('keydown', handleKeyNavigation)
    
    // Set up the reactive watcher for agent changes
    setupAgentWatcher()
  }
})

onBeforeUnmount(() => {
  if (process.client) {
    window.removeEventListener('keydown', handleKeyNavigation)
  }
})
</script>

<style>
/* CSS Variables for theming */
:root {
  --bg-primary: #0f172a;
  --bg-secondary: rgba(30, 41, 59, 0.95);
  --bg-tertiary: rgba(51, 65, 85, 0.8);
  --bg-active: rgba(59, 130, 246, 0.15);
  --border-color: rgba(51, 65, 85, 0.5);
  --border-active: rgba(59, 130, 246, 0.3);
  --text-primary: #e2e8f0;
  --text-secondary: #94a3b8;
  --accent-color: #3b82f6;
  --accent-hover: #2563eb;
  --accent-light: rgba(59, 130, 246, 0.2);
  --shadow-color: rgba(0, 0, 0, 0.2);
  --backdrop-blur: 0.75rem;
  --transition-speed: 0.3s;
  --border-radius: 1.5rem;
  --spacing-xs: 0.5rem;
  --spacing-sm: 0.75rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --glow-color: rgba(59, 130, 246, 0.6);
}

/* Light mode variables */
.dashboard-container:not(.dark-mode) {
  --bg-primary: #f8fafc;
  --bg-secondary: rgba(248, 250, 252, 0.95);
  --bg-tertiary: rgba(226, 232, 240, 0.8);
  --bg-active: rgba(59, 130, 246, 0.1);
  --border-color: rgba(226, 232, 240, 0.8);
  --border-active: rgba(59, 130, 246, 0.3);
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --shadow-color: rgba(0, 0, 0, 0.1);
  --glow-color: rgba(59, 130, 246, 0.4);
}

/* Global Reset */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body, html {
  height: 100%;
  width: 100%;
  overflow: hidden;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
}

/* Dashboard Layout */
.dashboard-container {
  display: grid;
  grid-template-columns: 7rem 1fr;
  grid-template-rows: 1fr auto;
  grid-template-areas: 
    "sidebar content"
    "bottom bottom";
  height: 100vh;
  width: 100vw;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: all var(--transition-speed) ease;
  position: relative;
  overflow: hidden;
}

/* Tab Navigation */
.tab-navigation {
  grid-area: sidebar;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  align-items: center;
  backdrop-filter: blur(var(--backdrop-blur));
  box-shadow: 0 4px 12px var(--shadow-color);
  z-index: 20;
  position: relative;
}

.logo-container {
  padding: var(--spacing-md) 0;
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: var(--spacing-md);
}

.logo {
  width: 4.5rem;
  height: 4.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 1rem;
  position: relative;
  overflow: hidden;
}

.logo::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    transparent, 
    transparent, 
    transparent, 
    rgba(255, 255, 255, 0.2)
  );
  transform: rotate(45deg);
  animation: shine 3s infinite;
}

@keyframes shine {
  0% {
    top: -50%;
    left: -50%;
  }
  100% {
    top: 150%;
    left: 150%;
  }
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.tabs-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
  padding: 0 var(--spacing-xs);
  flex: 1;
}

.utilities-container {
  margin-top: auto;
  padding: var(--spacing-md) 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  border-top: 1px solid var(--border-color);
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 5rem;
  padding: var(--spacing-md);
  border-radius: 1rem;
  cursor: pointer;
  color: var(--text-secondary);
  background: transparent;
  transition: all 0.7s ease;
  position: relative;
  overflow: hidden;
}

.tab-item:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.tab-item.active {
  color: var(--accent-color);
  background: var(--bg-active);
  border: 1px solid var(--border-active);
}

.active-indicator {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 0;
  background: var(--accent-color);
  border-radius: 0 4px 4px 0;
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-item.active .active-indicator {
  height: 60%;
  opacity: 1;
}

.tab-icon {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-xs);
  position: relative;
  z-index: 2;
}

.tab-icon svg {
  width: 1.75rem;
  height: 1.75rem;
  stroke-width: 2;
  transition: all var(--transition-speed) ease;
}

.tab-item.active .tab-icon svg {
  transform: scale(1.1);
  filter: drop-shadow(0 0 6px var(--glow-color));
  transition: transform 0.8s ease, filter 1.2s ease;
}

.tab-name {
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
  position: relative;
  z-index: 2;
}

.glow-effect {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 1rem;
  opacity: 0;
  z-index: 1;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.tab-item.active .glow-effect {
  box-shadow: 0 0 20px var(--glow-color);
  opacity: 0.5;
  animation: pulse 5s infinite;
}

@keyframes pulse {
  0% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 0.2;
  }
}

.theme-toggle {
  height: 4rem;
}

/* Tab Content */
.tab-content {
  grid-area: content;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
  z-index: 10;
}

.tab-panel {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  padding: var(--spacing-md);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 1.8s cubic-bezier(0.4, 0, 0.2, 1), opacity 1.8s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  transform: translateX(100px);
  z-index: 1;
}

.tab-panel.active {
  opacity: 1;
  transform: translateX(0);
  z-index: 5;
}

.tab-panel.inactive {
  opacity: 0;
  transform: translateX(-100px);
  z-index: 1;
}

/* Map & Weather Panel */
.map-weather-panel {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 60% 40%;
  gap: var(--spacing-md);
}

.map-container {
  border-radius: var(--border-radius);
  overflow: hidden;
  position: relative;
  box-shadow: 0 var(--spacing-xs) var(--spacing-lg) var(--shadow-color);
}

.weather-container {
  border-radius: var(--border-radius);
  overflow: hidden;
  position: relative;
  min-height: 0;
}

/* Media Panel */
.media-panel {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 1fr 1fr;
  gap: var(--spacing-md);
  height: 100%;
}

.music-container, .news-container {
  border-radius: var(--border-radius);
  overflow: hidden;
  position: relative;
  box-shadow: 0 var(--spacing-xs) var(--spacing-lg) var(--shadow-color);
  display: flex;
  flex-direction: column;
  min-height: 0; /* Important for Firefox */
}

/* Face Panel */
.face-panel {
  padding: var(--spacing-md);
  height: 100%;
  display: flex;
  overflow: hidden;
}

/* Face loading placeholder */
.face-loading-placeholder {
  height: 100%;
  background: rgba(15, 23, 42, 0.95);
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 3px solid rgba(59, 130, 246, 0.3);
  border-radius: 50%;
  border-top-color: var(--accent-color);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Bottom Panel */
.bottom-panel {
  grid-area: bottom;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: auto auto;
  gap: 0.5rem;
  padding: 0.5rem;
  background: var(--bg-secondary);
  backdrop-filter: blur(var(--backdrop-blur));
  border-top: 1px solid var(--border-color);
  max-height: 35vh;
  z-index: 30;
  position: relative;
}

.agent-container {
  border-radius: var(--border-radius);
  overflow: hidden;
  height: 20vh;
  display: flex;
  width: 100%;
}

.input-container {
  border-radius: var(--border-radius);
  overflow: hidden;
  height: 12vh;
}

/* Transition Overlay */
.transition-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 1000;
}

.transition-circle {
  position: absolute;
  top: var(--origin-y);
  left: var(--origin-x);
  transform: translate(-50%, -50%) scale(0);
  width: 2px;
  height: 2px;
  border-radius: 50%;
  background: var(--accent-color);
  box-shadow: 0 0 40px 20px var(--accent-color);
  opacity: 0;
  animation: circleExpand 2.5s cubic-bezier(0.215, 0.610, 0.355, 1.000) forwards;
}

@keyframes circleExpand {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0.8;
  }
  60% {
    opacity: 0.5;
  }
  100% {
    transform: translate(-50%, -50%) scale(100);
    opacity: 0;
  }
}

/* Media Queries */
@media (min-width: 1024px) {
  .dashboard-container {
    grid-template-columns: 8rem 1fr;
  }
  
  .map-weather-panel {
    grid-template-columns: 3fr 1fr;
    grid-template-rows: 1fr;
  }

  .media-panel {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr;
  }
  
  /* Ensure the weather component is fully visible in horizontal layout */
  .weather-container {
    display: flex;
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    grid-template-columns: 4.5rem 1fr;
  }
  
  .tab-name {
    font-size: 0.65rem;
  }
  
  .logo {
    width: 3rem;
    height: 3rem;
  }
  
  .tab-item {
    height: 4.5rem;
    padding: var(--spacing-sm);
  }
  
  .tab-icon svg {
    width: 1.5rem;
    height: 1.5rem;
  }
}

/* Hamburger menu for very small screens */
@media (max-width: 480px) {
  .dashboard-container {
    grid-template-columns: 1fr;
    grid-template-areas: 
      "content"
      "bottom";
  }
  
  .tab-navigation {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 4rem;
    flex-direction: row;
    border-right: none;
    border-top: 1px solid var(--border-color);
    z-index: 100;
  }
  
  .logo-container {
    display: none;
  }
  
  .tabs-container {
    flex-direction: row;
    justify-content: space-around;
    gap: 0;
    padding: 0;
  }
  
  .utilities-container {
    display: none;
  }
  
  .tab-item {
    height: 4rem;
    width: auto;
    border-radius: 0;
    padding: var(--spacing-xs);
  }
  
  .tab-icon {
    margin-bottom: 2px;
  }
  
  .tab-icon svg {
    width: 1.5rem;
    height: 1.5rem;
  }
  
  .tab-name {
    font-size: 0.6rem;
  }
  
  .active-indicator {
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 3px;
  }
  
  .tab-item.active .active-indicator {
    width: 50%;
    height: 3px;
  }
  
  .bottom-panel {
    padding-bottom: 4.5rem;
  }
}

/* Additional style adjustments for the components */
.weather-widget, .music-dashboard, .news-dashboard, .face-dashboard {
  padding: 0 !important;
  height: 100%;
}

.weather-container, .music-container, .news-container {
  border-radius: var(--border-radius);
}

/* Override map widget container */
.map-widget-container {
  height: 100% !important;
}

/* Component Visibility fixes */
.dashboard-container :deep(.face-dashboard),
.dashboard-container :deep(.weather-widget),
.dashboard-container :deep(.music-dashboard),
.dashboard-container :deep(.news-dashboard) {
  height: 100%;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dashboard-container :deep(.face-container),
.dashboard-container :deep(.weather-container),
.dashboard-container :deep(.music-container),
.dashboard-container :deep(.news-container) {
  height: 100%;
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Fix for Map component */
.dashboard-container :deep(.map-widget-container) {
  height: 100% !important;
}

/* Fix for News pagination */
.dashboard-container :deep(.news-container .carousel-pagination) {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

/* Fix for Face component */
.dashboard-container :deep(.face-dashboard) {
  flex: 1;
  overflow: hidden;
}

.dashboard-container :deep(.face-container) {
  flex: 1;
  height: 100%;
  max-height: 100%;
  overflow: hidden;
}

/* Weather component adjustments */
.dashboard-container :deep(.weather-widget) {
  flex: 1;
  min-height: 0;
}

.dashboard-container :deep(.weather-container) {
  flex: 1;
  min-height: 0;
}

/* Make News component more compact */
.dashboard-container :deep(.news-dashboard .content-wrapper) {
  gap: 0.5rem;
  padding: 0.75rem;
}

.dashboard-container :deep(.news-dashboard .articles-container) {
  min-height: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.dashboard-container :deep(.news-dashboard .carousel-container) {
  flex: 1;
  min-height: 0;
}

.dashboard-container :deep(.weather-content) {
  gap: 0.75rem;
}

/* Accessibility - reduce motion option */
@media (prefers-reduced-motion: reduce) {
  * {
    transition: none !important;
    animation: none !important;
  }
  
  .tab-panel {
    transition: opacity 0.1s linear !important;
  }
  
  .tab-panel.active,
  .tab-panel.inactive {
    transform: none !important;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .dashboard-container {
    --bg-primary: white;
    --bg-secondary: white;
    --bg-tertiary: white;
    --bg-active: #e6f0ff;
    --border-color: black;
    --border-active: blue;
    --text-primary: black;
    --text-secondary: #505050;
    --accent-color: blue;
    --accent-hover: darkblue;
    --accent-light: lightblue;
    --shadow-color: transparent;
  }
  
  .tab-item {
    border: 2px solid black;
    margin-bottom: 4px;
  }
  
  .tab-item.active {
    background-color: #e6f0ff;
    border: 2px solid blue;
  }
  
  .logo {
    background: blue;
    border: 2px solid black;
  }
  
  .tab-item.active .glow-effect {
    box-shadow: none;
    animation: none;
  }
  
  .transition-circle {
    display: none;
  }
}
</style>