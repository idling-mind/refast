"""Alert — /docs/components/alert."""

from refast import Context
from refast.components import (
    Alert,
    Button,
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

PAGE_TITLE = "Alert"
PAGE_ROUTE = "/docs/components/alert"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_variant(ctx: Context, value: str):
    ctx.state.set("alrt_variant", value)
    await ctx.refresh()


async def _set_dismissible(ctx: Context, value: bool):
    ctx.state.set("alrt_dismissible", value)
    await ctx.refresh()


async def _dismiss(ctx: Context):
    ctx.state.set("alrt_dismissed", True)
    await ctx.refresh()


async def _reset_alert(ctx: Context):
    ctx.state.set("alrt_dismissed", False)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    variant = ctx.state.get("alrt_variant", "default")
    dismissible = ctx.state.get("alrt_dismissible", False)
    dismissed = ctx.state.get("alrt_dismissed", False)

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    Row(
                        gap=4,
                        wrap=True,
                        class_name="mb-4",
                        children=[
                            Column(
                                gap=1,
                                children=[
                                    Text("Variant", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in [
                                                "default",
                                                "success",
                                                "warning",
                                                "destructive",
                                                "info",
                                            ]
                                        ],
                                        value=variant,
                                        on_change=ctx.callback(_set_variant),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("Dismissible", class_name="text-sm font-medium"),
                                    Checkbox(
                                        label="dismissible",
                                        checked=dismissible,
                                        on_change=ctx.callback(_set_dismissible),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30",
                        children=[
                            Alert(
                                title="Heads up!",
                                message="This is an example alert message.",
                                variant=variant,
                                dismissible=dismissible,
                                on_dismiss=ctx.callback(_dismiss) if dismissible else None,
                            )
                            if not dismissed
                            else Button("Reset", on_click=ctx.callback(_reset_alert))
                        ],
                    ),
                    Markdown(
                        content=(
                            f"```python\n"
                            f"Alert(\n"
                            f'    title="Heads up!",\n'
                            f'    message="This is an example alert message.",\n'
                            f'    variant="{variant}",\n'
                            f"    dismissible={dismissible},\n"
                            + (
                                "    on_dismiss=ctx.callback(handle_dismiss),\n"
                                if dismissible
                                else ""
                            )
                            + ")\n"
                            "```"
                        )
                    ),
                ]
            ),
        ]
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Alert component reference page."""
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
An inline status message that draws the user's attention without
interrupting their workflow (unlike a dialog or toast).

```python
from refast.components import Alert

Alert(title="Success!", message="Your changes have been saved.", variant="success")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `str \\| None` | `None` | Bold heading of the alert |
| `message` | `str \\| None` | `None` | Body text |
| `variant` | `"default" \\| "success" \\| "warning" \\| "destructive" \\| "info"` | `"default"` | Color and icon |
| `dismissible` | `bool` | `False` | Show a close button |
| `on_dismiss` | `Callback \\| None` | `None` | Called when the close button is clicked |
| `children` | `ChildrenType` | `None` | Custom content inside the alert |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Variants

```python
Alert(title="Note", message="Informational message.", variant="default")
Alert(title="Success", message="Operation completed.", variant="success")
Alert(title="Warning", message="Proceed with caution.", variant="warning")
Alert(title="Error", message="Something went wrong.", variant="destructive")
Alert(title="Info", message="Here is some information.", variant="info")
```

## Dismissible Alert

```python
async def handle_dismiss(ctx: Context):
    ctx.state.set("show_alert", False)
    await ctx.refresh()

# In your render function:
Alert(
    title="Session expiring",
    message="Your session will expire in 5 minutes.",
    variant="warning",
    dismissible=True,
    on_dismiss=ctx.callback(handle_dismiss),
)
```

## With Custom Children

```python
Alert(
    title="Custom content",
    children=[
        Text("This alert has a custom body with rich content."),
        Button("Take action", size="sm", variant="outline", class_name="mt-2"),
    ]
)
```
"""
