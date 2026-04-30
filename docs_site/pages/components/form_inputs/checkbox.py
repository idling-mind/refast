"""Checkbox — /docs/components/checkbox."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    CheckboxGroup,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Checkbox"
PAGE_ROUTE = "/docs/components/checkbox"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_checked(ctx: Context, value: bool):
    ctx.state.set("chk_checked", value)
    await ctx.refresh()


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("chk_disabled", value)
    await ctx.refresh()


async def _set_error(ctx: Context, value: bool):
    ctx.state.set("chk_error", value)
    await ctx.refresh()


async def _set_orientation(ctx: Context, value: str):
    ctx.state.set("chk_orientation", value)
    await ctx.refresh()


async def _set_group_value(ctx: Context, value: list):
    ctx.state.set("chk_group_value", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    checked = ctx.state.get("chk_checked", False)
    disabled = ctx.state.get("chk_disabled", False)
    show_error = ctx.state.get("chk_error", False)
    orientation = ctx.state.get("chk_orientation", "vertical")
    group_value = ctx.state.get("chk_group_value", ["apple"])

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    # Single Checkbox
                    Text("Single Checkbox", class_name="text-base font-semibold mb-3"),
                    Row(
                        gap=4,
                        wrap=True,
                        class_name="mb-4",
                        children=[
                            Column(
                                gap=1,
                                children=[
                                    Text("checked", class_name="text-sm font-medium"),
                                    Checkbox(
                                        label="toggle checked",
                                        checked=checked,
                                        on_change=ctx.callback(_set_checked),
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
                                    Text("error", class_name="text-sm font-medium"),
                                    Checkbox(
                                        label="show error",
                                        checked=show_error,
                                        on_change=ctx.callback(_set_error),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        class_name="border rounded-lg p-6 bg-muted/30 mb-6",
                        children=[
                            Checkbox(
                                name="agree",
                                value="yes",
                                label="I agree to the terms of service",
                                description="You must accept to continue.",
                                checked=checked,
                                disabled=disabled,
                                error="You must accept the terms." if show_error else None,
                                on_change=ctx.callback(_set_checked),
                            )
                        ],
                    ),
                    Markdown(
                        content=(
                            f"```python\n"
                            f"Checkbox(\n"
                            f'    name="agree",\n'
                            f'    value="yes",\n'
                            f'    label="I agree to the terms of service",\n'
                            f"    checked={checked},\n"
                            f"    disabled={disabled},\n"
                            f'    error={"None" if not show_error else repr("You must accept the terms.")},\n'
                            f"    on_change=ctx.callback(handle_toggle),\n"
                            f")\n"
                            f"```"
                        )
                    ),
                    Separator(class_name="my-6"),
                    # CheckboxGroup
                    Text("CheckboxGroup", class_name="text-base font-semibold mb-3"),
                    Row(
                        gap=4,
                        wrap=True,
                        class_name="mb-4",
                        children=[
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
                        ],
                    ),
                    Container(
                        class_name="border rounded-lg p-6 bg-muted/30",
                        children=[
                            CheckboxGroup(
                                name="fruits",
                                label="Favourite Fruits",
                                description="Select all that apply.",
                                value=group_value,
                                orientation=orientation,
                                on_change=ctx.callback(_set_group_value),
                                children=[
                                    Checkbox(value="apple", label="Apple"),
                                    Checkbox(value="banana", label="Banana"),
                                    Checkbox(value="cherry", label="Cherry"),
                                    Checkbox(value="mango", label="Mango"),
                                ],
                            )
                        ],
                    ),
                    Markdown(
                        content=(
                            f"```python\n"
                            f"CheckboxGroup(\n"
                            f'    name="fruits",\n'
                            f'    label="Favourite Fruits",\n'
                            f'    value={group_value!r},\n'
                            f'    orientation="{orientation}",\n'
                            f"    on_change=ctx.callback(handle_change),\n"
                            f"    children=[\n"
                            f'        Checkbox(value="apple", label="Apple"),\n'
                            f'        Checkbox(value="banana", label="Banana"),\n'
                            f'        Checkbox(value="cherry", label="Cherry"),\n'
                            f"    ],\n"
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
    """Render the Checkbox component reference page."""
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
Single checkbox input and grouped multi-select checkboxes.

```python
from refast.components import Checkbox, CheckboxGroup

# Single checkbox
Checkbox(
    name="agree",
    value="yes",
    label="I agree to the terms of service",
    required=True,
    on_change=ctx.callback(handle_toggle),
)

# Grouped checkboxes
CheckboxGroup(
    name="interests",
    label="Your Interests",
    value=["python", "react"],
    orientation="vertical",
    on_change=ctx.callback(handle_change),
    children=[
        Checkbox(value="python", label="Python"),
        Checkbox(value="react", label="React"),
        Checkbox(value="rust", label="Rust"),
    ],
)
```
"""

REFERENCE = """
## Checkbox Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \\| None` | `None` | HTML name attribute |
| `value` | `str \\| None` | `None` | Value submitted when checked |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below the checkbox |
| `checked` | `bool` | `False` | Controlled checked state |
| `default_checked` | `bool` | `False` | Uncontrolled initial state |
| `required` | `bool` | `False` | Shows required asterisk |
| `disabled` | `bool` | `False` | Disables interaction |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired when checked state changes |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## CheckboxGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \\| None` | `None` | Group name for form submission |
| `children` | `list[Checkbox]` | `[]` | Checkbox items |
| `label` | `str \\| None` | `None` | Group label |
| `description` | `str \\| None` | `None` | Help text below label |
| `value` | `list[str]` | `[]` | Controlled list of selected values |
| `default_value` | `list[str] \\| None` | `None` | Uncontrolled initial values |
| `orientation` | `"vertical" \\| "horizontal"` | `"vertical"` | Layout orientation |
| `required` | `bool` | `False` | Shows required asterisk |
| `disabled` | `bool` | `False` | Disables all checkboxes in the group |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired with the new list of selected values |
| `class_name` | `str` | `""` | Extra Tailwind classes |
"""
