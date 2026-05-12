"""Popover — /docs/components/popover."""

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
    Popover,
    PopoverContent,
    PopoverTrigger,
    Row,
    Select,
    Separator,
    Text,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Popover"
PAGE_ROUTE = "/docs/components/popover"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_side(ctx: Context, value: str):
    ctx.state.set("pop_side", value)
    await ctx.refresh()


async def _set_align(ctx: Context, value: str):
    ctx.state.set("pop_align", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    side = ctx.state.get("pop_side", "bottom")
    align = ctx.state.get("pop_align", "center")

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Side", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["top", "right", "bottom", "left"]
                        ],
                        value=side,
                        on_change=ctx.callback(_set_side),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Align", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["start", "center", "end"]
                        ],
                        value=align,
                        on_change=ctx.callback(_set_align),
                    ),
                ],
            ),
        ],
        preview=[
            Popover(
                side=side,
                align=align,
                children=[
                    PopoverTrigger(
                        children=[Button("Open Popover")]
                    ),
                    PopoverContent(
                        side=side,
                        align=align,
                        children=[
                            Column(
                                gap=2,
                                children=[
                                    Text(
                                        "Popover Content",
                                        class_name="font-semibold text-sm",
                                    ),
                                    Text(
                                        "This is a floating content panel triggered by a button.",
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                    Text(
                                        f"side={side!r}, align={align!r}",
                                        class_name="text-xs font-mono text-muted-foreground mt-1",
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Popover(\n"
                f'    side="{side}",\n'
                f'    align="{align}",\n'
                f"    children=[\n"
                f"        PopoverTrigger(children=[Button(\"Open Popover\")]),\n"
                f"        PopoverContent(\n"
                f'            side="{side}",\n'
                f'            align="{align}",\n'
                f"            children=[...],\n"
                f"        ),\n"
                f"    ]\n"
                f")\n"
                f"```"
            )
        ),
        preview_class="border rounded-lg p-10 bg-muted/30 flex items-center justify-center min-h-[120px]",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Popover component reference page."""
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


# ── Content ───────────────────────────────────────────────────────────────

INTRO = """
Displays rich content in a floating panel, triggered by a button.
Unlike a tooltip, a popover can contain interactive elements.

```python
from refast.components import Popover, PopoverTrigger, PopoverContent
```
"""

REFERENCE = """
## Props

### `Popover`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `bool \\| None` | `None` | Controlled open state |
| `default_open` | `bool` | `False` | Initial open state |
| `on_open_change` | `Callback \\| None` | `None` | Called when open state changes |
| `side` | `"top" \\| "right" \\| "bottom" \\| "left"` | `"bottom"` | Preferred side |
| `align` | `"start" \\| "center" \\| "end"` | `"center"` | Content alignment |
| `trigger` | `Component \\| None` | `None` | Shorthand trigger component |

### `PopoverContent`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"top" \\| "right" \\| "bottom" \\| "left"` | `"bottom"` | Preferred side |
| `side_offset` | `int` | `4` | Pixels from the trigger |
| `align` | `"start" \\| "center" \\| "end"` | `"center"` | Alignment relative to trigger |

## Component Hierarchy

```
Popover
├── PopoverTrigger   ← button that opens the panel
└── PopoverContent   ← floating panel content
```

## Example — Settings Popover

```python
Popover(
    children=[
        PopoverTrigger(children=[IconButton(icon="settings")]),
        PopoverContent(
            side="bottom",
            align="end",
            children=[
                Heading("Display settings", level=4),
                Separator(class_name="my-2"),
                Row([Label("Theme"), Select(options=[...])]),
                Row([Label("Font size"), Select(options=[...])]),
            ]
        ),
    ]
)
```

## Shorthand with `trigger`

```python
Popover(
    trigger=Button("Options"),
    side="bottom",
    align="start",
    children=[
        PopoverContent(children=[...]),
    ]
)
```
"""
