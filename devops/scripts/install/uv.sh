#!/bin/bash

function install_uv() {
    # Check if curl is available
    if command -v curl &> /dev/null; then
        echo "Installing uv using curl..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    # Check if wget is available
    elif command -v wget &> /dev/null; then
        echo "Installing uv using wget..."
        wget -qO- https://astral.sh/uv/install.sh | sh
    else
        echo "Error: Neither curl nor wget is installed. Please install one of them and try again."
        return 1
    fi
}

# Add main execution block
echo "Starting uv installation..."
if install_uv; then
    echo "uv installation completed successfully!"
else
    echo "uv installation failed!" >&2
    exit 1
fi