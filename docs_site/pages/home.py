"""Home page — / — Landing page for the Refast documentation site."""

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
    Flex,
    Grid,
    Heading,
    Icon,
    Markdown,
    Row,
    Separator,
    Text,
)

PAGE_TITLE = "Home"
PAGE_ROUTE = "/"


def render(ctx):
    """Render the documentation home page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-5xl mx-auto p-6",
        children=[
            # Hero section
            Column(
                gap=4,
                class_name="text-center py-12",
                children=[
                    Row([Badge(["v0.1.0"], variant="secondary")], justify="center"),
                    Heading("Refast", level=1, class_name="text-5xl font-bold"),
                    Text(
                        "Build reactive web apps with Python. Powered by FastAPI and React.",
                        class_name="text-xl text-muted-foreground max-w-2xl mx-auto",
                    ),
                    Row(
                        gap=3,
                        justify="center",
                        class_name="mt-4",
                        children=[
                            Button(
                                "Get Started",
                                on_click=ctx.callback(_nav, path="/docs/getting-started"),
                            ),
                            Button(
                                "View Examples",
                                variant="outline",
                                on_click=ctx.callback(_nav, path="/docs/examples"),
                            ),
                        ],
                    ),
                ],
            ),
            Separator(),
            # Quick install
            Markdown(
                content="""
```python
pip install refast
```
""",
                class_name="my-6",
            ),
            # Feature cards
            Grid(
                columns=3,
                gap=6,
                class_name="my-8",
                children=[
                    _feature_card(
                        "Python First",
                        "box",
                        "Define your entire UI in Python. No HTML, no templates, no JavaScript required.",
                    ),
                    _feature_card(
                        "Reactive Updates",
                        "refresh-cw",
                        "Push real-time updates via WebSocket. Targeted DOM updates without full page reloads.",
                    ),
                    _feature_card(
                        "FastAPI Native",
                        "zap",
                        "Plugs into any FastAPI app with include_router(). Full async/await support.",
                    ),
                    _feature_card(
                        "60+ Components",
                        "component",
                        "Full shadcn/ui component library — buttons, forms, cards, charts, dialogs, and more.",
                    ),
                    _feature_card(
                        "Type Safe",
                        "shield",
                        "Complete type hints and Pydantic validation. Catch errors before runtime.",
                    ),
                    _feature_card(
                        "Extensible",
                        "puzzle",
                        "Build custom components and extensions. Publish and share via entry points.",
                    ),
                ],
            ),
            Separator(),
            # Minimal example
            Column(
                gap=4,
                class_name="my-8",
                children=[
                    Heading("Minimal Example", level=2, class_name="text-center"),
                    Markdown(
                        content="""
```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Button, Text

ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    async def on_click(ctx: Context):
        await ctx.show_toast("Hello from Refast!", variant="success")

    return Container(
        class_name="p-8",
        children=[
            Text("Welcome to Refast!"),
            Button("Click Me", on_click=ctx.callback(on_click)),
        ],
    )

app = FastAPI()
app.include_router(ui.router)
```
"""
                    ),
                ],
            ),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


async def _nav(ctx, path: str = "/"):
    await ctx.navigate(path)


def _feature_card(title: str, icon: str, description: str):
    """Create a feature highlight card."""
    return Card(
        children=[
            CardHeader(
                children=[
                    Row(
                        gap=2,
                        align="center",
                        children=[
                            Icon(icon, class_name="text-primary"),
                            CardTitle(title),
                        ],
                    ),
                ],
            ),
            CardContent(
                children=[
                    Text(description, class_name="text-muted-foreground text-sm"),
                ],
            ),
        ],
    )
