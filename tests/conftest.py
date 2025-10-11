"""Test fixtures."""

import pytest


@pytest.fixture(autouse=True)
def global_env(monkeypatch):
    """Provide the env that your DI needs to build clients, without touching the network."""
    monkeypatch.setenv("TOKEN_VALIDATOR_CLIENT_BASE_URL", "http://localhost:8001")
    monkeypatch.setenv("USER_CLIENT_BASE_URL", "http://localhost:8002")


__all__ = [
    global_env,
]
