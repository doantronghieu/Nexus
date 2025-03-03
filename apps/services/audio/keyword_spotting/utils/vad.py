"""
Voice Activity Detection utilities for audio processing.
"""

import time
import numpy as np
from loguru import logger

class VoiceActivityDetector:
    """Detects voice activity in audio streams based on energy thresholds."""
    
    def __init__(self, threshold: float = 0.01, silence_duration: float = 0.5):
        """
        Initialize VAD.
        
        Args:
            threshold: Energy threshold for speech detection
            silence_duration: Seconds of silence to consider speech ended
        """
        self.threshold = threshold
        self.silence_duration = silence_duration
        self.speaking_started = None
        self.is_speaking = False
        self.last_active_time = None

    def detect(self, audio_data: np.ndarray) -> tuple[bool, float | None]:
        """
        Detect voice activity in audio data.
        
        Args:
            audio_data: Audio samples
            
        Returns:
            Tuple of (is_speaking, speech_start_time)
        """
        current_time = time.time()
        
        # Calculate energy of latest audio chunk (100ms at 16kHz)
        chunk_size = min(1600, len(audio_data))
        energy = np.mean(np.square(audio_data[-chunk_size:]))
        is_active = energy > self.threshold
        
        # State transition logic
        if not self.is_speaking and is_active:
            # Start of speech
            self.speaking_started = current_time
            self.is_speaking = True
            self.last_active_time = current_time
            logger.debug(f"Speech started (energy: {energy:.6f})")
            
        elif self.is_speaking and is_active:
            # Continued speech
            self.last_active_time = current_time
            
        elif self.is_speaking and not is_active:
            # Check if silence has been long enough
            if current_time - self.last_active_time > self.silence_duration:
                self.is_speaking = False
                self.speaking_started = None
                logger.debug("Speech ended (silence threshold reached)")
        
        return self.is_speaking, self.speaking_started