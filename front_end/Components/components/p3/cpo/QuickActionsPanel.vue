<template>
  <div class="quick-actions">
    <h3 class="panel-title">Quick Actions</h3>
    
    <div class="action-buttons">
      <button class="action-button restart" @click="performAction('restart')">
        <div class="button-icon">⟳</div>
        <div class="button-text">Remote Restart</div>
      </button>
      
      <button class="action-button diagnostics" @click="performAction('diagnostics')">
        <div class="button-icon">🔍</div>
        <div class="button-text">Run Diagnostics</div>
      </button>
      
      <button class="action-button logs" @click="performAction('logs')">
        <div class="button-icon">📋</div>
        <div class="button-text">View Error Logs</div>
      </button>
      
      <button class="action-button escalate" @click="performAction('escalate')">
        <div class="button-icon">⚠️</div>
        <div class="button-text">Escalate Issue</div>
      </button>
    </div>
    
    <div v-if="lastAction" class="action-status">
      <div class="status-message">{{ statusMessage }}</div>
      <div v-if="actionInProgress" class="loading-indicator">
        <div class="loading-spinner"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuickActionsPanel',
  props: {
    chargerId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      lastAction: null,
      actionInProgress: false,
      statusMessage: ''
    }
  },
  methods: {
    performAction(action) {
      this.lastAction = action;
      this.actionInProgress = true;
      
      // Simulate action being performed
      setTimeout(() => {
        this.actionInProgress = false;
        
        switch(action) {
          case 'restart':
            this.statusMessage = `Restart command sent to charger ${this.chargerId}`;
            break;
          case 'diagnostics':
            this.statusMessage = `Diagnostics running on charger ${this.chargerId}`;
            break;
          case 'logs':
            this.statusMessage = `Retrieved error logs for charger ${this.chargerId}`;
            break;
          case 'escalate':
            this.statusMessage = `Issue escalated to Level 2 support`;
            break;
        }
        
        this.$emit('action-performed', { action, chargerId: this.chargerId });
      }, 1500);
    }
  }
}
</script>

<style scoped>
.quick-actions {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1rem;
}

.panel-title {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: 500;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button:hover {
  background-color: #f8f9fa;
}

.button-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.button-text {
  font-size: 0.875rem;
  text-align: center;
}

.restart:hover {
  border-color: #28a745;
}

.diagnostics:hover {
  border-color: #007bff;
}

.logs:hover {
  border-color: #6c757d;
}

.escalate:hover {
  border-color: #dc3545;
}

.action-status {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-size: 0.875rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 123, 255, 0.2);
  border-radius: 50%;
  border-top-color: #007bff;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
