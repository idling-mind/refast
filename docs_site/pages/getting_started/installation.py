"""Installation & Getting Started — /docs/getting-started."""

from refast.components import (
    Container,
    Heading,
    Markdown,
    Separator,
)


PAGE_TITLE = "Installation & Getting Started"
PAGE_ROUTE = "/docs/getting-started"


def render(ctx):
    """Render the getting started page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ---------------------------------------------------------------------------
# PAGE CONTENT — To be expanded by an agent.
# See getting_started/AGENT_INSTRUCTIONS.md for full requirements.
# ---------------------------------------------------------------------------

CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Prerequisites

- Python 3.11 or later
- FastAPI
- uvicorn (or any ASGI server)

## Install Refast

```bash
pip install refast
# or with uv
uv pip install refast
```

## Your First App

Create a file called `app.py`:

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Heading, Text

ui = RefastApp(title="Hello Refast")

@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="max-w-2xl mx-auto p-8",
        children=[
            Heading("Hello, Refast!", level=1),
            Text("Your first Refast app is running."),
        ],
    )

app = FastAPI()
app.include_router(ui.router)
```

## Run It

```bash
uvicorn app:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## What Just Happened?

1. `RefastApp` creates the Refast framework instance
2. `@ui.page("/")` registers a page handler for the root route
3. The handler returns a **component tree** — Python objects that describe the UI
4. `app.include_router(ui.router)` mounts Refast's routes into your FastAPI app
5. When a browser visits `/`, Refast renders the component tree to JSON and serves an HTML shell that boots the React frontend
6. A WebSocket connection is established for real-time events and updates

## Next Steps

- [Architecture](/docs/architecture) — How Refast works under the hood
- [Quick Tour](/docs/quick-tour) — Build a todo app step by step
- [Components](/docs/concepts/components) — Learn about the component model
"""
