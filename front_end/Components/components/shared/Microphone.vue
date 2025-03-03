<template>
  <div class="microphone-container">
    <button 
      class="microphone-button"
      :class="{ 'recording': isRecording, 'calibrating': isCalibrating }"
      @click="toggleRecording"
      :disabled="isProcessing"
    >
      <span v-if="isProcessing">Processing...</span>
      <span v-else-if="isCalibrating">Calibrating... {{ calibrationTimeRemaining }}s</span>
      <span v-else-if="isRecording">Recording... {{ elapsedTime }}s</span>
      <span v-else>Start Recording</span>
    </button>
    
    <!-- Audio level visualization -->
    <div v-if="isRecording || isCalibrating" class="audio-visualization">
      <div class="audio-level-container">
        <div class="audio-level-bar" :style="{ width: `${audioLevelWidth}%` }"></div>
      </div>
      <div class="audio-level-text">
        <span>Audio Level: {{ displayedAudioLevel }} / 10</span>
        <span class="silence-indicator" :class="{ 'is-silent': isSilent }">{{ isSilent ? 'SILENT' : 'ACTIVE' }}</span>
      </div>
      <div class="silence-timer" v-if="silenceElapsed > 0">
        <span>Silence: {{ (silenceElapsed / 1000).toFixed(1) }}s</span>
      </div>
    </div>
    
    <!-- Advanced controls -->
    <div class="controls-container" v-if="!isRecording && !isCalibrating">
      <!-- Calibration time control -->
      <div class="threshold-control">
        <label for="calibTime">Calibration Time: {{ calibrationTimeValue }}s</label>
        <input 
          type="range" 
          id="calibTime" 
          min="1" 
          max="10" 
          step="1" 
          v-model.number="calibrationTimeValue"
        >
      </div>
      
      <button @click="startCalibrationOnly" class="calibrate-button">
        Calibrate Noise (without recording)
      </button>
    </div>
    
    <!-- Recording controls -->
    <div class="controls-container" v-if="isRecording || isCalibrating">
      <!-- Silence threshold control -->
      <div class="threshold-control" v-if="!isCalibrated">
        <label for="threshold">Absolute Threshold: {{ silenceThreshold.toFixed(3) }}</label>
        <input 
          type="range" 
          id="threshold" 
          min="0.001" 
          max="0.05" 
          step="0.001" 
          v-model.number="silenceThreshold"
        >
      </div>
      
      <!-- Relative threshold (when calibrated) -->
      <div class="threshold-control" v-if="isCalibrated">
        <label for="relThreshold">Relative Threshold: {{ relativeThreshold.toFixed(3) }}</label>
        <input 
          type="range" 
          id="relThreshold" 
          min="0.001" 
          max="0.02" 
          step="0.001" 
          v-model.number="relativeThreshold"
        >
        <div class="info-text">
          <span>Noise Floor: {{ noiseFloor.toFixed(4) }}</span>
          <span>Detection at: {{ (noiseFloor + relativeThreshold).toFixed(4) }}</span>
        </div>
      </div>
      
      <!-- Variance threshold control -->
      <div class="threshold-control">
        <label for="variance">Variance Threshold: {{ varianceThreshold.toFixed(6) }}</label>
        <input 
          type="range" 
          id="variance" 
          min="0.000005" 
          max="0.001" 
          step="0.000005" 
          v-model.number="varianceThreshold"
        >
      </div>
      
      <button @click="recalibrate" class="calibrate-button" v-if="isRecording && !isCalibrating">
        Recalibrate
      </button>
      
      <button @click="stopCalibrationOnly" class="calibrate-button stop" v-if="isCalibrating && isCalibrationOnly">
        Stop Calibration
      </button>
    </div>
    
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  name: 'MicrophoneComponent',
  props: {
    initialSilenceThreshold: {
      type: Number,
      default: 0.01, // Audio level below this is considered silence
    },
    showControls: {
      type: Boolean,
      default: true, // Whether to show threshold controls
    },
    silenceDuration: {
      type: Number,
      default: 2000, // Duration of silence in ms before stopping (2 seconds)
    },
    maxRecordingTime: {
      type: Number,
      default: 60, // Maximum recording time in seconds
    },
    calibrationTime: {
      type: Number,
      default: 5, // Calibration time in seconds
    }
  },
  data() {
    return {
      isRecording: false,
      isProcessing: false,
      errorMessage: '',
      mediaRecorder: null,
      audioStream: null,
      audioContext: null,
      analyzer: null,
      audioChunks: [],
      silenceTimer: null,
      recordingTimer: null,
      elapsedTime: 0,
      silenceElapsed: 0,
      silenceStartTime: null,
      lastAudioLevel: 0,
      displayedAudioLevel: 0,
      audioLevelWidth: 0,
      isSilent: false,
      silenceThreshold: this.initialSilenceThreshold,
      // Noise calibration variables
      isCalibrating: false,
      // Calibration mode flag
      isCalibrationOnly: false,
      isCalibrated: false,
      calibrationSamples: [],
      calibrationTimeRemaining: 0,
      calibrationTimer: null,
      calibrationTimeValue: this.calibrationTime, // User-configurable value
      noiseFloor: 0,
      // Speech detection variables
      audioSamples: [],
      audioSampleWindow: 20,
      varianceThreshold: 0.0001,
      logCounter: 0,
      // Silence detection threshold for calibrated environment
      relativeThreshold: 0.01
    };
  },
  methods: {
    async toggleRecording() {
      if (this.isRecording) {
        this.stopRecording();
      } else {
        await this.startRecording();
      }
    },
    
    recalibrate() {
      // Reset calibration variables to start fresh
      this.isCalibrated = false;
      this.isCalibrating = true;
      this.calibrationSamples = [];
      this.calibrationTimeRemaining = this.calibrationTimeValue;
      
      // Start calibration timer
      if (this.calibrationTimer) {
        clearInterval(this.calibrationTimer);
      }
      
      this.calibrationTimer = setInterval(() => {
        this.calibrationTimeRemaining--;
        if (this.calibrationTimeRemaining <= 0) {
          // Time's up - finalize calibration
          clearInterval(this.calibrationTimer);
          this.finalizeCalibration();
        }
      }, 1000);
      
      console.log(`Recalibrating noise floor for ${this.calibrationTimeValue} seconds...`);
    },
    
    async startCalibrationOnly() {
      try {
        this.errorMessage = '';
        this.isProcessing = true;
        
        // Set calibration-only mode
        this.isCalibrationOnly = true;
        
        // Reset calibration variables
        this.isCalibrated = false;
        this.isCalibrating = true;
        this.calibrationSamples = [];
        this.audioSamples = [];
        this.noiseFloor = 0;
        this.calibrationTimeRemaining = this.calibrationTimeValue;
        
        // Request microphone access
        this.audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Set up audio context and analyzer for silence detection
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = this.audioContext.createMediaStreamSource(this.audioStream);
        this.analyzer = this.audioContext.createAnalyser();
        this.analyzer.fftSize = 256;
        source.connect(this.analyzer);
        
        // Start calibration process without recording
        this.isProcessing = false;
        
        // Start silence detection for calibration
        this.startSilenceDetection();
        
        // Start calibration timer
        this.calibrationTimer = setInterval(() => {
          this.calibrationTimeRemaining--;
          if (this.calibrationTimeRemaining <= 0) {
            // Time's up - finalize calibration
            clearInterval(this.calibrationTimer);
            this.finalizeCalibration();
            this.stopCalibrationOnly();
          }
        }, 1000);
        
        console.log(`Starting calibration-only mode for ${this.calibrationTimeValue} seconds...`);
      } catch (error) {
        this.errorMessage = `Microphone access error: ${error.message}`;
        this.isProcessing = false;
        this.isCalibrating = false;
        this.isCalibrationOnly = false;
        console.error('Error accessing microphone:', error);
      }
    },
    
    stopCalibrationOnly() {
      // Only stop if in calibration-only mode
      if (!this.isCalibrationOnly) return;
      
      // Clear calibration timer
      if (this.calibrationTimer) {
        clearInterval(this.calibrationTimer);
        this.calibrationTimer = null;
      }
      
      // Reset calibration-only mode
      this.isCalibrationOnly = false;
      this.isCalibrating = false;
      
      // Stop and clean up audio tracks
      if (this.audioStream) {
        this.audioStream.getTracks().forEach(track => track.stop());
        this.audioStream = null;
      }
      
      if (this.audioContext) {
        this.audioContext.close();
        this.audioContext = null;
      }
      
      console.log('Calibration-only mode stopped');
    },
    
    finalizeCalibration() {
      if (this.calibrationSamples.length > 0) {
        const sortedSamples = [...this.calibrationSamples].sort((a, b) => a - b);
        // Use the median of the lowest 75% of samples as the noise floor
        const medianIndex = Math.floor(sortedSamples.length * 0.75);
        this.noiseFloor = sortedSamples[medianIndex];
        console.log(`Noise floor calibrated to: ${this.noiseFloor.toFixed(4)}, range: ${sortedSamples[0].toFixed(4)}-${sortedSamples[sortedSamples.length-1].toFixed(4)}`);
      } else {
        console.log('No calibration samples collected, using default noise floor');
        this.noiseFloor = 0.01; // Fallback value
      }
      
      this.isCalibrated = true;
      this.isCalibrating = false;
    },
    
    async startRecording() {
      try {
        this.errorMessage = '';
        this.isProcessing = true;
        this.audioChunks = [];
        this.elapsedTime = 0;
        
        // Reset calibration variables
        this.isCalibrated = false;
        this.isCalibrating = true;
        this.calibrationSamples = [];
        this.audioSamples = [];
        this.noiseFloor = 0;
        this.calibrationTimeRemaining = this.calibrationTimeValue;
        
        // Request microphone access
        this.audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Set up audio context and analyzer for silence detection
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = this.audioContext.createMediaStreamSource(this.audioStream);
        this.analyzer = this.audioContext.createAnalyser();
        this.analyzer.fftSize = 256;
        source.connect(this.analyzer);
        
        // Set up media recorder
        this.mediaRecorder = new MediaRecorder(this.audioStream);
        this.mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        };
        
        this.mediaRecorder.onstop = () => {
          this.processRecording();
        };
        
        // Start recording
        this.mediaRecorder.start();
        this.isRecording = true;
        this.isProcessing = false;
        
        // Start silence detection
        this.startSilenceDetection();
        
        // Start calibration timer
        this.calibrationTimer = setInterval(() => {
          this.calibrationTimeRemaining--;
          if (this.calibrationTimeRemaining <= 0) {
            // Time's up - finalize calibration
            clearInterval(this.calibrationTimer);
            this.finalizeCalibration();
          }
        }, 1000);
        
        // Start elapsed time counter
        this.recordingTimer = setInterval(() => {
          this.elapsedTime++;
          if (this.elapsedTime >= this.maxRecordingTime) {
            this.stopRecording();
          }
        }, 1000);
        
      } catch (error) {
        this.errorMessage = `Microphone access error: ${error.message}`;
        this.isProcessing = false;
        console.error('Error accessing microphone:', error);
      }
    },
    
    startSilenceDetection() {
      const bufferLength = this.analyzer.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      
      // Check for silence every 100ms
      const checkSilence = () => {
        if (!this.isRecording && !this.isCalibrating) return;
        
        this.analyzer.getByteFrequencyData(dataArray);
        
        // Calculate average volume level
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
          sum += dataArray[i];
        }
        const average = sum / bufferLength / 255; // Normalize to 0-1
        
        // Collect samples during calibration phase
        if (this.isCalibrating) {
          this.calibrationSamples.push(average);
        }
        
        // Calculate the adjusted audio level (with noise reduction)
        const adjustedLevel = Math.max(0, average - (this.isCalibrated ? this.noiseFloor : 0));
        this.lastAudioLevel = adjustedLevel;
        
        // Add to rolling window for detecting speech patterns
        this.audioSamples.push(adjustedLevel);
        if (this.audioSamples.length > this.audioSampleWindow) {
          this.audioSamples.shift();
        }
        
        // Calculate variance which helps detect speech patterns (speech has higher variance)
        let mean = 0;
        let variance = 0;
        
        if (this.audioSamples.length > 5) { // Need enough samples to calculate meaningful variance
          mean = this.audioSamples.reduce((sum, val) => sum + val, 0) / this.audioSamples.length;
          variance = this.audioSamples.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / this.audioSamples.length;
        }
        
        // Convert to display values (0-10 scale)
        // Scale based on calibrated environment
        let displayScale = 1;
        if (this.isCalibrated) {
          // Base the scale factor on the noise floor, making louder environments less sensitive
          displayScale = Math.max(0.2, 1 - (this.noiseFloor * 10));
        }
        
        this.displayedAudioLevel = Math.min(10, Math.round(adjustedLevel * displayScale * 100));
        this.audioLevelWidth = this.displayedAudioLevel * 10; // 0-100% for CSS width
        
        // Log every ~5 seconds for debugging
        if (this.logCounter++ % 150 === 0) {
          console.log(`Audio: ${adjustedLevel.toFixed(4)}, Variance: ${variance.toFixed(6)}, NoiseFloor: ${this.noiseFloor.toFixed(4)}, Scale: ${displayScale.toFixed(2)}`);
        }
        
        // Determine silence based on either:
        // 1. Level below absolute threshold when uncalibrated
        // 2. Level below relative threshold above noise floor when calibrated
        // 3. Low variance indicates steady background noise rather than speech
        let actualThreshold = this.silenceThreshold;
        if (this.isCalibrated) {
          // In calibrated mode, we use a relative threshold above the noise floor
          actualThreshold = this.noiseFloor + this.relativeThreshold;
        }
        
        // Check if we're silent based on level and variance
        this.isSilent = adjustedLevel < actualThreshold && variance < this.varianceThreshold;
        
        if (this.isSilent && this.isRecording) {
          if (!this.silenceStartTime) {
            this.silenceStartTime = Date.now();
          }
          
          // Calculate current silence duration
          this.silenceElapsed = Date.now() - this.silenceStartTime;
          
          if (!this.silenceTimer && this.silenceElapsed >= this.silenceDuration) {
            console.log(`Stopping due to silence: ${this.silenceElapsed}ms at level ${average.toFixed(3)}`);
            this.stopRecording();
          } else if (!this.silenceTimer) {
            this.silenceTimer = setTimeout(() => {
              // Double-check we're still silent before stopping
              if (this.isSilent) {
                console.log(`Auto-stopping after silence duration: ${this.silenceDuration}ms`);
                this.stopRecording();
              }
            }, this.silenceDuration - this.silenceElapsed);
          }
        } else {
          // If above threshold, clear silence timer and reset counter
          if (this.silenceTimer) {
            clearTimeout(this.silenceTimer);
            this.silenceTimer = null;
          }
          this.silenceStartTime = null;
          this.silenceElapsed = 0;
        }
        
        // Continue checking for silence
        requestAnimationFrame(checkSilence);
      };
      
      checkSilence();
    },
    
    stopRecording() {
      if (!this.isRecording || !this.mediaRecorder) return;
      
      // Clear all timers
      if (this.silenceTimer) {
        clearTimeout(this.silenceTimer);
        this.silenceTimer = null;
      }
      
      if (this.recordingTimer) {
        clearInterval(this.recordingTimer);
        this.recordingTimer = null;
      }
      
      if (this.calibrationTimer) {
        clearInterval(this.calibrationTimer);
        this.calibrationTimer = null;
      }
      
      // Stop recording
      if (this.mediaRecorder.state !== 'inactive') {
        this.mediaRecorder.stop();
      }
      
      this.isRecording = false;
      
      // Stop and clean up audio tracks
      if (this.audioStream) {
        this.audioStream.getTracks().forEach(track => track.stop());
        this.audioStream = null;
      }
      
      if (this.audioContext) {
        this.audioContext.close();
        this.audioContext = null;
      }
    },
    
    async processRecording() {
      if (this.audioChunks.length === 0) {
        this.errorMessage = 'No audio recorded';
        return;
      }
      
      this.isProcessing = true;
      
      try {
        // Create audio blob from chunks
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        
        // Emit the recorded audio blob to parent component
        this.$emit('recording-complete', audioBlob);
        
      } catch (error) {
        this.errorMessage = `Processing error: ${error.message}`;
        console.error('Error processing recording:', error);
      } finally {
        this.isProcessing = false;
      }
    }
  },
  beforeUnmount() {
    // Clean up resources
    this.stopRecording();
  },
  
  watch: {
    // Log changes to thresholds for debugging
    silenceThreshold(newVal) {
      console.log(`Absolute silence threshold changed to: ${newVal.toFixed(3)}`);
    },
    relativeThreshold(newVal) {
      console.log(`Relative silence threshold changed to: ${newVal.toFixed(3)}`);
      if (this.isCalibrated) {
        console.log(`Effective detection threshold: ${(this.noiseFloor + newVal).toFixed(4)}`);
      }
    },
    varianceThreshold(newVal) {
      console.log(`Variance threshold changed to: ${newVal.toFixed(6)}`);
    },
    calibrationTimeValue(newVal) {
      console.log(`Calibration time changed to: ${newVal} seconds`);
      // Emit event to allow parent components to update their prop if needed
      this.$emit('update:calibrationTime', newVal);
    }
  }
};
</script>

<style scoped>
.microphone-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
  max-width: 300px;
}

.microphone-button {
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 150px;
  height: 50px;
  border-radius: 25px;
  border: none;
  background-color: #4a90e2;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0 20px;
}

.microphone-button:hover:not(:disabled) {
  background-color: #357ae8;
  transform: scale(1.05);
}

.microphone-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.microphone-button.recording {
  background-color: #e74c3c;
  animation: pulse 1.5s infinite;
}

.microphone-button.calibrating {
  background-color: #f39c12;
  animation: pulse 1s infinite;
}

/* Audio visualization styling */
.audio-visualization {
  width: 100%;
  margin-top: 10px;
}

.audio-level-container {
  width: 100%;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
}

.audio-level-bar {
  height: 100%;
  background-color: #2ecc71;
  transition: width 0.1s ease;
}

.audio-level-text {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  font-size: 0.9rem;
}

.silence-indicator {
  font-weight: bold;
}

.silence-indicator.is-silent {
  color: #e74c3c;
}

.silence-timer {
  width: 100%;
  text-align: center;
  margin-top: 5px;
  font-size: 0.9rem;
  font-weight: bold;
  color: #e74c3c;
}

.controls-container {
  width: 100%;
  margin-top: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.threshold-control {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.threshold-control label {
  margin-bottom: 5px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
}

.threshold-control input {
  width: 100%;
  margin-bottom: 2px;
}

.info-text {
  width: 100%;
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #666;
  margin-top: 3px;
}

.calibrate-button {
  margin-top: 5px;
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.calibrate-button:hover {
  background-color: #2980b9;
}

.calibrate-button.stop {
  background-color: #e74c3c;
}

.calibrate-button.stop:hover {
  background-color: #c0392b;
}

.error-message {
  color: #e74c3c;
  font-size: 0.9rem;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(231, 76, 60, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(231, 76, 60, 0);
  }
}
</style>
