"""Components — /docs/concepts/components."""

from refast.components import Badge, Container, Heading, Markdown, Separator, Text

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "Components"
PAGE_ROUTE = "/docs/concepts/components"


def render(ctx):
    """Render the components concept page."""
    from docs_site.app import docs_layout

    basic_demo = Container(
        children=[
            Heading("Hello", level=1),
            Text("World"),
        ]
    )

    live_demo = Container(
        id="components-live-demo",
        children=[
            Heading("Live demo: component tree", level=3, class_name="text-lg font-semibold"),
            Text(
                "This block is rendered with real components to show how nesting works.",
                class_name="text-sm text-muted-foreground",
            ),
            Container(
                class_name="mt-4 rounded-md border border-dashed p-4",
                children=[
                    Heading("Root Container", level=4, class_name="text-base font-semibold"),
                    Container(
                        class_name="space-y-2 rounded-md bg-muted/50 p-3",
                        children=[
                            Heading("Heading child", level=5),
                            Text("Text child inside the same container."),
                            Badge("Badge child", variant="secondary"),
                        ],
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


CONTENT = r"""
## Overview

Everything you see in a Refast UI is a **component**. Components are plain Python
objects that describe what should be rendered in the browser. They form a tree —
exactly like HTML nodes — and serialize to JSON that the React client renders.

## Basic usage

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

This tree is serialized and sent to the frontend for rendering.

{{ basic_demo }}


## Render model

Every component implements `render()` and returns a dict with `type`, `id`, `props`,
and `children`. Python `snake_case` props are converted to `camelCase` in the
frontend transport so React receives the right shape.

```python
container = Container(class_name="p-4", children=[Text("Hi")])
container.render()
# => {
#     "type": "Container",
#     "id": "auto-generated-uuid",
#     "props": {"class_name": "p-4", "style": {}},
#     "children": [
#         {"type": "Text", "id": "...", "props": {"class_name": "", "style": {}}, "children": ["Hi"]}
#     ]
# }
```

## Base components

| Component | Purpose | When to use |
|-----------|---------|-------------|
| `Container` | `<div>`-like wrapper that can hold children and utility classes | Any layout block, panels, cards |
| `Text` | Inline text node | Body copy, labels, helper text |
| `Fragment` | Groups children without adding a DOM element | When you need siblings without an extra wrapper |
| `Slot` | Placeholder that lets children flow through composed components | When building reusable component shells |

## Common props

| Prop | Type | Notes |
|------|------|-------|
| `id` | `str` | Auto-generated if omitted; set explicitly for targeted updates (`ctx.replace`, `ctx.update_props`, etc.) |
| `class_name` | `str` | Tailwind classes for styling; preferred over `style` |
| `children` | list, component, or string | Nested component tree; `None` values are ignored |
| `style` | `dict[str, Any]` | For dynamic inline values only (e.g., computed heights); keep static styles in `class_name` |
| `**props` | any | Extra props are forwarded and serialized; keep them `snake_case` so the client can convert to `camelCase` |

## Patterns & best practices

- Give components stable `id` values when you plan to target them with updates. It's also
  helpful to set explicit `id` for all components so that when you call `ctx.refresh()`
  the components that haven't changed don't get re-created with new auto-generated IDs.
- Keep `render()` pure: compute data before constructing components; do not mutate state there.
- Use `class_name` for styling; reserve `style` for computed values that Tailwind cannot express.
- Pass props in `snake_case`; in development you can set `REFAST_VALIDATE_PROPS=1` to log camelCase mistakes.
- Prefer composing small components instead of large monoliths so targeted updates stay cheap.

## Important notes

- Auto-generated IDs change when a component instance is recreated; set explicit IDs when a stable DOM target is required.
- Children must be components or strings; passing raw dicts will raise validation errors.
- The registry lookup is case-sensitive; `component_type` must match the registered name exactly.

- [Component Reference](/docs/components/layout) — Detailed props for each UI element

## Nested component example code

Here's a simple example of a nested component tree:

```python
Container(
    id="components-live-demo",
    children=[
        Heading("Live demo: component tree", level=3, class_name="text-lg font-semibold"),
        Text(
            "This block is rendered with real components to show how nesting works.",
            class_name="text-sm text-muted-foreground",
        ),
        Container(
            class_name="mt-4 rounded-md border border-dashed p-4",
            children=[
                Heading("Root Container", level=4, class_name="text-base font-semibold"),
                Container(
                    class_name="space-y-2 rounded-md bg-muted/50 p-3",
                    children=[
                        Heading("Heading child", level=5),
                        Text("Text child inside the same container."),
                        Badge("Badge child", variant="secondary"),
                    ],
                ),
            ],
        ),
    ],
)
```

{{ live_demo }}


## Next steps

- [Callbacks & Events](/docs/concepts/callbacks) — Wire components to interactions
- [State Management](/docs/concepts/state) — Keep data across callbacks
- [DOM Updates](/docs/concepts/updates) — Targeted replacements, appends, and prop updates
"""
