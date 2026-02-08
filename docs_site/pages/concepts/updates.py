"""DOM Updates — /docs/concepts/updates."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "DOM Updates"
PAGE_ROUTE = "/docs/concepts/updates"


def render(ctx):
    """Render the DOM updates concept page."""
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

Refast provides two approaches to updating the UI from Python:

1. **Full re-render** — Rebuild the entire page from state
2. **Targeted updates** — Surgically modify specific elements by ID

## Full Re-Render

```python
async def handle_click(ctx: Context):
    ctx.state.set("count", ctx.state.get("count", 0) + 1)
    await ctx.refresh()  # Re-runs the page handler, sends full tree
```

`ctx.push_update()` does the same thing — re-renders and sends the full component tree.

## Targeted Updates

For better performance, update only what changed:

```python
# Replace a component entirely
await ctx.replace("my-card", Card(children=[Text("Updated!")]))

# Append a child to a container
await ctx.append("todo-list", new_todo_item)

# Prepend a child
await ctx.prepend("messages", new_message)

# Remove an element
await ctx.remove("item-42")

# Update specific props without re-rendering
await ctx.update_props("my-button", {"variant": "secondary", "disabled": True})

# Update text content
await ctx.update_text("status-label", "Processing...")

# Append to a list prop (e.g., adding options to a select)
await ctx.append_prop("my-chart", "data", new_data_point)
```

> **Important**: Targeted updates require the target component to have an `id` prop.

## When to Use Which

| Approach | Best For |
|----------|----------|
| `ctx.refresh()` | Simple state changes, full page updates |
| `ctx.replace()` | Swapping a section with new content |
| `ctx.append()` / `ctx.prepend()` | Adding items to lists (chat, todos) |
| `ctx.update_props()` | Changing styles, disabled state, values |
| `ctx.remove()` | Deleting items |

## Example: Progress Updates

```python
async def long_task(ctx: Context):
    for i in range(100):
        await ctx.update_props("progress-bar", {"value": i + 1})
        await asyncio.sleep(0.05)
    await ctx.update_text("status", "Complete!")
```

## Next Steps

- [Routing & Navigation](/docs/concepts/routing) — Multi-page navigation
- [Streaming](/docs/concepts/streaming) — Incremental content updates
"""
