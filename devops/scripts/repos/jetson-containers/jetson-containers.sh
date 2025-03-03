#!/bin/bash
 
# https://github.com/dusty-nv/jetson-containers/tree/master

sudo git config --global --add safe.directory /home/aic/jetson-containers
jetson-containers update

# vLLM
jetson-containers run dustynv/vllm:r36.4.0
vllm serve meta-llama/Llama-3.2-1B --dtype auto --api-key token-abc123

# llama.cpp
jetson-containers run dustynv/llama_cpp:r36.4.0