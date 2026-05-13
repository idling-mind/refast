"""Streaming — /docs/concepts/streaming."""

import asyncio
import random

from refast.components import Badge, Button, Container, Heading, Markdown, Row, Separator
from refast.context import Context

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "Streaming"
PAGE_ROUTE = "/docs/concepts/streaming"

# ---------------------------------------------------------------------------
# Sample content to stream word-by-word (simulates LLM output)
# ---------------------------------------------------------------------------

_SAMPLE_RESPONSE = """\
# Streaming works!

This text is being delivered **token by token**, just like a large language model.

## Why streaming matters

1. **Immediate feedback** — users see output as it arrives, not after a delay.
2. **Better perceived performance** — partial results feel faster than waiting.
3. **Progressive disclosure** — complex output becomes readable incrementally.

## Code pattern

```python
async def stream_answer(ctx: Context):
    await ctx.update_props("output", {"content": "", "streaming": True})
    async for chunk in llm.stream(prompt):
        await ctx.append_prop("output", "content", chunk)
    await ctx.update_props("output", {"streaming": False})
```

Streaming is complete. ✓\
"""

# ---------------------------------------------------------------------------
# Callbacks (module-level for stability across re-renders)
# ---------------------------------------------------------------------------

_streaming_flags: dict[int, bool] = {}


async def demo_start_stream(ctx: Context) -> None:
    """Stream the sample text word-by-word into the Markdown component."""
    session_id = id(ctx)
    _streaming_flags[session_id] = True

    await ctx.update_props("stream-output", {"content": ""})
    await ctx.update_text("stream-status", "Streaming…")
    await ctx.update_props("stream-status", {"variant": "default"})
    await ctx.update_props("stream-stop-btn", {"disabled": False})
    await ctx.update_props("stream-start-btn", {"disabled": True})

    words = _SAMPLE_RESPONSE.split(" ")
    for i, word in enumerate(words):
        if not _streaming_flags.get(session_id, False):
            await ctx.update_text("stream-status", "Stopped")
            await ctx.update_props("stream-status", {"variant": "secondary"})
            break
        chunk = word if i == 0 else " " + word
        await ctx.append_prop("stream-output", "content", chunk)
        await asyncio.sleep(random.uniform(0.03, 0.09))
    else:
        await ctx.update_text("stream-status", "Complete ✓")
        await ctx.update_props("stream-status", {"variant": "success"})

    await ctx.update_props("stream-stop-btn", {"disabled": True})
    await ctx.update_props("stream-start-btn", {"disabled": False})
    _streaming_flags.pop(session_id, None)


async def demo_stop_stream(ctx: Context) -> None:
    """Signal the running stream to stop."""
    _streaming_flags[id(ctx)] = False


async def demo_clear_stream(ctx: Context) -> None:
    """Clear the output area."""
    await ctx.update_props("stream-output", {"content": ""})
    await ctx.update_text("stream-status", "Ready")
    await ctx.update_props("stream-status", {"variant": "secondary"})
    await ctx.update_props("stream-stop-btn", {"disabled": True})
    await ctx.update_props("stream-start-btn", {"disabled": False})


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------

CONTENT = r"""
## Overview

Streaming lets you push content to the browser **incrementally** — ideal for LLM
responses, real-time logs, live sensor data, or anything that arrives piece by piece.

Refast provides two low-level primitives you compose together:

| Method | What it does |
|---|---|
| `ctx.append_prop(id, prop, value)` | Concatenates strings, extends lists |
| `ctx.update_props(id, props)` | Sets any prop — use for start/stop indicators |

---

## Streaming text (`append_prop`)

The canonical pattern for token-by-token text streaming:

```python
async def stream_answer(ctx: Context):
    # 1. Reset content
    await ctx.update_props("ai-output", {"content": ""})

    # 2. Append each chunk as it arrives
    async for chunk in llm.stream(prompt):
        await ctx.append_prop("ai-output", "content", chunk)
```

The target component must have a matching `id`:

```python
Markdown(content="", id="ai-output")
```

`append_prop` **concatenates** string props, so each chunk is appended to whatever
is already in `content`.

---

## How `append_prop` handles different prop types

### String props — concatenation

```python
# content = "Hello"
await ctx.append_prop("my-md", "content", " World")
# content = "Hello World"
```

### List props — append or extend

```python
# data = [1, 2, 3]
await ctx.append_prop("my-chart", "data", 4)          # → [1, 2, 3, 4]
await ctx.append_prop("my-chart", "data", [5, 6])     # → [1, 2, 3, 4, 5, 6]
```

### Uninitialised props

If the prop doesn't exist yet, Refast infers the type from the value:

```python
await ctx.append_prop("id", "content", "Hello")   # content = "Hello"
await ctx.append_prop("id", "data",    [1, 2])    # data    = [1, 2]
await ctx.append_prop("id", "items",   {"x": 1}) # items   = [{"x": 1}]
```

---

## Streaming chart data

For live charts, append data points one at a time:

```python
async def stream_sensor(ctx: Context):
    await ctx.update_props("sensor-chart", {"data": []})   # clear first

    async for reading in sensor.stream():
        point = {"time": reading.timestamp, "value": reading.value}
        await ctx.append_prop("sensor-chart", "data", point)

    # Trim to last N points when the chart grows too large
    # (use update_props with the full sliced list)
```

---

## Showing a streaming indicator

`Markdown` has no built-in streaming indicator. Use a separate `Badge` or `Text`
component alongside it to signal status:

```python
# Layout
Badge("Ready", id="status-badge", variant="secondary")
Markdown(id="output", content="")

async def on_generate(ctx: Context):
    await ctx.update_props("status-badge", {"variant": "default"})
    await ctx.update_text("status-badge", "Generating…")

    await ctx.update_props("output", {"content": ""})
    async for chunk in llm.stream(prompt):
        await ctx.append_prop("output", "content", chunk)

    await ctx.update_text("status-badge", "Done")
    await ctx.update_props("status-badge", {"variant": "success"})
```

---

## Stopping a stream

Because streaming runs inside a Python coroutine, you control cancellation with a
shared flag:

```python
_flags: dict = {}

async def start(ctx: Context):
    _flags[id(ctx)] = True
    async for chunk in llm.stream(prompt):
        if not _flags.get(id(ctx)):
            break
        await ctx.append_prop("output", "content", chunk)
    _flags.pop(id(ctx), None)

async def stop(ctx: Context):
    _flags[id(ctx)] = False
```

---

## Performance tips

- **Chunk size** — very small chunks (single characters) produce more WebSocket messages.
  Streaming word-by-word is a good balance for LLM output.
- **High-frequency data** — if you receive >30 updates/second, buffer and flush on a timer:

```python
async def stream_fast(ctx: Context):
    buf = ""
    t = asyncio.get_event_loop().time()

    async for chunk in fast_source():
        buf += chunk
        now = asyncio.get_event_loop().time()
        if now - t > 0.033:               # ~30 fps
            await ctx.append_prop("output", "content", buf)
            buf = ""
            t = now

    if buf:
        await ctx.append_prop("output", "content", buf)
```

---

## Live demo

Click **Start streaming** to see token-by-token text delivery into a `Markdown`
component. Use **Stop** to interrupt mid-stream.

{{ stream_demo }}

---

## Next Steps

- [DOM Updates](/docs/concepts/updates) — All targeted update methods
- [Background Jobs](/docs/concepts/background) — Long-running tasks and broadcasting
- [Examples: Streaming](/docs) — Full working example in `examples/streaming/app.py`
"""


def render(ctx: Context):
    """Render the streaming concept page with a live demo."""
    from docs_site.app import docs_layout

    stream_demo = Container(
        class_name="space-y-4",
        children=[
            # Controls
            Row(
                class_name="flex flex-wrap items-center gap-2",
                children=[
                    Button(
                        "Start streaming",
                        id="stream-start-btn",
                        on_click=ctx.callback(demo_start_stream),
                        variant="default",
                    ),
                    Button(
                        "Stop",
                        id="stream-stop-btn",
                        on_click=ctx.callback(demo_stop_stream),
                        variant="outline",
                        disabled=True,
                    ),
                    Button(
                        "Clear",
                        on_click=ctx.callback(demo_clear_stream),
                        variant="ghost",
                        class_name="text-xs",
                    ),
                    Badge("Ready", id="stream-status", variant="secondary"),
                ],
            ),
            # Output
            Container(
                class_name="rounded-md border bg-muted/30 p-4 min-h-[160px]",
                children=[
                    Markdown(
                        id="stream-output",
                        content="Output will appear here…",
                    ),
                ],
            ),
        ],
    )

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)
