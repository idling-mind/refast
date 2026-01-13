"""Connection Status Example - WebSocket Disconnection Indicator.

This example demonstrates the ConnectionStatus component which displays
an indicator when the WebSocket connection is lost and fires callbacks
on connection state changes.

Run with:
    cd examples/connection_status
    uvicorn app:app --reload

To test disconnection:
    1. Open the app in browser
    2. Stop the uvicorn server
    3. Observe the disconnection indicator appear
    4. Restart the server
    5. Observe the reconnection (indicator disappears, callbacks fire)
"""

from datetime import datetime

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Alert,
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Code,
    Column,
    ConnectionStatus,
    Container,
    Grid,
    Heading,
    Icon,
    Paragraph,
    Row,
    Spinner,
    Text,
    ThemeSwitcher,
)

# Create the Refast app
ui = RefastApp(title="Connection Status Demo")
app = FastAPI()


# ============================================================================
# Backend Callbacks
# ============================================================================


async def handle_disconnect(ctx: Context):
    """Handle disconnection event on the backend."""
    # This would typically log the event or clean up resources
    print(f"[{datetime.now().isoformat()}] User disconnected!")
    # Note: Since user is disconnected, we can't send them updates here
    # This is more for cleanup/logging purposes


async def handle_reconnect(ctx: Context):
    """Handle reconnection event on the backend."""
    print(f"[{datetime.now().isoformat()}] User reconnected!")
    # Show a welcome back toast
    await ctx.show_toast(
        "Welcome back! Connection restored.",
        variant="success",
        duration=3000,
    )


async def manual_disconnect_test(ctx: Context):
    """Manually test the disconnection indicator by showing a toast."""
    await ctx.show_toast(
        "To test disconnection, stop the server (Ctrl+C) and restart it.",
        variant="info",
        duration=5000,
    )


# ============================================================================
# Main Page
# ============================================================================


@ui.page("/")
def home(ctx: Context):
    """Main page with ConnectionStatus examples."""
    return Container(
        class_name="min-h-screen bg-background",
        children=[
            # Header
            Row(
                class_name="border-b px-6 py-4 mb-6",
                children=[
                    Column(
                        class_name="flex-1",
                        children=[
                            Heading("Connection Status Demo", level=1),
                            Text(
                                "Demonstrates WebSocket disconnection detection",
                                class_name="text-muted-foreground",
                            ),
                        ],
                    ),
                    ThemeSwitcher(),
                ],
            ),
            # Main content
            Column(
                class_name="max-w-4xl mx-auto",
                gap=4,
                children=[
                    # Introduction Card
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("How It Works"),
                                    CardDescription(
                                        "The ConnectionStatus component monitors the WebSocket "
                                        "connection and displays an indicator when disconnected."
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Paragraph(
                                        "Try these steps to see it in action:",
                                        class_name="mb-4",
                                    ),
                                    Column(
                                        class_name="gap-2 pl-4",
                                        children=[
                                            Row(
                                                class_name="items-center",
                                                gap=2,
                                                children=[
                                                    Badge("1", variant="outline"),
                                                    Text(
                                                        "Stop the uvicorn server (Ctrl+C in the terminal)"
                                                    ),
                                                ],
                                            ),
                                            Row(
                                                class_name="items-center",
                                                gap=2,
                                                children=[
                                                    Badge("2", variant="outline"),
                                                    Text(
                                                        "Watch the disconnection indicator appear "
                                                        "(bottom-right corner)"
                                                    ),
                                                ],
                                            ),
                                            Row(
                                                class_name="items-center",
                                                children=[
                                                    Badge("3", variant="outline"),
                                                    Text(
                                                        "Restart the server: uvicorn app:app --reload"
                                                    ),
                                                ],
                                            ),
                                            Row(
                                                class_name="items-center",
                                                gap=2,
                                                children=[
                                                    Badge("4", variant="outline"),
                                                    Text(
                                                        "See the reconnection toast notification"
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Examples Grid
                    Grid(
                        columns=2,
                        gap=4,
                        children=[
                            # Example 1: Default ConnectionStatus
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Default Indicator"),
                                            CardDescription(
                                                "Built-in disconnection indicator with "
                                                "reconnection status"
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Paragraph(
                                                "When no children are provided, ConnectionStatus "
                                                "shows a default indicator with connection state.",
                                                class_name="text-sm text-muted-foreground mb-4",
                                            ),
                                            Alert(
                                                title="Active Now",
                                                message="The default indicator is active in the "
                                                "bottom-right corner. It's invisible while "
                                                "connected.",
                                                variant="info",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            # Example 2: Custom Children
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Custom Content"),
                                            CardDescription(
                                                "Provide custom children to display your own "
                                                "disconnection UI"
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Paragraph(
                                                "You can pass any components as children. "
                                                "They'll only be visible when disconnected.",
                                                class_name="text-sm text-muted-foreground mb-4",
                                            ),
                                            Alert(
                                                title="Example",
                                                message="See the top-left indicator with custom "
                                                "content (only visible when disconnected).",
                                                variant="default",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            # Example 3: Callbacks
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Event Callbacks"),
                                            CardDescription(
                                                "Fire callbacks on disconnect/reconnect events"
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Paragraph(
                                                "Both Python (backend) and JavaScript (frontend) "
                                                "callbacks are supported.",
                                                class_name="text-sm text-muted-foreground mb-4",
                                            ),
                                            Column(
                                                gap=2,
                                                children=[
                                                    Row(
                                                        class_name="items-center",
                                                        gap=2,
                                                        children=[
                                                            Badge(
                                                                "Python", variant="default"
                                                            ),
                                                            Text(
                                                                "on_disconnect, on_reconnect",
                                                                class_name="text-sm",
                                                            ),
                                                        ],
                                                    ),
                                                    Row(
                                                        class_name="items-center",
                                                        gap=2,
                                                        children=[
                                                            Badge(
                                                                "JavaScript",
                                                                variant="secondary",
                                                            ),
                                                            Text(
                                                                "js_on_disconnect, js_on_reconnect",
                                                                class_name="text-sm",
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            # Example 4: Positions
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Positioning"),
                                            CardDescription(
                                                "Choose where the indicator appears"
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Paragraph(
                                                "Available positions:",
                                                class_name="text-sm text-muted-foreground mb-2",
                                            ),
                                            Row(
                                                class_name="items-center flex-wrap",
                                                gap=2,
                                                children=[
                                                    Badge("top-left", variant="outline"),
                                                    Badge("top-right", variant="outline"),
                                                    Badge("bottom-left", variant="outline"),
                                                    Badge(
                                                        "bottom-right", variant="default"
                                                    ),
                                                    Badge("inline", variant="outline"),
                                                ],
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                    ),
                    # Inline Example
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Inline Position Example"),
                                    CardDescription(
                                        "Use position='inline' to embed the status in your layout"
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Row(
                                        class_name="gap-4 items-center",
                                        children=[
                                            Text("Connection Status:"),
                                            # This inline indicator shows connection status
                                            # in the document flow
                                            ConnectionStatus(
                                                position="inline",
                                                children_connected=[
                                                    Row(
                                                        class_name="gap-2 items-center px-3 py-1 "
                                                        "rounded-full bg-green-500/10",
                                                        children=[
                                                            Icon(
                                                                "wifi",
                                                                class_name="h-4 w-4 text-green-600",
                                                            ),
                                                            Text(
                                                                "Online",
                                                                class_name="text-sm font-medium "
                                                                "text-green-600",
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                                children_disconnected=[
                                                    Row(
                                                        class_name="gap-2 items-center px-3 py-1 "
                                                        "rounded-full bg-destructive/10",
                                                        children=[
                                                            Icon(
                                                                "wifi-off",
                                                                class_name="h-4 w-4 text-destructive",
                                                            ),
                                                            Text(
                                                                "Offline",
                                                                class_name="text-sm font-medium "
                                                                "text-destructive",
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Paragraph(
                                        [
                                            "The inline indicator above shows 'Online' when "
                                            "connected and 'Offline' when disconnected. "
                                            "Try stopping the server to see it change!"
                                        ],
                                        class_name="text-sm text-muted-foreground mt-4",
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Code Example
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Code Example"),
                                    CardDescription("How to use ConnectionStatus in your app"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Paragraph(
                                        "Add the ConnectionStatus component to your page:",
                                        class_name="mb-4",
                                    ),
                                    Code(
                                        inline=False,
                                        language="python",
                                        code="""ConnectionStatus(
    position="bottom-right",
    on_disconnect=ctx.callback(handle_disconnect),
    on_reconnect=ctx.callback(handle_reconnect),
    js_on_disconnect=ctx.js("console.log('Lost connection')"),
    js_on_reconnect=ctx.js("console.log('Back online!')"),
    children_connected=[
        Badge("Online", variant="success")
    ],
    children_disconnected=[
        Alert(
            title="Connection Lost",
            message="Reconnecting...",
            variant="destructive"
        )
    ]
)"""
                                    )
                                ]
                            ),
                        ]
                    ),
                    # Test Button
                    Row(
                        class_name="justify-center mb-6",
                        children=[
                            Button(
                                "How to Test Disconnection",
                                on_click=ctx.callback(manual_disconnect_test),
                                variant="outline",
                            ),
                        ],
                    ),
                ],
            ),
            # ========================================================================
            # ConnectionStatus Components
            # ========================================================================
            # Default indicator (bottom-right) - invisible when connected
            ConnectionStatus(
                position="bottom-right",
                on_disconnect=ctx.callback(handle_disconnect),
                on_reconnect=ctx.callback(handle_reconnect),
                js_on_disconnect=ctx.js("console.log('[JS] Disconnected!')"),
                js_on_reconnect=ctx.js("console.log('[JS] Reconnected!')"),
                debounce_ms=500,
            ),
            # Custom indicator (top-left) with custom content
            ConnectionStatus(
                position="top-left",
                children_disconnected=[
                    Card(
                        class_name="shadow-lg border-destructive",
                        children=[
                            CardContent(
                                class_name="p-4",
                                children=[
                                    Row(
                                        class_name="items-center",
                                        gap=3,
                                        children=[
                                            Spinner(
                                                size="sm",
                                                class_name="text-destructive",
                                            ),
                                            Column(
                                                gap=1,
                                                children=[
                                                    Text(
                                                        "Connection Lost",
                                                        class_name="font-semibold text-destructive",
                                                    ),
                                                    Text(
                                                        "Attempting to reconnect...",
                                                        class_name="text-sm text-muted-foreground",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# Include the Refast router in the FastAPI app
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)