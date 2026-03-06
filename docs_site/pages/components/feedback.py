"""Feedback & Overlay — /docs/components/feedback."""

from refast.components import Container, Heading, Separator

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "Feedback & Overlay"
PAGE_ROUTE = "/docs/components/feedback"


def render(ctx):
    """Render the feedback components reference page."""
    from docs_site.app import docs_layout

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
## Overview

Feedback components communicate status and system state to the user.
Overlay components display content in floating layers above the page.

---

## Alert

Displays an inline status message with an optional title and dismiss action.

```python
Alert(
    title="Heads Up!",
    message="Your session will expire in 5 minutes.",
    variant="warning",
)
Alert(
    message="File deleted successfully.",
    variant="success",
    dismissible=True,
    on_dismiss=ctx.callback(clear_alert),
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `str \| None` | `None` | Bold heading shown above the message |
| `message` | `str` | `""` | Body text of the alert |
| `variant` | `"default" \| "success" \| "warning" \| "destructive" \| "info"` | `"default"` | Visual style |
| `dismissible` | `bool` | `False` | Shows an × close button |
| `on_dismiss` | `Callback \| None` | `None` | Called when the close button is clicked |

---

## Spinner

Animated loading indicator.

```python
Spinner()             # medium by default
Spinner(size="sm")    # compact inline spinner
Spinner(size="lg")    # large full-page indicator
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Size of the spinner |

---

## Progress

Horizontal progress bar for deterministic operations.

```python
Progress(
    value=65,
    max=100,
    label="Uploading...",
    show_value=True,
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `float` | `0` | Current progress value |
| `max` | `float` | `100` | Maximum value |
| `label` | `str \| None` | `None` | Text label above the bar |
| `show_value` | `bool` | `False` | Show the `value/max` as text |
| `foreground_color` | `str \| None` | `None` | Override bar fill colour (CSS value) |
| `track_color` | `str \| None` | `None` | Override track colour (CSS value) |
| `striped` | `bool` | `False` | Striped animated pattern |

---

## Skeleton

Placeholder shape used while content is loading.

```python
Skeleton(width="100%", height=20)                   # rectangular
Skeleton(variant="circular", width=40, height=40)   # avatar placeholder
Skeleton(variant="text", width="60%")               # text line
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `"rectangular" \| "circular" \| "text"` | `"rectangular"` | Shape variant |
| `width` | `str \| int \| None` | `None` | Width (px or CSS string) |
| `height` | `str \| int \| None` | `None` | Height (px or CSS string) |

---

## ConnectionStatus

Shows connection state to the user. Renders different content depending on
whether the WebSocket connection is active.

```python
ConnectionStatus(
    children_connected=[Text("● Online", class_name="text-green-500")],
    children_disconnected=[Text("● Offline", class_name="text-red-500")],
    position="bottom-right",
    debounce_ms=1000,
    on_disconnect=ctx.callback(handle_disconnect),
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children_connected` | `list` | `[]` | Content shown when connected |
| `children_disconnected` | `list` | `[]` | Content shown when disconnected |
| `position` | `"top-left" \| "top-right" \| "bottom-left" \| "bottom-right" \| None` | `None` | Fixed screen corner; `None` renders inline |
| `debounce_ms` | `int` | `0` | Milliseconds to wait before updating state |
| `on_disconnect` | `Callback \| None` | `None` | Python callback on disconnection |
| `on_reconnect` | `Callback \| None` | `None` | Python callback on reconnection |
| `js_on_disconnect` | `str \| None` | `None` | Raw JS expression run on disconnect |
| `js_on_reconnect` | `str \| None` | `None` | Raw JS expression run on reconnect |

---

## Dialog

A modal dialog that blocks interaction with the page until dismissed.

```python
Dialog(
    children=[
        DialogTrigger(children=[Button("Delete", variant="destructive")]),
        DialogContent(
            children=[
                DialogHeader(
                    children=[
                        DialogTitle("Are you sure?"),
                        DialogDescription("This action cannot be undone."),
                    ]
                ),
                DialogFooter(
                    children=[
                        DialogCancel("Cancel"),
                        DialogAction("Delete", on_click=ctx.callback(delete_item)),
                    ]
                ),
            ]
        ),
    ]
)
```

| Component | Key Props | Notes |
|-----------|-----------|-------|
| `Dialog` | `open`, `default_open`, `on_open_change` | Root; controls open state |
| `DialogTrigger` | `children` | Element that opens the dialog |
| `DialogContent` | `children` | The dialog panel |
| `DialogHeader` | `children` | Top section (title + description) |
| `DialogFooter` | `children` | Bottom section (action buttons) |
| `DialogTitle` | `title` or `children` | Bold heading |
| `DialogDescription` | `description` or `children` | Muted sub-text |
| `DialogAction` | `label`, `on_click`, `variant` | Confirms the action |
| `DialogCancel` | `label`, `on_click` | Dismisses the dialog |

---

## Sheet

A panel that slides in from one edge of the screen.

```python
Sheet(
    children=[
        SheetTrigger(children=[Button("Open Settings")]),
        SheetContent(
            side="right",
            children=[
                SheetHeader(
                    children=[
                        SheetTitle("Settings"),
                        SheetDescription("Adjust your preferences."),
                    ]
                ),
                SheetFooter(
                    children=[SheetClose(children=[Button("Close")])]
                ),
            ],
        ),
    ]
)
```

### SheetContent

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"top" \| "right" \| "bottom" \| "left"` | `"right"` | Which edge it slides from |

Other sub-components: `SheetTrigger`, `SheetClose`, `SheetHeader`,
`SheetFooter`, `SheetTitle`, `SheetDescription`.

---

## Drawer

Similar to `Sheet` but styled as a drawer — typically used for bottom-anchored panels.

```python
Drawer(
    children=[
        DrawerTrigger(children=[Button("Open Drawer")]),
        DrawerContent(
            children=[
                DrawerHeader(
                    children=[
                        DrawerTitle("Cart"),
                        DrawerDescription("Review your items."),
                    ]
                ),
                DrawerFooter(
                    children=[
                        Button("Checkout", on_click=ctx.callback(checkout)),
                        DrawerClose(children=[Button("Cancel", variant="outline")]),
                    ]
                ),
            ]
        ),
    ]
)
```

Sub-components: `DrawerTrigger`, `DrawerContent`, `DrawerHeader`, `DrawerFooter`,
`DrawerTitle`, `DrawerDescription`, `DrawerClose`.

---

## Popover

A small floating panel anchored to a trigger element.

```python
Popover(
    children=[
        PopoverTrigger(children=[Button("Filter", variant="outline")]),
        PopoverContent(
            side="bottom",
            align="start",
            children=[Text("Filter options here")],
        ),
    ]
)
```

### PopoverContent

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"top" \| "right" \| "bottom" \| "left"` | `"bottom"` | Preferred placement side |
| `side_offset` | `int` | `4` | Pixel gap from trigger |
| `align` | `"start" \| "center" \| "end"` | `"center"` | Alignment along the side |

---

## HoverCard

A card that appears on hover, useful for previews or extra details.

```python
HoverCard(
    open_delay=500,
    close_delay=200,
    children=[
        HoverCardTrigger(children=[Link("@username", href="/profile")]),
        HoverCardContent(
            children=[Text("User profile preview here")]
        ),
    ]
)
```

### HoverCard

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open_delay` | `int` | `700` | Milliseconds before showing the card |
| `close_delay` | `int` | `300` | Milliseconds before hiding the card |

### HoverCardContent

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"top" \| "right" \| "bottom" \| "left"` | `"bottom"` | Preferred placement |
| `align` | `"start" \| "center" \| "end"` | `"center"` | Alignment |
| `side_offset` | `int` | `4` | Pixel gap from trigger |
"""
