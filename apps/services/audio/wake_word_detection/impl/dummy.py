import numpy as np
from pynput import audio

class PorcupineWakeWord(WakeWordDetector):
    async def _initialize_engine(self) -> None:
        logger.info("Initializing Porcupine engine")
        self.engine = await self._load_porcupine()
        self.stream = None
        
    async def __call__(self, audio_path: Path) -> bool:
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        pcm = await self._load_audio(audio_path)
        return await self.engine.process(pcm)
    
    async def start_stream(
        self,
        callback: Optional[Callable[[bool], None]] = None
    ) -> AsyncIterator[bool]:
        if self.stream:
            await self.stop_stream()
        
        self.stream = audio.LiveStream(
            sample_rate=16000,
            chunk_size=512,
            channels=1
        )
        
        async with self.stream:
            while True:
                chunk = await self.stream.read()
                detected = await self.engine.process(chunk)
                
                if callback and detected:
                    callback(detected)
                    
                yield detected
    
    async def stop_stream(self) -> None:
        if self.stream:
            await self.stream.close()
            self.stream = None

# Usage
# File-based detection
async with PorcupineWakeWord() as detector:
    detected = await detector(Path("audio.wav"))
    
# Real-time detection with callback
def on_wake_word(detected: bool):
    if detected:
        logger.info("Wake word detected!")

async with PorcupineWakeWord() as detector:
    async for detected in detector.start_stream(callback=on_wake_word):
        if detected:
            # Do something when wake word is detected
            pass