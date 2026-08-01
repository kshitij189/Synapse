"""Synapse Backend — Application Exceptions.

All application-specific exceptions derive from :class:`SynapseException`.
Each subclass maps to a specific HTTP status code and carries a machine-readable
``error_code`` for programmatic error handling by API consumers.

Reference: Document 19 (COD-05 §5.4) — Error classification.
Reference: Document 24 (EP-05 §5.18) — Error propagation.
"""

from __future__ import annotations

from typing import Any


class SynapseException(Exception):
    """Base exception for the Synapse platform.

    All domain and application exceptions should extend this class so that
    the global exception handler can convert them into a structured API
    error response.
    """

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"

    def __init__(
        self,
        detail: str = "An unexpected error occurred.",
        error_code: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self.detail = detail
        if error_code is not None:
            self.error_code = error_code
        self.extra = extra
        super().__init__(self.detail)


class NotFoundException(SynapseException):
    """Raised when a requested resource cannot be found."""

    status_code: int = 404
    error_code: str = "NOT_FOUND"

    def __init__(
        self,
        detail: str = "The requested resource was not found.",
        error_code: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail=detail, error_code=error_code, extra=extra)


class ValidationException(SynapseException):
    """Raised when input validation fails at the application level."""

    status_code: int = 422
    error_code: str = "VALIDATION_ERROR"

    def __init__(
        self,
        detail: str = "Validation failed.",
        error_code: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail=detail, error_code=error_code, extra=extra)


class UnauthorizedException(SynapseException):
    """Raised when authentication is missing or invalid."""

    status_code: int = 401
    error_code: str = "UNAUTHORIZED"

    def __init__(
        self,
        detail: str = "Authentication is required.",
        error_code: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail=detail, error_code=error_code, extra=extra)


class ForbiddenException(SynapseException):
    """Raised when the authenticated user lacks permission."""

    status_code: int = 403
    error_code: str = "FORBIDDEN"

    def __init__(
        self,
        detail: str = "You do not have permission to perform this action.",
        error_code: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail=detail, error_code=error_code, extra=extra)


class InternalServerException(SynapseException):
    """Raised for internal / infrastructure-level errors."""

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"

    def __init__(
        self,
        detail: str = "An internal server error occurred.",
        error_code: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(detail=detail, error_code=error_code, extra=extra)
