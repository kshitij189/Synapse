"""Tests for health and system endpoints.

Reference: Document 24 (EP-13 §13.12) — Health checks.
"""

from __future__ import annotations

import httpx
import pytest

from app.shared.constants import SERVICE_NAME


@pytest.mark.asyncio
async def test_root_endpoint(client: httpx.AsyncClient) -> None:
    """Test the root identification endpoint."""
    response = await client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["service"] == SERVICE_NAME
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_health_endpoint(client: httpx.AsyncClient) -> None:
    """Test the liveness health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "environment" in data


@pytest.mark.asyncio
async def test_version_endpoint(client: httpx.AsyncClient) -> None:
    """Test the version metadata endpoint."""
    response = await client.get("/version")
    assert response.status_code == 200

    data = response.json()
    assert data["service"] == SERVICE_NAME
    assert "version" in data
    assert "python_version" in data
