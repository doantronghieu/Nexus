#!/bin/bash
# Get the directory of the script
SCRIPT_DIR=$(dirname "$0")
# Get the parent directory of the script (devops folder)
PARENT_DIR=$(dirname "$SCRIPT_DIR")
# Construct the path to the docker-compose.yaml file
COMPOSE_FILE="$PARENT_DIR/docker/docker-compose.yaml"

# Stop the Ollama service
docker compose -f "$COMPOSE_FILE" stop ollama
docker compose -f "$COMPOSE_FILE" rm -f ollama

echo "Ollama has been stopped and removed."