#!/bin/bash

# Exit on error, undefined variables, and pipe failures
set -euo pipefail

# Script constants
REPO_URL="https://github.com/lingjzhu/clap-ipa"
REPO_PATH="others/repos/clap-ipa"
TARGET_PATH="apps/services/audio/keyword_spotting/impl/clap"

# Source utilities
SCRIPT_DIR="$(dirname "$0")"
source "${SCRIPT_DIR}/../../utils.sh"

# Function to handle repository setup
setup_repository() {
    if [ -d "$REPO_PATH" ]; then
        echo "Repository directory exists. Updating..."
        cd "$REPO_PATH"
        git pull
        cd - > /dev/null
    else
        echo "Cloning repository..."
        mkdir -p "$(dirname "$REPO_PATH")"
        git clone "$REPO_URL" "$REPO_PATH"
    fi
}

# Function to copy required files
copy_files() {
    echo "Copying clap directory to implementation path..."
    mkdir -p "$(dirname "$TARGET_PATH")"
    rm -rf "$TARGET_PATH"
    cp -r "${REPO_PATH}/clap" "$TARGET_PATH"
}

# Main execution
main() {
    echo "Starting clap-ipa setup..."
    
    # Check and activate conda environment
    check_and_activate_conda_env
    
    # Setup repository
    setup_repository
    
    # Install package
    cd "$REPO_PATH"
    pip install .
    cd - > /dev/null
    
    # Copy implementation files
    copy_files
    
    echo "Setup clap-ipa completed successfully!"
}

# Execute main function
main

# chmod +x devops/scripts/setup/repos/clap-ipa.sh
# ./devops/scripts/setup/repos/clap-ipa.sh