#!/usr/bin/env python3

import sys
import subprocess
import pkg_resources

def install_required_packages():
    required_packages = ['vosk', 'pyaudio']
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    
    for package in required_packages:
        if package not in installed_packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully!")

# Install required packages
print("Checking and installing required packages...")
install_required_packages()

# Now import the required packages
import pyaudio
import queue
from vosk import Model, KaldiRecognizer
import json

class SpeechRecognizer:
    def __init__(self):
        # Audio parameters
        self.FRAME_RATE = 16000
        self.CHANNELS = 1
        self.CHUNK_SIZE = 8000
        
        # Initialize model
        self.model = Model(lang="en-us")
        self.recognizer = KaldiRecognizer(self.model, self.FRAME_RATE)
        self.recognizer.SetWords(True)

    def inference(self, audio_data):
        """
        Perform inference on audio data
        
        Args:
            audio_data: bytes of audio data
        
        Returns:
            str: recognized text
        """
        if self.recognizer.AcceptWaveform(audio_data):
            result = json.loads(self.recognizer.Result())
            return result["text"]
        return ""

    def get_partial_result(self):
        """Get partial recognition result"""
        return json.loads(self.recognizer.PartialResult())["partial"]

    def get_final_result(self):
        """Get final recognition result"""
        return json.loads(self.recognizer.FinalResult())["text"]


def start_microphone_stream(recognizer: SpeechRecognizer):
    """Helper function to stream from microphone"""
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=recognizer.CHANNELS,
        rate=recognizer.FRAME_RATE,
        input=True,
        frames_per_buffer=recognizer.CHUNK_SIZE
    )
    
    print("Listening... Press Ctrl+C to stop")
    
    try:
        while True:
            data = stream.read(recognizer.CHUNK_SIZE)
            text = recognizer.inference(data)
            if text:
                print("You said:", text)
    
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def main():
    recognizer = SpeechRecognizer()
    
    # Example 1: Using with microphone
    start_microphone_stream(recognizer)
    
    # Example 2: Using with specific audio data
    """
    # Process specific audio data
    audio_data = b'...'  # your audio bytes here
    text = recognizer.inference(audio_data)
    print("Recognized:", text)
    """

if __name__ == "__main__":
    main()
