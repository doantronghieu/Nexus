<template>
  <div class="music-dashboard">
    <div class="music-container">
      <!-- Content Section -->
      <div class="content-wrapper">
        <!-- Header Row -->
        <div class="header-row">
          <div class="title-section">
            <h2 class="title">Music</h2>
            <div class="status-badge" :class="{ active: userInteracted }">
              <span class="status-dot"></span>
              {{ autoplayStatusText }}
            </div>
          </div>
          <div class="header-actions">
            <button
              @click="togglePlaylistPanel"
              class="action-button"
              :class="{ active: showPlaylists }"
              aria-label="Playlists"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2h2a2 2 0 012 2v6zm0-10a2 2 0 01-2-2V5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H9zm10 10a2 2 0 01-2 2h-2a2 2 0 01-2-2v-6a2 2 0 012-2h2a2 2 0 012 2v6z" />
              </svg>
            </button>
            <button
              @click="showSearch = !showSearch"
              class="action-button"
              :class="{ active: showSearch }"
              aria-label="Toggle search"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Current Track Info -->
        <div class="track-info" :class="{ 'has-track': currentVideoId }">
          <div class="album-artwork" v-if="currentVideoId">
            <div class="artwork-image" :style="albumArtStyle"></div>
            <div class="visualizer" v-if="isPlaying">
              <div class="bar" v-for="n in 12" :key="n"></div>
            </div>
          </div>
          <div class="track-details">
            <div class="current-title">{{ currentTitle || 'No track selected' }}</div>
            <div class="track-artist" v-if="currentArtist">{{ currentArtist }}</div>
            <div class="track-status">
              <div class="status-indicator" :class="{ playing: isPlaying }">
                <span class="status-dot"></span>
                {{ playerStatus }}
              </div>
              <div v-if="currentQuery" class="query-tag">
                {{ currentQuery }}
              </div>
            </div>
          </div>
        </div>

        <!-- Search Section -->
        <transition 
          name="search-slide"
          @enter="initializeSearch"
        >
          <div v-if="showSearch" class="search-section">
            <form @submit.prevent="handleSearch" class="search-form">
              <div class="input-wrapper">
                <input
                  type="text"
                  v-model="searchQuery"
                  ref="searchInput"
                  class="search-input"
                  placeholder="Search for music..."
                  :disabled="isLoading"
                />
                <button
                  type="submit"
                  class="search-button"
                  :disabled="isLoading"
                  aria-label="Search"
                >
                  <div v-if="isLoading" class="loading-dots">
                    <span></span><span></span><span></span>
                  </div>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </button>
              </div>
              <!-- Playlist Selection -->
              <div class="playlist-select-container" v-if="playlists.length > 0">
                <select v-model="selectedPlaylist" class="playlist-select">
                  <option value="">Add to playlist (optional)</option>
                  <option v-for="playlist in playlists" :key="playlist.name" :value="playlist.name">{{ playlist.name }}</option>
                </select>
                <button @click.prevent="openCreatePlaylistModal" type="button" class="playlist-create-button">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  New
                </button>
              </div>
              <div v-else class="playlist-create-container">
                <button @click.prevent="openCreatePlaylistModal" type="button" class="playlist-create-full-button">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Create Playlist
                </button>
              </div>
            </form>
          </div>
        </transition>
        
        <!-- Playlists Panel -->
        <transition name="slide-right">
          <div v-if="showPlaylists" class="playlists-panel">
            <div class="playlists-header">
              <h3 class="playlists-title">Your Playlists</h3>
              <button @click="openCreatePlaylistModal" class="playlist-add-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                New
              </button>
            </div>
            
            <input 
              type="text" 
              v-model="playlistSearch" 
              class="playlist-search" 
              placeholder="Search playlists..."
            />
            
            <div class="playlists-list" v-if="filteredPlaylists.length > 0">
              <div 
                v-for="playlist in filteredPlaylists" 
                :key="playlist.name" 
                class="playlist-item"
                @click="viewPlaylist(playlist)"
              >
                <div class="playlist-grid">
                  <div class="playlist-thumbnail" v-for="(track, index) in playlist.tracks.slice(0, 4)" :key="index">
                    <img :src="track.thumbnail || getFallbackThumbnail()" :alt="track.title">
                  </div>
                  <div v-for="i in Math.max(0, 4 - playlist.tracks.length)" :key="`empty-${i}`" class="playlist-thumbnail empty"></div>
                </div>
                <div class="playlist-info">
                  <div class="playlist-name">{{ playlist.name }}</div>
                  <div class="playlist-count">{{ playlist.tracks.length }} tracks</div>
                </div>
                <div class="playlist-actions">
                  <button @click.stop="playPlaylist(playlist)" class="playlist-play">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="playlists-empty">
              <p v-if="playlistSearch.trim()">No playlists matching "{{ playlistSearch }}"</p>
              <p v-else>No playlists found</p>
              <button @click="openCreatePlaylistModal" class="create-first-button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Create Playlist
              </button>
            </div>
          </div>
        </transition>

        <!-- Status Message -->
        <transition name="fade">
          <div v-if="statusMessage" 
               class="status-message" 
               :class="statusMessageClass"
               role="alert">
            {{ statusMessage }}
          </div>
        </transition>

        <!-- Audio Player Controls -->
        <div v-if="currentVideoId" class="player-controls">
          <!-- Progress Bar -->
          <div class="progress-container">
            <div class="time-display current-time">{{ formatTime(currentTime) }}</div>
            <div class="progress-bar">
              <div class="progress-background"></div>
              <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
              <input 
                type="range" 
                min="0" 
                :max="duration" 
                step="0.1" 
                v-model="currentTime"
                @input="seekAudio"
                class="progress-input"
              >
            </div>
            <div class="time-display duration">{{ formatTime(duration) }}</div>
          </div>
          
          <!-- Control Buttons -->
          <div class="controls-row">
            <button class="control-button" @click="handlePrevious" aria-label="Previous track">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M19 20L9 12l10-8v16z"></path>
                <line x1="5" y1="19" x2="5" y2="5"></line>
              </svg>
            </button>
            
            <button class="control-button play-button" @click="togglePlay(true)" aria-label="Play or pause">
              <svg v-if="isPlaying" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="6" y="4" width="4" height="16"></rect>
                <rect x="14" y="4" width="4" height="16"></rect>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
            </button>
            
            <button class="control-button" @click="handleNext" aria-label="Next track">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M5 4l10 8-10 8V4z"></path>
                <line x1="19" y1="5" x2="19" y2="19"></line>
              </svg>
            </button>
          </div>
          
          <!-- Volume Control -->
          <div class="volume-container">
            <button class="volume-button" @click="toggleMute" aria-label="Toggle mute">
              <svg v-if="isMuted" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M11 5L6 9H2v6h4l5 4V5z"></path>
                <line x1="23" y1="9" x2="17" y2="15"></line>
                <line x1="17" y1="9" x2="23" y2="15"></line>
              </svg>
              <svg v-else-if="volume > 0.5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M11 5L6 9H2v6h4l5 4V5z"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M11 5L6 9H2v6h4l5 4V5z"></path>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
              </svg>
            </button>
            <div class="volume-slider">
              <div class="volume-fill" :style="{ width: (volume * 100) + '%' }"></div>
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.01" 
                v-model="volume"
                @input="changeVolume"
                class="volume-input"
              >
            </div>
          </div>
          
          <!-- Hidden audio element -->
          <audio
            ref="audioPlayer"
            @canplay="onCanPlay"
            @timeupdate="updateTime"
            @playing="onPlaying"
            @pause="onPause"
            @ended="onEnded"
            @error="onError"
          ></audio>
        </div>
      </div>
    </div>

    <!-- Create Playlist Modal -->
    <div v-if="showCreatePlaylistModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3 class="modal-title">Create New Playlist</h3>
          <button @click="closeCreatePlaylistModal" class="modal-close-button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="input-group">
            <label for="playlistName" class="input-label">Playlist Name</label>
            <input type="text" id="playlistName" v-model="newPlaylistName" class="modal-input" placeholder="My Playlist" />
          </div>
          <div class="input-group">
            <label for="playlistDescription" class="input-label">Description (optional)</label>
            <textarea id="playlistDescription" v-model="newPlaylistDescription" class="modal-textarea" placeholder="Add a description..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeCreatePlaylistModal" class="modal-cancel-button">Cancel</button>
          <button @click="createPlaylist" class="modal-confirm-button">Create Playlist</button>
        </div>
      </div>
    </div>
    
    <!-- Playlist View Modal -->
    <div v-if="showPlaylistViewModal && currentPlaylist" class="modal-overlay">
      <div class="modal-container playlist-view-modal">
        <div class="modal-header">
          <div class="playlist-view-header">
            <h3 class="modal-title">{{ currentPlaylist.name }}</h3>
            <p class="playlist-description">{{ currentPlaylist.description || 'No description' }}</p>
            <p class="playlist-track-count">{{ currentPlaylist.tracks.length }} tracks</p>
          </div>
          <button @click="closeViewPlaylistModal" class="modal-close-button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="modal-body playlist-tracks">
          <div v-if="currentPlaylist.tracks.length === 0" class="playlist-empty-message">
            <p>This playlist is empty</p>
          </div>
          <div v-else class="track-list">
            <div v-for="(track, index) in currentPlaylist.tracks" :key="track.id" class="track-item">
              <div class="track-number">{{ index + 1 }}</div>
              <div class="track-thumbnail">
                <img :src="track.thumbnail || getFallbackThumbnail()" :alt="track.title">
              </div>
              <div class="track-details">
                <div class="track-title">{{ track.title }}</div>
                <div class="track-metadata">{{ track.duration || '0:00' }}</div>
              </div>
              <div class="track-actions">
                <button @click="playFromPlaylist(track, true)" class="track-play-button">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  </svg>
                </button>
                <button @click="removeTrackFromPlaylist(currentPlaylist.name, track.id)" class="track-remove-button">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="deletePlaylist" class="playlist-delete-button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete Playlist
          </button>
          <button @click="clearPlaylist" class="playlist-clear-button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Clear Playlist
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import services from '@/configs/services_info.json'

// State management
const userInteracted = ref(true)
const showSearch = ref(false)
const showPlaylists = ref(false)
const currentVideoId = ref(null)
const currentQuery = ref(null)
const currentTitle = ref(null)
const currentArtist = ref("")
const isPlaying = ref(false)
const isLoading = ref(false)
const searchQuery = ref('')
const statusMessage = ref('')
const statusType = ref('info')
const playerStatus = ref('')
const retryCount = ref(0)
const maxRetries = 3
const audioContext = ref(null)
const searchInput = ref(null)
const audioPlayer = ref(null)
const playingStatus = ref(true) // Track Redis playing status
const continuePlayCommand = ref(false) // Track continue play command

// Initialize playlist state
const playlists = ref([])
const playlistSearch = ref('')
const selectedPlaylist = ref('')
const currentPlaylist = ref(null)
const showCreatePlaylistModal = ref(false)
const showPlaylistViewModal = ref(false)
const newPlaylistName = ref('')
const newPlaylistDescription = ref('')

// Audio player state
const duration = ref(0)
const currentTime = ref(0)
const volume = ref(0.7)
const isMuted = ref(false)
const prevVolume = ref(0.7)

// Album art fallbacks
const albumImages = [
  'https://placehold.co/400x400/3b82f6/ffffff?text=Music',
  'https://placehold.co/400x400/6366f1/ffffff?text=Music',
  'https://placehold.co/400x400/8b5cf6/ffffff?text=Music',
  'https://placehold.co/400x400/ec4899/ffffff?text=Music',
  'https://placehold.co/400x400/f43f5e/ffffff?text=Music',
]

// Computed values for player
const progressPercentage = computed(() => {
  if (duration.value === 0) return 0
  return (currentTime.value / duration.value) * 100
})

// Random album art
const randomAlbumArt = computed(() => {
  // Get a consistent image based on the title
  if (!currentTitle.value) return albumImages[0]
  const hash = currentTitle.value.split('').reduce((acc, char) => {
    return acc + char.charCodeAt(0)
  }, 0)
  return albumImages[hash % albumImages.length]
})

const albumArtStyle = computed(() => {
  return {
    backgroundImage: `url(${randomAlbumArt.value})`
  }
})

// Computed playlist values
const filteredPlaylists = computed(() => {
  if (!playlistSearch.value.trim()) return playlists.value
  
  const searchTerm = playlistSearch.value.toLowerCase()
  return playlists.value.filter(p => 
    p.name.toLowerCase().includes(searchTerm) || 
    (p.description && p.description.toLowerCase().includes(searchTerm))
  )
})

// Server configuration
const API_BASE_URL = services['svc-music'].url

// Handlers
const keyboardHandler = ref(null)
const checkInterval = ref(null)

// API Methods
const apiRequest = async (endpoint) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Accept': 'application/json',
    },
    mode: 'cors'
  })
  return response
}

// Check playing status from Redis
const checkPlayingStatus = async () => {
  try {
    const response = await apiRequest('/playing-status')
    if (!response.ok) {
      console.warn('Playing status endpoint not found, defaulting to false')
      return { playing: false, continuePlay: false } // Default to false if endpoint not found
    }
    
    const data = await response.json()
    return { 
      playing: data.playing === true,
      continuePlay: data.continuePlay === true
    }
  } catch (error) {
    console.error('Error checking playing status:', error)
    return { playing: false, continuePlay: false } // Default to false on error
  }
}

// Extract artist from title
const extractArtistFromTitle = (title) => {
  if (!title) return ""
  
  // Common patterns: "Artist - Title" or "Artist : Title"
  const separators = [' - ', ' : ', ' – ', ': ', ' | ']
  
  for (const separator of separators) {
    if (title.includes(separator)) {
      return title.split(separator)[0].trim()
    }
  }
  
  return ""
}

// MODIFIED: Check for current video and playing status
const checkCurrentVideo = async () => {
  if (!userInteracted.value) return

  try {
    // First check if we should be playing
    const statusData = await checkPlayingStatus()
    const shouldBePlaying = statusData.playing
    const shouldContinuePlay = statusData.continuePlay
    
    // Update states
    playingStatus.value = shouldBePlaying
    continuePlayCommand.value = shouldContinuePlay
    
    // Handle continue play command
    if (shouldContinuePlay) {
      if (currentVideoId.value && !isPlaying.value) {
        // We have a video that's paused, resume it
        const player = audioPlayer.value
        if (player) {
          await player.play()
          isPlaying.value = true
          playerStatus.value = 'Playing'
          showStatus('Playback resumed by voice command', 'success')
        }
      }
      
      // Reset the continue play command (this should be done by the backend, but we can also handle it here)
      try {
        await fetch(`${API_BASE_URL}/reset-continue-play`, { method: 'POST' })
      } catch (err) {
        console.warn('Failed to reset continue play command:', err)
      }
    }
    
    // If not playing but audio is playing, pause it
    if (!shouldBePlaying && isPlaying.value && audioPlayer.value && !shouldContinuePlay) {
      audioPlayer.value.pause()
      isPlaying.value = false
      playerStatus.value = 'Stopped by voice command'
      showStatus('Playback stopped by voice command', 'info')
      return
    }
    
    // Original code for checking current video
    const response = await apiRequest('/current-video')
    if (!response.ok) {
      if (response.status === 404) return // Expected when no video is playing
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    if (data.video_id && data.video_id !== currentVideoId.value) {
      currentVideoId.value = data.video_id
      currentQuery.value = data.query
      retryCount.value = 0
      await getVideoInfo(data.video_id, data.query)
      
      // Only play if we should be playing
      if (shouldBePlaying || shouldContinuePlay) {
        await playCurrentVideo(shouldContinuePlay) // Pass flag to force play
      }
    }
  } catch (error) {
    console.error('Error checking current video:', error)
    if (!error.message.includes('404')) {
      showStatus('Failed to check current video status.', 'error')
    }
  }
}

// Get video information
const getVideoInfo = async (videoId, query) => {
  try {
    const response = await apiRequest(`/search?query=${encodeURIComponent(query)}&mode=llm`)
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    
    const data = await response.json()
    const videoInfo = data.results.find(r => r.id === videoId)
    if (videoInfo) {
      currentTitle.value = videoInfo.title
      currentArtist.value = extractArtistFromTitle(videoInfo.title)
    }
  } catch (error) {
    console.error('Error getting video title:', error)
    showStatus('Failed to get video information.', 'error')
  }
}

// Start listening and initialize polling
const startListening = async () => {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext
    audioContext.value = new AudioContext()
    userInteracted.value = true
    showStatus('Auto-play enabled. Ready to play music!', 'success')
    checkInterval.value = setInterval(checkCurrentVideo, 3000)
    await checkCurrentVideo()
  } catch (error) {
    console.error('Error initializing audio:', error)
    showStatus('Failed to initialize audio. Please try again.', 'error')
  }
}

// Computed values
const autoplayStatusText = computed(() => {
  return userInteracted.value ? 'Auto-play enabled' : 'Auto-play disabled'
})

const statusMessageClass = computed(() => ({
  'error': statusType.value === 'error',
  'success': statusType.value === 'success',
  'info': statusType.value === 'info'
}))

// Format time for display (mm:ss)
const formatTime = (seconds) => {
  if (isNaN(seconds) || seconds === Infinity) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// Methods
const showStatus = (message, type = 'info') => {
  statusMessage.value = message
  statusType.value = type
  
  if (type !== 'error') {
    setTimeout(() => {
      statusMessage.value = ''
    }, 5000)
  }
}

// Handle search
const handleSearch = async (e) => {
  e?.preventDefault()
  
  if (!searchQuery.value) {
    showStatus('Please enter a search query', 'error')
    return
  }

  try {
    isLoading.value = true
    statusMessage.value = ''
    
    let url = `${API_BASE_URL}/search?query=${encodeURIComponent(searchQuery.value)}&mode=llm`
    
    // Add to playlist if selected
    if (selectedPlaylist.value) {
      url += `&playlist=${encodeURIComponent(selectedPlaylist.value)}`
    }
    
    const response = await fetch(url)
    if (!response.ok) throw new Error('Search failed')
    
    const data = await response.json()
    
    if (data.results.length === 0) {
      showStatus('No results found', 'info')
      return
    }

    if (data.most_viewed_id) {
      const mostViewed = data.results.find(r => r.id === data.most_viewed_id)
      if (mostViewed) {
        currentTitle.value = mostViewed.title
        currentArtist.value = extractArtistFromTitle(mostViewed.title)
        currentVideoId.value = mostViewed.id
        
        // Only start playing if playingStatus is true or user explicitly requested
        const forcePlay = !selectedPlaylist.value // Force play only if not adding to playlist
        await playCurrentVideo(forcePlay)
      }
    }
    
    // Show different message if adding to playlist
    if (selectedPlaylist.value) {
      showStatus(`Added to playlist "${selectedPlaylist.value}"`, 'success')
      // Refresh playlists after adding
      await loadPlaylists()
    } else {
      showStatus('Playing the most viewed result...', 'success')
    }
  } catch (error) {
    console.error('Error:', error)
    showStatus('Failed to search. Please try again.', 'error')
  } finally {
    isLoading.value = false
  }
}

// MODIFIED: Add forcePlay parameter to override playingStatus
const playCurrentVideo = async (forcePlay = false) => {
  if (!currentVideoId.value || !userInteracted.value) return
  
  // Don't play if playing status is false and not forcing play
  if (!playingStatus.value && !forcePlay) {
    playerStatus.value = 'Stopped (by voice command)'
    return
  }
  
  try {
    playerStatus.value = 'Loading audio...'
    const player = audioPlayer.value
    player.src = `${API_BASE_URL}/play/${currentVideoId.value}`
    
    await new Promise((resolve, reject) => {
      player.oncanplay = resolve
      player.onerror = reject
      setTimeout(() => reject(new Error('Loading timeout')), 10000)
    })
    
    await player.play()
    isPlaying.value = true
    retryCount.value = 0
    
    // If this was a manual override, show appropriate message
    if (forcePlay && !playingStatus.value) {
      showStatus('Manually resumed playback', 'success')
    }
  } catch (error) {
    console.error('Error playing video:', error)
    retryCount.value++
    
    if (retryCount.value < maxRetries) {
      showStatus(`Retrying... (${retryCount.value}/${maxRetries})`, 'info')
      setTimeout(() => playCurrentVideo(forcePlay), 3000)
    } else {
      showStatus('Failed to play audio after multiple attempts.', 'error')
      retryCount.value = 0
    }
  }
}

// MODIFIED: Toggle play/pause with option to force play (manual override)
const togglePlay = (manualOverride = false) => {
  const player = audioPlayer.value
  if (!player) return
  
  if (isPlaying.value) {
    player.pause()
  } else {
    // If manual override, play regardless of playingStatus
    if (manualOverride) {
      player.play().catch(error => {
        console.error('Error playing audio:', error)
        showStatus('Failed to play audio', 'error')
      })
      
      // Only show message if overriding playingStatus
      if (!playingStatus.value) {
        showStatus('Manually resumed playback', 'success')
      }
    } 
    // Otherwise, only play if playing status is true
    else if (playingStatus.value) {
      player.play().catch(error => {
        console.error('Error playing audio:', error)
        showStatus('Failed to play audio', 'error')
      })
    } else {
      showStatus('Playback is currently stopped by voice command. Click play again to override.', 'info')
    }
  }
}

// Seek to position
const seekAudio = () => {
  const player = audioPlayer.value
  if (!player) return
  
  player.currentTime = currentTime.value
}

// Update current time during playback
const updateTime = () => {
  const player = audioPlayer.value
  if (!player) return
  
  currentTime.value = player.currentTime
  duration.value = player.duration || 0
}

// Handle volume change
const changeVolume = () => {
  const player = audioPlayer.value
  if (!player) return
  
  player.volume = volume.value
  if (volume.value > 0) {
    isMuted.value = false
  }
}

// Toggle mute
const toggleMute = () => {
  const player = audioPlayer.value
  if (!player) return
  
  if (isMuted.value) {
    volume.value = prevVolume.value
    player.volume = volume.value
    isMuted.value = false
  } else {
    prevVolume.value = volume.value
    volume.value = 0
    player.volume = 0
    isMuted.value = true
  }
}

// Handle previous track (with playlist support)
const handlePrevious = () => {
  // If time is > 3 seconds, just restart the current track
  const player = audioPlayer.value
  if (!player) return
  
  if (player.currentTime > 3) {
    player.currentTime = 0
    return
  }
  
  // If we're in a playlist, go to the previous track
  if (currentPlaylist.value && currentPlaylist.value.tracks.length > 0) {
    const currentIndex = currentPlaylist.value.tracks.findIndex(t => t.id === currentVideoId.value)
    if (currentIndex > 0) {
      const prevTrack = currentPlaylist.value.tracks[currentIndex - 1]
      currentVideoId.value = prevTrack.id
      currentTitle.value = prevTrack.title
      currentArtist.value = extractArtistFromTitle(prevTrack.title)
      playCurrentVideo(true) // Force play
      return
    }
  }
  
  // If at the start of playlist or no playlist, just restart
  player.currentTime = 0
}

// Handle next track (with playlist support)
const handleNext = () => {
  // If we're in a playlist, go to the next track
  if (currentPlaylist.value && currentPlaylist.value.tracks.length > 0) {
    const currentIndex = currentPlaylist.value.tracks.findIndex(t => t.id === currentVideoId.value)
    if (currentIndex !== -1 && currentIndex < currentPlaylist.value.tracks.length - 1) {
      const nextTrack = currentPlaylist.value.tracks[currentIndex + 1]
      currentVideoId.value = nextTrack.id
      currentTitle.value = nextTrack.title
      currentArtist.value = extractArtistFromTitle(nextTrack.title)
      playCurrentVideo(true) // Force play
      return
    }
  }
  
  // If no playlist or at the end
  showStatus('No next track available', 'info')
}

// MODIFIED: Add manualOverride parameter
const playFromPlaylist = (track, manualOverride = false) => {
  currentVideoId.value = track.id
  currentTitle.value = track.title
  currentArtist.value = extractArtistFromTitle(track.title)
  
  // Play respecting the override
  playCurrentVideo(manualOverride)
  
  if (!playingStatus.value && !manualOverride) {
    showStatus('Track is queued but not playing due to voice command. Press play to override.', 'info')
  }
}

const handleKeydown = (e) => {
  // Only handle space key if it's not from an input element
  if (e.code === 'Space' && 
      e.target.tagName !== 'INPUT' && 
      e.target.tagName !== 'TEXTAREA') {
    e.preventDefault();
    togglePlay(true); // Treat keyboard as manual override
  }
};

// Init search
const initializeSearch = () => {
  if (searchInput.value) {
    setTimeout(() => {
      searchInput.value.focus()
    }, 100)
  }
}

// Player event handlers
const onCanPlay = () => {
  playerStatus.value = 'Ready to play'
  duration.value = audioPlayer.value.duration || 0
}

const onPlaying = () => {
  isPlaying.value = true
  playerStatus.value = 'Playing'
}

const onPause = () => {
  isPlaying.value = false
  playerStatus.value = 'Paused'
}

const onEnded = () => {
  isPlaying.value = false
  playerStatus.value = 'Ended'
  // Could handle auto-advancing to next track here
  handleNext()
}

const onError = () => {
  isPlaying.value = false
  playerStatus.value = 'Error playing audio'
  if (retryCount.value < maxRetries) {
    setTimeout(() => playCurrentVideo(), 3000)
  }
}

// Playlist Management Methods
const togglePlaylistPanel = () => {
  showPlaylists.value = !showPlaylists.value
  if (showPlaylists.value) {
    loadPlaylists()
  }
}

const loadPlaylists = async (refreshUI = false) => {
  try {
    const response = await fetch(`${API_BASE_URL}/playlists`)
    if (!response.ok) throw new Error('Failed to load playlists')
    
    const data = await response.json()
    playlists.value = data.playlists || []
  } catch (error) {
    console.error('Error loading playlists:', error)
    showStatus('Failed to load playlists', 'error')
  }
}

const openCreatePlaylistModal = () => {
  newPlaylistName.value = ''
  newPlaylistDescription.value = ''
  showCreatePlaylistModal.value = true
}

const closeCreatePlaylistModal = () => {
  showCreatePlaylistModal.value = false
}

const getFallbackThumbnail = () => {
  return albumImages[Math.floor(Math.random() * albumImages.length)]
}

const createPlaylist = async () => {
  if (!newPlaylistName.value.trim()) {
    showStatus('Please enter a playlist name', 'error')
    return
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/playlists`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newPlaylistName.value.trim(),
        description: newPlaylistDescription.value.trim()
      })
    })
    
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create playlist')
    }
    
    showStatus(`Playlist "${newPlaylistName.value}" created successfully`, 'success')
    showCreatePlaylistModal.value = false
    await loadPlaylists()
  } catch (error) {
    console.error('Error creating playlist:', error)
    showStatus(error.message || 'Failed to create playlist', 'error')
  }
}

const viewPlaylist = (playlist) => {
  currentPlaylist.value = playlist
  showPlaylistViewModal.value = true
}

const closeViewPlaylistModal = () => {
  showPlaylistViewModal.value = false
}

const playPlaylist = async (playlist) => {
  if (!playlist || playlist.tracks.length === 0) {
    showStatus(`Playlist "${playlist.name}" is empty`, 'error')
    return
  }
  
  currentPlaylist.value = playlist
  const firstTrack = playlist.tracks[0]
  currentVideoId.value = firstTrack.id
  currentTitle.value = firstTrack.title
  currentArtist.value = extractArtistFromTitle(firstTrack.title)
  
  // Play with manual override
  await playCurrentVideo(true)
  showStatus(`Playing playlist: ${playlist.name}`, 'success')
}

const deletePlaylist = async () => {
  if (!currentPlaylist.value) return
  
  try {
    const response = await fetch(`${API_BASE_URL}/playlists/${encodeURIComponent(currentPlaylist.value.name)}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) throw new Error('Failed to delete playlist')
    
    showStatus(`Playlist "${currentPlaylist.value.name}" deleted successfully`, 'success')
    showPlaylistViewModal.value = false
    await loadPlaylists()
  } catch (error) {
    console.error('Error deleting playlist:', error)
    showStatus('Failed to delete playlist', 'error')
  }
}

const clearPlaylist = async () => {
  if (!currentPlaylist.value) return
  
  try {
    const response = await fetch(`${API_BASE_URL}/playlist-action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'clear',
        playlist_name: currentPlaylist.value.name
      })
    })
    
    if (!response.ok) throw new Error('Failed to clear playlist')
    
    showStatus(`Playlist "${currentPlaylist.value.name}" cleared successfully`, 'success')
    currentPlaylist.value.tracks = []
    await loadPlaylists()
  } catch (error) {
    console.error('Error clearing playlist:', error)
    showStatus('Failed to clear playlist', 'error')
  }
}

const removeTrackFromPlaylist = async (playlistName, trackId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/playlist-action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'remove',
        playlist_name: playlistName,
        track_id: trackId
      })
    })
    
    if (!response.ok) throw new Error('Failed to remove track from playlist')
    
    showStatus('Track removed from playlist', 'success')
    
    // Update current playlist if open
    if (currentPlaylist.value && currentPlaylist.value.name === playlistName) {
      currentPlaylist.value.tracks = currentPlaylist.value.tracks.filter(t => t.id !== trackId)
    }
    
    await loadPlaylists()
  } catch (error) {
    console.error('Error removing track from playlist:', error)
    showStatus('Failed to remove track from playlist', 'error')
  }
}

const addCurrentTrackToPlaylist = async (playlistName) => {
  if (!currentVideoId.value || !currentTitle.value) {
    showStatus('No track is currently playing', 'error')
    return
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/playlist-action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'add',
        playlist_name: playlistName,
        track_info: {
          id: currentVideoId.value,
          title: currentTitle.value,
          thumbnail: randomAlbumArt.value,
          duration: formatTime(duration.value),
          view_count: 0 // We don't have this info, so using 0
        }
      })
    })
    
    if (!response.ok) throw new Error('Failed to add track to playlist')
    
    showStatus(`Track added to "${playlistName}" successfully`, 'success')
    await loadPlaylists()
  } catch (error) {
    console.error('Error adding track to playlist:', error)
    showStatus('Failed to add track to playlist', 'error')
  }
}

// Watch for changes in playing status
watch(playingStatus, (newStatus, oldStatus) => {
  if (oldStatus && !newStatus && isPlaying.value && audioPlayer.value) {
    // If status changed from true to false while playing, stop playback
    audioPlayer.value.pause()
    isPlaying.value = false
    playerStatus.value = 'Stopped by voice command'
    showStatus('Playback stopped by voice command', 'info')
  }
})

// Watch for continue play command
watch(continuePlayCommand, (newValue, oldValue) => {
  if (newValue && !oldValue) {
    // If continue play command is received
    if (currentVideoId.value && !isPlaying.value) {
      const player = audioPlayer.value
      if (player) {
        player.play()
          .then(() => {
            isPlaying.value = true
            playerStatus.value = 'Playing'
            showStatus('Playback resumed by voice command', 'success')
          })
          .catch(err => {
            console.error('Error resuming playback:', err)
            showStatus('Failed to resume playback', 'error')
          })
      }
    }
  }
})

onMounted(() => {
  // Start listening automatically
  startListening()
  
  // Load playlists
  loadPlaylists()
  
  document.addEventListener('keydown', handleKeydown);
})

onUnmounted(() => {
  // Clean up event listeners
  document.removeEventListener('keydown', handleKeydown);

  // Clear polling interval
  if (checkInterval.value) {
    clearInterval(checkInterval.value)
  }
  
  // Clean up audio context
  if (audioContext.value) {
    audioContext.value.close()
  }
})
</script>

<style scoped>
.music-dashboard {
  height: 100%;
  padding: 1.5rem;
}

.music-container {
  height: 100%;
  background: rgba(15, 23, 42, 0.95);
  border-radius: 1.5rem;
  box-shadow: 
    0 0.5rem 2rem rgba(0, 0, 0, 0.05),
    0 0.125rem 0.5rem rgba(0, 0, 0, 0.05);
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
}

.title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
  letter-spacing: 0.01em;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  background: rgba(51, 65, 85, 0.5);
  color: #94a3b8;
  transition: all 0.3s ease;
}

.status-badge.active {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.status-dot {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background: currentColor;
}

/* Header Actions */
.header-actions {
  display: flex;
  gap: 0.75rem;
}

.action-button {
  width: 2.5rem;
  height: 2.5rem;
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

.action-button:hover {
  background: rgba(71, 85, 105, 0.5);
  transform: translateY(-0.0625rem);
}

.action-button.active {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.action-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

/* Track Info with Album Art */
.track-info {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  transition: all 0.3s ease;
  align-items: center;
}

.track-info.has-track {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.2);
}

.album-artwork {
  position: relative;
  width: 5rem;
  height: 5rem;
  border-radius: 0.75rem;
  overflow: hidden;
  flex-shrink: 0;
}

.artwork-image {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: all 0.3s ease;
}

.visualizer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2rem;
  display: flex;
  justify-content: space-evenly;
  align-items: flex-end;
  padding: 0 0.25rem;
  background: linear-gradient(transparent, rgba(15, 23, 42, 0.5));
}

.visualizer .bar {
  width: 0.2rem;
  background: #3b82f6;
  border-radius: 0.125rem 0.125rem 0 0;
  animation: sound 1.3s ease-in-out infinite;
}

.visualizer .bar:nth-child(2n) {
  animation-delay: 0.2s;
}

.visualizer .bar:nth-child(3n) {
  animation-delay: 0.4s;
}

.visualizer .bar:nth-child(4n) {
  animation-delay: 0.6s;
}

.track-details {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.current-title {
  font-size: 1rem;
  font-weight: 500;
  color: #e2e8f0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.track-artist {
  font-size: 0.875rem;
  color: #94a3b8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.track-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #94a3b8;
}

.status-indicator.playing {
  color: #4ade80;
}

.query-tag {
  font-size: 0.875rem;
  color: #94a3b8;
  padding: 0.25rem 0.75rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 9999px;
  max-width: 12.5rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Search Section */
.search-section {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 1rem;
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
}

.search-form {
  width: 100%;
}

.input-wrapper {
  position: relative;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  border-radius: 0.75rem;
  background: rgba(30, 41, 59, 0.8);
  font-size: 0.95rem;
  color: #e2e8f0;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.1875rem rgba(59, 130, 246, 0.1);
}

.search-button {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #94a3b8;
  padding: 0.5rem;
  cursor: pointer;
  transition: color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-button:hover:not(:disabled) {
  color: #3b82f6;
}

.search-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

/* Playlist Selection */
.playlist-select-container {
  display: flex;
  margin-top: 0.75rem;
  gap: 0.75rem;
}

.playlist-select {
  flex: 1;
  background: rgba(30, 41, 59, 0.6);
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  border-radius: 0.5rem;
  color: #e2e8f0;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1rem;
  padding-right: 2.5rem;
}

.playlist-create-button {
  background: rgba(37, 99, 235, 0.2);
  color: #60a5fa;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.2s ease;
}

.playlist-create-button svg {
  width: 0.875rem;
  height: 0.875rem;
}

.playlist-create-button:hover {
  background: rgba(37, 99, 235, 0.3);
}

.playlist-create-container {
  margin-top: 0.75rem;
}

.playlist-create-full-button {
  width: 100%;
  background: rgba(37, 99, 235, 0.2);
  color: #60a5fa;
  border: none;
  border-radius: 0.5rem;
  padding: 0.625rem;
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  transition: all 0.2s ease;
}

.playlist-create-full-button svg {
  width: 1rem;
  height: 1rem;
}

.playlist-create-full-button:hover {
  background: rgba(37, 99, 235, 0.3);
}

/* Playlists Panel */
.playlists-panel {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 1rem;
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.playlists-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.playlists-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.playlist-add-button {
  background: rgba(37, 99, 235, 0.2);
  color: #60a5fa;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.2s ease;
}

.playlist-add-button svg {
  width: 0.875rem;
  height: 0.875rem;
}

.playlist-add-button:hover {
  background: rgba(37, 99, 235, 0.3);
}

.playlist-search {
  background: rgba(30, 41, 59, 0.8);
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  border-radius: 0.5rem;
  color: #e2e8f0;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  width: 100%;
  transition: all 0.2s ease;
}

.playlist-search:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.1875rem rgba(59, 130, 246, 0.1);
}

.playlists-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
  max-height: 16rem;
  scrollbar-width: thin;
  scrollbar-color: #334155 transparent;
}

.playlists-list::-webkit-scrollbar {
  width: 0.25rem;
}

.playlists-list::-webkit-scrollbar-track {
  background: transparent;
}

.playlists-list::-webkit-scrollbar-thumb {
  background-color: #334155;
  border-radius: 0.125rem;
}

.playlist-item {
  background: rgba(30, 41, 59, 0.7);
  border-radius: 0.75rem;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.playlist-item:hover {
  background: rgba(30, 41, 59, 0.9);
  transform: translateY(-0.125rem);
}

.playlist-grid {
  width: 3.5rem;
  height: 3.5rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 0.125rem;
  border-radius: 0.5rem;
  overflow: hidden;
  flex-shrink: 0;
}

.playlist-thumbnail {
  background: #1e293b;
  overflow: hidden;
  position: relative;
}

.playlist-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.playlist-thumbnail.empty {
  background: rgba(30, 41, 59, 0.7);
}

.playlist-info {
  flex: 1;
  min-width: 0;
}

.playlist-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.playlist-count {
  font-size: 0.75rem;
  color: #94a3b8;
}

.playlist-actions {
  display: flex;
  align-items: center;
  justify-content: center;
}

.playlist-play {
  background: transparent;
  border: none;
  color: #94a3b8;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
}

.playlist-play svg {
  width: 1.25rem;
  height: 1.25rem;
}

.playlist-play:hover {
  color: #60a5fa;
}

.playlists-empty {
  text-align: center;
  padding: 1rem 0;
}

.playlists-empty p {
  margin: 0 0 1rem;
  color: #94a3b8;
}

.create-first-button {
  background: rgba(37, 99, 235, 0.2);
  color: #60a5fa;
  border: none;
  border-radius: 0.5rem;
  padding: 0.625rem 1rem;
  font-size: 0.875rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  transition: all 0.2s ease;
}

.create-first-button svg {
  width: 1rem;
  height: 1rem;
}

.create-first-button:hover {
  background: rgba(37, 99, 235, 0.3);
}

/* Enhanced Player Controls */
.player-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: auto;
  padding-top: 1rem;
}

/* Progress Bar */
.progress-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.time-display {
  font-size: 0.75rem;
  color: #94a3b8;
  min-width: 2.5rem;
  text-align: center;
}

.progress-bar {
  flex: 1;
  height: 0.375rem;
  position: relative;
  border-radius: 0.1875rem;
  overflow: hidden;
}

.progress-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 0.1875rem;
}

.progress-fill {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  background: #3b82f6;
  border-radius: 0.1875rem;
  transition: width 0.1s ease;
}

.progress-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  margin: 0;
}

/* Control Buttons */
.controls-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.control-button {
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
}

.control-button svg {
  width: 1.5rem;
  height: 1.5rem;
}

.control-button:hover {
  color: #e2e8f0;
  transform: scale(1.05);
}

.play-button {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.play-button:hover {
  background: rgba(59, 130, 246, 0.3);
}

.play-button svg {
  width: 1.75rem;
  height: 1.75rem;
}

/* Volume Control */
.volume-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.volume-button {
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0.25rem;
}

.volume-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

.volume-button:hover {
  color: #e2e8f0;
}

.volume-slider {
  flex: 1;
  height: 0.25rem;
  background: rgba(51, 65, 85, 0.5);
  border-radius: 0.125rem;
  position: relative;
  overflow: hidden;
}

.volume-fill {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  background: #3b82f6;
  border-radius: 0.125rem;
}

.volume-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  margin: 0;
}

/* Loading Animation */
.loading-dots {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.loading-dots span {
  width: 0.25rem;
  height: 0.25rem;
  border-radius: 50%;
  background: currentColor;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

/* Status Message */
.status-message {
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  animation: slideIn 0.3s ease;
}

.status-message.error {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  border: 0.0625rem solid rgba(239, 68, 68, 0.2);
}

.status-message.success {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
  border: 0.0625rem solid rgba(34, 197, 94, 0.2);
}

.status-message.info {
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
  border: 0.0625rem solid rgba(59, 130, 246, 0.2);
}

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.modal-container {
  background: rgba(30, 41, 59, 0.95);
  border-radius: 1rem;
  width: 100%;
  max-width: 28rem;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 0.625rem 1.5rem rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.playlist-view-modal {
  max-width: 36rem;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 0.0625rem solid rgba(51, 65, 85, 0.5);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #e2e8f0;
  margin: 0;
}

.modal-close-button {
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.2s ease;
  display: flex;
}

.modal-close-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

.modal-close-button:hover {
  color: #e2e8f0;
}

.modal-body {
  padding: 1.5rem;
  flex: 1;
  overflow-y: auto;
}

.input-group {
  margin-bottom: 1.25rem;
}

.input-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.modal-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  border-radius: 0.5rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.modal-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.1875rem rgba(59, 130, 246, 0.1);
}

.modal-textarea {
  width: 100%;
  min-height: 6rem;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 0.0625rem solid rgba(51, 65, 85, 0.5);
  border-radius: 0.5rem;
  color: #e2e8f0;
  font-size: 0.95rem;
  resize: vertical;
  transition: all 0.2s ease;
}

.modal-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 0.1875rem rgba(59, 130, 246, 0.1);
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 0.0625rem solid rgba(51, 65, 85, 0.5);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.modal-cancel-button {
  padding: 0.5rem 1rem;
  background: rgba(51, 65, 85, 0.5);
  color: #e2e8f0;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-cancel-button:hover {
  background: rgba(71, 85, 105, 0.5);
}

.modal-confirm-button {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.modal-confirm-button:hover {
  background: #2563eb;
}

/* Playlist View Styles */
.playlist-view-header {
  display: flex;
  flex-direction: column;
}

.playlist-description {
  font-size: 0.875rem;
  color: #94a3b8;
  margin: 0.25rem 0 0;
}

.playlist-track-count {
  font-size: 0.875rem;
  font-weight: 500;
  color: #60a5fa;
  margin: 0.5rem 0 0;
}

.playlist-tracks {
  max-height: 24rem;
  overflow-y: auto;
}

.playlist-empty-message {
  padding: 2rem 0;
  text-align: center;
  color: #94a3b8;
}

.track-list {
  display: flex;
  flex-direction: column;
}

.track-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 0.0625rem solid rgba(51, 65, 85, 0.5);
}

.track-item:last-child {
  border-bottom: none;
}

.track-number {
  width: 1.5rem;
  text-align: center;
  font-size: 0.875rem;
  color: #94a3b8;
}

.track-thumbnail {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.25rem;
  overflow: hidden;
  flex-shrink: 0;
}

.track-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.track-details {
  flex: 1;
  min-width: 0;
}

.track-title {
  font-size: 0.875rem;
  color: #e2e8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.track-metadata {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 0.25rem;
}

.track-actions {
  display: flex;
  gap: 0.5rem;
}

.track-play-button,
.track-remove-button {
  background: transparent;
  border: none;
  color: #94a3b8;
  padding: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
}

.track-play-button svg,
.track-remove-button svg {
  width: 1rem;
  height: 1rem;
}

.track-play-button:hover {
  color: #60a5fa;
}

.track-remove-button:hover {
  color: #f87171;
}

.playlist-delete-button,
.playlist-clear-button {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.playlist-delete-button {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

.playlist-delete-button:hover {
  background: rgba(239, 68, 68, 0.2);
}

.playlist-clear-button {
  background: rgba(51, 65, 85, 0.5);
  color: #e2e8f0;
}

.playlist-clear-button:hover {
  background: rgba(71, 85, 105, 0.5);
}

.playlist-delete-button svg,
.playlist-clear-button svg {
  width: 1rem;
  height: 1rem;
}

/* Animations */
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

@keyframes slideIn {
  from { transform: translateY(-0.625rem); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes sound {
  0% { height: 0.3rem; }
  50% { height: 1.5rem; }
  100% { height: 0.3rem; }
}

/* Transitions */
.search-slide-enter-active,
.search-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 12.5rem;
}

.search-slide-enter-from,
.search-slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-0.625rem);
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 31.25rem;
}

.slide-right-enter-from,
.slide-right-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-0.625rem);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Light Mode Support */
@media (prefers-color-scheme: light) {
  .music-container {
    background: rgba(255, 255, 255, 0.95);
    border-color: rgba(226, 232, 240, 0.8);
  }

  .title {
    color: #1e293b;
  }

  .status-badge {
    background: rgba(241, 245, 249, 0.8);
    color: #64748b;
  }

  .action-button {
    background: rgba(241, 245, 249, 0.8);
    color: #64748b;
  }

  .track-info {
    background: rgba(248, 250, 252, 0.8);
  }

  .current-title {
    color: #1e293b;
  }

  .search-input {
    background: white;
    color: #1e293b;
    border-color: rgba(226, 232, 240, 0.8);
  }
}

/* Touch Device Optimizations */
@media (hover: none) and (pointer: coarse) {
  .action-button,
  .search-button {
    min-height: 2.75rem;
    min-width: 2.75rem;
  }

  .search-input {
    font-size: 1rem;
    padding: 0.75rem 2.75rem 0.75rem 0.75rem;
  }
  
  .control-button {
    min-height: 2.75rem;
    min-width: 2.75rem;
  }
  
  .play-button {
    min-height: 3.5rem;
    min-width: 3.5rem;
  }
  
  .progress-bar, .volume-slider {
    height: 0.5rem;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  .music-container {
    background: white;
    border: 0.125rem solid black;
  }

  .title {
    color: black;
  }

  .status-badge {
    background: white;
    border: 0.125rem solid black;
    color: black;
  }

  .status-badge.active {
    background: #4ade80;
    color: black;
  }

  .action-button {
    background: white;
    border: 0.125rem solid black;
    color: black;
  }

  .track-info {
    background: white;
    border: 0.125rem solid black;
  }

  .current-title {
    color: black;
  }

  .status-indicator {
    color: black;
  }

  .query-tag {
    background: white;
    border: 0.125rem solid black;
    color: black;
  }

  .search-input {
    background: white;
    border: 0.125rem solid black;
    color: black;
  }

  .status-message {
    border: 0.125rem solid currentColor;
  }
}

/* Responsive Design */
@media (max-width: 48em) { /* 768px */
  .music-dashboard {
    padding: 1rem;
  }

  .content-wrapper {
    padding: 1rem;
  }

  .title {
    font-size: 1.125rem;
  }

  .action-button {
    width: 2.25rem;
    height: 2.25rem;
  }

  .track-info {
    padding: 0.75rem;
  }

  .search-section {
    padding: 0.75rem;
  }
  
  .album-artwork {
    width: 4rem;
    height: 4rem;
  }
  
  .controls-row {
    gap: 1rem;
  }
  
  .play-button {
    width: 3rem;
    height: 3rem;
  }

  .playlist-select-container {
    flex-direction: column;
  }

  .modal-container {
    max-width: 100%;
  }
}
</style>