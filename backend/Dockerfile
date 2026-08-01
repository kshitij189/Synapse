# ── Stage 1: Builder ────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install uv for fast dependency resolution.
RUN pip install --no-cache-dir uv

# Copy dependency manifest first to leverage Docker layer caching.
COPY pyproject.toml ./

# Install production dependencies into a virtual environment.
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache .

# ── Stage 2: Runtime ───────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="Synapse Platform Team"
LABEL description="Synapse Backend — Autonomous Adaptive Organization Platform"

# Create a non-root user for security.
RUN groupadd --gid 1000 synapse && \
    useradd --uid 1000 --gid synapse --shell /bin/bash --create-home synapse

WORKDIR /app

# Copy the virtual environment from the builder stage.
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application source.
COPY ./app ./app

# Switch to the non-root user.
USER synapse

EXPOSE 8000

# Healthcheck using the /health endpoint.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start the application using uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
