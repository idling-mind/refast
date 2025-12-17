# Stage 8: Documentation

## Progress

- [ ] Task 8.1: Docs app structure
- [ ] Task 8.2: Custom documentation components
- [ ] Task 8.3: Home page
- [ ] Task 8.4: Getting started guide
- [ ] Task 8.5: Components reference
- [ ] Task 8.6: Events guide
- [ ] Task 8.7: Sessions guide
- [ ] Task 8.8: Security guide
- [ ] Task 8.9: API reference generation
- [ ] Task 8.10: Deployment

## Objectives

Build documentation using Refast itself (self-documenting):
- Create documentation app with Refast
- Custom components for docs (code blocks, API docs, examples)
- Comprehensive guides and references
- Deployable static/dynamic site

## Prerequisites

- All previous stages complete
- Examples working

---

## Task 8.1: Docs App Structure

### Description
Set up the documentation application structure.

### Files to Create

**docs/app.py**
```python
"""Refast Documentation - Built with Refast."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from refast import RefastApp, Context
from refast.components import (
    Container,
    Column,
    Row,
    Text,
    Button,
    Heading,
    Link,
)
from refast.theme import Theme

from docs.components.layout import DocsLayout, Sidebar, NavItem
from docs.pages import (
    home,
    getting_started,
    components,
    events,
    sessions,
    security,
    api_reference,
)


# Create FastAPI app
app = FastAPI(title="Refast Documentation")

# Create Refast UI with custom theme
theme = Theme(
    primary="#3B82F6",  # Blue
    secondary="#10B981",  # Green
    font_family="Inter, system-ui, sans-serif",
)

ui = RefastApp(
    title="Refast Documentation",
    theme=theme,
)


# Navigation structure
NAV_ITEMS = [
    NavItem(label="Home", path="/"),
    NavItem(label="Getting Started", path="/getting-started"),
    NavItem(
        label="Guides",
        children=[
            NavItem(label="Components", path="/components"),
            NavItem(label="Events", path="/events"),
            NavItem(label="Sessions", path="/sessions"),
            NavItem(label="Security", path="/security"),
        ]
    ),
    NavItem(label="API Reference", path="/api"),
]


def with_layout(page_fn):
    """Wrap a page function with the docs layout."""
    def wrapper(ctx: Context):
        content = page_fn(ctx)
        return DocsLayout(
            nav_items=NAV_ITEMS,
            children=[content],
        )
    return wrapper


# Register pages
@ui.page("/")
@with_layout
def index(ctx: Context):
    return home.render(ctx)


@ui.page("/getting-started")
@with_layout
def getting_started_page(ctx: Context):
    return getting_started.render(ctx)


@ui.page("/components")
@with_layout
def components_page(ctx: Context):
    return components.render(ctx)


@ui.page("/events")
@with_layout
def events_page(ctx: Context):
    return events.render(ctx)


@ui.page("/sessions")
@with_layout
def sessions_page(ctx: Context):
    return sessions.render(ctx)


@ui.page("/security")
@with_layout
def security_page(ctx: Context):
    return security.render(ctx)


@ui.page("/api")
@with_layout
def api_page(ctx: Context):
    return api_reference.render(ctx)


# Mount
app.include_router(ui.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
```

**docs/__init__.py**
```python
"""Refast Documentation package."""
```

**docs/pages/__init__.py**
```python
"""Documentation pages."""

from docs.pages import (
    home,
    getting_started,
    components,
    events,
    sessions,
    security,
    api_reference,
)

__all__ = [
    "home",
    "getting_started",
    "components",
    "events",
    "sessions",
    "security",
    "api_reference",
]
```

**docs/components/__init__.py**
```python
"""Custom documentation components."""

from docs.components.code_block import CodeBlock
from docs.components.api_doc import APIDoc, ParamDoc
from docs.components.example import Example
from docs.components.layout import DocsLayout, Sidebar, NavItem

__all__ = [
    "CodeBlock",
    "APIDoc",
    "ParamDoc",
    "Example",
    "DocsLayout",
    "Sidebar",
    "NavItem",
]
```

### Acceptance Criteria

- [ ] Docs app structure created
- [ ] Navigation defined
- [ ] Layout wrapper works
- [ ] App runs

---

## Task 8.2: Custom Documentation Components

### Description
Create custom components for documentation.

### Files to Create

**docs/components/code_block.py**
```python
"""Code block component with syntax highlighting."""

from refast.components.base import Component
from typing import Any


class CodeBlock(Component):
    """
    Code block with syntax highlighting.
    
    Uses Prism.js or highlight.js on the frontend.
    
    Example:
        ```python
        CodeBlock(
            code='print("Hello")',
            language="python",
            show_line_numbers=True,
        )
        ```
    """
    
    component_type: str = "CodeBlock"
    
    def __init__(
        self,
        code: str,
        language: str = "python",
        title: str | None = None,
        show_line_numbers: bool = False,
        highlight_lines: list[int] | None = None,
        copyable: bool = True,
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
        self.code = code
        self.language = language
        self.title = title
        self.show_line_numbers = show_line_numbers
        self.highlight_lines = highlight_lines or []
        self.copyable = copyable
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "code": self.code,
                "language": self.language,
                "title": self.title,
                "showLineNumbers": self.show_line_numbers,
                "highlightLines": self.highlight_lines,
                "copyable": self.copyable,
                "className": self.class_name,
            },
        }
```

**docs/components/api_doc.py**
```python
"""API documentation components."""

from refast.components.base import Component
from refast.components import Container, Column, Row, Text, Badge, Divider
from typing import Any
from pydantic import BaseModel


class ParamDoc(BaseModel):
    """Documentation for a parameter."""
    name: str
    type: str
    description: str
    required: bool = True
    default: str | None = None


class APIDoc(Component):
    """
    API documentation block for a function/class.
    
    Example:
        ```python
        APIDoc(
            name="RefastApp",
            kind="class",
            signature="RefastApp(title: str = 'Refast App', ...)",
            description="Main Refast application class.",
            params=[
                ParamDoc(name="title", type="str", description="App title"),
            ],
        )
        ```
    """
    
    component_type: str = "APIDoc"
    
    def __init__(
        self,
        name: str,
        kind: str,  # "function", "class", "method"
        signature: str,
        description: str,
        params: list[ParamDoc] | None = None,
        returns: str | None = None,
        raises: list[str] | None = None,
        examples: list[str] | None = None,
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
        self.name = name
        self.kind = kind
        self.signature = signature
        self.description = description
        self.params = params or []
        self.returns = returns
        self.raises = raises or []
        self.examples = examples or []
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "kind": self.kind,
                "signature": self.signature,
                "description": self.description,
                "params": [p.model_dump() for p in self.params],
                "returns": self.returns,
                "raises": self.raises,
                "examples": self.examples,
                "className": self.class_name,
            },
        }
```

**docs/components/example.py**
```python
"""Interactive example component."""

from refast.components.base import Component
from refast.components import Container, Column, Row, Text, Button, Tabs, TabItem
from typing import Any, Callable

from docs.components.code_block import CodeBlock


class Example(Component):
    """
    Interactive example with code and live preview.
    
    Example:
        ```python
        Example(
            title="Button Example",
            code='''
            Button("Click me", on_click=ctx.callback(handle_click))
            ''',
            preview=Button("Click me"),
        )
        ```
    """
    
    component_type: str = "Example"
    
    def __init__(
        self,
        title: str,
        code: str,
        preview: Component | None = None,
        description: str | None = None,
        language: str = "python",
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
        self.title = title
        self.code = code
        self.preview = preview
        self.description = description
        self.language = language
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "code": self.code,
                "preview": self.preview.render() if self.preview else None,
                "description": self.description,
                "language": self.language,
                "className": self.class_name,
            },
        }
```

**docs/components/layout.py**
```python
"""Documentation layout components."""

from refast.components.base import Component
from refast.components import Container, Column, Row, Text, Link
from typing import Any
from pydantic import BaseModel


class NavItem(BaseModel):
    """Navigation item."""
    label: str
    path: str | None = None
    children: list["NavItem"] | None = None


class Sidebar(Component):
    """Documentation sidebar navigation."""
    
    component_type: str = "DocsSidebar"
    
    def __init__(
        self,
        items: list[NavItem],
        current_path: str = "/",
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
        self.items = items
        self.current_path = current_path
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "items": [item.model_dump() for item in self.items],
                "currentPath": self.current_path,
                "className": self.class_name,
            },
        }


class DocsLayout(Component):
    """Main documentation layout with sidebar and content."""
    
    component_type: str = "DocsLayout"
    
    def __init__(
        self,
        nav_items: list[NavItem],
        children: list[Component] | None = None,
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
        self.nav_items = nav_items
        self._children = children or []
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "navItems": [item.model_dump() for item in self.nav_items],
                "className": self.class_name,
            },
            "children": [child.render() for child in self._children],
        }
```

### Acceptance Criteria

- [ ] CodeBlock renders with syntax highlighting
- [ ] APIDoc displays documentation
- [ ] Example shows code and preview
- [ ] Layout works with sidebar

---

## Task 8.3: Home Page

### Description
Create the documentation home page.

### Files to Create

**docs/pages/home.py**
```python
"""Documentation home page."""

from refast import Context
from refast.components import (
    Container,
    Column,
    Row,
    Text,
    Button,
    Heading,
    Card,
    CardContent,
    Grid,
    Link,
)
from docs.components import CodeBlock


def render(ctx: Context):
    """Render the home page."""
    return Container(
        class_name="max-w-4xl mx-auto py-12 px-4",
        children=[
            # Hero section
            Column(
                align="center",
                class_name="text-center mb-12",
                children=[
                    Heading("Refast", level=1, class_name="text-5xl font-bold mb-4"),
                    Text(
                        "Build reactive web applications with Python",
                        class_name="text-xl text-gray-600 mb-8",
                    ),
                    Row(
                        gap=4,
                        justify="center",
                        children=[
                            Button(
                                "Get Started",
                                variant="primary",
                                size="lg",
                                on_click=ctx.callback(
                                    lambda ctx: ctx.navigate("/getting-started")
                                ),
                            ),
                            Button(
                                "View on GitHub",
                                variant="outline",
                                size="lg",
                            ),
                        ]
                    ),
                ]
            ),
            
            # Quick example
            Card(
                class_name="mb-12",
                children=[
                    CardContent(
                        children=[
                            CodeBlock(
                                code='''from refast import RefastApp, Context
from refast.components import Container, Text, Button

ui = RefastApp()

@ui.page("/")
def home(ctx: Context):
    count = ctx.session.get("count", 0)
    
    return Container(children=[
        Text(f"Count: {count}"),
        Button("Increment", on_click=ctx.callback(increment)),
    ])

async def increment(ctx: Context):
    count = ctx.session.get("count", 0) + 1
    ctx.session.set("count", count)
    await ctx.refresh()''',
                                language="python",
                                title="Quick Example",
                            ),
                        ]
                    ),
                ]
            ),
            
            # Features grid
            Heading("Features", level=2, class_name="text-center mb-8"),
            Grid(
                columns=3,
                gap=6,
                class_name="mb-12",
                children=[
                    feature_card(
                        "🐍 Python-First",
                        "Write your entire UI in Python. No JavaScript required.",
                    ),
                    feature_card(
                        "⚡ Reactive",
                        "Real-time updates with WebSocket streaming.",
                    ),
                    feature_card(
                        "🔒 Secure",
                        "Built-in CSRF protection, rate limiting, and CSP.",
                    ),
                    feature_card(
                        "🎨 Beautiful",
                        "Pre-built shadcn/ui components out of the box.",
                    ),
                    feature_card(
                        "📦 Pluggable",
                        "Add to any FastAPI app with include_router.",
                    ),
                    feature_card(
                        "🔧 Extensible",
                        "Create custom components from any React library.",
                    ),
                ]
            ),
        ]
    )


def feature_card(title: str, description: str) -> Card:
    """Create a feature card."""
    return Card(
        class_name="h-full",
        children=[
            CardContent(
                children=[
                    Column(
                        gap=2,
                        children=[
                            Heading(title, level=3, class_name="text-lg"),
                            Text(description, class_name="text-gray-600"),
                        ]
                    ),
                ]
            ),
        ]
    )
```

### Acceptance Criteria

- [ ] Hero section displays
- [ ] Quick example shows
- [ ] Features grid renders
- [ ] Navigation works

---

## Task 8.4: Getting Started Guide

### Description
Create the getting started documentation.

### Files to Create

**docs/pages/getting_started.py**
```python
"""Getting started guide."""

from refast import Context
from refast.components import (
    Container,
    Column,
    Text,
    Heading,
    Card,
    CardContent,
    Alert,
)
from docs.components import CodeBlock


def render(ctx: Context):
    """Render the getting started page."""
    return Container(
        class_name="prose max-w-none",
        children=[
            Heading("Getting Started", level=1),
            Text(
                "Get up and running with Refast in minutes.",
                class_name="lead text-xl text-gray-600 mb-8",
            ),
            
            # Installation
            Heading("Installation", level=2),
            CodeBlock(
                code="pip install refast",
                language="bash",
                title="Install Refast",
            ),
            
            # Quick start
            Heading("Quick Start", level=2),
            Text("Create a simple Refast application:"),
            CodeBlock(
                code='''# app.py
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Text, Button, Input, Column

# Create FastAPI app
app = FastAPI()

# Create Refast UI
ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    name = ctx.session.get("name", "World")
    
    return Container(
        class_name="p-4",
        children=[
            Column(
                gap=4,
                children=[
                    Text(f"Hello, {name}!", class_name="text-2xl"),
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

async def update_name(ctx: Context, value: str = ""):
    if value:
        ctx.session.set("name", value)
        await ctx.refresh()

# Mount Refast to FastAPI
app.include_router(ui.router)''',
                language="python",
                title="app.py",
                show_line_numbers=True,
            ),
            
            # Run the app
            Heading("Run the Application", level=2),
            CodeBlock(
                code="uvicorn app:app --reload",
                language="bash",
            ),
            Text("Open http://localhost:8000 in your browser."),
            
            # Next steps
            Heading("Next Steps", level=2),
            Column(
                gap=2,
                children=[
                    Text("• Learn about components →"),
                    Text("• Understand events and callbacks →"),
                    Text("• Explore session management →"),
                    Text("• Review security features →"),
                ]
            ),
        ]
    )
```

### Acceptance Criteria

- [ ] Installation instructions clear
- [ ] Quick start example works
- [ ] Code blocks display properly
- [ ] Next steps links work

---

## Task 8.5 - 8.8: Guide Pages

Create similar documentation pages for:
- `docs/pages/components.py` - Component reference
- `docs/pages/events.py` - Events guide
- `docs/pages/sessions.py` - Sessions guide
- `docs/pages/security.py` - Security guide

Each follows the same pattern as getting_started.py.

---

## Task 8.9: API Reference Generation

### Description
Auto-generate API reference from docstrings.

### Files to Create

**docs/pages/api_reference.py**
```python
"""Auto-generated API reference."""

import inspect
from refast import Context
from refast.components import Container, Column, Heading, Text, Tabs, TabItem
from docs.components import APIDoc, ParamDoc

import refast
from refast import RefastApp
from refast.context import Context as RefastContext
from refast.components.base import Component


def render(ctx: Context):
    """Render the API reference page."""
    return Container(
        class_name="max-w-4xl",
        children=[
            Heading("API Reference", level=1),
            Text(
                "Complete API documentation for Refast.",
                class_name="text-xl text-gray-600 mb-8",
            ),
            
            Tabs(
                children=[
                    TabItem(
                        label="Core",
                        children=[core_api()],
                    ),
                    TabItem(
                        label="Components",
                        children=[components_api()],
                    ),
                    TabItem(
                        label="Events",
                        children=[events_api()],
                    ),
                    TabItem(
                        label="Sessions",
                        children=[sessions_api()],
                    ),
                ]
            ),
        ]
    )


def core_api():
    """Core API documentation."""
    return Column(
        gap=6,
        children=[
            Heading("Core Classes", level=2),
            
            APIDoc(
                name="RefastApp",
                kind="class",
                signature="RefastApp(title='Refast App', theme=None, secret_key=None)",
                description="Main Refast application class. Create an instance to define your UI.",
                params=[
                    ParamDoc(
                        name="title",
                        type="str",
                        description="The title of the application.",
                        required=False,
                        default="'Refast App'",
                    ),
                    ParamDoc(
                        name="theme",
                        type="Theme | None",
                        description="Custom theme configuration.",
                        required=False,
                        default="None",
                    ),
                    ParamDoc(
                        name="secret_key",
                        type="str | None",
                        description="Secret key for CSRF and session security.",
                        required=False,
                        default="None",
                    ),
                ],
                examples=[
                    '''ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx):
    return Container(children=[Text("Hello!")])''',
                ],
            ),
            
            APIDoc(
                name="Context",
                kind="class",
                signature="Context(request, session, ...)",
                description="Context object passed to page functions and callbacks.",
                params=[
                    ParamDoc(
                        name="session",
                        type="Session",
                        description="The current user session.",
                        required=True,
                    ),
                ],
            ),
        ]
    )


def components_api():
    """Components API documentation."""
    return Column(
        gap=6,
        children=[
            Heading("Components", level=2),
            Text("All available UI components."),
            
            # Would auto-generate from component classes
            APIDoc(
                name="Container",
                kind="class",
                signature="Container(children=None, id=None, class_name='')",
                description="Basic container component for grouping elements.",
                params=[
                    ParamDoc(name="children", type="list[Component]", description="Child components"),
                    ParamDoc(name="id", type="str | None", description="Element ID"),
                    ParamDoc(name="class_name", type="str", description="CSS classes"),
                ],
            ),
            
            APIDoc(
                name="Button",
                kind="class",
                signature="Button(label, variant='default', on_click=None, ...)",
                description="Button component with click handling.",
                params=[
                    ParamDoc(name="label", type="str", description="Button text"),
                    ParamDoc(name="variant", type="str", description="Visual variant"),
                    ParamDoc(name="on_click", type="Callback | None", description="Click handler"),
                ],
            ),
        ]
    )


def events_api():
    """Events API documentation."""
    return Column(
        gap=6,
        children=[
            Heading("Events API", level=2),
            Text("Event handling and real-time updates."),
        ]
    )


def sessions_api():
    """Sessions API documentation."""
    return Column(
        gap=6,
        children=[
            Heading("Sessions API", level=2),
            Text("Session management classes and stores."),
        ]
    )
```

### Acceptance Criteria

- [ ] API docs render
- [ ] Tabs work
- [ ] Documentation accurate
- [ ] Examples included

---

## Task 8.10: Deployment

### Description
Set up documentation deployment.

### Files to Create

**docs/Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install -e .

# Copy docs
COPY docs/ ./docs/

# Run
CMD ["uvicorn", "docs.app:app", "--host", "0.0.0.0", "--port", "8080"]
```

**docs/README.md**
```markdown
# Refast Documentation

The documentation for Refast, built using Refast itself.

## Running Locally

```bash
cd docs
uvicorn app:app --reload --port 8001
```

Then open http://localhost:8001

## Building for Production

```bash
docker build -t refast-docs .
docker run -p 8080:8080 refast-docs
```

## Structure

- `app.py` - Main documentation app
- `pages/` - Documentation pages
- `components/` - Custom doc components
```

### Acceptance Criteria

- [ ] Docs run locally
- [ ] Docker build works
- [ ] Can deploy to hosting

---

## Final Checklist for Stage 8

- [ ] Docs app structure complete
- [ ] Custom components work
- [ ] All pages render
- [ ] API reference generated
- [ ] Deployment ready
- [ ] Update `.github/copilot-instructions.md` status to 🟢
