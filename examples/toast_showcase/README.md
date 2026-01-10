# Toast Showcase Example

This example demonstrates all the toast notification features available in Refast using the [Sonner](https://sonner.emilkowal.ski/) library.

## Running the Example

```bash
cd examples/toast_showcase
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.

## Features Demonstrated

### Basic Variants

- **Default** - Standard toast notification
- **Success** - Green toast for successful operations
- **Error** - Red toast for errors
- **Warning** - Yellow/orange toast for warnings
- **Info** - Blue toast for informational messages
- **Loading** - Toast with a spinner for async operations

### Toast with Description

Add a secondary description text below the main message:

```python
await ctx.show_toast(
    "File uploaded",
    variant="success",
    description="Your file 'document.pdf' has been uploaded successfully."
)
```

### Duration Options

Control how long toasts stay visible:

```python
# Quick toast (1 second)
await ctx.show_toast("Quick!", duration=1000)

# Long toast (10 seconds)
await ctx.show_toast("Take your time", duration=10000)

# Persistent toast (until dismissed)
await ctx.show_toast("Action required", duration=100000, close_button=True)
```

### Action Buttons

Add interactive buttons to toasts:

```python
# With action button
await ctx.show_toast(
    "Item deleted",
    action={"label": "Undo", "callback_id": "undo_delete"}
)

# With cancel button
await ctx.show_toast(
    "Sending...",
    variant="loading",
    cancel={"label": "Cancel", "callback_id": "cancel_send"}
)

# With both buttons
await ctx.show_toast(
    "Confirm changes?",
    action={"label": "Save", "callback_id": "save"},
    cancel={"label": "Discard", "callback_id": "discard"}
)
```

Don't forget to register the callbacks:

```python
ui.register_callback("undo_delete", undo_delete)
```

### Position Options

Show toasts in different positions:

```python
await ctx.show_toast("Top Left", position="top-left")
await ctx.show_toast("Top Center", position="top-center")
await ctx.show_toast("Top Right", position="top-right")
await ctx.show_toast("Bottom Left", position="bottom-left")
await ctx.show_toast("Bottom Center", position="bottom-center")
await ctx.show_toast("Bottom Right", position="bottom-right")
```

### Style Options

```python
# Inverted colors
await ctx.show_toast("Inverted", invert=True)

# Non-dismissible (can't click to dismiss)
await ctx.show_toast("Processing...", dismissible=False)
```

### Updating Toasts

Use `toast_id` to update existing toasts:

```python
# Show loading toast
await ctx.show_toast(
    "Uploading...",
    variant="loading",
    toast_id="upload"
)

# Later, update to success
await ctx.show_toast(
    "Upload complete!",
    variant="success",
    toast_id="upload"
)
```

## Theme Support

Toasts automatically follow the current page theme. Use the `ThemeSwitcher` component to allow users to toggle between light and dark modes - toast notifications will automatically update to match.

```python
from refast.components import ThemeSwitcher

# Add to your page layout
ThemeSwitcher()  # Toasts will follow this theme
```

## API Reference

### `ctx.show_toast()` Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | str | required | Main toast message |
| `variant` | str | "default" | "default", "success", "error", "warning", "info", "loading" |
| `description` | str | None | Secondary text below message |
| `duration` | int | None | Duration in ms (uses Toaster default if not set) |
| `position` | str | None | Override position for this toast |
| `dismissible` | bool | True | Whether clicking dismisses the toast |
| `close_button` | bool | None | Whether to show close button |
| `invert` | bool | False | Invert the color scheme |
| `action` | dict | None | Action button: `{"label": str, "callback_id": str}` |
| `cancel` | dict | None | Cancel button: `{"label": str, "callback_id": str}` |
| `toast_id` | str | None | Custom ID for updating/dismissing |
