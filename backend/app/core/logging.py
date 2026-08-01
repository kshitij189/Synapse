"""Synapse Backend — Structured Logging.

All log output is formatted as JSON to satisfy the observability requirements
documented in EP-13 §13.5.  The ``request_id`` context variable is populated by
the request-ID middleware so that every log line emitted during a request can be
correlated.

Reference: Document 24 (EP-13 §13.5) — Logging standards (JSON, UTC, fields).
Reference: Document 24 (EP-04 §4.16) — Log levels.
Reference: Document 19 (COD-05 §5.6) — Logging categories.
"""

from __future__ import annotations

import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.config.settings import Settings

# ── Context variable for per-request correlation ────────────────────────
request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


class JSONFormatter(logging.Formatter):
    """Produce a single-line JSON object for every log record.

    Fields emitted (per EP-13 §13.5):
    - ``timestamp``  — ISO-8601 in UTC
    - ``level``      — log severity
    - ``service``    — service name
    - ``environment``— deployment environment
    - ``version``    — application version
    - ``logger``     — Python logger name
    - ``message``    — human-readable message
    - ``request_id`` — correlation ID (when available)
    """

    def __init__(
        self,
        service: str = "synapse-backend",
        environment: str = "development",
        version: str = "0.1.0",
    ) -> None:
        super().__init__()
        self._service = service
        self._environment = environment
        self._version = version

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "service": self._service,
            "environment": self._environment,
            "version": self._version,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Attach correlation ID when available.
        rid = request_id_ctx.get()
        if rid is not None:
            log_entry["request_id"] = rid

        # Attach exception info when present.
        if record.exc_info and record.exc_info[1] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


def setup_logging(settings: Settings) -> None:
    """Configure the root logger with the :class:`JSONFormatter`.

    This function should be called **once** during application startup.
    """
    root_logger = logging.getLogger()

    # Prevent duplicate handlers when hot-reloading.
    if root_logger.handlers:
        root_logger.handlers.clear()

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(
        JSONFormatter(
            service=settings.app_name,
            environment=settings.environment,
            version=settings.app_version,
        )
    )

    root_logger.setLevel(settings.log_level)
    root_logger.addHandler(handler)

    # Silence overly chatty third-party loggers.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
