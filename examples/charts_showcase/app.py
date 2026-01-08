import uvicorn
from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Grid,
    Heading,
    Paragraph,
    Row,
    Text,
)
from refast.components.shadcn.charts import (
    Area,
    AreaChart,
    Bar,
    BarChart,
    CartesianGrid,
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
    Line,
    LineChart,
    Pie,
    PieChart,
    PieLabel,
    PolarAngleAxis,
    PolarGrid,
    PolarRadiusAxis,
    Radar,
    RadarChart,
    RadialBar,
    RadialBarChart,
    Sector,
    XAxis,
    YAxis,
)

ui = RefastApp("Charts Showcase")

# Sample Data
AREA_DATA = [
    {"month": "January", "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March", "desktop": 237, "mobile": 120},
    {"month": "April", "desktop": 73, "mobile": 190},
    {"month": "May", "desktop": 209, "mobile": 130},
    {"month": "June", "desktop": 214, "mobile": 140},
]

BAR_DATA = [
    {"month": "January", "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March", "desktop": 237, "mobile": 120},
    {"month": "April", "desktop": 73, "mobile": 190},
    {"month": "May", "desktop": 209, "mobile": 130},
    {"month": "June", "desktop": 214, "mobile": 140},
]

LINE_DATA = [
    {"month": "January", "desktop": 186},
    {"month": "February", "desktop": 305},
    {"month": "March", "desktop": 237},
    {"month": "April", "desktop": 73},
    {"month": "May", "desktop": 209},
    {"month": "June", "desktop": 214},
]

PIE_DATA = [
    {"browser": "chrome", "visitors": 275, "fill": "var(--color-chrome)"},
    {"browser": "safari", "visitors": 200, "fill": "var(--color-safari)"},
    {"browser": "firefox", "visitors": 187, "fill": "var(--color-firefox)"},
    {"browser": "edge", "visitors": 173, "fill": "var(--color-edge)"},
    {"browser": "other", "visitors": 90, "fill": "var(--color-other)"},
]

RADAR_DATA = [
    {"skill": "Speed", "desktop": 120, "mobile": 110},
    {"skill": "Reliability", "desktop": 98, "mobile": 130},
    {"skill": "Comfort", "desktop": 86, "mobile": 130},
    {"skill": "Safety", "desktop": 99, "mobile": 100},
    {"skill": "Efficiency", "desktop": 85, "mobile": 90},
    {"skill": "Power", "desktop": 65, "mobile": 85},
]

RADIAL_DATA = [
    {"activity": "activity 1", "value": 70, "fill": "var(--color-chrome)"},
    {"activity": "activity 2", "value": 50, "fill": "var(--color-safari)"},
    {"activity": "activity 3", "value": 30, "fill": "var(--color-firefox)"},
]


@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="min-h-screen p-8 bg-background",
        children=[
            Heading("Refast Charts Showcase", class_name="mb-4 text-3xl font-bold"),
            Paragraph(
                "A collection of beautiful charts built with Recharts and shadcn/ui.",
                class_name="mb-8 text-muted-foreground",
            ),
            Grid(
                class_name="grid-cols-1 md:grid-cols-2 gap-8",
                children=[
                    # Area Chart Section
                    _render_area_chart_card(),
                    # Bar Chart Section
                    _render_bar_chart_card(),
                    # Line Chart Section
                    _render_line_chart_card(),
                    # Pie Chart Section
                    _render_pie_chart_card(),
                    # Radar Chart Section
                    _render_radar_chart_card(),
                    # Radial Chart Section
                    _render_radial_chart_card(),
                ],
            ),
        ],
    )


def _render_area_chart_card():
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Area Chart - Stacked"),
                    CardDescription("Showing desktop and mobile visitors over time"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
                            "mobile": ChartConfig(label="Mobile", color="hsl(var(--chart-2))"),
                        },
                        children=AreaChart(
                            data=AREA_DATA,
                            children=[
                                CartesianGrid(vertical=False),
                                XAxis(
                                    data_key="month",
                                    tick_line=False,
                                    axis_line=False,
                                    tick_margin=8,
                                    tick_formatter="value.slice(0,3)",
                                ),
                                ChartTooltip(
                                    cursor=False, content=ChartTooltipContent(indicator="dot")
                                ),
                                Area(
                                    data_key="mobile",
                                    type="natural",
                                    fill="var(--color-mobile)",
                                    fill_opacity=0.4,
                                    stroke="var(--color-mobile)",
                                    stacked_id="a",
                                ),
                                Area(
                                    data_key="desktop",
                                    type="natural",
                                    fill="var(--color-desktop)",
                                    fill_opacity=0.4,
                                    stroke="var(--color-desktop)",
                                    stacked_id="a",
                                ),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _render_bar_chart_card():
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Bar Chart - Multiple"),
                    CardDescription("Comparing desktop vs mobile usage"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
                            "mobile": ChartConfig(label="Mobile", color="hsl(var(--chart-2))"),
                        },
                        children=BarChart(
                            data=BAR_DATA,
                            children=[
                                CartesianGrid(vertical=False),
                                XAxis(
                                    data_key="month",
                                    tick_line=False,
                                    tick_margin=10,
                                    axis_line=False,
                                    tick_formatter="value.slice(0,3)",
                                ),
                                ChartTooltip(
                                    cursor=False, content=ChartTooltipContent(indicator="dashed")
                                ),
                                Bar(data_key="desktop", fill="var(--color-desktop)", radius=4),
                                Bar(data_key="mobile", fill="var(--color-mobile)", radius=4),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _render_line_chart_card():
    return Card(
        children=[
            CardHeader(children=[CardTitle("Line Chart"), CardDescription("Simple trend analysis")]),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
                        },
                        children=LineChart(
                            data=LINE_DATA,
                            margin={"left": 12, "right": 12, "top": 12, "bottom": 12},
                            children=[
                                CartesianGrid(vertical=False),
                                XAxis(
                                    data_key="month",
                                    tick_line=False,
                                    axis_line=False,
                                    tick_margin=8,
                                    tick_formatter="value.slice(0,3)",
                                ),
                                ChartTooltip(
                                    cursor=False, content=ChartTooltipContent(hide_label=False)
                                ),
                                Line(
                                    data_key="desktop",
                                    type="natural",
                                    stroke="var(--color-desktop)",
                                    stroke_width=2,
                                    dot=False,
                                ),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _render_pie_chart_card():
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Pie Chart - Donut"),
                    CardDescription("Browser market share distribution"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "chrome": ChartConfig(label="Chrome", color="hsl(var(--chart-1))"),
                            "safari": ChartConfig(label="Safari", color="hsl(var(--chart-2))"),
                            "firefox": ChartConfig(label="Firefox", color="hsl(var(--chart-3))"),
                            "edge": ChartConfig(label="Edge", color="hsl(var(--chart-4))"),
                            "other": ChartConfig(label="Other", color="hsl(var(--chart-5))"),
                        },
                        class_name="mx-auto aspect-square max-h-[250px]",
                        children=PieChart(
                            children=[
                                ChartTooltip(
                                    cursor=False, content=ChartTooltipContent(hide_label=True)
                                ),
                                Pie(
                                    data=PIE_DATA,
                                    data_key="visitors",
                                    name_key="browser",
                                    inner_radius=60,
                                    label=False,
                                ),
                            ]
                        ),
                    )
                ]
            ),
        ]
    )


def _render_radar_chart_card():
    return Card(
        children=[
            CardHeader(
                children=[CardTitle("Radar Chart"), CardDescription("Performance metrics comparison")]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
                            "mobile": ChartConfig(label="Mobile", color="hsl(var(--chart-2))"),
                        },
                        class_name="mx-auto aspect-square max-h-[250px]",
                        children=RadarChart(
                            data=RADAR_DATA,
                            children=[
                                ChartTooltip(cursor=False, content=ChartTooltipContent()),
                                PolarGrid(),
                                PolarAngleAxis(data_key="skill"),
                                Radar(
                                    data_key="desktop",
                                    fill="var(--color-desktop)",
                                    fill_opacity=0.6,
                                ),
                                Radar(
                                    data_key="mobile", fill="var(--color-mobile)", fill_opacity=0.6
                                ),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _render_radial_chart_card():
    return Card(
        children=[
            CardHeader(
                children=[CardTitle("Radial Bar Chart"), CardDescription("Activity progress overview")]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "visitors": ChartConfig(label="Visitors"),
                            "chrome": ChartConfig(label="Chrome", color="hsl(var(--chart-1))"),
                            "safari": ChartConfig(label="Safari", color="hsl(var(--chart-2))"),
                            "firefox": ChartConfig(label="Firefox", color="hsl(var(--chart-3))"),
                        },
                        class_name="mx-auto aspect-square max-h-[250px]",
                        children=RadialBarChart(
                            data=RADIAL_DATA,
                            inner_radius="30%",
                            outer_radius="100%",
                            start_angle=0,
                            end_angle=250,
                            children=[
                                RadialBar(data_key="value", background=False, corner_radius=10),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    uvicorn.run(app)
