from fastapi import FastAPI
from refast import RefastApp
from refast.components import (
    Button,
    Card,
    Container,
    Heading,
    Input,
    Text,
    Row,
)
from refast.context import Context
import random
import asyncio

app = FastAPI(title="Refast Component Refresh Demo")
ui = RefastApp("Component Refresh Demo")
app.include_router(ui.router)


class AppState:
    def __init__(self):
        self.counter_full = 0
        self.counter_partial = 0
        self.random_val = 0


# Global state simulation
state = AppState()


async def do_full_refresh(ctx: Context):
    """Update state and refresh the entire page."""
    # Using global app state
    state.counter_full += 1
    state.random_val = random.randint(1, 100)

    # Using per-session state (ctx.state)
    current_count = ctx.state.get("session_counter", 0)
    ctx.state["session_counter"] = current_count + 1

    # This will cause focus loss in inputs and potential screen flash
    await ctx.refresh()


async def do_partial_refresh(ctx: Context):
    """Update state and refresh only the target component."""
    # Using global app state
    state.counter_partial += 1
    state.random_val = random.randint(1, 100)

    # Using per-session state (ctx.state)
    current_count = ctx.state.get("session_counter", 0)
    ctx.state["session_counter"] = current_count + 1

    # This keeps focus intact on other elements and only updates the target
    await ctx.refresh(target_id="partial-refresh-area")


@ui.page("/")
def home(ctx: Context):
    # Retrieve session state with default
    session_count = ctx.state.get("session_counter", 0)

    return Container(
        class_name="p-8",
        children=[
            Heading("Partial vs Full Refresh Demo", level=1, class_name="text-3xl font-bold mb-6"),
            Text(
                "This example demonstrates how to update specific parts of the page "
                "without re-rendering everything. This prevents screen flashing and focus loss.",
                class_name="mb-8 text-gray-600",
            ),
            # Show session state vs global state concept
            Container(
                class_name="mb-8 p-4 bg-blue-50 border border-blue-200 rounded",
                children=[
                    Heading("State Context", level=3, class_name="font-bold mb-2"),
                    Text(
                        f"Global App State (Shared): Full={state.counter_full}, Partial={state.counter_partial}"
                    ),
                    Text(f"Session State (ctx.state, Per-User): {session_count}"),
                ],
            ),
            Container(
                class_name="grid grid-cols-1 md:grid-cols-2 gap-8",
                children=[
                    # Left Column: Full Refresh
                    Card(
                        title="Scenario 1: Full Page Refresh",
                        children=[
                            Container(
                                class_name="space-y-4 p-4",
                                children=[
                                    Text(
                                        "Clicking below refreshes the ENTIRE page.",
                                        class_name="text-sm font-semibold",
                                    ),
                                    Row(
                                        class_name="bg-red-50 p-4 rounded border border-red-200",
                                        children=[
                                            Text(
                                                f"Counter: {state.counter_full}",
                                                class_name="text-xl font-bold text-red-700",
                                            ),
                                            Text(
                                                f"Random Val: {state.random_val}",
                                                class_name="text-sm text-red-600",
                                            ),
                                            Text(
                                                f"Update Timestamp: {asyncio.get_event_loop().time()}",
                                                class_name="text-xs text-green-800 mt-2",
                                            ),
                                        ],
                                        gap=4,
                                        align="center",
                                    ),
                                    Input(
                                        name="full-refresh-input",
                                        placeholder="Type here then click Refresh...",
                                        class_name="w-full",
                                    ),
                                    Button(
                                        "Refresh Entire Page (ctx.refresh())",
                                        on_click=ctx.callback(do_full_refresh),
                                        variant="destructive",
                                        class_name="w-full",
                                    ),
                                    Text(
                                        "Notice: Focus is LOST from the input box after clicking.",
                                        class_name="text-xs text-red-500 italic",
                                    ),
                                ],
                            )
                        ],
                    ),
                    # Right Column: Partial Refresh
                    Card(
                        title="Scenario 2: Partial Refresh",
                        children=[
                            Container(
                                class_name="space-y-4 p-4",
                                children=[
                                    Text(
                                        "Clicking below refreshes ONLY this card.",
                                        class_name="text-sm font-semibold",
                                    ),
                                    # This ID is critical for partial refresh targeting
                                    Row(
                                        id="partial-refresh-area",
                                        class_name="bg-green-50 p-4 rounded border border-green-200 transition-colors duration-200",
                                        children=[
                                            Text(
                                                f"Counter: {state.counter_partial}",
                                                class_name="text-xl font-bold text-green-700",
                                            ),
                                            Text(
                                                f"Random Val: {state.random_val}",
                                                class_name="text-sm text-green-600",
                                            ),
                                            Text(
                                                f"Update Timestamp: {asyncio.get_event_loop().time() if state.counter_partial > 0 else 'Never'}",
                                                class_name="text-xs text-green-800 mt-2",
                                            ),
                                        ],
                                        gap=4,
                                        align="center",
                                    ),
                                    Input(
                                        name="partial-refresh-input",
                                        placeholder="Type here then click Refresh...",
                                        class_name="w-full",
                                    ),
                                    Button(
                                        "Refresh Target ID (ctx.refresh(target_id=...))",
                                        on_click=ctx.callback(do_partial_refresh),
                                        variant="default",  # Green/Primary by default in shadcn
                                        class_name="w-full bg-green-600 hover:bg-green-700",
                                    ),
                                    Text(
                                        "Notice: Focus remains inside this input box!",
                                        class_name="text-xs text-green-600 italic",
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            ),
            Container(
                class_name="mt-8 p-6 bg-gray-50 rounded-lg border",
                children=[
                    Heading("How it works", level=3, class_name="text-xl font-bold mb-2"),
                    Text(
                        "1. Assign a unique ID to the container you want to update: `Container(id='my-target', ...)`",
                        class_name="code block mb-1",
                    ),
                    Text(
                        "2. Call `await ctx.refresh(target_id='my-target')` in your event handler.",
                        class_name="code block",
                    ),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
