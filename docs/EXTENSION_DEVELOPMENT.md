# Refast Extension Development Guide

This guide covers how to create third-party extensions for Refast that provide custom React components. Extensions allow you to wrap existing React libraries (like react-leaflet, react-codemirror, etc.) and expose them as Python components.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Extension Architecture](#extension-architecture)
4. [Creating Python Components](#creating-python-components)
5. [Creating React Components](#creating-react-components)
6. [Building the Extension](#building-the-extension)
7. [Publishing Your Extension](#publishing-your-extension)
8. [Advanced Topics](#advanced-topics)
9. [Complete Example: refast-leaflet](#complete-example-refast-leaflet)

---

## Overview

A Refast extension is a Python package that:

1. **Provides Python component classes** that define props and render to JSON
2. **Bundles React components** as UMD modules that register with Refast
3. **Includes static assets** (JavaScript, CSS) that get injected into the page

When a user installs your extension (`pip install refast-leaflet`), they can:
- Import and use your Python components
- The React components are automatically loaded and registered

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        Python Side                               │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │  Extension      │───▶│  RefastApp      │                     │
│  │  (LeafletExt)   │    │  _extensions    │                     │
│  └─────────────────┘    └─────────────────┘                     │
│          │                      │                                │
│          ▼                      ▼                                │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │  Python         │    │  HTML Shell     │                     │
│  │  Components     │───▶│  + script tags  │                     │
│  │  (MapContainer) │    │  for extension  │                     │
│  └─────────────────┘    └─────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Browser Side                              │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │  refast-client  │    │  Extension JS   │                     │
│  │  .js loaded     │───▶│  UMD loaded     │                     │
│  └─────────────────┘    └─────────────────┘                     │
│          │                      │                                │
│          ▼                      ▼                                │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │  window.        │◀───│  Registers      │                     │
│  │  RefastClient   │    │  components     │                     │
│  │  .componentReg  │    │  with registry  │                     │
│  └─────────────────┘    └─────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Minimal Extension Structure

```
refast-myext/
├── pyproject.toml
├── src/
│   └── refast_myext/
│       ├── __init__.py
│       ├── components.py
│       └── static/
│           └── refast-myext.js
└── frontend/                  # Optional: React source
    ├── package.json
    ├── vite.config.ts
    └── src/
        └── index.tsx
```

### Step 1: Create the Extension Class

```python
# src/refast_myext/__init__.py
from pathlib import Path
from refast.extensions import Extension
from .components import MyComponent

class MyExtension(Extension):
    name = "refast-myext"
    version = "0.1.0"
    description = "My custom components for Refast"
    
    scripts = ["refast-myext.js"]
    styles = []  # Add CSS files if needed
    
    @property
    def static_path(self) -> Path:
        return Path(__file__).parent / "static"
    
    @property
    def components(self) -> list:
        return [MyComponent]

# Export for convenience
__all__ = ["MyExtension", "MyComponent"]
```

### Step 2: Create Python Components

```python
# src/refast_myext/components.py
from typing import Any
from refast.components.base import Component

class MyComponent(Component):
    """A custom component."""
    
    component_type = "MyComponent"  # Must match React component name
    
    def __init__(
        self,
        title: str,
        value: int = 0,
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
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
                "on_click": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
            },
            "children": self._render_children(),
        }
```

### Step 3: Create the React Component (UMD Bundle)

```javascript
// static/refast-myext.js (pre-built UMD)
(function() {
  'use strict';
  
  const { componentRegistry, React } = window.RefastClient;
  
  // Note: onClick is already a function (converted by ComponentRenderer)
  const MyComponent = ({ title, value, onClick, className, children }) => {
    const handleClick = () => {
      // Simply call the function - it's already wrapped by Refast
      if (onClick) {
        onClick({ value });
      }
    };
    
    return React.createElement('div', 
      { className: `my-component ${className || ''}`, onClick: handleClick },
      React.createElement('h3', null, title),
      React.createElement('span', null, `Value: ${value}`),
      children
    );
  };
  
  componentRegistry.register('MyComponent', MyComponent);
  
  console.log('refast-myext: Registered MyComponent');
})();
```

### Step 4: Configure Entry Point

```toml
# pyproject.toml
[project]
name = "refast-myext"
version = "0.1.0"
dependencies = ["refast>=0.1.0"]

[project.entry-points."refast.extensions"]
refast_myext = "refast_myext:MyExtension"
```

### Step 5: Use the Extension

```python
# In user's app
from refast import RefastApp
from refast_myext import MyComponent

ui = RefastApp(title="My App")
# Extension auto-discovered via entry point!

@ui.page("/")
def home(ctx):
    return MyComponent(title="Hello", value=42)
```

---

## Extension Architecture

### The Extension Base Class

All extensions must inherit from `refast.extensions.Extension`:

```python
from refast.extensions import Extension

class MyExtension(Extension):
    # Required: Unique identifier
    name: str = "refast-myext"
    
    # Optional metadata
    version: str = "0.1.0"
    description: str = ""
    
    # Static assets (relative to static_path)
    scripts: list[str] = ["bundle.js"]
    styles: list[str] = ["styles.css"]
    
    @property
    def static_path(self) -> Path | None:
        """Return path to static assets directory."""
        return Path(__file__).parent / "static"
    
    @property
    def components(self) -> list[type[Component]]:
        """Return list of component classes."""
        return [Component1, Component2]
    
    def on_register(self, app: RefastApp) -> None:
        """Called when extension is registered."""
        # Custom initialization logic
        pass
```

### Extension Discovery

Extensions are discovered automatically via Python entry points:

```toml
# pyproject.toml
[project.entry-points."refast.extensions"]
my_extension = "my_package:MyExtension"
```

Or registered manually:

```python
from refast import RefastApp
from refast_myext import MyExtension

ui = RefastApp(
    extensions=[MyExtension()],
    auto_discover_extensions=False  # Disable auto-discovery
)
```

### Asset Loading Order

1. Refast client CSS (`refast-client.css`)
2. Extension CSS files (in extension registration order)
3. Refast client JS (`refast-client.js`) - exposes `window.RefastClient`
4. Extension JS files (in extension registration order)

---

## Creating Python Components

> **Note**: For a deep dive into component architecture, prop naming conventions, and event handling, see the [Component Development Guide](COMPONENT_DEVELOPMENT.md).

### Basic Component

```python
from typing import Any
from refast.components.base import Component

class Counter(Component):
    """A counter component with increment/decrement buttons."""
    
    component_type = "Counter"
    
    def __init__(
        self,
        value: int = 0,
        min_value: int | None = None,
        max_value: int | None = None,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.on_change = on_change
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value,
                "min_value": self.min_value,
                "max_value": self.max_value,
                "on_change": self._serialize_callback(self.on_change),
                "class_name": self.class_name,
            },
            "children": self._render_children(),
        }
    
    def _serialize_callback(self, callback: Any) -> dict | None:
        if callback is None:
            return None
        if hasattr(callback, "serialize"):
            return callback.serialize()
        return callback
```

### Using ReactComponent Base Class

For simpler wrapping, use the `ReactComponent` base class:

```python
from refast.components.registry import ReactComponent, register_component

@register_component("MapContainer", package="refast-leaflet")
class MapContainer(ReactComponent):
    """Leaflet map container."""
    
    def __init__(
        self,
        center: tuple[float, float] = (0, 0),
        zoom: int = 13,
        style: dict | None = None,
        on_click: Any = None,
        **kwargs,
    ):
        super().__init__(
            props={
                "center": list(center),
                "zoom": zoom,
                "style": style or {"height": "400px", "width": "100%"},
            },
            events={
                "on_click": on_click,
            },
            **kwargs,
        )
```

### Component with Children

```python
class Card(Component):
    component_type = "Card"
    
    def __init__(self, title: str = "", **kwargs):
        super().__init__(**kwargs)
        self.title = title
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "class_name": self.class_name,
            },
            "children": self._render_children(),  # Renders child components
        }

# Usage:
Card(title="My Card").add(
    Text("Card content"),
    Button("Click me"),
)
```

---

## Creating React Components

### Setting Up the Frontend Build

Create a `frontend/` directory with Vite configuration:

```json
// frontend/package.json
{
  "name": "refast-myext-frontend",
  "private": true,
  "scripts": {
    "build": "vite build",
    "dev": "vite build --watch"
  },
  "dependencies": {
    "your-react-library": "^1.0.0"
  },
  "peerDependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

```typescript
// frontend/vite.config.ts
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.tsx'),
      name: 'RefastMyExt',
      fileName: () => 'refast-myext.js',
      formats: ['umd'],
    },
    outDir: '../src/refast_myext/static',
    emptyOutDir: false,
    rollupOptions: {
      // Don't bundle React - use Refast's version
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'window.RefastClient.React',
          'react-dom': 'window.RefastClient.ReactDOM',
        },
      },
    },
  },
});
```

### React Component Template

```tsx
// frontend/src/index.tsx
import React from 'react';

// Get registry from Refast client
const { componentRegistry } = window.RefastClient;

// Import your React library
import { SomeLibraryComponent } from 'some-library';

// Your component props
// IMPORTANT: Callbacks are converted to functions by ComponentRenderer
// so you receive actual functions, not CallbackRef objects
interface MyComponentProps {
  title: string;
  value: number;
  onClick?: (data: Record<string, unknown>) => void;  // Already a function!
  className?: string;
  children?: React.ReactNode;
}

const MyComponent: React.FC<MyComponentProps> = ({
  title,
  value,
  onClick,
  className,
  children,
}) => {
  const handleClick = () => {
    // Simply call the function - ComponentRenderer already wrapped it
    if (onClick) {
      onClick({ value });
    }
  };
  
  return (
    <div className={className} onClick={handleClick}>
      <h3>{title}</h3>
      <span>Value: {value}</span>
      {children}
    </div>
  );
};

// Register with Refast
componentRegistry.register('MyComponent', MyComponent);

// Export for debugging
export { MyComponent };
```

### Understanding Callback Handling

**Important:** When Refast's `ComponentRenderer` renders your extension component, it automatically converts callback references (the serialized `{ callbackId: "..." }` objects) into actual JavaScript functions. This means:

1. **Your component receives functions, not callback refs** - The `onClick` prop is already a callable function
2. **Just call the function with event data** - No need to manually dispatch events or access WebSocket
3. **The data you pass becomes `ctx.event.data` in Python** - Include any relevant event information

```tsx
// ✅ CORRECT - Callbacks are already functions
interface MyComponentProps {
  onClick?: (data: Record<string, unknown>) => void;
}

const MyComponent: React.FC<MyComponentProps> = ({ onClick }) => {
  const handleClick = () => {
    onClick?.({ value: 42, name: "test" });  // Just call it!
  };
  return <button onClick={handleClick}>Click me</button>;
};
```

### Manual Callback Invocation (Advanced)

In rare cases where you need to invoke callbacks manually (e.g., from library event handlers that don't go through ComponentRenderer's prop processing), use the `refast:callback` custom event:

```tsx
// Type for raw callback references (before ComponentRenderer processes them)
interface CallbackRef {
  callbackId: string;
  boundArgs?: Record<string, unknown>;
}

// Helper to manually invoke callbacks via Refast's event system
function invokeCallback(callback: CallbackRef | undefined, data: Record<string, unknown> = {}): void {
  if (!callback?.callbackId) return;
  
  // Dispatch custom event that Refast's EventManager listens for
  const event = new CustomEvent('refast:callback', {
    detail: {
      callbackId: callback.callbackId,
      data: { ...(callback.boundArgs || {}), ...data },
    },
  });
  window.dispatchEvent(event);
}
```

**When to use manual invocation:**
- Wrapping libraries that manage their own event systems (e.g., ECharts, D3)
- Events triggered outside React's synthetic event system
- Canvas or WebGL libraries with custom event handling

### Handling Callbacks

Callbacks from Python are serialized as objects with a `callbackId`:

```javascript
// Python: on_click=ctx.callback(handle_click)
// Serializes to: { callbackId: "abc123", boundArgs: {...}, ... }

// ComponentRenderer converts this to a function automatically
// Your component receives: onClick = (data) => { /* sends to server */ }
```

### Rendering Children

Children from Python are passed as a `children` prop (array of component trees):

```tsx
interface Props {
  children?: React.ReactNode;
}

const Container: React.FC<Props> = ({ children }) => {
  return (
    <div className="container">
      {children}  {/* Refast's ComponentRenderer handles this */}
    </div>
  );
};
```

---

## Building the Extension

### Build Script

Add a build script to automate the process:

```python
# scripts/build.py
import subprocess
from pathlib import Path

def build():
    root = Path(__file__).parent.parent
    frontend = root / "frontend"
    
    # Install dependencies
    subprocess.run(["npm", "install"], cwd=frontend, check=True)
    
    # Build UMD bundle
    subprocess.run(["npm", "run", "build"], cwd=frontend, check=True)
    
    print("Build complete!")

if __name__ == "__main__":
    build()
```

### Pre-built Distribution

Include pre-built assets in your package:

```toml
# pyproject.toml
[tool.setuptools.package-data]
refast_myext = ["static/*.js", "static/*.css"]
```

---

## Publishing Your Extension

### Package Structure

```
refast-myext/
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   └── refast_myext/
│       ├── __init__.py
│       ├── components.py
│       ├── py.typed              # For type hints
│       └── static/
│           ├── refast-myext.js   # Pre-built UMD
│           └── refast-myext.css  # Optional CSS
├── frontend/                      # Source (not published)
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       └── index.tsx
└── tests/
    └── test_components.py
```

### pyproject.toml

```toml
[project]
name = "refast-myext"
version = "0.1.0"
description = "Custom components for Refast"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
dependencies = [
    "refast>=0.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
]

[project.entry-points."refast.extensions"]
refast_myext = "refast_myext:MyExtension"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
refast_myext = ["static/*.js", "static/*.css"]
```

### Publishing to PyPI

```bash
# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

---

## Advanced Topics

### Wrapping Complex React Libraries

Example: Wrapping react-leaflet

```tsx
// frontend/src/index.tsx
import React from 'react';
import { MapContainer as LeafletMap, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const { componentRegistry, React: R } = window.RefastClient;

interface MapContainerProps {
  center: [number, number];
  zoom: number;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}

const MapContainer: React.FC<MapContainerProps> = ({
  center,
  zoom,
  style = { height: '400px', width: '100%' },
  children,
}) => {
  return (
    <LeafletMap center={center} zoom={zoom} style={style}>
      <TileLayer
        attribution='&copy; OpenStreetMap'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {children}
    </LeafletMap>
  );
};

componentRegistry.register('MapContainer', MapContainer);
componentRegistry.register('TileLayer', TileLayer);
componentRegistry.register('Marker', Marker);
componentRegistry.register('Popup', Popup);
```

### Handling External CSS

If your library requires CSS (like Leaflet), include it in your build:

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    cssCodeSplit: false,  // Bundle all CSS together
    rollupOptions: {
      output: {
        assetFileNames: 'refast-myext.[ext]',
      },
    },
  },
});
```

Then reference it in your extension:

```python
class LeafletExtension(Extension):
    scripts = ["refast-leaflet.js"]
    styles = ["refast-leaflet.css"]  # Includes leaflet CSS
```

### Extension Configuration

Pass configuration from Python to JavaScript:

```python
# Python side
class MyExtension(Extension):
    def __init__(self, api_key: str = ""):
        super().__init__()
        self.api_key = api_key
    
    def on_register(self, app: RefastApp) -> None:
        # Inject config into page
        app._extension_config = getattr(app, '_extension_config', {})
        app._extension_config[self.name] = {"apiKey": self.api_key}
```

```typescript
// JavaScript side
const config = window.__REFAST_EXTENSION_CONFIG__?.['refast-myext'];
const apiKey = config?.apiKey || '';
```

### Shared State Between Components

Use React Context for shared state within your extension:

```tsx
const MapContext = React.createContext<MapInstance | null>(null);

const MapProvider: React.FC<Props> = ({ children }) => {
  const [map, setMap] = React.useState<MapInstance | null>(null);
  
  return (
    <MapContext.Provider value={map}>
      {children}
    </MapContext.Provider>
  );
};

componentRegistry.register('MapProvider', MapProvider);
```

### Wrapping Libraries with Custom Event Systems

Some libraries (like ECharts, D3, Three.js) manage their own event systems outside of React. In these cases, callback props won't be automatically converted to functions because they're not passed through React's prop system.

**The Problem:**
```tsx
// ECharts manages its own events - not through React props
useEffect(() => {
  const chart = echarts.init(containerRef.current);
  
  // This callback comes from props, but ECharts calls it directly
  // NOT through ComponentRenderer's prop processing
  chart.on('click', (params) => {
    // onClick here is still a CallbackRef object, not a function!
    onClick(params);  // ❌ Won't work - onClick is { callbackId: "..." }
  });
}, []);
```

**The Solution - Use `refast:callback` Custom Event:**

```tsx
import React, { useRef, useEffect } from 'react';
import * as echarts from 'echarts';

// Type for raw callback references
interface CallbackRef {
  callbackId: string;
  boundArgs?: Record<string, unknown>;
}

// Helper to invoke callbacks via Refast's event system
function invokeCallback(callback: CallbackRef | undefined, data: Record<string, unknown> = {}): void {
  if (!callback?.callbackId) return;
  
  // Dispatch custom event that Refast's EventManager listens for
  const event = new CustomEvent('refast:callback', {
    detail: {
      callbackId: callback.callbackId,
      data: { ...(callback.boundArgs || {}), ...data },
    },
  });
  window.dispatchEvent(event);
}

interface EChartsProps {
  option?: object;
  onClick?: CallbackRef;  // Raw callback ref (not processed by ComponentRenderer)
}

const EChartsComponent: React.FC<EChartsProps> = ({ option, onClick }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<echarts.ECharts | null>(null);
  
  useEffect(() => {
    if (!containerRef.current) return;
    
    const chart = echarts.init(containerRef.current);
    chartRef.current = chart;
    
    if (option) {
      chart.setOption(option);
    }
    
    // Setup event handler - manually invoke the callback
    if (onClick) {
      chart.on('click', (params: unknown) => {
        // Serialize event params and invoke callback
        invokeCallback(onClick, {
          name: (params as any).name,
          value: (params as any).value,
          seriesName: (params as any).seriesName,
        });
      });
    }
    
    return () => {
      chart.dispose();
    };
  }, [option, onClick]);
  
  return <div ref={containerRef} style={{ width: '100%', height: '400px' }} />;
};

componentRegistry.register('ECharts', EChartsComponent);
```

**Key Points:**
1. **Identify when manual invocation is needed** - If your library manages events outside React's synthetic event system
2. **Use `refast:callback` custom event** - This is what Refast's EventManager listens for
3. **Include `boundArgs`** - Merge them with your event data for proper callback argument handling
4. **Serialize event data** - Only include serializable data (no DOM elements, circular references)

---

## Complete Example: refast-leaflet

A full example of wrapping react-leaflet for Refast.

### Directory Structure

```
refast-leaflet/
├── pyproject.toml
├── README.md
├── src/
│   └── refast_leaflet/
│       ├── __init__.py
│       ├── components.py
│       ├── static/
│       │   ├── refast-leaflet.js
│       │   └── refast-leaflet.css
│       └── py.typed
└── frontend/
    ├── package.json
    ├── vite.config.ts
    └── src/
        └── index.tsx
```

### Python Components

```python
# src/refast_leaflet/__init__.py
from pathlib import Path
from refast.extensions import Extension
from .components import MapContainer, TileLayer, Marker, Popup

class LeafletExtension(Extension):
    name = "refast-leaflet"
    version = "0.1.0"
    description = "Interactive maps for Refast using Leaflet"
    
    scripts = ["refast-leaflet.js"]
    styles = ["refast-leaflet.css"]
    
    @property
    def static_path(self) -> Path:
        return Path(__file__).parent / "static"
    
    @property
    def components(self) -> list:
        return [MapContainer, TileLayer, Marker, Popup]

__all__ = ["LeafletExtension", "MapContainer", "TileLayer", "Marker", "Popup"]
```

```python
# src/refast_leaflet/components.py
from typing import Any
from refast.components.base import Component

class MapContainer(Component):
    """Leaflet map container."""
    
    component_type = "MapContainer"
    
    def __init__(
        self,
        center: tuple[float, float] = (51.505, -0.09),
        zoom: int = 13,
        height: str = "400px",
        width: str = "100%",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
    ):
        super().__init__(id=id, class_name=class_name)
        self.center = center
        self.zoom = zoom
        self.height = height
        self.width = width
        self.on_click = on_click
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "center": list(self.center),
                "zoom": self.zoom,
                "style": {"height": self.height, "width": self.width},
                "on_click": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
            },
            "children": self._render_children(),
        }

class TileLayer(Component):
    """Tile layer for maps."""
    
    component_type = "TileLayer"
    
    def __init__(
        self,
        url: str = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attribution: str = "&copy; OpenStreetMap contributors",
        id: str | None = None,
    ):
        super().__init__(id=id)
        self.url = url
        self.attribution = attribution
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "url": self.url,
                "attribution": self.attribution,
            },
            "children": [],
        }

class Marker(Component):
    """Map marker."""
    
    component_type = "Marker"
    
    def __init__(
        self,
        position: tuple[float, float],
        on_click: Any = None,
        id: str | None = None,
    ):
        super().__init__(id=id)
        self.position = position
        self.on_click = on_click
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "position": list(self.position),
                "on_click": self.on_click.serialize() if self.on_click else None,
            },
            "children": self._render_children(),
        }

class Popup(Component):
    """Marker popup."""
    
    component_type = "Popup"
    
    def __init__(
        self,
        content: str = "",
        id: str | None = None,
    ):
        super().__init__(id=id)
        self.content = content
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "content": self.content,
            },
            "children": self._render_children(),
        }
```

### React Components

```tsx
// frontend/src/index.tsx
import React from 'react';
import { MapContainer as LeafletMapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix default marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const { componentRegistry } = window.RefastClient;

// Register components
componentRegistry.register('MapContainer', LeafletMapContainer);
componentRegistry.register('TileLayer', TileLayer);
componentRegistry.register('Marker', Marker);
componentRegistry.register('Popup', Popup);

console.log('refast-leaflet: Components registered');
```

### Usage

```python
from refast import RefastApp
from refast.components import Container
from refast_leaflet import MapContainer, TileLayer, Marker, Popup

ui = RefastApp(title="Map Demo")

@ui.page("/")
def home(ctx):
    map = MapContainer(
        center=(51.505, -0.09),
        zoom=13,
        height="500px",
    )
    map.add(TileLayer())
    
    marker = Marker(position=(51.505, -0.09))
    marker.add(Popup(content="Hello from London!"))
    map.add(marker)
    
    return Container().add(map)
```

---

## Troubleshooting

### Component Not Rendering

1. Check browser console for errors
2. Verify component is registered: `window.RefastClient.componentRegistry.list()`
3. Ensure component type in Python matches React: `component_type = "MyComponent"`

### JavaScript Not Loading

1. Check Network tab for 404 errors
2. Verify `static_path` returns correct path
3. Check extension is registered: `print(app.extensions)`

### Callbacks Not Working

There are two callback patterns in Refast extensions. Make sure you're using the right one:

**Pattern 1: Standard React Props (most components)**
- ComponentRenderer converts callback refs to functions automatically
- Your component receives a callable function
- Just call it: `onClick?.({ value: 42 })`

**Pattern 2: Library-managed events (ECharts, D3, etc.)**
- Library events bypass React's prop system
- You receive raw CallbackRef objects
- Must dispatch `refast:callback` custom event manually

**Debugging Steps:**
1. **Check what you're receiving** - Add `console.log(typeof onClick, onClick)` to see if it's a function or object
2. **If it's a function** - Just call it with event data
3. **If it's an object with `callbackId`** - Use manual `refast:callback` dispatch:
   ```javascript
   window.dispatchEvent(new CustomEvent('refast:callback', {
     detail: { callbackId: onClick.callbackId, data: { value: 42 } }
   }));
   ```
4. **Verify Python serialization** - Ensure callback is serialized: `self.on_click.serialize() if self.on_click else None`
5. **Check WebSocket connection** - Open DevTools Network tab, filter by WS, verify messages are being sent/received

### CSS Not Applied

1. Verify CSS file exists in `static/` directory
2. Check `styles` list in extension class
3. Inspect HTML to confirm `<link>` tag is present

---

## API Reference

### Extension Class

```python
class Extension(ABC):
    name: str                    # Required: unique extension name
    version: str = "0.0.0"       # Version string
    description: str = ""        # Description
    scripts: list[str] = []      # JS files to load
    styles: list[str] = []       # CSS files to load
    
    @property
    def static_path(self) -> Path | None: ...
    
    @property
    def components(self) -> list[type[Component]]: ...
    
    def on_register(self, app: RefastApp) -> None: ...
    def get_script_urls(self) -> list[str]: ...
    def get_style_urls(self) -> list[str]: ...
    def get_static_file_path(self, filename: str) -> Path | None: ...
    def validate(self) -> list[str]: ...
```

### window.RefastClient

```typescript
interface RefastClient {
  componentRegistry: ComponentRegistry;
  React: typeof React;
  ReactDOM: typeof ReactDOM;
  version: string;
}

interface ComponentRegistry {
  register(name: string, component: React.ComponentType): void;
  get(name: string): React.ComponentType | undefined;
  has(name: string): boolean;
  list(): string[];
}
```
