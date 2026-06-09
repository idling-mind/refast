"""BlockQuote — /docs/components/blockquote."""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    BlockQuote,
    Column,
    Container,
    Heading,
    Input,
    Markdown,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "BlockQuote"
PAGE_ROUTE = "/docs/components/blockquote"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_color(ctx: Context, value: str):
    ctx.state.set("bq_color", value)
    await ctx.refresh()


async def _set_icon(ctx: Context, value: str):
    ctx.state.set("bq_icon", value)
    await ctx.refresh()


async def _set_cite(ctx: Context, value: str):
    ctx.state.set("bq_cite", value)
    await ctx.refresh()


async def _set_text(ctx: Context, value: str):
    ctx.state.set("bq_text", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────

_COLORS = ["default", "secondary", "destructive", "info", "success", "warning"]
_ICONS = ["(none)", "quote", "info", "flame", "zap", "check-circle", "alert-triangle", "x-circle", "star"]


def _playground(ctx: Context):
    color = ctx.state.get("bq_color", "default")
    raw_icon = ctx.state.get("bq_icon", "(none)")
    icon = None if raw_icon == "(none)" else raw_icon
    cite = ctx.state.get("bq_cite", "Author")
    text = ctx.state.get("bq_text", "Doth mother know you weareth her drapes?")

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("color", class_name="text-sm font-medium"),
                    Select(
                        options=[{"value": c, "label": c} for c in _COLORS],
                        value=color,
                        on_change=ctx.callback(_set_color),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("icon", class_name="text-sm font-medium"),
                    Select(
                        options=[{"value": i, "label": i} for i in _ICONS],
                        value=raw_icon,
                        on_change=ctx.callback(_set_icon),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("cite", class_name="text-sm font-medium"),
                    Input(
                        value=cite,
                        placeholder="Author...",
                        on_change=ctx.callback(_set_cite),
                        debounce=300,
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("children (quote text)", class_name="text-sm font-medium"),
                    Input(
                        value=text,
                        placeholder="Quote text...",
                        on_change=ctx.callback(_set_text),
                        debounce=300,
                    ),
                ],
            ),
        ],
        preview=[
            BlockQuote(
                text or "Quote text",
                cite=cite or None,
                color=color,
                icon=icon,
            ),
        ],
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
Styled quotation block with an optional icon, named or arbitrary color, and
muted attribution footer.

```python
from refast.components import BlockQuote

# Minimal
BlockQuote("To be or not to be.", cite="Hamlet")

# With icon and color
BlockQuote(
    "With great power comes great responsibility.",
    cite="Uncle Ben",
    color="success",
    icon="check-circle",
)

# Custom CSS color
BlockQuote(
    "Any sufficiently advanced technology is indistinguishable from magic.",
    cite="Arthur C. Clarke",
    color="oklch(70% 0.15 280)",
    icon="zap",
    icon_size=24,
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `str \\| Component \\| list \\| None` | `None` | The quote body — accepts a string, a single component, or a list |
| `cite` | `str \\| None` | `None` | Attribution text shown below the quote (e.g. author name) |
| `color` | `str` | `"default"` | Named variant **or** any CSS color (see below) |
| `icon` | `str \\| None` | `None` | Lucide icon name displayed above the quote body |
| `icon_size` | `int` | `20` | Icon size in pixels |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |
| `style` | `dict \\| None` | `None` | Inline CSS overrides |

## Color Variants

Pass one of the built-in named variants to use theme-aware Tailwind classes for the
border and background:

| Variant | Border token | Background token |
|---------|--------------|------------------|
| `"default"` | `border-border` | `bg-muted/50` |
| `"secondary"` | `border-secondary` | `bg-secondary/20` |
| `"destructive"` | `border-destructive` | `bg-destructive/10` |
| `"info"` | `border-info` | `bg-info/10` |
| `"success"` | `border-success` | `bg-success/10` |
| `"warning"` | `border-warning` | `bg-warning/10` |

Any other string is treated as a **raw CSS color** applied via inline styles, with a
12 % opacity tint as the background:

```python
BlockQuote("Quote", color="#7c3aed")          # hex
BlockQuote("Quote", color="oklch(70% 0.2 240)")   # oklch
BlockQuote("Quote", color="rgb(100, 200, 50)")    # rgb
```

## Icon

Pass any name from the `Icon` component's supported Lucide icon set:

```python
BlockQuote("All good!", color="success", icon="check-circle")
BlockQuote("Warning!", color="warning", icon="alert-triangle")
BlockQuote("Error",    color="destructive", icon="x-circle")
BlockQuote("Info",     color="info",  icon="info")
```

## Children

`children` accepts the same types as other Refast container components:

```python
# Plain string
BlockQuote("Simple text quote.")

# Component child
BlockQuote(Paragraph("Rich paragraph content."), cite="Author")

# List of children
BlockQuote(
    ["First part of the quote. ", Text("Highlighted part.", class_name="font-bold")],
    cite="Mixed children example",
)
```
"""
