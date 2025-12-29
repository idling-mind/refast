"""Test FastAPI integration."""

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from refast import Context, RefastApp
from refast.components import Button, Container, Text


class TestFastAPIIntegration:
    """Test integration with existing FastAPI apps."""

    def test_mount_to_existing_app(self):
        """Test mounting Refast to existing FastAPI app."""
        # Existing FastAPI app with routes
        app = FastAPI()

        @app.get("/api/health")
        def health():
            return {"status": "healthy"}

        @app.get("/api/users")
        def list_users():
            return [{"id": 1, "name": "Alice"}]

        # Add Refast
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Text("Hello from Refast")

        app.include_router(ui.router, prefix="/ui")

        client = TestClient(app)

        # Original API still works
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

        response = client.get("/api/users")
        assert response.status_code == 200
        assert len(response.json()) == 1

        # Refast UI works
        response = client.get("/ui/")
        assert response.status_code == 200

    def test_multiple_refast_apps(self):
        """Test multiple Refast apps in one FastAPI app."""
        app = FastAPI()

        # Admin UI
        admin_ui = RefastApp(title="Admin")

        @admin_ui.page("/")
        def admin_home(ctx: Context):
            return Text("Admin Dashboard")

        # Public UI
        public_ui = RefastApp(title="Public")

        @public_ui.page("/")
        def public_home(ctx: Context):
            return Text("Welcome")

        app.include_router(admin_ui.router, prefix="/admin")
        app.include_router(public_ui.router, prefix="/app")

        client = TestClient(app)

        admin_response = client.get("/admin/")
        assert admin_response.status_code == 200

        public_response = client.get("/app/")
        assert public_response.status_code == 200

    def test_refast_with_middleware(self):
        """Test Refast with other middleware."""
        app = FastAPI()

        # Add custom middleware
        @app.middleware("http")
        async def add_custom_header(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Custom"] = "test"
            return response

        # Add Refast
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Text("Home")

        app.include_router(ui.router)

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.headers.get("X-Custom") == "test"

    def test_refast_with_lifespan(self):
        """Test Refast with FastAPI lifespan events."""
        startup_called = []
        shutdown_called = []

        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            startup_called.append(True)
            yield
            shutdown_called.append(True)

        app = FastAPI(lifespan=lifespan)

        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Text("Home")

        app.include_router(ui.router)

        with TestClient(app):
            assert len(startup_called) == 1

        assert len(shutdown_called) == 1

    def test_mixed_api_and_ui_routes(self):
        """Test mixing API and UI routes in the same app."""
        app = FastAPI()

        # API routes
        @app.get("/api/data")
        def get_data():
            return {"value": 42}

        @app.post("/api/data")
        def create_data(data: dict):
            return {"created": True, "data": data}

        # UI routes
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Container(
                children=[
                    Text("Dashboard"),
                    Button("Load Data", id="load-btn"),
                ]
            )

        @ui.page("/settings")
        def settings(ctx: Context):
            return Text("Settings Page")

        app.include_router(ui.router, prefix="/ui")

        client = TestClient(app)

        # API works
        response = client.get("/api/data")
        assert response.json()["value"] == 42

        response = client.post("/api/data", json={"key": "value"})
        assert response.json()["created"] is True

        # UI works
        response = client.get("/ui/")
        assert response.status_code == 200

        response = client.get("/ui/settings")
        assert response.status_code == 200


class TestRouterConfiguration:
    """Test router configuration options."""

    def test_custom_prefix(self):
        """Test with custom prefix."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Text("Home")

        app.include_router(ui.router, prefix="/custom/path")

        client = TestClient(app)
        response = client.get("/custom/path/")
        assert response.status_code == 200

    def test_with_tags(self):
        """Test router with tags."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Text("Home")

        app.include_router(ui.router, tags=["ui"])

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling integration."""

    def test_page_not_found_no_fallback(self):
        """Test 404 handling when no fallback page exists."""
        app = FastAPI()
        ui = RefastApp()

        # Only register /about, not /
        @ui.page("/about")
        def about(ctx: Context):
            return Text("About")

        app.include_router(ui.router)

        client = TestClient(app)
        # Since there's no "/" and no matching page, should get 404
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_page_error_handling(self):
        """Test error in page function."""
        app = FastAPI()
        ui = RefastApp()

        @ui.page("/error")
        def error_page(ctx: Context):
            raise ValueError("Test error")

        app.include_router(ui.router)

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/error")
        assert response.status_code == 500
