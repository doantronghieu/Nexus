#!/bin/bash

# Ref
# 
# 

#*------------------------------------------------------------------------------
source ../../utils.sh

#*------------------------------------------------------------------------------
check_and_activate_conda_env

if sudo pip show huggingface_hub > /dev/null 2>&1; then
    echo "huggingface_hub is already installed."
else
    echo "huggingface_hub is not installed. Installing now..."
    sudo pip install huggingface_hub
fi

#*------------------------------------------------------------------------------

# cd devops/scripts/repos/mlc

# Set the root path
ROOT_PATH="/"

# Set the models and libs directory paths
MODELS_DIR="${ROOT_PATH}/dist/models"
MODELS_MLC_DIR="${ROOT_PATH}/dist/models-MLC"
LIBS_DIR="${ROOT_PATH}/dist/libs"

# Download model
REPO_ID="microsoft/Phi-3-mini-128k-instruct"
MODEL_PATH="${MODELS_DIR}/${REPO_ID}"
MODEL_MLC_PATH="${MODELS_MLC_DIR}/${REPO_ID}"

# Create directories
sudo mkdir -p "$MODELS_DIR" "$LIBS_DIR" "$MODELS_MLC_DIR" "$MODEL_MLC_PATH"

sudo -E python download_HF_safetensors.py $REPO_ID

# The path where the model resides locally.
export LOCAL_MODEL_PATH=$MODEL_PATH
# The path where to place the model processed by MLC.
export MLC_MODEL_PATH=$MODELS_MLC_DIR
# The choice of quantization: q4f16_1, q4f16_ft
# https://github.com/mlc-ai/mlc-llm/blob/main/python/mlc_llm/quantization/quantization.py#L30
export QUANTIZATION=q4f16_1
# The choice of conversation template.
# https://github.com/mlc-ai/mlc-llm/blob/main/python/mlc_llm/interface/gen_config.py#L261
export CONV_TEMPLATE=phi-3

# mlc_llm gen_config $LOCAL_MODEL_PATH \
#     --quantization $QUANTIZATION \
#     --conv-template $CONV_TEMPLATE \
#     -o $MLC_MODEL_PATH

# mlc_llm convert_weight $LOCAL_MODEL_PATH \
#   --quantization $QUANTIZATION \
#   -o $MLC_MODEL_PATH

# source deploy_custom_model.sh