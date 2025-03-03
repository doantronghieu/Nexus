#!/bin/bash

find_root_path() {
    # Start from current directory and search upwards
    local current_dir="${PWD}"
    
    while [[ "$current_dir" != "/" ]]; do
        # Check for both apps and devops directories
        if [[ -d "$current_dir/apps" && -d "$current_dir/devops" ]]; then
            echo "$current_dir"
            return 0
        fi
        current_dir=$(dirname "$current_dir")
    done
    
    # If we reach here, no valid root was found
    echo "Error: Could not find project root directory (looking for apps/ and devops/)" >&2
    return 1
}

get_root_dir() {
    find_root_path
    return $?
}

#*------------------------------------------------------------------------------
check_and_activate_conda_env() {
    # First try to get conda root from environment variable
    if [[ -n "${CONDA_EXE:-}" ]]; then
        CONDA_ROOT=$(dirname $(dirname "$CONDA_EXE"))
        CONDA_SH="$CONDA_ROOT/etc/profile.d/conda.sh"
    else
        # Try to find conda root from the conda function
        CONDA_ROOT=$(conda info --base 2>/dev/null)
        if [[ $? -eq 0 ]]; then
            CONDA_SH="$CONDA_ROOT/etc/profile.d/conda.sh"
        fi
    fi

    if [[ ! -f "$CONDA_SH" ]]; then
        echo "Error: Unable to find conda.sh"
        echo "Conda root appears to be: $CONDA_ROOT"
        echo "Please ensure conda is properly initialized"
        return 1
    fi

    echo "Found conda.sh at: $CONDA_SH"
    . "$CONDA_SH"

    # Check for current conda environment with safe variable expansion
    local current_env="${CONDA_DEFAULT_ENV:-}"
    
    if [[ -z "$current_env" ]]; then
        echo "No conda environment is currently active."
        if conda env list | grep -q "dev"; then
            echo "Attempting to activate 'dev' environment..."
            if conda activate dev; then
                echo "Successfully activated 'dev' environment."
                return 0
            else
                echo "Error: Failed to activate 'dev' environment."
                return 1
            fi
        else
            echo "Error: 'dev' environment does not exist."
            return 1
        fi
    elif [[ "$current_env" != "dev" ]]; then
        echo "Current conda environment is '$current_env', not 'dev'."
        echo "Attempting to switch to 'dev' environment..."
        if conda activate dev; then
            echo "Successfully switched to 'dev' environment."
            return 0
        else
            echo "Error: Failed to switch to 'dev' environment."
            return 1
        fi
    else
        echo "Conda environment 'dev' is already active."
        return 0
    fi
}

#*------------------------------------------------------------------------------

# Function to check if Conda is installed
check_conda_installed() {
    if command -v conda &> /dev/null; then
        echo "Conda is installed."
        return 0
    else
        echo "Conda is not installed."
        return 1
    fi
}

# Function to initialize Conda
initialize_conda() {
    # Determine the path to conda.sh
    if [[ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]]; then
        CONDA_SH="$HOME/miniconda3/etc/profile.d/conda.sh"
    elif [[ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]]; then
        CONDA_SH="$HOME/anaconda3/etc/profile.d/conda.sh"
    else
        echo "Could not find conda.sh. Please ensure Conda is properly installed."
        return 1
    fi

    # Source conda.sh to initialize Conda
    source "$CONDA_SH"
    if [[ $? -ne 0 ]]; then
        echo "Failed to initialize Conda."
        return 1
    fi
    echo "Conda initialized."
    return 0
}

# Function to deactivate current Conda environment
deactivate_current_environment() {
    if [[ -n $CONDA_DEFAULT_ENV ]]; then
        echo "Deactivating current environment: $CONDA_DEFAULT_ENV"
        conda deactivate
        echo "Environment deactivated."
    else
        echo "No active Conda environment to deactivate."
    fi
}

# Function to activate the 'dev' environment
activate_dev_environment() {
    if conda env list | grep -q "dev"; then
        echo "Activating 'dev' environment..."
        conda activate dev
        if [[ $CONDA_DEFAULT_ENV == "dev" ]]; then
            echo "'dev' environment activated."
        else
            echo "Failed to activate 'dev' environment."
        fi
    else
        echo "The 'dev' environment does not exist. Please create it first."
    fi
}

# Main script execution
# if check_conda_installed; then
#     if initialize_conda; then
#         deactivate_current_environment
#         activate_dev_environment
#         echo "Script execution completed. Current environment: $CONDA_DEFAULT_ENV"
#         echo "To apply these changes to your current shell, run this script with 'source utils.sh'"
#     else
#         echo "Failed to initialize Conda. Cannot proceed with environment activation."
#     fi
# else
#     echo "Conda is required to activate the environment. Please install Conda and try again."
# fi