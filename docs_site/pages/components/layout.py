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
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Components in this section

- **Container** — A `<div>` wrapper, the most fundamental layout element
- **Flex** — Flexbox container with direction, alignment, gap
- **Row** — Shortcut for `Flex(direction="row")`
- **Column** — Shortcut for `Flex(direction="column")`
- **Grid** — CSS Grid with configurable columns and gap
- **Center** — Centers its children both horizontally and vertically
- **Box** — Generic container
- **Stack** — Vertical stack with gap
- **Separator** — Horizontal or vertical divider line
- **AspectRatio** — Maintains a specific aspect ratio
- **ScrollArea** / **ScrollBar** — Custom scrollable area
- **ResizablePanelGroup** / **ResizablePanel** / **ResizableHandle** — Resizable split panes

---

### Container

The basic building block. Renders a `<div>`.

```python
Container(
    id="main",
    class_name="max-w-4xl mx-auto p-6",
    children=[...],
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `str \| None` | `None` | Unique ID for targeted updates |
| `class_name` | `str` | `""` | Tailwind CSS classes |
| `children` | `list` | `[]` | Child components |
| `style` | `dict \| None` | `None` | Dynamic CSS properties |

---

### Flex

```python
Flex(
    direction="row",
    align="center",
    justify="between",
    gap=4,
    wrap="wrap",
    children=[...],
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `direction` | `"row" \| "column"` | `"row"` | Flex direction |
| `align` | `str` | `"stretch"` | Align items |
| `justify` | `str` | `"start"` | Justify content |
| `gap` | `str \| int` | `"0"` | Gap between children |
| `wrap` | `str` | `"nowrap"` | Flex wrap |

---

### Grid

```python
Grid(columns=3, gap=4, children=[...])
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | `int` | `1` | Number of columns |
| `gap` | `str \| int` | `"4"` | Gap between grid items |

---

*Each component above should have a complete props table and a live example.*
*See `AGENT_INSTRUCTIONS.md` for detailed requirements.*
"""
