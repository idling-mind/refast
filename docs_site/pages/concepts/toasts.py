"""Toast Notifications — /docs/concepts/toasts."""

from docs_site.pages.utils import render_markdown_with_demo_apps
from refast import Context
from refast.components import Button, Column, Container, Heading, Row, Separator, Text

PAGE_TITLE = "Toast Notifications"
PAGE_ROUTE = "/docs/concepts/toasts"


# ── Variant demo callbacks ────────────────────────────────────────────────


async def _toast_default(ctx: Context) -> None:
    await ctx.show_toast("This is a default toast notification.")


async def _toast_success(ctx: Context) -> None:
    await ctx.show_toast("Changes saved successfully!", variant="success")


async def _toast_error(ctx: Context) -> None:
    await ctx.show_toast(
        "Something went wrong",
        variant="error",
        description="Please try again or contact support.",
    )


async def _toast_warning(ctx: Context) -> None:
    await ctx.show_toast("Please review your input before continuing.", variant="warning")


async def _toast_info(ctx: Context) -> None:
    await ctx.show_toast("New features are available in this release.", variant="info")


async def _toast_loading(ctx: Context) -> None:
    await ctx.show_toast("Processing your request...", variant="loading", duration=3000)


# ── Demo builder ──────────────────────────────────────────────────────────


def _variants_demo(ctx: Context):
    return Column(
        gap=3,
        children=[
            Heading("Live demo: toast variants", level=3, class_name="text-lg font-semibold"),
            Text(
                "Click each button to trigger the corresponding toast variant.",
                class_name="text-sm text-muted-foreground",
            ),
            Row(
                gap=2,
                wrap=True,
                children=[
                    Button(
                        "Default",
                        on_click=ctx.callback(_toast_default),
                        variant="secondary",
                    ),
                    Button(
                        "Success",
                        on_click=ctx.callback(_toast_success),
                        variant="default",
                    ),
                    Button(
                        "Error",
                        on_click=ctx.callback(_toast_error),
                        variant="destructive",
                    ),
                    Button(
                        "Warning",
                        on_click=ctx.callback(_toast_warning),
                        variant="outline",
                    ),
                    Button(
                        "Info",
                        on_click=ctx.callback(_toast_info),
                        variant="ghost",
                    ),
                    Button(
                        "Loading",
                        on_click=ctx.callback(_toast_loading),
                        variant="secondary",
                    ),
                ],
            ),
        ],
    )


def render(ctx):
    """Render the toasts concept page."""
    from docs_site.app import docs_layout

    variants_demo = _variants_demo(ctx)

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
Toasts are non-intrusive, temporary notifications that appear on screen and disappear
automatically. Refast uses the [Sonner](https://sonner.emilkowal.ski/) library under the
hood for smooth, accessible toast notifications.

> **No setup required.** The toast manager is automatically included when you use
> `RefastApp`. There is no `<Toaster>` component to add.

## Basic Usage

Call `ctx.show_toast()` from any async callback:

```python
async def handle_save(ctx: Context):
    await ctx.show_toast("Changes saved!", variant="success")
```

## Variants

Six built-in variants cover all common notification needs:

| Variant | Use Case |
|---------|----------|
| `"default"` | General information (default) |
| `"success"` | Completed operations |
| `"error"` | Errors and failures |
| `"warning"` | Warnings and cautions |
| `"info"` | Informational messages |
| `"loading"` | In-progress operations (shows a spinner) |

{{ variants_demo }}

```python
await ctx.show_toast("All done!", variant="success")
await ctx.show_toast("Something went wrong", variant="error")
await ctx.show_toast("Please review your input", variant="warning")
await ctx.show_toast("New features available", variant="info")
await ctx.show_toast("Processing your request...", variant="loading")
```

## Adding a Description

Use `description` to provide additional context below the main message:

```python
await ctx.show_toast(
    "File uploaded",
    variant="success",
    description="Your file 'document.pdf' has been uploaded successfully.",
)

await ctx.show_toast(
    "Upload failed",
    variant="error",
    description="The file exceeds the maximum size of 10MB.",
)
```

## Duration

Control how long (in milliseconds) the toast stays visible. The default is `4000` ms.

```python
# Disappears in 1 second
await ctx.show_toast("Quick message!", duration=1000)

# Stays for 10 seconds
await ctx.show_toast("Important notice", variant="info", duration=10000)

# Persistent — use a very large duration combined with close_button=True
await ctx.show_toast(
    "Action required",
    variant="warning",
    duration=100000,
    close_button=True,
    description="Click × to dismiss",
)
```

## Position

Show the toast at any of the six screen positions. The default position is configured
globally, but can be overridden per toast:

```
top-left      top-center      top-right
bottom-left   bottom-center   bottom-right
```

```python
await ctx.show_toast("Saved", position="top-right")
await ctx.show_toast("Error", variant="error", position="bottom-center")
```

## Action & Cancel Buttons

Add interactive buttons to let users react to the notification.
The `callback` key accepts any callback returned by `ctx.callback()`, `ctx.js()`,
or `ctx.chain()`.

```python
# Single action button (e.g. Undo)
await ctx.show_toast(
    "Item deleted",
    description="The item has been moved to trash",
    action={"label": "Undo", "callback": ctx.callback(undo_delete)},
    duration=5000,
)

# Single cancel button
await ctx.show_toast(
    "Sending email...",
    variant="loading",
    cancel={"label": "Cancel", "callback": ctx.callback(cancel_send)},
    duration=10000,
)

# Both action and cancel buttons
await ctx.show_toast(
    "Confirm changes?",
    variant="info",
    description="You have unsaved changes that will be lost",
    action={"label": "Save", "callback": ctx.callback(save_changes)},
    cancel={"label": "Discard", "callback": ctx.callback(discard_changes)},
    duration=10000,
)
```

You can also use a JavaScript callback as the action:

```python
await ctx.show_toast(
    "Link ready",
    action={"label": "Open", "callback": ctx.js("window.open('/result')")},
)
```

## Style Options

### Close Button

Show an explicit × button so users can dismiss the toast manually:

```python
await ctx.show_toast("Review this", close_button=True)
```

### Non-Dismissible

Prevent the user from clicking on the toast to dismiss it (useful for loading states):

```python
await ctx.show_toast(
    "Processing...",
    variant="loading",
    dismissible=False,
    duration=3000,
)
```

### Inverted Colors

Flip the toast color scheme (useful for dark/light contrast scenarios):

```python
await ctx.show_toast("Inverted toast", invert=True)
```

## Updating Toasts

Assign a `toast_id` to a toast, then call `show_toast` again with the same `toast_id`
to update it in place — the existing notification is replaced without creating a new one.

```python
# Show a loading toast
await ctx.show_toast(
    "Uploading...",
    variant="loading",
    toast_id="upload-progress",
    description="Please wait while we upload your file",
)

await asyncio.sleep(2)

# Update the same toast to show completion
await ctx.show_toast(
    "Upload complete!",
    variant="success",
    toast_id="upload-progress",
    description="Your file has been uploaded successfully",
)
```

### Multi-Step Process

Chain multiple updates to walk the user through a sequence of steps:

```python
steps = [
    ("Connecting...",     "Establishing connection to server"),
    ("Authenticating...", "Verifying your credentials"),
    ("Syncing...",        "Downloading latest data"),
    ("Complete!",         "All data has been synchronized"),
]

for i, (title, description) in enumerate(steps):
    variant = "success" if i == len(steps) - 1 else "loading"
    await ctx.show_toast(title, variant=variant, toast_id="process", description=description)
    if i < len(steps) - 1:
        await asyncio.sleep(1.5)
```

## Custom Component Toasts

Pass any Refast component tree to the `component` parameter to render fully interactive
UI inside a toast. This is useful for confirmation dialogs, progress indicators, or any
custom layout.

> When using `component`, the `message` parameter is ignored — your component provides
> all the content.

### Confirmation with Buttons

```python
from refast.components import Badge, Button, Column, Heading, Row, Text

async def show_confirm_toast(ctx: Context):
    await ctx.show_toast(
        component=Column(
            gap=2,
            children=[
                Heading("Confirm Action", level=6),
                Text("This will permanently delete the selected items."),
                Row(
                    gap=2,
                    children=[
                        Button(
                            "Delete",
                            size="sm",
                            variant="destructive",
                            on_click=ctx.callback(do_delete),
                        ),
                        Button(
                            "Cancel",
                            size="sm",
                            variant="secondary",
                            on_click=ctx.callback(cancel_delete),
                        ),
                    ],
                ),
                Row(children=[Badge("Irreversible", variant="destructive", class_name="mt-1")]),
            ],
        ),
        duration=15000,
        close_button=True,
    )
```

### Progress Bar Inside a Toast

Combine a `toast_id` with `ctx.update_props()` to animate a progress bar that lives
inside the toast:

```python
from refast.components import Column, Heading, Progress, Text

async def show_progress_toast(ctx: Context):
    await ctx.show_toast(
        component=Column(
            gap=2,
            children=[
                Heading("Uploading file", level=6),
                Text("Please wait while we upload your file."),
                Progress(
                    id="toast-progress",
                    value=0,
                    max=100,
                    class_name="w-full",
                    foreground_color="primary",
                ),
            ],
        ),
        variant="default",
        duration=100000,
        close_button=True,
        toast_id="progress-toast",
    )

    for i in range(10):
        await ctx.update_props("toast-progress", {"value": (i + 1) * 10})
        await asyncio.sleep(1)

    await ctx.show_toast(
        "Upload complete!",
        variant="success",
        toast_id="progress-toast",
    )
```

## Full API Reference

```python
await ctx.show_toast(
    message="",                # Main message text (ignored when component is set)
    variant="default",         # "default" | "success" | "error" | "warning" | "info" | "loading"
    description=None,          # Secondary text shown below the message
    duration=None,             # Milliseconds visible (default: 4000)
    position=None,             # "top-left" | "top-center" | "top-right"
                               # "bottom-left" | "bottom-center" | "bottom-right"
    dismissible=True,          # Allow click-to-dismiss
    close_button=None,         # Show an explicit × close button
    invert=False,              # Invert the color scheme
    action=None,               # {"label": str, "callback": ctx.callback(fn)}
    cancel=None,               # {"label": str, "callback": ctx.callback(fn)}
    toast_id=None,             # Stable ID — reuse to update an existing toast
    component=None,            # Any Refast component tree rendered inside the toast
)
```

## Next Steps

- [JavaScript Interop](/docs/concepts/js-interop) — Use `ctx.js()` in toast action callbacks
- [Components Reference](/docs/components/feedback) — Progress, Badge, and other feedback components
- [Toast Showcase Example](https://github.com/your-repo/examples/toast_showcase) — Live demo of all features
"""
