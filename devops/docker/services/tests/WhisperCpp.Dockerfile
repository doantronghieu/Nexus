FROM ubuntu:22.04

# Install dependencies
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
WORKDIR /app

# Clone the whisper.cpp repository
RUN git clone https://github.com/ggerganov/whisper.cpp.git .

# Build the project
RUN cmake -B build && \
    cmake --build build --config Release

# Set up model directory
RUN mkdir -p models

# Download a model (base.en by default)
RUN bash ./models/download-ggml-model.sh base.en

# Download samples using make
RUN make samples

# Set the default command to run a sample file
ENTRYPOINT ["./build/bin/whisper-cli"]
CMD ["-m", "./models/ggml-base.en.bin", "-f", "./samples/jfk.wav"]