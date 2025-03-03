# Main Makefile

# Include other makefiles
include makefiles/ollama.mk

# You can add other includes here as your project grows
# include makefiles/other_component.mk

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available targets:"
	@echo "  ollama-start         - Start Ollama container"
	@echo "  ollama-stop          - Stop Ollama container"
	@echo "  ollama-run-model     - Run a model (use MODEL=<model_name> to specify)"
	@echo "  ollama-start-and-run - Start Ollama and run a model"

.PHONY: help