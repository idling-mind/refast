"""HoverCard — /docs/components/hover-card.

Interactive reference page for the HoverCard component family.
"""

from refast import Context
from refast.components import (
    Avatar,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    HoverCard,
    HoverCardContent,
    HoverCardTrigger,
    Link,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "HoverCard"
PAGE_ROUTE = "/docs/components/hover-card"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_side(ctx: Context, value: str):
    ctx.state.set("hvc_side", value)
    await ctx.refresh()


async def _set_align(ctx: Context, value: str):
    ctx.state.set("hvc_align", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    side = ctx.state.get("hvc_side", "bottom")
    align = ctx.state.get("hvc_align", "center")

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Side", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "top", "label": "top"},
                            {"value": "right", "label": "right"},
                            {"value": "bottom", "label": "bottom"},
                            {"value": "left", "label": "left"},
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
                            {"value": "start", "label": "start"},
                            {"value": "center", "label": "center"},
                            {"value": "end", "label": "end"},
                        ],
                        value=align,
                        on_change=ctx.callback(_set_align),
                    ),
                ],
            ),
        ],
        preview=[
            Text(
                "Hover over the link below to see the card appear.",
                class_name="text-sm text-muted-foreground mb-4",
            ),
            HoverCard(
                side=side,
                align=align,
                children=[
                    HoverCardTrigger(
                        children=[Link("@refast_framework", href="#")]
                    ),
                    HoverCardContent(
                        side=side,
                        align=align,
                        children=[
                            Row(
                                gap=3,
                                children=[
                                    Avatar(
                                        fallback="RF",
                                        size="md",
                                    ),
                                    Column(
                                        gap=1,
                                        children=[
                                            Text(
                                                "@refast_framework",
                                                class_name="font-semibold text-sm",
                                            ),
                                            Text(
                                                "Python + React framework for reactive web apps.",
                                                class_name="text-xs text-muted-foreground",
                                            ),
                                            Text(
                                                "Joined April 2026",
                                                class_name="text-xs text-muted-foreground",
                                            ),
                                        ],
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
                "```python\n"
                "HoverCard(\n"
                f'    side="{side}",\n'
                f'    align="{align}",\n'
                "    children=[\n"
                "        HoverCardTrigger(\n"
                '            children=[Link("@refast_framework", href="#")]\n'
                "        ),\n"
                "        HoverCardContent(\n"
                "            children=[\n"
                "                Row(gap=3, children=[\n"
                '                    Avatar(fallback="RF", size="md"),\n'
                "                    Column(gap=1, children=[\n"
                '                        Text("@refast_framework"),\n'
                '                        Text("Python + React framework."),\n'
                "                    ]),\n"
                "                ])\n"
                "            ]\n"
                "        ),\n"
                "    ],\n"
                ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-8 flex items-center justify-center bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the HoverCard component reference page."""
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
For sighted users to preview content behind a link. A card appears when
the user hovers over the trigger element.

```python
from refast.components import HoverCard, HoverCardTrigger, HoverCardContent, Link

HoverCard(
    children=[
        HoverCardTrigger(children=[Link("@shadcn", href="#")]),
        HoverCardContent(
            children=[
                Avatar(fallback="SC"),
                Text("@shadcn — UI component library"),
            ]
        ),
    ]
)
```
"""

REFERENCE = """
## HoverCard Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | A `HoverCardTrigger` and a `HoverCardContent`. |
| `open` | `bool \\| None` | `None` | Controlled open state. |
| `default_open` | `bool` | `False` | Initial open state (uncontrolled). |
| `on_open_change` | `Callback \\| None` | `None` | Fired when the open state changes. |
| `open_delay` | `int` | `700` | Milliseconds before the card opens on hover. |
| `close_delay` | `int` | `300` | Milliseconds before the card closes on mouse-leave. |
| `side` | `"top" \\| "right" \\| "bottom" \\| "left"` | `"bottom"` | Preferred side of the trigger. |
| `align` | `"start" \\| "center" \\| "end"` | `"center"` | Alignment relative to the trigger. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## HoverCardTrigger Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | The element that triggers the hover card (typically a `Link`). |
| `as_child` | `bool` | `False` | Merge props onto the child element. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## HoverCardContent Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Card content shown on hover. |
| `side` | `"top" \\| "right" \\| "bottom" \\| "left"` | `"bottom"` | Preferred placement. |
| `side_offset` | `int` | `4` | Pixel gap from the trigger. |
| `align` | `"start" \\| "center" \\| "end"` | `"center"` | Alignment relative to the trigger. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## User profile preview example

```python
HoverCard(
    children=[
        HoverCardTrigger(children=[Link("Alice Johnson", href="/users/alice")]),
        HoverCardContent(
            children=[
                Row(gap=3, children=[
                    Avatar(src="/avatars/alice.jpg", alt="Alice", size="lg"),
                    Column(gap=1, children=[
                        Text("Alice Johnson", class_name="font-semibold"),
                        Text("alice@example.com", class_name="text-sm text-muted-foreground"),
                        Badge(children=["Admin"]),
                    ]),
                ]),
            ]
        ),
    ]
)
```
"""
