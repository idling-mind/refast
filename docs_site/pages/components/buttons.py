"""Buttons & Actions — /docs/components/buttons."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Buttons & Actions"
PAGE_ROUTE = "/docs/components/buttons"


def render(ctx):
    """Render the buttons reference page."""
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

- **Button** — Standard clickable button with variants and sizes
- **IconButton** — Icon-only button
- **Toggle** — Toggle button with pressed/unpressed state
- **ToggleGroup** / **ToggleGroupItem** — Group of toggle buttons
- **DropdownMenu** and sub-components — Context menu triggered by a button

---

### Button

```python
Button("Click Me", variant="default", size="default", on_click=ctx.callback(handle))
Button("Delete", variant="destructive", icon="trash")
Button("Settings", variant="ghost", icon="settings", disabled=True)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | (positional) | Button text |
| `variant` | `"default" \| "secondary" \| "destructive" \| "outline" \| "ghost" \| "link"` | `"default"` | Visual variant |
| `size` | `"default" \| "sm" \| "lg" \| "icon"` | `"default"` | Button size |
| `icon` | `str \| None` | `None` | Lucide icon name |
| `disabled` | `bool` | `False` | Disabled state |
| `on_click` | `Callback \| None` | `None` | Click handler |

---

### DropdownMenu

```python
DropdownMenu(children=[
    DropdownMenuTrigger(children=[Button("Options", variant="outline")]),
    DropdownMenuContent(children=[
        DropdownMenuLabel("Actions"),
        DropdownMenuSeparator(),
        DropdownMenuItem("Edit", icon="edit", on_click=ctx.callback(edit)),
        DropdownMenuItem("Delete", icon="trash", on_click=ctx.callback(delete)),
    ]),
])
```

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
