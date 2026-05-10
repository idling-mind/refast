"""IconButton — /docs/components/icon-button.

Interactive reference page for the IconButton component.
"""

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
    Row,
    Select,
    Separator,
    Text,
)
from refast.components.shadcn.button import IconButton

PAGE_TITLE = "IconButton"
PAGE_ROUTE = "/docs/components/icon-button"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_icon(ctx: Context, value: str):
    ctx.state.set("ib_icon", value)
    await ctx.refresh()


async def _set_variant(ctx: Context, value: str):
    ctx.state.set("ib_variant", value)
    await ctx.refresh()


async def _set_size(ctx: Context, value: str):
    ctx.state.set("ib_size", value)
    await ctx.refresh()


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("ib_disabled", value)
    await ctx.refresh()


async def _noop(ctx: Context):
    pass


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    icon = ctx.state.get("ib_icon", "settings")
    variant = ctx.state.get("ib_variant", "ghost")
    size = ctx.state.get("ib_size", "md")
    disabled = ctx.state.get("ib_disabled", False)

    icon_options = [
        "settings",
        "trash",
        "edit",
        "copy",
        "download",
        "upload",
        "search",
        "plus",
        "x",
        "check",
        "star",
        "heart",
        "bell",
        "mail",
    ]

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
                                    Text("Icon", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in icon_options
                                        ],
                                        value=icon,
                                        on_change=ctx.callback(_set_icon),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("Variant", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in [
                                                "ghost",
                                                "default",
                                                "secondary",
                                                "destructive",
                                                "outline",
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
                                    Text("Size", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in ["xs", "sm", "md", "lg", "xl"]
                                        ],
                                        value=size,
                                        on_change=ctx.callback(_set_size),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("Disabled", class_name="text-sm font-medium"),
                                    Checkbox(
                                        label="disabled",
                                        checked=disabled,
                                        on_change=ctx.callback(_set_disabled),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Preview area
                    Container(
                        class_name="border rounded-lg p-6 flex items-center justify-center min-h-[80px] bg-muted/30",
                        children=[
                            IconButton(
                                icon=icon,
                                variant=variant,
                                size=size,
                                disabled=disabled,
                                aria_label=icon,
                                on_click=ctx.callback(_noop),
                            )
                        ],
                    ),
                    # Live code snippet
                    Markdown(
                        content=(
                            f"```python\n"
                            f"IconButton(\n"
                            f'    icon="{icon}",\n'
                            f'    variant="{variant}",\n'
                            f'    size="{size}",\n'
                            f'    disabled={disabled},\n'
                            f'    aria_label="{icon}",\n'
                            f"    on_click=ctx.callback(handle_click),\n"
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
    """Render the IconButton component reference page."""
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
A square icon-only button. Useful for toolbars, action columns, and compact UIs where
a text label would take too much space.

```python
from refast.components.shadcn.button import IconButton

IconButton(icon="trash", aria_label="Delete item", on_click=ctx.callback(handle_delete))
IconButton(icon="settings", variant="outline", size="lg")
IconButton(icon="copy", variant="ghost")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `icon` | `str` | *(required)* | Lucide icon name (e.g. `"trash"`, `"edit"`, `"settings"`) |
| `variant` | `"ghost" \\| "default" \\| "secondary" \\| "destructive" \\| "outline"` | `"ghost"` | Visual style |
| `size` | `"xs" \\| "sm" \\| "md" \\| "lg" \\| "xl"` | `"md"` | Button dimensions (also controls icon size) |
| `disabled` | `bool` | `False` | Prevents interaction |
| `aria_label` | `str \\| None` | `None` | Accessible label — defaults to icon name if omitted |
| `on_click` | `Callback \\| None` | `None` | Server callback invoked on click |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## All Variants

```python
IconButton(icon="settings")                          # ghost (default)
IconButton(icon="settings", variant="default")
IconButton(icon="settings", variant="secondary")
IconButton(icon="settings", variant="destructive")
IconButton(icon="settings", variant="outline")
```

## All Sizes

```python
IconButton(icon="settings", size="xs")
IconButton(icon="settings", size="sm")
IconButton(icon="settings", size="md")
IconButton(icon="settings", size="lg")
IconButton(icon="settings", size="xl")
```

## With Accessible Label

```python
# Always provide aria_label for screen-reader accessibility
IconButton(icon="trash", aria_label="Delete item", on_click=ctx.callback(handle_delete))
```

## Common Use Cases

```python
# Toolbar actions
Row(children=[
    IconButton(icon="bold", aria_label="Bold"),
    IconButton(icon="italic", aria_label="Italic"),
    IconButton(icon="underline", aria_label="Underline"),
])

# Table row actions
Row(children=[
    IconButton(icon="edit", aria_label="Edit", on_click=ctx.callback(handle_edit)),
    IconButton(icon="trash", variant="destructive", aria_label="Delete",
               on_click=ctx.callback(handle_delete)),
])
```
"""
