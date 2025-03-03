# Setup Guide

[← Back to Main Documentation](../../../../README.md)

## Legend

- ℹ️ Information only
- 🙅 Optional setup steps
- ⚙️ Required setup steps

## ⚙️ Initial Setup

Execute the general setup script. This script works for macOS and Linux:

```bash
source ./devops/scripts/setup.sh
```

Based on the `apps/.env.example` file, create the `apps/.env` file.

## ⚙️ Python Environment Setup

Configure the Python environment using Conda:

```bash
conda deactivate
conda activate dev
pip install --upgrade -r apps/requirements/dev.requirements.txt
```

## ⚙️ SSH Port Forwarding

When accessing services via SSH, run the following command on your local machine:

```bash
# Configure SSH tunnel for local access to remote services:
# Service Ports:
# - Database Services:
#   - MongoDB: 27017
#   - Redis: 6379
#   - Qdrant: 6335
# - API Services:
#   - FastAPI: 8000, 8765
#   - Custom Service: 5540, 8769
# - Web Services:
#   - Kafka UI: 9021
#   - Streamlit: 8501
#   - Nuxt.js: 3000
ssh -L 27017:localhost:27017 \
    -L 6379:localhost:6379 \
    -L 5540:localhost:5540 \
    -L 8000:localhost:8000 \
    -L 6335:localhost:6335 \
    -L 8765:localhost:8765 \
    -L 8769:localhost:8769 \
    -L 3000:localhost:3000 \
    -L 8501:localhost:8501 \
    -L 9021:localhost:9021 \
    hieudt71@jarvis-clone.servebeer.com \
    -p 2020
```

## 🙅 NVIDIA Jetson Setup

Refer to the Jetson environment setup script at [devops/scripts/setup/jetson.sh](./devops/scripts/setup/jetson.sh).

**Note**: This setup should be performed only once per device. Multiple executions may cause system conflicts.

## Other

Search for `[SETUP] IvyEdge` in the codebase and run all instances (Jupyter Notebook cells, files, ...) that contain this keyword.

## 🙅 External Dependencies

Clone required external repositories:

```bash
mkdir -p others/repos

# Machine Learning & Audio Processing
git clone https://github.com/vllm-project/vllm.git others/repos/vllm
git clone https://github.com/ufal/whisper_streaming.git others/repos/whisper_streaming
git clone https://github.com/ggerganov/whisper.cpp others/repos/whisper.cpp
git clone https://github.com/collabora/WhisperLive.git others/repos/WhisperLive
git clone https://github.com/NVIDIA-AI-IOT/whisper_trt.git others/repos/whisper_trt
git clone https://github.com/NVIDIA-AI-IOT/torch2trt.git others/repos/whisper_trt/torch2trt
git clone https://github.com/fishaudio/fish-speech others/repos/fish-speech
git clone https://github.com/rhasspy/piper.git others/repos/piper
```

## ℹ️ Service Management

Reference documentation for service configuration and deployment:

- `devops/mks/services.mk`
- `Makefile`
- `devops/docker/docker-compose.yaml`

Common service management commands:

```bash
make            # Display available commands
make start      # Launch all Docker services
make start jetson # Launch Jetson-specific services
```

Manual service deployment:

```bash
docker compose -f devops/docker/servers.docker-compose.yaml up --build --detach
docker compose -f devops/docker/services.docker-compose.yaml up --build --detach
```

## ℹ️ MongoDB Configuration

Connection string:

```text
mongodb://root:example@localhost:27017/?authSource=admin
```

Essential MongoDB commands:

```bash
show dbs                               # List databases
use <database_name>                    # Select database
show collections                       # List collections
db.<collection_name>.find().pretty()   # Display collection contents
```

## ⚙️ Data Ingestion

For data ingestion procedures, refer to the Jupyter notebook at:
- `apps/dev/frameworks/LlamaIndex/data.ipynb` (Old version 🙅‍♂️)
- `apps/services/projects/IvyEdge/setup.ipynb`

## Misc 🙅‍♂️

### MacOs

```bash
brew install --cask ollama
```

### Linux

```bash

```
