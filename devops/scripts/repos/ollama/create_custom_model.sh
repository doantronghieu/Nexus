#!/bin/bash

# Ref: 
# - https://github.com/ollama/ollama/blob/main/docs/modelfile.md
# - https://huggingface.co/second-state
# source create_custom_model.sh

# Source the utils script
source ../../utils.sh

# Define the URL as a variable
MODEL_URL="https://huggingface.co/second-state/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q5_K_M.gguf"

# Extract MODEL_NAME from MODEL_URL
MODEL_NAME=$(basename "$MODEL_URL" .gguf)

# Find root path
root_path=$(find_root_path)

if [[ -z "$root_path" ]]; then
    echo "Error: Root path not found."
    exit 1
fi

# Define directories
target_dir="${root_path}/data/assets/repos/ollama/models"
modelfile_dir="${root_path}/data/assets/repos/ollama/Modelfiles"

# Create the target directory if it doesn't exist
mkdir -p "$target_dir"
mkdir -p "$modelfile_dir"

# Check if the model file already exists
model_file="${target_dir}/${MODEL_NAME}.gguf"
if [[ -f "$model_file" ]]; then
    echo "Model file already exists at ${model_file}. Skipping download."
else
    # Download the model file using the URL variable
    wget -P "$target_dir" "$MODEL_URL"

    if [ $? -eq 0 ]; then
        echo "Model downloaded successfully to ${target_dir}"
    else
        echo "Error downloading the model"
        exit 1
    fi
fi

# Define Modelfile path
modelfile_path="${modelfile_dir}/${MODEL_NAME}.Modelfile"

# Function to create Modelfile
create_modelfile() {
    cat << EOF > "$modelfile_path"
FROM ${model_file}
PARAMETER temperature 0.0
SYSTEM """You are a helpful AI assistant."""
EOF
    echo "Modelfile created at $modelfile_path"
}

# Function to prompt user for Modelfile modification
prompt_for_modification() {
    while true; do
        read -p "Do you want to modify the Modelfile? (y/n): " modify_choice
        case $modify_choice in
            [Yy]* )
                echo "Please modify the Modelfile at $modelfile_path"
                echo "Once you've finished modifying, press Enter to continue."
                read -p "Press Enter when you're done..."
                return 0
                ;;
            [Nn]* )
                return 1
                ;;
            * )
                echo "Please answer yes (y) or no (n)."
                ;;
        esac
    done
}

# Check if Modelfile exists
if [[ -f "$modelfile_path" ]]; then
    echo "Existing Modelfile detected at $modelfile_path"
    while true; do
        read -p "Do you want to use this existing Modelfile to create the model? (y/n): " use_existing
        case $use_existing in
            [Yy]* )
                break
                ;;
            [Nn]* )
                create_modelfile
                prompt_for_modification
                break
                ;;
            * )
                echo "Please answer yes (y) or no (n)."
                ;;
        esac
    done
else
    create_modelfile
    prompt_for_modification
fi

# Check Conda installation and set up environment
if check_conda_installed; then
    if initialize_conda; then
        deactivate_current_environment
        activate_dev_environment
        
        # Call the Python script to create the Ollama model
        python_script="${root_path}/devops/scripts/repos/ollama/create_ollama_model.py"
        python "$python_script" "$modelfile_path" "$MODEL_NAME"
        
        # Deactivate the environment after running the script
        deactivate_current_environment
    else
        echo "Failed to initialize Conda. Cannot proceed with environment activation."
        exit 1
    fi
else
    echo "Conda is required to activate the environment. Please install Conda and try again."
    exit 1
fi

# Print command to run the Ollama model
echo "To run the Ollama model, use:"
echo "ollama run $MODEL_NAME"

# You can use the URL variable here if needed
echo "Model URL: $MODEL_URL"
echo "Model Name: $MODEL_NAME"