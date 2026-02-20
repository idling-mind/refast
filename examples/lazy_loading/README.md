# Lazy Loading Example

Demonstrates the `features` parameter on `RefastApp` for controlling which
frontend chunks the browser downloads.

## Quick Start

```bash
# All features (default) — every chunk loaded
uvicorn examples.lazy_loading.app:app_all --port 8001

# Charts only — only the charts chunk is loaded
uvicorn examples.lazy_loading.app:app_charts --port 8002

# Minimal — no feature chunks, core UI only
uvicorn examples.lazy_loading.app:app_minimal --port 8003
```

## How It Works

Refast's frontend is split into **feature chunks** via Vite's code-splitting:

| Chunk | Contents | Approx. Size |
|-------|----------|-------------|
| `charts` | Recharts + chart wrappers | ~200 KB |
| `markdown` | react-markdown + syntax highlighter | ~120 KB |
| `icons` | Lucide icons | ~80 KB |
| `navigation` | Breadcrumbs, menus, sidebar, pagination | ~40 KB |
| `overlay` | Dialogs, drawers, sheets, popovers | ~35 KB |
| `controls` | Switches, sliders, date pickers | ~30 KB |

By default (`features=None`), **all** chunks are preloaded via
`<link rel="modulepreload">` hints. When you set `features=["charts"]`,
only the `charts` chunk is preloaded — other chunks are never downloaded
unless a component from them appears in the rendered tree.

## What to Observe

1. Open **DevTools → Network** tab in your browser.
2. Compare the JS files loaded on each of the three apps.
3. In the **Minimal** app, you'll see only `refast-client.js` and shared
   vendor chunks — no feature-specific files.

## API

```python
from refast import RefastApp

# Load all features (default)
ui = RefastApp(title="My App")

# Only charts + icons
ui = RefastApp(title="My App", features=["charts", "icons"])

# Core UI only — no feature chunks
ui = RefastApp(title="My App", features=[])
```
