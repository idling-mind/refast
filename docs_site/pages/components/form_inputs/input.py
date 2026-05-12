"""Input — /docs/components/input."""

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
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Input"
PAGE_ROUTE = "/docs/components/input"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_type(ctx: Context, value: str):
    ctx.state.set("inp_type", value)
    await ctx.refresh()


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("inp_disabled", value)
    await ctx.refresh()


async def _set_required(ctx: Context, value: bool):
    ctx.state.set("inp_required", value)
    await ctx.refresh()


async def _set_error(ctx: Context, value: bool):
    ctx.state.set("inp_error", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    inp_type = ctx.state.get("inp_type", "text")
    disabled = ctx.state.get("inp_disabled", False)
    required = ctx.state.get("inp_required", False)
    show_error = ctx.state.get("inp_error", False)

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Type", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": t, "label": t}
                            for t in [
                                "text",
                                "email",
                                "password",
                                "number",
                                "search",
                                "tel",
                                "url",
                            ]
                        ],
                        value=inp_type,
                        on_change=ctx.callback(_set_type),
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
            Input(
                name="demo",
                label="Demo Input",
                description="Type something here.",
                placeholder="Enter text…",
                type=inp_type,
                disabled=disabled,
                required=required,
                error="This field is required." if show_error else None,
            )
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Input(\n"
                f'    name="demo",\n'
                f'    label="Demo Input",\n'
                f'    placeholder="Enter text…",\n'
                f'    type="{inp_type}",\n'
                f"    disabled={disabled},\n"
                f"    required={required},\n"
                f'    error={"None" if not show_error else repr("This field is required.")},\n'
                f")\n"
                f"```"
            )
        ),
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Input component reference page."""
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
A single-line text input with optional label, description, placeholder, validation, and event callbacks.

```python
from refast.components import Input

Input(name="username", placeholder="Enter username")
Input(
    name="email",
    label="Email Address",
    description="We'll never share your email.",
    type="email",
    required=True,
    error="Please enter a valid email",
    on_change=ctx.callback(handle_change),
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \\| None` | `None` | HTML name attribute |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below label |
| `type` | `"text" \\| "email" \\| "password" \\| "number" \\| "tel" \\| "url" \\| "search"` | `"text"` | Input type |
| `placeholder` | `str` | `""` | Placeholder text |
| `value` | `str \\| None` | `None` | Controlled value |
| `default_value` | `str \\| None` | `None` | Uncontrolled initial value |
| `required` | `bool` | `False` | Shows required asterisk |
| `disabled` | `bool` | `False` | Disables interaction |
| `read_only` | `bool` | `False` | Read-only mode |
| `error` | `str \\| None` | `None` | Error message |
| `debounce` | `int` | `0` | Delay in ms before `on_change` fires |
| `on_change` | `Callback \\| None` | `None` | Fired on value change |
| `on_blur` | `Callback \\| None` | `None` | Fired on blur |
| `on_focus` | `Callback \\| None` | `None` | Fired on focus |
| `on_keydown` | `Callback \\| None` | `None` | Fired on key-down |
| `on_keyup` | `Callback \\| None` | `None` | Fired on key-up |
| `on_input` | `Callback \\| None` | `None` | Fired on every input event |
| `class_name` | `str` | `""` | Extra Tailwind classes |
"""
