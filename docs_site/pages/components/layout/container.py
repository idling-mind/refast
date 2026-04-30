"""Container — /docs/components/container."""

from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Container"
PAGE_ROUTE = "/docs/components/container"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_padding(ctx: Context, value: str):
    ctx.state.set("con_padding", value)
    await ctx.refresh()


async def _set_border(ctx: Context, value: bool):
    ctx.state.set("con_border", value)
    await ctx.refresh()


async def _set_rounded(ctx: Context, value: bool):
    ctx.state.set("con_rounded", value)
    await ctx.refresh()


async def _set_bg(ctx: Context, value: str):
    ctx.state.set("con_bg", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    padding = ctx.state.get("con_padding", "p-4")
    border = ctx.state.get("con_border", False)
    rounded = ctx.state.get("con_rounded", False)
    bg = ctx.state.get("con_bg", "none")

    # Build class_name from options
    classes = [padding]
    if border:
        classes.append("border")
    if rounded:
        classes.append("rounded-lg")
    if bg == "muted":
        classes.append("bg-muted")
    elif bg == "muted/30":
        classes.append("bg-muted/30")
    elif bg == "primary/10":
        classes.append("bg-primary/10")
    class_name = " ".join(classes)

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    Row(
                        gap=4,
                        wrap=True,
                        class_name="mb-6",
                        children=[
                            Column(
                                gap=1,
                                children=[
                                    Text("Padding", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in ["p-2", "p-4", "p-6", "p-8"]
                                        ],
                                        value=padding,
                                        on_change=ctx.callback(_set_padding),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("Background", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": l}
                                            for v, l in [
                                                ("none", "none"),
                                                ("muted", "bg-muted"),
                                                ("muted/30", "bg-muted/30"),
                                                ("primary/10", "bg-primary/10"),
                                            ]
                                        ],
                                        value=bg,
                                        on_change=ctx.callback(_set_bg),
                                    ),
                                ],
                            ),
                            Column(
                                gap=2,
                                children=[
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                checked=border,
                                                on_change=ctx.callback(_set_border),
                                                id="con-border-cb",
                                            ),
                                            Text("border", class_name="text-sm"),
                                        ],
                                    ),
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                checked=rounded,
                                                on_change=ctx.callback(_set_rounded),
                                                id="con-rounded-cb",
                                            ),
                                            Text("rounded-lg", class_name="text-sm"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Preview
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30",
                        children=[
                            Container(
                                class_name=class_name,
                                children=[
                                    Text("Container content", class_name="text-sm font-medium"),
                                    Text(
                                        "This text lives inside the Container.",
                                        class_name="text-sm text-muted-foreground mt-1",
                                    ),
                                    Row(
                                        gap=2,
                                        class_name="mt-3",
                                        children=[
                                            Button("Action", size="sm"),
                                            Button("Cancel", size="sm", variant="outline"),
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                    Text(
                        f'class_name="{class_name}"',
                        class_name="text-xs text-muted-foreground mt-2 font-mono",
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
Generic `<div>` wrapper. Use `Container` to group elements and apply Tailwind
utility classes for spacing, borders, backgrounds, and layout.

```python
from refast.components import Container

Container(
    class_name="p-4 border rounded-lg bg-muted/30",
    children=[
        Text("Hello from inside a Container"),
    ],
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \\| Component \\| None` | `None` | Child components |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Tailwind CSS classes |
| `style` | `dict \\| None` | `None` | Inline CSS overrides |

## Notes

`Container` renders a plain `<div>`. It is the most basic building block — use
`Row`, `Column`, `Grid`, or `Flex` when you need flex/grid layout semantics.
Pass any Tailwind classes you need via `class_name`.

## Examples

```python
# Card-like container
Container(
    class_name="p-6 border rounded-xl shadow-sm",
    children=[Heading("My Card", level=3)],
)

# Full-width section with background
Container(
    class_name="w-full bg-muted py-12 px-6",
    children=[...],
)
```
"""
