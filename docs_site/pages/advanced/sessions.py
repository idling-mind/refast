"""Sessions — /docs/advanced/sessions."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Sessions"
PAGE_ROUTE = "/docs/advanced/sessions"


def render(ctx):
    """Render the sessions guide page."""
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

## Overview

Refast provides server-side session management for persisting data across requests
beyond the WebSocket connection lifetime.

## Session Object

```python
# In a callback
session = ctx.session

session.set("user_id", 123)
user_id = session.get("user_id")
session.delete("user_id")

# Bracket syntax
session["role"] = "admin"
role = session["role"]
```

## Session Stores

### MemoryStore (Default)

In-memory dictionary store. Simple, no dependencies, but data is lost on server restart.

```python
from refast.session.stores import MemoryStore

store = MemoryStore()
```

### RedisStore

Redis-backed store for production deployments with persistence and multi-server support.

```python
from refast.session.stores import RedisStore

store = RedisStore(redis_url="redis://localhost:6379")
```

## Session Middleware

Cookie-based session management:

```python
from refast.session import SessionMiddleware

app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret",
    store=MemoryStore(),
    cookie_name="session_id",
    max_age=3600,  # seconds
)
```

## State vs Session vs Store

| | `ctx.state` | `ctx.session` | `ctx.store` |
|---|---|---|---|
| **Location** | Server memory | Server store | Browser storage |
| **Lifetime** | WebSocket connection | Configurable TTL | Until cleared |
| **Shared across tabs** | No | Yes (same cookie) | Yes (same origin) |
| **Survives reload** | No | Yes | Yes |

## Next Steps

- [Security](/docs/advanced/security) — Securing sessions and requests
- [State Management](/docs/concepts/state) — Per-connection state
"""
