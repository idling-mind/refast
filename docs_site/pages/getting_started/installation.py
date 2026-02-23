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
## Prerequisites

- **Python 3.11+**
- Basic knowledge of Python and FastAPI is helpful but not required.

## Installation

Refast is available on PyPI and can be installed with `pip` or `uv`.

```bash
# Using pip
pip install refast

# Using uv (recommended)
uv pip install refast
```

## Your First App

Create a file named `app.py` with the following content:

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Heading, Text

# 1. Create the Refast app instance
ui = RefastApp(title="Hello Refast")

# 2. Define a page handler
@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="max-w-2xl mx-auto p-8 text-center",
        children=[
            Heading("Hello, Refast!", level=1, class_name="text-4xl mb-4"),
            Text("Your first Refast app is up and running."),
        ],
    )

# 3. Mount Refast to a FastAPI app
app = FastAPI()
app.include_router(ui.router)
```

## Run It

Refast apps are standard ASGI applications. You can run them with `uvicorn`:

```bash
uvicorn app:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser. You should see your "Hello, Refast!" message.

## Code Walkthrough

1. **`RefastApp`**: This is the main entry point. It handles page registration, event routing, and configuration.
2. **`@ui.page("/")`**: A decorator that registers a Python function as the handler for a specific route.
3. **`ctx: Context`**: The context object is passed to every page handler and callback. It provides access to state, session data, and methods like `navigate()` or `refresh()`.
4. **Components**: Functions like `Container`, `Heading`, and `Text` return Python objects representing UI elements. These are serialized to JSON and rendered by React on the client.
5. **`app.include_router(ui.router)`**: Refast integrates seamlessly into any FastAPI application by exposing a standard APIRouter.

## Project Structure

For larger applications, we recommend structuring your project like this:

```text
my_app/
├── app.py             # Main entry point
├── components/        # Reusable UI components
│   ├── __init__.py
│   └── layout.py
├── pages/             # Page handlers
│   ├── __init__.py
│   ├── home.py
│   └── settings.py
└── theme.py           # Custom theme configuration
```

## Next Steps

Now that you have Refast running, take the **Quick Tour** to build an interactive application.

- [Quick Tour](/docs/quick-tour) — Build a Todo app in 5 minutes
- [Architecture](/docs/architecture) — Understand how Refast works
- [Examples](/docs/examples) — See what's possible
"""
