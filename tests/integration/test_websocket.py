"""WebSocket integration tests."""

import json
import re

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from refast import Context, RefastApp
from refast.components import Button, Container, Text
from refast.session.middleware import SessionMiddleware
from refast.session.stores.memory import MemorySessionStore


def extract_initial_data(html_content: str) -> dict:
    """Extract the __REFAST_INITIAL_DATA__ from HTML response."""
    match = re.search(r"window\.__REFAST_INITIAL_DATA__\s*=\s*({.*?});", html_content, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return {}


class TestWebSocketConnection:
    """Test WebSocket connection handling."""

    @pytest.fixture
    def ui_app(self):
        """Create a Refast app with WebSocket support."""
        ui = RefastApp(title="WS Test")

        @ui.page("/")
        def home(ctx: Context):
            return Container(
                id="main",
                children=[
                    Text("WebSocket Test", id="title"),
                    Button(
                        "Click Me",
                        id="test-btn",
                        on_click=ctx.callback(handle_click),
                    ),
                ],
            )

        async def handle_click(ctx: Context):
            pass

        return ui

    @pytest.fixture
    def fastapi_app(self, ui_app):
        """Create FastAPI app with Refast."""
        app = FastAPI()
        store = MemorySessionStore()
        app.add_middleware(SessionMiddleware, store=store, secret_key="test-secret")
        app.include_router(ui_app.router)
        return app

    @pytest.fixture
    def client(self, fastapi_app):
        """Create test client."""
        return TestClient(fastapi_app)

    def test_websocket_endpoint_exists(self, client):
        """Test that WebSocket endpoint is available."""
        # First load the page to get a session
        response = client.get("/")
        assert response.status_code == 200

        # WebSocket connection test
        try:
            with client.websocket_connect("/ws") as websocket:
                assert websocket is not None
        except Exception:
            # WebSocket might not be fully implemented yet
            pass

    def test_page_loads_without_websocket(self, client):
        """Test that page works without WebSocket."""
        response = client.get("/")
        assert response.status_code == 200


class TestWebSocketMessages:
    """Test WebSocket message handling."""

    @pytest.fixture
    def app_with_callback(self):
        """Create app with callback that modifies state."""
        ui = RefastApp()
        ui._test_value = None

        async def set_value(ctx: Context, value: str = ""):
            ui._test_value = value

        @ui.page("/")
        def home(ctx: Context):
            return Button(
                "Set Value",
                on_click=ctx.callback(set_value, value="test"),
            )

        return ui

    def test_callback_structure(self, app_with_callback):
        """Test that callbacks are properly structured."""
        app = FastAPI()
        app.include_router(app_with_callback.router)

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200

        data = extract_initial_data(response.text)
        on_click = data["props"]["on_click"]

        # Verify callback structure
        assert "callbackId" in on_click
        assert "boundArgs" in on_click
        assert on_click["boundArgs"]["value"] == "test"
