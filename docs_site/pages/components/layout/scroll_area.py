"""ScrollArea — /docs/components/scroll-area."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    ScrollArea,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "ScrollArea"
PAGE_ROUTE = "/docs/components/scroll-area"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_type(ctx: Context, value: str):
    ctx.state.set("sa_type", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    scroll_type = ctx.state.get("sa_type", "hover")

    items = [
        "JavaScript",
        "TypeScript",
        "Python",
        "Rust",
        "Go",
        "Java",
        "C++",
        "Swift",
        "Kotlin",
        "Ruby",
        "Scala",
        "Haskell",
        "Elixir",
        "Clojure",
        "Dart",
    ]

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    Row(
                        gap=4,
                        wrap=True,
                        class_name="mb-4",
                        children=[
                            Column(
                                gap=1,
                                children=[
                                    Text("type", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in ["auto", "always", "scroll", "hover"]
                                        ],
                                        value=scroll_type,
                                        on_change=ctx.callback(_set_type),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Text(
                        "Hover over the area or scroll inside it to see the scrollbar:",
                        class_name="text-sm text-muted-foreground mb-2",
                    ),
                    ScrollArea(
                        type=scroll_type,
                        class_name="border rounded-lg",
                        style={"height": "12rem", "width": "16rem"},
                        children=[
                            Column(
                                gap=1,
                                class_name="p-3",
                                children=[
                                    Container(
                                        class_name="py-1 px-2 rounded text-sm hover:bg-muted cursor-default",
                                        children=[Text(item)],
                                    )
                                    for item in items
                                ],
                            )
                        ],
                    ),
                ]
            ),
        ]
    )


def render(ctx: Context):
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _playground(ctx),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


INTRO = """
A scrollable container with custom, styled scrollbars (Radix UI `ScrollArea`).

```python
from refast.components import ScrollArea

ScrollArea(
    class_name="h-72 w-48",
    children=[
        # tall content here
    ]
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \\| Component \\| None` | `None` | Scrollable content |
| `type` | `"auto" \\| "always" \\| "scroll" \\| "hover"` | `"hover"` | When the scrollbar is visible |
| `scroll_hide_delay` | `int` | `600` | ms before scrollbar hides (hover/scroll modes) |
| `dir` | `"ltr" \\| "rtl" \\| None` | `None` | Reading direction (inherits from document) |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes (use for height/width) |

## Notes

Always set a height via `class_name` (e.g. `h-72`). The `type` prop controls
scrollbar visibility:

- `"hover"` — shows on mouse hover  
- `"auto"` — shows when content overflows  
- `"always"` — always visible  
- `"scroll"` — shows while actively scrolling  

## Examples

```python
# Vertical list in a fixed height box
ScrollArea(
    class_name="h-80",
    children=[Column(gap=1, children=[Text(item) for item in long_list])],
)

# Horizontal scroll
ScrollArea(
    class_name="w-full",
    children=[
        Row(
            gap=4,
            class_name="w-max",
            children=[Card(...) for _ in range(20)],
        )
    ],
)
```
"""
