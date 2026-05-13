"""Avatar — /docs/components/avatar.

Interactive reference page for the Avatar component.
"""

from refast import Context
from refast.components import (
    Avatar,
    Card,
    CardContent,
    CardHeader,
    Checkbox,
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
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Avatar"
PAGE_ROUTE = "/docs/components/avatar"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_size(ctx: Context, value: str):
    ctx.state.set("avt_size", value)
    await ctx.refresh()


async def _set_show_image(ctx: Context, value: bool):
    ctx.state.set("avt_show_image", value)
    await ctx.refresh()


async def _set_fallback(ctx: Context, value: str):
    ctx.state.set("avt_fallback", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    size = ctx.state.get("avt_size", "md")
    show_image = ctx.state.get("avt_show_image", True)
    fallback = ctx.state.get("avt_fallback", "JD")

    src = (
        "https://api.dicebear.com/7.x/avataaars/svg?seed=john"
        if show_image
        else None
    )

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Size", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "sm", "label": "sm (32px)"},
                            {"value": "md", "label": "md (40px)"},
                            {"value": "lg", "label": "lg (48px)"},
                        ],
                        value=size,
                        on_change=ctx.callback(_set_size),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Show image", class_name="text-sm font-medium"),
                    Checkbox(
                        label="use image src",
                        checked=show_image,
                        on_change=ctx.callback(_set_show_image),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Fallback text", class_name="text-sm font-medium"),
                    Input(
                        value=fallback,
                        placeholder="JD",
                        on_change=ctx.callback(_set_fallback),
                    ),
                ],
            ),
        ],
        preview=[
            Avatar(
                src=src,
                alt="John Doe",
                fallback=fallback or "JD",
                size=size,
            )
        ],
        code=Markdown(
            content=(
                "```python\n"
                "Avatar(\n"
                + (f'    src="{src}",\n' if src else "    # no src — shows fallback\n")
                + '    alt="John Doe",\n'
                + f'    fallback="{fallback or "JD"}",\n'
                + f'    size="{size}",\n'
                + ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-6 flex items-center justify-center gap-4 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Avatar component reference page."""
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
Circular user image with an initials fallback. When the image is absent or
fails to load, the `fallback` string is shown instead.

```python
from refast.components import Avatar

# Image avatar
Avatar(src="/avatars/alice.jpg", alt="Alice", size="md")

# Initials-only avatar
Avatar(fallback="JD", size="lg")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `src` | `str \\| None` | `None` | URL of the user image. Omit to show initials only. |
| `alt` | `str` | `""` | Alternative text; also used to derive the fallback initial when `fallback` is not supplied. |
| `fallback` | `str \\| None` | `None` | Short string (one or two letters) shown when the image is unavailable. |
| `size` | `"sm" \\| "md" \\| "lg"` | `"md"` | Avatar diameter: `"sm"` = 32px, `"md"` = 40px, `"lg"` = 48px. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## All sizes

```python
Row(gap=4, children=[
    Avatar(fallback="SM", size="sm"),
    Avatar(fallback="MD", size="md"),
    Avatar(fallback="LG", size="lg"),
])
```

## With image

```python
Avatar(src="/avatars/alice.jpg", alt="Alice Johnson", size="lg")
```

## Initials fallback

```python
# Fallback derived from alt text
Avatar(alt="John Doe", size="md")       # shows "J"

# Explicit fallback string
Avatar(fallback="JD", size="md")        # shows "JD"
```

## In a user profile card

```python
Row(
    align="center",
    gap=3,
    children=[
        Avatar(src="/avatars/alice.jpg", alt="Alice", size="lg"),
        Column(gap=0, children=[
            Text("Alice Johnson", class_name="font-semibold"),
            Text("alice@example.com", class_name="text-sm text-muted-foreground"),
        ]),
    ],
)
```
"""
