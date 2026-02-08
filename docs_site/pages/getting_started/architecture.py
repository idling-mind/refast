"""Architecture — /docs/architecture."""

from refast.components import (
    Container,
    Heading,
    Markdown,
    Separator,
)


PAGE_TITLE = "Architecture"
PAGE_ROUTE = "/docs/architecture"


def render(ctx):
    """Render the architecture overview page."""
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


# ---------------------------------------------------------------------------
# PAGE CONTENT — To be expanded by an agent.
# See getting_started/AGENT_INSTRUCTIONS.md for full requirements.
# ---------------------------------------------------------------------------

CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Overview

Refast follows a **server-driven UI** architecture where the Python backend is the single
source of truth for the application state and UI structure.

## The Pipeline

```
Python (Server)          WebSocket           React (Browser)
┌──────────────┐        ┌─────────┐        ┌──────────────┐
│  Page Handler │──JSON──│   WS    │──JSON──│  Component   │
│  returns      │        │ Channel │        │  Renderer    │
│  Component    │        └─────────┘        │  (React)     │
│  Tree         │                           └──────────────┘
└──────────────┘                                   │
       ▲                                           │
       │              Events/Callbacks              │
       └────────────────────────────────────────────┘
```

## Request Lifecycle

### Initial Page Load (HTTP GET)

1. Browser requests `GET /`
2. Refast calls the registered page handler → returns a component tree
3. The tree is serialized to JSON
4. An HTML shell is returned containing:
   - CSS variables for the theme
   - The React client bundle (`refast-client.js` + `refast-client.css`)
   - The serialized component tree as embedded JSON
5. React boots, renders the component tree, and opens a WebSocket

### WebSocket Connection

Once the WebSocket is established:
- **Callbacks** → User interactions (clicks, input changes) send events via WebSocket
- **Updates** → Python handlers can push DOM updates back (replace, append, remove, etc.)
- **State** → Per-connection state persists across interactions
- **Store Sync** → Browser localStorage/sessionStorage can be read/written from Python

### SPA Navigation

When `ctx.navigate(path)` is called:
1. Frontend fetches `GET /path?format=json` (component tree only, no HTML shell)
2. React swaps the component tree in place
3. WebSocket stays connected — state persists

## Key Components

| Component | Role |
|-----------|------|
| `RefastApp` | Framework instance — registers pages, events, callbacks |
| `Context` | Per-request handle — state, store, callbacks, DOM updates |
| `State` | Server-side per-connection dictionary |
| `Store` | Client-side browser storage (local/session) accessible from Python |
| `Component` | Base class for all UI elements |
| `EventManager` | Routes events between frontend and backend |
| `BroadcastManager` | Pushes updates to multiple connected clients |

## Static Assets

Refast serves its React client from a built-in static directory:

- `/static/refast-client.js` — IIFE bundle (React + all components)
- `/static/refast-client.css` — Compiled Tailwind CSS
- `/static/ext/{name}/{file}` — Extension static files
"""
