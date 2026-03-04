"""Layout Components — /docs/components/layout."""

from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "Layout Components"
PAGE_ROUTE = "/docs/components/layout"


def render(ctx):
    """Render the layout components reference page."""
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

Layout components provide flexbox and CSS Grid primitives for building page
structure.  All components accept `id`, `class_name`, and arbitrary extra
props forwarded to the underlying DOM element.

---

## Row

Horizontal flex container (`flex flex-row`).

```python
from refast.components.shadcn import Row

Row(
    children=[Button("Save"), Button("Cancel", variant="outline")],
    justify="end",
    align="center",
    gap=2,
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Child components |
| `justify` | `"start" \| "end" \| "center" \| "between" \| "around" \| "evenly"` | `"start"` | `justify-content` |
| `align` | `"start" \| "end" \| "center" \| "stretch" \| "baseline"` | `"start"` | `align-items` |
| `gap` | `int` | `2` | Gap between children (Tailwind spacing unit × 0.25 rem) |
| `wrap` | `bool` | `False` | Whether children wrap onto multiple lines |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## Column

Vertical flex container (`flex flex-col`).

```python
from refast.components.shadcn import Column

Column(
    children=[Heading("Title", level=2), Paragraph("Body text")],
    gap=4,
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Child components |
| `justify` | `"start" \| "end" \| "center" \| "between" \| "around" \| "evenly"` | `"start"` | `justify-content` |
| `align` | `"start" \| "end" \| "center" \| "stretch" \| "baseline"` | `"stretch"` | `align-items` |
| `gap` | `int` | `2` | Gap between children (Tailwind spacing unit × 0.25 rem) |
| `wrap` | `bool` | `False` | Whether children wrap |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## Grid

CSS Grid container.

```python
from refast.components.shadcn import Grid

Grid(
    columns=3,
    gap=4,
    children=[Card(title=f"Item {i}") for i in range(6)],
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Grid cells |
| `columns` | `int \| str` | `1` | Number of equal columns, or a `gridTemplateColumns` CSS string |
| `rows` | `int \| str \| None` | `None` | Number of equal rows, or a `gridTemplateRows` CSS string |
| `gap` | `int` | `4` | Gap between cells (Tailwind spacing unit) |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## Flex

Generic flexbox container with full directional control.  For most cases
prefer the more ergonomic `Row` or `Column` shortcuts.

```python
from refast.components.shadcn import Flex

Flex(
    direction="column",
    justify="between",
    align="center",
    gap=4,
    wrap=True,
    children=[...],
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Child components |
| `direction` | `"row" \| "column" \| "row-reverse" \| "column-reverse"` | `"row"` | Flex direction |
| `justify` | `"start" \| "end" \| "center" \| "between" \| "around" \| "evenly"` | `"start"` | `justify-content` |
| `align` | `"start" \| "end" \| "center" \| "stretch" \| "baseline"` | `"stretch"` | `align-items` |
| `wrap` | `bool` | `False` | Whether children wrap |
| `gap` | `int` | `2` | Gap (Tailwind spacing unit) |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

---

## Center

Centers its children both horizontally and vertically inside a
`flex items-center justify-center` wrapper.

```python
from refast.components.shadcn import Center

Center(
    class_name="h-screen",
    children=[Heading("Welcome", level=1)],
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list \| Component \| None` | `None` | Content to center |
| `id` | `str \| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |
"""
