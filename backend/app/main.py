"""Synapse Backend — FastAPI Application Entry Point.

This module creates and configures the FastAPI application instance.  It wires
up the lifespan context manager (startup / shutdown), registers middleware,
exception handlers, and API routers.

Reference: Document 23 (TS-03 §3.5) — FastAPI as the API framework.
Reference: Document 24 (EP-05 §5.3) — Layered architecture.
Reference: Document 24 (EP-13 §13.7) — Always log startup and shutdown.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.config.settings import get_settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import setup_logging
from app.middleware.request_id import RequestIDMiddleware
from app.shared.constants import SERVICE_NAME

logger = logging.getLogger(__name__)


# ── Lifespan ────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan — startup and shutdown hooks.

    **Startup**:
    1. Load settings from the environment.
    2. Initialise structured JSON logging.
    3. Log the startup event.

    **Shutdown**:
    1. Log the shutdown event.
    2. Clean up resources (future milestones).
    """
    settings = get_settings()
    setup_logging(settings)

    logger.info(
        "Starting %s v%s (env=%s)",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )

    yield

    logger.info(
        "Shutting down %s v%s",
        settings.app_name,
        settings.app_version,
    )


# ── Application Factory ────────────────────────────────────────────────


def create_app() -> FastAPI:
    """Build and return a fully configured :class:`FastAPI` instance."""
    settings = get_settings()

    app = FastAPI(
        title=SERVICE_NAME,
        version=settings.app_version,
        description="Synapse Backend — Autonomous Adaptive Organization Platform",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── Middleware (outermost → innermost) ──────────────────────────
    app.add_middleware(RequestIDMiddleware)

    # ── Exception Handlers ─────────────────────────────────────────
    register_exception_handlers(app)

    # ── Routers ────────────────────────────────────────────────────
    app.include_router(health_router)

    return app


# The ``app`` object is referenced by ``uvicorn app.main:app``.
app: FastAPI = create_app()
