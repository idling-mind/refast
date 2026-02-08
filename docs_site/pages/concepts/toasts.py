"""Toast Notifications — /docs/concepts/toasts."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Toast Notifications"
PAGE_ROUTE = "/docs/concepts/toasts"


def render(ctx):
    """Render the toasts concept page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Overview

Toasts are non-intrusive notifications that appear temporarily. Refast uses the Sonner
library under the hood for smooth, accessible toast notifications.

## Basic Usage

```python
await ctx.show_toast("Operation successful!", variant="success")
```

## Variants

| Variant | Use Case |
|---------|----------|
| `"default"` | General information |
| `"success"` | Successful operations |
| `"error"` | Errors and failures |
| `"warning"` | Warnings and cautions |
| `"info"` | Informational messages |
| `"loading"` | In-progress operations |

## Full API

```python
await ctx.show_toast(
    message="File uploaded",
    variant="success",
    description="document.pdf was uploaded successfully",
    duration=5000,          # milliseconds (default: 4000)
    position="top-right",   # top-left, top-center, top-right,
                            # bottom-left, bottom-center, bottom-right
    dismissible=True,       # Can be dismissed by clicking
    close_button=True,      # Show close button
    invert=False,           # Invert colors
    action={"label": "Undo", "onClick": ctx.callback(undo)},
    cancel={"label": "Cancel", "onClick": ctx.callback(cancel)},
    toast_id="upload-toast", # Custom ID (for updating/dismissing)
)
```

## Positions

```
top-left      top-center      top-right
bottom-left   bottom-center   bottom-right
```

## Updating a Toast

Use `toast_id` to update an existing toast:

```python
await ctx.show_toast("Uploading...", variant="loading", toast_id="upload")
# ... later
await ctx.show_toast("Done!", variant="success", toast_id="upload")
```

## Next Steps

- [JavaScript Interop](/docs/concepts/js-interop) — Client-side callbacks
- [Components Reference](/docs/components/feedback) — Feedback components
"""
