"""Grid — /docs/components/grid."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Grid,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Grid"
PAGE_ROUTE = "/docs/components/grid"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_cols(ctx: Context, value: str):
    ctx.state.set("gr_cols", value)
    await ctx.refresh()


async def _set_gap(ctx: Context, value: str):
    ctx.state.set("gr_gap", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    cols = int(ctx.state.get("gr_cols", "3"))
    gap = int(ctx.state.get("gr_gap", "4"))

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
                                    Text("columns", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in ["1", "2", "3", "4", "5", "6"]
                                        ],
                                        value=str(cols),
                                        on_change=ctx.callback(_set_cols),
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
                                            for v in ["1", "2", "4", "6"]
                                        ],
                                        value=str(gap),
                                        on_change=ctx.callback(_set_gap),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30",
                        children=[
                            Grid(
                                columns=cols,
                                gap=gap,
                                children=[
                                    Container(
                                        class_name="border rounded-md p-3 bg-background text-center text-sm font-medium",
                                        children=[Text(f"Cell {i + 1}")],
                                    )
                                    for i in range(cols * 2)
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
CSS Grid container for equal-column layouts.

```python
from refast.components import Grid

Grid(
    columns=3,
    gap=4,
    children=[Card(...) for _ in range(6)],
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \\| Component \\| None` | `None` | Grid cell components |
| `columns` | `int \\| str` | `1` | Number of equal columns, or a CSS `gridTemplateColumns` string |
| `rows` | `int \\| str \\| None` | `None` | Number of equal rows, or a CSS `gridTemplateRows` string |
| `gap` | `int` | `4` | Gap between cells (Tailwind spacing unit) |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Advanced: Custom Template

Pass a CSS string to `columns` or `rows` for custom sizing:

```python
Grid(
    columns="200px 1fr 200px",
    gap=4,
    children=[sidebar, main, aside],
)
```

## Examples

```python
# 3-column card grid
Grid(
    columns=3,
    gap=6,
    class_name="max-w-5xl",
    children=[
        Card(children=[CardHeader(title=title)])
        for title in ["Alpha", "Beta", "Gamma"]
    ],
)
```
"""
