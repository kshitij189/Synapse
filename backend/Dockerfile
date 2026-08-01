# ==============================================================================
# Synapse Backend — Multi-Stage Dockerfile
# ==============================================================================
#
# Build targets:
#   Production : docker build -t synapse-backend .
#   Development: docker build --target development -t synapse-backend:dev .
#
# Reference: Document 23 (TS-06 §6.4) — Docker containerization standards.
# Reference: Document 24 (EP-15 §15.10) — Docker image standards.
# ==============================================================================


# ── Stage 1: Builder ────────────────────────────────────────────────────
# Installs dependencies into an isolated virtual environment.
# This stage is discarded in the final image to reduce size.
# ────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim AS builder

WORKDIR /build

# Install uv for fast, deterministic dependency resolution.
RUN pip install --no-cache-dir uv

# Copy dependency manifests and README (required by hatchling build backend)
# first to maximise Docker layer caching.
# A change to application source code will NOT invalidate this layer.
COPY pyproject.toml uv.lock* README.md ./

# Create a virtual environment and install production dependencies only.
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache .


# ── Stage 2: Development ───────────────────────────────────────────────
# Extends the runtime with dev dependencies and hot-reload support.
# Usage: docker build --target development -t synapse-backend:dev .
# ────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim AS development

WORKDIR /app

# Copy the virtual environment from the builder stage.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install development dependencies into the existing venv.
COPY pyproject.toml uv.lock* README.md ./
RUN pip install --no-cache-dir uv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache ".[dev]"

# Copy application source and tests.
COPY ./app ./app
COPY ./tests ./tests

# Development defaults.
ENV ENVIRONMENT=development \
    DEBUG=true \
    LOG_LEVEL=DEBUG \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

# Development server with hot-reload enabled.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ── Stage 3: Production (default) ─────────────────────────────────────
# Minimal, secure runtime image containing only production dependencies.
# Usage: docker build -t synapse-backend .
# ────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim AS production

# ── OCI Image Labels (EP-15 §15.10: Version labels) ───────────────────
LABEL org.opencontainers.image.title="synapse-backend"
LABEL org.opencontainers.image.version="0.1.0"
LABEL org.opencontainers.image.description="Synapse Backend — Autonomous Adaptive Organization Platform"
LABEL org.opencontainers.image.source="https://github.com/kshitij189/Synapse"
LABEL org.opencontainers.image.authors="Synapse Platform Team"
LABEL org.opencontainers.image.vendor="Synapse"
LABEL org.opencontainers.image.licenses="Proprietary"

# ── Non-root user (EP-15 §15.10: Non-root execution) ──────────────────
RUN groupadd --gid 1000 synapse && \
    useradd --uid 1000 --gid synapse --shell /bin/bash --create-home synapse

WORKDIR /app

# ── Copy only the pre-built virtual environment (no build tools) ───────
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# ── Copy application source only (no tests, docs, scripts) ────────────
COPY ./app ./app

# ── Production defaults ───────────────────────────────────────────────
ENV ENVIRONMENT=production \
    DEBUG=false \
    LOG_LEVEL=INFO \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── Switch to non-root user ───────────────────────────────────────────
USER synapse

EXPOSE 8000

# ── Health check (EP-13 §13.12) ──────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

# ── Start the application ────────────────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
