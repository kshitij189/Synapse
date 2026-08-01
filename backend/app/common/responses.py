"""Synapse Backend — Standard API Response Models.

Every API response is wrapped in a consistent envelope so that consumers can
rely on a predictable structure regardless of the endpoint.

Reference: Document 19 (COD-05 §5.5) — Consistent error response format.
Reference: Document 24 (EP-06) — API development standards.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Machine-readable error detail returned in error responses."""

    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error description.")
    details: Any | None = Field(default=None, description="Optional structured details.")


class ErrorResponse(BaseModel):
    """Standard error response envelope."""

    success: bool = Field(default=False, description="Always False for errors.")
    error: ErrorDetail


class ApiResponse(BaseModel, Generic[T]):
    """Standard success response envelope.

    Usage::

        ApiResponse[UserOut](data=user, message="User created.")
    """

    success: bool = Field(default=True, description="Always True for success.")
    data: T = Field(..., description="Response payload.")
    message: str | None = Field(default=None, description="Optional human-readable message.")
