# Phase 1: Build whisper.cpp with Ubuntu base (same as test dockerfile)
FROM ubuntu:22.04 AS whisper-builder

# Install dependencies for whisper.cpp
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    ffmpeg \
    libsdl2-dev \
    pkg-config \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /whisper-build

# Clone the whisper.cpp repository
RUN git clone https://github.com/ggerganov/whisper.cpp.git .

# Build the project
RUN cmake -B build && \
    cmake --build build --config Release

# Download models
RUN mkdir -p models && \
    cd models && \
    wget -O ggml-tiny.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin && \
    wget -O ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin

# Verify CLI works by testing
RUN cd samples && \
    wget -O jfk.wav https://github.com/ggerganov/whisper.cpp/raw/master/samples/jfk.wav && \
    cd .. && \
    ./build/bin/whisper-cli -m models/ggml-base.en.bin -f samples/jfk.wav

# Phase 2: Python environment on Ubuntu
FROM ubuntu:22.04 AS build

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-dev \
    python3-pip \
    build-essential \
    ffmpeg \
    libportaudio2 \
    libasound2-dev \
    portaudio19-dev \
    libsndfile1 \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app/apps

# Copy the requirements file and install dependencies
COPY apps/services/audio/speech_to_text/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/services/core.requirements.txt .
RUN pip install --no-cache-dir -r core.requirements.txt

COPY apps/services/audio/audio.requirements.txt .
RUN pip install --no-cache-dir -r audio.requirements.txt

# Copy the application code
COPY apps .

# Create directory for whisper assets
RUN mkdir -p /app/apps/services/audio/speech_to_text/impl/assets/whisper.cpp

# Copy the built whisper.cpp from the first phase
COPY --from=whisper-builder /whisper-build/ /app/apps/services/audio/speech_to_text/impl/assets/whisper.cpp/

# Phase 3: Production environment
FROM ubuntu:22.04

# Install Python and runtime dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    libportaudio2 \
    libasound2 \
    ffmpeg \
    libsndfile1 \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the working directory
WORKDIR /apps

# Create a non-root user for security
RUN adduser --disabled-password --no-create-home app

# Copy the virtual environment from the build stage
COPY --from=build /opt/venv /opt/venv
 
# Copy the application code and built whisper.cpp from the build stage
COPY --from=build /app/apps /apps

# Copy whisper shared libraries to system library path and update cache
RUN mkdir -p /usr/local/lib && \
    find /apps/services/audio/speech_to_text/impl/assets/whisper.cpp/build -name "*.so*" -exec cp {} /usr/local/lib/ \; && \
    cd /usr/local/lib && \
    for f in libwhisper.so*; do ln -sf $f ${f}.1 2>/dev/null || true; done && \
    ldconfig

# Create necessary directories
RUN mkdir -p /tmp/stt_service && \
    chown -R app:app /tmp/stt_service

# Expose the port
EXPOSE 8000

# Set the working directory
WORKDIR /apps/services/audio/speech_to_text/

# Run the Python server
CMD ["python3", "server.py"]