"""Routing & Navigation — /docs/concepts/routing."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Routing & Navigation"
PAGE_ROUTE = "/docs/concepts/routing"


def render(ctx):
    """Render the routing concept page."""
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

Refast supports **multi-page applications** with SPA-style navigation. Each page is
registered with `@ui.page()` and navigation happens via `ctx.navigate()`.

## Registering Pages

```python
ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    return Container(children=[Heading("Home")])

@ui.page("/about")
def about(ctx: Context):
    return Container(children=[Heading("About")])

@ui.page("/settings")
def settings(ctx: Context):
    return Container(children=[Heading("Settings")])
```

## Navigating Between Pages

```python
async def go_to_about(ctx: Context):
    await ctx.navigate("/about")

Button("About", on_click=ctx.callback(go_to_about))
```

## How SPA Navigation Works

1. `ctx.navigate("/about")` tells the frontend to fetch the new page
2. Frontend requests `GET /about?format=json` (JSON only, no HTML shell)
3. React swaps the component tree in place
4. **WebSocket stays connected** — `ctx.state` persists across navigations

## Refreshing the Current Page

```python
# Re-render the current page
await ctx.refresh()

# Navigate to a specific page (also re-renders)
await ctx.refresh("/settings")
```

## Link Component

For declarative navigation in the UI:

```python
Link("Go to About", href="/about")
```

## Important Notes

- Each page handler gets a fresh `ctx` argument but the **same WebSocket context** persists
- `ctx.state` carries over across `ctx.navigate()` calls
- On full page reload (F5), state is lost but `ctx.store` persists
- There's no wildcard/catch-all route support — each page must be registered explicitly

## Next Steps

- [Streaming](/docs/concepts/streaming) — Incremental content delivery
- [Background Jobs](/docs/concepts/background) — Running tasks across pages
"""
