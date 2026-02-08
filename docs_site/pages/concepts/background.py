"""Background Jobs & Broadcasting — /docs/concepts/background."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Background Jobs & Broadcasting"
PAGE_ROUTE = "/docs/concepts/background"


def render(ctx):
    """Render the background jobs concept page."""
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


CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Overview

Refast apps can run background tasks that push updates to connected clients in real time.
This is useful for dashboards, notifications, chat, and any scenario where the server
initiates updates.

## Running Background Tasks

Use `asyncio.create_task()` to spawn a background coroutine:

```python
import asyncio

async def on_click(ctx: Context):
    asyncio.create_task(long_running_job(ctx))
    await ctx.show_toast("Job started!", variant="info")

async def long_running_job(ctx: Context):
    for i in range(10):
        await ctx.update_text("status", f"Step {i+1}/10...")
        await asyncio.sleep(1)
    await ctx.update_text("status", "Done!")
```

## Broadcasting to All Clients

Access all connected WebSocket contexts via `ui.active_contexts`:

```python
async def broadcast_update(ui: RefastApp, message: str):
    for ctx in ui.active_contexts:
        await ctx.show_toast(message, variant="info")
```

## FastAPI Lifespan Pattern

For tasks that should run for the app's entire lifetime:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background task
    task = asyncio.create_task(periodic_updates(ui))
    yield
    # Cleanup
    task.cancel()

app = FastAPI(lifespan=lifespan)

async def periodic_updates(ui: RefastApp):
    while True:
        for ctx in ui.active_contexts:
            await ctx.update_text("clock", datetime.now().strftime("%H:%M:%S"))
        await asyncio.sleep(1)
```

## ctx.broadcast() and ctx.push_event()

```python
# Broadcast a custom event to all clients
await ctx.broadcast("notification", {"message": "Server update!"})

# Push a custom event to the current client only
await ctx.push_event("data_ready", {"id": 42})
```

## Important Notes

- Background tasks hold a reference to `ctx` — ensure the WebSocket is still connected
- Use `try/except` to handle disconnections gracefully
- For heavy processing, consider using a task queue (Celery, etc.)

## Next Steps

- [Theming](/docs/concepts/theming) — Changing the look and feel
- [Toast Notifications](/docs/concepts/toasts) — User feedback
"""
