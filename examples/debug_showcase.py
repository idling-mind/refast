from fastapi import FastAPI, HTTPException

from refast import Context, RefastApp
from refast.components import (
    Button,
    Card,
    CardContent,
    CardHeader,
    Center,
    Column,
    Container,
    Heading,
    Input,
    Row,
    Text,
    ThemeSwitcher,
)

# Start Refast app with debug mode enabled
ui = RefastApp(title="Refast DevTools Showcase", debug=True)


# --- Normal WebSocket traffic ---
async def handle_greet(ctx: Context, name: str):
    """Simple callback demonstrating normal request/response flow."""
    greeting = f"Hello, {name}!" if name else "Hello, stranger!"
    await ctx.update_text("greeting_text", greeting)
    await ctx.show_toast("Greeting updated!", variant="success")


# --- Deliberate Errors for testing ---
async def raise_python_error(ctx: Context):
    """Trigger a Python runtime exception."""
    raise ValueError(
        "This is a deliberate backend error raised to demonstrate Python Callback Exception tracking."
    )


async def raise_http_error(ctx: Context):
    """Trigger a FastAPI HTTP exception (e.g., simulate rate limit/validation failure)."""
    raise HTTPException(
        status_code=429,
        detail="Too many requests! This showcases Python HTTP Exception tracking in the DevTools console.",
    )


@ui.page("/")
def debug_showcase_page(ctx: Context):
    # We define a custom raw dict with an unknown component type to test
    # client-side missing component definition tracking.
    invalid_component = {
        "type": "NonExistentSuperWidget",
        "id": "missing_widget_id",
        "props": {"title": "Unsupported Widget"},
    }

    return Container(
        [
            Center(
                Column(
                    [
                        Heading("Refast DevTools Showcase", level=1, class_name="mb-2"),
                        Text(
                            "Use this page to test various WebSocket traffic and error scenarios in the DevTools Panel.",
                            class_name="text-muted-foreground mb-6 text-center max-w-lg",
                        ),
                    ],
                    align="center",
                )
            ),
            Row(
                [
                    # Card 1: Normal Traffic & Replay
                    Card(
                        [
                            CardHeader(
                                title="1. Normal Traffic & Replays",
                                description=(
                                    "Test standard WebSocket traffic and inspect collapsible payloads. "
                                    "You can click 'Replay Msg' on the outgoing callback to repeat this greet."
                                ),
                            ),
                            CardContent(
                                Column(
                                    [
                                        Input(
                                            placeholder="Enter your name...",
                                            on_change=ctx.save_prop("visitor_name"),
                                            class_name="mb-3",
                                        ),
                                        Button(
                                            "Greet Visitor",
                                            on_click=ctx.callback(handle_greet, props=["visitor_name"]),
                                            class_name="w-full",
                                        ),
                                        Text(
                                            "Waiting for greet...",
                                            id="greeting_text",
                                            class_name="mt-3 font-semibold text-center text-indigo-400",
                                        ),
                                    ]
                                )
                            ),
                        ],
                        class_name="flex-1 min-w-[300px]",
                    ),
                    # Card 2: Backend Exceptions
                    Card(
                        [
                            CardHeader(
                                title="2. Backend Exceptions",
                                description=(
                                    "Trigger standard Python exceptions or HTTPExceptions. "
                                    "Check the 'Errors' tab for full Python tracebacks."
                                ),
                            ),
                            CardContent(
                                Column(
                                    [
                                        Button(
                                            "Trigger Python Exception",
                                            on_click=ctx.callback(raise_python_error),
                                            variant="destructive",
                                            class_name="w-full mb-3",
                                        ),
                                        Button(
                                            "Trigger HTTP Exception (429)",
                                            on_click=ctx.callback(raise_http_error),
                                            variant="outline",
                                            class_name="w-full text-rose-500 hover:text-rose-600 border-rose-500/20 hover:bg-rose-500/10",
                                        ),
                                    ]
                                )
                            ),
                        ],
                        class_name="flex-1 min-w-[300px]",
                    ),
                ],
                class_name="gap-6 mb-6",
            ),
            Row(
                [
                    # Card 3: Client-side Errors
                    Card(
                        [
                            CardHeader(
                                title="3. Client-side JS / DOM Errors",
                                description = (
                                    "Test client-side runtime errors. Captures JS syntax errors, "
                                    "missing components, or nonexistent bound methods in DOM."
                                )
                            ),
                            CardContent(
                                Column(
                                    [
                                        # Trigger client-side JS Callback error
                                        Button(
                                            "Trigger JS Callback Exception",
                                            on_click=ctx.js(
                                                "const obj = {}; obj.nonexistent.method();"
                                            ),
                                            variant="secondary",
                                            class_name="w-full mb-3",
                                        ),
                                        # Trigger Missing Element (bound method)
                                        Button(
                                            "Call Method on Non-existent ID",
                                            on_click=ctx.bound_js(
                                                target_id="missing_element_123",
                                                method_name="click",
                                            ),
                                            variant="outline",
                                            class_name="w-full mb-3",
                                        ),
                                        # Trigger Missing Method on Existing Element
                                        Button(
                                            "Call Missing Method on Heading",
                                            on_click=ctx.bound_js(
                                                target_id="greeting_text",
                                                method_name="fakeMethodName",
                                            ),
                                            variant="outline",
                                            class_name="w-full",
                                        ),
                                    ]
                                )
                            ),
                        ],
                        class_name="flex-1 min-w-[300px]",
                    ),
                    # Card 4: Component / UI Errors
                    Card(
                        [
                            CardHeader(
                                title="4. Missing Component Definitions",
                                description=(
                                    "Test how missing component definitions are caught "
                                    "and logged in the DevTools console."
                                ),
                            ),
                            CardContent(
                                Column(
                                    [
                                        Text(
                                            "Below is a placeholder holding an unregistered component type:",
                                            class_name="text-xs text-muted-foreground mb-2",
                                        ),
                                        # Render the invalid component
                                        invalid_component,
                                    ]
                                )
                            ),
                        ],
                        class_name="flex-1 min-w-[300px]",
                    ),
                ],
                class_name="gap-6 mb-6",
            ),
            Center(ThemeSwitcher()),
        ],
        class_name="p-8 max-w-6xl mx-auto",
    )


# FastAPI mount
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    print("Starting Refast Developer Tools Showcase application on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
