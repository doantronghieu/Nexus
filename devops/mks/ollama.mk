# Makefile for Ollama operations

# Default model
DEFAULT_MODEL := llama3.1:8b

# Paths
SCRIPTS_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))../scripts

# Start Ollama container
ollama-start:
	@$(SCRIPTS_DIR)/run_ollama.sh $(filter jetson,$(MAKECMDGOALS))

# Stop Ollama container
ollama-stop:
	@if [ "$(filter jetson,$(MAKECMDGOALS))" = "jetson" ]; then \
		docker stop ollama && docker rm ollama; \
	else \
		$(SCRIPTS_DIR)/stop_ollama.sh; \
	fi

# All-in-one command to start Ollama and run a model
ollama-start-and-run:
	@$(SCRIPTS_DIR)/run_ollama_model.sh $(MODEL) $(filter jetson,$(MAKECMDGOALS))

ollama-list-model:
	@if [ "$(filter jetson,$(MAKECMDGOALS))" = "jetson" ]; then \
		docker exec ollama ollama list; \
	else \
		docker exec ollama ollama list; \
	fi

# This allows the 'jetson' argument to be passed without errors
jetson:
	@:

.PHONY: ollama-start ollama-stop ollama-run-model ollama-start-and-run jetson