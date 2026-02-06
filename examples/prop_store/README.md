# Prop Store Example

This example demonstrates the **prop_store** feature for efficient form handling.

## What is Prop Store?

The prop store is a **frontend-only** key-value store that captures values from component events (like input changes) without requiring server roundtrips for each state update.

### Traditional Approach (Without Prop Store)

```python
# Every keystroke triggers a server roundtrip
async def update_field(ctx: Context, name: str, value: str):
    form_data = ctx.state.get("form_data", {})
    form_data[name] = value
    ctx.state.set("form_data", form_data)

Input(
    on_change=ctx.callback(update_field, name="email")  # Server call on every change!
)
```

### New Approach (With Prop Store)

```python
# Values are stored on the frontend - no server calls until submit
Input(
    on_change=ctx.callback(store_as="email")  # Frontend-only!
)

async def handle_submit(ctx: Context):
    email = ctx.prop_store.get("email")  # Access all stored values
```

## Key Benefits

1. **Fewer Server Roundtrips**: Input values are captured on the frontend
2. **Less Boilerplate**: No need for individual state update handlers per field
3. **Better Performance**: No network latency on every keystroke
4. **Simple API**: Just use `store_as="key"` in your callbacks

## Running the Example

```bash
cd examples/prop_store
uvicorn app:app --reload
```

Then open http://127.0.0.1:8000 in your browser.

## How It Works

1. Input components use `on_change=ctx.callback(store_as="key")` to capture values
2. When the user types, values are stored in the frontend prop store (no server call)
3. When the Submit button is clicked, all prop store values are sent with the callback
4. The callback accesses values via `ctx.prop_store.get("key")`

## Advanced Usage

### Store with Custom Key Mapping

```python
# Map event data keys to different store keys
Input(
    on_change=ctx.callback(store_as={"value": "user_email", "name": "field_name"})
)
```

### Store and Call Function

```python
# Store value AND call a validation function
async def validate_email(ctx: Context, value: str):
    # Called on every change, value also stored as "email"
    if "@" not in value:
        await ctx.toast("Invalid email format", variant="warning")

Input(
    on_change=ctx.callback(validate_email, store_as="email")
)
```
