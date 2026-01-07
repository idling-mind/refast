"""SPA Navigation Example.

This example demonstrates:
- Single Page Application (SPA) navigation
- Conditional rendering based on state
- Shared layout (Navbar)
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Button,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Container,
    Row,
    Text,
)

ui = RefastApp(title="SPA Example")

# We need to define render_app later, but navigate needs to call it.
# Since Python resolves names at runtime, this is fine as long as render_app
# is defined before navigate is CALLED.


async def navigate(ctx: Context, page: str):
    """Navigate to a different page."""
    ctx.state.set("current_page", page)
    await ctx.replace("root-container", render_app(ctx))


def navbar(ctx: Context, current_page: str):
    """Render the navigation bar."""
    pages = ["Home", "About", "Settings"]

    return Card(
        class_name="mb-4",
        children=[
            CardContent(
                class_name="p-6",
                children=[
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Text("My App", class_name="font-bold text-xl"),
                            Row(
                                gap=2,
                                children=[
                                    Button(
                                        page,
                                        variant="default" if current_page == page else "ghost",
                                        on_click=ctx.callback(navigate, page=page),
                                    )
                                    for page in pages
                                ],
                            ),
                        ],
                    )
                ],
            )
        ],
    )


def home_page():
    return Card(
        children=[
            CardHeader(children=[CardTitle("Home Page")]),
            CardContent(children=[Text("Welcome to the home page!")]),
        ]
    )


def about_page():
    return Card(
        children=[
            CardHeader(children=[CardTitle("About Us")]),
            CardContent(children=[Text("We are a company that builds cool stuff.")]),
        ]
    )


def settings_page(ctx: Context):
    notifications = ctx.state.get("notifications", True)

    async def toggle_notifications(ctx: Context):
        ctx.state.set("notifications", not ctx.state.get("notifications", True))
        await ctx.replace("root-container", render_app(ctx))

    return Card(
        children=[
            CardHeader(children=[CardTitle("Settings")]),
            CardContent(
                children=[
                    Row(
                        align="center",
                        justify="between",
                        children=[
                            Text("Enable Notifications"),
                            Button(
                                "On" if notifications else "Off",
                                variant="outline" if notifications else "secondary",
                                on_click=ctx.callback(toggle_notifications),
                            ),
                        ],
                    )
                ]
            ),
        ]
    )


def render_app(ctx: Context):
    """Render the entire application."""
    current_page = ctx.state.get("current_page", "Home")

    content = None
    if current_page == "Home":
        content = home_page()
    elif current_page == "About":
        content = about_page()
    elif current_page == "Settings":
        content = settings_page(ctx)

    return Container(
        id="root-container",
        class_name="max-w-4xl mx-auto mt-10 p-4",
        children=[
            navbar(ctx, current_page),
            content,
        ],
    )


@ui.page("/")
def main(ctx: Context):
    return render_app(ctx)


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
