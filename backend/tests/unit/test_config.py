"""Tests for the application configuration module."""

from __future__ import annotations

import os
from unittest.mock import patch

from app.config.settings import Settings, get_settings


def test_default_settings() -> None:
    """Ensure settings can be instantiated with default values."""
    # Ensure no environment variables override the defaults during this test.
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.app_name == "synapse-backend"
        assert settings.environment == "development"
        assert settings.debug is False
        assert settings.log_level == "INFO"


def test_environment_override() -> None:
    """Ensure environment variables override default settings."""
    env_vars = {
        "APP_NAME": "test-service",
        "ENVIRONMENT": "testing",
        "DEBUG": "true",
        "LOG_LEVEL": "DEBUG",
        "PORT": "9090",
    }

    with patch.dict(os.environ, env_vars, clear=True):
        settings = Settings()
        assert settings.app_name == "test-service"
        assert settings.environment == "testing"
        assert settings.debug is True
        assert settings.log_level == "DEBUG"
        assert settings.port == 9090


def test_get_settings_caching() -> None:
    """Ensure get_settings returns the same cached instance."""
    settings_a = get_settings()
    settings_b = get_settings()
    assert settings_a is settings_b
