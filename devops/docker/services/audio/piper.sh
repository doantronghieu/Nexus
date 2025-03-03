#!/bin/bash

# conda deactivate
# conda activate dev

# # Install Piper TTS
# pip install piper-tts piper-phonemize-cross --no-deps

# Create directory structure
mkdir -p apps/services/audio/text_to_speech/impl/assets/piper/{models,data,download,outputs}

# Download model files
wget -P apps/services/audio/text_to_speech/impl/assets/piper/models https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx
wget -P apps/services/audio/text_to_speech/impl/assets/piper/models https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx.json

echo "Script execution completed."