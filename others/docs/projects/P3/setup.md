# Development Environment Setup Guide

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
```

Install Rust toolchain:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
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

## Infrastructure Setup

Launch required Docker containers:

```bash
docker compose -f devops/docker/infra/docker-compose.yaml up -d
```

## Running

```bash
conda deactivate && conda activate dev
cd apps/services/llm/agents/p3
python server.py
```

```bash
cd front_end/Components
npm install
npm run dev
```