#!/bin/bash

# Function to log messages with timestamps
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if Ollama is running
check_ollama_running() {
    if pgrep -x "ollama" > /dev/null; then
        log_message "Error: Ollama is currently running. Please stop it first."
        return 1
    fi
    return 0
}

# Function to safely remove models
remove_models() {
    local models_dir="$1"
    local backup_dir="${models_dir}_backup_$(date '+%Y%m%d_%H%M%S')"
    
    # Create backup
    log_message "Creating backup at $backup_dir"
    if ! cp -r "$models_dir" "$backup_dir"; then
        log_message "Error: Failed to create backup"
        return 1
    fi
    
    # Remove entire models directory and recreate it
    log_message "Removing models directory and contents"
    if ! rm -rf "$models_dir" && mkdir -p "$models_dir"; then
        log_message "Error: Failed to remove and recreate models directory"
        log_message "Restoring from backup..."
        cp -r "$backup_dir"/* "$models_dir"
        return 1
    fi
    
    # Create required subdirectories
    mkdir -p "$models_dir/blobs"
    mkdir -p "$models_dir/manifests"
    
    log_message "Successfully cleared models"
    log_message "Backup stored at: $backup_dir"
    return 0
}

# Main script
main() {
    # Check if running as root when needed
    if [ "$(uname -s)" = "Linux" ] && [ "$EUID" -ne 0 ]; then
        log_message "Error: On Linux, this script must be run as root"
        exit 1
    fi
    
    # Check if Ollama is running
    if ! check_ollama_running; then
        exit 1
    fi
    
    # Detect OS and set appropriate path
    local models_dir
    case "$(uname -s)" in
        Darwin)
            models_dir="${HOME}/.ollama/models"
            ;;
        Linux)
            models_dir="/usr/share/ollama/.ollama/models"
            ;;
        *)
            log_message "Error: Unsupported operating system"
            exit 1
            ;;
    esac
    
    log_message "Operating System: $(uname -s)"
    log_message "Models directory: $models_dir"
    
    # Confirm with user
    read -p "Are you sure you want to clear all Ollama models? This action cannot be undone. (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_message "Operation cancelled by user"
        exit 1
    fi
    
    # Remove models
    if ! remove_models "$models_dir"; then
        log_message "Failed to clear models"
        exit 1
    fi
}

# Run main function
main

# chmod +x clear-ollama-models.sh
# ./clear-ollama-models.sh