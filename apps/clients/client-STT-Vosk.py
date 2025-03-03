#!/usr/bin/env python3

import asyncio
import json
import wave
import sys
import logging
import argparse
import sounddevice as sd
from queue import Queue
from typing import Optional, List

import websockets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

class AudioClient:
    def __init__(self, uri: str, config: dict):
        self.uri = uri
        self.config = config
        self.audio_queue = Queue()
        
    def audio_callback(self, indata, frames, time, status):
        """Callback for sounddevice to handle audio chunks."""
        if status:
            logger.warning(f"Audio status: {status}")
        self.audio_queue.put(bytes(indata))

    async def process_file(self, filename: str):
        """Process an audio file."""
        async with websockets.connect(self.uri) as websocket:
            try:
                # Send configuration
                await websocket.send(json.dumps({"config": self.config}))
                await websocket.recv()  # Wait for configuration acknowledgment
                
                # Open and process audio file
                with wave.open(filename, "rb") as wf:
                    # Calculate buffer size (0.2 seconds of audio)
                    buffer_size = int(wf.getframerate() * 0.2)
                    
                    while True:
                        data = wf.readframes(buffer_size)
                        if len(data) == 0:
                            break
                            
                        await websocket.send(data)
                        result = await websocket.recv()
                        print(result)
                    
                    # Send EOF message
                    await websocket.send('{"eof" : 1}')
                    final_result = await websocket.recv()
                    print("Final result:", final_result)
                    
            except Exception as e:
                logger.error(f"Error during file processing: {str(e)}")

    async def process_microphone(self, device: Optional[int] = None, sample_rate: int = 16000):
        """Process audio from microphone."""
        async with websockets.connect(self.uri) as websocket:
            try:
                # Send configuration
                await websocket.send(json.dumps({"config": self.config}))
                await websocket.recv()  # Wait for configuration acknowledgment
                
                # Start audio stream
                with sd.RawInputStream(
                    samplerate=sample_rate,
                    blocksize=8000,
                    device=device,
                    dtype="int16",
                    channels=1,
                    callback=self.audio_callback
                ):
                    logger.info("Started recording. Press Ctrl+C to stop.")
                    
                    while True:
                        data = self.audio_queue.get()
                        await websocket.send(data)
                        result = await websocket.recv()
                        print(result)
                        
            except KeyboardInterrupt:
                logger.info("Stopped recording")
            except Exception as e:
                logger.error(f"Error during microphone processing: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Speech-to-Text Client")
    parser.add_argument("--uri", type=str, default="ws://localhost:8000/stt",
                      help="WebSocket server URI")
    parser.add_argument("--file", type=str, help="Audio file to process")
    parser.add_argument("--list-devices", action="store_true",
                      help="List available audio devices")
    parser.add_argument("--device", type=int_or_str,
                      help="Input device (numeric ID or substring)")
    parser.add_argument("--sample-rate", type=int, default=16000,
                      help="Audio sample rate")
    parser.add_argument("--alternatives", type=int, default=0,
                      help="Number of alternative transcriptions")
    parser.add_argument("--show-words", action="store_true",
                      help="Show word-level timing information")
    parser.add_argument("--partial-words", action="store_true",
                      help="Show words in partial results")
    parser.add_argument("--phrases", type=str, nargs="*",
                      help="List of possible phrases for recognition")
    parser.add_argument("--nlsml", action="store_true",
                      help="Output in NLSML format")
    
    args = parser.parse_args()
    
    if args.list_devices:
        print(sd.query_devices())
        sys.exit(0)
    
    # Prepare configuration
    config = {
        "sample_rate": args.sample_rate,
        "show_words": args.show_words,
        "max_alternatives": args.alternatives,
        "partial_words": args.partial_words,
        "nlsml": args.nlsml
    }
    
    if args.phrases:
        config["phrase_list"] = args.phrases
    
    client = AudioClient(args.uri, config)
    
    if args.file:
        asyncio.run(client.process_file(args.file))
    else:
        asyncio.run(client.process_microphone(args.device, args.sample_rate))

if __name__ == "__main__":
    main()