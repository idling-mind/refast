"""Full flow integration tests."""

import json
import re

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from refast import RefastApp, Context
from refast.components import Container, Text, Button, Input, Column
from refast.session.stores.memory import MemorySessionStore
from refast.session.middleware import SessionMiddleware


def extract_initial_data(html_content: str) -> dict:
    """Extract the __REFAST_INITIAL_DATA__ from HTML response."""
    match = re.search(r"window\.__REFAST_INITIAL_DATA__\s*=\s*({.*?});", html_content, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return {}


class TestFullFlow:
    """Test complete user flows."""

    @pytest.fixture
    def ui_app(self):
        """Create a full Refast app."""
        ui = RefastApp(title="Test App", secret_key="test-secret")

        @ui.page("/")
        def home(ctx: Context):
            count = ctx.state.get("count", 0)
            return Container(
                id="main",
                children=[
                    Text(f"Count: {count}", id="count-display"),
                    Button(
                        "Increment",
                        id="increment-btn",
                        on_click=ctx.callback(increment),
                    ),
                ],
            )

        async def increment(ctx: Context):
            count = ctx.state.get("count", 0) + 1
            ctx.state.set("count", count)

        return ui

    @pytest.fixture
    def fastapi_app(self, ui_app):
        """Mount to FastAPI."""
        app = FastAPI()
        store = MemorySessionStore()
        app.add_middleware(SessionMiddleware, store=store, secret_key="test-secret")
        app.include_router(ui_app.router, prefix="/ui")
        return app

    @pytest.fixture
    def client(self, fastapi_app):
        """Create test client."""
        return TestClient(fastapi_app)

    def test_page_loads(self, client):
        """Test that page loads with initial content."""
        response = client.get("/ui/")
        assert response.status_code == 200
        # The response should contain the initial component tree or HTML
        assert response.text is not None

    def test_page_returns_html_with_initial_data(self, client):
        """Test that page returns HTML with embedded component tree."""
        response = client.get("/ui/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        
        # Extract and verify the component tree from HTML
        data = extract_initial_data(response.text)
        assert "type" in data
        assert data["type"] == "Container"
        assert data["id"] == "main"


class TestComponentRendering:
    """Test component rendering."""

    def test_nested_components(self):
        """Test nested component rendering."""
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Container(
                id="outer",
                children=[
                    Column(
                        id="column",
                        children=[
                            Text("Line 1", id="line1"),
                            Text("Line 2", id="line2"),
                            Container(
                                id="inner",
                                children=[
                                    Text("Nested", id="nested"),
                                ],
                            ),
                        ],
                    )
                ],
            )

        app = FastAPI()
        app.include_router(ui.router)

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200

        data = extract_initial_data(response.text)
        assert data["id"] == "outer"
        assert data["type"] == "Container"
        assert len(data["children"]) == 1

    def test_component_with_props(self):
        """Test component with various props."""
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Button(
                "Click Me",
                id="btn",
                variant="primary",
                size="lg",
                disabled=True,
            )

        app = FastAPI()
        app.include_router(ui.router)

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200

        data = extract_initial_data(response.text)
        assert data["type"] == "Button"
        assert data["props"]["variant"] == "primary"
        assert data["props"]["size"] == "lg"
        assert data["props"]["disabled"] is True


class TestCallbackFlow:
    """Test callback invocation flow."""

    def test_callback_registered(self):
        """Test that callbacks are registered."""
        ui = RefastApp()
        callback_invoked = []

        async def handle_click(ctx: Context, value: str = "test"):
            callback_invoked.append(value)

        @ui.page("/")
        def home(ctx: Context):
            return Button(
                "Click",
                on_click=ctx.callback(handle_click, value="test"),
            )

        app = FastAPI()
        app.include_router(ui.router)

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200

        # Check that callback reference is in the rendered output
        data = extract_initial_data(response.text)
        assert data["props"].get("onClick") is not None
        on_click = data["props"]["onClick"]
        assert "callbackId" in on_click

    def test_multiple_callbacks_on_page(self):
        """Test multiple callbacks registered on a single page."""
        ui = RefastApp()

        async def handler1(ctx: Context):
            pass

        async def handler2(ctx: Context):
            pass

        @ui.page("/")
        def home(ctx: Context):
            return Column(
                children=[
                    Button("Btn1", on_click=ctx.callback(handler1)),
                    Button("Btn2", on_click=ctx.callback(handler2)),
                ]
            )

        app = FastAPI()
        app.include_router(ui.router)

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200

        data = extract_initial_data(response.text)
        children = data["children"]
        assert len(children) == 2

        # Both buttons should have different callback IDs
        cb1 = children[0]["props"]["onClick"]["callbackId"]
        cb2 = children[1]["props"]["onClick"]["callbackId"]
        assert cb1 != cb2


class TestMultiplePages:
    """Test multiple page routing."""

    def test_multiple_pages(self):
        """Test app with multiple pages."""
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Text("Home Page")

        @ui.page("/about")
        def about(ctx: Context):
            return Text("About Page")

        @ui.page("/contact")
        def contact(ctx: Context):
            return Text("Contact Page")

        app = FastAPI()
        app.include_router(ui.router)

        client = TestClient(app)

        # All pages should work
        response = client.get("/")
        assert response.status_code == 200

        response = client.get("/about")
        assert response.status_code == 200

        response = client.get("/contact")
        assert response.status_code == 200

    def test_page_content_differs(self):
        """Test that different pages have different content."""
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Text("Home Page", id="home-text")

        @ui.page("/about")
        def about(ctx: Context):
            return Text("About Page", id="about-text")

        app = FastAPI()
        app.include_router(ui.router)

        client = TestClient(app)

        home_response = client.get("/")
        about_response = client.get("/about")

        home_data = extract_initial_data(home_response.text)
        about_data = extract_initial_data(about_response.text)

        assert home_data["id"] == "home-text"
        assert about_data["id"] == "about-text"
