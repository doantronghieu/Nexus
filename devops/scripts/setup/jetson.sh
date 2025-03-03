#!/bin/bash

# Jetson System Setup Script
# This script automates the setup process for Jetson devices
# Including Docker configuration, swap setup, and power mode optimization

set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failures

# Backup directory
BACKUP_DIR="/var/backup/jetson-setup/$(date +%Y%m%d_%H%M%S)"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1" | tee -a "$BACKUP_DIR/setup.log"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$BACKUP_DIR/setup.log"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$BACKUP_DIR/setup.log"
}

# Initialize backup and logging
initialize_backup() {
    mkdir -p "$BACKUP_DIR"
    log_info "Created backup directory: $BACKUP_DIR"
    
    # Start logging
    exec 1> >(tee -a "$BACKUP_DIR/setup.log")
    exec 2> >(tee -a "$BACKUP_DIR/setup.log" >&2)
    
    log_info "Script started at $(date)"
}

# Cleanup function for error handling
cleanup() {
    local exit_code=$?
    log_info "Script ended at $(date)"
    
    if [ $exit_code -ne 0 ]; then
        log_error "Script failed with exit code $exit_code"
        log_info "Logs and backups available at $BACKUP_DIR"
    fi
    
    exit $exit_code
}

trap cleanup EXIT

# Backup a file before modification
backup_file() {
    local file="$1"
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/$(basename "$file").backup"
        log_info "Backed up $file"
    fi
}

# Validate JSON syntax
validate_json() {
    local json_content="$1"
    if ! echo "$json_content" | jq '.' >/dev/null 2>&1; then
        return 1
    fi
    return 0
}

# Check system resources
check_system_resources() {
    log_info "Checking system resources..."
    
    # Check available RAM
    local total_ram=$(free -g | awk '/^Mem:/{print $2}')
    if [ "$total_ram" -lt 4 ]; then
        log_error "Insufficient RAM. Minimum 4GB required, found ${total_ram}GB"
        exit 1
    fi
    
    # Check available disk space
    local root_space=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$root_space" -lt 10 ]; then
        log_error "Insufficient disk space. Minimum 10GB required, found ${root_space}GB"
        exit 1
    }
}

# Check running services
check_running_services() {
    log_info "Checking system services..."
    
    # Check Docker service status
    if systemctl is-active --quiet docker; then
        log_info "Docker service is running"
    else
        log_error "Docker service is not running"
        exit 1
    fi
}

# Verify Jetson environment
verify_jetson_environment() {
    log_info "Verifying Jetson environment..."
    
    # Check for L4T version
    if [ ! -f "/etc/nv_tegra_release" ]; then
        log_error "Not running on a Jetson device"
        exit 1
    fi
    
    # Extract L4T version
    local l4t_version=$(head -n 1 /etc/nv_tegra_release | grep -o 'R[0-9]\+\.[0-9]\+\.[0-9]\+')
    log_info "Detected L4T version: $l4t_version"
    
    # Verify supported version
    if ! [[ "$l4t_version" =~ ^R(32\.[7-9]|3[5-6]\.) ]]; then
        log_error "Unsupported L4T version. Requires >= R32.7.1"
        exit 1
    }
}

# Configure Docker runtime with safety checks
setup_docker_runtime() {
    local docker_config="/etc/docker/daemon.json"
    local docker_dir="$1"
    
    log_info "Configuring Docker runtime..."
    
    # Backup existing Docker configuration
    backup_file "$docker_config"
    
    # Create new Docker configuration
    local config_content=$(cat <<EOF
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },
    "default-runtime": "nvidia",
    "data-root": "${docker_dir}"
}
EOF
)

    # Validate JSON syntax
    if ! validate_json "$config_content"; then
        log_error "Invalid JSON configuration generated"
        exit 1
    }
    
    # Write configuration
    echo "$config_content" > "$docker_config"
    
    # Test Docker configuration
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker configuration test failed"
        # Restore backup
        if [ -f "$BACKUP_DIR/$(basename "$docker_config").backup" ]; then
            cp "$BACKUP_DIR/$(basename "$docker_config").backup" "$docker_config"
            log_info "Restored Docker configuration from backup"
        fi
        exit 1
    fi
}

# Setup swap with safety checks
setup_swap() {
    local swap_size="$1"
    local swap_path="$2"
    
    log_info "Setting up swap..."
    
    # Check available space
    local available_space=$(df -BG "$(dirname "$swap_path")" | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$available_space" -lt "$((swap_size + 1))" ]; then
        log_error "Insufficient space for swap file"
        exit 1
    }
    
    # Disable existing swap
    if swapon --show | grep -q "$swap_path"; then
        swapoff "$swap_path"
    fi
    
    # Create swap with safe permissions
    dd if=/dev/zero of="$swap_path" bs=1G count="$swap_size" status=progress
    chmod 600 "$swap_path"
    mkswap "$swap_path"
    
    # Test swap
    if ! swapon "$swap_path"; then
        log_error "Failed to activate swap"
        rm -f "$swap_path"
        exit 1
    fi
}

# Main setup function with error handling
main() {
    initialize_backup
    
    verify_jetson_environment
    check_system_resources
    check_running_services
    
    local DOCKER_ROOT="/mnt/docker"
    local SWAP_SIZE=16
    local SWAP_PATH="/mnt/16GB.swap"
    
    # Create directories if needed
    mkdir -p "$DOCKER_ROOT"
    
    # Perform setup steps with proper error handling
    if ! setup_docker_runtime "$DOCKER_ROOT"; then
        log_error "Docker setup failed"
        exit 1
    fi
    
    if ! setup_swap "$SWAP_SIZE" "$SWAP_PATH"; then
        log_error "Swap setup failed"
        exit 1
    fi
    
    log_info "Setup completed successfully"
    log_info "Backup and logs available at: $BACKUP_DIR"
}

# Execute main function
main