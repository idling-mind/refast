"""Utility Components — /docs/components/utility."""

from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "Utility Components"
PAGE_ROUTE = "/docs/components/utility"


def render(ctx):
    """Render the utility components reference page."""
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

Utility components cover visual helpers and interactive primitives that are
not strictly layout but still broadly reusable: separators, aspect-ratio
boxes, scrollable areas, collapsibles, carousels, resizable split-panes,
and UI feedback helpers.

---

## Separator

A thin horizontal or vertical divider line built on Radix UI Separator.

```python
from refast.components.shadcn import Separator

Separator()                          # horizontal (default)
Separator(orientation="vertical")    # vertical
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Direction of the line |
| `decorative` | `bool` | `True` | Hides from accessibility tree when `True` |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## AspectRatio

Constrains its children inside a box that maintains a fixed width-to-height
ratio, using the Radix UI AspectRatio primitive.

```python
from refast.components.shadcn import AspectRatio

AspectRatio(
    ratio=16 / 9,
    children=[Image(src="/banner.jpg", alt="Banner")],
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `ratio` | `float` | `1.0` | Width ÷ height, e.g. `16/9`, `4/3`, `1.0` |
| `children` | `list \| Component \| None` | `None` | Content to constrain |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## ScrollArea / ScrollBar

A scrollable area with custom styled scrollbars.  `ScrollArea` automatically
includes both vertical and horizontal scrollbars; `ScrollBar` is available
for advanced placement scenarios.

```python
from refast.components.shadcn import ScrollArea

ScrollArea(
    class_name="h-72 w-64",
    children=[Column(children=[Text(f"Line {i}") for i in range(50)])],
)
```

### ScrollArea props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Scrollable content |
| `type` | `"auto" \| "always" \| "scroll" \| "hover"` | `"hover"` | When the scrollbar is visible |
| `scroll_hide_delay` | `int` | `600` | ms before scrollbar hides (hover/scroll modes) |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### ScrollBar props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | Scrollbar axis |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## Collapsible / CollapsibleTrigger / CollapsibleContent

An animated expand/collapse section built on Radix UI Collapsible.

```python
from refast.components.shadcn import (
    Collapsible,
    CollapsibleTrigger,
    CollapsibleContent,
)

Collapsible(
    default_open=False,
    children=[
        CollapsibleTrigger(Button("Toggle details")),
        CollapsibleContent(
            children=[Paragraph("This section can be collapsed.")],
        ),
    ],
)
```

### Collapsible props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `bool \| None` | `None` | Controlled open state |
| `default_open` | `bool` | `False` | Initial state (uncontrolled) |
| `on_open_change` | `Callback \| None` | `None` | Fired on state change |
| `disabled` | `bool` | `False` | Prevents toggling |
| `children` | `list \| Component \| None` | `None` | Trigger + content |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### CollapsibleTrigger props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Interactive trigger element |
| `as_child` | `bool` | `True` | Merge props onto child (Radix asChild pattern) |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### CollapsibleContent props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Hidden/shown content |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## Carousel / CarouselContent / CarouselItem / CarouselPrevious / CarouselNext

A swipeable, keyboard-navigable carousel powered by Embla Carousel.

```python
from refast.components.shadcn import (
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselPrevious,
    CarouselNext,
)

Carousel(
    opts={"loop": True},
    children=[
        CarouselContent(
            children=[
                CarouselItem(children=[Card(title=f"Slide {i}")]) for i in range(5)
            ],
        ),
        CarouselPrevious(),
        CarouselNext(),
    ],
)
```

### Carousel props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Content + nav buttons |
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Scroll axis |
| `opts` | `dict \| None` | `None` | Embla options (e.g. `{"loop": True}`) |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### CarouselContent / CarouselItem / CarouselPrevious / CarouselNext

All four accept `id` and `class_name`.  `CarouselContent` and `CarouselItem`
also accept `children`.

---

## ResizablePanelGroup / ResizablePanel / ResizableHandle

Drag-to-resize split panels powered by `react-resizable-panels`.

```python
from refast.components.shadcn import (
    ResizablePanelGroup,
    ResizablePanel,
    ResizableHandle,
)

ResizablePanelGroup(
    direction="horizontal",
    children=[
        ResizablePanel(default_size=30, min_size=20, children=[sidebar]),
        ResizableHandle(with_handle=True),
        ResizablePanel(default_size=70, children=[main_content]),
    ],
)
```

### ResizablePanelGroup props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `direction` | `"horizontal" \| "vertical"` | `"horizontal"` | Split orientation |
| `children` | `list \| Component \| None` | `None` | Panels and handles |
| `on_layout` | `Callback \| None` | `None` | Fired with size array on resize |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### ResizablePanel props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `default_size` | `float` | `50` | Initial size as % of group |
| `min_size` | `float \| None` | `None` | Minimum size % |
| `max_size` | `float \| None` | `None` | Maximum size % |
| `collapsible` | `bool` | `False` | Allow full collapse |
| `collapsed_size` | `float \| None` | `None` | Size % when collapsed |
| `on_collapse` | `Callback \| None` | `None` | Fired on collapse |
| `on_expand` | `Callback \| None` | `None` | Fired on expand |
| `on_resize` | `Callback \| None` | `None` | Fired on every resize |
| `children` | `list \| Component \| None` | `None` | Panel content |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### ResizableHandle props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `with_handle` | `bool` | `False` | Show a grip icon on the handle bar |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## ThemeSwitcher

A button (toggle mode) or dropdown (dropdown mode) for switching between
light, dark, and system themes.  Persists preference to `localStorage`.

```python
from refast.components.shadcn import ThemeSwitcher

ThemeSwitcher()                                     # simple toggle

ThemeSwitcher(
    mode="dropdown",
    default_theme="dark",
    show_system_option=True,
    storage_key="my-app-theme",
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `default_theme` | `"light" \| "dark" \| "system"` | `"system"` | Theme used if no preference is stored |
| `storage_key` | `str` | `"refast-theme"` | `localStorage` key for persistence |
| `show_system_option` | `bool` | `True` | Show "System" option in dropdown mode |
| `mode` | `"toggle" \| "dropdown"` | `"toggle"` | Display mode |
| `on_change` | `Callback \| None` | `None` | Fired with the new theme string |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## Toaster

Renders the Sonner toast container.  Place this **once** in your app layout.
Trigger toasts from Python with `ctx.toast(...)`.

```python
from refast.components.shadcn import Toaster

# In your root layout:
Container(children=[..., Toaster(position="bottom-right", rich_colors=True)])
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `position` | `"top-left" \| "top-center" \| "top-right" \| "bottom-left" \| "bottom-center" \| "bottom-right"` | `"bottom-right"` | Where toasts appear |
| `expand` | `bool` | `False` | Expand toasts on hover by default |
| `duration` | `int` | `4000` | Default duration in ms |
| `visible_toasts` | `int` | `3` | Maximum simultaneous toasts |
| `close_button` | `bool` | `False` | Show close button on each toast |
| `rich_colors` | `bool` | `False` | Coloured backgrounds per variant |
| `theme` | `"light" \| "dark" \| "system"` | `"system"` | Toast colour theme |
| `offset` | `str \| int \| None` | `None` | Screen-edge offset (px or CSS value) |
| `gap` | `int` | `14` | Gap between stacked toasts (px) |
| `dir` | `"ltr" \| "rtl" \| "auto"` | `"auto"` | Text direction |
| `invert` | `bool` | `False` | Invert default colours |

---

## Empty

A zero-content placeholder that renders nothing.  Useful for conditional
rendering — swap it out via a targeted update.

```python
from refast.components.shadcn import Empty

Empty(
    icon="Inbox",
    title="No messages",
    description="You have no messages yet.",
    action=Button("Send one"),
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `icon` | `str \| None` | `None` | Lucide icon name shown above the title |
| `title` | `str` | `""` | Heading text |
| `description` | `str` | `""` | Sub-text |
| `action` | `Component \| None` | `None` | Optional CTA button |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## Kbd

Renders a keyboard key in a styled `<kbd>` element.

```python
from refast.components.shadcn import Kbd

Row(children=["Press ", Kbd("⌘"), " + ", Kbd("K"), " to open the palette."])
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `key` | `str` | (positional) | Key label to display |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## LoadingOverlay

Full-screen overlay with a spinner, displayed over existing content.

```python
from refast.components.shadcn import LoadingOverlay

LoadingOverlay(loading=is_saving, text="Saving…")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `loading` | `bool` | `False` | Whether the overlay is visible |
| `text` | `str` | `"Loading..."` | Message shown beside the spinner |
| `blur` | `bool` | `True` | Apply a blur effect to the content behind |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |
"""
