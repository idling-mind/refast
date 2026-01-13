# Connection Status Example

This example demonstrates the `ConnectionStatus` component which conditionally displays content based on WebSocket connection state and fires callbacks on connection state changes.

## Running the Example

```bash
cd examples/connection_status
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.

## Testing Disconnection

1. Open the app in your browser
2. Stop the uvicorn server (Ctrl+C in the terminal)
3. Observe the disconnection indicator appear (bottom-right and top-left corners)
4. Check the browser console for JS callback messages
5. Restart the server: `uvicorn app:app --reload`
6. Observe the reconnection (indicator changes, toast notification appears)

## Features Demonstrated

### 1. Default Indicator
When no children are provided, `ConnectionStatus` shows a default indicator when disconnected:
```python
ConnectionStatus(
    position="bottom-right",
)
```

### 2. Separate Connected/Disconnected Content
Show different content based on connection state:
```python
ConnectionStatus(
    position="inline",
    children_connected=[
        Badge("Online", variant="success")
    ],
    children_disconnected=[
        Badge("Offline", variant="destructive")
    ]
)
```

### 3. Disconnected-Only Content
Show content only when disconnected:
```python
ConnectionStatus(
    position="top-left",
    children_disconnected=[
        Card(
            children=[
                CardContent(
                    children=[
                        Spinner(),
                        Text("Connection Lost"),
                    ]
                )
            ]
        )
    ]
)
```

### 4. Python Callbacks
Fire backend callbacks on connection state changes:
```python
async def handle_disconnect(ctx: Context):
    print("User disconnected!")

async def handle_reconnect(ctx: Context):
    await ctx.show_toast("Welcome back!")

ConnectionStatus(
    on_disconnect=ctx.callback(handle_disconnect),
    on_reconnect=ctx.callback(handle_reconnect),
)
```

### 5. JavaScript Callbacks
Fire frontend-only callbacks without server roundtrip:
```python
ConnectionStatus(
    js_on_disconnect=ctx.js("console.log('Disconnected!')"),
    js_on_reconnect=ctx.js("console.log('Reconnected!')"),
)
```

### 6. Position Options
- `top-left` - Fixed position at top-left corner
- `top-right` - Fixed position at top-right corner
- `bottom-left` - Fixed position at bottom-left corner
- `bottom-right` - Fixed position at bottom-right corner (default)
- `inline` - No fixed positioning, flows with document

### 7. Debounce
Avoid rapid callback firing during reconnection attempts:
```python
ConnectionStatus(
    debounce_ms=500,  # default: 500ms
)
```

## Component Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children_connected` | `list` | `[]` | Content to show when connected |
| `children_disconnected` | `list` | `[]` | Content to show when disconnected |
| `position` | `str` | `"bottom-right"` | Position on screen |
| `on_disconnect` | `Callback` | `None` | Python callback for disconnect events |
| `on_reconnect` | `Callback` | `None` | Python callback for reconnect events |
| `js_on_disconnect` | `JsCallback` | `None` | JS callback for disconnect events |
| `js_on_reconnect` | `JsCallback` | `None` | JS callback for reconnect events |
| `debounce_ms` | `int` | `500` | Debounce time before firing callbacks |
| `class_name` | `str` | `""` | Additional CSS classes |

## Behavior Notes

- If both `children_connected` and `children_disconnected` are empty, a default disconnection indicator is shown when disconnected
- If only `children_disconnected` is provided, nothing is shown when connected
- If only `children_connected` is provided, nothing is shown when disconnected
- Callbacks are debounced to prevent rapid firing during reconnection attempts
