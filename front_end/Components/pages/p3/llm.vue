<template>
  <div class="llm-test-page">
    <div class="page-header">
      <h1>Vehicle Assistant Test</h1>
      <div class="version-indicator">v1.0</div>
    </div>
    
    <div class="conversation-container">
      <!-- Agent Nexus Component -->
      <AgentNexus ref="agentNexus" />
      
      <!-- Divider with indicator -->
      <div class="divider">
        <div class="divider-line"></div>
        <div class="input-label">Your Input</div>
        <div class="divider-line"></div>
      </div>
      
      <!-- Input Component -->
      <MultiModalInput @messageSent="handleMessageSent" />
    </div>
    
    <!-- System Status -->
    <div class="system-status">
      <div class="status-item">
        <span class="status-label">System:</span>
        <span class="status-value" :class="{ active: systemActive }">{{ systemActive ? 'Active' : 'Initializing...' }}</span>
      </div>
      <div class="status-item">
        <span class="status-label">Agent:</span>
        <span class="status-value">{{ currentAgent || 'None' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import AgentNexus from '@/components/p3/llm/AgentNexus.vue'
import MultiModalInput from '@/components/p3/llm/MultiModalInput.vue'

// References
const agentNexus = ref(null)
const systemActive = ref(false)
const startTime = ref(Date.now())

// Computed properties
const currentAgent = computed(() => {
  return agentNexus.value?.currentAgent || 'Vehicle Assistant'
})

// Handlers
const handleMessageSent = () => {
  if (agentNexus.value) {
    agentNexus.value.clearMessage()
  }
}

// Lifecycle hooks
onMounted(() => {
  // Simulate system coming online
  setTimeout(() => {
    systemActive.value = true
  }, 2000)
})
</script>

<style scoped>
.llm-test-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(to bottom, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
  color: #e2e8f0;
  padding: 1.5rem 2rem;
  position: relative;
  overflow: hidden;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(51, 65, 85, 0.5);
}

.page-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.version-indicator {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.conversation-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.divider {
  display: flex;
  align-items: center;
  width: 100%;
  margin: 0.5rem 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: rgba(51, 65, 85, 0.5);
}

.input-label {
  color: #94a3b8;
  font-size: 0.875rem;
  margin: 0 1rem;
  white-space: nowrap;
}

.system-status {
  display: flex;
  gap: 2rem;
  background: rgba(15, 23, 42, 0.8);
  padding: 1rem;
  border-radius: 0.75rem;
  border: 1px solid rgba(51, 65, 85, 0.5);
  margin-top: auto;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-label {
  color: #94a3b8;
  font-size: 0.875rem;
}

.status-value {
  color: #e2e8f0;
  font-size: 0.875rem;
  font-weight: 500;
  background: rgba(51, 65, 85, 0.5);
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
}

.status-value.active {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

/* Light Mode Support */
@media (prefers-color-scheme: light) {
  .llm-test-page {
    background: linear-gradient(to bottom, rgba(248, 250, 252, 0.95), rgba(241, 245, 249, 0.95));
    color: #1e293b;
  }

  .page-header h1 {
    color: #1e293b;
  }

  .divider-line {
    background: rgba(226, 232, 240, 0.8);
  }

  .input-label {
    color: #64748b;
  }

  .system-status {
    background: rgba(248, 250, 252, 0.8);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .status-label {
    color: #64748b;
  }

  .status-value {
    color: #1e293b;
    background: rgba(226, 232, 240, 0.8);
  }

  .status-value.active {
    background: rgba(59, 130, 246, 0.1);
    color: #3b82f6;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .llm-test-page {
    padding: 1rem;
  }

  .page-header h1 {
    font-size: 1.25rem;
  }

  .conversation-container {
    gap: 1rem;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .llm-test-page {
    background: white;
    color: black;
  }

  .page-header {
    border-bottom: 2px solid black;
  }

  .page-header h1 {
    color: black;
  }

  .version-indicator {
    background: white;
    color: black;
    border: 2px solid black;
  }

  .divider-line {
    background: black;
    height: 2px;
  }

  .input-label {
    color: black;
  }

  .system-status {
    background: white;
    border: 2px solid black;
  }

  .status-label, .status-value {
    color: black;
  }

  .status-value {
    background: white;
    border: 1px solid black;
  }

  .status-value.active {
    background: #e0e0e0;
    border: 2px solid black;
  }
}
</style>
