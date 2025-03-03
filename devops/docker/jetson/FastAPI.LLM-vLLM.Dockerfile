# Use the base image
FROM dustynv/vllm:r36.4.0

# Install additional Python packages
RUN pip install fastapi uvicorn python-multipart docstring_parser rich httpx[http2] bitsandbytes triton

# Set the working directory
WORKDIR /app

# Set model name as environment variable
# ENV MODEL_NAME="Qwen/Qwen2.5-0.5B-Instruct"
ENV MODEL_NAME="meta-llama/Llama-3.2-1B-Instruct"

# Use shell form to ensure environment variable expansion
CMD vllm serve \
    $MODEL_NAME \
    --gpu-memory-utilization 0.3 \
    --port 8768 \
    --enable-auto-tool-choice \
    --tool-call-parser llama3_json