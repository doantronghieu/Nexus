#!/bin/bash

# Get the current user
CURRENT_USER=$(whoami)

# Get the home directory (works on both Linux and macOS)
HOME_DIR=$(eval echo ~$CURRENT_USER)

# Define the paths
MLC_LLM_CACHE="$HOME_DIR/.cache/mlc_llm/"
HUGGINGFACE_CACHE="$HOME_DIR/.cache/huggingface/"
HUGGINGFACE_CACHE="$HOME_DIR/.cache/whisper/"
OLLAMA_DIR="$HOME_DIR/.ollama/"

# Function to delete contents of a directory
delete_contents() {
    local dir="$1"
    if [ -d "$dir" ]; then
        echo "Deleting contents of $dir"
        rm -rf "$dir"/*
    else
        echo "Directory $dir does not exist. Skipping."
    fi
}

# Delete contents of all three directories
delete_contents "$MLC_LLM_CACHE"
delete_contents "$HUGGINGFACE_CACHE"
delete_contents "$OLLAMA_DIR"

echo "Cleanup complete."