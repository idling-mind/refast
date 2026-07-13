"""Tests for RefastRouter class."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from refast import RefastApp


class TestRefastRouter:
    """Tests for router mounting and page handling."""

    def test_router_mounts_to_fastapi(self):
        """Test router can be mounted to FastAPI app."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            return None

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        response = client.get("/ui/")
        assert response.status_code == 200

    def test_page_returns_html(self):
        """Test that page requests return HTML content."""
        app = FastAPI()
        ui = RefastApp(title="Test App")

        @ui.page("/")
        def home(ctx):
            return None

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        response = client.get("/ui/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Test App" in response.text

    def test_page_not_found_returns_404(self):
        """Test 404 returned when no pages are registered."""
        app = FastAPI()
        ui = RefastApp()
        app.include_router(ui.router, prefix="/ui")

        client = TestClient(app)
        response = client.get("/ui/nonexistent")
        assert response.status_code == 404

    def test_page_fallback_to_index(self):
        """Test that unknown paths fall back to index page."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            return None

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        # Unknown path should fallback to "/"
        response = client.get("/ui/unknown")
        assert response.status_code == 200

    def test_multiple_pages_routing(self):
        """Test routing to multiple pages."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            return None

        @ui.page("/about")
        def about(ctx):
            return None

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        response_home = client.get("/ui/")
        response_about = client.get("/ui/about")

        assert response_home.status_code == 200
        assert response_about.status_code == 200

    def test_html_includes_initial_data_script(self):
        """Test that HTML does not include initial data script tag, as this behavior changed."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            return None

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        response = client.get("/ui/")
        assert "__REFAST_INITIAL_DATA__" not in response.text

    def test_html_includes_root_div(self):
        """Test that HTML includes root div for React."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            return None

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        response = client.get("/ui/")
        assert 'id="refast-root"' in response.text

    def test_api_page_handler_raises_when_page_returns_none(self):
        """Test that page-render API rejects page functions returning None."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            return None

        app.include_router(ui.router)
        client = TestClient(app)

        with pytest.raises(ValueError, match="Page function 'home' for path '/' returned None"):
            client.get("/api/page", headers={"referer": "http://testserver/"})

    def test_active_contexts_property(self):
        """Test active_contexts property returns values from _websocket_contexts."""
        app = RefastApp()
        # Initialize router
        _ = app.router
        refast_router = app._router

        assert refast_router.active_contexts == []

        # Mock a context
        mock_ws = object()
        mock_ctx = object()
        refast_router._websocket_contexts[mock_ws] = mock_ctx

        assert refast_router.active_contexts == [mock_ctx]


class TestWebSocketEndpoint:
    """Tests for WebSocket endpoint."""

    def test_websocket_endpoint_exists(self):
        """Test WebSocket endpoint is set up."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            return None

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        # WebSocket connection test
        with client.websocket_connect("/ui/ws") as websocket:  # noqa: F841
            # Just verify we can connect
            pass

    def test_websocket_store_init_http_exception(self):
        """Test that HTTPException raised during page init is caught and rendered."""
        from fastapi import HTTPException

        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            raise HTTPException(status_code=429, detail="Rate limited")

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        with client.websocket_connect("/ui/ws") as websocket:
            websocket.send_json({"type": "store_init", "path": "/", "data": {}})
            response = websocket.receive_json()
            assert response["type"] == "page_render"
            assert "Rate limited" in str(response["component"])
            assert "Error 429" in str(response["component"])

    def test_websocket_callback_http_exception(self):
        """Test that HTTPException raised in callback sends toast notification."""
        from fastapi import HTTPException

        from refast.components import Button

        app = FastAPI()
        ui = RefastApp()

        async def action(ctx):
            raise HTTPException(status_code=400, detail="Invalid action")

        @ui.page("/")
        def home(ctx):
            return Button("Click", on_click=ctx.callback(action))

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        with client.websocket_connect("/ui/ws") as websocket:
            # First initialize store to render and register callback
            websocket.send_json({"type": "store_init", "path": "/", "data": {}})
            render_resp = websocket.receive_json()
            assert render_resp["type"] == "page_render"

            ready_resp = websocket.receive_json()
            assert ready_resp["type"] == "store_ready"

            # Extract callback ID
            import json
            import re

            serialized = json.dumps(render_resp["component"])
            cb_ids = re.findall(r'"callbackId":\s*"([^"]+)"', serialized)
            assert len(cb_ids) > 0
            cb_id = cb_ids[0]

            # Trigger the callback
            websocket.send_json(
                {"type": "callback", "callback_id": cb_id, "data": {}, "event_data": {}}
            )

            # Wait for message response (should be the toast)
            response = websocket.receive_json()
            assert response["type"] == "toast"
            assert response["message"] == "Error 400"
            assert response["description"] == "Invalid action"
            assert response["variant"] == "destructive"
