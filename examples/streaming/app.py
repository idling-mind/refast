"""Streaming Example - Demonstrates append_prop for streaming content.

This example demonstrates:
- Streaming text to a Markdown component using append_prop
- Streaming data points to a chart using append_prop
- Using update_props to show streaming indicators
- Simulating LLM-style token streaming

Run this file with:
    python app.py

Then open http://localhost:8000 in your browser.
"""

import asyncio
import random
from datetime import datetime

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Separator,
    Text,
)
from refast.components.shadcn.charts import (
    CartesianGrid,
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
    Line,
    LineChart,
    XAxis,
    YAxis,
)

ui = RefastApp(title="Streaming Demo")


# Sample text to stream (simulating LLM output)
SAMPLE_RESPONSE = """# Hello, I'm streaming!

This text is being streamed **token by token**, just like a large language model would output it.

## Key Features

Here are some things you can do with streaming:

1. **Real-time feedback** - Users see content as it's generated
2. **Better UX** - No waiting for the full response
3. **Efficient updates** - Only send new content, not the entire text

## Code Example

```python
async def stream_response(ctx: Context):
    # Start streaming
    await ctx.update_props("output", {"streaming": True})

    async for chunk in llm.stream(prompt):
        await ctx.append_prop("output", "content", chunk)

    # End streaming
    await ctx.update_props("output", {"streaming": False})
```

## Math Support

Inline math: $E = mc^2$

## Images
![Random Image](https://picsum.photos/300/200)

That's it! The streaming is complete. 🎉
"""


async def stream_markdown(ctx: Context):
    """Stream text to the Markdown component token by token."""
    # Clear previous content and show streaming indicator
    await ctx.update_props("markdown-output", {"content": "", "streaming": True})
    await ctx.update_text("stream-status", "Streaming...")
    await ctx.update_props("stop-streaming", {"disabled": False})
    ctx.state.set("streaming_stopped", False)

    # Simulate token-by-token streaming (like an LLM)
    words = SAMPLE_RESPONSE.split(" ")
    for i, word in enumerate(words):
        # Add space before word (except first)
        chunk = word if i == 0 else " " + word
        await ctx.append_prop("markdown-output", "content", chunk)

        # Simulate varying token generation speed
        await asyncio.sleep(random.uniform(0.02, 0.08))
        if ctx.state.get("streaming_stopped", False):
            await ctx.show_toast("Streaming stopped by user.", "info")
            break

    # Done streaming
    await ctx.update_props("markdown-output", {"streaming": False})
    await ctx.update_text("stream-status", "Complete!")
    await ctx.update_props("stop-streaming", {"disabled": True})
    await ctx.show_toast("Streaming markdown complete!", "success")

async def stop_streaming(ctx: Context):
    """Stop the streaming process (simulated)."""
    # In a real scenario, you would have to manage the streaming task
    # Here we just update the status
    ctx.state.set("streaming_stopped", True)
    await ctx.update_props("markdown-output", {"streaming": False})
    await ctx.update_text("stream-status", "Streaming Stopped")


async def clear_markdown(ctx: Context):
    """Clear the Markdown content."""
    await ctx.update_props("markdown-output", {"content": ""})
    await ctx.update_text("stream-status", "Ready")


# Chart data storage (will be modified during streaming)
chart_data = []


def get_initial_chart_data():
    """Get empty initial chart data."""
    return []


async def stream_chart_data(ctx: Context):
    """Stream data points to the chart."""
    global chart_data

    # Reset chart data
    chart_data = []

    await ctx.update_text("chart-status", "Streaming data...")

    # Clear chart by updating with empty data
    await ctx.update_props("live-chart", {"data": []})

    # Stream 30 data points
    for i in range(30):
        # Generate new data point
        timestamp = datetime.now().strftime("%H:%M:%S")
        value = 50 + random.uniform(-20, 20) + (i * 1.0)  # Trending upward with noise

        new_point = {"time": timestamp, "value": round(value, 1)}
        chart_data.append(new_point)

        # Update chart with appended data point
        await ctx.append_prop("live-chart", "data", new_point)

        # Simulate data arrival interval
        await asyncio.sleep(1)

    await ctx.update_text("chart-status", "Complete! 30 data points streamed.")
    await ctx.show_toast("Chart data streaming complete!", "success")


async def add_single_point(ctx: Context):
    """Add a single random data point to the chart."""
    global chart_data

    timestamp = datetime.now().strftime("%H:%M:%S")

    # Base value on last point if exists, otherwise start at 50
    base = chart_data[-1]["value"] if chart_data else 50
    value = base + random.uniform(-5, 5)

    new_point = {"time": timestamp, "value": round(value, 1)}
    chart_data.append(new_point)

    # Keep only last 20 points for readability
    if len(chart_data) > 20:
        chart_data = chart_data[-20:]
        # Need to replace all data when trimming
        await ctx.update_props("live-chart", {"data": chart_data})
    else:
        # Just append the new point
        await ctx.append_prop("live-chart", "data", new_point)


async def clear_chart(ctx: Context):
    """Clear the chart data."""
    global chart_data
    chart_data = []
    await ctx.update_props("live-chart", {"data": []})
    await ctx.update_text("chart-status", "Ready")


# Chart configuration
chart_config = ChartConfig(
    label="Value",
    color="hsl(var(--chart-1))",
)


@ui.page("/")
def home(ctx: Context):
    """Home page with streaming demos."""
    return Container(
        class_name="max-w-4xl mx-auto py-8 px-4",
        children=[
            # Header
            Column(
                class_name="space-y-2 mb-8",
                children=[
                    Heading("Streaming Demo"),
                    Text(
                        "Streaming content with append_prop and real-time chart updates",
                        class_name="text-muted-foreground text-lg",
                    ),
                ],
            ),
            # Markdown Streaming Demo
            Card(
                class_name="mb-6",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Markdown Streaming"),
                                            CardDescription(
                                                "Stream text token-by-token, like an LLM response"
                                            ),
                                        ]
                                    ),
                                    Badge(
                                        "Ready",
                                        id="stream-status",
                                        variant="secondary",
                                    ),
                                ],
                            ),
                        ]
                    ),
                    CardContent(
                        class_name="space-y-4",
                        children=[
                            Row(
                                gap=2,
                                class_name="mb-4",
                                children=[
                                    Button(
                                        "Stream Response",
                                        on_click=ctx.callback(stream_markdown),
                                        variant="default",
                                    ),
                                    Button(
                                        "Stop Streaming",
                                        id="stop-streaming",
                                        on_click=ctx.callback(stop_streaming),
                                        variant="destructive",
                                        disabled=True,
                                    ),
                                    Button(
                                        "Clear",
                                        on_click=ctx.callback(clear_markdown),
                                        variant="outline",
                                    ),
                                ],
                            ),
                            Separator(),
                            Container(
                                class_name="min-h-[300px] p-4 border rounded-lg bg-muted/30",
                                children=[
                                    Markdown(
                                        id="markdown-output",
                                        content=(
                                            "Click 'Stream Response' to see streaming in action...",
                                        ),
                                        class_name="prose-sm",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Chart Streaming Demo
            Card(
                class_name="mb-6",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                class_name="justify-between items-center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Chart Data Streaming"),
                                            CardDescription(
                                                "Stream data points to a live chart using"
                                                " append_prop"
                                            ),
                                        ]
                                    ),
                                    Badge(
                                        "Ready",
                                        id="chart-status",
                                        variant="secondary",
                                    ),
                                ],
                            ),
                        ]
                    ),
                    CardContent(
                        class_name="space-y-4",
                        children=[
                            Row(
                                gap=2,
                                class_name="mb-4",
                                children=[
                                    Button(
                                        "Stream 30 Points",
                                        on_click=ctx.callback(stream_chart_data),
                                        variant="default",
                                    ),
                                    Button(
                                        "Add Single Point",
                                        on_click=ctx.callback(add_single_point),
                                        variant="outline",
                                    ),
                                    Button(
                                        "Clear",
                                        on_click=ctx.callback(clear_chart),
                                        variant="outline",
                                    ),
                                ],
                            ),
                            ChartContainer(
                                config={"value": chart_config},
                                class_name="h-[350px] w-full",
                                children=[
                                    LineChart(
                                        id="live-chart",
                                        animation_duration=100,
                                        data=get_initial_chart_data(),
                                        margin={"top": 20, "right": 20, "left": 20, "bottom": 20},
                                        children=[
                                            CartesianGrid(stroke_dasharray="3 3"),
                                            XAxis(
                                                data_key="time",
                                                tick_line=False,
                                                axis_line=False,
                                                tick_margin=8,
                                            ),
                                            YAxis(
                                                tick_line=False,
                                                axis_line=False,
                                                tick_margin=8,
                                            ),
                                            ChartTooltip(
                                                content=ChartTooltipContent(
                                                    hide_label=True,
                                                ),
                                            ),
                                            Line(
                                                data_key="value",
                                                type="natural",
                                                stroke="var(--color-value)",
                                                stroke_width=2,
                                                dot=True,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Usage Information
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("How It Works"),
                        ]
                    ),
                    CardContent(
                        children=[
                            Markdown(
                                content="""
## Streaming Text with `append_prop`

```python
async def stream_response(ctx: Context):
    # Clear and start streaming indicator
    await ctx.update_props("output", {"content": "", "streaming": True})

    # Stream tokens
    async for chunk in llm.stream(prompt):
        await ctx.append_prop("output", "content", chunk)

    # Done
    await ctx.update_props("output", {"streaming": False})
```

## Streaming Chart Data with `append_prop`

```python
async def stream_chart_data(ctx: Context):
    for point in data_stream:
        # Append data point to chart
        await ctx.append_prop("chart-id", "data", point)
        await asyncio.sleep(0.1)
```

## Key Methods

| Method | Use Case |
|--------|----------|
| `ctx.append_prop(id, prop, value)` | Append text to string props, items to array props |
| `ctx.update_props(id, props)` | Update any props (streaming indicators, etc.) |
| `ctx.append(id, component)` | Append child components (also works with strings) |
""",
                                allow_latex=False,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# Create FastAPI app
app = FastAPI()
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
