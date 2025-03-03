<template>
  <section class="info-section issue-section">
    <div class="section-header">
      <div class="section-title">
        <span class="section-icon">⚠️</span>
        Active Issue
      </div>
      <div class="status-badges">
        <div class="status-badge open">{{ supportCase.status || 'open' }}</div>
        <div class="status-badge medium">{{ supportCase.priority || 'Medium' }}</div>
      </div>
    </div>
    
    <div class="issue-details">
      <div class="issue-id">
        <div class="case-id">{{ supportCase.case_id }}</div>
        <div class="case-age">Opened {{ calculateDaysAgo(supportCase.created_at) }} days ago</div>
      </div>
      
      <div class="issue-type">{{ formatIssueType(supportCase.issue_type) }}</div>
      
      <div class="issue-description">
        {{ supportCase.description }}
      </div>
      
      <div class="troubleshooting-section" v-if="supportCase.troubleshooting_steps && supportCase.troubleshooting_steps.length">
        <div class="troubleshooting-header">
          <div class="troubleshooting-title">Troubleshooting Progress</div>
          <div class="troubleshooting-status">{{ completedSteps }}/{{ supportCase.troubleshooting_steps.length }} completed</div>
        </div>
        
        <div class="steps-list">
          <div 
            v-for="(step, index) in supportCase.troubleshooting_steps" 
            :key="index"
            class="step-item"
          >
            <div class="step-indicator" :class="step.status"></div>
            <div class="step-content">
              <div class="step-name">{{ step.step }}</div>
              <div v-if="step.notes" class="step-notes">{{ step.notes }}</div>
            </div>
            <div v-if="step.timestamp" class="step-time">{{ formatTime(step.timestamp) }}</div>
          </div>
        </div>
      </div>
      
      <div class="section-footer right-aligned">
        <button class="primary-button">Add Step</button>
        <button class="primary-button">Resolve Issue</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ActiveIssuePanel',
  props: {
    supportCase: {
      type: Object,
      required: true
    }
  },
  computed: {
    completedSteps() {
      if (!this.supportCase.troubleshooting_steps) return 0;
      return this.supportCase.troubleshooting_steps.filter(step => step.status === 'completed').length;
    }
  },
  methods: {
    formatIssueType(type) {
      if (!type) return 'Charging Interrupted';
      return type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    },
    formatTime(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    calculateDaysAgo(dateString) {
      if (!dateString) return 123;
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
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

.status-badges {
  display: flex;
  gap: 6px;
}

.status-badge {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: lowercase;
}

.status-badge.open {
  background-color: rgba(53, 99, 233, 0.1);
  color: var(--primary-blue);
}

.status-badge.medium {
  background-color: rgba(255, 184, 0, 0.1);
  color: var(--warning-yellow);
}

.issue-details {
  padding: 12px;
}

.issue-id {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.case-id {
  font-size: 13px;
  font-weight: 500;
}

.case-age {
  font-size: 12px;
  color: var(--neutral-600);
}

.issue-type {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
}

.issue-description {
  font-size: 13px;
  line-height: 1.4;
  padding: 8px 10px;
  background-color: var(--neutral-100);
  border-radius: 4px;
  margin-bottom: 16px;
}

.troubleshooting-section {
  margin-bottom: 16px;
  max-height: 150px;
  overflow-y: auto;
}

.troubleshooting-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.troubleshooting-title {
  font-size: 13px;
  font-weight: 500;
}

.troubleshooting-status {
  font-size: 12px;
  color: var(--neutral-600);
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.step-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 3px;
}

.step-indicator.completed {
  background-color: var(--success-green);
}

.step-indicator.pending {
  background-color: var(--neutral-500);
}

.step-content {
  flex: 1;
}

.step-name {
  font-size: 13px;
  margin-bottom: 2px;
}

.step-notes {
  font-size: 12px;
  color: var(--neutral-600);
}

.step-time {
  font-size: 12px;
  color: var(--neutral-600);
  min-width: 70px;
  text-align: right;
}

.section-footer {
  display: flex;
  gap: 12px;
  padding-top: 8px;
}

.right-aligned {
  justify-content: flex-end;
}

.primary-button {
  background-color: var(--primary-blue);
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.primary-button:hover {
  background-color: #2954d4;
}
</style>
