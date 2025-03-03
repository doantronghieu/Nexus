
# https://docs.vllm.ai/en/latest/models/supported_models.html#supported-models

# jetson-containers run -it dustynv/vllm:0.6.3-r36.4.0
jetson-containers run -it dustynv/vllm:r36.4.0

vllm serve Qwen/Qwen2.5-0.5B-Instruct --gpu-memory-utilization 0.3 #--port 8768
vllm serve meta-llama/Llama-3.2-1B-Instruct --gpu-memory-utilization 0.3 --max-model-len 23744

vllm chat
vllm chat --url http://localhost:8768/v1

curl http://localhost:8768/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "prompt": "San Francisco is a",
        "max_tokens": 7,
        "temperature": 0
    }'

