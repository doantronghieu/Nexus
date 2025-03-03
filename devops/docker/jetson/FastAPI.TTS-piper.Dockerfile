FROM dustynv/piper-tts:r36.2.0

# Install additional Python packages
RUN pip install fastapi uvicorn python-multipart python-dotenv loguru

# Set the working directory
WORKDIR /app

# We don't need to copy files here as we'll mount the entire directory structure

# Command to run the FastAPI application
CMD ["python3", "apps/services/jetson/FastAPI-TTS-Piper-Jetson.py"]