"""Synapse Backend — Health & System Endpoints.

Provides the three foundational endpoints required during the bootstrap
milestone:

- ``GET /``        — Service identification
- ``GET /health``  — Liveness health check
- ``GET /version`` — Version information

Reference: Document 24 (EP-13 §13.12) — Health checks.
"""

from __future__ import annotations

import sys

from fastapi import APIRouter

from app.config.settings import get_settings
from app.shared.constants import SERVICE_NAME
from app.utils.datetime import to_iso8601, utc_now

router = APIRouter(tags=["System"])


@router.get(
    "/",
    summary="Service identification",
    description="Returns the service name and running status.",
)
async def root() -> dict[str, str]:
    """Minimal probe confirming the service is reachable."""
    return {
        "service": SERVICE_NAME,
        "status": "running",
    }


@router.get(
    "/health",
    summary="Health check",
    description="Returns the current health status of the service.",
)
async def health() -> dict[str, str]:
    """Lightweight liveness check.

    This endpoint must execute quickly and avoid expensive I/O operations so
    that Kubernetes probes do not time out.
    """
    settings = get_settings()
    return {
        "status": "healthy",
        "timestamp": to_iso8601(utc_now()),
        "environment": settings.environment,
    }


@router.get(
    "/version",
    summary="Version information",
    description="Returns version metadata for the running service.",
)
async def version() -> dict[str, str]:
    """Return build / version metadata."""
    settings = get_settings()
    return {
        "version": settings.app_version,
        "service": settings.app_name,
        "python_version": sys.version,
    }
