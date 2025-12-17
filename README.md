# Refast

**Python + React UI Framework for Building Reactive Web Applications**

Refast is a framework that enables building reactive web applications with Python-first development. It uses FastAPI for the backend and React with shadcn/ui for the frontend.

## Features

- **Python-First Development**: Build your UI logic entirely in Python
- **Reactive Components**: Real-time updates via WebSocket
- **shadcn/ui Integration**: Beautiful, accessible components out of the box
- **FastAPI Integration**: Plug into any existing FastAPI application
- **Type Safety**: Full type hints and Pydantic validation throughout

## Installation

```bash
pip install refast
```

## Quick Start

```python
from refast import RefastApp, Context

ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    return Container(
        Text("Hello, World!"),
        Button("Click me", on_click=ctx.callback(handle_click))
    )

async def handle_click(ctx: Context):
    await ctx.show_toast("Button clicked!")

# Mount to FastAPI
from fastapi import FastAPI
app = FastAPI()
app.include_router(ui.router, prefix="/ui")
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
ruff check src/
```

## License

MIT
