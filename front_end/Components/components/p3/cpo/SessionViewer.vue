<template>
  <section class="info-section session-section">
    <div class="section-header">
      <div class="section-title">
        <span class="section-icon">⚡</span>
        Charging Session
      </div>
      <div class="session-id">{{ session.session_id }}</div>
    </div>
    
    <div class="session-details">
      <div class="session-time">
        <div class="time-start">
          <div class="time-value">{{ formatTime(session.start_time) }}</div>
          <div class="percent-value">{{ session.start_percentage }}%</div>
        </div>
        
        <div class="time-end">
          <div class="time-value">{{ formatTime(session.end_time) }}</div>
          <div class="percent-value">{{ session.end_percentage }}%</div>
        </div>
      </div>
      
      <div class="charging-progress">
        <div class="progress-bar">
          <div 
            class="progress-fill interrupted" 
            :style="{ width: calculateProgressWidth() + '%' }"
          ></div>
        </div>
      </div>
      
      <div class="session-info-grid">
        <div class="session-info-group">
          <div class="info-label">Duration</div>
          <div class="info-value">{{ calculateDuration(session.start_time, session.end_time) }}</div>
        </div>
        
        <div class="session-info-group">
          <div class="info-label">Status</div>
          <div class="info-value status-interrupted">{{ session.status }}</div>
        </div>
        
        <div class="session-info-group">
          <div class="info-label">Energy</div>
          <div class="info-value">{{ session.energy_delivered }} {{ session.energy_unit }}</div>
        </div>
        
        <div class="session-info-group" v-if="session.payment">
          <div class="info-label">Payment</div>
          <div class="info-value">
            {{ formatAmount(session.payment.amount, session.payment.currency) }}
            <div class="payment-method">via {{ session.payment.method }}</div>
          </div>
        </div>
      </div>
      
      <div class="error-section" v-if="hasErrors">
        <div class="error-header">
          <div class="error-title">Error Logs</div>
          <div class="error-count">{{ session.error_logs.length }} errors</div>
        </div>
        
        <div class="error-list">
          <div 
            v-for="(error, index) in session.error_logs" 
            :key="index"
            class="error-item"
          >
            <div class="error-time">{{ formatTime(error.timestamp) }}</div>
            <div class="error-code">{{ error.code }}</div>
            <div class="error-message">{{ error.message }}</div>
            <div class="error-severity medium">{{ error.severity }}</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SessionViewer',
  props: {
    session: {
      type: Object,
      required: true
    }
  },
  computed: {
    hasErrors() {
      return this.session.error_logs && this.session.error_logs.length > 0;
    }
  },
  methods: {
    formatTime(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    calculateProgressWidth() {
      const start = this.session.start_percentage || 0;
      const end = this.session.end_percentage || 0;
      const total = 100 - start;
      const actual = end - start;
      
      if (total <= 0) return 0;
      return (actual / total) * 100;
    },
    calculateDuration(startTime, endTime) {
      if (!startTime || !endTime) return '';
      
      const start = new Date(startTime);
      const end = new Date(endTime);
      const durationMs = end - start;
      
      const minutes = Math.floor(durationMs / 60000);
      return `${minutes}m`;
    },
    formatAmount(amount, currency) {
      if (amount === undefined) return '';
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency || 'EUR'
      }).format(amount);
    }
  }
}
</script>

<style scoped>
.info-section {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background-color: var(--neutral-100);
  border-bottom: 1px solid var(--neutral-200);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  font-size: 14px;
}

.section-icon {
  font-size: 16px;
}

.session-id {
  font-family: monospace;
  font-size: 12px;
  color: var(--neutral-600);
}

.session-details {
  padding: 12px;
}

.session-time {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.time-value {
  font-size: 12px;
  color: var(--neutral-600);
}

.percent-value {
  font-size: 13px;
  font-weight: 500;
}

.charging-progress {
  margin-bottom: 16px;
}

.progress-bar {
  height: 8px;
  background-color: var(--neutral-200);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--success-green);
}

.progress-fill.interrupted {
  background-color: var(--error-red);
}

.session-info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.info-label {
  font-size: 12px;
  color: var(--neutral-600);
  margin-bottom: 4px;
}

.info-value {
  font-size: 13px;
  font-weight: 500;
}

.status-interrupted {
  color: var(--error-red);
}

.payment-method {
  font-size: 12px;
  color: var(--neutral-600);
  font-weight: normal;
  margin-top: 2px;
}

.error-section {
  margin-top: 12px;
}

.error-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.error-title {
  font-size: 13px;
  font-weight: 500;
}

.error-count {
  font-size: 12px;
  color: var(--neutral-600);
}

.error-list {
  background-color: var(--neutral-100);
  border-radius: 4px;
  overflow: hidden;
  max-height: 150px;
  overflow-y: auto;
}

.error-item {
  display: flex;
  align-items: center;
  padding: 8px;
  gap: 8px;
  border-bottom: 1px solid var(--neutral-200);
}

.error-item:last-child {
  border-bottom: none;
}

.error-time {
  font-size: 12px;
  color: var(--neutral-600);
  width: 60px;
}

.error-code {
  font-family: monospace;
  font-size: 12px;
  font-weight: 500;
  width: 80px;
}

.error-message {
  font-size: 12px;
  flex: 1;
}

.error-severity {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 10px;
  text-transform: capitalize;
}

.error-severity.medium {
  background-color: rgba(255, 184, 0, 0.1);
  color: var(--warning-yellow);
}
</style>
