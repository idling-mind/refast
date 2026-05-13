"""Badge — /docs/components/badge."""

from refast import Context
from docs_site.pages.components.playground import playground_card
from refast.components import (
    Badge,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Input,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Badge"
PAGE_ROUTE = "/docs/components/badge"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_variant(ctx: Context, value: str):
    ctx.state.set("bg_variant", value)
    await ctx.refresh()


async def _set_text(ctx: Context, value: str):
    ctx.state.set("bg_text", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    variant = ctx.state.get("bg_variant", "default")
    badge_text = ctx.state.get("bg_text", "Badge")

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("variant", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in [
                                "default",
                                "secondary",
                                "destructive",
                                "outline",
                                "success",
                                "warning",
                            ]
                        ],
                        value=variant,
                        on_change=ctx.callback(_set_variant),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("text", class_name="text-sm font-medium"),
                    Input(
                        value=badge_text,
                        placeholder="Badge text...",
                        on_change=ctx.callback(_set_text),
                        debounce=300,
                    ),
                ],
            ),
        ],
        preview=[
            Badge(
                children=[badge_text or "Badge"],
                variant=variant,
            )
        ],
        preview_class="border rounded-lg p-6 bg-muted/30 flex items-center justify-center min-h-[80px]",
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
Small label for statuses, categories, and counts.

```python
from refast.components import Badge

Badge(children=["New"])
Badge(children=["Error"], variant="destructive")
Badge(children=["Active"], variant="success")
Badge(children=["Draft"], variant="outline")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \\| Component \\| None` | `None` | Badge content (usually a short string) |
| `variant` | `"default" \\| "secondary" \\| "destructive" \\| "outline" \\| "success" \\| "warning"` | `"default"` | Visual style |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Variants

| Variant | Use case |
|---------|----------|
| `default` | Primary / highlighted label |
| `secondary` | Low-emphasis label |
| `destructive` | Error or danger state |
| `outline` | Subtle bordered label |
| `success` | Positive / active state |
| `warning` | Caution state |

## Examples

```python
# Status indicators
Row(
    gap=2,
    children=[
        Badge(children=["200 OK"], variant="success"),
        Badge(children=["Deprecated"], variant="warning"),
        Badge(children=["Beta"]),
    ],
)

# With count
Badge(children=["12 new"], variant="secondary")
```
"""
