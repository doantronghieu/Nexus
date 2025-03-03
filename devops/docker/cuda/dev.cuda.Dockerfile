# Start from the CUDA base image
# https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md

# For Jetson
# https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-base/tags

# devel | runtime
FROM nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04 as base
# FROM nvidia/cuda:12.2.0-devel-ubuntu22.04 as base
# 12.2.2-devel-ubuntu22.04 | 12.2.2-cudnn8-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    git \
    vim \
    portaudio19-dev \
    ffmpeg \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \
    cmake \
    build-essential \
    tmux \
    libasound-dev \
    libportaudio2 \
    libportaudiocpp0 \
    libsox-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh

# Add conda to path
ENV PATH $CONDA_DIR/bin:$PATH

# Initialize conda for bash
RUN conda init bash

# Create a Python environment
RUN conda create -n dev python=3.12 -y

# Install common Python packages
RUN /bin/bash -c "source $CONDA_DIR/bin/activate dev && \
    conda install -y numpy pandas matplotlib scikit-learn jupyter && \
    conda clean -afy "

# Set the default command to bash
CMD ["/bin/bash"]