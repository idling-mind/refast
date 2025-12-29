# Stage 7: Integration & Examples

## Progress

- [ ] Task 7.1: Full integration testing
- [ ] Task 7.2: Asset bundling
- [ ] Task 7.3: Basic example app
- [ ] Task 7.4: Todo app example
- [ ] Task 7.5: Chat app example
- [ ] Task 7.6: Dashboard example
- [ ] Task 7.7: E2E tests

## Objectives

Integrate all components and create working examples:
- Full end-to-end integration tests
- Bundle frontend assets with Python package
- Create example applications demonstrating features
- Playwright-based E2E testing

## Prerequisites

- All previous stages complete
- Playwright installed for E2E tests

---

## Task 7.1: Full Integration Testing

### Description
Create comprehensive integration tests that test the full stack.

### Files to Create

**tests/integration/__init__.py**
```python
"""Integration tests for Refast."""
```

**tests/integration/test_full_flow.py**
```python
"""Full flow integration tests."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from refast import RefastApp, Context
from refast.components import Container, Text, Button, Input, Column
from refast.session.stores.memory import MemorySessionStore


class TestFullFlow:
    """Test complete user flows."""
    
    @pytest.fixture
    def ui_app(self):
        """Create a full Refast app."""
        ui = RefastApp(title="Test App", secret_key="test-secret")
        
        @ui.page("/")
        def home(ctx: Context):
            count = ctx.session.get("count", 0)
            return Container(
                id="main",
                children=[
                    Text(f"Count: {count}", id="count-display"),
                    Button(
                        "Increment",
                        id="increment-btn",
                        on_click=ctx.callback(increment),
                    ),
                ]
            )
        
        async def increment(ctx: Context):
            count = ctx.session.get("count", 0) + 1
            ctx.session.set("count", count)
            await ctx.replace("count-display", Text(f"Count: {count}"))
        
        return ui
    
    @pytest.fixture
    def fastapi_app(self, ui_app):
        """Mount to FastAPI."""
        app = FastAPI()
        store = MemorySessionStore()
        
        from refast.session.middleware import SessionMiddleware
        app.add_middleware(SessionMiddleware, store=store)
        
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
        assert "Count: 0" in response.text or "__REFAST_INITIAL_DATA__" in response.text
    
    def test_websocket_connects(self, client):
        """Test WebSocket connection."""
        with client.websocket_connect("/ui/ws") as websocket:
            # Connection should be established
            assert websocket is not None


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
                                ]
                            ),
                        ]
                    )
                ]
            )
        
        app = FastAPI()
        app.include_router(ui.router)
        
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200


class TestCallbackFlow:
    """Test callback invocation flow."""
    
    @pytest.fixture
    def callback_app(self):
        """Create app with callbacks."""
        ui = RefastApp()
        ui._callback_results = []
        
        @ui.page("/")
        def home(ctx: Context):
            return Button(
                "Click",
                on_click=ctx.callback(handle_click, value="test"),
            )
        
        async def handle_click(ctx: Context, value: str):
            ui._callback_results.append(value)
        
        return ui
    
    def test_callback_registered(self, callback_app):
        """Test that callbacks are registered."""
        app = FastAPI()
        app.include_router(callback_app.router)
        
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        
        # Check that callback was registered
        assert len(callback_app._callbacks) > 0
```

**tests/integration/test_fastapi_integration.py**
```python
"""Test FastAPI integration."""

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from refast import RefastApp


class TestFastAPIIntegration:
    """Test integration with existing FastAPI apps."""
    
    def test_mount_to_existing_app(self):
        """Test mounting Refast to existing FastAPI app."""
        # Existing FastAPI app with routes
        app = FastAPI()
        
        @app.get("/api/health")
        def health():
            return {"status": "healthy"}
        
        # Add Refast
        ui = RefastApp()
        
        @ui.page("/")
        def home(ctx):
            from refast.components import Text
            return Text("Hello from Refast")
        
        app.include_router(ui.router, prefix="/ui")
        
        client = TestClient(app)
        
        # Original API still works
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
        # Refast UI works
        response = client.get("/ui/")
        assert response.status_code == 200
    
    def test_multiple_refast_apps(self):
        """Test multiple Refast apps in one FastAPI app."""
        app = FastAPI()
        
        # Admin UI
        admin_ui = RefastApp(title="Admin")
        
        @admin_ui.page("/")
        def admin_home(ctx):
            from refast.components import Text
            return Text("Admin Dashboard")
        
        # Public UI
        public_ui = RefastApp(title="Public")
        
        @public_ui.page("/")
        def public_home(ctx):
            from refast.components import Text
            return Text("Welcome")
        
        app.include_router(admin_ui.router, prefix="/admin")
        app.include_router(public_ui.router, prefix="/app")
        
        client = TestClient(app)
        
        admin_response = client.get("/admin/")
        assert admin_response.status_code == 200
        
        public_response = client.get("/app/")
        assert public_response.status_code == 200
    
    def test_shared_dependencies(self):
        """Test using FastAPI dependencies with Refast."""
        app = FastAPI()
        
        # Dependency
        def get_user(request: Request):
            return {"id": 1, "name": "Test User"}
        
        ui = RefastApp()
        
        @ui.page("/")
        def home(ctx):
            from refast.components import Text
            # Access FastAPI request
            user = get_user(ctx._request)
            return Text(f"Hello, {user['name']}")
        
        app.include_router(ui.router)
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
```

### Acceptance Criteria

- [ ] Full flow tests pass
- [ ] Component rendering tests pass
- [ ] Callback tests pass
- [ ] FastAPI integration tests pass

---

## Task 7.2: Asset Bundling

### Description
Bundle frontend assets with Python package.

### Files to Create

**src/refast/static/__init__.py**
```python
"""Static asset management."""

from pathlib import Path

STATIC_DIR = Path(__file__).parent / "dist"


def get_static_dir() -> Path:
    """Get the path to static assets."""
    return STATIC_DIR


def get_client_js() -> str:
    """Get the path to the client JavaScript bundle."""
    js_file = STATIC_DIR / "refast-client.js"
    if js_file.exists():
        return str(js_file)
    raise FileNotFoundError("Client bundle not found. Run 'npm run build' in src/refast-client/")
```

**scripts/build.py**
```python
#!/usr/bin/env python3
"""Build script for Refast package."""

import subprocess
import shutil
from pathlib import Path


def build_frontend():
    """Build the frontend client."""
    client_dir = Path(__file__).parent.parent / "src" / "refast-client"
    
    # Install dependencies
    print("Installing frontend dependencies...")
    subprocess.run(["npm", "install"], cwd=client_dir, check=True)
    
    # Build
    print("Building frontend...")
    subprocess.run(["npm", "run", "build"], cwd=client_dir, check=True)
    
    # Copy to static
    dist_dir = client_dir / "dist"
    static_dir = Path(__file__).parent.parent / "src" / "refast" / "static" / "dist"
    
    print(f"Copying assets to {static_dir}")
    if static_dir.exists():
        shutil.rmtree(static_dir)
    shutil.copytree(dist_dir, static_dir)
    
    print("Frontend build complete!")


def build_package():
    """Build the Python package."""
    print("Building Python package...")
    subprocess.run(["python", "-m", "build"], check=True)
    print("Package build complete!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "frontend":
            build_frontend()
        elif sys.argv[1] == "package":
            build_package()
        elif sys.argv[1] == "all":
            build_frontend()
            build_package()
    else:
        build_frontend()
```

Update **pyproject.toml** to include static files:
```toml
[tool.hatch.build]
include = [
    "src/refast/**/*.py",
    "src/refast/static/dist/**/*",
]
```

### Acceptance Criteria

- [ ] Frontend builds to dist
- [ ] Assets copied to package
- [ ] Package includes static files

---

## Task 7.3: Basic Example App

### Description
Create a simple example application.

### Files to Create

**examples/basic/app.py**
```python
"""Basic Refast example application."""

from fastapi import FastAPI
import uvicorn

from refast import RefastApp, Context
from refast.components import (
    Container,
    Column,
    Row,
    Text,
    Button,
    Input,
    Card,
    CardHeader,
    CardContent,
    Heading,
)
from refast.session.middleware import SessionMiddleware
from refast.session.stores.memory import MemorySessionStore


# Create FastAPI app
app = FastAPI(title="Basic Refast Example")

# Add session middleware
store = MemorySessionStore()
app.add_middleware(SessionMiddleware, store=store)

# Create Refast UI
ui = RefastApp(title="Basic Example", secret_key="example-secret")


@ui.page("/")
def home(ctx: Context):
    """Home page."""
    name = ctx.session.get("name", "World")
    
    return Container(
        class_name="max-w-2xl mx-auto p-4",
        children=[
            Card(
                children=[
                    CardHeader(title="Welcome to Refast!"),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Text(f"Hello, {name}!", class_name="text-2xl"),
                                    Row(
                                        gap=2,
                                        children=[
                                            Input(
                                                name="name",
                                                placeholder="Enter your name",
                                                id="name-input",
                                            ),
                                            Button(
                                                "Update",
                                                on_click=ctx.callback(update_name),
                                            ),
                                        ]
                                    ),
                                ]
                            )
                        ]
                    ),
                ]
            ),
        ]
    )


async def update_name(ctx: Context, value: str = ""):
    """Update the user's name."""
    if value:
        ctx.session.set("name", value)
        await ctx.show_toast(f"Hello, {value}!")
        # Refresh the page
        await ctx.navigate("/")


@ui.page("/about")
def about(ctx: Context):
    """About page."""
    return Container(
        class_name="max-w-2xl mx-auto p-4",
        children=[
            Heading("About", level=1),
            Text("This is a basic Refast example application."),
            Button(
                "Back to Home",
                on_click=ctx.callback(lambda ctx: ctx.navigate("/")),
            ),
        ]
    )


# Mount Refast to FastAPI
app.include_router(ui.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**examples/basic/README.md**
```markdown
# Basic Refast Example

A simple example showing basic Refast features.

## Features Demonstrated

- Page routing
- Session management
- Callbacks
- Component composition
- Navigation

## Running

```bash
cd examples/basic
pip install -e ../../
uvicorn app:app --reload
```

Then open http://localhost:8000
```

### Acceptance Criteria

- [ ] Example runs
- [ ] Page loads
- [ ] Name update works
- [ ] Navigation works

---

## Task 7.4: Todo App Example

### Description
Create a todo list application example.

### Files to Create

**examples/todo_app/app.py**
```python
"""Todo App - Refast Example."""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
import uuid

from refast import RefastApp, Context
from refast.components import (
    Container,
    Column,
    Row,
    Text,
    Button,
    Input,
    Checkbox,
    Card,
    CardHeader,
    CardContent,
    CardFooter,
    Heading,
    IconButton,
    Divider,
)
from refast.session.middleware import SessionMiddleware
from refast.session.stores.memory import MemorySessionStore


# Data models
class Todo(BaseModel):
    id: str
    text: str
    completed: bool = False


# Create FastAPI app
app = FastAPI(title="Todo App")
store = MemorySessionStore()
app.add_middleware(SessionMiddleware, store=store)

# Create Refast UI
ui = RefastApp(title="Todo App")


def get_todos(ctx: Context) -> list[dict]:
    """Get todos from session."""
    return ctx.session.get("todos", [])


def save_todos(ctx: Context, todos: list[dict]) -> None:
    """Save todos to session."""
    ctx.session.set("todos", todos)


@ui.page("/")
def home(ctx: Context):
    """Main todo list page."""
    todos = get_todos(ctx)
    completed_count = sum(1 for t in todos if t["completed"])
    
    return Container(
        class_name="max-w-xl mx-auto p-4",
        children=[
            Card(
                children=[
                    CardHeader(
                        title="My Todo List",
                        description=f"{len(todos)} items, {completed_count} completed"
                    ),
                    CardContent(
                        children=[
                            # Add new todo input
                            Row(
                                gap=2,
                                class_name="mb-4",
                                children=[
                                    Input(
                                        name="new_todo",
                                        placeholder="What needs to be done?",
                                        id="new-todo-input",
                                    ),
                                    Button(
                                        "Add",
                                        variant="primary",
                                        on_click=ctx.callback(add_todo),
                                    ),
                                ]
                            ),
                            Divider(),
                            # Todo list
                            Column(
                                id="todo-list",
                                gap=2,
                                class_name="mt-4",
                                children=[
                                    render_todo_item(ctx, todo)
                                    for todo in todos
                                ],
                            ),
                        ]
                    ),
                    CardFooter(
                        children=[
                            Row(
                                justify="between",
                                children=[
                                    Button(
                                        "Clear Completed",
                                        variant="outline",
                                        on_click=ctx.callback(clear_completed),
                                    ),
                                    Button(
                                        "Clear All",
                                        variant="destructive",
                                        on_click=ctx.callback(clear_all),
                                    ),
                                ]
                            )
                        ]
                    ),
                ]
            ),
        ]
    )


def render_todo_item(ctx: Context, todo: dict) -> Container:
    """Render a single todo item."""
    return Container(
        id=f"todo-{todo['id']}",
        class_name="flex items-center gap-2 p-2 rounded hover:bg-gray-50",
        children=[
            Checkbox(
                checked=todo["completed"],
                on_change=ctx.callback(toggle_todo, todo_id=todo["id"]),
            ),
            Text(
                todo["text"],
                class_name="flex-1" + (" line-through text-gray-500" if todo["completed"] else ""),
            ),
            IconButton(
                icon="trash",
                variant="ghost",
                aria_label="Delete",
                on_click=ctx.callback(delete_todo, todo_id=todo["id"]),
            ),
        ]
    )


async def add_todo(ctx: Context, value: str = ""):
    """Add a new todo item."""
    if not value.strip():
        await ctx.show_toast("Please enter a todo item", variant="error")
        return
    
    todos = get_todos(ctx)
    new_todo = {
        "id": str(uuid.uuid4()),
        "text": value.strip(),
        "completed": False,
    }
    todos.append(new_todo)
    save_todos(ctx, todos)
    
    # Add to list
    await ctx.append("todo-list", render_todo_item(ctx, new_todo))
    await ctx.show_toast("Todo added!")


async def toggle_todo(ctx: Context, todo_id: str, checked: bool = False):
    """Toggle todo completion status."""
    todos = get_todos(ctx)
    
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = checked
            break
    
    save_todos(ctx, todos)
    
    # Update the item
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo:
        await ctx.replace(f"todo-{todo_id}", render_todo_item(ctx, todo))


async def delete_todo(ctx: Context, todo_id: str):
    """Delete a todo item."""
    todos = get_todos(ctx)
    todos = [t for t in todos if t["id"] != todo_id]
    save_todos(ctx, todos)
    
    await ctx.remove(f"todo-{todo_id}")
    await ctx.show_toast("Todo deleted")


async def clear_completed(ctx: Context):
    """Clear all completed todos."""
    todos = get_todos(ctx)
    completed_ids = [t["id"] for t in todos if t["completed"]]
    todos = [t for t in todos if not t["completed"]]
    save_todos(ctx, todos)
    
    for todo_id in completed_ids:
        await ctx.remove(f"todo-{todo_id}")
    
    await ctx.show_toast(f"Cleared {len(completed_ids)} completed items")


async def clear_all(ctx: Context):
    """Clear all todos."""
    todos = get_todos(ctx)
    save_todos(ctx, [])
    
    for todo in todos:
        await ctx.remove(f"todo-{todo['id']}")
    
    await ctx.show_toast("All todos cleared")


# Mount
app.include_router(ui.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Acceptance Criteria

- [ ] Can add todos
- [ ] Can toggle completion
- [ ] Can delete todos
- [ ] Clear completed works
- [ ] State persists in session

---

## Task 7.5: Chat App Example

### Description
Create a real-time chat application example.

### Files to Create

**examples/chat_app/app.py**
```python
"""Real-time Chat App - Refast Example."""

from fastapi import FastAPI
from datetime import datetime
import uvicorn
import uuid

from refast import RefastApp, Context
from refast.components import (
    Container,
    Column,
    Row,
    Text,
    Button,
    Input,
    Card,
    CardHeader,
    CardContent,
    Avatar,
    Divider,
    Slot,
)
from refast.session.middleware import SessionMiddleware
from refast.session.stores.memory import MemorySessionStore


# In-memory message store (shared across all sessions)
messages: list[dict] = []

# Create FastAPI app
app = FastAPI(title="Chat App")
store = MemorySessionStore()
app.add_middleware(SessionMiddleware, store=store)

# Create Refast UI
ui = RefastApp(title="Chat App")


@ui.page("/")
def chat_room(ctx: Context):
    """Main chat room."""
    username = ctx.session.get("username")
    
    if not username:
        return login_page(ctx)
    
    return Container(
        class_name="max-w-2xl mx-auto h-screen flex flex-col p-4",
        children=[
            # Header
            Card(
                class_name="mb-4",
                children=[
                    CardHeader(
                        title="Chat Room",
                        description=f"Logged in as {username}",
                    ),
                ]
            ),
            # Messages
            Card(
                class_name="flex-1 overflow-hidden flex flex-col",
                children=[
                    CardContent(
                        class_name="flex-1 overflow-y-auto",
                        children=[
                            Column(
                                id="message-list",
                                gap=2,
                                children=[
                                    render_message(msg, username)
                                    for msg in messages[-50:]  # Last 50 messages
                                ],
                            ),
                        ]
                    ),
                    Divider(),
                    # Input
                    CardContent(
                        children=[
                            Row(
                                gap=2,
                                children=[
                                    Input(
                                        name="message",
                                        placeholder="Type a message...",
                                        id="message-input",
                                        class_name="flex-1",
                                    ),
                                    Button(
                                        "Send",
                                        variant="primary",
                                        on_click=ctx.callback(send_message),
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )


def login_page(ctx: Context):
    """Login/username selection page."""
    return Container(
        class_name="max-w-md mx-auto mt-20 p-4",
        children=[
            Card(
                children=[
                    CardHeader(
                        title="Join Chat",
                        description="Enter a username to join the chat room",
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Input(
                                        name="username",
                                        placeholder="Your username",
                                        id="username-input",
                                    ),
                                    Button(
                                        "Join Chat",
                                        variant="primary",
                                        on_click=ctx.callback(join_chat),
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )


def render_message(msg: dict, current_user: str) -> Container:
    """Render a chat message."""
    is_own = msg["username"] == current_user
    
    return Container(
        id=f"msg-{msg['id']}",
        class_name=f"flex {'justify-end' if is_own else 'justify-start'}",
        children=[
            Row(
                gap=2,
                class_name=f"max-w-[80%] {'flex-row-reverse' if is_own else ''}",
                children=[
                    Avatar(name=msg["username"][0].upper()),
                    Column(
                        children=[
                            Text(
                                msg["username"],
                                class_name="text-xs text-gray-500",
                            ),
                            Container(
                                class_name=f"p-2 rounded-lg {'bg-blue-500 text-white' if is_own else 'bg-gray-200'}",
                                children=[Text(msg["text"])],
                            ),
                            Text(
                                msg["timestamp"],
                                class_name="text-xs text-gray-400",
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )


async def join_chat(ctx: Context, value: str = ""):
    """Handle user joining chat."""
    username = value.strip()
    if not username:
        await ctx.show_toast("Please enter a username", variant="error")
        return
    
    ctx.session.set("username", username)
    
    # Add system message
    system_msg = {
        "id": str(uuid.uuid4()),
        "username": "System",
        "text": f"{username} joined the chat",
        "timestamp": datetime.now().strftime("%H:%M"),
    }
    messages.append(system_msg)
    
    # Broadcast to all users
    await ctx.broadcast("chat:message", system_msg)
    
    # Refresh page
    await ctx.navigate("/")


async def send_message(ctx: Context, value: str = ""):
    """Send a chat message."""
    text = value.strip()
    if not text:
        return
    
    username = ctx.session.get("username", "Anonymous")
    
    msg = {
        "id": str(uuid.uuid4()),
        "username": username,
        "text": text,
        "timestamp": datetime.now().strftime("%H:%M"),
    }
    messages.append(msg)
    
    # Broadcast to all connected clients
    await ctx.broadcast("chat:message", msg)


# Event handler for incoming chat messages
@ui.on_event("chat:message")
async def on_chat_message(ctx: Context, event):
    """Handle incoming chat message broadcast."""
    msg = event.data
    username = ctx.session.get("username", "")
    
    # Append message to list
    await ctx.append("message-list", render_message(msg, username))


# Mount
app.include_router(ui.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Acceptance Criteria

- [ ] Users can join with username
- [ ] Messages send and display
- [ ] Real-time updates via broadcast
- [ ] Multiple users work

---

## Task 7.6: Dashboard Example

### Description
Create a data dashboard example.

### Files to Create

**examples/dashboard/app.py**
```python
"""Dashboard - Refast Example."""

from fastapi import FastAPI
import uvicorn
import random

from refast import RefastApp, Context
from refast.components import (
    Container,
    Column,
    Row,
    Grid,
    Text,
    Button,
    Card,
    CardHeader,
    CardContent,
    Heading,
    Badge,
    Progress,
    Tabs,
    TabItem,
    DataTable,
)
from refast.session.middleware import SessionMiddleware
from refast.session.stores.memory import MemorySessionStore


# Create FastAPI app
app = FastAPI(title="Dashboard")
store = MemorySessionStore()
app.add_middleware(SessionMiddleware, store=store)

# Create Refast UI
ui = RefastApp(title="Dashboard")


def generate_stats():
    """Generate random stats for demo."""
    return {
        "users": random.randint(1000, 5000),
        "revenue": random.randint(10000, 50000),
        "orders": random.randint(100, 500),
        "conversion": random.uniform(2.0, 5.0),
    }


def generate_chart_data():
    """Generate random chart data."""
    return [
        {"month": "Jan", "value": random.randint(100, 500)},
        {"month": "Feb", "value": random.randint(100, 500)},
        {"month": "Mar", "value": random.randint(100, 500)},
        {"month": "Apr", "value": random.randint(100, 500)},
        {"month": "May", "value": random.randint(100, 500)},
        {"month": "Jun", "value": random.randint(100, 500)},
    ]


@ui.page("/")
def dashboard(ctx: Context):
    """Main dashboard page."""
    stats = generate_stats()
    
    return Container(
        class_name="p-6",
        children=[
            # Header
            Row(
                justify="between",
                align="center",
                class_name="mb-6",
                children=[
                    Heading("Dashboard", level=1),
                    Button(
                        "Refresh Data",
                        on_click=ctx.callback(refresh_data),
                    ),
                ]
            ),
            
            # Stats cards
            Grid(
                columns=4,
                gap=4,
                class_name="mb-6",
                id="stats-grid",
                children=[
                    stat_card("Total Users", f"{stats['users']:,}", "+12%", "up"),
                    stat_card("Revenue", f"${stats['revenue']:,}", "+8%", "up"),
                    stat_card("Orders", f"{stats['orders']}", "-3%", "down"),
                    stat_card("Conversion", f"{stats['conversion']:.1f}%", "+0.5%", "up"),
                ]
            ),
            
            # Tabs
            Tabs(
                id="main-tabs",
                children=[
                    TabItem(
                        label="Overview",
                        children=[overview_tab(ctx)],
                    ),
                    TabItem(
                        label="Analytics",
                        children=[analytics_tab(ctx)],
                    ),
                    TabItem(
                        label="Reports",
                        children=[reports_tab(ctx)],
                    ),
                ]
            ),
        ]
    )


def stat_card(title: str, value: str, change: str, direction: str) -> Card:
    """Create a statistics card."""
    return Card(
        children=[
            CardContent(
                children=[
                    Column(
                        gap=2,
                        children=[
                            Text(title, class_name="text-sm text-gray-500"),
                            Text(value, class_name="text-2xl font-bold"),
                            Row(
                                gap=1,
                                children=[
                                    Badge(
                                        change,
                                        variant="success" if direction == "up" else "destructive",
                                    ),
                                    Text(
                                        "vs last month",
                                        class_name="text-xs text-gray-400",
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )


def overview_tab(ctx: Context) -> Container:
    """Overview tab content."""
    return Container(
        class_name="mt-4",
        children=[
            Grid(
                columns=2,
                gap=4,
                children=[
                    Card(
                        children=[
                            CardHeader(title="Revenue Trend"),
                            CardContent(
                                children=[
                                    # Placeholder for chart
                                    Container(
                                        class_name="h-64 bg-gray-100 rounded flex items-center justify-center",
                                        children=[Text("Chart placeholder")],
                                    ),
                                ]
                            ),
                        ]
                    ),
                    Card(
                        children=[
                            CardHeader(title="Recent Activity"),
                            CardContent(
                                children=[
                                    Column(
                                        gap=2,
                                        children=[
                                            activity_item("New order #1234", "2 min ago"),
                                            activity_item("User signup", "5 min ago"),
                                            activity_item("Payment received", "12 min ago"),
                                            activity_item("Order shipped", "1 hour ago"),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )


def activity_item(title: str, time: str) -> Row:
    """Render an activity item."""
    return Row(
        justify="between",
        class_name="py-2 border-b",
        children=[
            Text(title),
            Text(time, class_name="text-sm text-gray-500"),
        ]
    )


def analytics_tab(ctx: Context) -> Container:
    """Analytics tab content."""
    return Container(
        class_name="mt-4",
        children=[
            Card(
                children=[
                    CardHeader(title="Traffic Sources"),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    progress_item("Direct", 45),
                                    progress_item("Organic Search", 30),
                                    progress_item("Social Media", 15),
                                    progress_item("Referral", 10),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )


def progress_item(label: str, value: int) -> Column:
    """Render a progress item."""
    return Column(
        gap=1,
        children=[
            Row(
                justify="between",
                children=[
                    Text(label),
                    Text(f"{value}%"),
                ]
            ),
            Progress(value=value),
        ]
    )


def reports_tab(ctx: Context) -> Container:
    """Reports tab content."""
    data = [
        {"id": 1, "name": "Q1 Report", "date": "2024-03-31", "status": "Complete"},
        {"id": 2, "name": "Q2 Report", "date": "2024-06-30", "status": "In Progress"},
        {"id": 3, "name": "Annual Report", "date": "2024-12-31", "status": "Scheduled"},
    ]
    
    return Container(
        class_name="mt-4",
        children=[
            Card(
                children=[
                    CardHeader(
                        title="Generated Reports",
                        description="Download and manage your reports",
                    ),
                    CardContent(
                        children=[
                            DataTable(
                                data=data,
                                columns=[
                                    {"key": "name", "label": "Report Name"},
                                    {"key": "date", "label": "Date"},
                                    {"key": "status", "label": "Status"},
                                ],
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )


async def refresh_data(ctx: Context):
    """Refresh dashboard data."""
    stats = generate_stats()
    
    # Update stats grid
    await ctx.replace(
        "stats-grid",
        Grid(
            columns=4,
            gap=4,
            id="stats-grid",
            children=[
                stat_card("Total Users", f"{stats['users']:,}", "+12%", "up"),
                stat_card("Revenue", f"${stats['revenue']:,}", "+8%", "up"),
                stat_card("Orders", f"{stats['orders']}", "-3%", "down"),
                stat_card("Conversion", f"{stats['conversion']:.1f}%", "+0.5%", "up"),
            ]
        )
    )
    
    await ctx.show_toast("Data refreshed!")


# Mount
app.include_router(ui.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Acceptance Criteria

- [ ] Dashboard renders
- [ ] Stats display
- [ ] Tabs work
- [ ] Refresh updates data

---

## Task 7.7: E2E Tests

### Description
Create Playwright E2E tests.

### Files to Create

**tests/e2e/playwright.config.ts**
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './specs',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:8000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'python -m examples.basic.app',
    url: 'http://localhost:8000',
    reuseExistingServer: !process.env.CI,
  },
});
```

**tests/e2e/specs/basic.spec.ts**
```typescript
import { test, expect } from '@playwright/test';

test.describe('Basic Example', () => {
  test('loads the home page', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Refast/);
  });

  test('shows welcome message', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('text=Hello')).toBeVisible();
  });

  test('updates name on input', async ({ page }) => {
    await page.goto('/');
    
    // Enter a name
    await page.fill('#name-input', 'Alice');
    await page.click('text=Update');
    
    // Wait for update
    await expect(page.locator('text=Hello, Alice')).toBeVisible();
  });
});
```

**tests/e2e/specs/events.spec.ts**
```typescript
import { test, expect } from '@playwright/test';

test.describe('Event Handling', () => {
  test('WebSocket connects', async ({ page }) => {
    await page.goto('/');
    
    // Check for connected state
    const app = page.locator('.refast-app');
    await expect(app).toHaveAttribute('data-connected', 'true');
  });

  test('callback triggers update', async ({ page }) => {
    await page.goto('/');
    
    // Click a button
    const button = page.locator('#increment-btn');
    await button.click();
    
    // Wait for update
    await page.waitForTimeout(500);
    
    // Check update occurred
    // (specific assertions depend on the app)
  });
});
```

### Acceptance Criteria

- [ ] Playwright configured
- [ ] Basic tests pass
- [ ] Event tests pass
- [ ] CI integration ready

---

## Final Checklist for Stage 7

- [ ] Integration tests complete
- [ ] Asset bundling works
- [ ] Basic example works
- [ ] Todo example works
- [ ] Chat example works
- [ ] Dashboard example works
- [ ] E2E tests pass
- [ ] Update `.github/copilot-instructions.md` status to 🟢
