#!/bin/bash

source "$(dirname "$0")/../../../scripts/utils.sh"

ROOT_DIR=$(find_root_path)
MODEL_DIR="$ROOT_DIR/apps/services/audio/text_to_speech/impl/assets/kokoro/"

mkdir -p "$MODEL_DIR"

# List of files to download
FILES=(
    "kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
    # "kokoro-quant-convinteger.onnx https://github.com/taylorchu/kokoro-onnx/releases/download/v0.1.0/kokoro-quant-convinteger.onnx"
    # "voices.json https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.json"
    "voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
)

# Download function
download_file() {
    local filename=$1
    local url=$2
    local output="$MODEL_DIR/$filename"
    
    # Check if file already exists
    if [[ -f "$output" ]]; then
        echo "$filename already exists at $output, skipping download."
        return 0
    fi
    
    echo "Downloading $filename from $url..."
    if curl -L "$url" -o "$output"; then
        echo "$filename downloaded successfully to $output"
        return 0
    else
        echo "Failed to download $filename"
        return 1
    fi
}

# Download all files
for file in "${FILES[@]}"; do
    filename=$(echo "$file" | awk '{print $1}')
    url=$(echo "$file" | awk '{print $2}')
    if ! download_file "$filename" "$url"; then
        exit 1
    fi
done