"""Basic Refast Example - Counter Application.

This example demonstrates:
- Basic page routing with @ui.page
- Component rendering (Container, Text, Button)
- Callback handling with ctx.callback
- State management with ctx.state
"""
from ast import In

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Input,
    Row,
    Text,
)

# Create the Refast app
ui = RefastApp(title="Counter Example")


# Define callback handlers
async def increment(ctx: Context):
    """Increment the counter."""
    count = ctx.state.get("count", 0)
    ctx.state.set("count", count + 1)
    print("Incremented count to", ctx.state.get("count"))

    # Update just the text content
    await ctx.refresh()


async def decrement(ctx: Context):
    """Decrement the counter."""
    count = ctx.state.get("count", 0)
    ctx.state.set("count", max(0, count - 1))
    print("Decremented count to", ctx.state.get("count"))

    # Update just the text content
    await ctx.refresh()


async def reset(ctx: Context):
    """Reset the counter to zero."""
    ctx.state.set("count", 0)
    print("Reset count to", ctx.state.get("count"))

    # Update just the text content
    await ctx.refresh()

async def set_counter(ctx: Context):
    """Set the counter to a specific value from the input."""
    value = ctx.event_data.get("value", "")
    try:
        value = int(value)
        ctx.state.set("count", max(0, value))
        await ctx.refresh()
    except ValueError:
        print("Invalid input for count:", value)

# Define the main page
@ui.page("/")
def home(ctx: Context):
    """Home page with a counter."""
    count = ctx.state.get("count", 0)

    return Container(
        id="main-container",
        class_name="mt-10",
        style={"maxWidth": "28rem", "marginLeft": "auto", "marginRight": "auto"},
        children=[
            Card(
                id="counter-card",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Counter Example"),
                            CardDescription("A simple counter to demonstrate Refast basics"),
                        ]
                    ),
                    CardContent(
                        id="card-content",
                        children=[
                            Column(
                                id="counter-column",
                                gap=4,
                                children=[
                                    # Count display
                                    Container(
                                        id="count-display",
                                        class_name="text-center py-8",
                                        children=[
                                            Text(
                                                f"{count}",
                                                id="count-value",
                                                class_name="font-bold text-primary",
                                                style={"fontSize": "3.75rem", "lineHeight": "1"},
                                            )
                                        ],
                                    ),
                                    # Buttons row
                                    Row(
                                        id="buttons-row",
                                        gap=2,
                                        justify="center",
                                        children=[
                                            Button(
                                                "−",
                                                id="decrement-btn",
                                                variant="outline",
                                                size="lg",
                                                on_click=ctx.callback(decrement),
                                            ),
                                            Button(
                                                "+",
                                                id="increment-btn",
                                                variant="primary",
                                                size="lg",
                                                on_click=ctx.callback(increment),
                                            ),
                                        ],
                                    ),
                                    # Reset button
                                    Row(
                                        id="reset-row",
                                        justify="center",
                                        children=[
                                            Button(
                                                "Reset",
                                                id="reset-btn",
                                                variant="ghost",
                                                on_click=ctx.callback(reset),
                                            ),
                                        ],
                                    ),
                                    Input(
                                        id="input-count",
                                        type="number",
                                        placeholder="Set count",
                                        value=str(count),
                                        on_change=ctx.callback(set_counter),
                                    )
                                ],
                            ),

                        ]
                    ),
                ],
            )
        ],
    )

# Create the FastAPI app and mount Refast
app = FastAPI(title="Refast Basic Example")
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
