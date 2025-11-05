# # ---------- Stage 1: builder (installs deps into a venv) ----------
# FROM python:3.11-slim AS builder

# # System deps for building common Python wheels (psycopg2, numpy, etc.) — trim if not needed
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Keep Python from buffering logs & writing .pyc
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PIP_NO_CACHE_DIR=1

# WORKDIR /app

# # Copy only requirements first to leverage Docker layer cache
# COPY requirements.txt /app/requirements.txt

# # Create a virtualenv inside /opt/venv and install deps
# RUN python -m venv /opt/venv \
#     && /opt/venv/bin/pip install --upgrade pip \
#     && /opt/venv/bin/pip install -r /app/requirements.txt

# # ---------- Stage 2: runtime (copy code + venv, drop root) ----------
# FROM python:3.11-slim

# # Same envs in runtime
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     PIP_NO_CACHE_DIR=1 \
#     # Change this to match your module and variable (e.g., "application:application" or "app:app")
#     APP_MODULE=application:application \
#     # Optional: tweak Gunicorn without editing CMD
#     GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000 --workers 2 --threads 4 --timeout 120"

# # Copy venv from builder
# COPY --from=builder /opt/venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"

# # Create non-root user
# RUN useradd -ms /bin/bash appuser
# USER appuser

# WORKDIR /app

# # Copy your app code
# COPY --chown=appuser:appuser . /app

# # Expose the port your app listens on
# EXPOSE 8000

# # Simple healthcheck; change /health to your route if needed
# HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
#   CMD curl -fsS http://127.0.0.1:8000/ || exit 1

# # Start Gunicorn
# # APP_MODULE must be "module_name:variable_name"
# ENTRYPOINT ["gunicorn"]
# CMD ["${APP_MODULE}"]

# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies required for scientific Python stacks
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better caching
COPY requirements.txt setup.py ./
COPY src ./src

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the application source
COPY . .

# EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "application:app"]

EXPOSE 8000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} application:application"]
