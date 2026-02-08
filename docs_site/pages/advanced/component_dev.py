"""Building Components — /docs/advanced/component-dev."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Building Components"
PAGE_ROUTE = "/docs/advanced/component-dev"


def render(ctx):
    """Render the component development guide page."""
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
> Adapt from `docs/COMPONENT_DEVELOPMENT.md` and `docs/NAMING_CONVENTIONS.md`.

## Overview

You can create custom components to extend Refast's UI library. A component has two
parts: a **Python class** (backend) and a **React component** (frontend).

## Python Side

Subclass `Component` and implement `render()`:

```python
from refast.components.base import Component

class MyWidget(Component):
    component_type: str = "MyWidget"

    def __init__(self, title: str, value: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.value = value

    def render(self):
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "value": self.value,
                "className": self.class_name,
            },
            "children": self._render_children(),
        }
```

## React Side

Register a React component in the ComponentRegistry:

```typescript
import { ComponentRegistry } from './registry';

function MyWidget({ title, value, className }: MyWidgetProps) {
    return (
        <div className={className}>
            <h3>{title}</h3>
            <span>{value}</span>
        </div>
    );
}

ComponentRegistry.register('MyWidget', MyWidget);
```

## Naming Conventions

| Python | JSON Wire | React |
|--------|-----------|-------|
| `snake_case` | `camelCase` | `camelCase` |
| `class_name` | `className` | `className` |
| `on_click` | `onClick` | `onClick` |
| `data_key` | `dataKey` | `dataKey` |

The conversion is automatic — write Python in `snake_case` and the frontend receives `camelCase`.

## Registration

Components must be registered in the `ComponentRegistry` to be rendered by the frontend's
`ComponentRenderer`. Use `ComponentRegistry.register(name, component)`.

## Next Steps

- [Building Extensions](/docs/advanced/extension-dev) — Package components as extensions
- [Naming Conventions](/docs/advanced/styling) — Full naming reference
"""
