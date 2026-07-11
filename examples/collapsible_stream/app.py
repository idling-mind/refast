"""Collapsible Streaming Example.

Demonstrates programmatic Collapsible control (collapse/expand) via bound JS
callbacks during a real-time data streaming session.
"""

import asyncio

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
    Text,
    ThemeSwitcher,
)
from refast.components.shadcn.utility import Collapsible, CollapsibleContent, CollapsibleTrigger

ui = RefastApp(title="Collapsible Streaming Demo")


async def run_collapsible_stream(ctx: Context):
    """Executes the streaming sequence across multiple collapsible blocks."""
    # Disable the start button during streaming to prevent overlapping runs
    await ctx.update_props("start-btn", {"disabled": True})
    await ctx.update_text("stream-status", "Streaming Part 1...")

    # Clear container of any previous collapsible blocks
    await ctx.update_props("collapsible-container", {"children":[]})

    # --- PART 1 ---
    col_id_1 = "collapsible-1"
    content_id_1 = "content-1"
    badge_id_1 = "badge-1"

    # Create the first collapsible. It is default_open=True so the user sees the stream.
    col1 = Collapsible(
        id=col_id_1,
        default_open=True,
        children=[
            CollapsibleTrigger(
                Row(
                    id="sample",
                    children=[
                        Badge("Active", id=badge_id_1, variant="secondary"),
                        Heading("Part 1: Ingestion & Verification", level=3, class_name="text-lg font-medium"),
                    ],
                    align="center",
                    justify="start",
                    gap=3,
                ),
                class_name="p-4 cursor-pointer"
            ),
            CollapsibleContent(
                Container(
                    children=[
                        Markdown(
                            id=content_id_1,
                            content="Connecting to data source...",
                            class_name="prose-sm mt-2 p-3 bg-muted/30 rounded border text-foreground/80",
                        )
                    ],
                    class_name="px-4 pb-4",
                )
            ),
        ],
        class_name="border rounded-lg mb-4 overflow-hidden bg-card text-card-foreground shadow-sm",
    )

    # Append to container
    await ctx.append("collapsible-container", col1)
    await asyncio.sleep(0.5)

    # Stream content into Part 1
    sentences_1 = [
        "Gathering preliminary data from ingestion node alpha...",
        "Analyzing system latency and processing throughput metrics...",
        "Verifying cryptographic integrity of block signatures...",
        "Establishing secure websocket connection channel for telemetry...",
        "Part 1 data ingestion has completed successfully."
    ]

    await ctx.update_props(content_id_1, {"content": ""})
    for sentence in sentences_1:
        await ctx.append_prop(content_id_1, "content", sentence + "\n\n")
        await asyncio.sleep(0.8)

    # Update badge to reflect completion
    await ctx.update_props(badge_id_1, {"variant": "success"})
    await ctx.update_text(badge_id_1, "Completed")
    await ctx.show_toast("Part 1 stream finished. Collapsing section...", "info")
    await asyncio.sleep(0.5)

    # Close Part 1 programmatically using the new bound method!
    await ctx.call_bound_js(col_id_1, "collapse")
    await asyncio.sleep(1.0)  # Wait for transition

    # --- PART 2 ---
    await ctx.update_text("stream-status", "Streaming Part 2...")
    col_id_2 = "collapsible-2"
    content_id_2 = "content-2"
    badge_id_2 = "badge-2"

    # Create the second collapsible, also default_open=True.
    col2 = Collapsible(
        id=col_id_2,
        default_open=True,
        children=[
            CollapsibleTrigger(
                Row(
                    children=[
                        Badge("Active", id=badge_id_2, variant="secondary"),
                        Heading("Part 2: Processing & Aggregation", level=3, class_name="text-lg font-medium"),
                    ],
                    align="center",
                    justify="start",
                    gap=3,
                ),
                class_name="p-4 cursor-pointer"
            ),
            CollapsibleContent(
                Container(
                    children=[
                        Markdown(
                            id=content_id_2,
                            content="Initializing analysis pipeline...",
                            class_name="prose-sm mt-2 p-3 bg-muted/30 rounded border text-foreground/80",
                        )
                    ],
                    class_name="px-4 pb-4",
                )
            ),
        ],
        class_name="border rounded-lg mb-4 overflow-hidden bg-card text-card-foreground shadow-sm",
    )

    # Append to container
    await ctx.append("collapsible-container", col2)
    await asyncio.sleep(0.5)

    # Stream content into Part 2
    sentences_2 = [
        "Compiling aggregated logs from cluster beta database shards...",
        "Running machine learning inference model on incoming feature tensors...",
        "Applying schema validation rules and data sanity checks...",
        "Generating final PDF and spreadsheet report summaries...",
        "Part 2 processing completed. All systems operational."
    ]

    await ctx.update_props(content_id_2, {"content": ""})
    for sentence in sentences_2:
        await ctx.append_prop(content_id_2, "content", sentence + "\n\n")
        await asyncio.sleep(0.8)

    # Update Part 2 badge to success
    await ctx.update_props(badge_id_2, {"variant": "success"})
    await ctx.update_text(badge_id_2, "Completed")
    await ctx.show_toast("Part 2 stream finished. Collapsing section...", "info")
    await asyncio.sleep(0.5)

    # Close Part 2 programmatically using the new bound method!
    await ctx.call_bound_js(col_id_2, "collapse")
    await asyncio.sleep(0.5)

    # Finalize state
    await ctx.update_text("stream-status", "Stream Sequence Completed")
    await ctx.show_toast("All streams completed successfully!", "success")
    await ctx.update_props("start-btn", {"disabled": False})


@ui.page("/")
def home(ctx: Context):
    """Home page rendering the stream controller and collapsible container."""
    return Container(
        class_name="max-w-3xl mx-auto py-12 px-6 space-y-8",
        children=[
            # Header
            Row(
                justify="between",
                children=[
                    Column(
                        class_name="space-y-1",
                        children=[
                            Heading("Collapsible Streaming", level=1),
                            Text(
                                "Demonstrates programmatically collapsing sections after real-time data streaming.",
                                class_name="text-muted-foreground text-sm",
                            ),
                        ],
                    ),
                    ThemeSwitcher(),
                ],
            ),

            # Stream Controller Card
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Control Panel"),
                            CardDescription("Trigger the multi-part streaming pipeline. Watch sections open, stream, and close automatically."),
                        ]
                    ),
                    CardContent(
                        class_name="space-y-4",
                        children=[
                            Row(
                                gap=4,
                                class_name="items-center",
                                children=[
                                    Button(
                                        "Start Stream Sequence",
                                        id="start-btn",
                                        on_click=ctx.callback(run_collapsible_stream),
                                        variant="default",
                                    ),
                                    Badge(
                                        "Ready",
                                        id="stream-status",
                                        variant="outline",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),

            # Dynamic Container for Collapsible blocks
            Column(
                id="collapsible-container",
                class_name="space-y-4 min-h-[100px]",
                children=[
                    Container(
                        class_name="text-center py-8 text-muted-foreground border border-dashed rounded-lg",
                        children=[
                            Text("No streams running. Click 'Start Stream Sequence' to begin.")
                        ],
                    )
                ],
            ),
        ],
    )


# Create FastAPI application
app = FastAPI()
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
