"""InputOTP — /docs/components/input-otp."""

from refast import Context
from refast.components import (
    Alert,
    Badge,
    Container,
    Heading,
    Markdown,
    Separator,
)

PAGE_TITLE = "InputOTP"
PAGE_ROUTE = "/docs/components/input-otp"


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the InputOTP component reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Badge("Not Yet Implemented", variant="secondary", class_name="mb-4"),
            Alert(
                title="Coming Soon",
                message=(
                    "The InputOTP family of components is planned but not yet implemented. "
                    "It will provide accessible one-time password / verification code inputs "
                    "with configurable length, grouping, and separators."
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

The `InputOTP` family follows the shadcn/ui composable pattern — build your OTP
input from individual slot and group primitives:

```python
from refast.components.shadcn.input import (  # not yet available
    InputOTP,
    InputOTPGroup,
    InputOTPSlot,
    InputOTPSeparator,
)

# 6-digit OTP with middle separator
InputOTP(
    max_length=6,
    value=otp_value,
    disabled=False,
    on_change=ctx.callback(handle_otp_change),
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
)

# 4-digit PIN (no separator)
InputOTP(
    max_length=4,
    on_change=ctx.callback(handle_pin_change),
    children=[
        InputOTPGroup(children=[
            InputOTPSlot(index=0),
            InputOTPSlot(index=1),
            InputOTPSlot(index=2),
            InputOTPSlot(index=3),
        ]),
    ],
)
```

## Planned Component Props

### InputOTP

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `max_length` | `int` | required | Total number of OTP characters |
| `value` | `str \\| None` | `None` | Controlled value |
| `disabled` | `bool` | `False` | Disables all slots |
| `on_change` | `Callback \\| None` | `None` | Fired with the current OTP string |
| `children` | `list` | required | `InputOTPGroup` / `InputOTPSeparator` children |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### InputOTPGroup

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list[InputOTPSlot]` | required | `InputOTPSlot` children |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### InputOTPSlot

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `index` | `int` | required | Zero-based position within the OTP string |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### InputOTPSeparator

A decorative separator between groups. No required props.

## Workaround

Until `InputOTP` is available, use multiple single-character `Input` fields
managed with component state, or a single `Input` with `maxlength` + formatting.
"""
