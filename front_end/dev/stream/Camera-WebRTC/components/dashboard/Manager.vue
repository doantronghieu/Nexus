<template>
  <div class="manager-dashboard">
    <!-- Client List Section -->
    <div class="clients-section">
      <h2 class="section-title">
        Connected Clients
        <span class="connection-status" :class="connectionStatus">
          {{ connectionStatus }}
        </span>
      </h2>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="clients.length === 0" class="no-clients">
        <div class="placeholder-content">
          <Users class="placeholder-icon" />
          <p>No clients connected</p>
        </div>
      </div>

      <div v-else class="client-list">
        <div 
          v-for="client in clients" 
          :key="client.client_id"
          class="client-card"
          :class="{ 
            'active': selectedClient?.client_id === client.client_id,
            'streaming': client.is_streaming 
          }"
          @click="selectClient(client)"
        >
          <div class="client-info">
            <div class="client-header">
              <h3 class="client-id">{{ truncateClientId(client.client_id) }}</h3>
              <span 
                class="status-indicator"
                :class="{ 'active': client.is_streaming }"
              >
                {{ client.is_streaming ? 'Streaming' : 'Connected' }}
              </span>
            </div>
            <div class="client-details">
              <p class="detail-item">
                <span class="label">Connected:</span>
                {{ formatTime(client.connection_time) }}
              </p>
              <p class="detail-item">
                <span class="label">Frames:</span>
                {{ client.frames_count }}
              </p>
              <p class="detail-item" v-if="client.last_frame_time">
                <span class="label">Last Frame:</span>
                {{ formatTime(client.last_frame_time) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Frame Viewer Section -->
    <div class="frame-viewer-section">
      <div v-if="selectedClient" class="frame-viewer">
        <h3 class="viewer-title">
          Stream: {{ truncateClientId(selectedClient.client_id) }}
          <span 
            class="status-badge"
            :class="{ 'active': selectedClient.is_streaming }"
          >
            {{ selectedClient.is_streaming ? 'Live' : 'Inactive' }}
          </span>
        </h3>
        <div class="frame-container">
          <div v-if="frameError" class="frame-error">
            <AlertCircle class="error-icon" />
            <p>{{ frameError }}</p>
          </div>
          <img 
            v-else
            ref="frameImage"
            :src="frameUrl" 
            alt="Client stream"
            class="frame-image"
            @error="handleFrameError"
            @load="handleFrameLoad"
            :style="{
              opacity: isFrameLoading ? 0.7 : 1,
              transition: 'opacity 0.1s ease'
            }"
          />
        </div>
      </div>
      <div v-else class="no-client-selected">
        <div class="placeholder-content">
          <MonitorPlay class="placeholder-icon" />
          <p>Select a client to view their stream</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useConfig } from '~/composables/useConfig'
import { useNotification } from '~/composables/useNotification'
import { MonitorPlay, Users, AlertCircle } from 'lucide-vue-next'

const { 
  getFastAPIBaseUrl, 
  connectionStatus: wsConnectionStatus,
  setupWebSocket,
  addMessageHandler,
  removeMessageHandler 
} = useConfig()

const { error: showError } = useNotification()

const clients = ref([])
const selectedClient = ref(null)
const frameUpdateCounter = ref(0)
const error = ref(null)
const frameError = ref(null)
const isFrameLoading = ref(false)
const lastFrameTime = ref(0)
const frameUpdateDelay = 100 // Minimum time between updates in ms


const connectionStatus = computed(() => wsConnectionStatus.value?.state || 'disconnected')

const frameUrl = computed(() => {
  if (!selectedClient.value) return ''
  return `${getFastAPIBaseUrl()}/manager/clients/${selectedClient.value.client_id}/latest-frame?t=${lastFrameTime.value}`
})

function handleFrameLoad() {
  isFrameLoading.value = false
  frameError.value = null
}

function handleFrameError() {
  isFrameLoading.value = false
  if (selectedClient.value?.is_streaming) {
    frameError.value = 'Failed to load latest frame'
  }
}

function updateFrame() {
  if (!selectedClient.value?.is_streaming) return
  isFrameLoading.value = true
  lastFrameTime.value = Date.now()
}

function handleMessage(data) {
  try {
    if (data.type === 'client_update') {
      updateClient(data.client)
      // Check if this update is for the selected client
      if (selectedClient.value?.client_id === data.client.client_id) {
        const now = Date.now()
        // Only update if enough time has passed since last update
        if (now - lastFrameTime.value >= frameUpdateDelay) {
          updateFrame()
        }
      }
    } else if (data.type === 'client_disconnected') {
      handleClientDisconnect(data.client_id)
    }
  } catch (err) {
    console.error('Error handling websocket message:', err)
  }
}

function updateClient(clientData) {
  const index = clients.value.findIndex(c => c.client_id === clientData.client_id)
  
  if (index !== -1) {
    // Update existing client
    clients.value[index] = {
      ...clients.value[index],
      ...clientData
    }
    
    // If this is the selected client, update it
    if (selectedClient.value?.client_id === clientData.client_id) {
      selectedClient.value = clients.value[index]
      if (clientData.is_streaming) {
        frameError.value = null
        refreshFrame()
      }
    }
  } else {
    // Add new client
    clients.value.push(clientData)
  }
}

function handleClientDisconnect(clientId) {
  const index = clients.value.findIndex(c => c.client_id === clientId)
  if (index !== -1) {
    clients.value.splice(index, 1)
    if (selectedClient.value?.client_id === clientId) {
      selectedClient.value = null
      showError('Selected client disconnected')
    }
  }
}

function refreshFrame() {
  frameUpdateCounter.value = Date.now()
}

async function fetchClients() {
  try {
    const response = await fetch(`${getFastAPIBaseUrl()}/manager/clients`)
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}: ${response.statusText}`)
    }
    const data = await response.json()
    clients.value = data
    
    // Update selected client if it exists
    if (selectedClient.value) {
      const updated = data.find(c => c.client_id === selectedClient.value.client_id)
      if (updated) {
        selectedClient.value = updated
      } else {
        selectedClient.value = null
        showError('Selected client no longer connected')
      }
    }
    
    error.value = null
  } catch (err) {
    console.error('Error fetching clients:', err)
    error.value = `Failed to fetch clients: ${err.message}`
  }
}

function selectClient(client) {
  selectedClient.value = client
  frameError.value = null
  refreshFrame()
}

function formatTime(timestamp) {
  if (!timestamp) return 'N/A'
  const date = new Date(timestamp)
  return new Intl.DateTimeFormat('default', {
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric'
  }).format(date)
}

function truncateClientId(id) {
  if (!id) return ''
  if (id.length <= 12) return id
  return `${id.slice(0, 8)}...${id.slice(-4)}`
}

onMounted(() => {
  // Ensure WebSocket connection is established
  setupWebSocket()
  
  // Add message handler for real-time updates
  addMessageHandler(handleMessage)
  
  // Initial fetch
  fetchClients()
  
  onUnmounted(() => {
    removeMessageHandler(handleMessage)
  })
})
</script>

<style scoped>
.manager-dashboard {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 24px;
  height: calc(100vh - 64px); /* Account for nav bar */
  padding: 16px;
  overflow: hidden; /* Prevent overall dashboard scroll */
}

.clients-section {
  background: #1E1E1E;
  border-radius: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.section-title {
  font-size: 18px;
  font-weight: 500;
  color: #FFFFFF;
  padding: 16px;
  margin: 0;
  flex-shrink: 0; /* Prevent title from shrinking */
}

.client-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 16px 16px;
  overflow-y: auto; /* Allow list to scroll */
  flex: 1; /* Take remaining space */
}

.client-card {
  background: #2D2D2D;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.client-card:hover {
  background: #383838;
}

.client-card.active {
  background: #383838;
  border: 1px solid #2196F3;
}

.client-card.streaming .status-indicator {
  background: #4CAF50;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.6; }
  100% { opacity: 1; }
}

.client-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.client-id {
  font-size: 16px;
  font-weight: 500;
  color: #FFFFFF;
}

.status-indicator {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  background: #404040;
  color: #FFFFFF;
}

.status-indicator.active {
  background: #4CAF50;
}

.client-details {
  font-size: 12px;
  color: #808080;
}

.detail-item {
  margin: 4px 0;
}

.label {
  color: #A0A0A0;
  margin-right: 4px;
}

.frame-viewer-section {
  background: #1E1E1E;
  border-radius: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.viewer-title {
  padding: 16px;
  font-size: 18px;
  font-weight: 500;
  color: #FFFFFF;
  background: #2D2D2D;
  flex-shrink: 0; /* Prevent title from shrinking */
}

.status-badge {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  background: #404040;
  color: #FFFFFF;
}

.status-badge.active {
  background: #4CAF50;
  animation: pulse 2s infinite;
}

.frame-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000000;
  overflow: hidden;
  position: relative;
}

.frame-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  will-change: opacity;
  backface-visibility: hidden;
  transform: translateZ(0);
}

.frame-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #f44336;
}

.error-icon {
  width: 24px;
  height: 24px;
}

.no-client-selected,
.no-clients {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2D2D2D;
  min-height: 400px;
}

.placeholder-content {
  text-align: center;
  color: #808080;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.placeholder-icon {
  width: 48px;
  height: 48px;
  color: #808080;
}

.error-message {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.2);
  color: #f44336;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 16px;
  font-size: 14px;
}

.connection-status {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  margin-left: 8px;
  text-transform: capitalize;
}

.connection-status.connected {
  background: #4CAF50;
  color: white;
}

.connection-status.disconnected {
  background: #f44336;
  color: white;
}

.connection-status.error {
  background: #ff9800;
  color: white;
}

/* Light theme */
@media (prefers-color-scheme: light) {
  .clients-section,
  .frame-viewer-section {
    background: #FFFFFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .section-title {
    color: #000000;
  }

  .client-card {
    background: #F5F5F5;
  }

  .client-card:hover {
    background: #EEEEEE;
  }

  .client-card.active {
    background: #E3F2FD;
  }

  .client-id {
    color: #000000;
  }

  .viewer-title {
    background: #F5F5F5;
    color: #000000;
  }

  .no-client-selected,
  .no-clients {
    background: #F5F5F5;
  }

  .client-details {
    color: #666666;
  }

  .label {
    color: #444444;
  }

  .placeholder-content,
  .placeholder-icon {
    color: #666666;
  }
}

/* Mobile responsive */
@media (max-width: 768px) {
  .manager-dashboard {
    grid-template-columns: 1fr;
    height: calc(100vh - 50px);
    padding: 8px;
    gap: 8px;
  }

  .clients-section {
    height: 40vh; /* Take 40% of viewport height on mobile */
    min-height: 300px;
  }

  .frame-viewer-section {
    height: calc(60vh - 32px); /* Take remaining space accounting for gaps */
  }

  .section-title,
  .viewer-title {
    padding: 12px;
    font-size: 16px;
  }

  .client-list {
    padding: 0 12px 12px;
  }
}
</style>