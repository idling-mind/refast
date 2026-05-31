# Refast — Core Setup & App Creation

## Installation

```bash
pip install refast
# or with uv (preferred in this repo)
uv pip install refast
```

---

## Creating a RefastApp

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast import components as rc          # namespace import (common pattern)
from refast.theme import rose_theme          # optional theme

ui = RefastApp(
    title="My App",                          # browser tab title
    theme=rose_theme,                        # Theme instance (optional)
    secret_key="my-secret",                  # session encryption (optional)
    debug=False,
    favicon="/static/favicon.ico",           # emoji ("🚀") or URL
    custom_css=["/styles/main.css"],         # URL → <link>; inline string → <style>
    custom_js=["console.log('loaded')"],     # URL → <script src>; inline → <script>
    head_tags=['<meta name="description" content="...">'],
    preloaded_features=["charts", "markdown", "icons"],  # warm lazy JS chunks at startup
    extensions=[MyExtension()],              # explicit extension list
    auto_discover_extensions=True,           # default: scan entry points
)
```

### Built-in Themes

```python
from refast.theme import (
    default_theme, rose_theme, amber_minimal_theme,
    caffine_theme, catppuccin_theme, ocean_breeze_theme,
)
```

### Mounting to FastAPI

```python
app = FastAPI()
app.include_router(ui.router)           # mount at root (/)

# or with a prefix
app.include_router(ui.router, prefix="/ui")
```

---

## Defining Pages

Page handlers are **synchronous** functions that receive `ctx` and return a component tree:

```python
@ui.page("/")
def home(ctx: Context):
    return rc.Container(children=[
        rc.Heading("Home", level=1),
    ])

@ui.page("/dashboard")
def dashboard(ctx: Context):
    return rc.Container(children=[rc.Text("Dashboard")])
```

**IMPORTANT**: Page functions must be `def` (sync), NOT `async def`. Callbacks must be `async def`.

### URL Path Parameters

```python
@ui.page("/users/{user_id:int}")
def user_detail(ctx: Context):
    user_id: int = ctx.path_params["user_id"]  # auto-coerced to int
    return rc.Text(f"User {user_id}")

@ui.page("/posts/{slug:str}")
def post(ctx: Context):
    slug: str = ctx.path_params["slug"]
    return rc.Text(f"Post: {slug}")
```

Type annotations in route patterns:

| Pattern | Matches | Python type |
|---------|---------|------------|
| `{name}` or `{name:str}` | Any path segment | `str` |
| `{id:int}` | Digits only | `int` |
| `{value:float}` | Numeric | `float` |
| `{id:uuid}` | UUID format | `str` |

Exact paths are matched first (O(1)); parameterised patterns are tried in registration order.

### Query Parameters

```python
@ui.page("/search")
def search(ctx: Context):
    q = ctx.query_params.get("q", "")
    page = int(ctx.query_params.get("page", "1"))
    genre = ctx.query_params.get("genre", "all")
    return rc.Text(f"Searching for: {q}, page {page}")
```

---

## The Context Object (`ctx`)

`ctx` is passed to every page function and every callback. It is per-WebSocket-connection.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `ctx.state` | `State` | Per-connection in-memory state dict |
| `ctx.store` | `Store` | Browser storage (`ctx.store.local`, `ctx.store.session`) |
| `ctx.session` | `Session` | Server-side session (long-lived data) |
| `ctx.path_params` | `dict[str, Any]` | URL path parameters (coerced to declared types) |
| `ctx.query_params` | `dict[str, str]` | URL query string parameters |
| `ctx.url` | `str` | Full current URL path + query string |
| `ctx.event_data` | `dict/list/Any` | Raw event data from the frontend component |

### Async Update Methods (call inside callback functions)

```python
# Re-render the entire page with current state
await ctx.refresh()

# Partial re-render — find component by id, re-run page function, replace only that subtree
await ctx.refresh(target_id="todo-list")

# SPA navigation — updates URL, re-renders new page, WebSocket stays connected
await ctx.load("/dashboard")
await ctx.load("/page", scroll_to="section-id", scroll_behavior="smooth")

# Full browser redirect (can open in new tab)
await ctx.redirect("/external")
await ctx.redirect("https://...", target="_blank")

# DOM mutations by component id
await ctx.replace("comp-id", NewComponent(...))
await ctx.append("list-id", NewItem(...))
await ctx.prepend("list-id", FirstItem(...))
await ctx.remove("comp-id")

# Prop updates on an existing component (no full re-render)
await ctx.update_props("comp-id", {"class_name": "p-4"})
await ctx.update_props("container", {"children": [rc.Text("New")]})

# Text content update (lightest update)
await ctx.update_text("heading-id", "New Title")

# Streaming — incrementally append to a prop (e.g. Markdown, chart data)
await ctx.append_prop("output", "content", chunk)

# Toast notifications
await ctx.show_toast("Saved!", variant="success")
await ctx.show_toast("Error", variant="error", description="Details here")
await ctx.show_toast("Deleted", action={"label": "Undo", "callback": ctx.callback(undo)})
await ctx.show_toast("Loading...", variant="loading", toast_id="proc")
await ctx.show_toast("Done!", variant="success", toast_id="proc")  # update existing toast by id

# Execute JS in the browser from a callback
await ctx.call_js("window.scrollTo({ top: 0, behavior: 'smooth' })")
await ctx.call_js("document.getElementById(args.id)?.focus()", id="input-1")

# Call a component's imperative method (bound JS)
await ctx.call_bound_js("canvas-id", "clearCanvas")
await ctx.call_bound_js("canvas-id", "eraseMode", True)
```

### DOM Update Cost Reference

| Method | Cost | Best For |
|--------|------|----------|
| `ctx.refresh()` | Full tree | State-driven pages |
| `ctx.refresh(target_id=...)` | One subtree | Localised state changes |
| `ctx.replace(id, component)` | One component | Section swap |
| `ctx.append(id, component)` | One component | Lists, feeds, chat |
| `ctx.prepend(id, component)` | One component | Reverse-order lists |
| `ctx.remove(id)` | One ID | Deleting items |
| `ctx.update_props(id, props)` | Changed props | Disable, style, clear children |
| `ctx.update_text(id, text)` | New string | Status labels, counters |
| `ctx.append_prop(id, prop, value)` | Value delta | Streaming text/chart data |

---

## State Management

### `ctx.state` — Per-Connection In-Memory State

```python
# Dict-style access
ctx.state["count"] = 0
count = ctx.state["count"]
ctx.state.get("count", 0)          # with default
ctx.state.set("count", 42)         # explicit setter
ctx.state.update({"a": 1, "b": 2})

# Check existence
"count" in ctx.state

# Snapshot
d = ctx.state.to_dict()
```

**Key rule**: `ctx.state` lives for the WebSocket connection only — it resets if the user refreshes the browser page.

### Browser Storage (Persists Beyond WS Connection)

```python
# localStorage — survives browser restarts
theme = ctx.store.local.get("theme", "light")
ctx.store.local.set("theme", "dark")

# sessionStorage — survives until tab closes
ctx.store.session.set("wizard_step", 2)

# Pull latest browser values into ctx.store
await ctx.store.sync()
```

### Typed Pydantic State (Optional)

```python
from pydantic import BaseModel

class AppState(BaseModel):
    count: int = 0
    user: str | None = None

@ui.page("/")
def home(ctx: Context[AppState]):
    count = ctx.state.count   # attribute-style access
    return rc.Text(f"Count: {count}")
```

---

## Defining Callback Functions

Callbacks are top-level `async def` functions — **never** defined inside page functions:

```python
async def handle_click(ctx: Context):
    """Simple trigger — no extra args."""
    count = ctx.state.get("count", 0)
    ctx.state.set("count", count + 1)
    await ctx.refresh()

async def delete_item(ctx: Context, item_id: int):
    """Bound arg — item_id is pre-bound at callback creation time."""
    items = ctx.state.get("items", [])
    ctx.state["items"] = [i for i in items if i["id"] != item_id]
    await ctx.refresh()

async def submit_form(ctx: Context, email: str = "", name: str = ""):
    """Props — values come from the frontend prop store."""
    # Called via: ctx.callback(submit_form, props=["email", "name"])
    if not email:
        await ctx.show_toast("Email required", variant="error")
        return
    await ctx.show_toast("Submitted!", variant="success")

async def on_input_change(ctx: Context):
    """Read raw event data from the component."""
    value = ctx.event_data.get("value", "")
    ctx.state.set("query", value)
    await ctx.refresh(target_id="results")
```

---

## App Startup

```python
# app.py
from fastapi import FastAPI
from refast import RefastApp, Context
from refast import components as rc

ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    return rc.Container(children=[rc.Heading("Hello", level=1)])

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run with:
```bash
python app.py
# or
uvicorn app:app --reload
```

---

## Common Gotchas

1. **Page functions are sync, callbacks are async.** `@ui.page` handlers must be `def`, callbacks must be `async def`.
2. **`ctx.refresh()` re-runs the page function.** State mutations before `await ctx.refresh()` are visible in the new render.
3. **Use `ctx.refresh(target_id="...")` for partial updates** to avoid re-rendering the whole page and prevent focus loss.
4. **`ctx.state` resets on page refresh** (F5). Use `ctx.store.local` for browser-persistent data.
5. **`ctx.event_data`** contains the raw payload from the component (e.g., `{"value": "hello"}` for an `Input` `on_change`).
6. **URL params use `{name:type}` syntax** inside the route string — values land in `ctx.path_params` already coerced.
7. **`ui.router`** is lazy — it creates the `RefastRouter` on first access, which is fine for `app.include_router(ui.router)`.
