"""Row — /docs/components/row."""

from refast import Context
from refast.components import (
    Button,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Row"
PAGE_ROUTE = "/docs/components/row"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_justify(ctx: Context, value: str):
    ctx.state.set("row_justify", value)
    await ctx.refresh()


async def _set_align(ctx: Context, value: str):
    ctx.state.set("row_align", value)
    await ctx.refresh()


async def _set_gap(ctx: Context, value: str):
    ctx.state.set("row_gap", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    justify = ctx.state.get("row_justify", "start")
    align = ctx.state.get("row_align", "start")
    gap = int(ctx.state.get("row_gap", "2"))

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
                                    Text("justify", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in [
                                                "start",
                                                "end",
                                                "center",
                                                "between",
                                                "around",
                                                "evenly",
                                            ]
                                        ],
                                        value=justify,
                                        on_change=ctx.callback(_set_justify),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("align", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in [
                                                "start",
                                                "end",
                                                "center",
                                                "stretch",
                                                "baseline",
                                            ]
                                        ],
                                        value=align,
                                        on_change=ctx.callback(_set_align),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("gap", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in ["1", "2", "4", "6", "8"]
                                        ],
                                        value=str(gap),
                                        on_change=ctx.callback(_set_gap),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30 min-h-[80px]",
                        children=[
                            Row(
                                justify=justify,
                                align=align,
                                gap=gap,
                                children=[
                                    Button("Item 1", variant="outline"),
                                    Button("Item 2", variant="outline"),
                                    Button("Item 3", variant="outline"),
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
Horizontal flex container (`flex flex-row`) for arranging children side by side.

```python
from refast.components import Row

Row(
    children=[Button("Save"), Button("Cancel", variant="outline")],
    justify="end",
    align="center",
    gap=2,
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \\| Component \\| None` | `None` | Child components |
| `justify` | `"start" \\| "end" \\| "center" \\| "between" \\| "around" \\| "evenly"` | `"start"` | justify-content |
| `align` | `"start" \\| "end" \\| "center" \\| "stretch" \\| "baseline"` | `"start"` | align-items |
| `gap` | `int` | `2` | Gap between children (Tailwind spacing unit) |
| `wrap` | `bool` | `False` | Whether children wrap |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Examples

```python
# Spaced action bar
Row(
    justify="between",
    align="center",
    children=[
        Heading("Page Title", level=2),
        Row(gap=2, children=[Button("New"), Button("Settings", variant="ghost")]),
    ],
)

# Wrapping tag list
Row(
    wrap=True,
    gap=2,
    children=[Badge(children=[tag]) for tag in tags],
)
```
"""
