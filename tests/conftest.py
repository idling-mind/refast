"""Shared pytest fixtures."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from refast import RefastApp


@pytest.fixture
def app() -> RefastApp:
    """Create a fresh RefastApp instance."""
    return RefastApp(title="Test App")


@pytest.fixture
def fastapi_app(app: RefastApp) -> FastAPI:
    """Create a FastAPI app with Refast mounted."""
    fastapi = FastAPI()
    fastapi.include_router(app.router, prefix="/ui")
    return fastapi


@pytest.fixture
def client(fastapi_app: FastAPI) -> TestClient:
    """Create a test client."""
    return TestClient(fastapi_app)
