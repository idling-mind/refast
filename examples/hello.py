import asyncio

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Button,
    Center,
    Column,
    Heading,
    Input,
    Row,
    Text,
    ThemeSwitcher,
    Tooltip,
)

ui = RefastApp(title="Hello World App")

async def change_title(ctx: Context, input_name: str):
    """Change the page title to greet the user."""
    if ctx.state.get("counter", 0) > 0:
        await ctx.show_toast("You are persistent, aren't you? Hello again!")
    ctx.state.set("counter", ctx.state.get("counter", 0) + 1)  # Example of using state
    await ctx.update_text("page_title", f"Hello, {input_name}!")
    await asyncio.sleep(5)  # Simulate a delay for demonstration
    await ctx.show_toast("Had your time in the spotlight? Now back to the World!")
    await asyncio.sleep(2)
    await ctx.update_text("page_title", "Hello, World!")


@ui.page("/")
def hello_world_page(ctx: Context):
    return Center(
        Column(
            [
                Heading("Hello, World!", id="page_title", level=1),
                Text("Welcome to your first Refast app."),
                Row(
                    [
                        Input(placeholder="What is your name?", on_change=ctx.save_prop("input_name")),
                        Tooltip(
                            "Type in your name and click the button.",
                            children=Button("Ok", variant="primary", on_click=ctx.callback(change_title, props=["input_name"])),
                        ),
                    ]
                ),
                ThemeSwitcher(),
            ],
            align="center",
            # Full view height
        ),
        class_name="h-screen"
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
