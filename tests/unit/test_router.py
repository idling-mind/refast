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
        """Test active_contexts property returns values from _connection_contexts."""
        app = RefastApp()
        # Initialize router
        _ = app.router
        refast_router = app._router

        assert refast_router.active_contexts == []

        # Mock a context
        conn_id = "test-connection-id"
        mock_ctx = object()
        refast_router._connection_contexts[conn_id] = mock_ctx

        assert refast_router.active_contexts == [mock_ctx]


class TestSSEAndEventEndpoints:
    """Tests for SSE and HTTP POST Event endpoints registration."""

    def test_endpoints_registered(self):
        """Test SSE and Event endpoints are registered on the router."""
        ui = RefastApp()
        # Trigger router initialization
        router = ui.router
        
        routes = [r.path for r in router.routes]
        assert "/api/events" in routes
        assert "/api/event" in routes
