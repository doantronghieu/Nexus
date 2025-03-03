<template>
  <section class="info-section comm-section">
    <div class="section-header">
      <div class="section-title">
        <span class="section-icon">💬</span>
        Communication Log
      </div>
      <div class="case-id">{{ caseId }}</div>
    </div>
    
    <div class="comm-details">
      <div class="messages-list" ref="messagesList" :style="{maxHeight: messagesListHeight}">
        <div v-if="entries.length === 0" class="empty-state">
          No messages yet
        </div>
        
        <div 
          v-for="(entry, index) in entries" 
          :key="index"
          class="message-item"
        >
          <div class="message-header">
            <div class="message-agent">{{ entry.agent_id }}</div>
            <div class="message-time">{{ formatTime(entry.timestamp) }}</div>
          </div>
          <div class="message-content">{{ entry.message }}</div>
        </div>
      </div>
      
      <div class="message-composer">
        <textarea 
          v-model="newMessage" 
          placeholder="Type a new note..." 
          class="message-input"
          @keyup.ctrl.enter="addMessage"
          rows="2"
        ></textarea>
        
        <div class="composer-footer">
          <div class="composer-hint">Ctrl+Enter to send</div>
          <button class="add-note-button" @click="addMessage" :disabled="!newMessage.trim()">
            Add Note
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'CommunicationLog',
  props: {
    caseId: {
      type: String,
      default: ''
    },
    initialEntries: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      entries: [...this.initialEntries],
      newMessage: '',
      messagesListHeight: 'calc(100% - 120px)'
    }
  },
  updated() {
    this.scrollToBottom();
  },
  methods: {
    formatTime(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    addMessage() {
      if (!this.newMessage.trim()) return;
      
      const newEntry = {
        timestamp: new Date().toISOString(),
        agent_id: 'AGT-456',
        message: this.newMessage.trim()
      };
      
      this.entries.push(newEntry);
      this.$emit('entry-added', newEntry);
      this.newMessage = '';
    },
    scrollToBottom() {
      if (this.$refs.messagesList) {
        this.$refs.messagesList.scrollTop = this.$refs.messagesList.scrollHeight;
      }
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

.case-id {
  font-family: monospace;
  font-size: 12px;
  color: var(--neutral-600);
}

.comm-details {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.messages-list {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  border-bottom: none;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--neutral-600);
  font-style: italic;
}

.message-item {
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--neutral-200);
}

.message-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.message-agent {
  font-size: 12px;
  font-weight: 500;
  color: var(--primary-blue);
}

.message-time {
  font-size: 12px;
  color: var(--neutral-600);
}

.message-content {
  font-size: 13px;
  line-height: 1.4;
}

.message-composer {
  padding: 12px;
  background-color: #fff;
  border-top: 1px solid var(--neutral-200);
  position: sticky;
  bottom: 0;
  width: 100%;
}

.message-input {
  width: 100%;
  padding: 8px;
  border: 1px solid var(--neutral-300);
  border-radius: 4px;
  font-size: 13px;
  font-family: inherit;
  resize: none;
  height: 50px;
  margin-bottom: 8px;
}

.message-input:focus {
  outline: none;
  border-color: var(--primary-blue);
}

.composer-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.composer-hint {
  font-size: 11px;
  color: var(--neutral-600);
}

.add-note-button {
  background-color: var(--primary-blue);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.add-note-button:hover {
  background-color: #2954d4;
}

.add-note-button:disabled {
  background-color: var(--neutral-400);
  cursor: not-allowed;
}
</style>
