"""Store (Browser Storage) — /docs/concepts/store."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Store (Browser Storage)"
PAGE_ROUTE = "/docs/concepts/store"


def render(ctx):
    """Render the store concept page."""
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

`ctx.store` provides Python access to the browser's `localStorage` and `sessionStorage`.
Unlike `ctx.state` (server-side, lost on disconnect), the store persists across page
reloads and reconnections.

## Two Stores

```python
# localStorage — persists until explicitly cleared
ctx.store.local.set("theme", "dark")
ctx.store.local.get("theme")

# sessionStorage — cleared when the tab closes
ctx.store.session.set("draft", "hello")
ctx.store.session.get("draft")
```

## store_as — Form Input Shortcut

The `store_as` parameter on callbacks automatically stores the input value client-side:

```python
Input(placeholder="Email", store_as="email")

async def submit(ctx: Context):
    email = ctx.prop_store.get("email", "")
    # Process the email...
```

This avoids a server roundtrip on every keystroke — the value is stored in the browser
and only sent when a callback reads `ctx.prop_store`.

## Syncing

To get the latest values from the browser:

```python
await ctx.sync_store()
# Now ctx.store.local and ctx.store.session are up-to-date
```

## API Reference

| Method | Description |
|--------|-------------|
| `store.local.get(key, default)` | Read from localStorage |
| `store.local.set(key, value)` | Write to localStorage |
| `store.local.delete(key)` | Remove a key |
| `store.local.clear()` | Clear all localStorage |
| `store.local.get_all()` | Get all key-value pairs |
| `store.session.*` | Same API for sessionStorage |
| `await ctx.sync_store()` | Pull latest values from browser |

## Next Steps

- [DOM Updates](/docs/concepts/updates) — Pushing changes to the UI
- [Callbacks](/docs/concepts/callbacks) — How store_as works with callbacks
"""
