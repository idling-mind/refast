"""Column — /docs/components/column."""

from refast import Context
from refast.components import (
    Badge,
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
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Column"
PAGE_ROUTE = "/docs/components/column"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_gap(ctx: Context, value: str):
    ctx.state.set("col_gap", value)
    await ctx.refresh()


async def _set_align(ctx: Context, value: str):
    ctx.state.set("col_align", value)
    await ctx.refresh()


async def _set_justify(ctx: Context, value: str):
    ctx.state.set("col_justify", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    gap = int(ctx.state.get("col_gap", "2"))
    align = ctx.state.get("col_align", "stretch")
    justify = ctx.state.get("col_justify", "start")

    return playground_card(
        options=[
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
        ],
        preview=[
            Column(
                gap=gap,
                align=align,
                justify=justify,
                children=[
                    Button("First item", variant="outline"),
                    Button("Second item", variant="outline"),
                    Button("Third item", variant="outline"),
                ],
            )
        ],
        preview_class="border rounded-lg p-4 bg-muted/30 min-h-[160px]",
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
Vertical flex container (`flex flex-col`) for stacking children top-to-bottom.

```python
from refast.components import Column

Column(
    children=[
        Heading("Title", level=2),
        Text("Subtitle text"),
        Button("Call to action"),
    ],
    gap=4,
    align="start",
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \\| Component \\| None` | `None` | Child components |
| `justify` | `"start" \\| "end" \\| "center" \\| "between" \\| "around" \\| "evenly"` | `"start"` | justify-content |
| `align` | `"start" \\| "end" \\| "center" \\| "stretch" \\| "baseline"` | `"stretch"` | align-items |
| `gap` | `int` | `2` | Gap between children (Tailwind spacing unit) |
| `wrap` | `bool` | `False` | Whether children wrap |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Notes

`Column` defaults `align` to `"stretch"` (unlike `Row` which defaults to `"start"`),
so children fill the column's cross-axis width by default.

## Examples

```python
# Form field stack
Column(
    gap=4,
    children=[
        Input(label="Name", placeholder="Your name"),
        Input(label="Email", type="email"),
        Button("Submit"),
    ],
)

# Sidebar navigation
Column(
    gap=1,
    class_name="w-48",
    children=[NavLink(href=r) for r in routes],
)
```
"""
