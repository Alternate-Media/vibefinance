# Dockerfile for FastAPI Backend (Hardened Ubuntu)

# Stage 1: Builder
FROM ubuntu:24.04 as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies & Python build tools
# software-properties-common is needed for add-apt-repository if using deadsnakes, 
# but Ubuntu 24.04 has Python 3.12 by default.
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    python3-pip \
    python3-dev \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml .

# Install dependencies
RUN pip install --upgrade pip && pip install .

# Stage 2: Runner
FROM ubuntu:24.04

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies
# libpq5 is needed for psycopg (PostgreSQL adapter)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-minimal \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual env from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . .

# Create a non-root user
RUN groupadd -r app && useradd -r -g app app
USER app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
