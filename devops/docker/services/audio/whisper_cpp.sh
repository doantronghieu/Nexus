#!/bin/bash

# Clone the whisper.cpp repository
git clone https://github.com/ggerganov/whisper.cpp apps/services/audio/speech_to_text/impl/assets/whisper.cpp

# Download models
# https://github.com/ggerganov/whisper.cpp/blob/master/models/download-ggml-model.sh
sh apps/services/audio/speech_to_text/impl/assets/whisper.cpp/models/download-ggml-model.sh tiny
sh apps/services/audio/speech_to_text/impl/assets/whisper.cpp/models/download-ggml-model.sh tiny-q5_1

cd apps/services/audio/speech_to_text/impl/assets/whisper.cpp
cmake -B build
cmake --build build --config Release

# ./build/bin/whisper-cli -h
# Test
./build/bin/whisper-cli -m models/ggml-tiny.bin -f samples/jfk.wav -np -nt

echo "Setup and quantization completed successfully!"