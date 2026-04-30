"""DatePicker — /docs/components/date-picker."""

from refast import Context
from refast.components import (
    Alert,
    Badge,
    Container,
    Heading,
    Markdown,
    Separator,
)

PAGE_TITLE = "DatePicker"
PAGE_ROUTE = "/docs/components/date-picker"


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the DatePicker component reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Badge("Not Yet Implemented", variant="secondary", class_name="mb-4"),
            Alert(
                title="Coming Soon",
                description=(
                    "The DatePicker component is planned but not yet implemented. "
                    "It will provide a calendar popup for selecting single dates or "
                    "date ranges, with support for min/max constraints and custom formatting."
                ),
                variant="default",
            ),
            Markdown(content=PLANNED),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Content ───────────────────────────────────────────────────────────────

PLANNED = """
## Planned API

Once implemented, `DatePicker` will provide a calendar popup bound to a text input:

```python
from refast.components.shadcn.input import DatePicker  # not yet available

DatePicker(
    name="appointment",
    label="Appointment Date",
    description="Select a date for your appointment.",
    value="2026-05-15",          # ISO 8601 string
    min_date="2026-01-01",
    max_date="2026-12-31",
    disabled=False,
    placeholder="Pick a date…",
    on_change=ctx.callback(handle_date_change),
)
```

## Planned Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \\| None` | `None` | HTML name attribute |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below label |
| `value` | `str \\| None` | `None` | Controlled value (ISO 8601 date string) |
| `placeholder` | `str` | `"Pick a date…"` | Placeholder text |
| `min_date` | `str \\| None` | `None` | Earliest selectable date (ISO 8601) |
| `max_date` | `str \\| None` | `None` | Latest selectable date (ISO 8601) |
| `disabled` | `bool` | `False` | Disables interaction |
| `required` | `bool` | `False` | Shows required asterisk |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired with the new ISO date string |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Workaround

Until `DatePicker` is available, use a plain `Input` with `type="date"`:

```python
from refast.components import Input

Input(
    name="appointment",
    label="Appointment Date",
    type="date",
    on_change=ctx.callback(handle_date_change),
)
```
"""
