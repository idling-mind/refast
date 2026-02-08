"""Components — /docs/concepts/components."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Components"
PAGE_ROUTE = "/docs/concepts/components"


def render(ctx):
    """Render the components concept page."""
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

Everything in Refast's UI is a **component**. Components are Python objects that describe
what should be rendered in the browser. They form a tree — just like HTML elements do.

## The Component Tree

A page handler returns a root component. That component has children, which have their
own children, forming a tree:

```python
Container(
    children=[
        Heading("Hello", level=1),
        Text("World"),
    ]
)
```

This gets serialized to JSON and sent to the React frontend, which renders it.

## Base Components

| Component | Purpose |
|-----------|---------|
| `Container` | A `<div>` wrapper — the most common layout element |
| `Text` | A `<span>` for inline text |
| `Fragment` | Groups children without adding a DOM wrapper |

## Common Props

Every component accepts:

- **`id`** — Unique identifier for targeted updates (`ctx.replace()`, etc.)
- **`class_name`** — Tailwind CSS classes for styling
- **`children`** — List of child components
- **`style`** — Dict of CSS properties (for dynamic values only)

## Rendering

Components have a `render()` method that produces a JSON-serializable dict:

```python
{
    "type": "Container",
    "id": "my-container",
    "props": {"className": "p-4"},
    "children": [...]
}
```

> **Note**: Python `snake_case` props are automatically converted to `camelCase` for the frontend.

## Next Steps

- [Callbacks & Events](/docs/concepts/callbacks) — Making components interactive
- [Component Reference](/docs/components/layout) — Full API for each component
"""
