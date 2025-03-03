<template>
  <div class="dashboard-layout">
    <nav class="dashboard-nav">
      <NuxtLink to="/" class="nav-item">Camera</NuxtLink>
      <NuxtLink to="/dashboard/status" class="nav-item">Status</NuxtLink>
      <NuxtLink to="/dashboard/settings" class="nav-item">Settings</NuxtLink>
    </nav>
    
    <main class="dashboard-content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  background: #f5f5f5;
}

.dashboard-nav {
  display: flex;
  gap: 20px;
  padding: 16px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-item {
  text-decoration: none;
  color: #666;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.2s;
}

.nav-item:hover {
  background: #f5f5f5;
}

.nav-item.router-link-active {
  background: #e3f2fd;
  color: #2196F3;
}

.dashboard-content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .dashboard-nav {
    padding: 12px;
    gap: 12px;
  }

  .nav-item {
    padding: 6px 12px;
    font-size: 14px;
  }

  .dashboard-content {
    padding: 16px;
  }
}
</style>