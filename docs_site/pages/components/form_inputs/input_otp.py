"""InputOTP — /docs/components/input-otp."""

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
from refast.components.shadcn.controls import (
    InputOTP,
    InputOTPGroup,
    InputOTPSeparator,
    InputOTPSlot,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "InputOTP"
PAGE_ROUTE = "/docs/components/input-otp"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("otp_disabled", value)
    await ctx.refresh()


async def _set_required(ctx: Context, value: bool):
    ctx.state.set("otp_required", value)
    await ctx.refresh()


async def _set_length(ctx: Context, value: str):
    ctx.state.set("otp_length", value)
    ctx.state.set("otp_value", "")
    ctx.state.set("otp_complete", None)
    await ctx.refresh()


async def _on_change(ctx: Context, value: str):
    ctx.state.set("otp_value", value)
    ctx.state.set("otp_complete", None)
    await ctx.refresh()


async def _on_complete(ctx: Context, value: str):
    ctx.state.set("otp_complete", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    disabled = ctx.state.get("otp_disabled", False)
    required = ctx.state.get("otp_required", False)
    length = int(ctx.state.get("otp_length", "6"))
    current_value = ctx.state.get("otp_value", "")
    completed = ctx.state.get("otp_complete", None)

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Length", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "4", "label": "4 digits"},
                            {"value": "6", "label": "6 digits"},
                            {"value": "8", "label": "8 digits"},
                        ],
                        value=str(length),
                        on_change=ctx.callback(_set_length),
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
        ],
        preview=[
            InputOTP(
                max_length=length,
                disabled=disabled,
                required=required,
                label="Verification Code",
                description="Enter the code sent to your device.",
                on_change=ctx.callback(_on_change),
                on_complete=ctx.callback(_on_complete),
            ),
            Text(
                f"Value: {current_value or '—'}",
                class_name="text-sm text-muted-foreground",
            ),
            *(
                [Text(f"✓ Completed: {completed}", class_name="text-sm text-green-600 font-medium")]
                if completed and len(completed) == length
                else []
            ),
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"InputOTP(\n"
                f"    max_length={length},\n"
                f"    disabled={disabled},\n"
                f"    required={required},\n"
                f"    on_change=ctx.callback(handle_change),\n"
                f"    on_complete=ctx.callback(handle_complete),\n"
                f")\n"
                f"```"
            )
        ),
        preview_class="border rounded-lg p-6 bg-muted/30 flex flex-col items-center gap-4",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the InputOTP component reference page."""
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
Accessible one-time password input composed from individual slot primitives.
Supports configurable length, custom grouping, and separators.

```python
from refast.components.shadcn.controls import (
    InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator,
)

# Simple 6-digit OTP (auto-layout)
InputOTP(
    max_length=6,
    on_complete=ctx.callback(handle_complete),
)

# Custom layout: two groups of 3 separated by a dash
InputOTP(
    max_length=6,
    children=[
        InputOTPGroup(children=[
            InputOTPSlot(index=0),
            InputOTPSlot(index=1),
            InputOTPSlot(index=2),
        ]),
        InputOTPSeparator(),
        InputOTPGroup(children=[
            InputOTPSlot(index=3),
            InputOTPSlot(index=4),
            InputOTPSlot(index=5),
        ]),
    ],
    on_complete=ctx.callback(handle_complete),
)
```
"""

REFERENCE = """
## InputOTP Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `max_length` | `int` | `6` | Total number of OTP characters |
| `value` | `str \\| None` | `None` | Controlled value |
| `disabled` | `bool` | `False` | Disables all slots |
| `pattern` | `str \\| None` | `None` | Regex pattern to validate each character |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below label |
| `required` | `bool` | `False` | Shows required asterisk |
| `error` | `str \\| None` | `None` | Error message |
| `on_change` | `Callback \\| None` | `None` | Fired with the current OTP string on every keystroke |
| `on_complete` | `Callback \\| None` | `None` | Fired when all slots are filled |
| `children` | `list \\| None` | `None` | Custom `InputOTPGroup` / `InputOTPSeparator` layout |

## InputOTPSlot Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `index` | `int` | required | Zero-based position within the parent `InputOTP` |
"""
