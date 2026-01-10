from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components.shadcn import (
    Alert,
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    Heading,
    Paragraph,
    ThemeSwitcher,
)
from refast.components.shadcn.layout import Column, Flex, Grid, Row

ui = RefastApp("Colors Showcase")
app = FastAPI(title="Colors Showcase App")


def render_color_swatch(color_name: str, shade: int, bg_class: str, text_class: str) -> Flex:
    """Render a single color swatch with shade label."""
    return Flex(
        class_name=f"{bg_class} rounded-md h-24 w-full p-2 flex flex-col justify-end items-start border",
        children=[
            Paragraph(text=str(shade), class_name=f"{text_class} text-xs font-mono font-bold"),
        ],
    )


def render_palette_row(color_name: str, base_color: str) -> Column:
    """Render a full row of shades for a given color using CSS classes."""
    shades = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

    return Column(
        class_name="mb-6",
        children=[
            Heading(
                text=color_name,
                level=4,
                class_name="mb-2 text-sm font-semibold capitalize text-muted-foreground",
            ),
            Grid(
                columns=11,
                gap=2,
                class_name="w-full",
                children=[
                    render_color_swatch(
                        color_name,
                        shade,
                        f"bg-{base_color}-{shade}",
                        "text-white" if shade >= 400 else "text-black",
                    )
                    for shade in shades
                ],
            ),
        ],
    )


@ui.page("/")
def home(ctx: Context) -> Flex:
    return Flex(
        direction="column",
        gap="xl",
        class_name="container mx-auto py-xl gap-xl",
        children=[
            # Header
            Row(
                [
                    Column(
                        class_name="",
                        children=[
                            Heading(
                                text="Refast Color Palette Showcase",
                                level=1,
                                class_name="text-4xl font-bold tracking-tight",
                            ),
                            Paragraph(
                                text="Demonstration of semantic colors and the extended Tailwind color palette integration.",
                                class_name="text-lg text-muted-foreground",
                            ),
                        ],
                    ),
                    Column([ThemeSwitcher()]),
                ],
                class_name="items-center justify-between mb-4 mt-8",
            ),
            # Semantic Colors Section
            Card(
                class_name="border-l-8 border-primary mb-8",
                children=[
                    CardHeader(
                        title="Semantic Colors",
                        description="Core functional colors acting as indicators for state.",
                    ),
                    CardContent(
                        class_name="space-y-8",
                        children=[
                            # Alerts
                            Grid(
                                columns=2,
                                gap=6,
                                children=[
                                    Alert(
                                        title="Success",
                                        message="Operation completed successfully. (bg-success)",
                                        variant="success",
                                        dismissible=True,
                                        # Note: If python validation fails for variant, we might need to rely on class_name
                                        # But let's assume it passes or we suppress it.
                                        # Actually, the python type hint is just a hint, runtime it might pass if not strictly checked in __init__
                                        # But if it is checked, we can use class_name="bg-success/15 text-success border-success/50" manually
                                    ),
                                    Alert(
                                        title="Warning",
                                        message="Please be careful with this action. (bg-warning)",
                                        variant="warning",
                                    ),
                                    Alert(
                                        title="Info",
                                        message="Here is some useful information. (bg-info)",
                                        variant="info",
                                    ),
                                    Alert(
                                        title="Destructive (Failure)",
                                        message="Something went wrong. (bg-destructive)",
                                        variant="destructive",
                                    ),
                                ],
                            ),
                            # Buttons
                            Column(
                                gap=2,
                                children=[
                                    Paragraph(
                                        text="Buttons with semantic colors",
                                        class_name="text-sm font-medium text-muted-foreground",
                                    ),
                                    Flex(
                                        gap=4,
                                        wrap="wrap",
                                        children=[
                                            Button("Default Button"),
                                            Button(
                                                "Success Action",
                                                class_name="bg-success text-success-foreground hover:bg-success/90",
                                            ),
                                            Button(
                                                "Warning Action",
                                                class_name="bg-warning text-warning-foreground hover:bg-warning/90",
                                            ),
                                            Button(
                                                "Info Action",
                                                class_name="bg-info text-info-foreground hover:bg-info/90",
                                            ),
                                            Button("Destructive Action", variant="destructive"),
                                        ],
                                    ),
                                ],
                            ),
                            # Badges
                            Column(
                                gap=2,
                                children=[
                                    Paragraph(
                                        text="Badges",
                                        class_name="text-sm font-medium text-muted-foreground",
                                    ),
                                    Flex(
                                        gap=2,
                                        children=[
                                            Badge(children=["Default"]),
                                            Badge(children=["Success"], variant="success"),
                                            Badge(children=["Warning"], variant="warning"),
                                            Badge(children=["Destructive"], variant="destructive"),
                                            # Manual info badge since it might not be in the literal
                                            Badge(
                                                children=["Info"],
                                                class_name="bg-info text-info-foreground hover:bg-info/80 border-transparent",
                                            ),
                                            Badge(children=["Outline"], variant="outline"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Palette Colors Section
            Card(
                children=[
                    CardHeader(
                        title="Extended Palette",
                        description="Full range of Tailwind colors (50-950) available for custom styling.",
                    ),
                    CardContent(
                        children=[
                            render_palette_row("Red", "red"),
                            render_palette_row("Orange", "orange"),
                            render_palette_row("Yellow", "yellow"),
                            render_palette_row("Green", "green"),
                            render_palette_row("Teal", "teal"),
                            render_palette_row("Blue", "blue"),
                            render_palette_row("Purple", "purple"),
                            render_palette_row("Pink", "pink"),
                            render_palette_row("Gray", "gray"),
                            render_palette_row("Slate (Default Gray)", "slate"),
                        ]
                    ),
                ]
            ),
        ],
    )


app.include_router(ui.router)  # Mount the Refast app onto the FastAPI app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
