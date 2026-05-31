# Refast — Events, Callbacks & Forms

## Callback Types Overview

| Method | Runs Where | Roundtrip? | Use For |
|--------|-----------|------------|---------|
| `ctx.callback(fn)` | Server (Python) | Yes | State changes, DB calls, navigation |
| `ctx.js("code")` | Browser (JS) | No | Instant UI tweaks, no state needed |
| `ctx.save_prop("key")` | Browser (JS) | No | Capture input values for later |
| `ctx.chain([...])` | Both | Depends | Compose multiple actions on one event |
| `ctx.bound_js("id", "method")` | Browser (JS) | No | Call component imperative methods |

---

## 1. Server Callbacks — `ctx.callback(fn)`

The most common pattern: run an async Python function when an event fires.

```python
# Basic callback
rc.Button("Save", on_click=ctx.callback(save_data))

# Callback with bound arguments (pre-bound at render time)
rc.Button("Delete", on_click=ctx.callback(delete_item, item_id=42))

# Access bound args in the handler
async def delete_item(ctx: Context, item_id: int):
    items = ctx.state.get("items", [])
    ctx.state["items"] = [i for i in items if i["id"] != item_id]
    await ctx.refresh()
```

### Reusing One Callback for Multiple Components

Pass different kwargs to share a single handler across many components — a very common pattern for lists and button groups:

```python
@ui.page("/")
def page(ctx: Context):
    return rc.Row(children=[
        rc.Button("Blue",  on_click=ctx.callback(button_click, button_name="blue")),
        rc.Button("Green", on_click=ctx.callback(button_click, button_name="green")),
        rc.Button("Red",   on_click=ctx.callback(button_click, button_name="red")),
    ])

async def button_click(ctx: Context, button_name: str):
    await ctx.show_toast(f"{button_name} button clicked", variant="info")
```

This works for any component event and any number of kwargs:

```python
# Delete buttons in a list — each bound to its own item id
rc.Column(children=[
    rc.Row(children=[
        rc.Text(item["title"]),
        rc.IconButton(
            icon="trash",
            on_click=ctx.callback(delete_item, item_id=item["id"]),
        ),
    ])
    for item in ctx.state.get("items", [])
])

async def delete_item(ctx: Context, item_id: int):
    items = ctx.state.get("items", [])
    ctx.state["items"] = [i for i in items if i["id"] != item_id]
    await ctx.refresh()
```

The kwargs are serialised into the callback token at render time and delivered as Python keyword arguments when the event fires — no lookup tables or closures needed.

### Debounce and Throttle

```python
# Debounce — wait 300ms after last event before firing (ideal for search)
rc.Input(on_change=ctx.callback(search, debounce=300))

# Throttle — fire at most once per 200ms (ideal for scroll/resize)
rc.Input(on_change=ctx.callback(update, throttle=200))
```

### `ctx.event_data` — Raw Event Payload

Each component fires specific event data. Access it in the callback:

```python
async def on_select(ctx: Context):
    value = ctx.event_data.get("value", "")
    ctx.state["selected"] = value
    await ctx.refresh()
```

Common `ctx.event_data` shapes:
- `Input on_change` → `{"value": "hello"}`
- `Select on_change` → `{"value": "us"}`
- `Checkbox on_change` → `{"checked": True, "value": "yes"}`
- `CheckboxGroup on_change` → `{"value": ["apple", "banana"]}`
- `RadioGroup on_change` → `{"value": "pro"}`
- `Switch on_checked_change` → `True` or `False`
- `Slider on_value_change` → `[50]`
- `DataTable on_row_click` → `{"id": 1, "name": "Alice", ...}` (entire row)
- `DataTable on_sort_change` → `{"key": "name", "direction": "asc"}`
- `DataTable on_page_change` → `{"page": 2}`
- `Form on_submit` → `{"email": "alice@example.com", "name": "Alice", ...}`
- `Tabs on_value_change` → `{"value": "overview"}`

---

## 2. The Prop Store Pattern

The prop store lets inputs capture values **client-side** without a server roundtrip. Values are only sent to the server when a callback explicitly requests them via `props=[...]`.

### Why It Exists

Without prop store: every `on_change` keystroke → server roundtrip → state update → `ctx.refresh()`.  
With prop store: keystrokes stay in the browser; only the submit click causes a roundtrip.

### Basic Form Pattern

```python
@ui.page("/")
def form_page(ctx: Context):
    return rc.Container(children=[
        rc.Input(
            name="email",
            label="Email",
            on_change=ctx.save_prop("email"),    # stores value in browser; NO server call
        ),
        rc.Input(
            name="username",
            label="Username",
            on_change=ctx.save_prop("username"),
        ),
        rc.Button(
            "Submit",
            on_click=ctx.callback(handle_submit, props=["email", "username"]),
        ),
    ])

async def handle_submit(ctx: Context, email: str = "", username: str = ""):
    # email and username arrive as keyword arguments (fetched from browser prop store)
    if "@" not in email:
        await ctx.show_toast("Invalid email", variant="error")
        return
    await ctx.show_toast(f"Welcome, {username}!", variant="success")
```

### Advanced Key Mapping

`ctx.save_prop` can map a specific event field to a custom prop name:

```python
# Map event.value → "order_amount" and event.name → "field_id"
rc.Input(
    name="amount",
    on_change=ctx.save_prop({"value": "order_amount", "name": "field_id"}),
)
```

### Regex `props` Patterns

```python
# Collect all props whose names start with "form_"
rc.Button(on_click=ctx.callback(handle_submit, props=["form_.*"]))
```

### Comparison: `ctx.state` vs Prop Store

| | `ctx.state` | Prop Store |
|--|------------|-----------|
| **Location** | Server (Python) | Browser |
| **Roundtrip per update** | Yes | No |
| **Persistence** | WebSocket session | Until page refresh |
| **Use case** | App logic, computed UI | Form inputs, transient values |
| **Access** | `ctx.state.get()` anywhere | Kwargs in callbacks with `props=[...]` |

---

## 3. Debounced Validate-While-Typing

Use `ctx.chain` to store the value AND validate on the same event:

```python
rc.Input(
    name="email",
    on_change=ctx.chain([
        ctx.save_prop("email"),                                        # immediate, no roundtrip
        ctx.callback(validate_email, props=["email"], debounce=300),   # debounced server call
    ])
)

async def validate_email(ctx: Context, email: str = ""):
    is_valid = "@" in email and "." in email.split("@")[-1]
    await ctx.update_props("email-input", {"error": None if is_valid else "Invalid email"})
```

---

## 4. `ctx.chain` — Composing Multiple Actions

Chain multiple actions on a single event. Default mode is `"serial"`.

```python
# Serial (default) — run in order, second waits for first
rc.Button("Submit", on_click=ctx.chain([
    ctx.js("showSpinner()"),
    ctx.callback(handle_submit, props=["email"]),
]))

# Parallel — all actions fire simultaneously
rc.Button("Save All", on_click=ctx.chain([
    ctx.callback(save_user, props=["name"]),
    ctx.callback(save_settings, props=["theme"]),
], mode="parallel"))
```

---

## 5. JavaScript Callbacks — `ctx.js()`

Run JavaScript on the frontend without any server roundtrip.

```python
# Simple DOM manipulation
rc.Button("Scroll to top", on_click=ctx.js("window.scrollTo({ top: 0, behavior: 'smooth' })"))

# Toggle CSS class
rc.Button("Toggle dark", on_click=ctx.js("document.body.classList.toggle('dark')"))

# Access event data and pre-bound args in JS
rc.Button("Log value", on_click=ctx.js(
    "console.log('id:', args.item_id, 'event:', event)",
    item_id=42,   # bound as args.item_id
))

# Call a server callback FROM JavaScript (for conditional logic)
rc.Input(on_keydown=ctx.js(
    "if (event.key === 'Enter') refast.invoke(args.on_enter, {value: event.value})",
    on_enter=ctx.callback(handle_enter),
))
```

Available JS globals in `ctx.js` strings:
- `event` — the raw browser event (or parsed component event data)
- `args` — the bound kwargs dict
- `element` — the DOM element that fired the event
- `refast` — Refast JS API (e.g. `refast.invoke(callback, data)`)

---

## 6. Bound JS — `ctx.bound_js()`

Call an imperative method on a specific component's JS instance (e.g. a chart, canvas, or custom component that exposes methods):

```python
# In event handler (on_click etc.):
rc.Button("Clear", on_click=ctx.bound_js("canvas-id", "clearCanvas"))
rc.Button("Eraser", on_click=ctx.bound_js("canvas-id", "eraseMode", True))

# From a Python callback (async push):
await ctx.call_bound_js("chart-id", "setOption", {...})
await ctx.call_bound_js("canvas-id", "clearCanvas")
```

---

## 7. Form Handling Patterns

### Full Form with Validation

```python
@ui.page("/contact")
def contact_page(ctx: Context):
    errors = ctx.state.get("errors", {})
    return rc.Form(
        on_submit=ctx.callback(handle_contact),
        children=[
            rc.Input(
                name="name",
                label="Full Name",
                required=True,
                error=errors.get("name"),
            ),
            rc.Input(
                name="email",
                label="Email",
                type="email",
                required=True,
                error=errors.get("email"),
            ),
            rc.Textarea(
                name="message",
                label="Message",
                rows=5,
                required=True,
                error=errors.get("message"),
            ),
            rc.Button("Send", type="submit"),
        ],
    )

async def handle_contact(ctx: Context):
    data = ctx.event_data  # {"name": "Alice", "email": "alice@example.com", "message": "..."}
    errors = {}
    if not data.get("name"):
        errors["name"] = "Name is required."
    if "@" not in data.get("email", ""):
        errors["email"] = "Valid email required."
    if len(data.get("message", "")) < 10:
        errors["message"] = "Message too short."
    
    if errors:
        ctx.state["errors"] = errors
        await ctx.refresh()
        return
    
    # Process submission
    ctx.state["errors"] = {}
    await ctx.show_toast("Message sent!", variant="success")
    await ctx.load("/")
```

### Controlled Input Pattern (Live Updates)

When you need server-side logic on every change (e.g. live search), use a controlled input with `ctx.callback` directly:

```python
@ui.page("/search")
def search_page(ctx: Context):
    query = ctx.state.get("query", "")
    results = do_search(query) if query else []
    return rc.Column(children=[
        rc.Input(
            value=query,
            placeholder="Search...",
            on_change=ctx.callback(on_search_change, debounce=300),
        ),
        rc.Column(
            id="results",
            children=[rc.Text(r["title"]) for r in results],
        ),
    ])

async def on_search_change(ctx: Context):
    query = ctx.event_data.get("value", "")
    ctx.state["query"] = query
    await ctx.refresh(target_id="results")
```

---

## 8. Toast Notifications (Reference)

```python
# From a callback:
await ctx.show_toast("Saved!", variant="success")
await ctx.show_toast("Warning message", variant="warning")
await ctx.show_toast("Error occurred", variant="error", description="Details here")
await ctx.show_toast("Informational note", variant="info")

# Loading state → update to done
await ctx.show_toast("Processing...", variant="loading", toast_id="job-1")
await ctx.show_toast("Done!", variant="success", toast_id="job-1")  # replaces by id

# With action button
await ctx.show_toast(
    "Item deleted",
    action={"label": "Undo", "callback": ctx.callback(undo_delete)},
)
```

---

## 9. Keyboard Shortcuts

```python
from refast.components import KeyboardShortcut

# In the page component tree:
rc.KeyboardShortcut(
    shortcuts={
        "ctrl+k": ctx.callback(open_search),
        "ctrl+s": ctx.callback(save),
        "escape": ctx.callback(close_dialog),
    },
    priority=10,           # higher = takes precedence
    prevent_default=True,  # stop browser default (e.g. Ctrl+S save dialog)
)
```

The `KeyboardShortcut` component listens globally on the page. Add it anywhere in the component tree.
