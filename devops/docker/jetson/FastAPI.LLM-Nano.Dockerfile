# Use the base image
FROM dustynv/nano_llm:r36.2.0

# Install additional Python packages
RUN pip install fastapi uvicorn python-multipart docstring_parser rich httpx[http2]

# Set the working directory
WORKDIR /app

# Command to run the FastAPI application
CMD ["python3", "apps/services/jetson/FastAPI-LLM-Nano-Jetson.py"]
