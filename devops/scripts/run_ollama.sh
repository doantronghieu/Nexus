#!/bin/bash

set -e  # Exit on error

# Get the directory of the script
SCRIPT_DIR=$(dirname "$0")
# Get the parent directory of the script (devops folder)
PARENT_DIR=$(dirname "$SCRIPT_DIR")
# Construct the path to the docker-compose.yaml file
COMPOSE_FILE="$PARENT_DIR/docker/docker-compose.yaml"

# Function to check docker service
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo "Docker service is not running"
        exit 1
    fi
}

# Function to check and remove existing container
check_and_remove_container() {
    if docker ps -a | grep -q ollama; then
        echo "Ollama container already exists. Removing it..."
        docker rm -f ollama
    fi
}

# Function to check port availability
check_port() {
    if lsof -Pi :11434 -sTCP:LISTEN -t >/dev/null ; then
        echo "Port 11434 is already in use"
        exit 1
    fi
}

# Function to check GPU support for Docker
check_gpu_support() {
    if ! docker info | grep -q "Runtimes.*nvidia" ; then
        echo "Docker NVIDIA runtime is not set up"
        exit 1
    fi
}

# Initial docker check
check_docker

# Check if 'jetson' is passed as an argument
if [[ "$1" == "jetson" ]]; then
    check_and_remove_container
    check_port
    echo "Running Ollama for Jetson"
    jetson-containers run -d --name ollama dustynv/ollama:r36.2.0
else
    # Detect the operating system
    if [[ "$(uname)" == "Linux" ]]; then
        check_and_remove_container
        check_port
        # Check for NVIDIA GPU on Linux
        if [[ -f "/proc/driver/nvidia/version" ]]; then
            check_gpu_support
            echo "Running Ollama on Linux with GPU support"
            docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
        else
            echo "Running Ollama on Linux without GPU support"
            docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
        fi
    elif [[ "$(uname)" == "Darwin" ]]; then
        # macOS
        docker compose -f "$COMPOSE_FILE" pull ollama
        docker compose -f "$COMPOSE_FILE" up -d ollama
        echo "Ollama is running on macOS"
    else
        # Other operating systems
        docker compose -f "$COMPOSE_FILE" pull ollama
        docker compose -f "$COMPOSE_FILE" up -d ollama
        echo "Ollama is running"
    fi
fi