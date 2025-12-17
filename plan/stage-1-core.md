# Stage 1: Core Framework Foundation

## Progress

- [x] Task 1.1: Project setup
- [x] Task 1.2: RefastApp class
- [x] Task 1.3: Router integration
- [x] Task 1.4: Context class
- [x] Task 1.5: State management
- [x] Task 1.6: Tests configuration (Callback system included in Context)

## Objectives

Build the foundational classes that everything else depends on:
- `RefastApp` - Main application class
- `RefastRouter` - FastAPI router integration
- `Context` - Request context for callbacks
- `State` - State management container
- `Callback` - Callback registration and invocation

## Prerequisites

- Python 3.11+
- FastAPI knowledge
- Pydantic v2

---

## Task 1.1: Project Setup

### Description
Set up the Python package structure with pyproject.toml and basic configuration.

### Files to Create

**pyproject.toml**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "refast"
version = "0.1.0"
description = "Python + React UI framework for building reactive web applications"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [
    { name = "Your Name", email = "you@example.com" }
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Framework :: FastAPI",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "fastapi>=0.104.0",
    "pydantic>=2.0.0",
    "uvicorn>=0.24.0",
    "websockets>=12.0",
    "python-multipart>=0.0.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.25.0",
    "ruff>=0.1.0",
]
redis = [
    "redis>=5.0.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

**src/refast/__init__.py**
```python
"""
Refast - Python + React UI Framework

A framework for building reactive web applications with Python-first development.
"""

from refast.app import RefastApp
from refast.context import Context
from refast.state import State

__version__ = "0.1.0"
__all__ = ["RefastApp", "Context", "State"]
```

### Tests to Write

**tests/conftest.py** - Shared fixtures
**tests/unit/test_init.py** - Test imports work

### Acceptance Criteria

- [ ] `pip install -e .` works
- [ ] `from refast import RefastApp` works
- [ ] `pytest tests/` runs (even if empty)
- [ ] `ruff check src/` passes

---

## Task 1.2: RefastApp Class

### Description
Create the main application class that holds configuration and page definitions.

### Files to Create

**src/refast/app.py**

```python
"""Main RefastApp class."""

from typing import Any, Callable, TypeVar
from fastapi import APIRouter

from refast.router import RefastRouter
from refast.context import Context

PageFunc = TypeVar("PageFunc", bound=Callable[..., Any])


class RefastApp:
    """
    Main Refast application class.
    
    Example:
        ```python
        from refast import RefastApp
        
        ui = RefastApp(title="My App")
        
        @ui.page("/")
        def home(ctx: Context):
            return Container(Text("Hello World"))
        
        # Mount to FastAPI
        app.include_router(ui.router, prefix="/ui")
        ```
    
    Args:
        title: Application title
        theme: Theme configuration (default or custom)
        secret_key: Secret key for session encryption
        debug: Enable debug mode
    """
    
    def __init__(
        self,
        title: str = "Refast App",
        theme: str | dict[str, Any] | None = None,
        secret_key: str | None = None,
        debug: bool = False,
    ):
        self.title = title
        self.theme = theme
        self.secret_key = secret_key
        self.debug = debug
        
        self._pages: dict[str, Callable] = {}
        self._callbacks: dict[str, Callable] = {}
        self._event_handlers: dict[str, Callable] = {}
        self._router: RefastRouter | None = None
    
    @property
    def router(self) -> APIRouter:
        """Get the FastAPI router for mounting."""
        if self._router is None:
            self._router = RefastRouter(self)
        return self._router.api_router
    
    @property
    def pages(self) -> dict[str, Callable]:
        """Get registered pages."""
        return self._pages.copy()
    
    def page(self, path: str) -> Callable[[PageFunc], PageFunc]:
        """
        Decorator to register a page.
        
        Args:
            path: URL path for the page
            
        Returns:
            Decorator function
            
        Example:
            ```python
            @ui.page("/dashboard")
            def dashboard(ctx: Context):
                return Container(...)
            ```
        """
        def decorator(func: PageFunc) -> PageFunc:
            self._pages[path] = func
            return func
        return decorator
    
    def on_event(self, event_type: str) -> Callable[[Callable], Callable]:
        """
        Decorator to register an event handler.
        
        Args:
            event_type: The event type to handle (e.g., "user:click")
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            self._event_handlers[event_type] = func
            return func
        return decorator
    
    def register_callback(self, callback_id: str, func: Callable) -> None:
        """Register a callback function."""
        self._callbacks[callback_id] = func
    
    def get_callback(self, callback_id: str) -> Callable | None:
        """Get a registered callback by ID."""
        return self._callbacks.get(callback_id)
```

### Tests to Write

**tests/unit/test_app.py**
```python
import pytest
from refast import RefastApp

class TestRefastApp:
    def test_create_with_defaults(self):
        app = RefastApp()
        assert app.title == "Refast App"
        assert app.debug is False
    
    def test_create_with_custom_title(self):
        app = RefastApp(title="Custom App")
        assert app.title == "Custom App"
    
    def test_page_decorator_registers_page(self):
        app = RefastApp()
        
        @app.page("/")
        def home(ctx):
            return None
        
        assert "/" in app.pages
        assert app.pages["/"] == home
    
    def test_multiple_pages(self):
        app = RefastApp()
        
        @app.page("/")
        def home(ctx):
            pass
        
        @app.page("/about")
        def about(ctx):
            pass
        
        assert len(app.pages) == 2
    
    def test_on_event_decorator(self):
        app = RefastApp()
        
        @app.on_event("user:click")
        def handle_click(ctx, event):
            pass
        
        assert "user:click" in app._event_handlers
    
    def test_router_property_returns_api_router(self):
        app = RefastApp()
        router = app.router
        assert router is not None
```

### Acceptance Criteria

- [ ] RefastApp can be instantiated with defaults
- [ ] Page decorator registers pages correctly
- [ ] Event handlers can be registered
- [ ] Router property returns FastAPI APIRouter

---

## Task 1.3: Router Integration

### Description
Create the FastAPI router that serves pages and handles WebSocket connections.

### Files to Create

**src/refast/router.py**

```python
"""FastAPI router integration for Refast."""

from typing import TYPE_CHECKING, Any
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

if TYPE_CHECKING:
    from refast.app import RefastApp


class RefastRouter:
    """
    FastAPI router that serves Refast pages.
    
    This router provides:
    - GET endpoints for each registered page
    - WebSocket endpoint for real-time updates
    - Static file serving for the React client
    """
    
    def __init__(self, app: "RefastApp"):
        self.app = app
        self.api_router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self) -> None:
        """Set up all routes."""
        # WebSocket endpoint
        self.api_router.add_api_websocket_route(
            "/ws",
            self._websocket_handler,
        )
        
        # Page routes are added dynamically
        self.api_router.add_api_route(
            "/{path:path}",
            self._page_handler,
            methods=["GET"],
            response_class=HTMLResponse,
        )
    
    async def _page_handler(self, request: Request, path: str = "") -> HTMLResponse:
        """Handle page requests."""
        from refast.context import Context
        
        # Normalize path
        page_path = f"/{path}" if not path.startswith("/") else path
        if page_path != "/" and page_path.endswith("/"):
            page_path = page_path.rstrip("/")
        
        # Find the page
        page_func = self.app._pages.get(page_path)
        if page_func is None:
            page_func = self.app._pages.get("/")  # Fallback to index
        
        if page_func is None:
            return HTMLResponse(content="<h1>404 - Page Not Found</h1>", status_code=404)
        
        # Create context and render page
        ctx = Context(request=request, app=self.app)
        component = page_func(ctx)
        
        # Render to HTML shell with component data
        html = self._render_html_shell(component, ctx)
        return HTMLResponse(content=html)
    
    async def _websocket_handler(self, websocket: WebSocket) -> None:
        """Handle WebSocket connections for real-time updates."""
        await websocket.accept()
        
        try:
            while True:
                data = await websocket.receive_json()
                # Process incoming events
                await self._handle_websocket_message(websocket, data)
        except WebSocketDisconnect:
            pass
    
    async def _handle_websocket_message(
        self, websocket: WebSocket, data: dict[str, Any]
    ) -> None:
        """Process incoming WebSocket messages."""
        message_type = data.get("type")
        
        if message_type == "callback":
            callback_id = data.get("callbackId")
            callback_data = data.get("data", {})
            
            callback = self.app.get_callback(callback_id)
            if callback:
                # Create context for callback
                from refast.context import Context
                ctx = Context(websocket=websocket, app=self.app)
                await callback(ctx, **callback_data)
        
        elif message_type == "event":
            event_type = data.get("eventType")
            handler = self.app._event_handlers.get(event_type)
            if handler:
                from refast.context import Context
                from refast.events.types import Event
                ctx = Context(websocket=websocket, app=self.app)
                event = Event(type=event_type, data=data.get("data", {}))
                await handler(ctx, event)
    
    def _render_html_shell(self, component: Any, ctx: "Context") -> str:
        """Render the HTML shell with embedded component data."""
        import json
        
        component_json = json.dumps(
            component.render() if hasattr(component, "render") else {}
        )
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.app.title}</title>
    <script>
        window.__REFAST_INITIAL_DATA__ = {component_json};
    </script>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/static/refast-client.js"></script>
</body>
</html>"""
```

### Tests to Write

**tests/unit/test_router.py**
```python
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from refast import RefastApp

class TestRefastRouter:
    def test_router_mounts_to_fastapi(self):
        app = FastAPI()
        ui = RefastApp()
        
        @ui.page("/")
        def home(ctx):
            return None
        
        app.include_router(ui.router, prefix="/ui")
        client = TestClient(app)
        
        response = client.get("/ui/")
        assert response.status_code == 200
    
    def test_page_not_found_returns_404(self):
        app = FastAPI()
        ui = RefastApp()
        app.include_router(ui.router, prefix="/ui")
        
        client = TestClient(app)
        response = client.get("/ui/nonexistent")
        assert response.status_code == 404
```

### Acceptance Criteria

- [ ] Router mounts to FastAPI app
- [ ] Page routes return HTML
- [ ] WebSocket endpoint accepts connections
- [ ] 404 returned for unknown pages

---

## Task 1.4: Context Class

### Description
Create the Context class that provides access to state, session, and update methods.

### Files to Create

**src/refast/context.py**

```python
"""Context class for request handling."""

from typing import TYPE_CHECKING, Any, Callable, Generic, TypeVar
from dataclasses import dataclass, field
import uuid

from fastapi import Request, WebSocket

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.session import Session

T = TypeVar("T")


@dataclass
class Callback:
    """
    Represents a callback that can be triggered from the frontend.
    
    Callbacks are serializable references to Python functions that
    the frontend can invoke via WebSocket.
    """
    
    id: str
    func: Callable
    bound_args: dict[str, Any] = field(default_factory=dict)
    
    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        return {
            "callbackId": self.id,
            "boundArgs": self.bound_args,
        }


class Context(Generic[T]):
    """
    Request context passed to page functions and callbacks.
    
    Provides access to:
    - State management
    - Session data
    - Component update methods
    - Callback creation
    
    Example:
        ```python
        @ui.page("/")
        def home(ctx: Context):
            count = ctx.state.get("count", 0)
            return Button(
                f"Count: {count}",
                on_click=ctx.callback(increment, amount=1)
            )
        
        async def increment(ctx: Context, amount: int):
            ctx.state["count"] = ctx.state.get("count", 0) + amount
            await ctx.push_update()
        ```
    """
    
    def __init__(
        self,
        request: Request | None = None,
        websocket: WebSocket | None = None,
        app: "RefastApp | None" = None,
    ):
        self._request = request
        self._websocket = websocket
        self._app = app
        self._state: dict[str, Any] = {}
        self._session: "Session | None" = None
        self._pending_updates: list[dict[str, Any]] = []
    
    @property
    def state(self) -> dict[str, Any]:
        """Access the state dictionary."""
        return self._state
    
    @property
    def session(self) -> "Session":
        """Access the session."""
        if self._session is None:
            from refast.session import Session
            self._session = Session()
        return self._session
    
    def callback(
        self,
        func: Callable,
        **bound_args: Any,
    ) -> Callback:
        """
        Create a callback that can be triggered from the frontend.
        
        Args:
            func: The function to call
            **bound_args: Arguments to bind to the callback
            
        Returns:
            Callback object that serializes for frontend
            
        Example:
            ```python
            Button(
                "Delete",
                on_click=ctx.callback(delete_item, item_id=item["id"])
            )
            ```
        """
        callback_id = str(uuid.uuid4())
        cb = Callback(id=callback_id, func=func, bound_args=bound_args)
        
        # Register with app
        if self._app:
            self._app.register_callback(callback_id, func)
        
        return cb
    
    async def push_update(self) -> None:
        """Push state updates to the frontend."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "state_update",
                "state": self._state,
            })
    
    async def replace(self, target_id: str, component: Any) -> None:
        """Replace a component in the frontend."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "update",
                "operation": "replace",
                "targetId": target_id,
                "component": component.render() if hasattr(component, "render") else component,
            })
    
    async def append(self, target_id: str, component: Any) -> None:
        """Append a component to a container."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "update",
                "operation": "append",
                "targetId": target_id,
                "component": component.render() if hasattr(component, "render") else component,
            })
    
    async def prepend(self, target_id: str, component: Any) -> None:
        """Prepend a component to a container."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "update",
                "operation": "prepend",
                "targetId": target_id,
                "component": component.render() if hasattr(component, "render") else component,
            })
    
    async def remove(self, target_id: str) -> None:
        """Remove a component from the frontend."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "update",
                "operation": "remove",
                "targetId": target_id,
            })
    
    async def update_props(self, target_id: str, props: dict[str, Any]) -> None:
        """Update props of an existing component."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "update",
                "operation": "update_props",
                "targetId": target_id,
                "props": props,
            })
    
    async def navigate(self, path: str) -> None:
        """Navigate to a different page."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "navigate",
                "path": path,
            })
    
    async def show_toast(
        self,
        message: str,
        variant: str = "default",
        duration: int = 3000,
    ) -> None:
        """Show a toast notification."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "toast",
                "message": message,
                "variant": variant,
                "duration": duration,
            })
    
    async def push_event(self, event_type: str, data: Any) -> None:
        """Push an event to the frontend."""
        if self._websocket:
            await self._websocket.send_json({
                "type": "event",
                "eventType": event_type,
                "data": data,
            })
    
    async def broadcast(self, event_type: str, data: Any) -> None:
        """Broadcast an event to all connected clients."""
        # This will be implemented in the events module
        pass
```

### Tests to Write

**tests/unit/test_context.py**
```python
import pytest
from refast.context import Context, Callback

class TestCallback:
    def test_callback_has_id(self):
        def my_func():
            pass
        cb = Callback(id="test-id", func=my_func)
        assert cb.id == "test-id"
    
    def test_callback_serialize(self):
        def my_func():
            pass
        cb = Callback(id="test-id", func=my_func, bound_args={"x": 1})
        serialized = cb.serialize()
        assert serialized["callbackId"] == "test-id"
        assert serialized["boundArgs"] == {"x": 1}

class TestContext:
    def test_state_is_dict(self):
        ctx = Context()
        assert isinstance(ctx.state, dict)
    
    def test_callback_creates_callback_object(self):
        ctx = Context()
        def my_handler():
            pass
        cb = ctx.callback(my_handler, item_id=123)
        assert isinstance(cb, Callback)
        assert cb.bound_args == {"item_id": 123}
    
    def test_callback_generates_unique_ids(self):
        ctx = Context()
        def handler():
            pass
        cb1 = ctx.callback(handler)
        cb2 = ctx.callback(handler)
        assert cb1.id != cb2.id
```

### Acceptance Criteria

- [ ] Context holds state and session
- [ ] Callbacks are serializable
- [ ] Update methods work with WebSocket
- [ ] Navigation and toast methods exist

---

## Task 1.5: State Management

### Description
Create the State class for typed state management.

### Files to Create

**src/refast/state.py**

```python
"""State management for Refast."""

from typing import Any, Generic, TypeVar, get_type_hints
from pydantic import BaseModel

T = TypeVar("T")


class State(Generic[T]):
    """
    State container with optional type validation.
    
    Can be used with a Pydantic model for typed state:
    
    Example:
        ```python
        class AppState(BaseModel):
            count: int = 0
            user: str | None = None
        
        @ui.page("/")
        def home(ctx: Context[AppState]):
            ctx.state.count += 1
            return Text(f"Count: {ctx.state.count}")
        ```
    
    Or as a simple dict:
        ```python
        ctx.state["count"] = 0
        ```
    """
    
    def __init__(self, initial: T | dict[str, Any] | None = None):
        if isinstance(initial, BaseModel):
            self._data = initial.model_dump()
            self._model_class = type(initial)
        elif isinstance(initial, dict):
            self._data = initial.copy()
            self._model_class = None
        else:
            self._data = {}
            self._model_class = None
    
    def __getitem__(self, key: str) -> Any:
        return self._data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value
    
    def __contains__(self, key: str) -> bool:
        return key in self._data
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value with optional default."""
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value."""
        self._data[key] = value
    
    def update(self, data: dict[str, Any]) -> None:
        """Update multiple values."""
        self._data.update(data)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self._data.copy()
    
    def validate(self) -> bool:
        """Validate against the model if one was provided."""
        if self._model_class:
            try:
                self._model_class(**self._data)
                return True
            except Exception:
                return False
        return True
```

### Tests to Write

**tests/unit/test_state.py**

```python
import pytest
from pydantic import BaseModel
from refast.state import State

class TestState:
    def test_state_as_dict(self):
        state = State()
        state["count"] = 0
        assert state["count"] == 0
    
    def test_state_get_with_default(self):
        state = State()
        assert state.get("missing", 42) == 42
    
    def test_state_contains(self):
        state = State({"key": "value"})
        assert "key" in state
        assert "missing" not in state
    
    def test_state_with_pydantic_model(self):
        class AppState(BaseModel):
            count: int = 0
            name: str = ""
        
        state = State(AppState())
        assert state["count"] == 0
        state["count"] = 5
        assert state["count"] == 5
    
    def test_state_to_dict(self):
        state = State({"a": 1, "b": 2})
        d = state.to_dict()
        assert d == {"a": 1, "b": 2}
```

### Acceptance Criteria

- [ ] State works as a dictionary
- [ ] State works with Pydantic models
- [ ] State is serializable
- [ ] State validation works

---

## Task 1.6: Tests Configuration

### Description
Set up pytest configuration and shared fixtures.

### Files to Create

**tests/__init__.py**
```python
"""Refast test suite."""
```

**tests/conftest.py**
```python
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
```

**tests/unit/__init__.py**
```python
"""Unit tests for Refast."""
```

### Acceptance Criteria

- [ ] `pytest tests/` runs successfully
- [ ] All fixtures work
- [ ] Test discovery works

---

## Final Checklist for Stage 1

- [ ] All files created
- [ ] All tests pass
- [ ] `ruff check src/` passes
- [ ] `pip install -e .` works
- [ ] Update `.github/copilot-instructions.md` status to 🟢
