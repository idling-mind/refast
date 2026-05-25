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


async def _set_icon(ctx: Context, value: str):
    ctx.state.set("bg_icon", value)
    await ctx.refresh()


async def _set_icon_position(ctx: Context, value: str):
    ctx.state.set("bg_icon_position", value)
    await ctx.refresh()


async def _set_size(ctx: Context, value: str):
    ctx.state.set("bg_size", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    variant = ctx.state.get("bg_variant", "default")
    badge_text = ctx.state.get("bg_text", "Badge")
    icon = ctx.state.get("bg_icon", "") or None
    icon_position = ctx.state.get("bg_icon_position", "left")
    size = ctx.state.get("bg_size", "md")

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
            Column(
                gap=1,
                children=[
                    Text("icon", class_name="text-sm font-medium"),
                    Input(
                        value=ctx.state.get("bg_icon", ""),
                        placeholder="e.g. check, star, alert-circle",
                        on_change=ctx.callback(_set_icon),
                        debounce=300,
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("icon_position", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "left", "label": "left"},
                            {"value": "right", "label": "right"},
                        ],
                        value=icon_position,
                        on_change=ctx.callback(_set_icon_position),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("size", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": s, "label": s}
                            for s in ["xs", "sm", "md", "lg", "xl"]
                        ],
                        value=size,
                        on_change=ctx.callback(_set_size),
                    ),
                ],
            ),
        ],
        preview=[
            Badge(
                children=[badge_text or "Badge"],
                variant=variant,
                icon=icon,
                icon_position=icon_position,
                size=size,
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

# With icons
Badge(children=["Verified"], icon="check-circle")
Badge(children=["Warning"], icon="alert-triangle", variant="warning")
Badge(children=["New"], icon="arrow-right", icon_position="right")

# Sizes
Badge(children=["Tiny"], size="xs")
Badge(children=["Small"], size="sm")
Badge(children=["Default"], size="md")
Badge(children=["Large"], size="lg")
Badge(children=["XLarge"], size="xl")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \\| Component \\| None` | `None` | Badge content (usually a short string) |
| `variant` | `"default" \\| "secondary" \\| "destructive" \\| "outline" \\| "success" \\| "warning"` | `"default"` | Visual style |
| `icon` | `str \\| None` | `None` | Lucide icon name (e.g. `"check"`, `"star"`, `"alert-circle"`) |
| `icon_position` | `"left" \\| "right"` | `"left"` | Position of the icon relative to badge text |
| `size` | `"xs" \\| "sm" \\| "md" \\| "lg" \\| "xl"` | `"md"` | Size of the badge |
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

## Sizes

| Size | Description |
|------|-------------|
| `xs` | Extra small — compact inline use |
| `sm` | Small |
| `md` | Default |
| `lg` | Large |
| `xl` | Extra large |

## Examples

```python
# Status indicators with icons
Row(
    gap=2,
    children=[
        Badge(children=["200 OK"], variant="success", icon="check"),
        Badge(children=["Deprecated"], variant="warning", icon="alert-triangle"),
        Badge(children=["Beta"]),
    ],
)

# Icon on the right
Badge(children=["Explore"], icon="arrow-right", icon_position="right")

# Size scale
Row(
    gap=2,
    class_name="items-center",
    children=[
        Badge(children=["xs"], size="xs"),
        Badge(children=["sm"], size="sm"),
        Badge(children=["md"], size="md"),
        Badge(children=["lg"], size="lg"),
        Badge(children=["xl"], size="xl"),
    ],
)

# With count
Badge(children=["12 new"], variant="secondary")
```
"""
