#!/bin/bash

jetson-containers run \
  -e HUGGINGFACE_TOKEN=HF_API_KEY \
  -e FORCE_BUILD=on \
  dustynv/tensorrt_llm:0.12-r36.4.0 \
    /opt/TensorRT-LLM/llama.sh