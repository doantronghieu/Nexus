# Build stage
FROM python:3.11-slim-bullseye AS build

# Create a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the working directory
WORKDIR /app/apps

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  python3-dev \
  libssl-dev \
  portaudio19-dev \
  libasound2-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY apps/services/SERVICE/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/services/core.requirements.txt .
RUN pip install --no-cache-dir -r core.requirements.txt

# Copy the application code (local -> container)
COPY apps .

# Production stage
FROM python:3.11-slim-bullseye

# Set the working directory
WORKDIR /apps

# Install runtime system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
  libssl-dev \
  libgl1-mesa-glx \
  libglib2.0-0 \
  libportaudio2 \
  libasound2 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN adduser --disabled-password --no-create-home app

# Copy the virtual environment from the build stage
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code from the build stage
COPY --from=build /app/apps /apps

# Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1

# Switch to the non-root user
# USER app

# Expose the port (just for documenting)
EXPOSE 8000

# Set the command to run the FastAPI app
WORKDIR /apps/services/SERVICE/

CMD ["python", "server.py"]