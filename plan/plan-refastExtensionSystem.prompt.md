# Plan: Refast Extension System for Third-Party Components

## Overview

The current Refast framework has **partial infrastructure** for extensions—the Python-side `ComponentRegistry` and `ReactComponent` base class exist, but key pieces are missing to enable true third-party component packages. This plan outlines changes to enable packages like `refast-leaflet` that wrap external React libraries.

---

## Current State Analysis

### What Exists

1. **Python-side `@register_component` decorator** - Can register components with package/module metadata
2. **`get_external_packages()` function** - Returns mapping of component names to NPM packages (but never used!)
3. **`ReactComponent` base class** - Designed for wrapping external React components
4. **`componentRegistry` on frontend** - Has `register()` and `get()` methods

### What's Missing

1. **Package metadata is stored but never used** - The `package` and `module` fields in `ComponentRegistration` are never read to dynamically load components
2. **No dynamic component loading** - All React components must be bundled at build time
3. **No external asset injection** - No mechanism to add extra `<script>` or `<link>` tags for third-party JS/CSS
4. **No plugin discovery** - No way to scan for installed packages that provide Refast components

---

## Implementation Steps

### Step 1: Create an Extension Base Class

Create `src/refast/extensions/` module with an `Extension` base class that defines:
- Extension metadata (name, version, description)
- Static assets (scripts, styles, static_path)
- Component list
- Optional initialization hooks

```python
# src/refast/extensions/base.py
from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from refast.components.base import Component

class Extension(ABC):
    """Base class for Refast extensions."""
    
    name: str  # Unique extension name (e.g., "refast-leaflet")
    version: str = "0.0.0"
    description: str = ""
    
    # Static assets to inject into HTML
    scripts: list[str] = []  # JS files relative to static_path
    styles: list[str] = []   # CSS files relative to static_path
    
    # Path to static assets directory
    @property
    def static_path(self) -> Path | None:
        return None
    
    # Components provided by this extension
    @property
    def components(self) -> list[type["Component"]]:
        return []
    
    def on_register(self, app: "RefastApp") -> None:
        """Called when extension is registered with an app."""
        pass
```

### Step 2: Implement Extension Discovery

Modify `RefastApp` to discover and load extensions:

1. **Entry point discovery** using `importlib.metadata` to find packages with `refast.extensions` entry point
2. **Manual registration** via `app.register_extension(extension)`
3. **Auto-registration** of discovered extensions on app init

```python
# In RefastApp.__init__
def __init__(
    self,
    title: str = "Refast App",
    extensions: list[Extension] | None = None,
    auto_discover_extensions: bool = True,
):
    self._extensions: dict[str, Extension] = {}
    
    if auto_discover_extensions:
        self._discover_extensions()
    
    if extensions:
        for ext in extensions:
            self.register_extension(ext)
```

### Step 3: Modify HTML Shell Rendering

Update `_render_html_shell()` in `app.py` to:
1. Collect all extension assets
2. Inject `<script>` tags for extension JS bundles
3. Inject `<link>` tags for extension CSS

```python
def _render_html_shell(self, component: Any, ctx: "Context") -> str:
    # Collect extension assets
    ext_scripts = []
    ext_styles = []
    for ext in self._extensions.values():
        for script in ext.scripts:
            ext_scripts.append(f'/static/ext/{ext.name}/{script}')
        for style in ext.styles:
            ext_styles.append(f'/static/ext/{ext.name}/{style}')
    
    # Build HTML with extension assets...
```

### Step 4: Add Extension Static File Routing

Add routes in `router.py` to serve extension static files:

```python
@router.get("/static/ext/{extension_name}/{filename:path}")
async def serve_extension_static(extension_name: str, filename: str):
    ext = app._extensions.get(extension_name)
    if ext and ext.static_path:
        file_path = ext.static_path / filename
        if file_path.exists():
            return FileResponse(file_path)
    raise HTTPException(404)
```

### Step 5: Expose componentRegistry Globally

Modify `src/refast-client/src/index.tsx` to expose the registry on `window`:

```typescript
// Expose for extensions
declare global {
  interface Window {
    RefastClient: {
      componentRegistry: typeof componentRegistry;
      React: typeof React;
      ReactDOM: typeof ReactDOM;
    };
  }
}

window.RefastClient = {
  componentRegistry,
  React,
  ReactDOM,
};
```

This allows extension UMD bundles to register their components:

```javascript
// In extension's UMD bundle
(function() {
  const { componentRegistry, React } = window.RefastClient;
  
  const MapContainer = (props) => {
    // Component implementation using react-leaflet
  };
  
  componentRegistry.register('MapContainer', MapContainer);
})();
```

### Step 6: Write Extension Documentation

Create comprehensive documentation in `docs/EXTENSION_DEVELOPMENT.md` covering:

1. **Extension package structure**
2. **Python component definition**
3. **React component bundling (Vite UMD config)**
4. **Static asset setup**
5. **Entry point configuration in pyproject.toml**
6. **Simple and complex examples**

---

## Further Considerations

### 1. Build-time vs Runtime Loading Strategy

**Runtime UMD Loading (Recommended Primary Approach)**
- Extensions ship pre-built UMD bundles
- No rebuild needed when adding/removing extensions
- Components self-register on `window.RefastClient.componentRegistry`
- Simpler for users: just `pip install refast-leaflet`

**Build-time Bundling (Alternative for Advanced Users)**
- Extensions provide source React components
- User runs a build command that bundles everything together
- Better tree-shaking and optimization
- Required for extensions that need deep integration

**Decision needed:** Should we support both? Primary approach should be runtime for simplicity.

### 2. TypeScript Types for Extension Authors

Options:
1. **Publish `@refast/types` on npm** with `componentRegistry` types, callback types, prop interfaces
2. **Document the API in the extension guide** with type definitions inline
3. **Export types from the main bundle** accessible via `window.RefastClient.types`

**Recommendation:** Start with option 2 (documented types), add npm package later if demand exists.

### 3. Peer Dependency Strategy

Extensions like `refast-leaflet` need React. Strategy:

1. **Document that extensions must use `peerDependencies`** for React
2. **Externalize React in extension Vite config** - React is already on `window.RefastClient.React`
3. **Provide a starter template** with correct Vite config for extensions

Example extension `vite.config.ts`:
```typescript
export default defineConfig({
  build: {
    lib: {
      entry: 'src/index.tsx',
      name: 'RefastLeaflet',
      fileName: 'refast-leaflet',
      formats: ['umd'],
    },
    rollupOptions: {
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

### 4. Version Compatibility

How to handle version mismatches between:
- Refast core version
- Extension version
- Shared dependencies (React, Radix UI, etc.)

**Proposal:**
1. Extensions declare compatible Refast versions in `pyproject.toml`
2. Warn at runtime if versions don't match
3. Document which React version is bundled with each Refast release

---

## Example Extension Structure

```
refast-leaflet/
├── pyproject.toml
├── README.md
├── src/
│   └── refast_leaflet/
│       ├── __init__.py           # Extension class + component exports
│       ├── components.py         # Python component definitions
│       └── static/
│           ├── refast-leaflet.js  # UMD bundle (React components)
│           └── refast-leaflet.css # Leaflet CSS + custom styles
└── frontend/                      # React source (for development)
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── index.tsx              # Entry point, registers components
        └── components/
            ├── MapContainer.tsx
            ├── Marker.tsx
            └── TileLayer.tsx
```

**pyproject.toml:**
```toml
[project]
name = "refast-leaflet"
version = "0.1.0"
dependencies = ["refast>=0.1.0"]

[project.entry-points."refast.extensions"]
refast_leaflet = "refast_leaflet:LeafletExtension"
```

**src/refast_leaflet/__init__.py:**
```python
from pathlib import Path
from refast.extensions import Extension
from .components import MapContainer, Marker, TileLayer, Popup

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
        return [MapContainer, Marker, TileLayer, Popup]

# Convenience exports
__all__ = ["LeafletExtension", "MapContainer", "Marker", "TileLayer", "Popup"]
```

---

## Implementation Priority

1. **Phase 1: Core Extension Infrastructure**
   - [ ] Create `Extension` base class
   - [ ] Add extension registration to `RefastApp`
   - [ ] Implement entry point discovery
   - [ ] Add extension static file routing

2. **Phase 2: Frontend Integration**
   - [ ] Expose `componentRegistry` on `window.RefastClient`
   - [ ] Expose React/ReactDOM for extensions
   - [ ] Test with a simple UMD extension

3. **Phase 3: Documentation & Tooling**
   - [ ] Write `EXTENSION_DEVELOPMENT.md`
   - [ ] Create extension starter template
   - [ ] Build a reference extension (e.g., `refast-leaflet` or `refast-codemirror`)

4. **Phase 4: Advanced Features (Future)**
   - [ ] Build-time bundling option
   - [ ] TypeScript types package
   - [ ] Extension marketplace/registry
