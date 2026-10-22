# ==============================================================================
# VERDURE: Precision Leaf Doctor Production Dockerfile
# NexAI Hackathon 2026 • Challenge 2.2: Leaf Doctor for Real Field Photos
# Multi-stage lightweight CPU inference container (~450MB image size)
# ==============================================================================

FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

WORKDIR /app

# Install minimal OS dependencies for OpenCV headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU index first to avoid CUDA gigabytes
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir opencv-python-headless fastapi uvicorn pydantic python-multipart pillow

# Copy application source and models
COPY . /app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
