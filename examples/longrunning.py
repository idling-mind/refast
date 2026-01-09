import asyncio
import random

from fastapi import FastAPI

from refast import Context, RefastApp
from refast import components as rc

app = FastAPI()
ui = RefastApp(title="Long Running Tasks App")


async def run_background_task(ctx: Context):
    """Execution logic for the long-running task."""
    try:
        # Reset stop flag at start
        ctx.state["stop_task"] = False

        for i in range(10):
            if ctx.state.get("stop_task"):
                await ctx.show_toast("Long task stopped", variant="warning")
                await ctx.update_text("task-status", "Task was stopped by the user.")
                await ctx.update_props("task-progress", {"foregroundColor": "destructive"})
                await ctx.update_props("stop-task-button", {"style": {"display": "none"}})
                await ctx.update_props("start-task-button", {"style": {"display": "inline-block"}})
                await ctx.update_text("start-task-button", "Restart Long Task")
                return

            await ctx.update_props("stop-task-button", {"style": {"display": "inline-block"}})
            await asyncio.sleep(random.uniform(1.0, 5.0))  # Simulate work
            await ctx.update_text("task-status", f"Task progress: {((i + 1) / 10) * 100:.0f}%")
            await ctx.update_props("task-progress", {"value": (i + 1) / 10 * 100})

        await ctx.show_toast("Long task completed", variant="success")
        await ctx.update_props("stop-task-button", {"style": {"display": "none"}})
        await ctx.update_props("start-task-button", {"style": {"display": "inline-block"}})
        await ctx.update_props("task-progress", {"foregroundColor": "success"})
    except Exception as e:
        print(f"Task error: {e}")
        # Handle disconnection or other errors gracefully


async def start_long_task(ctx: Context):
    await ctx.update_props("start-task-button", {"style": {"display": "none"}})
    await ctx.show_toast("Long task started", variant="info")
    await ctx.update_text("task-status", "Task is starting...")
    # Run the task in the background so we don't block the WebSocket loop
    # preventing other events (like stop_long_task) from being processed.
    asyncio.create_task(run_background_task(ctx))


async def stop_long_task(ctx: Context):
    ctx.state["stop_task"] = True
    await ctx.update_text("task-status", "Stopping task...")
    await ctx.show_toast("Stop signal sent", variant="info")


@ui.page("/")
def long_running_page(ctx: Context):
    return rc.Container(
        [
            rc.Heading("Long Running Tasks Example", level=1),
            rc.Text("This page demonstrates long-running tasks.", id="info-text"),
            rc.Button(
                "Start Long Task",
                id="start-task-button",
                on_click=ctx.callback(start_long_task),
            ),
            rc.Button(
                "Stop Long Task",
                id="stop-task-button",
                on_click=ctx.callback(stop_long_task),
                variant="destructive",
                style={"display": "none"},  # Initially hidden
            ),
            rc.Text("", id="task-status", class_name="text-lg font-medium justify-center"),
            rc.Progress(value=0, id="task-progress", foreground_color="primary", striped="animated"),
        ],
        class_name="flex flex-col gap-4 p-4 max-w-6xl mx-auto",
    )


app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
