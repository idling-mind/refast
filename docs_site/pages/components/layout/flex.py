"""Flex — /docs/components/flex."""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Button,
    Checkbox,
    Column,
    Container,
    Flex,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Flex"
PAGE_ROUTE = "/docs/components/flex"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_direction(ctx: Context, value: str):
    ctx.state.set("fx_direction", value)
    await ctx.refresh()


async def _set_justify(ctx: Context, value: str):
    ctx.state.set("fx_justify", value)
    await ctx.refresh()


async def _set_align(ctx: Context, value: str):
    ctx.state.set("fx_align", value)
    await ctx.refresh()


async def _set_gap(ctx: Context, value: str):
    ctx.state.set("fx_gap", value)
    await ctx.refresh()


async def _set_wrap(ctx: Context, value: bool):
    ctx.state.set("fx_wrap", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    direction = ctx.state.get("fx_direction", "row")
    justify = ctx.state.get("fx_justify", "start")
    align = ctx.state.get("fx_align", "stretch")
    gap = int(ctx.state.get("fx_gap", "2"))
    wrap = ctx.state.get("fx_wrap", False)

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("direction", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in [
                                "row",
                                "column",
                                "row-reverse",
                                "column-reverse",
                            ]
                        ],
                        value=direction,
                        on_change=ctx.callback(_set_direction),
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
                            for v in ["1", "2", "4", "6"]
                        ],
                        value=str(gap),
                        on_change=ctx.callback(_set_gap),
                    ),
                ],
            ),
            Column(
                gap=2,
                justify="end",
                children=[
                    Row(
                        gap=2,
                        align="center",
                        children=[
                            Checkbox(
                                checked=wrap,
                                on_change=ctx.callback(_set_wrap),
                                id="fx-wrap-cb",
                            ),
                            Text("wrap", class_name="text-sm"),
                        ],
                    ),
                ],
            ),
        ],
        preview=[
            Flex(
                direction=direction,
                justify=justify,
                align=align,
                gap=gap,
                wrap=wrap,
                children=[
                    Button("Alpha", variant="outline"),
                    Button("Beta", variant="outline"),
                    Button("Gamma", variant="outline"),
                ],
            )
        ],
        preview_class="border rounded-lg p-4 bg-muted/30 min-h-[120px]",
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
Generic flexbox container with full directional control. For most cases prefer
`Row` (horizontal) or `Column` (vertical) directly — `Flex` is useful when you
need to switch direction dynamically.

```python
from refast.components import Flex

Flex(
    direction="row",
    justify="between",
    align="center",
    gap=4,
    wrap=True,
    children=[...],
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \\| Component \\| None` | `None` | Child components |
| `direction` | `"row" \\| "column" \\| "row-reverse" \\| "column-reverse"` | `"row"` | flex-direction |
| `justify` | `"start" \\| "end" \\| "center" \\| "between" \\| "around" \\| "evenly"` | `"start"` | justify-content |
| `align` | `"start" \\| "end" \\| "center" \\| "stretch" \\| "baseline"` | `"stretch"` | align-items |
| `wrap` | `bool` | `False` | Whether children wrap |
| `gap` | `int` | `2` | Gap between children (Tailwind spacing unit) |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Notes

`Flex` maps directly to `Row` when `direction="row"` and `Column` when
`direction="column"` on the React side. Prefer `Row`/`Column` for static layouts.
"""
