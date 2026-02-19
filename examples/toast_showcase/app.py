"""Toast Showcase Example - Demonstrating Sonner Toast Features.

This example demonstrates all the toast notification features available in Refast
using the Sonner library.

Run with:
    cd examples/toast_showcase
    uvicorn app:app --reload
"""

import asyncio

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
    Grid,
    Heading,
    Row,
    Text,
    ThemeSwitcher,
)

# Create the Refast app
ui = RefastApp(title="Toast Showcase")
app = FastAPI()


# ============================================================================
# Basic Toast Callbacks
# ============================================================================


async def show_default_toast(ctx: Context):
    """Show a basic default toast."""
    await ctx.show_toast("This is a default toast notification")


async def show_success_toast(ctx: Context):
    """Show a success toast."""
    await ctx.show_toast("Operation completed successfully!", variant="success")


async def show_error_toast(ctx: Context):
    """Show an error toast."""
    await ctx.show_toast("Something went wrong!", variant="error")


async def show_warning_toast(ctx: Context):
    """Show a warning toast."""
    await ctx.show_toast("Please review your input", variant="warning")


async def show_info_toast(ctx: Context):
    """Show an info toast."""
    await ctx.show_toast("New features are available", variant="info")


async def show_loading_toast(ctx: Context):
    """Show a loading toast."""
    await ctx.show_toast("Processing your request...", variant="loading")


# ============================================================================
# Toast with Description
# ============================================================================


async def show_toast_with_description(ctx: Context):
    """Show a toast with a description."""
    await ctx.show_toast(
        "File uploaded",
        variant="success",
        description="Your file 'document.pdf' has been uploaded successfully.",
    )


async def show_error_with_description(ctx: Context):
    """Show an error toast with details."""
    await ctx.show_toast(
        "Upload failed",
        variant="error",
        description="The file exceeds the maximum size of 10MB. Please try a smaller file.",
    )


# ============================================================================
# Toast Duration Options
# ============================================================================


async def show_short_toast(ctx: Context):
    """Show a toast that disappears quickly (1 second)."""
    await ctx.show_toast(
        "Quick message!",
        duration=1000,
        description="This toast disappears in 1 second",
    )


async def show_long_toast(ctx: Context):
    """Show a toast that stays longer (10 seconds)."""
    await ctx.show_toast(
        "Important notice",
        variant="info",
        duration=10000,
        description="This toast stays visible for 10 seconds",
    )


async def show_persistent_toast(ctx: Context):
    """Show a toast that stays until dismissed."""
    await ctx.show_toast(
        "Action required",
        variant="warning",
        duration=100000,  # Very long duration
        description="Click the X button to dismiss this toast",
        close_button=True,
    )


# ============================================================================
# Toast with Action Buttons
# ============================================================================


async def show_toast_with_action(ctx: Context):
    """Show a toast with an action button."""
    await ctx.show_toast(
        "Item deleted",
        description="The item has been moved to trash",
        action={"label": "Undo", "callback": ctx.callback(undo_delete)},
        duration=5000,
    )


async def undo_delete(ctx: Context):
    """Handle the undo action from toast."""
    await ctx.show_toast("Item restored!", variant="success")


async def show_toast_with_cancel(ctx: Context):
    """Show a toast with a cancel button."""
    await ctx.show_toast(
        "Sending email...",
        variant="loading",
        description="Your message is being sent",
        cancel={"label": "Cancel", "callback": ctx.callback(cancel_send)},
        duration=10000,
    )


async def cancel_send(ctx: Context):
    """Handle the cancel action from toast."""
    await ctx.show_toast("Email cancelled", variant="warning")


async def show_toast_with_both_buttons(ctx: Context):
    """Show a toast with both action and cancel buttons."""
    await ctx.show_toast(
        "Confirm changes?",
        variant="info",
        description="You have unsaved changes that will be lost",
        action={"label": "Save", "callback": ctx.callback(save_changes)},
        cancel={"label": "Discard", "callback": ctx.callback(discard_changes)},
        duration=10000,
    )


async def save_changes(ctx: Context):
    """Handle save action."""
    await ctx.show_toast("Changes saved!", variant="success")


async def discard_changes(ctx: Context):
    """Handle discard action."""
    await ctx.show_toast("Changes discarded", variant="warning")


# ============================================================================
# Toast Position Options
# ============================================================================


async def show_toast_top_left(ctx: Context):
    """Show a toast in top-left position."""
    await ctx.show_toast("Top Left", position="top-left")


async def show_toast_top_center(ctx: Context):
    """Show a toast in top-center position."""
    await ctx.show_toast("Top Center", position="top-center")


async def show_toast_top_right(ctx: Context):
    """Show a toast in top-right position."""
    await ctx.show_toast("Top Right", position="top-right")


async def show_toast_bottom_left(ctx: Context):
    """Show a toast in bottom-left position."""
    await ctx.show_toast("Bottom Left", position="bottom-left")


async def show_toast_bottom_center(ctx: Context):
    """Show a toast in bottom-center position."""
    await ctx.show_toast("Bottom Center", position="bottom-center")


async def show_toast_bottom_right(ctx: Context):
    """Show a toast in bottom-right position."""
    await ctx.show_toast("Bottom Right", position="bottom-right")


# ============================================================================
# Toast Style Options
# ============================================================================


async def show_inverted_toast(ctx: Context):
    """Show an inverted toast."""
    await ctx.show_toast(
        "Inverted colors",
        invert=True,
        description="This toast has inverted colors",
    )


async def show_non_dismissible_toast(ctx: Context):
    """Show a non-dismissible toast."""
    await ctx.show_toast(
        "Processing...",
        variant="loading",
        dismissible=False,
        duration=3000,
        description="This toast cannot be dismissed by clicking",
    )


# ============================================================================
# Advanced: Updating Toasts
# ============================================================================


async def show_updating_toast(ctx: Context):
    """Show a toast that updates its state."""
    # Show loading toast with ID
    await ctx.show_toast(
        "Uploading...",
        variant="loading",
        toast_id="upload-progress",
        description="Please wait while we upload your file",
    )

    # Simulate upload progress
    await asyncio.sleep(2)

    # Update the toast to success
    await ctx.show_toast(
        "Upload complete!",
        variant="success",
        toast_id="upload-progress",
        description="Your file has been uploaded successfully",
    )


async def show_multi_step_toast(ctx: Context):
    """Show a toast that goes through multiple steps."""
    steps = [
        ("Connecting...", "Establishing connection to server"),
        ("Authenticating...", "Verifying your credentials"),
        ("Syncing...", "Downloading latest data"),
        ("Complete!", "All data has been synchronized"),
    ]

    for i, (title, description) in enumerate(steps):
        variant = "success" if i == len(steps) - 1 else "loading"
        await ctx.show_toast(
            title,
            variant=variant,
            toast_id="multi-step",
            description=description,
        )
        if i < len(steps) - 1:
            await asyncio.sleep(1.5)


# ============================================================================
# Page Layout
# ============================================================================


@ui.page("/")
def home(ctx: Context):
    """Home page with toast examples."""
    return Container(
        class_name="p-8 max-w-6xl mx-auto",
        children=[
            # Header with ThemeSwitcher
            Row(
                class_name="mb-8 justify-between items-start",
                children=[
                    Column(
                        gap=2,
                        children=[
                            Heading("Toast Notifications Showcase"),
                            Text(
                                "Explore all the toast notification options available with Sonner",
                                class_name="text-muted-foreground text-lg",
                            ),
                        ],
                    ),
                    ThemeSwitcher(),
                ],
            ),
            # Main content grid
            Grid(
                columns={"default": 1, "md": 2},
                gap=6,
                children=[
                    # Basic Variants Card
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Basic Variants"),
                                    CardDescription(
                                        "Different toast styles for different purposes"
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Column(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Default Toast",
                                                on_click=ctx.callback(show_default_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                            Button(
                                                "Success Toast",
                                                on_click=ctx.callback(show_success_toast),
                                                variant="outline",
                                                class_name="w-full justify-start text-green-600",
                                            ),
                                            Button(
                                                "Error Toast",
                                                on_click=ctx.callback(show_error_toast),
                                                variant="outline",
                                                class_name="w-full justify-start text-red-600",
                                            ),
                                            Button(
                                                "Warning Toast",
                                                on_click=ctx.callback(show_warning_toast),
                                                variant="outline",
                                                class_name="w-full justify-start text-yellow-600",
                                            ),
                                            Button(
                                                "Info Toast",
                                                on_click=ctx.callback(show_info_toast),
                                                variant="outline",
                                                class_name="w-full justify-start text-blue-600",
                                            ),
                                            Button(
                                                "Loading Toast",
                                                on_click=ctx.callback(show_loading_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                        ],
                                    )
                                ]
                            ),
                        ]
                    ),
                    # With Description Card
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("With Description"),
                                    CardDescription("Toasts can have additional descriptive text"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Column(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Success with Description",
                                                on_click=ctx.callback(show_toast_with_description),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                            Button(
                                                "Error with Description",
                                                on_click=ctx.callback(show_error_with_description),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                        ],
                                    )
                                ]
                            ),
                        ]
                    ),
                    # Duration Options Card
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Duration Options"),
                                    CardDescription("Control how long toasts stay visible"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Column(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Short (1s)",
                                                on_click=ctx.callback(show_short_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                            Button(
                                                "Long (10s)",
                                                on_click=ctx.callback(show_long_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                            Button(
                                                "Persistent (until dismissed)",
                                                on_click=ctx.callback(show_persistent_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                        ],
                                    )
                                ]
                            ),
                        ]
                    ),
                    # Action Buttons Card
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Action Buttons"),
                                    CardDescription("Add interactive buttons to toasts"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Column(
                                        gap=2,
                                        children=[
                                            Button(
                                                "With Undo Action",
                                                on_click=ctx.callback(show_toast_with_action),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                            Button(
                                                "With Cancel Button",
                                                on_click=ctx.callback(show_toast_with_cancel),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                            Button(
                                                "With Both Buttons",
                                                on_click=ctx.callback(show_toast_with_both_buttons),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                        ],
                                    )
                                ]
                            ),
                        ]
                    ),
                    # Position Options Card
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Position Options"),
                                    CardDescription("Show toasts in different screen positions"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Grid(
                                        columns={"default": 2},
                                        gap=2,
                                        children=[
                                            Button(
                                                "Top Left",
                                                on_click=ctx.callback(show_toast_top_left),
                                                variant="outline",
                                                size="sm",
                                            ),
                                            Button(
                                                "Top Center",
                                                on_click=ctx.callback(show_toast_top_center),
                                                variant="outline",
                                                size="sm",
                                            ),
                                            Button(
                                                "Top Right",
                                                on_click=ctx.callback(show_toast_top_right),
                                                variant="outline",
                                                size="sm",
                                            ),
                                            Button(
                                                "Bottom Left",
                                                on_click=ctx.callback(show_toast_bottom_left),
                                                variant="outline",
                                                size="sm",
                                            ),
                                            Button(
                                                "Bottom Center",
                                                on_click=ctx.callback(show_toast_bottom_center),
                                                variant="outline",
                                                size="sm",
                                            ),
                                            Button(
                                                "Bottom Right",
                                                on_click=ctx.callback(show_toast_bottom_right),
                                                variant="outline",
                                                size="sm",
                                            ),
                                        ],
                                    )
                                ]
                            ),
                        ]
                    ),
                    # Style Options Card
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Style Options"),
                                    CardDescription("Customize toast appearance and behavior"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Column(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Inverted Colors",
                                                on_click=ctx.callback(show_inverted_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                            Button(
                                                "Non-Dismissible",
                                                on_click=ctx.callback(show_non_dismissible_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                        ],
                                    )
                                ]
                            ),
                        ]
                    ),
                    # Updating Toasts Card
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Updating Toasts"),
                                    CardDescription("Update existing toasts with new content"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Column(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Upload Progress",
                                                on_click=ctx.callback(show_updating_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                            Button(
                                                "Multi-Step Process",
                                                on_click=ctx.callback(show_multi_step_toast),
                                                variant="outline",
                                                class_name="w-full justify-start",
                                            ),
                                        ],
                                    )
                                ]
                            ),
                        ]
                    ),
                ],
            ),
            # Note: No Toaster component needed - ToastManager is automatically included
        ],
    )


app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
