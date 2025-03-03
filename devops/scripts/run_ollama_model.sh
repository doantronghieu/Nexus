#!/bin/bash
# Default model
DEFAULT_MODEL="qwen2.5:0.5b"
# Get the model name from the argument, or use the default
MODEL=${1:-$DEFAULT_MODEL}
# Get the directory of the script
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Function to check if Ollama is ready
check_ollama_ready() {
 local max_attempts=30
 local attempt=1
 local wait_time=2
 echo "Waiting for Ollama to be ready..."
 while [ $attempt -le $max_attempts ]; do
   if curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/api/tags | grep -q "200"; then
     echo "Ollama is ready!"
     return 0
   fi
   echo "Attempt $attempt: Ollama is not ready yet. Waiting..."
   sleep $wait_time
   attempt=$((attempt + 1))
 done
 echo "Ollama failed to become ready after $max_attempts attempts."
 return 1
}

# Check if Ollama container is running
if ! docker ps | grep -q ollama; then
 echo "Ollama container is not running. Starting it now..."
 $SCRIPT_DIR/run_ollama.sh
 # Wait for Ollama to be ready
 if ! check_ollama_ready; then
   echo "Failed to start Ollama. Exiting."
   exit 1
 fi
fi

# Run the specified model
echo "Running model: $MODEL"
docker exec -d ollama ollama pull $MODEL
docker exec -d ollama ollama run $MODEL

echo "Model $MODEL is now running in the Ollama container."