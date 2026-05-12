"""DatePicker — /docs/components/date-picker."""

from refast import Context
from refast.components import (
    Alert,
    Badge,
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
from refast.components.shadcn.controls import DatePicker
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "DatePicker"
PAGE_ROUTE = "/docs/components/date-picker"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("dp_disabled", value)
    await ctx.refresh()


async def _set_required(ctx: Context, value: bool):
    ctx.state.set("dp_required", value)
    await ctx.refresh()

async def _set_caption_layout(ctx: Context, value: str):
    ctx.state.set("dp_caption_layout", value)
    await ctx.refresh()

async def _set_mode(ctx: Context, value: str):
    ctx.state.set("dp_mode", value)
    ctx.state.set("dp_value", None)
    await ctx.refresh()


async def _on_change(ctx: Context):
    value = ctx.event_data.get("value", None)
    ctx.state.set("dp_value", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    disabled = ctx.state.get("dp_disabled", False)
    required = ctx.state.get("dp_required", False)
    mode = ctx.state.get("dp_mode", "single")
    selected = ctx.state.get("dp_value", None)
    caption_layout = ctx.state.get("dp_caption_layout", "dropdown")

    placeholder = "Pick a date range\u2026" if mode == "range" else "Pick a date\u2026"

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Mode", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "single", "label": "single"},
                            {"value": "range", "label": "range"},
                        ],
                        value=mode,
                        on_change=ctx.callback(_set_mode),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("disabled", class_name="text-sm font-medium"),
                    Checkbox(
                        label="disabled",
                        checked=disabled,
                        on_change=ctx.callback(_set_disabled),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("required", class_name="text-sm font-medium"),
                    Checkbox(
                        label="required",
                        checked=required,
                        on_change=ctx.callback(_set_required),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("caption layout", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "dropdown", "label": "dropdown"},
                            {"value": "inline", "label": "inline"},
                        ],
                        value=caption_layout,
                        on_change=ctx.callback(_set_caption_layout),
                    ),
                ],
            ),
        ],
        preview=[
            DatePicker(
                label="Date",
                description="Select a date.",
                value=selected,
                mode=mode,
                placeholder=placeholder,
                disabled=disabled,
                required=required,
                on_change=ctx.callback(_on_change),
                caption_layout=caption_layout,
            ),
            Text(
                f"Selected value: {selected}",
                class_name="text-sm text-muted-foreground mt-2",
            ),
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"DatePicker(\n"
                f'    label="Date",\n'
                f'    mode="{mode}",\n'
                f"    disabled={disabled},\n"
                f"    required={required},\n"
                f"    caption_layout='{caption_layout}',\n"

                f"    required={required},\n"
                f"    on_change=ctx.callback(handle_change),\n"
                f")\n"
                f"```"
            )
        ),
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the DatePicker component reference page."""
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
A button trigger that opens a calendar popover for date selection.
Supports single, multiple, and range date selection.

```python
from refast.components.shadcn.controls import DatePicker

DatePicker(
    label="Appointment date",
    placeholder="Pick a date",
    on_change=ctx.callback(handle_date_change),
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `date \\| list[date] \\| dict \\| None` | `None` | Controlled selected value |
| `mode` | `"single" \\| "multiple" \\| "range"` | `"single"` | Selection mode |
| `placeholder` | `str` | `"Pick a date"` | Button text when no date selected |
| `disabled` | `bool` | `False` | Disables interaction |
| `format` | `str` | `"PPP"` | date-fns format string |
| `caption_layout` | `"label" \\| "dropdown" \\| ...` | `"label"` | Calendar header style |
| `min_date` | `date \\| str \\| None` | `None` | Earliest selectable date |
| `max_date` | `date \\| str \\| None` | `None` | Latest selectable date |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text |
| `required` | `bool` | `False` | Shows required asterisk |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired when selection changes |

## Range Mode

```python
DatePicker(
    mode="range",
    placeholder="Select date range",
    on_change=ctx.callback(handle_range),
)
```
"""
