"""Radio — /docs/components/radio."""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Radio,
    RadioGroup,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Radio"
PAGE_ROUTE = "/docs/components/radio"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_value(ctx: Context, value: str):
    ctx.state.set("rad_value", value)
    await ctx.refresh()


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("rad_disabled", value)
    await ctx.refresh()


async def _set_orientation(ctx: Context, value: str):
    ctx.state.set("rad_orientation", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    value = ctx.state.get("rad_value", "medium")
    disabled = ctx.state.get("rad_disabled", False)
    orientation = ctx.state.get("rad_orientation", "vertical")

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("orientation", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "vertical", "label": "vertical"},
                            {"value": "horizontal", "label": "horizontal"},
                        ],
                        value=orientation,
                        on_change=ctx.callback(_set_orientation),
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
        ],
        preview=[
            RadioGroup(
                name="size",
                label="T-Shirt Size",
                description="Select your preferred size.",
                value=value,
                orientation=orientation,
                disabled=disabled,
                on_change=ctx.callback(_set_value),
                children=[
                    Radio(value="small", label="Small"),
                    Radio(value="medium", label="Medium"),
                    Radio(value="large", label="Large"),
                    Radio(value="xl", label="Extra Large"),
                ],
            )
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"RadioGroup(\n"
                f'    name="size",\n'
                f'    label="T-Shirt Size",\n'
                f'    value="{value}",\n'
                f'    orientation="{orientation}",\n'
                f"    disabled={disabled},\n"
                f"    on_change=ctx.callback(handle_change),\n"
                f"    children=[\n"
                f'        Radio(value="small", label="Small"),\n'
                f'        Radio(value="medium", label="Medium"),\n'
                f'        Radio(value="large", label="Large"),\n'
                f"    ],\n"
                f")\n"
                f"```"
            )
        ),
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Radio component reference page."""
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
Single radio button and grouped radio selection components. Use `RadioGroup` to group
multiple `Radio` items for single-choice selection.

```python
from refast.components import Radio, RadioGroup

RadioGroup(
    name="plan",
    label="Billing Plan",
    value="pro",
    orientation="vertical",
    on_change=ctx.callback(handle_change),
    children=[
        Radio(value="free", label="Free"),
        Radio(value="pro", label="Pro"),
        Radio(value="enterprise", label="Enterprise", disabled=True),
    ],
)
```
"""

REFERENCE = """
## Radio Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str` | required | Value emitted when this radio is selected |
| `name` | `str \\| None` | `None` | HTML name attribute (shared within a group) |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below the radio |
| `checked` | `bool` | `False` | Controlled checked state |
| `default_checked` | `bool` | `False` | Uncontrolled initial state |
| `required` | `bool` | `False` | Shows required asterisk |
| `disabled` | `bool` | `False` | Disables this radio button |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired when this radio is selected |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## RadioGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \\| None` | `None` | Group name for form submission |
| `children` | `list[Radio]` | `[]` | Radio items |
| `label` | `str \\| None` | `None` | Group label |
| `description` | `str \\| None` | `None` | Help text below label |
| `value` | `str \\| None` | `None` | Controlled selected value |
| `default_value` | `str \\| None` | `None` | Uncontrolled initial value |
| `orientation` | `"vertical" \\| "horizontal"` | `"vertical"` | Layout orientation |
| `required` | `bool` | `False` | Shows required asterisk |
| `disabled` | `bool` | `False` | Disables all radios in the group |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired with the newly selected value |
| `class_name` | `str` | `""` | Extra Tailwind classes |
"""
