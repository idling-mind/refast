"""Text & Paragraph — /docs/components/text."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Paragraph,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Text & Paragraph"
PAGE_ROUTE = "/docs/components/text"

_SAMPLE = "The quick brown fox jumps over the lazy dog."


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_color(ctx: Context, value: str):
    ctx.state.set("tx_color", value)
    await ctx.refresh()


async def _set_size(ctx: Context, value: str):
    ctx.state.set("tx_size", value)
    await ctx.refresh()


async def _set_weight(ctx: Context, value: str):
    ctx.state.set("tx_weight", value)
    await ctx.refresh()


async def _set_lead(ctx: Context, value: bool):
    ctx.state.set("tx_lead", value)
    await ctx.refresh()


async def _set_muted(ctx: Context, value: bool):
    ctx.state.set("tx_muted", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    color = ctx.state.get("tx_color", "")
    size = ctx.state.get("tx_size", "text-base")
    weight = ctx.state.get("tx_weight", "font-normal")
    lead = ctx.state.get("tx_lead", False)
    muted = ctx.state.get("tx_muted", False)

    text_class = " ".join(filter(None, [color, size, weight]))
    para_class = " ".join(filter(None, [color, size, weight]))

    return Card(
        children=[
            CardHeader(title="Interactive Playground — Text"),
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
                                    Text("color", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": l}
                                            for v, l in [
                                                ("", "default"),
                                                ("text-muted-foreground", "muted"),
                                                ("text-primary", "primary"),
                                                ("text-destructive", "destructive"),
                                                ("text-blue-600", "blue"),
                                            ]
                                        ],
                                        value=color,
                                        on_change=ctx.callback(_set_color),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("size", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in [
                                                "text-xs",
                                                "text-sm",
                                                "text-base",
                                                "text-lg",
                                                "text-xl",
                                                "text-2xl",
                                            ]
                                        ],
                                        value=size,
                                        on_change=ctx.callback(_set_size),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("weight", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in [
                                                "font-light",
                                                "font-normal",
                                                "font-medium",
                                                "font-semibold",
                                                "font-bold",
                                            ]
                                        ],
                                        value=weight,
                                        on_change=ctx.callback(_set_weight),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30",
                        children=[
                            Column(
                                gap=3,
                                children=[
                                    Text(
                                        "Text component: " + _SAMPLE,
                                        class_name=text_class,
                                    ),
                                ],
                            )
                        ],
                    ),
                ]
            ),
        ]
    )


def _para_playground(ctx: Context):
    lead = ctx.state.get("tx_lead", False)
    muted = ctx.state.get("tx_muted", False)

    return Card(
        children=[
            CardHeader(title="Interactive Playground — Paragraph"),
            CardContent(
                children=[
                    Row(
                        gap=4,
                        class_name="mb-4",
                        children=[
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Checkbox(
                                        checked=lead,
                                        on_change=ctx.callback(_set_lead),
                                        id="tx-lead-cb",
                                    ),
                                    Text("lead (larger intro text)", class_name="text-sm"),
                                ],
                            ),
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Checkbox(
                                        checked=muted,
                                        on_change=ctx.callback(_set_muted),
                                        id="tx-muted-cb",
                                    ),
                                    Text("muted (text-muted-foreground)", class_name="text-sm"),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30",
                        children=[
                            Paragraph(
                                "Paragraph component: " + _SAMPLE,
                                lead=lead,
                                muted=muted,
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
            _para_playground(ctx),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


INTRO = """
Two text primitives: **`Text`** for inline/span-like text, and **`Paragraph`**
for block-level `<p>` elements.

```python
from refast.components import Text, Paragraph

# Inline text with Tailwind classes
Text("Hello world", class_name="text-lg font-semibold text-primary")

# Block paragraph
Paragraph("Body copy goes here.", muted=True)

# Lead paragraph (larger intro text)
Paragraph("Welcome to the docs.", lead=True)
```
"""

REFERENCE = """
## Text Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `str` | *(required)* | Text content |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Tailwind CSS classes |
| `style` | `dict \\| None` | `None` | Inline CSS overrides |

## Paragraph Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | *(required)* | Paragraph content |
| `lead` | `bool` | `False` | Larger lead paragraph style |
| `muted` | `bool` | `False` | Applies `text-muted-foreground` |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |
| `style` | `dict \\| None` | `None` | Inline CSS overrides |

## Notes

Use `Text` when you need fine-grained control over individual spans. Use
`Paragraph` for prose content — it renders a semantic `<p>` element.
"""
