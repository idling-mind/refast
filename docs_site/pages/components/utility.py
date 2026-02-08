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
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Components in this section

- **Icon** — Lucide icon with ~100 curated icons
- **ThemeSwitcher** — Light/Dark/System toggle dropdown
- **ConnectionStatus** — WebSocket connection state indicator
- **Slot** — Dynamic content placeholder for targeted updates
- **Empty** — Renders nothing (useful for conditional rendering)
- **LoadingOverlay** — Full overlay with spinner
- **Kbd** — Keyboard shortcut display

---

### Icon

```python
Icon("settings", size=24, class_name="text-primary")
Icon("check", size=16, class_name="text-green-500")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str` | (positional) | Lucide icon name |
| `size` | `int` | `24` | Icon size in pixels |

Available icons include: `home`, `settings`, `search`, `user`, `check`, `x`, `plus`,
`minus`, `trash`, `edit`, `save`, `download`, `upload`, `folder`, `file`, `mail`,
`bell`, `calendar`, `clock`, `heart`, `star`, `eye`, `lock`, `unlock`, and many more.

---

### ThemeSwitcher

```python
from refast.components.shadcn import ThemeSwitcher

ThemeSwitcher()  # Renders a dropdown: Light | Dark | System
```

---

### ConnectionStatus

```python
ConnectionStatus()
```

Displays the current WebSocket connection state with a colored indicator:
- 🟢 Connected
- 🔴 Disconnected
- 🟡 Reconnecting

---

### Slot

A placeholder that can be filled later via targeted updates:

```python
Slot(id="dynamic-content", fallback=Text("Loading..."))
```

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
