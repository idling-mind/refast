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
## Overview

Refast apps can run **background tasks** that push updates to connected clients in real time,
and **broadcast** those updates to every connected WebSocket. This is the foundation for
dashboards, notifications, progress indicators, and multi-user collaboration features.

Two main patterns exist:

| Pattern | When to use |
|---------|-------------|
| `asyncio.create_task()` | Triggered by a user action; task is tied to one client's `ctx` |
| `lifespan` + `ui.active_contexts` | Server-initiated; pushes updates to *all* connected clients |

---

## Per-Client Background Tasks

Use `asyncio.create_task()` inside a callback to run work in the background without
blocking the WebSocket event loop. The task holds onto the same `ctx` object so it can
push incremental updates to that client.

```python
import asyncio
from refast import Context, RefastApp
from refast.components import Button, Container, Progress, Text

ui = RefastApp(title="Background Jobs")


async def run_job(ctx: Context):
    \"""Background coroutine — runs outside the event loop.\"""
    try:
        ctx.state["stop"] = False
        for i in range(10):
            if ctx.state.get("stop"):
                await ctx.update_text("status", "Stopped.")
                return

            await asyncio.sleep(1)  # simulate work
            pct = (i + 1) * 10
            await ctx.update_text("status", f"Progress: {pct}%")
            await ctx.update_props("progress-bar", {"value": pct})

        await ctx.show_toast("Job complete!", variant="success")
    except Exception as e:
        # Handle disconnection or other errors gracefully
        print(f"Job error: {e}")


async def start(ctx: Context):
    asyncio.create_task(run_job(ctx))
    await ctx.show_toast("Job started", variant="info")


async def stop(ctx: Context):
    ctx.state["stop"] = True


@ui.page("/")
def home(ctx: Context):
    return Container(children=[
        Button("Start", on_click=ctx.callback(start)),
        Button("Stop",  on_click=ctx.callback(stop), variant="destructive"),
        Text("", id="status"),
        Progress(value=0, id="progress-bar"),
    ])
```

**Key points:**
- `asyncio.create_task()` returns immediately so the button click is acknowledged right away.
- The task communicates back only via `ctx` methods (`update_text`, `update_props`,
  `show_toast`, `refresh`, …).
- Always wrap the task body in `try/except` — the WebSocket may close before the task finishes.
- Use `ctx.state` as a stop-flag channel between the event handler and the running task.

---

## Broadcasting to All Clients

`ui.active_contexts` returns a list of every currently connected client's `Context`.
Iterate over it to push the same update to everyone.

```python
async def notify_all(ui: RefastApp, message: str):
    for ctx in ui.active_contexts:
        try:
            await ctx.show_toast(message, variant="info")
        except Exception:
            pass  # client may have disconnected
```

### Replacing a component on all clients

```python
async def broadcast_news(ui: RefastApp, headline: str):
    for ctx in ui.active_contexts:
        try:
            await ctx.replace("news-banner", Text(headline, class_name="font-bold text-lg"))
        except Exception:
            pass
```

---

## Lifespan Pattern — Server-Initiated Tasks

For tasks that should run for the app's **entire lifetime** (live dashboards, clocks,
monitoring feeds), use the FastAPI `lifespan` context manager to start and cleanly
stop a background coroutine.

```python
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from refast import Context, RefastApp
from refast.components import Container, Text

ui = RefastApp(title="Live Clock")


@ui.page("/")
def home(ctx: Context):
    return Container(children=[Text("--:--:--", id="clock")])


async def clock_task(ui: RefastApp):
    \"""Runs forever; updates the clock for every connected client.\"""
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        for ctx in ui.active_contexts:
            try:
                await ctx.update_text("clock", now)
            except Exception:
                pass
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(clock_task(ui))
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(ui.router)
```

The pattern in brief:

1. Define an `async` coroutine that loops forever (or until cancelled).
2. Inside the loop, iterate `ui.active_contexts` and push updates.
3. Start it with `asyncio.create_task()` in `lifespan` startup; cancel on shutdown.

---

## Per-Client State in Broadcast Tasks

`ui.active_contexts` gives you every client's `ctx`, including their individual
`ctx.state`. You can combine shared server data with per-client state:

```python
async def update_all(ui: RefastApp, shared_value: int):
    for ctx in ui.active_contexts:
        try:
            # Per-client counter
            count = ctx.state.get("updates", 0) + 1
            ctx.state.set("updates", count)

            await ctx.update_props("metrics", {
                "value": shared_value,
                "label": f"Updated {count}× for you",
            })
        except Exception:
            pass
```

---

## Pushing Custom Events

`ctx.push_event()` sends a named event payload to the **current client's** frontend.
This is useful if you have custom JavaScript that listens for Refast events.

```python
async def data_ready(ctx: Context):
    result = await fetch_data()
    await ctx.push_event("data:ready", {"rows": result})
```

---

## Important Notes

- **Hold `ctx` carefully** — Background tasks keep a reference to `ctx` alive. If the
  WebSocket closes, subsequent `await ctx.…()` calls will raise because the send will
  fail. Always wrap in `try/except`.
- **`ctx.state` is not thread-safe** — Background tasks run in the same event loop thread,
  so `asyncio`-based access is safe. Never use `threading.Thread` to mutate state.
- **Heavy CPU work** — For CPU-bound tasks, offload to a process pool:
  `await asyncio.get_event_loop().run_in_executor(None, cpu_bound_fn)`.
- **Task queues** — For distributed or durable background work, integrate Celery, ARQ, or
  another task queue and have workers push results back via a shared store.

---

## Next Steps

- [Streaming](/docs/concepts/streaming) — Incremental content delivery token-by-token
- [State](/docs/concepts/state) — Managing per-client state across interactions
- [Routing](/docs/concepts/routing) — Multi-page SPA navigation
"""
