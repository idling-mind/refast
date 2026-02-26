"""State & Store — /docs/concepts/state."""

from refast.components import Container, Heading, Markdown, Separator

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "State & Store"
PAGE_ROUTE = "/docs/concepts/state"


def render(ctx):
    """Render the state and store concept page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
## Overview

Refast gives you two complementary state layers:

- `ctx.state`: server-side, per-WebSocket-session state for app logic and UI rendering
- `ctx.store`: browser storage (`localStorage` + `sessionStorage`) for values that should survive refreshes

Use both intentionally: keep authoritative runtime state on the server, and persist user/device preferences in browser storage.

## Basic Usage

```python
# Server-side state (per connection)
ctx.state.set("counter", 0)
count = ctx.state.get("counter", 0)

# Browser store (persists client-side)
ctx.store.local.set("theme", "dark")
ctx.store.session.set("draft", "hello")

# Bracket syntax works for both state and store
ctx.state["counter"] = 42
ctx.store.local["theme"] = "light"
```

## Detailed API

### `ctx.state`

| Method | Description |
|---|---|
| `state.get(key, default)` | Get value with default |
| `state.set(key, value)` | Set one value |
| `state.update(dict)` | Set multiple values |
| `state.to_dict()` | Copy state to a dict |
| `state["key"] = value` | Bracket assignment |

### `ctx.store.local` and `ctx.store.session`

| Method | Description |
|---|---|
| `get(key, default)` | Read cached value |
| `set(key, value)` | Set one key |
| `set_many(dict)` | Set multiple keys |
| `delete(key)` | Remove key |
| `clear()` | Remove all keys |
| `get_all()` | Copy all key-values |
| `keys()`, `values()`, `items()` | Collection helpers |
| `await ctx.store.sync()` | Pull latest values from browser |

`ctx.store.local` maps to `localStorage` and `ctx.store.session` maps to `sessionStorage`.

## `ctx.refresh()` and `target_id`

`ctx.refresh()` supports two modes:

```python
# Full page refresh for current route fallback
await ctx.refresh()

# Refresh a specific route
await ctx.refresh(path="/docs/concepts/state")

# Targeted refresh: replace only one component subtree
await ctx.refresh(target_id="counter-panel")
```

When `target_id` is provided, Refast re-renders the page on the server, finds that component by id, and sends a targeted `replace` update only for that node.

If the id is missing or not present in the freshly rendered tree, no targeted update is sent.

## Why component IDs matter for partial refresh

To avoid broad re-renders, assign stable `id` values to the component you intend to refresh and to important parent containers you may update later.

```python
from refast.components import Button, Container, Heading, Text

@ui.page("/")
def home(ctx):
    count = ctx.state.get("count", 0)
    return Container(
        id="page-root",
        children=[
            Heading("Counter", id="counter-title", level=2),
            Container(
                id="counter-panel",
                children=[Text(f"Count: {count}", id="counter-value")],
            ),
            Button("+1", on_click=ctx.callback(increment)),
        ],
    )

async def increment(ctx):
    ctx.state.set("count", ctx.state.get("count", 0) + 1)
    await ctx.refresh(target_id="counter-panel")
```

Why this helps:

- Only `counter-panel` is replaced, so unrelated inputs and focus are preserved.
- Stable parent ids (like `page-root`) enable future targeted operations (`append`, `prepend`, `update_props`) without falling back to full-page patterns.
- If ids are missing, you usually have to refresh a larger subtree (or the whole page), which is more disruptive.

## Patterns & Best Practices

- Use `ctx.state` for server-owned logic (workflow steps, computed UI state, permissions).
- Use `ctx.store.local` for durable preferences (theme, table settings, dismissed banners).
- Use `ctx.store.session` for per-tab temporary data (drafts, wizard progress).
- Keep ids deterministic for components that need targeted refresh/update behavior.
- Prefer `ctx.refresh(target_id=...)` for localized visual changes.

## State vs Store

| | `ctx.state` | `ctx.store.local` / `ctx.store.session` |
|---|---|---|
| **Location** | Server (Python process) | Browser storage |
| **Lifetime** | WebSocket session | Across refreshes (`local`), until tab closes (`session`) |
| **Scope** | Single connection/tab | Browser origin (`local`) or single tab (`session`) |
| **Best for** | Runtime UI/app logic | Persistence and user preferences |
| **Sync behavior** | Immediate in memory | Cached in Python, optionally refreshed via `await ctx.store.sync()` |

## Important Notes

- `ctx.state` is reset when the WebSocket session ends (tab close/reload/disconnect).
- State is not shared between tabs unless you explicitly broadcast and synchronize.
- Store writes are queued and synced to browser automatically after updates.
- Call `await ctx.store.sync()` before reading values that may have changed directly in JavaScript.
- `ctx.refresh(target_id=...)` only updates that component subtree when the id exists in the latest render.

## Next Steps

- [Callbacks](/docs/concepts/callbacks) — Triggering updates and passing prop values
- [DOM Updates](/docs/concepts/updates) — Pushing changes to the UI
- [Routing & Navigation](/docs/concepts/routing) — How refresh and navigation interact
"""
