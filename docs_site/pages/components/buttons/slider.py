"""Slider — /docs/components/slider.

Interactive reference page for the Slider component.
"""
from turtle import st

from refast import Context
from refast.components import (
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
from refast.components.shadcn.controls import Slider
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Slider"
PAGE_ROUTE = "/docs/components/slider"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_value(ctx: Context, value: list):
    ctx.state.set("sl_value", value)
    await ctx.refresh()


async def _set_min(ctx: Context, value: str):
    try:
        ctx.state.set("sl_min", float(value))
    except (ValueError, TypeError):
        pass
    await ctx.refresh()


async def _set_max(ctx: Context, value: str):
    try:
        ctx.state.set("sl_max", float(value))
    except (ValueError, TypeError):
        pass
    await ctx.refresh()


async def _set_step(ctx: Context, value: str):
    try:
        ctx.state.set("sl_step", float(value))
    except (ValueError, TypeError):
        pass
    await ctx.refresh()


async def _set_orientation(ctx: Context, value: str):
    ctx.state.set("sl_orientation", value)
    await ctx.refresh()


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("sl_disabled", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    sl_min = ctx.state.get("sl_min", 0)
    sl_max = ctx.state.get("sl_max", 100)
    step = ctx.state.get("sl_step", 1)
    orientation = ctx.state.get("sl_orientation", "horizontal")
    disabled = ctx.state.get("sl_disabled", False)
    value = ctx.state.get("sl_value", [50])

    # Clamp value within range
    current = value[0] if value else sl_min

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Min", class_name="text-sm font-medium"),
                    Input(
                        value=str(int(sl_min) if sl_min == int(sl_min) else sl_min),
                        type="number",
                        on_change=ctx.callback(_set_min),
                        class_name="w-24",
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Max", class_name="text-sm font-medium"),
                    Input(
                        value=str(int(sl_max) if sl_max == int(sl_max) else sl_max),
                        type="number",
                        on_change=ctx.callback(_set_max),
                        class_name="w-24",
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Step", class_name="text-sm font-medium"),
                    Input(
                        value=str(int(step) if step == int(step) else step),
                        type="number",
                        on_change=ctx.callback(_set_step),
                        class_name="w-24",
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Orientation", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "horizontal", "label": "horizontal"},
                            {"value": "vertical", "label": "vertical"},
                        ],
                        value=orientation,
                        on_change=ctx.callback(_set_orientation),
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
        preview=[
            Container(
                style={"height": "200px"} if orientation == "vertical" else {},
                children=[
                    Slider(
                        value=value,
                        min=sl_min,
                        max=sl_max,
                        step=step,
                        orientation=orientation,
                        disabled=disabled,
                        show_value=True,
                        on_value_change=ctx.callback(_set_value),
                    ),
                ],
            ),
            Text(
                f"Current value: {current}",
                class_name="text-sm text-muted-foreground mb-2",
            ),
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Slider(\n"
                f"    value=[{current}],\n"
                f"    min={sl_min},\n"
                f"    max={sl_max},\n"
                f"    step={step},\n"
                f'    orientation="{orientation}",\n'
                f"    disabled={disabled},\n"
                f"    show_value=True,\n"
                f"    on_value_change=ctx.callback(handle_change),\n"
                f")\n"
                f"```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Slider component reference page."""
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
A draggable range slider for selecting a numeric value (or range).

```python
from refast.components.shadcn.controls import Slider

# Basic slider
Slider(value=[50], min=0, max=100, on_value_change=ctx.callback(handle_change))

# With label and description
Slider(
    label="Volume",
    description="Adjust the output volume",
    value=[volume],
    show_value=True,
    on_value_change=ctx.callback(handle_volume),
)

# Vertical slider
Slider(value=[50], orientation="vertical", class_name="h-40")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `list[float] \\| None` | `None` | Controlled value(s) — a list allows range sliders |
| `default_value` | `list[float] \\| None` | `[0]` | Initial value (uncontrolled) |
| `min` | `float` | `0` | Minimum value |
| `max` | `float` | `100` | Maximum value |
| `step` | `float` | `1` | Increment between values |
| `disabled` | `bool` | `False` | Prevents interaction |
| `orientation` | `"horizontal" \\| "vertical"` | `"horizontal"` | Slider direction |
| `label` | `str \\| None` | `None` | Visible label above the slider |
| `description` | `str \\| None` | `None` | Helper text below the slider |
| `show_value` | `bool` | `False` | Display current value next to thumb |
| `required` | `bool` | `False` | Marks the field as required |
| `error` | `str \\| None` | `None` | Validation error message |
| `on_value_change` | `Callback \\| None` | `None` | Called continuously while dragging |
| `on_value_commit` | `Callback \\| None` | `None` | Called once when the user releases the thumb |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Controlled Usage

```python
async def handle_volume(ctx: Context, value: list):
    ctx.state.set("volume", value[0])
    await ctx.refresh()

Slider(
    value=[ctx.state.get("volume", 50)],
    min=0,
    max=100,
    on_value_change=ctx.callback(handle_volume),
)
```

## on_value_change vs on_value_commit

```python
# on_value_change fires on every drag tick — good for live preview
Slider(value=[v], on_value_change=ctx.callback(handle_live))

# on_value_commit fires only when the thumb is released — good for expensive operations
Slider(value=[v], on_value_commit=ctx.callback(handle_commit))
```

## Range Slider

Pass two values to create a range slider with two thumbs:

```python
Slider(
    value=[20, 80],
    min=0,
    max=100,
    on_value_change=ctx.callback(handle_range),
)
```

## Vertical

```python
Slider(
    value=[50],
    orientation="vertical",
    class_name="h-40",
    on_value_change=ctx.callback(handle_change),
)
```
"""
