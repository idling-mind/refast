"""State Management — /docs/concepts/state."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "State Management"
PAGE_ROUTE = "/docs/concepts/state"


def render(ctx):
    """Render the state management concept page."""
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

`ctx.state` is a **per-connection, server-side** dictionary that persists across
callbacks within a single WebSocket session. It's the primary way to track
application state in Refast.

## Basic Usage

```python
# Set a value
ctx.state.set("counter", 0)

# Get a value (with optional default)
count = ctx.state.get("counter", 0)

# Bracket syntax also works
ctx.state["counter"] = 42
count = ctx.state["counter"]

# Update multiple values at once
ctx.state.update({"name": "Alice", "role": "admin"})
```

## Pattern: State + Refresh

The most common pattern is to modify state in a callback, then re-render:

```python
async def increment(ctx: Context):
    count = ctx.state.get("counter", 0)
    ctx.state.set("counter", count + 1)
    await ctx.refresh()  # Re-renders the page with new state
```

## State vs Store

| | `ctx.state` | `ctx.store` |
|---|---|---|
| **Location** | Server (Python) | Browser (localStorage/sessionStorage) |
| **Lifetime** | WebSocket session | Persists across reloads |
| **Access** | Instant (in-memory) | Requires sync for reads |
| **Use case** | App logic, UI state | Form drafts, user preferences |

## Important Notes

- State is **lost** when the WebSocket disconnects (page close, refresh)
- State is **not shared** between different browser tabs
- For persistent storage, use `ctx.store` (see [Store](/docs/concepts/store))
- On initial HTTP GET (first page load), state is empty — only populated within callbacks

## Next Steps

- [Store (Browser Storage)](/docs/concepts/store) — Persistent client-side storage
- [DOM Updates](/docs/concepts/updates) — Pushing changes to the UI
"""
