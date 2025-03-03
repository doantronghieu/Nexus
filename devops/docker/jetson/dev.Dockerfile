# Start from the L4T ML base image
FROM nvcr.io/nvidia/l4t-ml:r36.2.0-py3

# xhost + 
# nvcr.io/nvidia/l4t-base:r36.2.0
# nvcr.io/nvidia/l4t-ml:r36.2.0-py3
# nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
# nvcr.io/nvidia/l4t-tensorrt:r8.6.2-ls
# nvcr.io/nvidia/l4t-tensorrt:r8.6.2-runtime
# nvcr.io/nvidia/l4t-cuda:12.2.12-devel
# nvcr.io/nvidia/l4t-cuda:12.2.12-runtime

# docker run -it --rm --net=host --runtime nvidia -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix nvcr.io/nvidia/l4t-ml:r36.2.0-py3

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

# # Install Miniconda
# ENV CONDA_DIR /opt/conda
# RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O ~/miniconda.sh && \
#     /bin/bash ~/miniconda.sh -b -p $CONDA_DIR && \
#     rm ~/miniconda.sh

# # Add conda to path
# ENV PATH $CONDA_DIR/bin:$PATH

# # Initialize conda for bash
# RUN conda init bash

# # Create a Python environment
# RUN conda create -n dev python=3.9 -y

# # Install common Python packages
# RUN /bin/bash -c "source $CONDA_DIR/bin/activate dev && \
#     conda install -y numpy pandas matplotlib scikit-learn jupyter && \
#     conda clean -afy "

# Set the default command to bash
CMD ["/bin/bash"]