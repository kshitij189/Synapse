"""Synapse Backend — FastAPI Exception Handlers.

These handlers translate application exceptions and framework validation errors
into a consistent JSON error response.  Internal implementation details are
never exposed to API consumers.

Reference: Document 19 (COD-05 §5.5) — Error handling workflow.
Reference: Document 24 (EP-05 §5.18) — Error propagation.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import SynapseException

logger = logging.getLogger(__name__)


def _error_body(
    code: str,
    message: str,
    details: Any | None = None,
) -> dict[str, Any]:
    """Build the canonical error response envelope."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
    }


async def synapse_exception_handler(
    request: Request,
    exc: SynapseException,
) -> JSONResponse:
    """Handle all :class:`SynapseException` subclasses."""
    logger.warning(
        "Application error: %s (code=%s, status=%d)",
        exc.detail,
        exc.error_code,
        exc.status_code,
        extra={"error_code": exc.error_code, "extra": exc.extra},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(
            code=exc.error_code,
            message=exc.detail,
            details=exc.extra,
        ),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle Pydantic / FastAPI request validation errors.

    Field-level details are returned so consumers can display inline
    validation messages.
    """
    field_errors: list[dict[str, Any]] = []
    for error in exc.errors():
        field_errors.append(
            {
                "field": ".".join(str(loc) for loc in error.get("loc", [])),
                "message": error.get("msg", ""),
                "type": error.get("type", ""),
            }
        )

    logger.info(
        "Request validation failed with %d error(s).",
        len(field_errors),
    )
    return JSONResponse(
        status_code=422,
        content=_error_body(
            code="VALIDATION_ERROR",
            message="Request validation failed.",
            details=field_errors,
        ),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Catch-all for unexpected exceptions.

    Internal details are logged but **not** returned to the caller.
    """
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content=_error_body(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred.",
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all exception handlers to the FastAPI application."""
    app.add_exception_handler(SynapseException, synapse_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
