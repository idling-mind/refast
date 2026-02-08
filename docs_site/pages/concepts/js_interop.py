"""JavaScript Interop — /docs/concepts/js-interop."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "JavaScript Interop"
PAGE_ROUTE = "/docs/concepts/js-interop"


def render(ctx):
    """Render the JS interop concept page."""
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

Sometimes you need client-side logic without a server roundtrip — animations, DOM
manipulation, localStorage access, or third-party JS library calls. Refast provides
several JavaScript interop mechanisms.

## ctx.js() — Client-Side Callback

Creates a callback that runs JavaScript in the browser, no server roundtrip:

```python
Button(
    "Toggle Dark Mode",
    on_click=ctx.js("document.documentElement.classList.toggle('dark')"),
)
```

## ctx.bound_js() — Target Element Methods

Call methods on a specific component by ID:

```python
ctx.bound_js("my-video", "play")
ctx.bound_js("my-dialog", "showModal")
```

## ctx.call_js() — Immediate Execution

Execute JavaScript immediately from a Python callback:

```python
async def save_to_clipboard(ctx: Context):
    await ctx.call_js("navigator.clipboard.writeText('Hello!')")
```

## ctx.call_bound_js() — Immediate Bound Call

```python
async def focus_input(ctx: Context):
    await ctx.call_bound_js("my-input", "focus")
```

## Summary

| Method | When It Runs | Server Roundtrip? |
|--------|-------------|-------------------|
| `ctx.js(code)` | On user interaction | No |
| `ctx.bound_js(id, method)` | On user interaction | No |
| `ctx.call_js(code)` | Immediately (from Python) | No (sent via WS) |
| `ctx.call_bound_js(id, method)` | Immediately (from Python) | No (sent via WS) |
| `ctx.callback(fn)` | On user interaction | Yes |

## When to Use JS vs Python Callbacks

**Use JS callbacks** for:
- UI-only interactions (toggle class, scroll, focus)
- Performance-sensitive actions (hover effects)
- Browser API access (clipboard, geolocation)

**Use Python callbacks** for:
- Business logic, data processing
- State changes that affect the UI
- Database or API operations

## Next Steps

- [Building Components](/docs/advanced/component-dev) — Custom component development
- [Building Extensions](/docs/advanced/extension-dev) — Packaging reusable functionality
"""
