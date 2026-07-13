"""
Bound Overlays Demo

Demonstrates calling Sheet, Drawer, and Dialog imperative methods (open, close, toggle)
via:
  - ctx.bound_js()      → pure client-side (no server roundtrip)
  - ctx.call_bound_js() → server-initiated (from a Python callback after processing)

Run with:
    cd examples/bound_overlays
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
    Dialog,
    DialogAction,
    DialogCancel,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    Drawer,
    DrawerClose,
    DrawerContent,
    DrawerDescription,
    DrawerFooter,
    DrawerHeader,
    DrawerTitle,
    Grid,
    Heading,
    Paragraph,
    Row,
    Sheet,
    SheetClose,
    SheetContent,
    SheetDescription,
    SheetFooter,
    SheetHeader,
    SheetTitle,
)

ui = RefastApp(title="Bound Overlays Demo")

# Unique IDs for overlays
DIALOG_ID = "demo-dialog"
SHEET_ID = "demo-sheet"
DRAWER_ID = "demo-drawer"


# Server-side callbacks (using ctx.call_bound_js)
async def open_dialog_after_delay(ctx: Context):
    await ctx.show_toast("Simulating background server task for 1.5 seconds...", variant="info")
    await asyncio.sleep(1.5)
    await ctx.call_bound_js(DIALOG_ID, "open")
    await ctx.show_toast("Dialog opened from server!", variant="success")


async def open_sheet_after_delay(ctx: Context):
    await ctx.show_toast("Simulating background server task for 1.5 seconds...", variant="info")
    await asyncio.sleep(1.5)
    await ctx.call_bound_js(SHEET_ID, "open")
    await ctx.show_toast("Sheet opened from server!", variant="success")


async def open_drawer_after_delay(ctx: Context):
    await ctx.show_toast("Simulating background server task for 1.5 seconds...", variant="info")
    await asyncio.sleep(1.5)
    await ctx.call_bound_js(DRAWER_ID, "open")
    await ctx.show_toast("Drawer opened from server!", variant="success")


@ui.page("/")
async def main_page(ctx: Context):
    return Container(
        class_name="max-w-5xl py-12 px-4 mx-auto",
        children=[
            # Header section
            Container(
                class_name="text-center mb-12",
                children=[
                    Heading("Bound Overlays Control", level=1, class_name="text-4xl font-extrabold tracking-tight mb-3"),
                    Paragraph(
                        "Interact with Sheet, Drawer, and Dialog components dynamically using client-side event handlers "
                        "or server-side callback triggers.",
                        class_name="text-muted-foreground max-w-2xl mx-auto text-lg",
                    ),
                ],
            ),

            # The overlay definitions (rendered in the page DOM structure, hidden by default)
            Dialog(
                id=DIALOG_ID,
                children=[
                    DialogContent(
                        children=[
                            DialogHeader(
                                [
                                    DialogTitle("System Confirmation"),
                                    DialogDescription("This Dialog was triggered imperatively via bound_js!"),
                                ]
                            ),
                            Paragraph(
                                "Dialogs are ideal for critical path tasks or confirmations. "
                                "You can click action buttons below or close this dialogue.",
                                class_name="text-sm text-muted-foreground my-2"
                            ),
                            DialogFooter(
                                [
                                    DialogCancel("Cancel"),
                                    DialogAction("Acknowledge"),
                                ]
                            ),
                        ]
                    )
                ],
            ),

            Sheet(
                id=SHEET_ID,
                backdrop=False,
                children=[
                    SheetContent(
                        side="right",
                        children=[
                            SheetHeader(
                                [
                                    SheetTitle("Navigation Drawer / Sheet"),
                                    SheetDescription("This Sheet slides in from the right edge."),
                                ]
                            ),
                            Container(
                                class_name="py-6 flex flex-col gap-4",
                                children=[
                                    Paragraph("Use sheets for complex detail views, side navigations, or quick filters."),
                                    Button("Perform Action", class_name="w-full"),
                                ]
                            ),
                            SheetFooter(
                                SheetClose(Button("Dismiss Sheet", variant="outline", class_name="w-full"))
                            ),
                        ]
                    )
                ],
            ),

            Drawer(
                id=DRAWER_ID,
                children=[
                    DrawerContent(
                        children=[
                            DrawerHeader(
                                [
                                    DrawerTitle("Quick Actions Drawer"),
                                    DrawerDescription("This Drawer slides up from the bottom of the viewport."),
                                ]
                            ),
                            Container(
                                class_name="py-8 max-w-md mx-auto text-center flex flex-col gap-2",
                                children=[
                                    Paragraph("Drawers are optimized for mobile layouts but function smoothly on all devices."),
                                ]
                            ),
                            DrawerFooter(
                                DrawerClose(Button("Close Actions", variant="secondary", class_name="max-w-xs mx-auto w-full"))
                            ),
                        ]
                    )
                ],
            ),

            # Main layout card grid controls
            Grid(
                columns=3,
                gap=8,
                children=[
                    # Dialog Controls Card
                    Card(
                        class_name="border shadow-md",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Dialog"),
                                    CardDescription("Centered modal overlays"),
                                ]
                            ),
                            CardContent(
                                class_name="flex flex-col gap-3 pt-2",
                                children=[
                                    Button(
                                        "Open Dialog (Client)",
                                        on_click=ctx.bound_js(DIALOG_ID, "open"),
                                        variant="default",
                                    ),
                                    Button(
                                        "Toggle Dialog (Client)",
                                        on_click=ctx.bound_js(DIALOG_ID, "toggle"),
                                        variant="outline",
                                    ),
                                    Button(
                                        "Delayed Open (Server)",
                                        on_click=ctx.callback(open_dialog_after_delay),
                                        variant="secondary",
                                    ),
                                ],
                            ),
                        ]
                    ),

                    # Sheet Controls Card
                    Card(
                        class_name="border shadow-md",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Sheet"),
                                    CardDescription("Slide-out sidebar overlays"),
                                ]
                            ),
                            CardContent(
                                class_name="flex flex-col gap-3 pt-2",
                                children=[
                                    Button(
                                        "Open Sheet (Client)",
                                        on_click=ctx.bound_js(SHEET_ID, "open"),
                                        variant="default",
                                    ),
                                    Button(
                                        "Toggle Sheet (Client)",
                                        on_click=ctx.bound_js(SHEET_ID, "toggle"),
                                        variant="outline",
                                    ),
                                    Button(
                                        "Delayed Open (Server)",
                                        on_click=ctx.callback(open_sheet_after_delay),
                                        variant="secondary",
                                    ),
                                ],
                            ),
                        ]
                    ),

                    # Drawer Controls Card
                    Card(
                        class_name="border shadow-md",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Drawer"),
                                    CardDescription("Bottom drawer overlays"),
                                ]
                            ),
                            CardContent(
                                class_name="flex flex-col gap-3 pt-2",
                                children=[
                                    Button(
                                        "Open Drawer (Client)",
                                        on_click=ctx.bound_js(DRAWER_ID, "open"),
                                        variant="default",
                                    ),
                                    Button(
                                        "Toggle Drawer (Client)",
                                        on_click=ctx.bound_js(DRAWER_ID, "toggle"),
                                        variant="outline",
                                    ),
                                    Button(
                                        "Delayed Open (Server)",
                                        on_click=ctx.callback(open_drawer_after_delay),
                                        variant="secondary",
                                    ),
                                ],
                            ),
                        ]
                    ),
                ],
            ),
        ],
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
