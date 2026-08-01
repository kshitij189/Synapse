"""Synapse Backend — DateTime Utilities.

All timestamps within the platform use UTC.  These helpers ensure consistent
datetime handling across the codebase.
"""

from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return the current UTC datetime (timezone-aware)."""
    return datetime.now(UTC)


def to_iso8601(dt: datetime) -> str:
    """Format a datetime as an ISO-8601 string.

    If the datetime is naive it is assumed to be UTC.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.isoformat()
