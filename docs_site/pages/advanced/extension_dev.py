"""Building Extensions — /docs/advanced/extension-dev."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Building Extensions"
PAGE_ROUTE = "/docs/advanced/extension-dev"


def render(ctx):
    """Render the extension development guide page."""
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
> Adapt from `docs/EXTENSION_DEVELOPMENT.md`.

## Overview

Extensions package custom components, scripts, and styles into reusable units that
can be distributed and installed into any Refast app.

## Extension Class

```python
from refast.extensions import Extension
from pathlib import Path

class MyExtension(Extension):
    name = "my-extension"
    version = "1.0.0"
    description = "A custom extension"
    scripts = ["my-extension.js"]
    styles = ["my-extension.css"]

    @property
    def static_path(self) -> Path:
        return Path(__file__).parent / "static"

    @property
    def components(self) -> list:
        return [MyCustomComponent]
```

## Project Structure

```
my_extension/
├── __init__.py          # Extension class
├── components.py        # Python components
├── static/
│   ├── my-extension.js  # UMD React bundle
│   └── my-extension.css # Styles
└── pyproject.toml       # Package config with entry point
```

## Entry Point Registration

```toml
[project.entry-points."refast.extensions"]
my_ext = "my_extension:MyExtension"
```

## Frontend Bundle

Extensions export a UMD module that registers components via the global API:

```javascript
(function() {
    const registry = window.RefastComponentRegistry;
    registry.register('MyComponent', MyReactComponent);
})();
```

## Using an Extension

```python
from my_extension import MyExtension

ui = RefastApp(
    title="My App",
    extensions=[MyExtension()],
)
```

Or rely on auto-discovery via entry points:

```python
ui = RefastApp(title="My App", auto_discover_extensions=True)
```

## Static Asset Serving

Extension assets are served at `/static/ext/{extension_name}/{filename}`.

## Next Steps

- [Building Components](/docs/advanced/component-dev) — Component development basics
- [Security](/docs/advanced/security) — Securing your app
"""
