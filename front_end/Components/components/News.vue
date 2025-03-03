<template>
  <div class="news-dashboard">
    <div class="news-container">
      <!-- Content Section -->
      <div class="content-wrapper">
        <!-- Header Row -->
        <div class="header-row">
          <div class="title-section">
            <h2 class="title">News Feed</h2>
            <div class="source-toggle">
              <button
                class="source-btn"
                :class="{ active: selectedSource === 'nytimes' }"
                @click="selectSource('nytimes')"
              >
                NY Times
              </button>
              <button
                class="source-btn"
                :class="{ active: selectedSource === 'vnexpress' }"
                @click="selectSource('vnexpress')"
              >
                VN Express
              </button>
            </div>
          </div>
          <div class="actions-group">
            <div class="update-status">
              <span class="status-dot" :class="{ active: !isLoading }"></span>
              <span class="status-text">{{ lastUpdatedTime }}</span>
            </div>
            <button
              @click="refreshFeed"
              class="action-button"
              :class="{ loading: isLoading }"
              :disabled="isLoading"
              aria-label="Refresh news"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 12a9 9 0 11-9-9c2.52 0 4.85.99 6.57 2.57L21 8"/>
                <path d="M21 3v5h-5"/>
              </svg>
            </button>
            <button
              @click="showSettings = true"
              class="action-button"
              aria-label="Open settings"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
                <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Articles Container -->
        <div class="articles-container" :class="{ loading: isLoading }">
          <!-- Error State -->
          <div v-if="error" class="error-state">
            <div class="error-content">
              <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              <p class="error-message">{{ error }}</p>
              <button class="retry-btn" @click="refreshFeed">
                Try Again
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-else-if="isLoading && !articles.length" class="loading-state">
            <div class="loading-indicator">
              <div class="loading-ring">
                <div></div><div></div><div></div><div></div>
              </div>
              <span class="loading-text">Loading latest news...</span>
            </div>
          </div>

          <!-- Articles List -->
          <div v-else class="carousel-container">
            <!-- Navigation Buttons -->
            <button 
              class="carousel-nav prev"
              @click="prevArticle"
              :disabled="currentIndex === 0"
              aria-label="Previous article"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M15 18l-6-6 6-6"/>
              </svg>
            </button>
            
            <button 
              class="carousel-nav next"
              @click="nextArticle" 
              :disabled="currentIndex >= articles.length - 1"
              aria-label="Next article"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 18l6-6-6-6"/>
              </svg>
            </button>

            <!-- Article Card -->
            <Transition name="slide" mode="out-in">
              <div 
                v-if="currentArticle"
                :key="currentArticle.guid"
                class="article-card"
                @click="openArticle(currentArticle.link)"
              >
                <div 
                  v-if="currentArticle.imageUrl"
                  class="article-image"
                  :style="{ backgroundImage: `url(${currentArticle.imageUrl})` }"
                ></div>
                <div class="article-content">
                  <div class="article-meta">
                    <span class="article-source">{{ selectedSource === 'nytimes' ? 'NY Times' : 'VN Express' }}</span>
                    <span class="article-time">{{ formatTime(currentArticle.pubDate) }}</span>
                  </div>
                  <h3 class="article-title">{{ currentArticle.title }}</h3>
                  <p class="article-description">{{ stripHtml(currentArticle.description) }}</p>
                  <div class="article-actions">
                    <button class="read-more-btn">
                      Read Full Article
                      <svg xmlns="http://www.w3.org/2000/svg" class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                        <polyline points="15 3 21 3 21 9"/>
                        <line x1="10" y1="14" x2="21" y2="3"/>
                      </svg>
                    </button>
                    <button class="share-btn" @click.stop="shareArticle(currentArticle)">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="18" cy="5" r="3"/>
                        <circle cx="6" cy="12" r="3"/>
                        <circle cx="18" cy="19" r="3"/>
                        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
                      </svg>
                      Share
                    </button>
                  </div>
                </div>
              </div>
            </Transition>
         </div>

         <!-- Pagination Indicators -->
         <div class="carousel-pagination">
           <button
             v-for="(_, index) in articles"
             :key="index"
             class="pagination-dot"
             :class="{ active: index === currentIndex }"
             @click="goToArticle(index)"
             :aria-label="'Go to article ' + (index + 1)"
           ></button>
         </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Settings Modal -->
  <Transition name="modal">
    <div v-if="showSettings" class="settings-modal">
      <div class="modal-overlay" @click="showSettings = false"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">Settings</h3>
          <button class="close-button" @click="showSettings = false">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="settings-row">
            <div class="setting-group">
              <label class="toggle">
                <input
                  type="checkbox"
                  v-model="settings.autoSwitch"
                  @change="handleAutoSwitchChange"
                >
                <span class="toggle-slider"></span>
              </label>
              <span class="setting-label">Auto-switch</span>
            </div>
            <div class="setting-group" v-if="settings.autoSwitch">
              <input
                type="number"
                v-model="settings.interval"
                min="1"
                max="60"
                class="interval-input"
                @change="handleIntervalChange"
              >
              <span class="setting-label">seconds</span>
            </div>
            <button 
              class="reset-button"
              @click="resetSettings"
              title="Reset to defaults"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M3 12a9 9 0 1 0 9-9 9 9 0 0 0-9 9z"/>
                <path d="M12 7v5l3 3"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>

  <!-- Share Modal -->
  <Transition name="modal">
    <div v-if="showShareModal" class="settings-modal">
      <div class="modal-overlay" @click="showShareModal = false"></div>
      <div class="modal-content share-modal">
        <div class="modal-header">
          <h3 class="modal-title">Share Article</h3>
          <button class="close-button" @click="showShareModal = false">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="share-options">
            <button class="share-option" @click="simulateShare('copy')">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
              </svg>
              <span>Copy Link</span>
            </button>
            <button class="share-option" @click="simulateShare('email')">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <span>Email</span>
            </button>
            <button class="share-option" @click="simulateShare('message')">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/>
              </svg>
              <span>Message</span>
            </button>
          </div>
          <div class="share-preview" v-if="shareArticle">
            <h4 class="share-title">{{ shareArticle.title }}</h4>
            <p class="share-description">{{ stripHtml(shareArticle.description).substring(0, 120) }}...</p>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch, computed } from 'vue'

// Settings state
const showSettings = ref(false)
const settings = reactive({
  autoSwitch: true,
  interval: 5
})

// Share modal state
const showShareModal = ref(false)
const shareArticle = ref(null)

const simulateShare = (method) => {
  if (!shareArticle.value) return
  
  let message = ''
  switch(method) {
    case 'copy':
      message = 'Link copied to clipboard!'
      break
    case 'email':
      message = 'Opening email client...'
      break
    case 'message':
      message = 'Opening messaging app...'
      break
    default:
      message = 'Sharing article...'
  }
  
  // Show status message
  showStatus(message, 'success')
  
  // Close share modal
  showShareModal.value = false
}

const handleAutoSwitchChange = () => {
  if (settings.autoSwitch) {
    startAutoSwitch()
  } else {
    stopAutoSwitch()
  }
}

const handleIntervalChange = () => {
  // Ensure interval is between 1 and 60 seconds
  settings.interval = Math.min(60, Math.max(1, settings.interval))
  if (settings.autoSwitch) {
    stopAutoSwitch()
    startAutoSwitch()
  }
}

const resetSettings = () => {
  settings.autoSwitch = true
  settings.interval = 5
  stopAutoSwitch()
  startAutoSwitch()
}

// Start auto-switching with custom interval
const startAutoSwitch = () => {
  if (!settings.autoSwitch) return
  if (autoSwitchTimer) return
  autoSwitchTimer = setInterval(() => {
    if (currentIndex.value >= articles.value.length - 1) {
      currentIndex.value = 0
    } else {
      nextArticle()
    }
  }, settings.interval * 1000)
}

// Proxy URLs through a CORS proxy service
const CORS_PROXY = 'https://api.allorigins.win/raw?url='

const RSS_URLS = {
  nytimes: 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
  vnexpress: 'https://vnexpress.net/rss/tin-moi-nhat.rss'
}

const getProxiedUrl = (url) => `${CORS_PROXY}${encodeURIComponent(url)}`

const selectedSource = ref('nytimes')
const articles = ref([])
const lastUpdatedTime = ref('Not updated')
const isLoading = ref(false)
const error = ref(null)
const currentIndex = ref(0)

// Computed property for current article
const currentArticle = computed(() => articles.value[currentIndex.value] || null)

// Auto-switching timer
let autoSwitchTimer = null

// Stop auto-switching
const stopAutoSwitch = () => {
  if (autoSwitchTimer) {
    clearInterval(autoSwitchTimer)
    autoSwitchTimer = null
  }
}

// Carousel navigation methods
const nextArticle = () => {
  stopAutoSwitch() // Stop auto-switching on manual navigation
  if (currentIndex.value < articles.value.length - 1) {
    currentIndex.value++
  }
  startAutoSwitch() // Restart auto-switching after manual navigation
}

const prevArticle = () => {
  stopAutoSwitch() // Stop auto-switching on manual navigation
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
  startAutoSwitch() // Restart auto-switching after manual navigation
}

const goToArticle = (index) => {
  stopAutoSwitch() // Stop auto-switching on manual navigation
  currentIndex.value = index
  startAutoSwitch() // Restart auto-switching after manual navigation
}

// Clean up on component unmount
onUnmounted(() => {
  stopAutoSwitch()
})

// Fetch RSS feed
const fetchRssFeed = async (url) => {
  const attempts = [
    // First try: Direct fetch with no-cors mode
    async () => {
      const response = await fetch(url, { mode: 'no-cors' })
      if (!response.ok) throw new Error('Direct fetch failed')
      return response.text()
    },
    // Second try: Through CORS proxy
    async () => {
      const proxyUrl = getProxiedUrl(url)
      const response = await fetch(proxyUrl)
      if (!response.ok) throw new Error('Proxy fetch failed')
      return response.text()
    }
  ]

  let lastError
  for (const attempt of attempts) {
    try {
      return await attempt()
    } catch (err) {
      lastError = err
      continue
    }
  }

  throw new Error('Unable to load news feed. Please try again later.')
}

// Parse XML content into a structured format
const parseNYTimesArticles = (xmlContent) => {
  const parser = new DOMParser()
  const xmlDoc = parser.parseFromString(xmlContent, 'text/xml')
  const items = xmlDoc.getElementsByTagName('item')
  
  return Array.from(items).map(item => {
    const mediaContent = item.getElementsByTagName('media:content')[0]
    const summary = item.getElementsByTagName('description')[0]?.textContent || ''
    
    // Improve summary - try to get a better description
    let description = summary
    try {
      const contentEncoded = item.getElementsByTagName('content:encoded')[0]?.textContent
      if (contentEncoded && contentEncoded.length > summary.length) {
        // Extract the first paragraph from content:encoded
        const div = document.createElement('div')
        div.innerHTML = contentEncoded
        const firstP = div.querySelector('p')
        if (firstP && firstP.textContent.length > summary.length) {
          description = firstP.textContent
        }
      }
    } catch (error) {
      // Keep using summary if there's any error
    }
    
    return {
      title: item.getElementsByTagName('title')[0]?.textContent || '',
      description: description,
      link: item.getElementsByTagName('link')[0]?.textContent || '',
      pubDate: item.getElementsByTagName('pubDate')[0]?.textContent || '',
      guid: item.getElementsByTagName('guid')[0]?.textContent || '',
      imageUrl: mediaContent?.getAttribute('url') || ''
    }
  })
}

const parseVNExpressArticles = (xmlContent) => {
  const parser = new DOMParser()
  const xmlDoc = parser.parseFromString(xmlContent, 'text/xml')
  const items = xmlDoc.getElementsByTagName('item')
  
  return Array.from(items).map(item => {
    const description = item.getElementsByTagName('description')[0]?.textContent || ''
    const imageMatch = description.match(/<img.*?src="(.*?)"/)
    
    // Try to extract a cleaner description by removing HTML tags
    let cleanDescription = description
    try {
      const div = document.createElement('div')
      div.innerHTML = description
      // Remove the image element if it exists
      const img = div.querySelector('img')
      if (img) img.remove()
      // Get text content
      cleanDescription = div.textContent.trim()
    } catch (error) {
      // Keep using original description if there's any error
    }
    
    return {
      title: item.getElementsByTagName('title')[0]?.textContent || '',
      description: cleanDescription,
      link: item.getElementsByTagName('link')[0]?.textContent || '',
      pubDate: item.getElementsByTagName('pubDate')[0]?.textContent || '',
      guid: item.getElementsByTagName('guid')[0]?.textContent || '',
      imageUrl: imageMatch ? imageMatch[1] : ''
    }
  })
}

// Format the publication time
const formatTime = (pubDate) => {
  try {
    const date = new Date(pubDate)
    const now = new Date()
    const diff = now - date
    
    // Less than an hour
    if (diff < 3600000) {
      const minutes = Math.floor(diff / 60000)
      return `${minutes} min ago`
    }
    
    // Less than a day
    if (diff < 86400000) {
      const hours = Math.floor(diff / 3600000)
      return `${hours}h ago`
    }
    
    // Format date
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    const month = months[date.getMonth()]
    const day = date.getDate()
    const hours = date.getHours()
    const minutes = date.getMinutes()
    const ampm = hours >= 12 ? 'PM' : 'AM'
    const formattedHours = hours % 12 || 12
    const formattedMinutes = minutes.toString().padStart(2, '0')
    
    return `${month} ${day}, ${formattedHours}:${formattedMinutes} ${ampm}`
  } catch (error) {
    return pubDate
  }
}

// Strip HTML tags from description
const stripHtml = (html) => {
  const tmp = document.createElement('div')
  tmp.innerHTML = html
  return (tmp.textContent || tmp.innerText || '').trim()
}

// Handle article click
const openArticle = (url) => {
  window.open(url, '_blank')
}

// Format current time for last updated
const formatCurrentTime = () => {
  const now = new Date()
  const hours = now.getHours()
  const minutes = now.getMinutes()
  const ampm = hours >= 12 ? 'PM' : 'AM'
  const formattedHours = hours % 12 || 12
  const formattedMinutes = minutes.toString().padStart(2, '0')
  return `${formattedHours}:${formattedMinutes} ${ampm}`
}

// Update articles based on selected source
const updateArticles = async () => {
  error.value = null
  isLoading.value = true
  
  try {
    const url = RSS_URLS[selectedSource.value]
    const xmlContent = await fetchRssFeed(url)
    
    const newArticles = selectedSource.value === 'nytimes'
      ? parseNYTimesArticles(xmlContent)
      : parseVNExpressArticles(xmlContent)
    
    // Filter out articles without titles or descriptions
    articles.value = newArticles.filter(article => 
      article.title && article.description && 
      article.title.trim() !== '' && 
      article.description.trim() !== ''
    )
    
    lastUpdatedTime.value = formatCurrentTime()
    
    // If no articles after filtering, show an error
    if (articles.value.length === 0) {
      throw new Error('No valid articles found in the feed')
    }
    
    // Reset current index and restart auto-switching
    currentIndex.value = 0
    stopAutoSwitch() // Stop any existing timer
    startAutoSwitch() // Start new timer
    
    // Show success message
    showStatus(`${articles.value.length} articles loaded from ${selectedSource.value === 'nytimes' ? 'NY Times' : 'VN Express'}`, 'success')
  } catch (err) {
    error.value = err.message
    articles.value = []
  } finally {
    isLoading.value = false
  }
}

// Show status message
const showStatus = (message, type = 'info') => {
  const statusElem = document.createElement('div')
  statusElem.className = `floating-status ${type}`
  statusElem.textContent = message
  
  document.body.appendChild(statusElem)
  
  // Animate in
  setTimeout(() => {
    statusElem.classList.add('show')
  }, 10)
  
  // Remove after 3 seconds
  setTimeout(() => {
    statusElem.classList.remove('show')
    setTimeout(() => {
      document.body.removeChild(statusElem)
    }, 300)
  }, 3000)
}

// Share article
const shareArticleHandler = (article) => {
  shareArticle.value = article
  showShareModal.value = true
}

// Refresh feed manually
const refreshFeed = () => {
  updateArticles()
}

// Watch for source changes
watch(selectedSource, updateArticles)

const selectSource = (source) => {
  selectedSource.value = source
}

onMounted(() => {
  updateArticles()
  
  // Add global styles for floating status
  const style = document.createElement('style')
  style.textContent = `
    .floating-status {
      position: fixed;
      bottom: 2rem;
      left: 50%;
      transform: translateX(-50%) translateY(100%);
      padding: 0.75rem 1.5rem;
      border-radius: 0.75rem;
      background: rgba(15, 23, 42, 0.9);
      color: white;
      font-size: 0.875rem;
      font-weight: 500;
      z-index: 9999;
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
      backdrop-filter: blur(0.25rem);
    }
    
    .floating-status.show {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }
    
    .floating-status.success {
      background: rgba(34, 197, 94, 0.9);
    }
    
    .floating-status.error {
      background: rgba(239, 68, 68, 0.9);
    }
    
    .floating-status.info {
      background: rgba(59, 130, 246, 0.9);
    }
  `
  document.head.appendChild(style)
})
</script>

<style scoped>
:root {
  --base-size: 1rem;  /* 16px */
  --scale-factor: 1.25;  /* For fluid scaling */
}

.news-dashboard {
  height: 100%;
  padding: 1.5rem;
}

.news-container {
  height: 100%;
  background: rgba(15, 23, 42, 0.95);
  border-radius: 1.5rem;
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.05);
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  overflow: hidden;
  position: relative;
  backdrop-filter: blur(0.75rem);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-wrapper {
  height: 100%;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Header Styling */
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.title {
  font-size: clamp(1.125rem, 2vw + 0.5rem, 1.25rem);
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
  letter-spacing: 0.01em;
  white-space: nowrap;
}

/* Source Toggle in Header */
.source-toggle {
  display: flex;
  gap: 0.25rem;
  background: rgba(30, 41, 59, 0.5);
  padding: 0.25rem;
  border-radius: 0.75rem;
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
}

.source-btn {
  padding: 0.375rem 0.75rem;
  border-radius: 0.5rem;
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  min-height: 2.75rem;  /* Minimum 44px touch target */
  min-width: 2.75rem;
}

.source-btn.active {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.source-btn:hover:not(.active) {
  background: rgba(51, 65, 85, 0.3);
  color: #e2e8f0;
}

.actions-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.update-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #94a3b8;
}

.status-dot {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background: #64748b;
  transition: all 0.3s ease;
}

.status-dot.active {
  background: #10b981;
}

.action-button {
  width: 2.75rem;  /* 44px minimum touch target */
  height: 2.75rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(51, 65, 85, 0.5);
  border: none;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover:not(:disabled) {
  background: rgba(71, 85, 105, 0.5);
  color: #e2e8f0;
  transform: translateY(-0.0625rem);
}

.action-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

.action-button.loading svg {
  animation: spin 1s linear infinite;
}

/* Articles Container */
.articles-container {
  flex: 1;
  overflow-y: auto;
  position: relative;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.article-card {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: auto 1fr;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  cursor: pointer;
  transition: all 0.2s ease;
  height: 100%;
}

.article-card:hover {
  background: rgba(30, 41, 59, 0.8);
  transform: translateY(-0.0625rem);
}

.article-image {
  width: 100%;
  height: 12rem;
  border-radius: 0.75rem;
  background-size: cover;
  background-position: center;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
}

.article-image::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(to bottom, transparent, rgba(15, 23, 42, 0.5));
  pointer-events: none;
}

.article-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 1;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-source {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  letter-spacing: 0.05em;
}

.article-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

.article-title {
  font-size: clamp(1.25rem, 2vw + 0.5rem, 1.5rem);
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
  line-height: 1.4;
}

.article-description {
  font-size: clamp(0.875rem, 1vw + 0.5rem, 1rem);
  color: #94a3b8;
  margin: 0;
  line-height: 1.6;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
}

.article-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
}

.read-more-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.read-more-btn:hover {
  background: rgba(59, 130, 246, 0.2);
}

.read-more-btn svg {
  width: 1rem;
  height: 1rem;
}

.share-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #94a3b8;
  background: rgba(51, 65, 85, 0.3);
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.share-btn:hover {
  background: rgba(51, 65, 85, 0.5);
  color: #e2e8f0;
}

.share-btn svg {
  width: 1rem;
  height: 1rem;
}

/* Loading State */
.loading-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-text {
  color: #94a3b8;
  font-size: 0.875rem;
}

.loading-ring {
  display: inline-block;
  position: relative;
  width: 2.5rem;
  height: 2.5rem;
}

.loading-ring div {
  box-sizing: border-box;
  display: block;
  position: absolute;
  width: 2rem;
  height: 2rem;
  margin: 0.25rem;
  border: 0.1875rem solid #3b82f6;
  border-radius: 50%;
  animation: loading-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  border-color: #3b82f6 transparent transparent transparent;
}

.loading-ring div:nth-child(1) { animation-delay: -0.45s; }
.loading-ring div:nth-child(2) { animation-delay: -0.3s; }
.loading-ring div:nth-child(3) { animation-delay: -0.15s; }

/* Error State */
.error-state {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  max-width: 20rem;
  text-align: center;
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  background: rgba(239, 68, 68, 0.1);
  border: 0.0625rem solid rgba(239, 68, 68, 0.2);
  border-radius: 1rem;
}

.error-icon {
  width: 2rem;
  height: 2rem;
  color: #ef4444;
}

.error-message {
  margin: 0;
  color: #ef4444;
  font-size: 0.875rem;
}

.retry-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  background: #ef4444;
  color: white;
  border: none;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 2.75rem;  /* 44px minimum touch target */
}

.retry-btn:hover {
  opacity: 0.9;
  transform: translateY(-0.0625rem);
}

/* Animations */
@keyframes loading-ring {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.news-transition-enter-from {
  opacity: 0;
  transform: translateX(50px);
}

.news-transition-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}

/* Carousel Styles */
.carousel-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 2.75rem;  /* 44px touch target */
  height: 2.75rem;
  border-radius: 50%;
  background: rgba(30, 41, 59, 0.8);
  border: none;
  color: #e2e8f0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 10;
}

.carousel-nav:hover:not(:disabled) {
  background: rgba(30, 41, 59, 1);
  transform: translateY(-50%) scale(1.1);
}

.carousel-nav:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.carousel-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  padding: 0 3.5rem;
}

.carousel-nav.prev {
  left: 0.5rem;
}

.carousel-nav.next {
  right: 0.5rem;
}

.article-card {
  margin: 0 0.5rem;
}

.carousel-nav svg {
  width: 1.25rem;
  height: 1.25rem;
}

.carousel-pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.pagination-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: rgba(203, 213, 225, 0.4);
  border: none;
  padding: 0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-dot.active {
  background: #3b82f6;
  transform: scale(1.2);
}

/* Scrollbar Styling */
.articles-container::-webkit-scrollbar {
  width: 6px;
}

.articles-container::-webkit-scrollbar-track {
  background: transparent;
}

.articles-container::-webkit-scrollbar-thumb {
  background-color: rgba(203, 213, 225, 0.4);
  border-radius: 3px;
}

/* Share Modal Styles */
.share-modal {
  max-width: 30rem;
}

.share-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.share-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem;
  background: rgba(30, 41, 59, 0.5);
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.share-option:hover {
  background: rgba(30, 41, 59, 0.8);
  transform: translateY(-0.125rem);
}

.share-option svg {
  width: 1.5rem;
  height: 1.5rem;
  color: #3b82f6;
}

.share-preview {
  padding: 1rem;
  background: rgba(30, 41, 59, 0.5);
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  border-radius: 0.75rem;
}

.share-title {
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
}

.share-description {
  font-size: 0.875rem;
  color: #94a3b8;
  margin: 0;
}

/* Light Mode Support */
@media (prefers-color-scheme: light) {
  .news-container {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .title {
    color: #1e293b;
  }

  .source-badge {
    background: rgba(241, 245, 249, 0.8);
    color: #64748b;
  }

  .source-badge.active {
    background: rgba(59, 130, 246, 0.1);
  }

  .action-button {
    background: rgba(241, 245, 249, 0.8);
    color: #64748b;
  }

  .source-toggle {
    background: rgba(248, 250, 252, 0.8);
  }

  .article-card {
    background: rgba(248, 250, 252, 0.8);
  }

  .article-card:hover {
    background: rgba(241, 245, 249, 0.9);
  }

  .article-title {
    color: #1e293b;
  }

  .article-description {
    color: #64748b;
  }
  
  .read-more-btn {
    background: rgba(59, 130, 246, 0.1);
  }
  
  .share-btn {
    background: rgba(226, 232, 240, 0.5);
    color: #64748b;
  }
  
  .share-btn:hover {
    background: rgba(226, 232, 240, 0.8);
    color: #1e293b;
  }
  
  .share-option {
    background: rgba(248, 250, 252, 0.8);
  }
  
  .share-option:hover {
    background: rgba(241, 245, 249, 0.9);
  }
  
  .share-title {
    color: #1e293b;
  }
  
  .share-description {
    color: #64748b;
  }
}

/* Touch Device Optimizations */
@media (hover: none) and (pointer: coarse) {
  .action-button {
    min-height: 44px;
    min-width: 44px;
  }

  .source-btn {
    padding: 1rem;
  }

  .articles-container::-webkit-scrollbar {
    width: 8px;
  }

  .article-card {
    padding: 1.25rem;
  }
  
  .read-more-btn, .share-btn {
    min-height: 2.75rem;
    min-width: 2.75rem;
    padding: 0.75rem 1rem;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .news-dashboard {
    padding: 0.75rem;
  }

  .content-wrapper {
    padding: 0.75rem;
    gap: 1rem;
  }

  .header-row {
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .title-section {
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .title {
    font-size: 1rem;
    text-align: center;
    min-width: max-content;
  }

  .source-toggle {
    flex-shrink: 0;
  }

  .source-btn {
    padding: 0.375rem 0.5rem;
    font-size: 0.8125rem;
  }

  .actions-group {
    flex-shrink: 0;
    margin-left: auto;
  }

  .update-status {
    display: none;
  }
  
  /* Article card adjustments */
  .article-image {
    height: 10rem;
  }
  
  .article-title {
    font-size: 1.125rem;
  }
  
  .article-description {
    font-size: 0.875rem;
    -webkit-line-clamp: 3;
  }
  
  .article-actions {
    flex-direction: column;
    gap: 0.75rem;
    align-items: stretch;
  }
  
  .share-options {
    grid-template-columns: 1fr;
  }

  .carousel-container {
    padding: 0 2.5rem;
  }

  .carousel-nav {
    width: 36px;
    height: 36px;
  }

  .carousel-nav svg {
    width: 16px;
    height: 16px;
  }

  .carousel-nav.prev {
    left: 0.25rem;
  }

  .carousel-nav.next {
    right: 0.25rem;
  }

  .article-card {
    margin: 0 0.25rem;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .title-section {
    gap: 1rem;
  }

  .source-btn {
    padding: 0.375rem 0.5rem;
    font-size: 0.8125rem;
  }
}

/* Settings Modal */
.settings-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(4px);
}

.modal-content {
  position: relative;
  width: 90%;
  max-width: 25rem;
  background: rgba(30, 41, 59, 0.95);
  border-radius: 1rem;
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  box-shadow: 0 1.25rem 1.5625rem -0.3125rem rgba(0, 0, 0, 0.1), 0 0.625rem 0.625rem -0.3125rem rgba(0, 0, 0, 0.04);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(51, 65, 85, 0.5);
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.close-button {
  width: 2.75rem;  /* 44px touch target */
  height: 2.75rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(51, 65, 85, 0.5);
  border: none;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: rgba(71, 85, 105, 0.5);
  color: #e2e8f0;
}

.close-button svg {
  width: 1rem;
  height: 1rem;
}

.modal-body {
  padding: 1.5rem;
}

.settings-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.setting-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.setting-label {
  font-size: 0.875rem;
  color: #e2e8f0;
  white-space: nowrap;
}

.interval-input {
  width: 3.125rem;
  height: 2.75rem;  /* 44px touch target */
  padding: 0 0.5rem;
  font-size: 0.875rem;
  color: #e2e8f0;
  background: rgba(51, 65, 85, 0.5);
  border: 0.0625rem solid rgba(71, 85, 105, 0.5);
  border-radius: 0.375rem;
  outline: none;
  transition: all 0.2s ease;
}

.interval-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}

.interval-input::-webkit-inner-spin-button,
.interval-input::-webkit-outer-spin-button {
  opacity: 1;
  height: 24px;
}

.reset-button {
  width: 2.75rem;  /* 44px touch target */
  height: 2.75rem;
  padding: 0;
  border: none;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-button:hover {
  color: #e2e8f0;
  transform: rotate(45deg);
}

.reset-button svg {
  width: 16px;
  height: 16px;
}

/* Toggle Switch */
.toggle {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 24px;
  transition: all 0.2s ease;
}

.toggle-slider:before {
  content: "";
  position: absolute;
  height: 20px;
  width: 20px;
  left: 2px;
  bottom: 2px;
  background: #94a3b8;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.toggle input:checked + .toggle-slider {
  background: rgba(59, 130, 246, 0.2);
}

.toggle input:checked + .toggle-slider:before {
  transform: translateX(20px);
  background: #3b82f6;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.modal-enter-from .modal-overlay,
.modal-leave-to .modal-overlay {
  opacity: 0;
}

/* Slide Transitions */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease-out;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Focus Accessibility */
.action-button:focus-visible,
.source-btn:focus-visible,
.close-button:focus-visible,
.article-card:focus-visible,
.read-more-btn:focus-visible,
.share-btn:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

/* Light Mode Support for Modal */
@media (prefers-color-scheme: light) {
  .modal-content {
    background: rgba(255, 255, 255, 0.95);
  }

  .modal-title {
    color: #1e293b;
  }

  .setting-label {
    color: #1e293b;
  }

  .interval-input {
    background: white;
    color: #1e293b;
    border-color: rgba(226, 232, 240, 0.8);
  }
}
</style>