"""Basic Refast Example - Counter Application.

This example demonstrates:
- Basic page routing with @ui.page
- Component rendering (Container, Text, Button)
- Callback handling with ctx.callback
- State management with ctx.state
"""

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
    await ctx.update_text("count-value", str(ctx.state.get("count")))


async def decrement(ctx: Context):
    """Decrement the counter."""
    count = ctx.state.get("count", 0)
    ctx.state.set("count", max(0, count - 1))
    print("Decremented count to", ctx.state.get("count"))

    # Update just the text content
    await ctx.update_text("count-value", str(ctx.state.get("count")))


async def reset(ctx: Context):
    """Reset the counter to zero."""
    ctx.state.set("count", 0)
    print("Reset count to", ctx.state.get("count"))

    # Update just the text content
    await ctx.update_text("count-value", str(ctx.state.get("count")))


# Define the main page
@ui.page("/")
def home(ctx: Context):
    """Home page with a counter."""
    count = ctx.state.get("count", 0)

    return Container(
        id="main-container",
        class_name="max-w-md mx-auto mt-10",
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
                        children=[
                            Column(
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
                                                class_name="text-6xl font-bold text-blue-600",
                                            )
                                        ],
                                    ),
                                    # Buttons row
                                    Row(
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
                                ],
                            )
                        ]
                    ),
                ],
            )
        ],
    )


@ui.page("/about")
def about(ctx: Context):
    """About page."""
    return Container(
        id="about-container",
        class_name="max-w-md mx-auto mt-10",
        children=[
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("About Refast"),
                            CardDescription("Python + React UI Framework"),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Text(
                                        "Refast is a Python-first web UI framework that "
                                        "combines FastAPI on the backend with React on "
                                        "the frontend."
                                    ),
                                    Text(
                                        "Key features include:",
                                    ),
                                    Column(
                                        gap=1,
                                        children=[
                                            Text("• Type-safe components"),
                                            Text("• Real-time updates via WebSocket"),
                                            Text("• Session management"),
                                            Text("• Built-in security features"),
                                        ],
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            )
        ],
    )


# Create the FastAPI app and mount Refast
app = FastAPI(title="Refast Basic Example")
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
