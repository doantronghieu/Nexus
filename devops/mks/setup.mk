# setup.mk

# Define the shell to use
SHELL := /bin/bash

# Define the root directory
ROOT_DIR := $(shell pwd)

# Define the path to setup.sh
SETUP_SCRIPT := $(ROOT_DIR)/devops/scripts/setup.sh

# Run the setup.sh script
setup:
	@echo "Ensuring setup.sh is executable..."
	@chmod +x $(SETUP_SCRIPT)
	@echo "Running setup.sh..."
	@$(SETUP_SCRIPT)
	@echo "Setup complete."

.PHONY: setup