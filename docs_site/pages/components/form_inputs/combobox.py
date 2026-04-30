"""Combobox — /docs/components/combobox."""

from refast import Context
from refast.components import (
    Alert,
    Badge,
    Container,
    Heading,
    Markdown,
    Separator,
)

PAGE_TITLE = "Combobox"
PAGE_ROUTE = "/docs/components/combobox"


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Combobox component reference page."""
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
                    "The Combobox component is planned but not yet implemented. "
                    "It will provide a searchable dropdown with support for both "
                    "freeform text entry and selecting from a predefined list of options."
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

Once implemented, `Combobox` will provide a searchable dropdown that combines
free-text input with option selection:

```python
from refast.components.shadcn.input import Combobox  # not yet available

Combobox(
    name="framework",
    label="Framework",
    placeholder="Search frameworks…",
    options=[
        {"value": "react", "label": "React"},
        {"value": "vue", "label": "Vue"},
        {"value": "svelte", "label": "Svelte"},
    ],
    value=selected_value,
    disabled=False,
    on_change=ctx.callback(handle_change),
)
```

## Planned Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | `list[dict]` | required | List of `{"value": str, "label": str}` dicts |
| `name` | `str \\| None` | `None` | HTML name attribute |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below label |
| `value` | `str \\| None` | `None` | Controlled selected value |
| `placeholder` | `str` | `"Search…"` | Input placeholder text |
| `disabled` | `bool` | `False` | Disables interaction |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired when selection changes |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Use For

- Large option sets that benefit from search/filtering
- User-typed values that map to a canonical option
- Autocomplete-style inputs

## Use `Select` Instead When

- The option list is short (< 10 items)
- Free-text entry is not needed
"""
