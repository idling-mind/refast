"""Heading — /docs/components/heading."""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Column,
    Container,
    Heading,
    Input,
    Markdown,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Heading"
PAGE_ROUTE = "/docs/components/heading"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_level(ctx: Context, value: str):
    ctx.state.set("hd_level", value)
    await ctx.refresh()


async def _set_text(ctx: Context, value: str):
    ctx.state.set("hd_text", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    level = int(ctx.state.get("hd_level", "1"))
    text = ctx.state.get("hd_text", "The quick brown fox")

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("level", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": str(n), "label": f"h{n}"}
                            for n in range(1, 7)
                        ],
                        value=str(level),
                        on_change=ctx.callback(_set_level),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("text", class_name="text-sm font-medium"),
                    Input(
                        value=text,
                        placeholder="Heading text...",
                        on_change=ctx.callback(_set_text),
                        debounce=300,
                    ),
                ],
            ),
        ],
        preview=[Heading(text or "Heading text", level=level)],
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
HTML heading elements `<h1>` through `<h6>` with consistent typography styles.

```python
from refast.components import Heading

Heading("Page Title", level=1)
Heading("Section", level=2, class_name="text-blue-600")
Heading("Sub-section", level=3)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | *(required)* | Heading content |
| `level` | `1 \\| 2 \\| 3 \\| 4 \\| 5 \\| 6` | `1` | HTML heading level (`h1`–`h6`) |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |
| `style` | `dict \\| None` | `None` | Inline CSS overrides |

## All Levels

| Level | Tag | Default Style |
|-------|-----|---------------|
| `1` | `<h1>` | `text-4xl font-extrabold` |
| `2` | `<h2>` | `text-3xl font-semibold` |
| `3` | `<h3>` | `text-2xl font-semibold` |
| `4` | `<h4>` | `text-xl font-semibold` |
| `5` | `<h5>` | `text-lg font-medium` |
| `6` | `<h6>` | `text-base font-medium` |

## Examples

```python
Column(
    gap=2,
    children=[
        Heading("Dashboard", level=1),
        Heading("Recent Activity", level=2),
        Heading("Today", level=3, class_name="text-muted-foreground"),
    ],
)
```
"""
