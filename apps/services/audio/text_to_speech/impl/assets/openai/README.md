# OpenAI TTS Implementation

This directory contains the OpenAI Text-to-Speech implementation.

## Features

- High-quality speech synthesis using OpenAI's TTS API
- Support for multiple voices (alloy, ash, coral, echo, fable, onyx, nova, sage, shimmer)
- Support for multiple audio formats (mp3, opus, aac, flac, wav, pcm)
- Control over speech speed
- Two quality models: tts-1 (faster) and tts-1-hd (higher quality)

## Configuration

The OpenAI TTS implementation requires an API key. You can set it:

1. In the configuration (`OpenAITTSConfig.api_key`)
2. As an environment variable: `OPENAI_API_KEY`

## Usage

```python
from services.audio.text_to_speech.impl.openai_tts import OpenAITTS, OpenAITTSConfig
from services.audio.text_to_speech.core import AudioConfig

# Configure the service
config = OpenAITTSConfig(
    tts_model="tts-1-hd",  # tts-1 or tts-1-hd
    voice_id="alloy",      # See available_voices for options
)

# Create the service
tts = OpenAITTS(
    name="OpenAITTS",
    model_config=config,
    audio_config=AudioConfig(format="mp3")
)

# Generate speech
async def generate_speech():
    audio_data = await tts.synthesize_text(
        "Hello, this is a test of the OpenAI text-to-speech system.",
        voice_override="nova"  # Optional: override the default voice
    )
    
    # Save to file
    with open("output.mp3", "wb") as f:
        f.write(audio_data)
```

## Voice Options

- `alloy`: Neutral voice
- `echo`: Male voice
- `fable`: Male voice
- `onyx`: Male voice
- `nova`: Female voice
- `shimmer`: Female voice
- `ash`: Neutral voice
- `coral`: Female voice
- `sage`: Male voice

## Supported Languages

The OpenAI TTS implementation supports multiple languages. See the OpenAI documentation for details on language support.
