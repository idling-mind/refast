"""DOM Updates — /docs/concepts/updates."""

import refast.components as rc
from refast.components import Badge, Button, Container, Heading, Separator, Text
from refast.context import Context

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "DOM Updates"
PAGE_ROUTE = "/docs/concepts/updates"

_ITEM_CLASS = "flex items-center justify-between rounded border px-3 py-2 text-sm bg-muted/30"


def _make_item(n: int, label: str | None = None, badge_variant: str = "secondary") -> rc.Container:
    """Return a styled list item with a stable id."""
    return rc.Container(
        id=f"updates-item-{n}",
        class_name=_ITEM_CLASS,
        children=[
            rc.Text(label or f"Item #{n}"),
            rc.Badge(f"#{n}", variant=badge_variant),
        ],
    )


# ---------------------------------------------------------------------------
# Callback functions (module-level so they are stable across renders)
# ---------------------------------------------------------------------------


async def demo_append_item(ctx: Context):
    count = ctx.state.get("demo_item_count", 2) + 1
    ctx.state.set("demo_item_count", count)
    await ctx.append("updates-list", _make_item(count))
    await ctx.update_text("updates-op-status", f"append → added Item #{count}")


async def demo_prepend_item(ctx: Context):
    count = ctx.state.get("demo_item_count", 2) + 1
    ctx.state.set("demo_item_count", count)
    await ctx.prepend("updates-list", _make_item(count, f"Item #{count} (prepended)", "outline"))
    await ctx.update_text("updates-op-status", f"prepend → added Item #{count} at top")


async def demo_remove_last(ctx: Context):
    count = ctx.state.get("demo_item_count", 2)
    if count < 1:
        await ctx.update_text("updates-op-status", "Nothing to remove.")
        return
    await ctx.remove(f"updates-item-{count}")
    ctx.state.set("demo_item_count", count - 1)
    await ctx.update_text("updates-op-status", f"remove → deleted Item #{count}")


async def demo_toggle_button(ctx: Context):
    disabled = ctx.state.get("demo_btn_disabled", False)
    new_disabled = not disabled
    ctx.state.set("demo_btn_disabled", new_disabled)
    await ctx.update_props(
        "updates-toggle-btn",
        {"disabled": new_disabled, "variant": "ghost" if new_disabled else "default"},
    )
    state_label = "disabled" if new_disabled else "enabled"
    await ctx.update_text("updates-op-status", f"update_props → toggle button is now {state_label}")


async def demo_replace_first(ctx: Context):
    flip = ctx.state.get("demo_replace_flip", False)
    ctx.state.set("demo_replace_flip", not flip)
    new_label = "Item #1 (replaced!)" if not flip else "Item #1"
    new_badge = "destructive" if not flip else "secondary"
    await ctx.replace("updates-item-1", _make_item(1, new_label, new_badge))
    await ctx.update_text("updates-op-status", "replace → swapped Item #1 in place")


async def demo_reset(ctx: Context):
    ctx.state.set("demo_item_count", 2)
    ctx.state.set("demo_btn_disabled", False)
    ctx.state.set("demo_replace_flip", False)
    await ctx.update_props(
        "updates-list",
        {"children": [_make_item(1), _make_item(2)]},
    )
    await ctx.update_props("updates-toggle-btn", {"disabled": False, "variant": "default"})
    await ctx.update_text("updates-op-status", "Reset to initial state.")


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------

CONTENT = r"""
## Overview

Refast gives you two strategies for pushing UI changes from Python:

1. **Full re-render** — re-run the page function and send the entire component tree.
2. **Targeted updates** — surgically modify one element by `id` without re-rendering anything else.

Use full re-renders for simplicity. Use targeted updates when you need to stream data,
update high-frequency values, or preserve focus and scroll position in unrelated parts
of the page.

---

## Full re-render: `ctx.refresh()`

`ctx.refresh()` re-runs the current page function with the latest state and sends the
resulting component tree to the client.

```python
async def increment(ctx: Context):
    ctx.state["count"] = ctx.state.get("count", 0) + 1
    await ctx.refresh()                         # full page re-render
```

Pass `target_id` to re-render only a subtree — Refast runs the page function, finds the
component with that id, and sends only that node as a targeted `replace` update.

```python
async def increment(ctx: Context):
    ctx.state["count"] = ctx.state.get("count", 0) + 1
    await ctx.refresh(target_id="counter-panel")  # only counter-panel is replaced
```

---

## Targeted updates

All methods below send a single WebSocket message that modifies one element.
The target component **must have an `id` prop** — Refast uses that to locate the DOM node.

### `ctx.replace(id, component)`

Swap an element entirely with a new component tree.

```python
await ctx.replace("my-card", Card(children=[Text("Updated content!")]))
```

### `ctx.append(id, component)` / `ctx.prepend(id, component)`

Add a child to the **end** or **beginning** of a container.

```python
await ctx.append("chat-list", MessageBubble(text="New message"))
await ctx.prepend("notifications", NotificationItem(msg="New alert"))
```

### `ctx.remove(id)`

Delete an element from the DOM.

```python
await ctx.remove("notification-42")
```

### `ctx.update_props(id, props)`

Change specific props without replacing the component.
Supports a special `"children"` key to replace all children at once.

```python
# Toggle a button
await ctx.update_props("submit-btn", {"disabled": True, "variant": "ghost"})

# Clear a container's children
await ctx.update_props("result-panel", {"children": []})

# Replace children with new components
await ctx.update_props("result-panel", {
    "children": [Heading("Results", level=3), Text("3 items found")],
})
```

### `ctx.update_text(id, text)`

Update only the text content of a component — the lightest possible update.

```python
await ctx.update_text("status-label", "Processing…")
await ctx.update_text("status-label", "Done!")
```

### `ctx.append_prop(id, prop_name, value)`

Append a value to a component's prop.
For string props it concatenates; for list props it appends (or extends for lists).
Primarily used for streaming text into a `Markdown` or `Text` component.

```python
# Stream LLM tokens into a Markdown component
async def stream_answer(ctx: Context):
    await ctx.update_props("ai-output", {"streaming": True})
    async for chunk in llm_stream():
        await ctx.append_prop("ai-output", "content", chunk)
    await ctx.update_props("ai-output", {"streaming": False})

# Append a data point to a chart
await ctx.append_prop("live-chart", "data", {"x": timestamp, "y": value})
```

---

## Performance comparison

| Method | Network cost | Re-render | Best for |
|---|---|---|---|
| `ctx.refresh()` | Full tree | Full | State-driven pages |
| `ctx.refresh(target_id=...)` | One subtree | Partial | Localised state changes |
| `ctx.replace()` | One component | None | Section swap |
| `ctx.append()` / `ctx.prepend()` | One component | None | Lists, feeds, chat |
| `ctx.remove()` | One ID | None | Deleting items |
| `ctx.update_props()` | Changed props only | None | Disabling, styling |
| `ctx.update_text()` | New string | None | Status labels, counters |
| `ctx.append_prop()` | Value delta | None | Streaming, live charts |

---

## Example: long-running task with progress

```python
import asyncio
from refast import Context
from refast.components import Progress, Text

async def run_task(ctx: Context):
    for i in range(10):
        await asyncio.sleep(0.5)
        pct = (i + 1) * 10
        await ctx.update_props("task-progress", {"value": pct})
        await ctx.update_text("task-status", f"Progress: {pct}%")
    await ctx.update_text("task-status", "Complete!")
```

---

## Live demo

Try the targeted update operations below. Each button calls a Python callback that
sends a focused WebSocket message — no full page re-render happens.

{{ updates_demo }}

---

## Important notes

- **IDs must be unique** in the rendered tree. Duplicate ids cause undefined behaviour.
- Targeted updates are **additive for the session** — items you append survive until the
  WebSocket session ends (tab close / reload). Use `ctx.refresh(target_id=...)` or
  `ctx.update_props(..., {"children": [...]})` to restore a known state.
- `ctx.update_props()` with `"children"` **replaces** all children of the target; it is
  not the same as appending.
- Targeted updates bypass the page render function, so they can run inside
  `asyncio.create_task()` background jobs without blocking the event loop.

---

## Next Steps

- [Routing & Navigation](/docs/concepts/routing) — SPA navigation and `ctx.load()`
- [Streaming](/docs/concepts/streaming) — Incremental text updates with `ctx.stream()`
- [Background Jobs](/docs/concepts/background) — Broadcasting updates to all clients
"""


def render(ctx):
    """Render the DOM updates concept page with a live demo."""
    from docs_site.app import docs_layout

    updates_demo = Container(
        id="updates-demo-container",
        class_name="space-y-4",
        children=[
            Heading("Live demo: targeted updates", level=3, class_name="text-lg font-semibold"),
            Text(
                "Each button sends one targeted WebSocket message. Watch the operation log below the list.",
                class_name="text-sm text-muted-foreground",
            ),
            # The list container — append/prepend/remove target this id
            Container(
                id="updates-list",
                class_name="flex flex-col gap-2 rounded-md border p-3 min-h-[96px]",
                children=[_make_item(1), _make_item(2)],
            ),
            # Operation log
            Text(
                "Waiting for an operation…",
                id="updates-op-status",
                class_name="text-xs text-muted-foreground font-mono",
            ),
            # Control buttons
            Container(
                class_name="flex flex-wrap gap-2",
                children=[
                    Button("append()", on_click=ctx.callback(demo_append_item), variant="default"),
                    Button(
                        "prepend()",
                        on_click=ctx.callback(demo_prepend_item),
                        variant="secondary",
                    ),
                    Button(
                        "remove() last",
                        on_click=ctx.callback(demo_remove_last),
                        variant="outline",
                    ),
                    Button(
                        "replace() Item #1",
                        on_click=ctx.callback(demo_replace_first),
                        variant="outline",
                    ),
                ],
            ),
            Container(
                class_name="flex flex-wrap gap-2 items-center",
                children=[
                    # This button's own props get toggled by demo_toggle_button
                    Button(
                        "update_props() toggle me",
                        id="updates-toggle-btn",
                        on_click=ctx.callback(demo_toggle_button),
                        variant="default",
                    ),
                    Badge("update_props target", variant="outline"),
                ],
            ),
            Button(
                "Reset demo",
                on_click=ctx.callback(demo_reset),
                variant="ghost",
                class_name="text-xs",
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
