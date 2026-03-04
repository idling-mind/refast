"""Base components — /docs/components/base."""

from refast.components import Container, Heading, Separator

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "Base Components"
PAGE_ROUTE = "/docs/components/base"


def render(ctx):
    """Render the base components page."""
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
## Introduction

The base components form the foundation of building a UI in Refast. They represent standard building blocks like `Container` (similar to a `<div>`), `Text` (like a `<span>` or `<p>`), and others, upon which more complex layouts and components are built.

Refast provides a consistent set of base components across the frontend and backend. 

### Common Properties

All base components (and most complex components) support a core set of common arguments:

- `id` (str, optional): A unique identifier for the component. When not provided, an auto-generated ID is used. Use a static ID when you need to target a component for specific updates via `ctx.replace` or `ctx.update_props`.
- `class_name` (str): Tailwind utility classes applied to the main wrapper element. This is the preferred way to handle styling.
- `style` (dict, optional): Inline styles to apply to the main wrapper. Prefer `class_name` over `style`.
- `children` (list | Component | str, optional): The nested content for the component.

### Container

`Container` is the most generic layout element, functioning like an HTML `<div>`.

```python
Container(
    class_name="p-4 border rounded-lg bg-muted/50",
    children=[
        Heading("Example Container", level=3),
        Text("This is content inside a container."),
    ]
)
```

### Fragment

`Fragment` is a wrapper that does not render a DOM element itself, identical to React's `<Fragment>` or `<>...</>`. It is useful when you need to group multiple sibling components together to satisfy a requirement for a single parent node (for example, returning multiple elements from a single python function without adding an extra layout `DIV`).

```python
Fragment(
    children=[
        Heading("First Heading", level=3),
        Heading("Second Heading", level=3),
    ]
)
```


### Slot

`Slot` acts as a placeholder or passthrough for children inside custom composite components. When building higher-level component compositions entirely in Python, you can use `Slot` to render whatever children were passed to the instance.

```python
from refast.components.base import Component
from refast.components.shadcn.layout import Container
from refast.components.base import Slot

class CustomHeader(Component):
    component_type = "CustomHeader"
    
    def render(self):
        return Container(
            class_name="flex items-center justify-between p-4 bg-primary text-primary-foreground",
            children=[
                Slot() # This will render whatever children are passed to CustomHeader
            ]
        ).render()
```
"""
