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
## Overview

Refast is built on a **Server-Driven UI** architecture. The Python backend is the single source of truth for the application state, business logic, and UI structure. The React frontend acts as a thin renderer.

## High-Level Architecture

```mermaid
graph TD
    User((User)) <--> |HTTP/WS| FastAPI[FastAPI App]
    subgraph Server [Refast Backend]
        FastAPI --> RefastApp
        RefastApp --> Router
        RefastApp --> Context
        Context --> State[State Management]
        Context --> Components[Component Tree]
    end
    subgraph Client [Browser]
        React[React Client]
        DOM[DOM]
        React --> |Events| Context
        Context --> |Updates| React
        React --> DOM
    end
```

## Request Lifecycle

### 1. Initial Page Load (HTTP GET)

When a user visits a Refast application:

1. The browser sends a `GET /` request.
2. FastAPI routes the request to Refast's page handler.
3. The handler executes in Python and returns a tree of component objects (e.g., `Container`, `Button`).
4. Refast serializes this component tree to JSON.
5. An HTML shell is returned, which includes:
   - The serialized initial state and component tree.
   - The React client bundle (`/static/refast-client.js`).
   - Theme CSS variables.
6. The browser loads the HTML, executes the React bundle, and hydrates the view.

### 2. WebSocket Connection

Immediately after hydration, the React client establishes a **WebSocket connection** back to the server. This persistent connection enables:

- **Real-time Updates**: The server can push UI changes to the client at any time.
- **Event Handling**: User interactions (clicks, input changes) are sent as events to the server.
- **State Synchronization**: Client-side state (like form inputs) can be synced to the server.

### 3. SPA Navigation

Refast behaves like a Single Page Application (SPA). When `ctx.navigate("/about")` is called:

1. The client fetches the new page's component tree via a lightweight JSON request (not full HTML).
2. The React client swaps the current component tree with the new one.
3. The browser URL is updated without a full page reload.
4. State is preserved or reset based on configuration.

## Key Components

| Component | Role |
| :--- | :--- |
| **`RefastApp`** | The central application instance. Manages configuration, routes, and extensions. |
| **`Context`** | Passed to every handler. Provides access to `state`, `store`, `navigate`, and more. |
| **`Component`** | Base class for all UI elements. Includes `Container`, `Button`, `Text`, etc. |
| **`State`** | Server-side storage for transient data during a user session. |
| **`Store`** | Interface for persistent storage (cookies, local storage, session storage). |
| **`EventManager`** | Internal system that routes client events to Python callbacks. |

## Static Assets

Refast serves its client assets automatically:

- `/static/refast-client.js`: The bundled React runtime and component library.
- `/static/refast-client.css`: Compiled Tailwind CSS styles.
- `/static/favicon.ico`: Default favicon (customizable).

Extensions can also serve their own static files under `/static/ext/{name}/`.
"""
