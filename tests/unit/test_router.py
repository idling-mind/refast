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

    @pytest.mark.asyncio
    async def test_sse_handler_headers_and_heartbeat(self):
        """Test that SSE handler returns correct headers and the generator yields heartbeats."""
        import asyncio
        from unittest.mock import patch
        from fastapi import Request
        from refast.context import Context

        ui = RefastApp()
        _ = ui.router
        router = ui._router

        conn_id = "test-sse-handler-conn"
        ctx = Context(connection_id=conn_id, app=ui)
        router._connection_contexts[conn_id] = ctx

        # Create a dummy request
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/events",
            "headers": [],
            "query_string": b"",
        }
        request = Request(scope)

        response = await router._sse_handler(request, conn_id)

        # 1. Verify headers
        assert response.headers["cache-control"] == "no-cache, no-transform"
        assert response.headers["connection"] == "keep-alive"
        assert response.headers["x-accel-buffering"] == "no"

        # 2. Verify body iterator yields items
        body_iterator = response.body_iterator

        call_count = 0

        async def mock_wait_for(fut, timeout):
            try:
                fut.close()
            except RuntimeError:
                pass
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return {"type": "test_msg"}
            else:
                raise asyncio.TimeoutError()

        with patch("asyncio.wait_for", side_effect=mock_wait_for):
            gen = body_iterator
            
            # First yield should be the message we mock returned
            first_val = await gen.__anext__()
            assert "test_msg" in first_val
            
            # Second yield should be the heartbeat because wait_for raises TimeoutError
            second_val = await gen.__anext__()
            assert "keepalive" in second_val
            
            # Mark connection as disconnected so the loop exits
            conn = router.stream.get_connection(conn_id)
            if conn:
                conn.connected = False
                
            with pytest.raises(StopAsyncIteration):
                await gen.__anext__()

