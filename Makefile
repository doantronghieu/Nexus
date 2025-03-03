# Makefile

# Check for Docker Compose command
COMPOSE_CMD := $(shell if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then \
					echo "docker compose"; \
				elif command -v docker-compose >/dev/null 2>&1; then \
					echo "docker-compose"; \
				else \
					echo "echo 'Error: Docker Compose not found' >&2; exit 1"; \
				fi)

# Use the determined Docker Compose command for the main services
export DOCKER_COMPOSE_INFRA := $(COMPOSE_CMD) -f devops/docker/infra.docker-compose.yaml
export DOCKER_COMPOSE_SERVERS := $(COMPOSE_CMD) -f devops/docker/servers.docker-compose.yaml

# Define a separate variable for services
export DOCKER_COMPOSE_TTS_JETSON := $(COMPOSE_CMD) -f devops/docker/jetson/FastAPI.TTS-piper.docker-compose.yaml
export DOCKER_COMPOSE_LLM_NANO_JETSON := $(COMPOSE_CMD) -f devops/docker/jetson/FastAPI.LLM-Nano.docker-compose.yaml

# Include service-specific makefiles
include devops/mks/setup.mk
include devops/mks/qdrant.mk
include devops/mks/ollama.mk
include devops/mks/postgres.mk
include devops/mks/mongo.mk
include devops/mks/services.mk

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available commands:"
	@echo " make setup                               - Run the setup script to make all .sh files executable"
	@echo " make start [jetson]                      - Start all services (use 'jetson' for Jetson-specific Ollama)"
	@echo " make stop [jetson]                       - Stop all services (use 'jetson' for Jetson-specific Ollama)"
	@echo " make remove [jetson]                     - Remove all services (use 'jetson' for Jetson-specific Ollama)"
	@echo " make start-<service> [jetson]            - Start a specific service"
	@echo " make stop-<service> [jetson]             - Stop a specific service"
	@echo " make remove-<service> [jetson]           - Remove a specific service"
	@echo " make start-multi [jetson] <services...>  - Start multiple specific services"
	@echo " make stop-multi [jetson] <services...>   - Stop multiple specific services"
	@echo " make remove-multi [jetson] <services...> - Remove multiple specific services"
	@echo " make ollama-list-model                   - List currently supported models"
	@echo " make ps                                  - List all running services"
	@echo " make down                                - Stop and remove all services"

# List all running services
ps:
	$(DOCKER_COMPOSE_INFRA) ps
	$(DOCKER_COMPOSE_SERVERS) ps

# Stop and remove all services
down:
	$(DOCKER_COMPOSE_INFRA) down
	$(DOCKER_COMPOSE_SERVERS) down

.PHONY: help ps down