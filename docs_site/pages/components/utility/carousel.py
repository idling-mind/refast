"""Carousel — /docs/components/carousel."""
from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Carousel"
PAGE_ROUTE = "/docs/components/carousel"

_SLIDES = [
    ("Slide 1", "from-blue-400 to-blue-600", "🌊"),
    ("Slide 2", "from-purple-400 to-purple-600", "🔮"),
    ("Slide 3", "from-green-400 to-green-600", "🌿"),
    ("Slide 4", "from-orange-400 to-orange-600", "🔥"),
    ("Slide 5", "from-pink-400 to-pink-600", "🌸"),
]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_orientation(ctx: Context, value: str):
    ctx.state.set("car_orientation", value)
    await ctx.refresh()


async def _set_loop(ctx: Context, value: bool):
    ctx.state.set("car_loop", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    orientation = ctx.state.get("car_orientation", "horizontal")
    loop = ctx.state.get("car_loop", False)

    items = [
        CarouselItem(
            children=[
                Container(
                    class_name=f"rounded-lg bg-gradient-to-br {gradient} flex flex-col items-center justify-center gap-2",
                    children=[
                        Text(emoji, class_name="text-4xl"),
                        Text(label, class_name="text-white font-semibold"),
                    ],
                )
            ]
        )
        for label, gradient, emoji in _SLIDES
    ]

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Orientation", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["horizontal", "vertical"]
                        ],
                        value=orientation,
                        on_change=ctx.callback(_set_orientation),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Loop", class_name="text-sm font-medium"),
                    Checkbox(
                        label="loop continuously",
                        checked=loop,
                        on_change=ctx.callback(_set_loop),
                    ),
                ],
            ),
        ],
        preview=[
            Carousel(
                orientation=orientation,
                loop=loop,
                id=f"carousel-demo-{orientation}-{'loop' if loop else 'noloop'}",
                class_name="w-full max-w-lg mx-auto",
                children=[
                    CarouselContent(children=items),
                    CarouselPrevious(),
                    CarouselNext(),
                ],
                style={"height": "200px"},
            ),
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Carousel(\n"
                f'    orientation="{orientation}",\n'
                f"    loop={loop},\n"
                f"    children=[\n"
                f"        CarouselContent(\n"
                f"            children=[\n"
                f"                CarouselItem(children=[Card(title=\"Slide 1\", ...)]),\n"
                f"                CarouselItem(children=[Card(title=\"Slide 2\", ...)]),\n"
                f"                CarouselItem(children=[Card(title=\"Slide 3\", ...)]),\n"
                f"            ]\n"
                f"        ),\n"
                f"        CarouselPrevious(),\n"
                f"        CarouselNext(),\n"
                f"    ]\n"
                f")\n"
                f"```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Carousel component reference page."""
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
A touch-friendly, swipeable carousel powered by [Embla Carousel](https://www.embla-carousel.com/).
Supports horizontal and vertical orientations, looping, and custom slide content.

```python
from refast.components import (
    Carousel, CarouselContent, CarouselItem,
    CarouselPrevious, CarouselNext,
)
```
"""

REFERENCE = """
## Props

### `Carousel`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `"horizontal" \\| "vertical"` | `"horizontal"` | Scroll axis |
| `loop` | `bool` | `False` | Whether to wrap around continuously |
| `opts` | `dict \\| None` | `None` | Embla Carousel options (advanced) |
| `children` | `ChildrenType` | `None` | `CarouselContent` + navigation buttons |

### `CarouselItem`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ChildrenType` | `None` | Slide content |
| `class_name` | `str` | `""` | Extra Tailwind classes (e.g. `"basis-1/2"` for multi-visible) |

### `CarouselPrevious` / `CarouselNext`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `on_click` | `Callback \\| None` | `None` | Optional server callback when navigating |

## Component Hierarchy

```
Carousel
├── CarouselContent
│   ├── CarouselItem  ← slide 1
│   ├── CarouselItem  ← slide 2
│   └── CarouselItem  ← slide N
├── CarouselPrevious  ← prev button (outside CarouselContent)
└── CarouselNext      ← next button (outside CarouselContent)
```

## Multi-slide Visible

Use `class_name="basis-1/3"` on `CarouselItem` to show multiple slides
at once:

```python
Carousel(
    children=[
        CarouselContent(
            children=[
                CarouselItem(
                    class_name="basis-1/3",
                    children=[Card(title=f"Item {i}")]
                )
                for i in range(9)
            ]
        ),
        CarouselPrevious(),
        CarouselNext(),
    ]
)
```

## Vertical Carousel

```python
Carousel(
    orientation="vertical",
    class_name="h-64",
    children=[
        CarouselContent(class_name="h-full"),
        CarouselPrevious(),
        CarouselNext(),
    ]
)
```

## Advanced Options (Embla)

Pass any Embla Carousel option via `opts`:

```python
Carousel(
    opts={"align": "start", "skipSnaps": False},
    loop=True,
    children=[...]
)
```
"""
