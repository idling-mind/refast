import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import Button, Container, Text

ui = RefastApp(title="Hello World App")

async def print_message(ctx: Context):
    await ctx.show_toast("Button clicked!", variant="success")
    print("Hello from the hello.py example!")

@ui.page("/")
def hello_world_page(ctx: Context):
    return Container(
        [
            Text("Hello, World!", id="hello-text", size="xl", weight="bold"),
            Button("Click Me", on_click=ctx.callback(print_message)),
        ],
        class_name="flex flex-row items-center justify-center h-screen gap-4 m-8 p-6",
    )

async def update_value():
    print("Starting periodic updates...")
    while True:
        print("active contexts:", ui.active_contexts)
        for ctx in ui.active_contexts:
            if not ctx.state.get("counter"):
                ctx.state["counter"] = 0
            await ctx.replace("hello-text", Text(f"hi {ctx.state.get('counter')}", id="hello-text", size="xl", weight="bold"))
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