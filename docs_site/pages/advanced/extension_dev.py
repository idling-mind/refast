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
Extensions let you package custom React components, scripts, and styles into
reusable Python packages that can be distributed on PyPI and installed into any
Refast app.

## Quickstart with the Cookiecutter Template

The fastest way to create an extension is with the official cookiecutter template:

```bash
pip install cookiecutter
cookiecutter gh:idling-mind/refast-extension-template
```

The template generates a fully-wired project with:

- Python component class (with correct `render()` and `extra_props` support)
- React + TypeScript frontend (Vite, with auto-registration via `RefastClient`)
- Hatch build hook that compiles the frontend automatically on `pip install`
- Entry point for auto-discovery by Refast
- Optional usage example app

After running the template generator, answer the prompts:

```
extension_name [my-component]: sketch-canvas
package_name [refast_sketch_canvas]:
component_name [SketchCanvas]:
extension_class_name [SketchCanvasExtension]:
description [A custom Refast extension]: Interactive drawing canvas
author_name [Your Name]: Jane Doe
...
```

Then build and install:

```bash
cd refast-sketch-canvas
pip install -e .          # builds the frontend via hatch hook automatically
```

See [idling-mind/refast-extension-template](https://github.com/idling-mind/refast-extension-template)
for full template documentation.

---

## Project Structure

An extension has two parts: a Python package and a compiled React frontend.

```
refast-myext/
├── pyproject.toml              # Hatch build config + entry point
├── hatch_build.py              # Build hook: runs npm build on pip install
├── src/
│   └── refast_myext/
│       ├── __init__.py         # Extension class + exports
│       ├── components.py       # Python component definitions
│       └── static/             # Built JS/CSS assets (generated)
│           └── refast-myext.js
└── frontend/                   # React source
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── src/
        ├── index.tsx           # Registers components with RefastClient
        ├── MyComponent.tsx     # Your React component
        └── utils.ts
```

---

## Step 1 — Extension Class

```python
# src/refast_myext/__init__.py
from pathlib import Path
from refast.extensions import Extension
from .components import MyComponent

class MyExtension(Extension):
    name = "refast-myext"          # unique identifier
    version = "0.1.0"
    description = "My custom components for Refast"
    scripts = ["refast-myext.js"]  # paths relative to static_path
    styles = []                    # CSS files if needed

    @property
    def static_path(self) -> Path:
        return Path(__file__).parent / "static"

    @property
    def components(self) -> list:
        return [MyComponent]

__all__ = ["MyExtension", "MyComponent"]
```

---

## Step 2 — Python Component

Python components define the API consumed by app developers. All prop names
must use `snake_case`; the frontend converts them to `camelCase` automatically.

```python
# src/refast_myext/components.py
from typing import Any
from refast.components.base import Component

class MyComponent(Component):
    \"""A custom counter component.\"""

    component_type = "MyComponent"  # MUST match the React component name exactly

    def __init__(
        self,
        title: str,
        value: int = 0,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **extra_props: Any,
    ):
        super().__init__(id=id, class_name=class_name, extra_props=extra_props)
        self.title = title
        self.value = value
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "value": self.value,
                # snake_case → camelCase conversion happens in the frontend
                "on_click": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
```

### Key rules

- **`component_type`** must exactly match the name used in `componentRegistry.register()`
- **All prop keys** in `render()` must be `snake_case`
- **Serialize callbacks** with `.serialize()` — never pass raw callables
- **Pass through `extra_props`** so users can forward arbitrary HTML/React attributes

---

## Step 3 — React Component

The frontend entry point registers components into `RefastClient.componentRegistry`.
`window.RefastClient` is available after the Refast client script loads, which is
always before extension scripts.

```tsx
// frontend/src/index.tsx
import { MyComponent } from './MyComponent';

function register(): void {
  if (!window.RefastClient) {
    console.error('[refast-myext] RefastClient not found on window');
    return;
  }
  const { componentRegistry } = window.RefastClient;
  if (!componentRegistry.has('MyComponent')) {
    componentRegistry.register('MyComponent', MyComponent);
  }
}

register();
```

```tsx
// frontend/src/MyComponent.tsx
import React from 'react';

interface MyComponentProps {
  id?: string;
  className?: string;
  title?: string;
  value?: number;
  onClick?: () => void;   // camelCase — converted from on_click by ComponentRenderer
  'data-refast-id'?: string;
}

export function MyComponent({ id, title, value, onClick, ...props }: MyComponentProps) {
  return (
    <div id={id} {...props}>
      <h3>{title}</h3>
      <span>{value}</span>
      <button onClick={() => onClick?.({ value })}>Click me</button>
    </div>
  );
}
```

---

## Step 4 — Build Configuration

```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "refast-myext"
version = "0.1.0"
dependencies = ["refast>=0.1.0"]

# Auto-discovery: Refast finds this extension automatically after pip install
[project.entry-points."refast.extensions"]
refast_myext = "refast_myext:MyExtension"
```

The `hatch_build.py` build hook (generated by the template) runs `npm install && npm run build`
automatically whenever the package is installed with pip.

---

## Step 5 — Using the Extension

```python
from refast import RefastApp, Context
from refast_myext import MyComponent

# Option A: explicit registration
ui = RefastApp(title="My App", extensions=[MyExtension()])

# Option B: auto-discovery via entry points (default)
ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    async def handle_click(ctx: Context):
        await ctx.set_state("count", ctx.state.get("count", 0) + 1)

    return MyComponent(
        title="Counter",
        value=ctx.state.get("count", 0),
        on_click=ctx.callback(handle_click),
    )
```

---

## Asset Loading Order

Refast injects assets into the HTML shell in this order:

1. `refast-client.css` — base styles
2. Extension CSS files (registration order)
3. `refast-client.js` — exposes `window.RefastClient`
4. Extension JS files (registration order)

Extension scripts can safely reference `window.RefastClient` because they always
load after it.

Extension static files are served at `/static/ext/{extension_name}/{filename}`.

---

## Real-World Example

[refast-echarts](https://github.com/idling-mind/refast-echarts) is a published
extension that wraps Apache ECharts. It follows the same pattern described here
and is a good reference when building your own extension.

---

## Next Steps

- [Building Components](/docs/advanced/component-dev) — Detailed component development patterns
- [Security](/docs/advanced/security) — Securing your app
"""
