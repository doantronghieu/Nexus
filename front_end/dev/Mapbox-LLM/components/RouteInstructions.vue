<template>
  <div 
    id="instructions" 
    class="panel" 
    :class="{ active: show }" 
    role="complementary" 
    aria-label="Route instructions"
  >
    <div class="route-header">
      <h2>Route Instructions</h2>
      <button 
        class="minimize-button"
        @click="isMinimized = !isMinimized"
        :aria-label="isMinimized ? 'Expand route details' : 'Minimize route details'"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          :class="{ 'rotate-180': !isMinimized }"
          class="h-6 w-6 transition-transform duration-200" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </div>
    
    <div class="route-content" :class="{ 'minimized': isMinimized }">
      <template v-if="routeData && routeData.routes && routeData.routes[0]">
        <div class="route-summary">
          <div class="summary-grid">
            <div class="route-summary-item">
              <div class="summary-icon">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div class="summary-content">
                <span class="summary-label">Distance</span>
                <span class="summary-value">{{ formatDistance(routeData.routes[0].distance) }}</span>
              </div>
            </div>
            <div class="route-summary-item">
              <div class="summary-icon">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="summary-content">
                <span class="summary-label">Duration</span>
                <span class="summary-value">{{ formatDuration(routeData.routes[0].duration) }}</span>
              </div>
            </div>
            <div class="route-summary-item">
              <div class="summary-icon">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="summary-content">
                <span class="summary-label">Arrival</span>
                <span class="summary-value">{{ calculateArrivalTime(routeData.routes[0].duration) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="!isMinimized" class="route-steps-container">
          <div class="progress-bar">
            <div class="progress" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          
          <TransitionGroup 
            name="list" 
            tag="ol"
            class="steps-list"
          >
            <li 
              v-for="(step, index) in routeData.routes[0].legs[0].steps" 
              :key="index"
              :class="{ 'active': currentStepIndex === index }"
              @click="setCurrentStep(index, step)"
              @mouseenter="handleStepHover(index)"
              @mouseleave="handleStepLeave()"
            >
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-content">
                <div class="step-instruction" v-html="formatInstruction(step.maneuver.instruction)"></div>
                <div class="step-distance" v-if="step.distance">
                  {{ formatDistance(step.distance) }}
                </div>
              </div>
              <div class="step-icon">
                {{ getManeuverIcon(step.maneuver.type, step.maneuver.instruction) }}
              </div>
            </li>
          </TransitionGroup>
        </div>
      </template>
      
      <div v-else-if="error" class="error-message">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <p>Sorry, couldn't calculate the route. Please try again.</p>
      </div>

      <div v-else class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
        </svg>
        <p>Select a destination to see route instructions</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  routeData: {
    type: Object,
    default: () => null
  },
  error: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['step-selected', 'step-hover'])
const isMinimized = ref(false)
const currentStepIndex = ref(0)

const progressPercentage = computed(() => {
  if (!props.routeData?.routes?.[0]?.legs?.[0]?.steps) return 0
  return ((currentStepIndex.value + 1) / props.routeData.routes[0].legs[0].steps.length) * 100
})

function formatDistance(meters) {
  if (!meters) return '-'
  if (meters < 1000) return `${Math.round(meters)}m`
  return `${(meters/1000).toFixed(1)}km`
}

function formatDuration(seconds) {
  if (!seconds) return '-'
  if (seconds < 60) return `${Math.round(seconds)}s`
  if (seconds < 3600) return `${Math.floor(seconds/60)}min`
  const hours = Math.floor(seconds/3600)
  const minutes = Math.floor((seconds%3600)/60)
  return `${hours}h ${minutes}min`
}

function calculateArrivalTime(durationSeconds) {
  const now = new Date()
  const arrivalTime = new Date(now.getTime() + (durationSeconds * 1000))
  return arrivalTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function formatInstruction(instruction) {
  return instruction
    .replace(/(\d+(\.\d+)?)\s*(meters|km|m)/gi, '<span class="highlight-distance">$&</span>')
    .replace(/(onto|on|to)\s+([A-Za-z0-9\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd))/gi, '$1 <span class="highlight-street">$2</span>')
}

function getManeuverIcon(type, instruction) {
  const maneuverType = (type || '').toLowerCase().trim();
  const maneuverInstruction = (instruction || '').toLowerCase().trim();

  if (maneuverInstruction.startsWith('drive')) return '↑';
  if (maneuverInstruction.includes('you have arrived')) return '◎';
  if (maneuverInstruction.startsWith('enter the roundabout')) return '⟳';
  if (maneuverInstruction.startsWith('exit the roundabout')) return '↱';
  if (maneuverInstruction.includes('sharp left')) return '↶';
  if (maneuverInstruction.includes('sharp right')) return '↷';
  if (maneuverInstruction.includes('turn left')) return '←';
  if (maneuverInstruction.includes('turn right')) return '→';
  
  switch (maneuverType) {
    case 'depart': return '●';
    case 'arrive': return '◎';
    case 'turn':
      if (maneuverInstruction.includes('left')) return '←';
      if (maneuverInstruction.includes('right')) return '→';
      return '→';
    case 'roundabout': return '⟳';
    case 'exit roundabout': return '↱';
    case 'sharp left': return '↶';
    case 'sharp right': return '↷';
    case 'merge': return '↣';
    case 'straight': return '↑';
    default: return '→';
  }
}

function setCurrentStep(index, step) {
  try {
    currentStepIndex.value = index;
    emit('step-selected', { index, step });
  } catch (error) {
    console.error('Error setting current step:', error);
    // Optionally show an error notification
  }
}

// Also add error handling to the hover handlers
function handleStepHover(index) {
  try {
    emit('step-hover', index);
  } catch (error) {
    console.error('Error handling step hover:', error);
  }
}

function handleStepLeave() {
  try {
    emit('step-hover', null);
  } catch (error) {
    console.error('Error handling step leave:', error);
  }
}
</script>

<style scoped>

#instructions {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 380px;
  max-height: calc(100vh - 40px);
  overflow: hidden;
  display: none;
  z-index: 1;
  transition: all 0.3s ease;
}

#instructions.active {
  display: block;
  animation: slideIn 0.3s ease;
}

.route-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--background-color);
  border-bottom: 1px solid var(--border-color);
  border-radius: 12px 12px 0 0;
  position: sticky;
  top: 0;
  z-index: 2;
}

.route-header h2 {
  margin: 0;
  color: var(--text-color);
  font-size: 18px;
  font-weight: 600;
}

.minimize-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: var(--text-secondary);
  border-radius: 50%;
  transition: all 0.2s ease;
}

.minimize-button:hover {
  background: rgba(0, 0, 0, 0.05);
  color: var(--text-color);
}

.route-content {
  height: calc(100vh - 140px);
  transition: max-height 0.3s ease;
}

.route-content.minimized {
  height: auto;
}

.route-summary {
  padding: 12px;
  background: var(--background-color);
  border-bottom: 1px solid var(--border-color);
}

.summary-grid {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.route-summary-item {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.summary-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: var(--primary-color);
  border-radius: 6px;
  color: white;
  flex-shrink: 0;
}

.summary-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.summary-label {
  font-size: 11px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.summary-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-color);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.route-steps-container {
  overflow-y: auto;
  height: calc(100% - 120px);
  background: var(--background-color);
}

.progress-bar {
  height: 4px;
  background: var(--border-color);
  margin: 0 16px;
  position: sticky;
  top: 0;
  z-index: 1;
}

.progress {
  height: 100%;
  background: var(--primary-color);
  transition: width 0.3s ease;
}

.steps-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.steps-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.2s ease;
}

.steps-list li:hover {
  background: rgba(37, 99, 235, 0.05);
}

.steps-list li.active {
  background: rgba(37, 99, 235, 0.1);
  border-left: 4px solid var(--primary-color);
}

.step-number {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
  min-width: 0;
}

.step-instruction {
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-color);
}

.step-distance {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.step-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.step-icon :deep(svg) {
  width: 16px;
  height: 16px;
}

.highlight-distance {
  color: var(--primary-color);
  font-weight: 500;
}

.highlight-street {
  color: var(--text-color);
  font-weight: 600;
}

.error-message, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 32px 16px;
  text-align: center;
  color: var(--text-secondary);
}

.error-message svg {
  color: var(--error-color);
}

.empty-state {
  padding: 48px 16px;
}

.empty-state svg {
  color: var(--text-secondary);
  opacity: 0.7;
}

.empty-state p {
  font-size: 14px;
  line-height: 1.5;
}

/* Animations */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* List transitions */
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.list-leave-active {
  position: absolute;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  #instructions {
    width: calc(100% - 20px);
    margin: 10px;
    max-height: 60vh;
    top: auto;
    bottom: 10px;
    left: 0;
  }

  .route-content {
    height: calc(60vh - 100px);
  }

  .route-steps-container {
    height: calc(100% - 120px);
  }

  .summary-grid {
    gap: 6px;
  }

  .route-summary-item {
    padding: 6px;
  }

  .summary-value {
    font-size: 12px;
  }

  .summary-label {
    font-size: 10px;
  }

  .step-instruction {
    font-size: 13px;
  }

  .steps-list li {
    padding: 12px;
  }
}

/* Extra small screens */
@media (max-width: 360px) {
  .summary-grid {
    flex-direction: column;
    gap: 8px;
  }

  .route-summary-item {
    padding: 8px;
  }

  .summary-value {
    font-size: 13px;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .route-summary-item {
    background: rgba(255, 255, 255, 0.05);
  }

  .steps-list li:hover {
    background: rgba(255, 255, 255, 0.05);
  }

  .steps-list li.active {
    background: rgba(37, 99, 235, 0.2);
  }

  .minimize-button:hover {
    background: rgba(255, 255, 255, 0.1);
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  #instructions,
  .route-content,
  .steps-list li,
  .route-summary-item {
    transition: none;
  }

  .list-move,
  .list-enter-active,
  .list-leave-active {
    transition: none;
  }
}
/* Add hover interaction styles */
.steps-list li {
  transition: all 0.2s ease;
}

.steps-list li:hover {
  transform: translateX(4px);
  background: rgba(37, 99, 235, 0.08);
}

.steps-list li.active {
  background: rgba(37, 99, 235, 0.12);
  border-left: 4px solid var(--primary-color);
  transform: translateX(4px);
}
</style>