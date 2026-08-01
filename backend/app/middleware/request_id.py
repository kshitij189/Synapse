"""Synapse Backend — Request ID Middleware.

Ensures that every request carries a unique ``X-Request-ID`` header.  If the
caller does not supply one, a UUID4 is generated.  The ID is stored in a
:mod:`contextvars` variable so the structured logger can include it
automatically.

Reference: Document 24 (EP-13 §13.11) — Correlation IDs.
"""

from __future__ import annotations

import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import request_id_ctx

_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Inject and propagate a unique request identifier."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        rid = request.headers.get(_HEADER) or str(uuid.uuid4())

        # Store in context variable for structured logging.
        token = request_id_ctx.set(rid)
        try:
            response = await call_next(request)
            response.headers[_HEADER] = rid
            return response
        finally:
            request_id_ctx.reset(token)
