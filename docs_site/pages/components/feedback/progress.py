"""Progress / Spinner / Skeleton — /docs/components/progress."""

from docs_site.pages.components.playground import playground_card
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
    Progress,
    Row,
    Select,
    Separator,
    Skeleton,
    Spinner,
    Text,
)

PAGE_TITLE = "Progress, Spinner & Skeleton"
PAGE_ROUTE = "/docs/components/progress"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_value(ctx: Context, value: str):
    ctx.state.set("prg_value", int(value))
    await ctx.refresh()


async def _set_indeterminate(ctx: Context, value: bool):
    ctx.state.set("prg_indeterminate", value)
    await ctx.refresh()


async def _set_show_value(ctx: Context, value: bool):
    ctx.state.set("prg_show_value", value)
    await ctx.refresh()


async def _set_striped(ctx: Context, value: str):
    ctx.state.set("prg_striped", value if value != "none" else None)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    value = ctx.state.get("prg_value", 40)
    indeterminate = ctx.state.get("prg_indeterminate", False)
    show_value = ctx.state.get("prg_show_value", False)
    striped = ctx.state.get("prg_striped", None)

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Value", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": str(v), "label": f"{v}%"}
                            for v in [0, 10, 25, 40, 60, 75, 90, 100]
                        ],
                        value=str(value),
                        on_change=ctx.callback(_set_value),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Striped", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "none", "label": "none"},
                            {"value": "static", "label": "static"},
                            {"value": "animated", "label": "animated"},
                        ],
                        value=striped or "none",
                        on_change=ctx.callback(_set_striped),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Show value", class_name="text-sm font-medium"),
                    Checkbox(
                        label="show_value",
                        checked=show_value,
                        on_change=ctx.callback(_set_show_value),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Indeterminate", class_name="text-sm font-medium"),
                    Checkbox(
                        label="indeterminate",
                        checked=indeterminate,
                        on_change=ctx.callback(_set_indeterminate),
                    ),
                ],
            ),
        ],
        preview=[
            Progress(
                value=None if indeterminate else value,
                show_value=show_value,
                striped=striped,
                label="Loading…" if indeterminate else None,
            ),
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Progress(\n"
                f"    value={None if indeterminate else value},\n"
                f"    show_value={show_value},\n"
                + (f'    striped="{striped}",\n' if striped else "")
                + ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
    )


def _spinner_section():
    return Card(
        class_name="mt-6",
        children=[
            CardHeader(title="Spinner"),
            CardContent(
                children=[
                    Text(
                        "Use Spinner to indicate an ongoing operation.",
                        class_name="text-sm text-muted-foreground mb-4",
                    ),
                    Row(
                        gap=6,
                        align="center",
                        class_name="border rounded-lg p-4 bg-muted/30",
                        children=[
                            Column(
                                gap=2,
                                align="center",
                                children=[
                                    Spinner(size="sm"),
                                    Text("sm", class_name="text-xs text-muted-foreground"),
                                ],
                            ),
                            Column(
                                gap=2,
                                align="center",
                                children=[
                                    Spinner(size="md"),
                                    Text("md", class_name="text-xs text-muted-foreground"),
                                ],
                            ),
                            Column(
                                gap=2,
                                align="center",
                                children=[
                                    Spinner(size="lg"),
                                    Text("lg", class_name="text-xs text-muted-foreground"),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        ]
    )


def _skeleton_section():
    return Card(
        class_name="mt-6",
        children=[
            CardHeader(title="Skeleton"),
            CardContent(
                children=[
                    Text(
                        "Use Skeleton placeholders while content is loading.",
                        class_name="text-sm text-muted-foreground mb-4",
                    ),
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30 space-y-3",
                        children=[
                            # Avatar + name row
                            Row(
                                gap=3,
                                align="center",
                                children=[
                                    Skeleton(width=40, height=40, circle=True),
                                    Column(
                                        gap=2,
                                        children=[
                                            Skeleton(width="60%", height=14),
                                            Skeleton(width="40%", height=12),
                                        ],
                                    ),
                                ],
                            ),
                            Skeleton(width="100%", height=14),
                            Skeleton(width="80%", height=14),
                            Skeleton(width="90%", height=14),
                        ],
                    ),
                ]
            ),
        ]
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Progress/Spinner/Skeleton reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _playground(ctx),
            _spinner_section(),
            _skeleton_section(),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Content ───────────────────────────────────────────────────────────────

INTRO = """
Three feedback primitives for communicating loading and progress states:
**Progress** (bar), **Spinner** (circular indicator), and **Skeleton** (content placeholder).

```python
from refast.components import Progress, Spinner, Skeleton
```
"""

REFERENCE = """
## Progress Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `int \\| None` | `0` | Current value (0–100). `None` = indeterminate |
| `max` | `int` | `100` | Maximum value |
| `label` | `str \\| None` | `None` | Accessible label |
| `show_value` | `bool` | `False` | Show `value%` text inside bar |
| `foreground_color` | `str \\| None` | `None` | Bar fill colour token |
| `striped` | `"static" \\| "animated" \\| None` | `None` | Striped pattern |

## Spinner Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `size` | `"sm" \\| "md" \\| "lg"` | `"md"` | Spinner size |

## Skeleton Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `width` | `str \\| int \\| None` | `None` | CSS width (e.g. `"60%"`, `200`) |
| `height` | `str \\| int \\| None` | `None` | CSS height |
| `variant` | `"text" \\| "circular" \\| "rectangular"` | `"text"` | Shape |
| `circle` | `bool` | `False` | Render as a circle (override) |

## Examples

```python
# Determinate progress
Progress(value=75, show_value=True)

# Indeterminate (animated)
Progress(value=None, label="Loading…")

# Animated striped
Progress(value=60, striped="animated", foreground_color="primary")

# Spinner while loading
Spinner(size="lg")

# Skeleton card placeholder
Column(gap=2, children=[
    Skeleton(width=200, height=20),
    Skeleton(width="100%", height=14),
    Skeleton(width="80%", height=14),
])
```
"""
