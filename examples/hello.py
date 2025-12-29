import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import Button, Container, Text, ThemeSwitcher

ui = RefastApp(title="Hello World App")


async def start_refresh(ctx: Context):
    ctx.state["refresh"] = "on"
    await ctx.show_toast("Refresh started", variant="success")
    await ctx.refresh()


async def stop_refresh(ctx: Context):
    ctx.state["refresh"] = "off"
    await ctx.show_toast("Refresh stopped", variant="success")
    await ctx.refresh()


@ui.page("/")
def hello_world_page(ctx: Context):
    print("Rendering Hello World Page")
    text = f"{ctx.state.get('prefix', 'Hello')} {ctx.state.get('counter', 0)}"
    refresh_state = True if ctx.state.get("refresh", "off") == "on" else False
    return Container(
        [
            Container(
                [Text(text, id="hello-text")],
                class_name="p-4 rounded-lg shadow-md bg-white dark:bg-gray-800",
            ),
            Container(
                [
                    Button(
                        "Start Refresh",
                        on_click=ctx.callback(start_refresh),
                        disabled=refresh_state,
                    ),
                    Button(
                        "Stop refresh",
                        on_click=ctx.callback(stop_refresh),
                        disabled=not refresh_state,
                    ),
                ],
                class_name="flex flex-row gap-4",
            ),
            ThemeSwitcher(default_theme="system"),
        ],
        class_name="flex flex-col gap-6 items-center justify-center min-h-screen gap-4 bg-gray-100 dark:bg-gray-900",
    )


async def update_value():
    print("Starting periodic updates...")
    while True:
        for ctx in ui.active_contexts:
            if ctx.state.get("refresh", "off") == "off":
                continue
            if not ctx.state.get("counter"):
                ctx.state["counter"] = 0
            if not ctx.state.get("prefix"):
                ctx.state["prefix"] = "Hello"
            await ctx.replace(
                "hello-text",
                Text(
                    f"{ctx.state.get('prefix')} {ctx.state.get('counter')}",
                    id="hello-text",
                    size="xl",
                    weight="bold",
                ),
            )
            ctx.state["counter"] += 1
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the Hello World App...")
    task = asyncio.create_task(update_value())
    yield
    task.cancel()
    print("Shutting down the Hello World App...")
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
