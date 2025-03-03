# Stream Service Documentation

## Overview
This document outlines the setup and running procedures for the Stream Service, a system that combines video streaming capabilities with machine learning processing.

## Prerequisites

### Required Software
- Python 3.11
- Conda Package Manager
- Node.js and NPM
- Nuxt.js Framework
- ngrok for Tunnel Management
- nginx Web Server

### Environment Setup
The service requires a Conda environment named `dev` running Python 3.11. Ensure all required software is installed on your system before proceeding.

## Installation

### 1. Python Backend Setup
```bash
# Activate the development environment
conda deactivate && conda activate dev

# Install Python dependencies
cd apps/services/dev/stream
pip install -r requirements.txt
```

### 2. Frontend Setup
```bash
# Install Node.js dependencies
cd front_end/dev/stream/Camera
npm install
```

### 3. ngrok Configuration
1. Set up ngrok authentication by following the official ngrok documentation
2. Configure your authentication token as specified in the ngrok docs
3. Verify your authentication status

## Running the Service

The service requires multiple components running simultaneously. Open separate terminal windows for each component:

### 1. Backend Server
```bash
cd apps/services/dev/stream
conda deactivate && conda activate dev
python server.py
```

### 2. Machine Learning Service
```bash
cd apps/services/dev/stream
conda deactivate && conda activate dev
python ml.py
```

### 3. Frontend Application
```bash
cd front_end/dev/stream/Camera
npm run dev
```

### 4. ngrok Tunnel
```bash
ngrok http --url=<NGROK_URL> 80
```

### 5. nginx Web Server
```bash
./devOps/setup/nginx/nginx-control.sh start
```

## Troubleshooting

If you encounter issues:
1. Ensure all prerequisites are properly installed
2. Verify that the Conda environment is activated
3. Check that all required ports are available
4. Confirm ngrok authentication is properly configured

## Additional Resources
- For detailed ngrok setup, refer to the [ngrok documentation](https://ngrok.com/docs)
- For nginx configuration details, consult the [nginx documentation](https://nginx.org/en/docs/)