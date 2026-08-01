"""Synapse Backend — Application Settings.

Configuration is loaded from environment variables and an optional ``.env`` file
using *pydantic-settings*.  Every setting has a sensible default so the
application can start in a development context without requiring a ``.env`` file.

Reference: Document 23 (TS-03) — Pydantic v2 for configuration management.
Reference: Document 24 (EP-02 §2.7) — Environment variable standards.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.shared.constants import SERVICE_NAME


class Settings(BaseSettings):
    """Application-wide settings sourced from environment variables.

    Attributes are grouped by responsibility: application identity, server
    binding, external service URLs (not connected during bootstrap), and
    observability controls.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application Identity ────────────────────────────────────────────
    app_name: str = SERVICE_NAME
    app_version: str = "0.1.0"
    environment: Literal["development", "testing", "staging", "production"] = "development"
    debug: bool = False

    # ── Server ──────────────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000

    # ── Logging ─────────────────────────────────────────────────────────
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # ── Database (setup only — not connected yet) ───────────────────────
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/synapse"

    # ── Redis (setup only — not connected yet) ──────────────────────────
    redis_url: str = "redis://localhost:6379/0"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the singleton *Settings* instance.

    The result is cached so repeated calls during a request lifecycle do
    not re-parse environment variables.
    """
    return Settings()
