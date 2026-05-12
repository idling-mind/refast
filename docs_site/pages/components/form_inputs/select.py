"""Select — /docs/components/select."""

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
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Select"
PAGE_ROUTE = "/docs/components/select"

_FRUIT_OPTIONS = [
    {"value": "apple", "label": "Apple"},
    {"value": "banana", "label": "Banana"},
    {"value": "cherry", "label": "Cherry"},
    {"value": "grape", "label": "Grape"},
    {"value": "mango", "label": "Mango"},
    {"value": "orange", "label": "Orange"},
    {"value": "strawberry", "label": "Strawberry"},
]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("sel_disabled", value)
    await ctx.refresh()


async def _set_required(ctx: Context, value: bool):
    ctx.state.set("sel_required", value)
    await ctx.refresh()


async def _set_placeholder(ctx: Context, value: bool):
    ctx.state.set("sel_placeholder", value)
    await ctx.refresh()


async def _set_error(ctx: Context, value: bool):
    ctx.state.set("sel_error", value)
    await ctx.refresh()


async def _on_select(ctx: Context, value: str):
    ctx.state.set("sel_value", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    disabled = ctx.state.get("sel_disabled", False)
    required = ctx.state.get("sel_required", False)
    show_placeholder = ctx.state.get("sel_placeholder", True)
    show_error = ctx.state.get("sel_error", False)
    selected = ctx.state.get("sel_value", None)

    placeholder = "Choose a fruit…" if show_placeholder else ""

    return playground_card(
        options=[
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
                    Text("placeholder", class_name="text-sm font-medium"),
                    Checkbox(
                        label="show placeholder",
                        checked=show_placeholder,
                        on_change=ctx.callback(_set_placeholder),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("error", class_name="text-sm font-medium"),
                    Checkbox(
                        label="show error",
                        checked=show_error,
                        on_change=ctx.callback(_set_error),
                    ),
                ],
            ),
        ],
        preview=[
            Select(
                name="fruit",
                label="Favourite Fruit",
                description="Pick your favourite fruit from the list.",
                options=_FRUIT_OPTIONS,
                value=selected,
                placeholder=placeholder,
                disabled=disabled,
                required=required,
                error="Please select an option." if show_error else None,
                on_change=ctx.callback(_on_select),
            )
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Select(\n"
                f'    name="fruit",\n'
                f'    label="Favourite Fruit",\n'
                f"    options=[\n"
                f'        {{"value": "apple", "label": "Apple"}},\n'
                f"        ...\n"
                f"    ],\n"
                f'    placeholder="{placeholder}",\n'
                f"    disabled={disabled},\n"
                f"    required={required},\n"
                f'    error={"None" if not show_error else repr("Please select an option.")},\n'
                f"    on_change=ctx.callback(handle_change),\n"
                f")\n"
                f"```"
            )
        ),
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Select component reference page."""
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
A native dropdown select component. Options are plain dicts with `value` and `label` keys.
Add `"disabled": True` to an option to make it unselectable.

```python
from refast.components import Select

Select(
    name="country",
    label="Country",
    description="Select your country of residence.",
    options=[
        {"value": "us", "label": "United States"},
        {"value": "gb", "label": "United Kingdom"},
        {"value": "de", "label": "Germany", "disabled": True},
    ],
    placeholder="Choose a country…",
    required=True,
    on_change=ctx.callback(handle_change),
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | `list[dict]` | required | List of `{"value": str, "label": str}` dicts. Add `"disabled": True` to disable an option |
| `name` | `str \\| None` | `None` | HTML name attribute |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below label |
| `value` | `str \\| None` | `None` | Controlled selected value |
| `default_value` | `str \\| None` | `None` | Uncontrolled initial value |
| `placeholder` | `str` | `"Select..."` | Placeholder option shown when nothing is selected |
| `required` | `bool` | `False` | Shows required asterisk |
| `disabled` | `bool` | `False` | Disables the select |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired when the selection changes |
| `class_name` | `str` | `""` | Extra Tailwind classes |
"""
