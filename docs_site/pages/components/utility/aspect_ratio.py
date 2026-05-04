"""AspectRatio — /docs/components/aspect-ratio."""

from refast import Context
from refast.components import (
    AspectRatio,
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

PAGE_TITLE = "AspectRatio"
PAGE_ROUTE = "/docs/components/aspect-ratio"

_RATIO_OPTIONS = [
    {"value": "16/9", "label": "16:9 (Widescreen)"},
    {"value": "4/3", "label": "4:3 (Classic TV)"},
    {"value": "1/1", "label": "1:1 (Square)"},
    {"value": "3/2", "label": "3:2 (Photo)"},
    {"value": "21/9", "label": "21:9 (Ultra-wide)"},
]

_RATIO_VALUES = {
    "16/9": 16 / 9,
    "4/3": 4 / 3,
    "1/1": 1.0,
    "3/2": 3 / 2,
    "21/9": 21 / 9,
}


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_ratio(ctx: Context, value: str):
    ctx.state.set("ar_ratio", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    ratio_key = ctx.state.get("ar_ratio", "16/9")
    ratio_val = _RATIO_VALUES.get(ratio_key, 16 / 9)

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
                                    Text("Ratio", class_name="text-sm font-medium"),
                                    Select(
                                        options=_RATIO_OPTIONS,
                                        value=ratio_key,
                                        on_change=ctx.callback(_set_ratio),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        class_name="max-w-sm",
                        children=[
                            AspectRatio(
                                ratio=ratio_val,
                                children=[
                                    Container(
                                        class_name="w-full h-full rounded-lg bg-muted border-2 border-border flex items-center justify-center",
                                        children=[
                                            Text(
                                                ratio_key.replace("/", " : "),
                                                class_name="text-lg font-bold text-primary",
                                            )
                                        ],
                                    )
                                ],
                            )
                        ],
                    ),
                    Markdown(
                        content=(
                            f"```python\n"
                            f"AspectRatio(\n"
                            f"    ratio={ratio_key},\n"
                            f"    children=[\n"
                            f"        Image(src=\"photo.jpg\", alt=\"Photo\", class_name=\"w-full h-full object-cover rounded-lg\"),\n"
                            f"    ]\n"
                            f")\n"
                            f"```"
                        )
                    ),
                ]
            ),
        ]
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the AspectRatio component reference page."""
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
Constrains its child to a fixed width-to-height ratio.
The child expands to fill the container while maintaining the ratio.

```python
from refast.components import AspectRatio

AspectRatio(ratio=16/9, children=[Image(src="...", alt="...")])
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `ratio` | `float` | `1.0` | Width ÷ height ratio, e.g. `16/9`, `4/3`, `1.0` |
| `children` | `ChildrenType` | `None` | Content to constrain (typically an `Image`) |
| `class_name` | `str` | `""` | Extra Tailwind classes on the wrapper |

## Common Ratios

| Ratio | Float | Use case |
|-------|-------|----------|
| `16/9` | `1.777…` | Video thumbnails, hero images |
| `4/3` | `1.333…` | Classic TV, legacy photos |
| `1/1` | `1.0` | Profile pictures, tiles |
| `3/2` | `1.5` | DSLR photos |
| `21/9` | `2.333…` | Cinematic banner images |

## With an Image

```python
AspectRatio(
    ratio=16/9,
    class_name="rounded-lg overflow-hidden",
    children=[
        Image(
            src="https://example.com/photo.jpg",
            alt="Landscape photo",
            class_name="w-full h-full object-cover",
        )
    ]
)
```

## With a Video Embed

```python
AspectRatio(
    ratio=16/9,
    children=[
        Container(
            extra_props={"as": "iframe", "src": "https://www.youtube.com/embed/..."},
            class_name="w-full h-full",
        )
    ]
)
```
"""
