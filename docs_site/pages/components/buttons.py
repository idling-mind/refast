"""Buttons & Controls — /docs/components/buttons."""

from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "Buttons & Controls"
PAGE_ROUTE = "/docs/components/buttons"


def render(ctx):
    """Render the buttons and controls reference page."""
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
## Overview

This section covers all press/toggle interaction components: standard buttons, icon
buttons, toggle buttons, toggle groups, switches, and sliders.

---

## Button

A standard clickable button styled with shadcn/ui conventions.

```python
from refast.components.shadcn.button import Button

# Default filled button
Button("Save", on_click=ctx.callback(handle_save))

# Destructive button with icon
Button("Delete", variant="destructive", icon="trash", on_click=ctx.callback(handle_delete))

# Ghost button with icon on the right
Button("Next", variant="ghost", icon="arrow-right", icon_position="right")

# Submit button
Button("Submit Form", size="lg", type="submit")

# Loading state (disabled + spinner)
Button("Processing…", loading=True)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(positional)* | Button text |
| `variant` | `"default" \| "secondary" \| "destructive" \| "outline" \| "ghost" \| "link"` | `"default"` | Visual style. `"default"` is the primary filled style. |
| `size` | `"sm" \| "md" \| "lg" \| "icon"` | `"md"` | Button dimensions. `"icon"` renders a square with no padding. |
| `icon` | `str \| None` | `None` | Lucide icon name (e.g. `"save"`, `"trash"`, `"settings"`). |
| `icon_position` | `"left" \| "right"` | `"left"` | Icon placement relative to the label. |
| `disabled` | `bool` | `False` | Prevents interaction. |
| `loading` | `bool` | `False` | Replaces icon with a spinner and disables the button. |
| `type` | `"button" \| "submit" \| "reset"` | `"button"` | HTML `<button>` type attribute. |
| `on_click` | `Callback \| None` | `None` | Server callback invoked on click. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### Variants

| Variant | Use case |
|---------|----------|
| `"default"` | Primary action — filled with `--primary` colour |
| `"secondary"` | Secondary action — muted filled style |
| `"destructive"` | Dangerous action — filled with `--destructive` colour |
| `"outline"` | Low-emphasis — bordered, transparent background |
| `"ghost"` | Invisible at rest — no border or background |
| `"link"` | Looks like a hyperlink — underline on hover |

---

## IconButton

A square button containing only an icon. Wraps `Button` internally with `size="icon"`.

```python
from refast.components.shadcn.button import IconButton

IconButton(icon="trash", aria_label="Delete item", on_click=ctx.callback(handle_delete))
IconButton(icon="settings", variant="outline", size="lg")
IconButton(icon="x", aria_label="Close dialog")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `icon` | `str` | *(required)* | Lucide icon name. |
| `variant` | `"default" \| "secondary" \| "destructive" \| "outline" \| "ghost"` | `"ghost"` | Visual style. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Controls icon and button size. |
| `disabled` | `bool` | `False` | Prevents interaction. |
| `aria_label` | `str \| None` | `None` | Accessible label — defaults to the icon name if omitted. |
| `on_click` | `Callback \| None` | `None` | Server callback invoked on click. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Toggle

A two-state button that visually indicates whether a feature is active. Think of bold/italic
toolbar buttons.

```python
from refast.components.shadcn.controls import Toggle

# Uncontrolled (internal state)
Toggle(label="Bold", icon="Bold", default_pressed=True)

# Controlled (Python holds the state)
Toggle(
    label="Italic",
    icon="Italic",
    pressed=state.italic,
    on_pressed_change=ctx.callback(handle_italic),
)

# Outline style, large size
Toggle(label="Underline", icon="Underline", variant="outline", size="lg")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | `""` | Visible text label. |
| `icon` | `str \| None` | `None` | Lucide icon name. |
| `pressed` | `bool \| None` | `None` | Controlled pressed state. Omit for uncontrolled. |
| `default_pressed` | `bool` | `False` | Initial pressed state (uncontrolled only). |
| `disabled` | `bool` | `False` | Prevents interaction. |
| `variant` | `"default" \| "outline"` | `"default"` | Visual style. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Button dimensions. |
| `on_pressed_change` | `Callback \| None` | `None` | Called with the new `bool` state when the toggle changes. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## ToggleGroup and ToggleGroupItem

A collection of `Toggle`-style items sharing a single selection model. Use `type="single"`
for exclusive selection (like text alignment) or `type="multiple"` for independent toggles
(like bold + italic simultaneously).

```python
from refast.components.shadcn.controls import ToggleGroup, ToggleGroupItem

# Single selection — only one item active at a time
ToggleGroup(
    type="single",
    default_value="center",
    on_value_change=ctx.callback(handle_alignment),
    children=[
        ToggleGroupItem(value="left",   icon="AlignLeft",   label="Left"),
        ToggleGroupItem(value="center", icon="AlignCenter", label="Center"),
        ToggleGroupItem(value="right",  icon="AlignRight",  label="Right"),
    ],
)

# Multiple selection — each item toggles independently
ToggleGroup(
    type="multiple",
    default_value={"bold": True, "italic": False, "underline": False},
    on_value_change=ctx.callback(handle_formatting),
    children=[
        ToggleGroupItem(value="bold",      icon="Bold",      label="Bold"),
        ToggleGroupItem(value="italic",    icon="Italic",    label="Italic"),
        ToggleGroupItem(value="underline", icon="Underline", label="Underline"),
    ],
)
```

**Callback value** — the `on_value_change` callback receives:

- `type="single"` → a single `str` (the selected item's `value`, or `""` if deselected)
- `type="multiple"` → a `dict[str, bool]` mapping each item `value` to its pressed state

### ToggleGroup props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `"single" \| "multiple"` | `"single"` | Selection behaviour. |
| `value` | `str \| list[str] \| dict[str, bool] \| None` | `None` | Controlled selected value(s). |
| `default_value` | `str \| list[str] \| dict[str, bool] \| None` | `None` | Initial selected value(s) (uncontrolled). |
| `disabled` | `bool` | `False` | Disables the entire group. |
| `variant` | `"default" \| "outline"` | `"default"` | Visual style applied to all items. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Size applied to all items. |
| `on_value_change` | `Callback \| None` | `None` | Called whenever the selection changes. |
| `children` | `list[ToggleGroupItem]` | `[]` | The items inside the group. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### ToggleGroupItem props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str` | *(required)* | Unique identifier for this item within the group. |
| `label` | `str` | `""` | Visible text label. |
| `icon` | `str \| None` | `None` | Lucide icon name. |
| `disabled` | `bool` | `False` | Disables this item only. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Switch

An on/off toggle rendered as a sliding pill — commonly used for boolean settings.

```python
from refast.components.shadcn.controls import Switch

# Uncontrolled
Switch(default_checked=True, name="notifications")

# Controlled
Switch(
    checked=state.dark_mode,
    on_change=ctx.callback(handle_dark_mode),
    name="dark_mode",
)

# Disabled
Switch(checked=True, disabled=True)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `checked` | `bool \| None` | `None` | Controlled checked state. Omit for uncontrolled. |
| `default_checked` | `bool` | `False` | Initial checked state (uncontrolled only). |
| `disabled` | `bool` | `False` | Prevents interaction. |
| `name` | `str \| None` | `None` | HTML `name` attribute for form submission. |
| `on_change` | `Callback \| None` | `None` | Called with the new `bool` state when toggled. The callback key in the serialized tree is `on_checked_change`. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Slider

A draggable range slider for selecting a numeric value or range.

```python
from refast.components.shadcn.controls import Slider

# Basic volume control
Slider(
    label="Volume",
    value=[75],
    min=0,
    max=100,
    step=1,
    on_value_change=ctx.callback(handle_volume),
)

# Range slider (two thumbs)
Slider(
    label="Price range",
    value=[20, 80],
    min=0,
    max=200,
    step=5,
    on_value_change=ctx.callback(handle_price_range),
)

# Vertical orientation with description
Slider(
    label="Brightness",
    description="Adjust display brightness",
    value=[50],
    orientation="vertical",
    on_value_commit=ctx.callback(handle_brightness_commit),
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `list[float] \| None` | `None` | Controlled value(s). One element = single thumb; two = range. |
| `default_value` | `list[float]` | `[0]` | Initial value(s) (uncontrolled). |
| `min` | `float` | `0` | Minimum value. |
| `max` | `float` | `100` | Maximum value. |
| `step` | `float` | `1` | Step increment. |
| `disabled` | `bool` | `False` | Prevents interaction. |
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Track orientation. |
| `label` | `str \| None` | `None` | Label displayed above the slider. |
| `description` | `str \| None` | `None` | Help text displayed below the label. |
| `required` | `bool` | `False` | Shows a required asterisk next to the label. |
| `error` | `str \| None` | `None` | Error message displayed below the slider. |
| `on_value_change` | `Callback \| None` | `None` | Called continuously as the thumb moves. Receives `list[float]`. |
| `on_value_commit` | `Callback \| None` | `None` | Called when the user releases the thumb. Receives `list[float]`. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |
"""
