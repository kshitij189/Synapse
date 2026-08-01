"""Synapse Backend — Pytest Fixtures.

Provides shared testing fixtures such as the FastAPI test client.

Reference: Document 24 (EP-14 §14.25) — Testing tools (pytest + httpx).
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport

from app.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Use asyncio for anyio-based tests."""
    return "asyncio"


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an asynchronous test client for the FastAPI application.

    This fixture uses :class:`httpx.ASGITransport` to route requests
    directly to the ASGI app without requiring a live server.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as ac:
        yield ac
