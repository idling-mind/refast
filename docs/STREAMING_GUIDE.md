# Streaming Guide

This guide covers streaming content in Refast applications, including streaming text to components and real-time data updates.

## Overview

Refast provides several methods for incrementally updating component content:

| Method | Use Case |
|--------|----------|
| `ctx.append_prop(id, prop, value)` | Append text to string props, extend array props |
| `ctx.update_props(id, props)` | Update any props (streaming indicators, etc.) |
| `ctx.call_bound_js(id, method, ...)` | Call component methods (chart setOption, etc.) |
| `ctx.append(id, component)` | Append child components (works with strings too) |

## Streaming Text to Markdown

The most common streaming use case is displaying LLM responses token-by-token:

```python
from refast import Context, RefastApp
from refast.components import Markdown, Button, Container

ui = RefastApp()

async def stream_llm_response(ctx: Context):
    """Stream tokens from an LLM to a Markdown component."""
    # 1. Clear content and show streaming indicator
    await ctx.update_props("output", {
        "content": "",
        "streaming": True  # Optional: for UI indicators
    })
    
    # 2. Stream tokens one by one
    async for chunk in llm.stream(prompt="Tell me a story"):
        await ctx.append_prop("output", "content", chunk)
    
    # 3. Signal streaming complete
    await ctx.update_props("output", {"streaming": False})

@ui.page("/")
def home(ctx: Context):
    return Container(
        children=[
            Button("Generate Story", on_click=ctx.callback(stream_llm_response)),
            Markdown(id="output", content="Click the button to generate...")
        ]
    )
```

## How `append_prop` Works

The `append_prop` method intelligently handles different prop types:

### String Props (Concatenation)

For string props like `content` in Markdown, values are concatenated:

```python
# Before: content = "Hello"
await ctx.append_prop("my-markdown", "content", " World")
# After: content = "Hello World"
```

### Array Props (Append/Extend)

For array props, single items are pushed, arrays are extended:

```python
# Append single item
# Before: data = [1, 2, 3]
await ctx.append_prop("my-list", "data", 4)
# After: data = [1, 2, 3, 4]

# Extend with array
# Before: data = [1, 2]
await ctx.append_prop("my-list", "data", [3, 4, 5])
# After: data = [1, 2, 3, 4, 5]
```

### Uninitialized Props

If the prop doesn't exist yet, it's initialized appropriately:

```python
# String value -> string prop
await ctx.append_prop("id", "content", "Hello")  # content = "Hello"

# Array value -> array prop
await ctx.append_prop("id", "data", [1, 2])  # data = [1, 2]

# Single non-string value -> array with that value
await ctx.append_prop("id", "items", {"x": 1})  # items = [{"x": 1}]
```

## Streaming Chart Data

For charts, use `append_prop` to append data points:

```python
from refast.components.shadcn.charts import (
    ChartConfig,
    ChartContainer,
    Line,
    LineChart,
    XAxis,
    YAxis,
)

# Store for accumulated data
chart_data = []

async def stream_sensor_data(ctx: Context):
    """Stream real-time sensor data to a chart."""
    global chart_data
    chart_data = []
    
    # Clear chart
    await ctx.update_props("sensor-chart", {"data": []})
    
    async for reading in sensor.stream():
        # Create new data point
        new_point = {"time": reading.timestamp, "value": reading.value}
        chart_data.append(new_point)
        
        # Append to chart
        await ctx.append_prop("sensor-chart", "data", new_point)

@ui.page("/")
def dashboard(ctx: Context):
    chart_config = ChartConfig(
        value={"label": "Value", "color": "hsl(var(--chart-1))"},
    )
    
    return Container(
        children=[
            Button("Start Streaming", on_click=ctx.callback(stream_sensor_data)),
            ChartContainer(
                config=chart_config,
                class_name="h-[400px] w-full",
                children=[
                    LineChart(
                        id="sensor-chart",
                        data=[],
                        children=[
                            XAxis(data_key="time"),
                            YAxis(),
                            Line(data_key="value", type="monotone"),
                        ],
                    ),
                ],
            ),
        ]
    )
```

## Streaming with Status Indicators

Show users when streaming is in progress:

```python
async def stream_with_status(ctx: Context):
    # Show streaming status
    await ctx.update_props("status-badge", {"children": ["Generating..."]})
    await ctx.update_props("output", {"content": "", "streaming": True})
    
    try:
        async for chunk in generate_content():
            await ctx.append_prop("output", "content", chunk)
    finally:
        # Always clean up status
        await ctx.update_props("status-badge", {"children": ["Complete"]})
        await ctx.update_props("output", {"streaming": False})
```

## Appending to Children

Use `ctx.append()` to add components or strings to a container's children:

```python
async def add_message(ctx: Context):
    """Add a new message to the chat."""
    message = ctx.state.get("input", "")
    
    # Append text directly to children
    await ctx.append("messages", f"\n{username}: {message}")
    
    # Or append a component
    await ctx.append("messages", Text(f"{username}: {message}"))
```

## Performance Considerations

### Batch Updates for High-Frequency Streams

For very high-frequency updates (>100/second), consider batching:

```python
async def stream_with_batching(ctx: Context):
    buffer = ""
    last_update = time.time()
    
    async for chunk in high_frequency_stream():
        buffer += chunk
        
        # Update at most 30 times per second
        if time.time() - last_update > 0.033:
            await ctx.append_prop("output", "content", buffer)
            buffer = ""
            last_update = time.time()
    
    # Flush remaining buffer
    if buffer:
        await ctx.append_prop("output", "content", buffer)
```

### Limiting Data Size for Charts

For real-time charts, limit the number of visible points:

```python
MAX_POINTS = 100

async def add_data_point(ctx: Context):
    chart_data["values"].append(new_value)
    chart_data["timestamps"].append(new_timestamp)
    
    # Keep only last N points
    if len(chart_data["values"]) > MAX_POINTS:
        chart_data["values"] = chart_data["values"][-MAX_POINTS:]
        chart_data["timestamps"] = chart_data["timestamps"][-MAX_POINTS:]
    
    await ctx.call_bound_js("chart", "setOption", {
        "xAxis": {"data": chart_data["timestamps"]},
        "series": [{"data": chart_data["values"]}]
    })
```

## Complete Example

See `examples/streaming/app.py` for a complete working example that demonstrates:

- Streaming text to a Markdown component
- Real-time chart data streaming
- Status indicators during streaming
- Proper cleanup on completion

Run it with:

```bash
cd examples/streaming
python app.py
```

Then open http://localhost:8000 in your browser.
