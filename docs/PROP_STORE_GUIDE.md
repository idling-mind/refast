# Prop Store Guide

The **Prop Store** is a frontend-only state management feature that enables efficient form handling by capturing component values without server roundtrips.

## Overview

When building forms in Refast, you typically need to track input values so they can be accessed when the user clicks a submit button. The traditional approach requires a callback for each input that syncs the value to `ctx.state` on every keystroke - resulting in unnecessary server roundtrips.

The prop store solves this by:
1. Storing values **on the frontend** when events occur (via `store_as`)
2. Sending requested values **only when a callback is invoked** (via `props=[...]`)
3. Delivering requested values as **keyword arguments** to your Python callback

## Basic Usage

### Storing Values

Use the `store_as` parameter in `ctx.callback()` to capture event values:

```python
from refast import Context, RefastApp
from refast.components import Input, Button, Container

ui = RefastApp()

@ui.page("/")
def form_page(ctx: Context):
    return Container(
        children=[
            # Store the input value as "email" (no server call on change)
            Input(
                placeholder="Enter email",
                on_change=ctx.callback(store_as="email"),
            ),
            
            # Store another input as "username"
            Input(
                placeholder="Enter username", 
                on_change=ctx.callback(store_as="username"),
            ),
            
            # Submit button - request props as keyword arguments
            Button(
                "Submit",
                on_click=ctx.callback(handle_submit, props=["email", "username"]),
            ),
        ]
    )
```

### Accessing Stored Values

Stored values are delivered as **keyword arguments** to your callback when you use `props=[...]`:

```python
async def handle_submit(ctx: Context, email: str = "", username: str = ""):
    # Values from store_as arrive as keyword arguments
    
    # Validate and process
    if not email or "@" not in email:
        await ctx.toast("Invalid email", variant="error")
        return
    
    # Use the values...
    await save_user(email, username)
    await ctx.toast("Saved successfully!")
```

## API Reference

### `ctx.callback(func=None, *, store_as=None, props=None, **bound_args)`

Create a callback with optional prop store functionality.

**Parameters:**
- `func` (Callable, optional): The Python function to call. If omitted with `store_as`, creates a store-only callback.
- `store_as` (str | dict, optional): Store directive for capturing event data.
  - `str`: Store the event's `value` under this key
  - `dict`: Map event data keys to store keys (e.g., `{"value": "email", "name": "field"}`)
- `props` (list[str], optional): List of prop store keys to send as keyword arguments. Supports regex patterns (e.g., `["input_.*"]`).
- `**bound_args`: Arguments to bind to the callback

**Returns:** `Callback` object

### `props` Parameter

The `props` parameter specifies which stored values to include as keyword arguments when the callback is invoked. Supports:

- **Exact keys**: `props=["email", "username"]`
- **Regex patterns**: `props=["input_.*"]` matches all keys starting with `input_`
- **Mixed**: `props=["email", "field_.*"]`

## Usage Patterns

### Store-Only (No Server Call)

When you only need to capture a value without any immediate processing:

```python
# No server roundtrip - value stored on frontend only
Input(on_change=ctx.callback(store_as="field_name"))
```

### Store and Process

When you need to both store the value AND run validation/processing:

```python
async def validate_and_store(ctx: Context, value: str):
    # This runs on every change (with debounce recommended)
    if len(value) < 3:
        await ctx.toast("Too short", variant="warning")

Input(
    on_change=ctx.callback(
        validate_and_store,
        store_as="username",  # Also stores as "username"
    )
)
```

### Advanced Key Mapping

Map specific event data fields to different store keys:

```python
# Store event.value as "order_amount" and event.name as "field_id"
Input(
    name="amount",
    on_change=ctx.callback(
        store_as={"value": "order_amount", "name": "field_id"}
    )
)
```

### Combining with Debounce

For real-time validation without excessive calls:

```python
from refast.components import Input

Input(
    on_change=ctx.callback(
        validate_email,
        store_as="email",
        debounce=300,  # Wait 300ms after typing stops
    )
)
```

## Comparison with ctx.state

| Feature | ctx.state | Prop Store (store_as + props) |
|---------|-----------|-------------------------------|
| Storage location | Backend (Python) | Frontend (Browser) |
| Server roundtrip | Every update | Only on callback invoke |
| Persistence | Across page renders | Until page refresh |
| Use case | App state, complex data | Form inputs, temp values |
| Access pattern | Read/write anytime | Keyword args in callbacks |

### When to Use Which

**Use `ctx.state` when:**
- You need to persist data across page navigation
- You need to trigger UI updates based on state changes
- You're storing complex application state

**Use `store_as` + `props` when:**
- Capturing form input values
- You don't need to react to every change
- You want to minimize server roundtrips
- Building multi-field forms with a single submit

## Complete Example

```python
from refast import Context, RefastApp
from refast.components import (
    Button, Card, CardContent, CardHeader, CardTitle,
    Column, Container, Input, Label, Alert,
)

ui = RefastApp(title="Registration Form")


async def handle_register(ctx: Context, username: str = "", email: str = "",
                          password: str = "", confirm_password: str = ""):
    # Values arrive as keyword arguments via props=[...]
    errors = []
    if len(username) < 3:
        errors.append("Username must be at least 3 characters")
    if "@" not in email:
        errors.append("Invalid email address")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if password != confirm_password:
        errors.append("Passwords don't match")
    
    if errors:
        ctx.state.set("errors", errors)
    else:
        ctx.state.set("errors", [])
        # Process registration...
        await ctx.toast("Registration successful!", variant="success")
    
    await ctx.refresh()


@ui.page("/")
def registration_form(ctx: Context):
    errors = ctx.state.get("errors", [])
    
    return Container(
        children=[
            Card(
                children=[
                    CardHeader(children=[CardTitle("Register")]),
                    CardContent(
                        children=[
                            # Show errors if any
                            *[Alert(variant="destructive", description=e) 
                              for e in errors],
                            
                            # Form fields - all use store_as
                            Column(
                                class_name="gap-4",
                                children=[
                                    Column(
                                        class_name="gap-2",
                                        children=[
                                            Label("Username"),
                                            Input(
                                                placeholder="Choose a username",
                                                on_change=ctx.callback(store_as="username"),
                                            ),
                                        ]
                                    ),
                                    Column(
                                        class_name="gap-2",
                                        children=[
                                            Label("Email"),
                                            Input(
                                                type="email",
                                                placeholder="your@email.com",
                                                on_change=ctx.callback(store_as="email"),
                                            ),
                                        ]
                                    ),
                                    Column(
                                        class_name="gap-2",
                                        children=[
                                            Label("Password"),
                                            Input(
                                                type="password",
                                                placeholder="••••••••",
                                                on_change=ctx.callback(store_as="password"),
                                            ),
                                        ]
                                    ),
                                    Column(
                                        class_name="gap-2",
                                        children=[
                                            Label("Confirm Password"),
                                            Input(
                                                type="password",
                                                placeholder="••••••••",
                                                on_change=ctx.callback(store_as="confirm_password"),
                                            ),
                                        ]
                                    ),
                                    Button(
                                        "Register",
                                        on_click=ctx.callback(
                                            handle_register,
                                            props=["username", "email", "password", "confirm_password"],
                                        ),
                                        class_name="w-full",
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
```

## Best Practices

1. **Use descriptive keys**: Name your store keys clearly (e.g., `"user_email"` not `"e"`)

2. **Group related fields**: Use dot notation for organization (e.g., `"shipping.address"`, `"shipping.city"`)

3. **Validate on submit**: Don't validate every keystroke unless needed - validate in the submit callback

4. **Combine with debounce for real-time validation**: If you need to show validation as the user types:
   ```python
   Input(on_change=ctx.callback(validate, store_as="field", debounce=300))
   ```

5. **Use regex patterns in props**: For forms with many fields sharing a prefix:
   ```python
   Button(on_click=ctx.callback(handle_submit, props=["form_.*"]))
   ```

6. **Clear sensitive data after use**: The prop store persists until page refresh, so clear sensitive fields after processing if needed

## Limitations

- **Frontend-only storage**: Values are lost on page refresh (use `ctx.state` or `ctx.store` for persistence)
- **No automatic sync**: Prop store values don't trigger re-renders
- **Callback-scoped access**: Values are only available as kwargs when `props=[...]` is specified
