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
