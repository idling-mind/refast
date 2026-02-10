# Prop Store Guide

The **Prop Store** is a frontend-only state management feature that enables efficient form handling by capturing component values without server roundtrips.

## Overview

When building forms in Refast, you typically need to track input values so they can be accessed when the user clicks a submit button. The traditional approach requires a callback for each input that syncs the value to `ctx.state` on every keystroke - resulting in unnecessary server roundtrips.

The prop store solves this by:
1. Storing values **on the frontend** when events occur
2. Sending all stored values **only when a callback is invoked**
3. Making stored values available via `ctx.prop_store` in any callback

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
            
            # Submit button - all prop_store values sent with this callback
            Button(
                "Submit",
                on_click=ctx.callback(handle_submit),
            ),
        ]
    )
```

### Accessing Stored Values

In any callback, access stored values via `ctx.prop_store`:

```python
async def handle_submit(ctx: Context):
    # Access values stored via store_as
    email = ctx.prop_store.get("email", "")
    username = ctx.prop_store.get("username", "")
    
    # Validate and process
    if not email or "@" not in email:
        await ctx.toast("Invalid email", variant="error")
        return
    
    # Use the values...
    await save_user(email, username)
    await ctx.toast("Saved successfully!")
```

## API Reference

### `ctx.callback(func=None, *, store_as=None, **bound_args)`

Create a callback with optional prop store functionality.

**Parameters:**
- `func` (Callable, optional): The Python function to call. If omitted with `store_as`, creates a store-only callback.
- `store_as` (str | dict, optional): Store directive for capturing event data.
  - `str`: Store the event's `value` under this key
  - `dict`: Map event data keys to store keys (e.g., `{"value": "email", "name": "field"}`)
- `**bound_args`: Arguments to bind to the callback

**Returns:** `Callback` object

### `ctx.prop_store`

A dict-like object containing all values stored via `store_as` directives.

**Methods:**
- `get(key, default=None)`: Get a stored value
- `keys()`: Get all stored keys
- `values()`: Get all stored values
- `items()`: Get all key-value pairs

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

| Feature | ctx.state | ctx.prop_store |
|---------|-----------|----------------|
| Storage location | Backend (Python) | Frontend (Browser) |
| Server roundtrip | Every update | Only on callback invoke |
| Persistence | Across page renders | Until page refresh |
| Use case | App state, complex data | Form inputs, temp values |
| Access pattern | Read/write anytime | Read in callbacks |

### When to Use Which

**Use `ctx.state` when:**
- You need to persist data across page navigation
- You need to trigger UI updates based on state changes
- You're storing complex application state

**Use `ctx.prop_store` when:**
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


async def handle_register(ctx: Context):
    # Get all form values from prop_store
    username = ctx.prop_store.get("username", "")
    email = ctx.prop_store.get("email", "")
    password = ctx.prop_store.get("password", "")
    confirm = ctx.prop_store.get("confirm_password", "")
    
    # Validate
    errors = []
    if len(username) < 3:
        errors.append("Username must be at least 3 characters")
    if "@" not in email:
        errors.append("Invalid email address")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if password != confirm:
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
                                        on_click=ctx.callback(handle_register),
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

5. **Clear sensitive data after use**: The prop store persists until page refresh, so clear sensitive fields after processing if needed

## Limitations

- **Frontend-only storage**: Values are lost on page refresh (use `ctx.state` or `ctx.store` for persistence)
- **No automatic sync**: Unlike `ctx.state`, prop_store values don't trigger re-renders
- **Callback-scoped access**: Values are only available when a callback is invoked
