"""
Resizable Panels - Imperative Control Example

Demonstrates calling ResizablePanel imperative methods via bound_js:
  - ctx.bound_js()      → pure client-side (no server roundtrip)
  - ctx.call_bound_js() → server-initiated (from a Python callback)

Methods exposed on each panel:
  collapse()          – fully collapses the panel (requires collapsible=True)
  expand(min_size?)   – expands a collapsed panel
  resize(size)        – sets the panel to a specific percentage
  getSize()           – returns current size (client-side only)
  isCollapsed()       – returns True if collapsed (client-side only)
  isExpanded()        – returns True if expanded (client-side only)

Run with:
    cd examples/resizable_panels
    uvicorn app:app --reload
"""

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
    Paragraph,
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
    Row,
    Text,
)

ui = RefastApp(title="Resizable Panels Demo")

# IDs for the two panels we control
LEFT_PANEL_ID = "panel-left"
RIGHT_PANEL_ID = "panel-right"


# ============================================================================
# Server-side callbacks (use ctx.call_bound_js)
# ============================================================================


async def set_equal_split(ctx: Context):
    """Reset both panels to an equal 50/50 split."""
    await ctx.call_bound_js(LEFT_PANEL_ID, "resize", 50)
    await ctx.call_bound_js(RIGHT_PANEL_ID, "resize", 50)
    await ctx.show_toast("Panels reset to 50/50", variant="info")


async def set_wide_left(ctx: Context):
    """Make the left panel dominant (70/30)."""
    await ctx.call_bound_js(LEFT_PANEL_ID, "resize", 70)
    await ctx.call_bound_js(RIGHT_PANEL_ID, "resize", 30)
    await ctx.show_toast("Left panel expanded to 70%", variant="info")


async def set_wide_right(ctx: Context):
    """Make the right panel dominant (30/70)."""
    await ctx.call_bound_js(LEFT_PANEL_ID, "resize", 30)
    await ctx.call_bound_js(RIGHT_PANEL_ID, "resize", 70)
    await ctx.show_toast("Right panel expanded to 70%", variant="info")


# ============================================================================
# Page
# ============================================================================


@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="p-8 max-w-5xl mx-auto space-y-8",
        children=[
            # Header
            Column(
                gap=2,
                children=[
                    Heading("Resizable Panels", level=1),
                    Text(
                        "Imperative panel control via ctx.bound_js() and ctx.call_bound_js().",
                        class_name="text-muted-foreground",
                    ),
                ],
            ),
            # ----------------------------------------------------------------
            # Section 1: ctx.bound_js() – pure client-side, no server roundtrip
            # ----------------------------------------------------------------
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("ctx.bound_js() — Client-Side Control"),
                            CardDescription(
                                "Button clicks call panel methods directly in the browser "
                                "with no server roundtrip."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    # Control buttons
                                    Row(
                                        gap=2,
                                        class_name="flex-wrap",
                                        children=[
                                            Button(
                                                "Collapse Left",
                                                variant="outline",
                                                on_click=ctx.bound_js(LEFT_PANEL_ID, "collapse"),
                                            ),
                                            Button(
                                                "Expand Left",
                                                variant="outline",
                                                on_click=ctx.bound_js(LEFT_PANEL_ID, "expand"),
                                            ),
                                            Button(
                                                "Collapse Right",
                                                variant="outline",
                                                on_click=ctx.bound_js(RIGHT_PANEL_ID, "collapse"),
                                            ),
                                            Button(
                                                "Expand Right",
                                                variant="outline",
                                                on_click=ctx.bound_js(RIGHT_PANEL_ID, "expand"),
                                            ),
                                            Button(
                                                "Left → 25%",
                                                variant="secondary",
                                                on_click=ctx.bound_js(LEFT_PANEL_ID, "resize", 25),
                                            ),
                                            Button(
                                                "Left → 75%",
                                                variant="secondary",
                                                on_click=ctx.bound_js(LEFT_PANEL_ID, "resize", 75),
                                            ),
                                        ],
                                    ),
                                    # The panels
                                    ResizablePanelGroup(
                                        direction="horizontal",
                                        class_name="h-48 rounded-lg border",
                                        children=[
                                            ResizablePanel(
                                                id=LEFT_PANEL_ID,
                                                default_size=50,
                                                min_size=0,
                                                collapsible=True,
                                                collapsed_size=0,
                                                children=[
                                                    Column(
                                                        class_name="h-full items-center justify-center p-4 bg-muted/30",
                                                        children=[
                                                            Badge("Left Panel", variant="secondary"),
                                                            Paragraph(
                                                                "Drag the handle or use the buttons above.",
                                                                class_name="text-xs text-muted-foreground text-center mt-2",
                                                            ),
                                                        ],
                                                    )
                                                ],
                                            ),
                                            ResizableHandle(with_handle=True),
                                            ResizablePanel(
                                                id=RIGHT_PANEL_ID,
                                                default_size=50,
                                                min_size=0,
                                                collapsible=True,
                                                collapsed_size=0,
                                                children=[
                                                    Column(
                                                        class_name="h-full items-center justify-center p-4 bg-muted/30",
                                                        children=[
                                                            Badge("Right Panel", variant="outline"),
                                                            Paragraph(
                                                                "Resize, collapse or expand via bound_js.",
                                                                class_name="text-xs text-muted-foreground text-center mt-2",
                                                            ),
                                                        ],
                                                    )
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
            # ----------------------------------------------------------------
            # Section 2: ctx.call_bound_js() – server-initiated
            # ----------------------------------------------------------------
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("ctx.call_bound_js() — Server-Initiated Control"),
                            CardDescription(
                                "Python callbacks use ctx.call_bound_js() to resize panels "
                                "after any server-side processing (e.g. loading data)."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Row(
                                        gap=2,
                                        class_name="flex-wrap",
                                        children=[
                                            Button(
                                                "Equal Split (50/50)",
                                                on_click=ctx.callback(set_equal_split),
                                            ),
                                            Button(
                                                "Left-Heavy (70/30)",
                                                variant="secondary",
                                                on_click=ctx.callback(set_wide_left),
                                            ),
                                            Button(
                                                "Right-Heavy (30/70)",
                                                variant="secondary",
                                                on_click=ctx.callback(set_wide_right),
                                            ),
                                        ],
                                    ),
                                    Text(
                                        "The panels above (in section 1) are the targets — "
                                        "the server resizes them by ID after the callback runs.",
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
        ],
    )


fastapi_app = FastAPI()
fastapi_app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
