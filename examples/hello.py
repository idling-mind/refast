import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import Button, Container, Text, ThemeSwitcher, ResizablePanel, ResizableHandle, ResizablePanelGroup

ui = RefastApp(title="Hello World App")


async def start_refresh(ctx: Context):
    ctx.store.local["refresh"] = "on"
    await ctx.show_toast("Refresh started", variant="success")
    await ctx.refresh()


async def stop_refresh(ctx: Context):
    ctx.store.local["refresh"] = "off"
    await ctx.show_toast("Refresh stopped", variant="success")
    await ctx.refresh()


@ui.page("/")
def hello_world_page(ctx: Context):
    print("Rendering Hello World Page")
    text = f"{ctx.store.local.get('prefix', 'Hello')} {ctx.store.local.get('counter', 0)}"
    print("refresh", ctx.store.local.get("refresh"))
    refresh_state = True if ctx.store.local.get("refresh", "off") == "on" else False
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
            Container(
                [
                    ResizablePanelGroup(
                        direction="horizontal",
                        children=[
                            ResizablePanel(
                                min_size=20,
                                default_size=50,
                                children=[Text("Resizable Panel 1 (50%)")],
                                class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md",
                            ),
                            ResizableHandle(with_handle=True),
                            ResizablePanel(
                                min_size=20,
                                default_size=50,
                                children=[
                                    ResizablePanelGroup(
                                        direction="vertical",
                                        children=[
                                            ResizablePanel(
                                                min_size=20,
                                                default_size=70,
                                                children=[Text("Resizable Panel 2 (70%)")],
                                                class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md",
                                            ),
                                            ResizableHandle(with_handle=True),
                                            ResizablePanel(
                                                min_size=20,
                                                default_size=30,
                                                children=[Text("Resizable Panel 3 (30%)")],
                                                class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md",
                                            ),
                                        ],
                                        class_name="w-full h-screen",
                                        style={"height": "400px"},
                                    )
                                ],
                                class_name="bg-white dark:bg-gray-800",
                            ),
                        ],
                        class_name="w-full border rounded-lg",
                    )
                ],
                class_name="w-full max-w-4xl"
            )
        ],
        class_name="flex flex-col gap-6 items-center justify-center min-h-screen gap-4 bg-gray-100 dark:bg-gray-900",
    )


async def update_value():
    print("Starting periodic updates...")
    while True:
        for ctx in ui.active_contexts:
            if ctx.store.local.get("refresh", "off") == "off":
                continue
            if not ctx.store.local.get("counter"):
                ctx.store.local["counter"] = 0
            if not ctx.store.local.get("prefix"):
                ctx.store.local["prefix"] = "Hello"
            await ctx.replace(
                "hello-text",
                Text(
                    f"{ctx.store.local.get('prefix')} {ctx.store.local.get('counter')}",
                    id="hello-text",
                    size="xl",
                    weight="bold",
                ),
            )
            print(ctx.store.local["counter"])
            ctx.store.local["counter"] += 1
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
