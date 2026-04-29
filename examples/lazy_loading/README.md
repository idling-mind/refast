# Lazy Loading Example

Demonstrates the `preloaded_features` parameter on `RefastApp` for controlling which
frontend chunks the browser downloads.

## Quick Start

```bash
# All feature chunks preloaded
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

By default (`preloaded_features=None`), no feature chunks are preloaded.
Feature chunks load on demand when their components are first rendered.
When you set `preloaded_features=["charts"]`, the `charts` chunk is warmed up
at startup while other chunks stay on-demand.

## What to Observe

1. Open **DevTools → Network** tab in your browser.
2. Compare the JS files loaded on each of the three apps.
3. In the **Minimal** app, you'll see only `refast-client.js` and shared
   vendor chunks — no feature-specific files.

## API

```python
from refast import RefastApp

# Load on demand only (default)
ui = RefastApp(title="My App")

# Only charts + icons
ui = RefastApp(title="My App", preloaded_features=["charts", "icons"])

# Core UI only — no feature chunks
ui = RefastApp(title="My App", preloaded_features=[])
```
