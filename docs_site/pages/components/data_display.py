"""Data Display — /docs/components/data-display."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Data Display"
PAGE_ROUTE = "/docs/components/data-display"


def render(ctx):
    """Render the data display reference page."""
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

This section covers all data-display components: primitive HTML table building
blocks, the high-level `DataTable`, `Tabs`, `Accordion`, `Badge`, `Avatar`,
`Image`, `List`, `Tooltip`, and the `HoverCard` family.

---

## Table primitives

Use the primitive table family when you need full layout control — custom cell
rendering, row selection, or complex action columns. For a turnkey table with
sorting, filtering, and pagination see [DataTable](#datatable).

```python
from refast.components.shadcn.data_display import (
    Table, TableHeader, TableBody,
    TableRow, TableHead, TableCell,
)

Table(
    children=[
        TableHeader(children=[
            TableRow(children=[
                TableHead(children=["Name"]),
                TableHead(children=["Email"]),
                TableHead(children=["Role"]),
            ]),
        ]),
        TableBody(children=[
            TableRow(children=[
                TableCell(children=["Alice"]),
                TableCell(children=["alice@example.com"]),
                TableCell(children=["Admin"]),
            ]),
            TableRow(children=[
                TableCell(children=["Bob"]),
                TableCell(children=["bob@example.com"]),
                TableCell(children=["Editor"]),
            ]),
        ]),
    ]
)
```

### Table

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `TableHeader` and `TableBody` components. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### TableHeader

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `TableRow` components for the header. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### TableBody

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `TableRow` components for the body. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### TableRow

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `TableHead` or `TableCell` components. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### TableHead

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Column header label — typically a string. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### TableCell

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Cell content. |
| `col_span` | `int \| None` | `None` | Number of columns this cell spans. |
| `row_span` | `int \| None` | `None` | Number of rows this cell spans. |
| `class_name` | `str` | `""` | Additional CSS class names. |

---

## DataTable

A high-level data table with built-in client-side sorting, filtering, and
pagination. Provide column definitions and a flat list of row dicts.

```python
from refast.components.shadcn.data_display import DataTable

async def on_row_click(ctx):
    row = ctx.event_data          # full row dict
    await ctx.show_toast(f"Clicked: {row['name']}")

async def on_sort(ctx):
    ctx.state.set("sort", ctx.event_data)
    await ctx.refresh()

async def on_page(ctx):
    ctx.state.set("page", ctx.event_data.get("page", 1))
    await ctx.refresh()

DataTable(
    columns=[
        {"key": "id",     "header": "#",      "width": "60px", "align": "right"},
        {"key": "name",   "header": "Name",   "sortable": True},
        {"key": "email",  "header": "Email",  "sortable": True},
        {"key": "role",   "header": "Role",   "align": "center"},
        {"key": "status", "header": "Status", "sortable": True},
    ],
    data=[
        {"id": 1, "name": "Alice", "email": "alice@example.com",
         "role": "Admin", "status": "active"},
        {"id": 2, "name": "Bob",   "email": "bob@example.com",
         "role": "Editor", "status": "inactive"},
    ],
    sortable=True,
    filterable=True,
    paginated=True,
    page_size=10,
    on_row_click=ctx.callback(on_row_click),
    on_sort_change=ctx.callback(on_sort),
    on_page_change=ctx.callback(on_page),
    empty_message="No users found.",
)
```

### Column definition format

Each entry in `columns` is a `dict`:

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `key` | `str` | ✓ | Field name used to look up values in each row. |
| `header` | `str` | ✓ | Column header label. |
| `sortable` | `bool` | | Per-column sort override. Falls back to the component-level `sortable` flag. |
| `width` | `str` | | CSS width, e.g. `"200px"`, `"20%"`. |
| `align` | `str` | | `"left"` (default), `"center"`, or `"right"`. |

### DataTable props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | `list[dict]` | *(required)* | Column definitions (see above). |
| `data` | `list[dict]` | *(required)* | Row data. Each dict should contain all keys referenced by `columns`. |
| `sortable` | `bool` | `True` | Enable clicking column headers to sort. |
| `filterable` | `bool` | `True` | Show a text filter input above the table. |
| `paginated` | `bool` | `True` | Show pagination controls below the table. |
| `page_size` | `int` | `10` | Rows per page. |
| `loading` | `bool` | `False` | Display a loading overlay. |
| `empty_message` | `str` | `"No data available"` | Shown when `data` is empty or no rows match. |
| `current_page` | `int \| None` | `None` | Controlled current page (1-based). |
| `on_row_click` | `Callback \| None` | `None` | Fired on row click. `ctx.event_data` is the row dict. |
| `on_sort_change` | `Callback \| None` | `None` | Fired on sort change. `ctx.event_data` is `{"key": ..., "direction": "asc"\|"desc"}` or `None`. |
| `on_filter_change` | `Callback \| None` | `None` | Fired when filter input changes. `ctx.event_data` is `{"value": ...}`. |
| `on_page_change` | `Callback \| None` | `None` | Fired on page change. `ctx.event_data` is `{"page": <n>}`. |
| `class_name` | `str` | `""` | Additional CSS class names. |

---

## Tabs / TabItem

A tabbed interface that switches between panels. Each `TabItem` defines one
tab button and its associated content panel.

```python
from refast.components.shadcn.data_display import Tabs, TabItem
from refast.components.base import Text

Tabs(
    default_value="overview",
    children=[
        TabItem(
            value="overview",
            label="Overview",
            children=[Text("Overview content here.")],
        ),
        TabItem(
            value="settings",
            label="Settings",
            children=[Text("Settings content here.")],
        ),
        TabItem(
            value="billing",
            label="Billing",
            disabled=True,
            children=[Text("Billing unavailable.")],
        ),
    ],
)
```

### Tabs props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list[TabItem]` | `[]` | `TabItem` components. |
| `default_value` | `str \| None` | `None` | Value of the initially active tab (uncontrolled). |
| `value` | `str \| None` | `None` | Controlled active tab. Pair with `on_value_change`. |
| `on_value_change` | `Callback \| None` | `None` | Called when the active tab changes. `ctx.event_data` is the new tab value. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### TabItem props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str` | *(required)* | Unique identifier for this panel within the `Tabs` group. |
| `label` | `str` | *(required)* | Text shown on the tab trigger button. |
| `children` | `list` | `[]` | Panel content shown when this tab is active. |
| `disabled` | `bool` | `False` | Grays out and disables the tab button. |
| `class_name` | `str` | `""` | Additional CSS class names. |

---

## Accordion / AccordionItem / AccordionTrigger / AccordionContent

Expandable/collapsible content sections. `type="single"` allows at most one
open item; `type="multiple"` allows any number.

```python
from refast.components.shadcn.data_display import (
    Accordion, AccordionItem, AccordionTrigger, AccordionContent,
)
from refast.components.base import Text

Accordion(
    type="single",
    collapsible=True,
    default_value="item-1",
    children=[
        AccordionItem(
            value="item-1",
            children=[
                AccordionTrigger(children=["Is it accessible?"]),
                AccordionContent(children=[
                    Text("Yes. It adheres to the WAI-ARIA spec.")
                ]),
            ],
        ),
        AccordionItem(
            value="item-2",
            children=[
                AccordionTrigger(children=["Is it styled?"]),
                AccordionContent(children=[
                    Text("Yes. It ships with default shadcn/ui styles.")
                ]),
            ],
        ),
    ],
)
```

### Accordion props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list[AccordionItem]` | `[]` | `AccordionItem` components. |
| `type` | `"single" \| "multiple"` | `"single"` | Selection behaviour. `"single"` opens at most one section. |
| `collapsible` | `bool` | `True` | If `True` and `type="single"`, allows closing all items. |
| `default_value` | `str \| list[str] \| None` | `None` | Initially open item(s). |
| `on_value_change` | `Callback \| None` | `None` | Called when open items change. `ctx.event_data` is the new value. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### AccordionItem props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str` | *(required)* | Unique identifier used by the parent `Accordion` to track state. |
| `children` | `list` | `[]` | One `AccordionTrigger` and one `AccordionContent`. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### AccordionTrigger props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Trigger label — typically a string. |
| `class_name` | `str` | `""` | Additional CSS class names on the trigger button. |

### AccordionContent props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Content revealed when the item is open. |
| `class_name` | `str` | `""` | Additional CSS class names on the content wrapper. |

---

## Avatar

Circular user avatar. Shows an image when `src` is provided; falls back to
`fallback` initials (or the first character of `alt`) when the image is
absent or fails to load.

```python
from refast.components.shadcn.data_display import Avatar

# Image avatar
Avatar(src="/avatars/alice.jpg", alt="Alice", size="md")

# Initials-only avatar
Avatar(fallback="JD", size="lg")

# Small avatar with explicit fallback
Avatar(src="/avatars/bob.jpg", alt="Bob", fallback="B", size="sm")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `src` | `str \| None` | `None` | URL of the user image. Omit to show initials only. |
| `alt` | `str` | `""` | Alternative text; also used to derive the fallback initial. |
| `fallback` | `str \| None` | `None` | Short string (1–2 chars) shown when the image is unavailable. |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Avatar diameter: `sm`=32 px, `md`=40 px, `lg`=48 px. |
| `class_name` | `str` | `""` | Additional CSS class names. |

---

## Badge

Small inline label for statuses, counts, or categories.

```python
from refast.components.shadcn.data_display import Badge

Badge(children=["New"])
Badge(children=["Error"], variant="destructive")
Badge(children=["Active"], variant="success")
Badge(children=["Pending"], variant="warning")
Badge(children=["Draft"], variant="outline")
Badge(children=["Beta"], variant="secondary")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Badge content — typically a short string. |
| `variant` | `"default" \| "secondary" \| "destructive" \| "outline" \| "success" \| "warning"` | `"default"` | Visual style. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### Variants

| Variant | Use case |
|---------|----------|
| `"default"` | Default primary style |
| `"secondary"` | Muted secondary style |
| `"destructive"` | Error / danger |
| `"outline"` | Bordered, no fill |
| `"success"` | Positive / active |
| `"warning"` | Caution / pending |

---

## Image

Responsive image with optional loading skeleton and fallback URL.

```python
from refast.components.shadcn.data_display import Image

# Basic image
Image(src="/images/photo.jpg", alt="A mountain landscape", width=800, height=600)

# With loading skeleton and fallback
Image(
    src="/images/dynamic.jpg",
    alt="Dynamic content",
    width="100%",
    object_fit="contain",
    loading=True,
    fallback_src="/images/placeholder.jpg",
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `src` | `str` | *(required)* | Image source URL. |
| `alt` | `str` | `""` | Alternative text. |
| `width` | `int \| str \| None` | `None` | Width in pixels (int) or CSS string. |
| `height` | `int \| str \| None` | `None` | Height in pixels (int) or CSS string. |
| `object_fit` | `"contain" \| "cover" \| "fill" \| "none" \| "scale-down"` | `"cover"` | CSS `object-fit` value. |
| `loading` | `bool` | `False` | Show a loading skeleton while the image loads. |
| `fallback_src` | `str \| None` | `None` | Fallback URL if the main image fails. |
| `class_name` | `str` | `""` | Additional CSS class names. |

---

## List

Ordered (`<ol>`) or unordered (`<ul>`) list. Children may be plain strings or
`ListItem` components.

```python
from refast.components.shadcn.data_display import List

# Unordered (bulleted)
List(children=["Apples", "Bananas", "Cherries"])

# Ordered (numbered)
List(ordered=True, children=["First step", "Second step", "Third step"])
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | List items — strings or `ListItem` components. |
| `ordered` | `bool` | `False` | If `True`, renders `<ol>` (numbered); otherwise `<ul>` (bulleted). |
| `class_name` | `str` | `""` | Additional CSS class names. |

---

## Tooltip

Floating plain-text tooltip that appears on hover above (or beside) a trigger
element. Wrap any single component with `Tooltip` to add hover text.

```python
from refast.components.shadcn.data_display import Tooltip
from refast.components.shadcn.button import Button, IconButton

# Tooltip on a button
Tooltip(
    content="This action cannot be undone.",
    children=[Button("Delete", variant="destructive")],
)

# Tooltip on an icon button, positioned to the right
Tooltip(
    content="Home page",
    side="right",
    side_offset=8,
    children=[IconButton(icon="home")],
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `str` | *(required)* | Plain-text tooltip message. |
| `children` | `list` | `[]` | The trigger element(s). Typically a single component. |
| `side` | `"top" \| "right" \| "bottom" \| "left"` | `"top"` | Preferred side of the trigger to show the tooltip. |
| `side_offset` | `int \| None` | `None` | Pixel gap between trigger and tooltip (defaults to `4` in the frontend). |
| `class_name` | `str` | `""` | Additional CSS class names on the tooltip content. |

---

## HoverCard / HoverCardTrigger / HoverCardContent

A rich preview card that appears on hover. Useful for profile previews or
link previews. The three components are used together.

```python
from refast.components.shadcn.overlay import (
    HoverCard, HoverCardTrigger, HoverCardContent,
)
from refast.components.shadcn.data_display import Avatar
from refast.components.shadcn.link import Link
from refast.components.base import Container, Text

HoverCard(
    open_delay=500,
    children=[
        HoverCardTrigger(
            children=[Link("@shadcn", href="https://twitter.com/shadcn")],
        ),
        HoverCardContent(
            side="bottom",
            children=[
                Container(class_name="flex gap-3 items-center", children=[
                    Avatar(src="/avatars/shadcn.png", alt="@shadcn", fallback="SC"),
                    Container(children=[
                        Text("@shadcn", class_name="font-semibold"),
                        Text("Creator of shadcn/ui", class_name="text-sm text-muted-foreground"),
                    ]),
                ]),
            ],
        ),
    ],
)
```

### HoverCard props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | One `HoverCardTrigger` and one `HoverCardContent`. |
| `open` | `bool \| None` | `None` | Controlled open state. Omit for uncontrolled. |
| `default_open` | `bool` | `False` | Initial open state (uncontrolled). |
| `open_delay` | `int` | `700` | Milliseconds before the card opens on hover. |
| `close_delay` | `int` | `300` | Milliseconds before the card closes after hover ends. |
| `on_open_change` | `Callback \| None` | `None` | Called when the open state changes. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### HoverCardTrigger props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | The element that activates the hover card on mouse-over. |
| `as_child` | `bool` | `False` | Merge props onto the first child instead of wrapping with a `<span>`. |
| `class_name` | `str` | `""` | Additional CSS class names. |

### HoverCardContent props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Content displayed inside the floating card. |
| `side` | `"top" \| "right" \| "bottom" \| "left"` | `"bottom"` | Preferred side relative to the trigger. |
| `side_offset` | `int` | `4` | Pixel gap between trigger and card. |
| `align` | `"start" \| "center" \| "end"` | `"center"` | Alignment of the card relative to the trigger. |
| `class_name` | `str` | `""` | Additional CSS class names. |
"""

## Components in this section

- **Table** / **TableHeader** / **TableBody** / **TableRow** / **TableHead** / **TableCell** — HTML table primitives
- **DataTable** — Higher-level data table component
- **Avatar** — User avatar with image or initials
- **Image** — Responsive image component
- **List** — Ordered or unordered list
- **Calendar** — Date display/selection calendar
- **Progress** — Progress bar
- **Skeleton** — Loading placeholder
- **Carousel** / **CarouselContent** / **CarouselItem** / **CarouselPrevious** / **CarouselNext** — Image/content carousel
- **Accordion** / **AccordionItem** / **AccordionTrigger** / **AccordionContent** — Expandable content sections
- **Tabs** / **TabItem** — Tabbed content switcher
- **HoverCard** / **HoverCardTrigger** / **HoverCardContent** — Card shown on hover
- **Tooltip** — Hover tooltip

---

### Table

```python
Table(children=[
    TableHeader(children=[
        TableRow(children=[
            TableHead("Name"),
            TableHead("Email"),
        ]),
    ]),
    TableBody(children=[
        TableRow(children=[
            TableCell("Alice"),
            TableCell("alice@example.com"),
        ]),
    ]),
])
```

---

### Tabs

```python
Tabs(
    default_value="tab1",
    children=[
        TabItem(label="Overview", value="tab1", children=[
            Text("Overview content"),
        ]),
        TabItem(label="Settings", value="tab2", children=[
            Text("Settings content"),
        ]),
    ],
)
```

---

### Accordion

```python
Accordion(
    type="single",
    collapsible=True,
    children=[
        AccordionItem(value="item1", children=[
            AccordionTrigger("Section 1"),
            AccordionContent(children=[Text("Content for section 1")]),
        ]),
    ],
)
```

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
