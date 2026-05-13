"""Form — /docs/components/form."""

from refast import Context
from refast.components import (
    Badge,
    Button,
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
    Separator,
    Text,
)
from refast.components.shadcn.form import Form, FormField, Label
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Form"
PAGE_ROUTE = "/docs/components/form"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _on_submit(ctx: Context):
    form_data = ctx.event_data
    name = (form_data.get("frm_name") or "").strip()
    email = (form_data.get("frm_email") or "").strip()

    errors: dict[str, str] = {}
    if not name:
        errors["frm_name_err"] = "Name is required."
    if not email or "@" not in email:
        errors["frm_email_err"] = "A valid email address is required."

    if errors:
        for key, msg in errors.items():
            ctx.state.set(key, msg)
        ctx.state.set("frm_submitted", False)
        ctx.state.set("frm_result", "")
    else:
        ctx.state.set("frm_name_err", "")
        ctx.state.set("frm_email_err", "")
        ctx.state.set("frm_submitted", True)
        ctx.state.set("frm_result", f"Hello, {name}! Confirmation sent to {email}.")

    await ctx.refresh()


async def _reset_form(ctx: Context):
    for key in ("frm_submitted", "frm_result", "frm_name_err", "frm_email_err"):
        ctx.state.set(key, "" if key in ("frm_result", "frm_name_err", "frm_email_err") else False)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    submitted = ctx.state.get("frm_submitted", False)
    result = ctx.state.get("frm_result", "")
    name_err = ctx.state.get("frm_name_err", "")
    email_err = ctx.state.get("frm_email_err", "")

    if submitted:
        demo_content = Column(
            gap=3,
            children=[
                Badge("Submitted Successfully", variant="default"),
                Text(result, class_name="text-sm text-muted-foreground"),
                Button(
                    "Reset",
                    variant="outline",
                    size="sm",
                    on_click=ctx.callback(_reset_form),
                ),
            ],
        )
    else:
        demo_content = Form(
            on_submit=ctx.callback(_on_submit),
            children=[
                FormField(
                    label="Full Name",
                    required=True,
                    error=name_err if name_err else None,
                    hint="First and last name.",
                    children=[
                        Input(
                            name="frm_name",
                            placeholder="Jane Smith",
                        )
                    ],
                ),
                FormField(
                    label="Email Address",
                    required=True,
                    error=email_err if email_err else None,
                    hint="We'll never share your email.",
                    children=[
                        Input(
                            name="frm_email",
                            type="email",
                            placeholder="jane@example.com",
                        )
                    ],
                ),
                Button("Submit", type="submit", class_name="mt-2"),
            ],
        )

    return playground_card(
        options=[],
        preview=[demo_content],
        code=Markdown(content=CODE_EXAMPLE),
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Form component reference page."""
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
Form wrapper components that intercept the browser submit event and route all data over
the WebSocket to a server callback. Also includes `FormField` for labelled field wrappers
and `Label` for standalone label elements.

```python
from refast.components.shadcn.form import Form, FormField, Label
from refast.components import Input, Button

async def handle_submit(ctx: Context, form_data: dict):
    name = form_data.get("name", "")
    email = form_data.get("email", "")
    # validate and process…
    await ctx.refresh()

Form(
    on_submit=ctx.callback(handle_submit),
    children=[
        FormField(
            label="Name",
            required=True,
            children=[Input(name="name", placeholder="Your name")],
        ),
        FormField(
            label="Email",
            hint="We'll never share your email.",
            required=True,
            children=[Input(name="email", type="email")],
        ),
        Button("Submit", type="submit"),
    ],
)
```
"""

CODE_EXAMPLE = """
```python
from refast.components.shadcn.form import Form, FormField
from refast.components import Input, Button

async def handle_submit(ctx: Context, form_data: dict):
    name = form_data.get("frm_name", "").strip()
    email = form_data.get("frm_email", "").strip()
    # process submission…
    await ctx.refresh()

Form(
    on_submit=ctx.callback(handle_submit),
    children=[
        FormField(
            label="Full Name",
            required=True,
            hint="First and last name.",
            children=[Input(name="frm_name", placeholder="Jane Smith")],
        ),
        FormField(
            label="Email Address",
            required=True,
            hint="We'll never share your email.",
            children=[Input(name="frm_email", type="email", placeholder="jane@example.com")],
        ),
        Button("Submit", type="submit", class_name="mt-2"),
    ],
)
```
"""

REFERENCE = """
## Form Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Form content — typically `FormField` components and a submit `Button` |
| `on_submit` | `Callback \\| None` | `None` | Called with `form_data: dict` when the form is submitted. Keys are `Input` `name` values |
| `id` | `str \\| None` | auto | Component ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

> **Note:** `method` and `enctype` are not configurable — all data is sent over the WebSocket.

## FormField Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | The input component(s) to wrap |
| `label` | `str \\| None` | `None` | Field label text |
| `hint` | `str \\| None` | `None` | Hint text displayed below the label |
| `error` | `str \\| None` | `None` | Validation error displayed below the field |
| `required` | `bool` | `False` | Shows required asterisk |
| `id` | `str \\| None` | auto | Component ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Label Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | required | Label text content |
| `html_for` | `str \\| None` | `None` | Associates label with a control's `id` (rendered as `htmlFor`) |
| `required` | `bool` | `False` | Shows required asterisk |
| `id` | `str \\| None` | auto | Component ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## InputWrapper Props

`InputWrapper` is a lower-level primitive for wrapping custom controls with label,
description, required indicator, and error message — without the `Form` context.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | The wrapped control(s) |
| `label` | `str \\| None` | `None` | Label text |
| `description` | `str \\| None` | `None` | Help text below the label |
| `required` | `bool` | `False` | Shows required asterisk |
| `error` | `str \\| None` | `None` | Error message |
| `id` | `str \\| None` | auto | Component ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |
"""
