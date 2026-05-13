"""Dialog & AlertDialog — /docs/components/dialog."""

from refast import Context
from refast.components import (
    Button,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Dialog,
    DialogAction,
    DialogCancel,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    Heading,
    Input,
    Markdown,
    Row,
    Separator,
    Text,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Dialog"
PAGE_ROUTE = "/docs/components/dialog"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _open_dialog(ctx: Context):
    ctx.state.set("dlg_open", True)
    await ctx.refresh()


async def _close_dialog(ctx: Context):
    ctx.state.set("dlg_open", False)
    await ctx.refresh()


async def _confirm_dialog(ctx: Context):
    ctx.state.set("dlg_open", False)
    ctx.state.set("dlg_confirmed", True)
    await ctx.refresh()


async def _set_dialog_open(ctx: Context, value: bool):
    ctx.state.set("dlg_open", value)
    await ctx.refresh()


async def _set_title(ctx: Context, value: str):
    ctx.state.set("dlg_title", value)
    await ctx.refresh()


async def _set_description(ctx: Context, value: str):
    ctx.state.set("dlg_description", value)
    await ctx.refresh()


async def _open_destructive(ctx: Context):
    ctx.state.set("dlg_destructive_open", True)
    await ctx.refresh()


async def _close_destructive(ctx: Context):
    ctx.state.set("dlg_destructive_open", False)
    await ctx.refresh()


async def _confirm_destructive(ctx: Context):
    ctx.state.set("dlg_destructive_open", False)
    ctx.state.set("dlg_destructive_confirmed", True)
    await ctx.refresh()


async def _set_destructive_open(ctx: Context, value: bool):
    ctx.state.set("dlg_destructive_open", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    open_state = ctx.state.get("dlg_open", False)
    confirmed = ctx.state.get("dlg_confirmed", False)
    title = ctx.state.get("dlg_title", "Edit Profile")
    description = ctx.state.get(
        "dlg_description", "Make changes to your profile here. Click save when done."
    )

    return playground_card(
        options=[
            Column(
                gap=1,
                class_name="flex-1 min-w-48",
                children=[
                    Text("Dialog title", class_name="text-sm font-medium"),
                    Input(
                        value=title,
                        on_change=ctx.callback(_set_title),
                        placeholder="Dialog title",
                    ),
                ],
            ),
            Column(
                gap=1,
                class_name="flex-1 min-w-48",
                children=[
                    Text("Description", class_name="text-sm font-medium"),
                    Input(
                        value=description,
                        on_change=ctx.callback(_set_description),
                        placeholder="Dialog description",
                    ),
                ],
            ),
        ],
        preview=[
            Dialog(
                open=open_state,
                on_open_change=ctx.callback(_set_dialog_open),
                children=[
                    DialogTrigger(
                        children=[
                            Button("Open Dialog", on_click=ctx.callback(_open_dialog)),
                        ]
                    ),
                    DialogContent(
                        children=[
                            DialogHeader(
                                children=[
                                    DialogTitle(title=title),
                                    DialogDescription(description=description),
                                ]
                            ),
                            DialogFooter(
                                children=[
                                    DialogCancel(
                                        label="Cancel",
                                        on_click=ctx.callback(_close_dialog),
                                    ),
                                    DialogAction(
                                        label="Save changes",
                                        on_click=ctx.callback(_confirm_dialog),
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
            ),
            Text(
                "Dialog confirmed!" if confirmed else "",
                class_name="text-sm text-green-600",
            ),
        ],
        preview_class="border rounded-lg p-4 bg-muted/30 flex flex-col gap-3 items-start",
    )


def _alert_dialog_section(ctx: Context):
    destructive_open = ctx.state.get("dlg_destructive_open", False)
    destructive_confirmed = ctx.state.get("dlg_destructive_confirmed", False)

    return Card(
        class_name="mt-6",
        children=[
            CardHeader(title="AlertDialog — Destructive Confirmation"),
            CardContent(
                children=[
                    Text(
                        "Use a destructive variant dialog to confirm dangerous actions.",
                        class_name="text-sm text-muted-foreground mb-4",
                    ),
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30 flex flex-col gap-3 items-start",
                        children=[
                            Dialog(
                                open=destructive_open,
                                on_open_change=ctx.callback(_set_destructive_open),
                                variant="destructive",
                                children=[
                                    DialogTrigger(
                                        children=[
                                            Button(
                                                "Delete Account",
                                                variant="destructive",
                                                on_click=ctx.callback(_open_destructive),
                                            ),
                                        ]
                                    ),
                                    DialogContent(
                                        children=[
                                            DialogHeader(
                                                children=[
                                                    DialogTitle(title="Are you absolutely sure?"),
                                                    DialogDescription(
                                                        description="This action cannot be undone. "
                                                        "This will permanently delete your account "
                                                        "and remove your data from our servers."
                                                    ),
                                                ]
                                            ),
                                            DialogFooter(
                                                children=[
                                                    DialogCancel(
                                                        label="Cancel",
                                                        on_click=ctx.callback(_close_destructive),
                                                    ),
                                                    DialogAction(
                                                        label="Delete",
                                                        on_click=ctx.callback(_confirm_destructive),
                                                        class_name="bg-destructive text-destructive-foreground hover:bg-destructive/90",
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            Text(
                                "Account deleted!" if destructive_confirmed else "",
                                class_name="text-sm text-destructive",
                            ),
                        ],
                    ),
                ]
            ),
        ]
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Dialog component reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _playground(ctx),
            _alert_dialog_section(ctx),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Content ───────────────────────────────────────────────────────────────

INTRO = """
A modal dialog that interrupts the user with important content and
expects a response. Use `variant="destructive"` for confirmation
of dangerous actions.

```python
from refast.components import (
    Dialog, DialogTrigger, DialogContent, DialogHeader,
    DialogTitle, DialogDescription, DialogFooter, DialogAction, DialogCancel,
)
```
"""

REFERENCE = """
## Props

### `Dialog`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `bool \\| None` | `None` | Controlled open state |
| `default_open` | `bool` | `False` | Initial open state |
| `on_open_change` | `Callback \\| None` | `None` | Called when open state changes |
| `title` | `str \\| None` | `None` | Shorthand title (skips `DialogHeader`) |
| `description` | `str \\| None` | `None` | Shorthand description |
| `confirm_label` | `str` | `"Continue"` | Label for the confirm button |
| `cancel_label` | `str` | `"Cancel"` | Label for the cancel button |
| `on_confirm` | `Callback \\| None` | `None` | Confirm callback |
| `on_cancel` | `Callback \\| None` | `None` | Cancel callback |
| `variant` | `"default" \\| "destructive"` | `"default"` | Visual style |
| `trigger` | `Component \\| None` | `None` | Shorthand trigger component |

### `DialogAction`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Button text |
| `on_click` | `Callback \\| None` | `None` | Click callback |

### `DialogCancel`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | `"Cancel"` | Button text |
| `on_click` | `Callback \\| None` | `None` | Click callback |

## Shorthand API

For simple dialogs, use the shorthand props on `Dialog` instead of
composing `DialogContent`, `DialogHeader`, etc.:

```python
Dialog(
    trigger=Button("Open"),
    title="Confirm action",
    description="Are you sure you want to proceed?",
    confirm_label="Yes, proceed",
    cancel_label="No, cancel",
    on_confirm=ctx.callback(handle_confirm),
    on_cancel=ctx.callback(handle_cancel),
)
```

## Composable API

For custom content, use the full component hierarchy:

```python
Dialog(
    open=show_dialog,
    on_open_change=ctx.callback(handle_open_change),
    children=[
        DialogTrigger(children=[Button("Open")]),
        DialogContent(
            children=[
                DialogHeader(
                    children=[
                        DialogTitle(title="Edit Profile"),
                        DialogDescription(description="Make changes here."),
                    ]
                ),
                # custom form fields
                DialogFooter(
                    children=[
                        DialogCancel(label="Cancel"),
                        DialogAction(label="Save", on_click=ctx.callback(handle_save)),
                    ]
                ),
            ]
        ),
    ]
)
```
"""
