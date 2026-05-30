"""Routing & Navigation — /docs/concepts/routing."""

from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "Routing & Navigation"
PAGE_ROUTE = "/docs/concepts/routing"


def render(ctx):
    """Render the routing concept page."""
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
## Overview

Refast supports **multi-page single-page applications** (SPAs). Each page is a Python
function registered with `@ui.page()`. Navigation happens over the existing WebSocket
connection — no full page reloads, no lost state, no flash of unstyled content.

Key benefits:
- **State persistence** — `ctx.state` survives navigation since the WebSocket stays connected
- **Instant transitions** — only the component tree is swapped, the HTML shell never reloads
- **Python-first** — pages are plain Python functions; no framework-specific file conventions

---

## Basic Usage

Register pages by decorating a function with `@ui.page(path)`:

```python
from refast import RefastApp, Context
from refast.components import Container, Heading, Button

ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    return Container(children=[Heading("Home", level=1)])

@ui.page("/about")
def about(ctx: Context):
    return Container(children=[Heading("About", level=1)])

@ui.page("/settings")
def settings(ctx: Context):
    return Container(children=[Heading("Settings", level=1)])
```

Each handler receives a `Context` object and must return a single root component.

---

## Navigating Between Pages

### Programmatic navigation — `ctx.load()`

Call `ctx.load(path)` from any callback to navigate to another registered page:

```python
async def go_to_about(ctx: Context):
    await ctx.load("/about")

Button("About", on_click=ctx.callback(go_to_about))
```

`ctx.load()` accepts optional scroll control arguments:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | required | Target page path, e.g. `"/docs/api"` |
| `scroll_to` | `str \| None` | `"top"` | `"top"` to scroll to top, an element `id` to scroll that element into view, or `None` to leave position unchanged |
| `scroll_behavior` | `str` | `"instant"` | `"instant"` (no animation) or `"smooth"` |

```python
# Scroll to a named section after navigation
await ctx.load("/docs/api", scroll_to="parameters-section", scroll_behavior="smooth")

# Keep current scroll position
await ctx.load("/docs/api", scroll_to=None)
```

### Declarative navigation — `Link` component

For inline navigation links in the UI, use the `Link` component:

```python
from refast.components import Link

Link("Go to About", href="/about")
Link("Open in new tab", href="/about", target="_blank")
```

`Link` renders as an anchor tag and participates in SPA navigation automatically for
internal paths.

### Browser redirect — `ctx.redirect()`

To redirect the browser itself (triggering a full navigation, useful for external URLs
or OAuth flows), use `ctx.redirect()`:

```python
# Redirect within the app (full reload)
await ctx.redirect("/login")

# Redirect to an external URL in a new tab
await ctx.redirect("https://example.com", target="_blank")
```

Unlike `ctx.load()`, `ctx.redirect()` causes a full browser navigation and does **not**
preserve WebSocket state.

---

## Refreshing a Page

`ctx.refresh()` re-renders the current page with the latest state, sending the updated
component tree over the existing WebSocket connection:

```python
# Re-render the current page
await ctx.refresh()

# Re-render a specific page (navigate + re-render)
await ctx.refresh("/settings")

# Targeted partial refresh — update only one component subtree
await ctx.refresh(target_id="sidebar")
```

| Parameter | Description |
|-----------|-------------|
| `path` | Page to render. Defaults to the current path. |
| `target_id` | If set, only the component with this `id` (and its children) is updated. Useful to avoid re-rendering unrelated inputs. |

---

## How SPA Navigation Works Internally

When you call `ctx.load("/about")`:

1. The server sends a `navigate` WebSocket message with the new path
2. The frontend updates the browser URL via the History API (no page reload)
3. The server immediately calls the target page's handler function
4. A `page_render` message is sent with the new component tree
5. React swaps the component tree in place — the HTML shell, WebSocket, and JS state all stay intact

```
Browser                         Server
   |                               |
   | ── callback fires ──────────> |
   |                               | ctx.load("/about")
   | <── { type: "navigate" } ─── |  ← URL updated, no reload
   |                               | about(ctx) called
   | <── { type: "page_render" } ─ |  ← new component tree
   | (React swaps tree)            |
```

---

## Parameterised Routes

Path segments wrapped in `{name}` are captured as path parameters:

```python
@ui.page("/user/{user_id}")
def user_profile(ctx: Context):
    user_id = ctx.path_params["user_id"]   # str by default
    return Container(children=[Heading(f"User: {user_id}")])
```

You can annotate the type to get automatic coercion:

| Type annotation | Pattern matched | Python type |
|-----------------|-----------------|-------------|
| `{name}` or `{name:str}` | Any path segment | `str` |
| `{id:int}` | Digits only | `int` |
| `{value:float}` | Numeric (with `.`) | `float` |
| `{id:uuid}` | UUID format | `str` |

```python
@ui.page("/product/{product_id:int}")
def product_detail(ctx: Context):
    product_id: int = ctx.path_params["product_id"]   # already an int
    return Container(children=[Heading(f"Product #{product_id}")])
```

Navigate to parameterised pages by constructing the URL:

```python
async def open_product(ctx: Context, product_id: int):
    await ctx.load(f"/product/{product_id}")
```

---

## Query Parameters & Current URL

### `ctx.query_params`

All query string values are exposed as `ctx.query_params`, a `dict[str, str]`. When a
key appears multiple times only the last value is kept.

```python
@ui.page("/search")
def search(ctx: Context):
    query = ctx.query_params.get("q", "")
    page  = int(ctx.query_params.get("page", "1"))
    genre = ctx.query_params.get("genre", "all")
    return Container(children=[Heading(f'Results for "{query}" (page {page})')])
```

Navigate with query parameters by including them in the path string:

```python
await ctx.load("/search?q=refast&page=2&genre=programming")
```

`ctx.query_params` is updated on every `ctx.load()` call, so callbacks on the new page
always see the correct values.

### `ctx.url`

`ctx.url` returns the **full current path including the query string** — useful when you
need to log the active URL, build share links, or pass the current location to another
function:

```python
@ui.page("/search")
def search(ctx: Context):
    current_url = ctx.url          # e.g. "/search?q=refast&page=2"
    path_only   = ctx.url.split("?")[0]  # "/search"
    ...
```

It reflects the latest navigation state, so after `await ctx.load("/books?sort=year")`
the value becomes `"/books?sort=year"` within that handler.

### Reference table

| Property | Type | Example | Description |
|----------|------|---------|-------------|
| `ctx.url` | `str` | `"/search?q=hi&page=2"` | Full path + query string |
| `ctx.query_params` | `dict[str, str]` | `{"q": "hi", "page": "2"}` | Parsed query parameters |
| `ctx.path_params` | `dict[str, Any]` | `{"id": 42}` | Path segment parameters (type-coerced) |

---

## Shared Layout Pattern

For pages that share a common shell (sidebar, navbar, footer), define a layout helper
and call it from every page handler:

```python
def app_layout(ctx: Context, content):
    """Shared layout wrapper."""
    return Container(
        class_name="flex min-h-screen",
        children=[
            sidebar(ctx),
            Container(class_name="flex-1 p-6", children=[content]),
        ],
    )

@ui.page("/")
def home(ctx: Context):
    return app_layout(ctx, Heading("Home"))

@ui.page("/about")
def about(ctx: Context):
    return app_layout(ctx, Heading("About"))
```

---

## State-Based Navigation (Single-Page Pattern)

For simpler apps, you can simulate multiple "pages" with `ctx.state` and
`ctx.replace()` instead of registering separate routes:

```python
async def navigate(ctx: Context, page: str):
    ctx.state.set("current_page", page)
    await ctx.replace("root-container", render_app(ctx))

def render_app(ctx: Context):
    current = ctx.state.get("current_page", "home")
    pages = {"home": home_content, "about": about_content}
    return Container(id="root-container", children=[pages[current]()])
```

Use registered routes when you want bookmarkable URLs, browser back/forward support,
and deep-linking. Use state-based navigation when the "pages" are transient views
not worth exposing as URLs (e.g. a multi-step wizard).

---

## Important Notes / Gotchas

- **No wildcard routes** — Refast does not support catch-all `/*` patterns. Every URL
  must be registered explicitly with `@ui.page()`.
- **`ctx.state` persists, `ctx.store` also persists** — WebSocket state survives
  `ctx.load()` calls. Browser storage (`ctx.store`) survives full F5 reloads but
  `ctx.state` does not.
- **Order of registration does not matter** for exact routes, but parameterised routes
  are matched in registration order — register more specific patterns first.
- **Page function called once per navigation** — every `ctx.load()` call invokes the
  target page function. Avoid expensive blocking work at the top level; push it into
  callbacks or background tasks.
- **Always return a single root component** — returning `None` or a list will cause a
  render error on the client.

---

## Next Steps

- [State & Store](/docs/concepts/state) — Managing data that persists across navigations
- [DOM Updates](/docs/concepts/updates) — Targeted component updates without full re-renders
- [Streaming](/docs/concepts/streaming) — Incremental content delivery
- [Background Jobs](/docs/concepts/background) — Running tasks that span pages
"""
