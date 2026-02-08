"""Quick Tour — /docs/quick-tour."""

from refast.components import (
    Container,
    Heading,
    Markdown,
    Separator,
)


PAGE_TITLE = "Quick Tour"
PAGE_ROUTE = "/docs/quick-tour"


def render(ctx):
    """Render the quick tour page."""
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

## Build a Todo App in 5 Minutes

This walkthrough builds a simple todo app from scratch, covering the core Refast patterns:
pages, components, callbacks, state management, and targeted DOM updates.

### Step 1: Create the App

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import (
    Button, Card, CardContent, CardHeader, CardTitle,
    Checkbox, Column, Container, Flex, Heading, Input, Row, Text,
)

ui = RefastApp(title="Todo App")
app = FastAPI()
app.include_router(ui.router)
```

### Step 2: Define the Page

```python
@ui.page("/")
def home(ctx: Context):
    todos = ctx.state.get("todos", [])
    # ... render UI
```

### Step 3: Add Callbacks

```python
async def add_todo(ctx: Context):
    text = ctx.prop_store.get("new_todo", "")
    if text.strip():
        todos = ctx.state.get("todos", [])
        todos.append({"text": text, "done": False})
        ctx.state.set("todos", todos)
        await ctx.refresh()
```

### Step 4: Wire Up the UI

```python
Input(
    placeholder="What needs to be done?",
    on_change=ctx.callback(add_todo),
    store_as="new_todo",
)
Button("Add", on_click=ctx.callback(add_todo))
```

### Step 5: Run

```bash
uvicorn app:app --reload
```

> See `examples/todo_app/app.py` for the complete working example.

## What You Learned

- **`@ui.page("/")`** registers a page handler
- **`ctx.state`** holds per-connection server-side state
- **`ctx.callback(fn)`** creates a callback that triggers a Python function on user interaction
- **`store_as="key"`** stores input values client-side, accessible via `ctx.prop_store`
- **`await ctx.refresh()`** re-renders the page with the current state
"""
