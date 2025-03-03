# IVyEdge Development Environment Setup Guide

## Table of Contents
- [Prerequisites](#prerequisites)
- [System Dependencies](#system-dependencies)
  - [Linux Installation](#linux-installation)
  - [MacOS Installation](#macos-installation)
  - [Common Dependencies](#common-dependencies)
- [Project Setup](#project-setup)
- [Infrastructure Setup](#infrastructure-setup)
- [Service Configuration](#service-configuration)
- [Validation](#validation)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before beginning the installation process, ensure you have:
- Administrator/sudo privileges on your system
- Stable internet connection
- At least 10GB of free disk space
- Git installed and configured

## System Dependencies

### Linux Installation

First, update your system packages:
```bash
sudo apt update -y
sudo apt upgrade -y
```

Install essential system packages:
```bash
# Install system utilities and development tools
sudo apt-get install -y \
    curl wget git-lfs cmake \
    portaudio19-dev python-all-dev \
    python3 python3-pip git-all tmux \
    libomp-dev tesseract-ocr libtesseract-dev

# Install snapd package manager
sudo apt install snapd

# Install multimedia tools
sudo snap install --edge ffmpeg
```

Install Node.js (v20.x):
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash - 
sudo apt-get install -y nodejs
```

Install Miniconda for Python environment management:
```bash
mkdir -p ~/miniconda3
ARCH=$(uname -m)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-${ARCH}.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

Install Docker and configure Docker Compose:
```bash
# Install Docker Compose
sudo mkdir -p /usr/local/lib/docker/cli-plugins
ARCH=$(uname -m)
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-${ARCH}" \
    -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Configure Docker permissions
sudo usermod -aG docker $USER
newgrp docker
exec su -l $USER

# Configure NVIDIA runtime for Docker
sudo sh -c 'cat <<EOF > /etc/docker/daemon.json
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "default-runtime": "nvidia"
}
EOF'

sudo systemctl restart docker
```

Install Rust toolchain:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

#### Jetson-specific Setup

For Jetson devices, additional setup is required:
```bash
# Clone and install Jetson containers
git clone https://github.com/dusty-nv/jetson-containers
bash jetson-containers/install.sh

# Run Ollama container
sudo jetson-containers run -d --name ollama dustynv/ollama:r36.4.0
```

### MacOS Installation

Install required packages using Homebrew:
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install core dependencies
brew install \
    wget git git-lfs cmake tmux \
    portaudio libomp python \
    docker-compose node tesseract

# Install applications
brew install --cask miniconda docker ollama
```

### Common Dependencies

Install Node Version Manager (nvm):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
```

Set up Python environment:
```bash
conda create --name dev python=3.11
```

## Project Setup

Install Python dependencies:
```bash
# Activate development environment
conda deactivate && conda activate dev

# Install development dependencies
pip install -r apps/requirements/dev.langchain.requirements.txt 

# Install core service dependencies
pip install -r apps/services/core.requirements.txt
```

## Service Configuration

Configure audio services:
```bash
# Configure Piper
chmod +x ./devops/docker/services/audio/piper.sh
./devops/docker/services/audio/piper.sh

# Configure Whisper
chmod +x ./devops/docker/services/audio/whisper_cpp.sh
./devops/docker/services/audio/whisper_cpp.sh
```

Data initialization: Run the setup notebook at `apps/services/projects/IvyEdge/setup.ipynb`

## Infrastructure Setup

Launch required Docker containers:

```bash
docker compose -f devops/docker/infra/docker-compose.yaml up -d
docker compose -f devops/docker/services.docker-compose.yaml up --build -d
docker compose -f devops/docker/apps/vehicle.docker-compose.yaml up --build -d
```

## Validation

### Service Testing

```bash
cd apps/services/SERVICE
conda deactivate && conda activate dev
python server.py
```

Access each service's UI at `http://localhost:PORT/ui` (PORT will be displayed in terminal)

### Application Testing

Test the LLM agent functionality using the development notebook:
`apps/services/llm/agents/vehicle/dev.ipynb`

## Troubleshooting

Common issues and solutions:

1. If Docker fails to start:
   - Ensure Docker daemon is running: `sudo systemctl status docker`
   - Check if user is in docker group: `groups $USER`

2. If Python packages fail to install:
   - Verify conda environment is active: `conda info --envs`
   - Update pip: `pip install --upgrade pip`

3. If services fail to start:
   - Check port availability: `netstat -tulpn`
   - Verify all Docker containers are running: `docker ps`
   - Check service logs: `docker logs <container_name>`

For additional support, consult the project documentation or open an issue in the repository.
