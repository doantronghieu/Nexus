<template>
  <header class="header">
    <div class="logo">
      <span class="logo-icon">⚡</span>
      <span class="logo-text">CPO Support</span>
    </div>
    
    <div class="search-container">
      <input 
        type="text" 
        placeholder="Search charger, customer, or case ID..." 
        class="search-input"
        :value="searchQuery"
        @input="$emit('update:search-query', $event.target.value)"
        @keyup.enter="$emit('search')"
      />
      <button class="search-button" @click="$emit('search')">🔍</button>
    </div>
    
    <div class="user-controls">
      <div class="language-selector">
        <select 
          :value="selectedLanguage"
          @change="$emit('update:selected-language', $event.target.value)"
        >
          <option value="en">English</option>
          <option value="de">German</option>
          <option value="fr">French</option>
          <option value="es">Spanish</option>
          <option value="it">Italian</option>
        </select>
      </div>
      
      <div class="agent-info">
        <span class="agent-icon">👤</span>
        <span class="agent-name">Agent: AGT-456</span>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderBar',
  props: {
    searchQuery: {
      type: String,
      default: ''
    },
    selectedLanguage: {
      type: String,
      default: 'en'
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #fff;
  border-bottom: 1px solid var(--neutral-300);
  height: 48px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-right: 24px;
}

.logo-icon {
  font-size: 18px;
  color: var(--primary-blue);
}

.logo-text {
  font-weight: 600;
  color: var(--neutral-900);
}

.search-container {
  position: relative;
  width: 400px;
  margin-right: auto;
}

.search-input {
  width: 100%;
  padding: 6px 32px 6px 8px;
  border: 1px solid var(--neutral-300);
  border-radius: 4px;
  font-size: 13px;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-blue);
}

.search-button {
  position: absolute;
  right: 4px;
  top: 4px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: var(--neutral-600);
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.language-selector select {
  padding: 4px 8px;
  border: 1px solid var(--neutral-300);
  border-radius: 4px;
  background-color: #fff;
  font-size: 13px;
}

.agent-info {
  display: flex;
  align-items: center;
  gap: 6px;
}

.agent-icon {
  font-size: 16px;
}

.agent-name {
  font-size: 13px;
  color: var(--neutral-700);
}

@media (max-width: 768px) {
  .search-container {
    width: 200px;
  }
  
  .agent-name {
    display: none;
  }
}
</style>
