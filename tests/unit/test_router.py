"""Tests for RefastRouter class."""

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
        """Test that HTML includes initial data script tag."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx):
            return None

        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)

        response = client.get("/ui/")
        assert "__REFAST_INITIAL_DATA__" in response.text

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
