# JavaScript Callbacks Example

This example demonstrates how to use `ctx.js()` and `ctx.call_js()` to execute JavaScript directly in the browser.

## Features Demonstrated

1. **Basic `ctx.js()` Examples** - Simple JavaScript execution on button clicks
2. **Bound Arguments** - Passing data from Python to JavaScript
3. **Accessing Event Data** - Using the `event` object in callbacks
4. **Python vs JavaScript Comparison** - When to use each approach
5. **`ctx.call_js()` from Python** - Executing JS after server-side logic
6. **DOM Manipulation** - Direct DOM manipulation with JavaScript
7. **Browser APIs** - Clipboard, Notifications, and more
8. **State & Store Sharing** - Reading/writing values from both Python and JavaScript

## Running the Example

```bash
cd examples/js_callbacks
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.

## Key Concepts

### `ctx.js()` - Client-side Event Handlers

Use `ctx.js()` when you want to execute JavaScript in response to an event without a server roundtrip:

```python
# Simple alert
Button("Click Me", on_click=ctx.js("alert('Hello!')"))

# With bound arguments
Button(
    "Delete",
    on_click=ctx.js("deleteItem(args.id)", id=123)
)

# Access event data
Input(on_change=ctx.js("console.log('Value:', event.value)"))
```

### `ctx.call_js()` - Execute JS from Python Callbacks

Use `ctx.call_js()` when you need to run JavaScript after server-side processing:

```python
async def save_data(ctx: Context):
    # Server-side logic first
    await database.save(data)
    
    # Then trigger client-side effects
    await ctx.call_js("confetti()")
    await ctx.call_js(
        "document.getElementById(args.id).focus()",
        id="next-input"
    )
```

### Sharing State Between Python and JavaScript

**Python State (`ctx.state`)** is server-side only - JavaScript cannot read it.

**localStorage (`ctx.store.local`)** can be shared! Python uses a `refast:local:` prefix:

```python
# Python - uses ctx.store.local (auto-prefixes key)
ctx.store.local.set("shared_value", 42)
value = ctx.store.local.get("shared_value")
```

```javascript
// JavaScript - must use the 'refast:local:' prefix
localStorage.setItem('refast:local:shared_value', '42');
let val = localStorage.getItem('refast:local:shared_value');
```

**Reading JS-modified values in Python:**

To read values that JavaScript has set directly in localStorage, use `await ctx.store.sync()` to refresh Python's cache:

```python
async def read_js_value(ctx: Context):
    # Sync store from browser first
    await ctx.store.sync()
    
    # Now get() returns the fresh browser value
    value = ctx.store.local.get("js_set_key")
```

### Available Variables in JavaScript

Inside `ctx.js()` callbacks, you have access to:

- **`event`** - Event data (value, checked, name, etc.)
- **`args`** - Bound arguments from Python
- **`element`** - The DOM element that triggered the event

### When to Use Each

| Use `ctx.js()` for | Use `ctx.callback()` for |
|-------------------|-------------------------|
| UI animations | Database operations |
| Toggling CSS classes | Server-side validation |
| Client-side libraries | State persistence |
| Immediate feedback | Business logic |
| DOM manipulations | Multi-client broadcasts |

### Storage Comparison

| Method | Instant | Persists | Python Reads | JS Reads |
|--------|---------|----------|--------------|----------|
| `ctx.state` | No | Session | ✅ Yes | ❌ No |
| `ctx.store.local` | No | Forever | ✅ Yes | ✅ Yes* |
| JS DOM state | ✅ Yes | No | ❌ No | ✅ Yes |
| JS localStorage (with prefix) | ✅ Yes | Forever | ✅ With sync** | ✅ Yes |

\* JS reads via: `localStorage.getItem('refast:local:key')`  
\** Use `await ctx.store.sync()` to refresh cache from browser

## Security Note

Never use user-provided strings directly in the JavaScript code:

```python
# ❌ DANGEROUS
Button(on_click=ctx.js(user_input))

# ✅ SAFE - Use bound arguments
Button(on_click=ctx.js("handleAction(args.action)", action=user_input))
```

Bound arguments are serialized as JSON data, not executable code.
