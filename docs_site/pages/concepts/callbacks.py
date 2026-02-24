"""Callbacks & Events — /docs/concepts/callbacks."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Callbacks & Events"
PAGE_ROUTE = "/docs/concepts/callbacks"


def render(ctx):
    """Render the callbacks concept page."""
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

Callbacks are the bridge between user interactions in the browser and Python functions
on the server. When a user clicks a button or changes an input, a callback sends an
event through the WebSocket to invoke your Python function.

## Creating Callbacks

```python
async def handle_click(ctx: Context):
    await ctx.show_toast("Clicked!", variant="success")

Button("Click Me", on_click=ctx.callback(handle_click))
```

## Bound Arguments

You can bind extra arguments to a callback:

```python
async def select_item(ctx: Context, item_id: str):
    ctx.state.set("selected", item_id)
    await ctx.refresh()

Button("Select", on_click=ctx.callback(select_item, item_id="abc123"))
```

## Event Props

| Prop | Triggered When |
|------|---------------|
| `on_click` | Element is clicked |
| `on_change` | Input value changes |
| `on_submit` | Form is submitted |
| `on_value_change` | Slider value changes |
| `on_value_commit` | Slider value committed |
| `on_pressed_change` | Toggle state changes |
| `on_open_change` | Dialog/sheet/popover opens or closes |
| `on_select` | Calendar date selected / Select value changes |
| `...` | Other events |

## The Callback Flow

1. User interacts with a component (click, type, etc.)
2. Frontend sends a `callback` message via WebSocket with the callback ID and data
3. Refast looks up the registered callback function
4. Your Python function runs with the `Context` — it can update state, push DOM updates, etc.
5. Any updates are sent back to the frontend via the same WebSocket

## save_prop — Instant Frontend State

For forms, you can avoid a server roundtrip on every keystroke by
storing input values directly in the frontend using `ctx.save_prop`:

```python
Input(placeholder="Name", on_change=ctx.save_prop("user_name"))
Button("Submit", on_click=ctx.callback(submit, props=["user_name"]))

async def submit(ctx: Context, user_name: str=""):
    await ctx.show_toast(f"Hello, {user_name}!", variant="success")
```

## Next Steps

- [State Management](/docs/concepts/state) — Persisting data across callbacks
- [DOM Updates](/docs/concepts/updates) — Pushing UI changes from Python
"""
