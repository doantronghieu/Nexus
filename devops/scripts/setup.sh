#!/bin/bash

set -euo pipefail  # Exit on error, unset variable, and pipe failure

# Get the root directory (Embedded-AI)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." &> /dev/null && pwd)"

source "$ROOT_DIR/devops/scripts/install/uv.sh"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >&2
}

# Error handling function
error() {
    log "ERROR: $1"
    exit 1
}

# Function to prompt for sudo password
prompt_sudo() {
    if ! sudo -n true 2>/dev/null; then
        log "Sudo access required. Please enter your password:"
        sudo -v || error "Failed to obtain sudo access."
    fi
    sudo -v  # Refresh sudo timeout
}

# Function to check if Homebrew is installed
check_homebrew() {
    if ! command -v brew &> /dev/null; then
        log "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || error "Failed to install Homebrew"
    else
        log "Homebrew is already installed"
    fi
}

# Function to make all .sh files in a directory and its subdirectories executable
make_executable() {
    log "Making all .sh files in $1 and its subdirectories executable..."
    find "$1" -type f -name "*.sh" -print0 | xargs -0 -I {} chmod +x {} || error "Failed to make scripts executable"
}

# Function to check if a package might trigger GRUB updates
check_grub_related_package() {
    local package=$1
    local grub_related_packages=(
        "linux-image"
        "linux-headers"
        "grub"
        "grub-common"
        "grub-pc"
        "grub-efi"
        "grub2"
        "linux-generic"
        "linux-modules"
    )

    # Check if package name contains any of the grub-related keywords
    for grub_pkg in "${grub_related_packages[@]}"; do
        if [[ "$package" == *"$grub_pkg"* ]]; then
            return 0  # Found a match
        fi
    done
    return 1  # No match found
}

# Function to install a single package and return status
install_package() {
    local package=$1
    local os_type=$2
    log "Installing $package..."

    case "$os_type" in
        darwin*)
            if ! HOMEBREW_NO_AUTO_UPDATE=1 brew install "$package" 2>/dev/null; then
                if ! HOMEBREW_NO_AUTO_UPDATE=1 brew upgrade "$package" 2>/dev/null; then
                    log "Failed to install $package."
                    return 1
                fi
            fi
            ;;
        linux-gnu*)
            # Check for GRUB-related dependencies
            local deps
            deps=$(apt-cache depends "$package" 2>/dev/null | grep -i "grub")
            if [ -n "$deps" ]; then
                log "Warning: $package has GRUB-related dependencies:"
                echo "$deps"
                read -p "Do you want to install this package? (y/N) " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    return 1
                fi
            fi

            if ! sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "$package"; then
                log "Failed to install $package."
                return 1
            fi
            ;;
        *)
            log "Unsupported operating system for package installation: $os_type"
            return 1
            ;;
    esac
}

# Function to install packages for macOS
install_packages_macos() {
    log "Updating Homebrew..."
    HOMEBREW_NO_AUTO_UPDATE=1 brew update || error "Failed to update Homebrew"

    local packages=(
        "ollama"
        "portaudio"
        "wget"
        "ffmpeg"
        "tesseract"
        "libomp"
        "cmake"
        "node"
        "docker"
        "docker-compose"
    )

    local failed_packages=()

    for package in "${packages[@]}"; do
        if ! install_package "$package" "darwin"; then
            failed_packages+=("$package")
        fi
    done

    if [ ${#failed_packages[@]} -eq 0 ]; then
        log "All packages installed successfully."
    else
        error "Failed to install packages: ${failed_packages[*]}"
    fi
}

# Function to install packages for Linux
install_packages_linux() {
    sudo DEBIAN_FRONTEND=noninteractive apt-get update || error "Failed to update apt"

    sudo apt-get clean
    sudo apt-get update
    sudo apt-get install -f

    local packages=(
        "build-essential"
        "tmux"
        "libasound-dev"
        "portaudio19-dev"
        "wget"
        "ffmpeg"
        "tesseract-ocr"
        "libtesseract-dev"
        "tesseract-ocr-eng"
        "cmake"
        "libportaudio2"
        "libportaudiocpp0"
        "libsox-dev"
        "libsdl2-dev"
        "libspeexdsp-dev"
    )

    local failed_packages=()
    local grub_related=()

    # First, check for GRUB-related packages
    for package in "${packages[@]}"; do
        if check_grub_related_package "$package"; then
            grub_related+=("$package")
        fi
    done

    # If GRUB-related packages are found, warn the user
    if [ ${#grub_related[@]} -gt 0 ]; then
        log "Warning: The following packages might trigger GRUB updates:"
        printf '%s\n' "${grub_related[@]}"
        read -p "Do you want to continue with installation? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error "Installation aborted by user"
        fi
    fi

    for package in "${packages[@]}"; do
        if ! install_package "$package" "linux-gnu"; then
            failed_packages+=("$package")
        fi
    done

    if [ ${#failed_packages[@]} -eq 0 ]; then
        log "All packages installed successfully."
    else
        error "Failed to install packages: ${failed_packages[*]}"
    fi
}

# Function to clean up unnecessary packages
cleanup_packages() {
    log "Cleaning up unnecessary packages..."
    case "$OSTYPE" in
        darwin*)
            HOMEBREW_NO_AUTO_UPDATE=1 brew cleanup -s || log "Warning: Failed to cleanup Homebrew packages"
            HOMEBREW_NO_AUTO_UPDATE=1 brew autoremove || log "Warning: Failed to remove unnecessary Homebrew packages"
            ;;
        linux-gnu*)
            sudo apt autoremove -y || log "Warning: Failed to remove unnecessary packages"
            ;;
    esac
}

# Function to upgrade available packages
upgrade_packages() {
    log "Checking for available package upgrades..."
    case "$OSTYPE" in
        darwin*)
            HOMEBREW_NO_AUTO_UPDATE=1 brew upgrade || log "Warning: Failed to upgrade Homebrew packages"
            ;;
        linux-gnu*)
            # Get list of upgradable packages excluding GRUB and kernel-related packages
            local upgrade_list=$(apt list --upgradable 2>/dev/null | grep -vE 'linux-|grub')
            
            if [ -n "$upgrade_list" ]; then
                log "Installing non-GRUB updates..."
                # Create a temporary file to store package names
                local tmp_file=$(mktemp)
                
                # Extract package names and exclude GRUB/kernel packages
                apt list --upgradable 2>/dev/null | 
                    grep -vE 'linux-|grub' | 
                    cut -d'/' -f1 > "$tmp_file"
                
                # Read and upgrade packages one by one
                while IFS= read -r package; do
                    if [ -n "$package" ]; then
                        log "Upgrading $package..."
                        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --only-upgrade "$package" || \
                            log "Warning: Failed to upgrade $package"
                    fi
                done < "$tmp_file"
                
                # Cleanup
                rm -f "$tmp_file"
            else
                log "No non-GRUB updates available."
            fi
            ;;
    esac
}

# Function to check if a package is GRUB or kernel-related
is_grub_related() {
    local package=$1
    echo "$package" | grep -qE 'linux-|grub|libc-dev'
}

# Function to check if Miniconda is installed
check_miniconda() {
    if command -v conda >/dev/null 2>&1; then
        local conda_version
        conda_version=$(conda --version 2>&1)
        if [[ $conda_version =~ ^conda[[:space:]]+[0-9]+\.[0-9]+\.[0-9]+ ]]; then
            log "Conda is installed and functioning. Version: $conda_version"
            return 0
        else
            log "Conda command exists but returned unexpected output: $conda_version"
            return 1
        fi
    else
        log "Conda is not installed or not in PATH."
        return 1
    fi
}

# Function to create and configure conda environment
create_conda_environment() {
    log "Creating conda environment 'dev' with Python 3.11..."

    # Check if environment already exists
    if conda info --envs | grep -q "^dev "; then
        log "Environment 'dev' already exists. Skipping creation."
        return 0
    fi

    # Create new environment with Python 3.11
    if ! conda create -y -n dev python=3.11; then
        error "Failed to create conda environment 'dev'"
    fi

    log "Conda environment 'dev' created successfully"
}

# Function to install and configure Git LFS
install_git_lfs() {
    log "Installing Git LFS..."

    # First try conda installation
    if command -v conda >/dev/null 2>&1; then
        log "Installing Git LFS via conda-forge..."
        if ! conda install -y -c conda-forge git-lfs; then
            log "Failed to install Git LFS via conda. Falling back to system package manager..."
        fi
    fi

    # Verify Git LFS installation or try system package manager
    if ! command -v git-lfs >/dev/null 2>&1; then
        case "$OSTYPE" in
            darwin*)
                install_package "git-lfs" "darwin" || error "Failed to install Git LFS via Homebrew"
                ;;
            linux-gnu*)
                install_package "git-lfs" "linux-gnu" || error "Failed to install Git LFS via apt"
                ;;
        esac
    fi

    # Initialize Git LFS
    log "Initializing Git LFS..."
    git lfs install || error "Failed to initialize Git LFS"

    # Verify installation
    if command -v git-lfs >/dev/null 2>&1; then
        local git_lfs_version
        git_lfs_version=$(git lfs version)
        log "Git LFS installed and initialized successfully. Version: $git_lfs_version"
    else
        error "Git LFS installation verification failed"
    fi
}

# Function to add Miniconda to PATH permanently
add_miniconda_to_path() {
    local miniconda_dir="$HOME/miniconda3"
    local shell_config

    # Determine the appropriate shell configuration file
    if [[ -f "$HOME/.zshrc" ]]; then
        shell_config="$HOME/.zshrc"
    elif [[ -f "$HOME/.bashrc" ]]; then
        shell_config="$HOME/.bashrc"
    else
        log "Warning: Unable to determine shell configuration file. Manual PATH adjustment may be necessary."
        return 1
    fi

    # Check if Miniconda path is already in the config file
    if grep -q "$miniconda_dir/bin" "$shell_config"; then
        log "Miniconda is already in PATH."
        return 0
    fi

    # Add Miniconda to PATH
    {
        echo ""
        echo "# Miniconda"
        echo "export PATH=\"$miniconda_dir/bin:\$PATH\""
    } >> "$shell_config"

    log "Added Miniconda to PATH in $shell_config"

    # Initialize conda for shell interaction
    "$miniconda_dir/bin/conda" init "$(basename "$SHELL")" || log "Warning: Failed to initialize conda for shell"
}

# Function to disable Conda base environment auto-activation
disable_conda_auto_activate() {
    log "Disabling Conda base environment auto-activation..."
    if conda config --set auto_activate_base false; then
        log "Conda base environment auto-activation has been disabled."
    else
        log "Warning: Failed to disable Conda base environment auto-activation."
    fi
}

# Function to install Miniconda on macOS
install_miniconda_macos() {
    if check_miniconda; then
        log "Skipping Miniconda installation as it's already installed."
        add_miniconda_to_path
        disable_conda_auto_activate
        return 0
    fi

    log "Installing Miniconda..."
    local miniconda_dir="$HOME/miniconda3"
    local miniconda_installer="$miniconda_dir/miniconda.sh"

    rm -rf "$miniconda_dir"
    mkdir -p "$miniconda_dir" || error "Failed to create Miniconda directory"

    local arch
    arch=$(uname -m)
    local miniconda_url
    case "$arch" in
        x86_64) miniconda_url="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh" ;;
        arm64) miniconda_url="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh" ;;
        *) error "Unsupported architecture: $arch" ;;
    esac

    curl -L "$miniconda_url" -o "$miniconda_installer" || error "Failed to download Miniconda"
    bash "$miniconda_installer" -b -u -p "$miniconda_dir" || error "Failed to install Miniconda"
    rm "$miniconda_installer"

    # Add Miniconda to PATH for the current session
    export PATH="$miniconda_dir/bin:$PATH"

    log "Miniconda installed successfully."
    conda --version || log "Warning: Unable to verify Conda version after installation"

    add_miniconda_to_path
    disable_conda_auto_activate
}

# Function to install Miniconda on Linux
install_miniconda_linux() {
    if check_miniconda; then
        log "Skipping Miniconda installation as it's already installed."
        add_miniconda_to_path
        disable_conda_auto_activate
        return 0
    fi

    log "Installing Miniconda..."
    local miniconda_dir="$HOME/miniconda3"
    local miniconda_installer="$miniconda_dir/miniconda.sh"

    rm -rf "$miniconda_dir"
    mkdir -p "$miniconda_dir" || error "Failed to create Miniconda directory"

    local arch
    arch=$(uname -m)
    local miniconda_url
    case "$arch" in
        x86_64) miniconda_url="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" ;;
        aarch64) miniconda_url="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh" ;;
        *) error "Unsupported architecture: $arch" ;;
    esac

    wget "$miniconda_url" -O "$miniconda_installer" || error "Failed to download Miniconda"
    bash "$miniconda_installer" -b -u -p "$miniconda_dir" || error "Failed to install Miniconda"
    rm "$miniconda_installer"

    # Add Miniconda to PATH for the current session
    export PATH="$miniconda_dir/bin:$PATH"

    log "Miniconda installed successfully."
    conda --version || log "Warning: Unable to verify Conda version after installation"

    add_miniconda_to_path
    disable_conda_auto_activate
}

# Function to install Node.js and npm for macOS
install_node_macos() {
    log "Checking Node.js installation..."
    if ! command -v node &> /dev/null; then
        if ! install_package "node" "darwin"; then
            error "Failed to install Node.js"
        fi
    else
        log "Node.js is already installed. Checking for updates..."
        HOMEBREW_NO_AUTO_UPDATE=1 brew upgrade node || log "Note: Node.js is up to date"
    fi

    # Verify Node.js installation
    if command -v node >/dev/null 2>&1; then
        local node_version
        node_version=$(node --version)
        log "Node.js installed successfully. Version: $node_version"

        # Verify npm installation
        local npm_version
        npm_version=$(npm --version)
        log "npm installed successfully. Version: $npm_version"

        # Install Nuxt globally
        log "Installing Nuxt globally..."
        if npm install -g nuxt; then
            local nuxt_version
            nuxt_version=$(npx nuxt --version 2>/dev/null || echo "unknown")
            log "Nuxt installed successfully. Version: $nuxt_version"
        else
            error "Failed to install Nuxt globally"
        fi
    else
        error "Node.js installation failed or Node.js is not in PATH."
    fi
}

# Function to install NVM and Node.js for Linux
install_nvm_and_nodejs_linux() {
    log "Checking system memory..."
    local available_memory
    available_memory=$(free -m | awk '/^Mem:/{print $7}')
    log "Available memory: ${available_memory}MB"

    # Ensure at least 1GB of available memory
    if [ "${available_memory}" -lt 1024 ]; then
        log "Warning: Low memory detected. Cleaning system caches..."
        sync && echo 3 | sudo tee /proc/sys/vm/drop_caches >/dev/null
    fi

    log "Purging existing Node.js installation..."
    sudo apt-get purge --auto-remove nodejs || error "Failed to purge existing Node.js installation"

    log "Installing NVM (Node Version Manager)..."
    # Download NVM installation script to verify it first
    local nvm_script="/tmp/nvm-install.sh"
    curl -o "$nvm_script" https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh || error "Failed to download NVM installation script"
    bash "$nvm_script" || error "Failed to install NVM"
    rm -f "$nvm_script"

    # Load NVM with error checking
    export NVM_DIR="$HOME/.nvm"
    if [ ! -s "$NVM_DIR/nvm.sh" ]; then
        error "NVM installation files not found"
    fi
    source "$NVM_DIR/nvm.sh" || error "Failed to source NVM script"

    # Verify NVM installation
    if ! command -v nvm >/dev/null 2>&1; then
        error "NVM installation failed or NVM is not in PATH"
    fi
    log "NVM installed successfully."

    # Install LTS version with memory monitoring
    log "Installing Node.js LTS version..."
    local node_install_cmd="nvm install --lts"
    if [ "${available_memory}" -lt 1024 ]; then
        # Use Node.js 16 LTS for lower memory systems
        node_install_cmd="nvm install lts/gallium" # Node.js 16 LTS
        log "Low memory system detected - installing Node.js 16 LTS for better compatibility"
    fi
    
    eval "$node_install_cmd" || error "Failed to install Node.js LTS version"
    nvm use --lts || error "Failed to set Node.js LTS version as default"

    # Verify Node.js installation
    if ! command -v node >/dev/null 2>&1; then
        error "Node.js installation failed or Node.js is not in PATH"
    fi
    
    local node_version
    node_version=$(node --version)
    log "Node.js installed successfully. Version: $node_version"

    # Configure Node.js for limited resources
    echo "max-old-space-size=512" > "$NVM_DIR/default-packages"

    # Install Nuxt with memory limits
    log "Installing Nuxt globally with memory limits..."
    if NODE_OPTIONS="--max-old-space-size=512" npm install -g nuxt; then
        local nuxt_version
        nuxt_version=$(NODE_OPTIONS="--max-old-space-size=512" npx nuxt --version 2>/dev/null || echo "unknown")
        log "Nuxt installed successfully. Version: $nuxt_version"
    else
        error "Failed to install Nuxt globally"
    fi
}

setup_docker_directories() {
    local docker_data_path="$ROOT_DIR/data/docker"
    log "Setting up Docker data directories in $docker_data_path"

    # First ensure the parent directories exist
    mkdir -p "$ROOT_DIR/data" || error "Failed to create Data directory"

    # Remove existing docker directory if it exists
    if [ -d "$docker_data_path" ]; then
        log "Removing existing Docker data directory..."
        rm -rf "$docker_data_path" || error "Failed to remove existing Docker data directory"
    fi

    # Create main docker directory
    mkdir -p "$docker_data_path" || error "Failed to create Docker data directory"

    # Define the list of required directories
    local directories=(
        "mongodb"
        "ollama"
        "postgres"
        "qdrant"
        "redis"
        "redisinsight"
    )

    # Create each directory and set appropriate permissions
    for dir in "${directories[@]}"; do
        local full_path="$docker_data_path/$dir"
        mkdir -p "$full_path" || error "Failed to create $dir directory"
        
        # Set permissions (adjust if needed for your specific use case)
        chmod 755 "$full_path" || error "Failed to set permissions for $dir directory"
        
        log "Created directory: $full_path"
    done

    # Verify all directories were created successfully
    local missing_dirs=()
    for dir in "${directories[@]}"; do
        if [ ! -d "$docker_data_path/$dir" ]; then
            missing_dirs+=("$dir")
        fi
    done

    if [ ${#missing_dirs[@]} -eq 0 ]; then
        log "All Docker data directories created successfully"
    else
        error "Failed to verify creation of directories: ${missing_dirs[*]}"
    fi
}



# Main execution
main() {
    log "Starting setup..."
    log "Root directory: $ROOT_DIR"
    make_executable "$ROOT_DIR"

    prompt_sudo
    setup_docker_directories
    
    case "$OSTYPE" in
        darwin*)
            log "Detected macOS system"
            check_homebrew
            install_packages_macos
            install_node_macos
            install_miniconda_macos
            create_conda_environment
            install_git_lfs
            install_uv
            cleanup_packages
            upgrade_packages
            ;;
        linux-gnu*)
            log "Detected Linux system"
            install_packages_linux
            install_miniconda_linux
            create_conda_environment
            install_nvm_and_nodejs_linux
            install_git_lfs
            install_uv
            cleanup_packages
            upgrade_packages
            ;;
        *)
            error "Unsupported operating system: $OSTYPE"
            ;;
    esac

    log "Setup completed successfully."
    log "Node.js, npm, Nuxt, Git LFS, and Miniconda have been installed."
    log "You can verify the installations with:"
    log "  node --version"
    log "  npm --version"
    log "  npx nuxt --version"
    log "  git lfs version"
    log "  conda --version"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        log "To use Miniconda in this session, please run: source $HOME/.zshrc (or .bashrc if you use bash)"
        log "To activate the dev environment, use 'conda activate dev'"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        log "To use Miniconda and NVM in this session, please run: source $HOME/.bashrc (or .zshrc if you use zsh)"
        log "To activate the dev environment, use 'conda activate dev'"
        log "To use a specific Node.js version, use 'nvm use <version>'"
    fi

    log "Miniconda will be available in all new terminal sessions automatically."
}

main