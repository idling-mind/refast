import uvicorn
from fastapi import FastAPI
import random

from refast import Context, RefastApp
from refast.components import (
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Paragraph,
    Row,
    TabItem,
    Tabs,
    ThemeSwitcher,
)
from refast.components.shadcn.charts import (
    Area,
    AreaChart,
    Bar,
    BarChart,
    CartesianGrid,
    ChartConfig,
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
    ComposedChart,
    Funnel,
    FunnelChart,
    Line,
    LineChart,
    Pie,
    PieChart,
    PolarAngleAxis,
    PolarGrid,
    Radar,
    RadarChart,
    RadialBar,
    RadialBarChart,
    ReferenceLine,
    Sankey,
    Scatter,
    ScatterChart,
    Treemap,
    XAxis,
    YAxis,
    ZAxis,
)

ui = RefastApp("Charts Showcase")

def get_data():

    data = {}

    # Sample Data
    months = ["January", "February", "March", "April", "May", "June"]
    browsers = ["Chrome", "Safari", "Firefox", "Edge", "Other"]
    performance_metrics = ["Speed", "Reliability", "Comfort", "Safety", "Efficiency", "Power"]
    colors = ["red", "blue", "green", "orange", "purple"]

    data["area_data"] = [
        {"month": month, "desktop": random.randint(100, 300), "mobile": random.randint(50, 200)}
        for month in months
    ]

    data["bar_data"] = [
        {"month": month, "desktop": random.randint(100, 300), "mobile": random.randint(50, 200)}
        for month in months
    ]

    data["line_data"] = [
        {"month": month, "desktop": random.randint(100, 300)} for month in months
    ]

    data["pie_data"] = [
        {"browser": browser, "visitors": random.randint(50, 300), "fill": f"var(--color-{browser.lower()})"}
        for browser in browsers
    ]

    data["radar_data"] = [
        {
            "skill": metric,
            "desktop": random.randint(20, 100),
            "mobile": random.randint(20, 100),
        }
        for metric in performance_metrics
    ]

    data["radial_data"] = [
        {"activity": f"activity {i+1}", "value": random.randint(20, 100), "fill": f"hsl(var(--chart-{(i%5)+1}))"}
        for i in range(5)
    ]

    # Scatter Chart Data
    data["scatter_data"] = [
        {"x": random.randint(100, 400), "y": random.randint(100, 400), "z": random.randint(100, 400)}
        for _ in range(6)
    ]

    data["scatter_data_2"] = [
        {"x": random.randint(150, 350), "y": random.randint(150, 350), "z": random.randint(100, 400)}
        for _ in range(6)
    ]

    # Composed Chart Data
    data["composed_data"] = [
        {
            "month": month,
            "revenue": random.randint(2000, 5000),
            "profit": random.randint(1000, 3000),
            "orders": random.randint(150, 300),
        }
        for month in months
    ]

    # Funnel Chart Data
    data["funnel_data"] = [
        {"name": "Visited", "value": 5000, "fill": "hsl(var(--chart-1))"},
        {"name": "Cart", "value": 2500, "fill": "hsl(var(--chart-2))"},
        {"name": "Checkout", "value": 1800, "fill": "hsl(var(--chart-3))"},
        {"name": "Purchase", "value": 800, "fill": "hsl(var(--chart-4))"},
    ]

    # Treemap Data
    data["treemap_data"] = [
        {
            "name": "Frontend",
            "children": [
                {"name": "React", "size": 3000, "fill": "hsl(var(--chart-1))"},
                {"name": "Vue", "size": 2000, "fill": "hsl(var(--chart-2))"},
                {"name": "Angular", "size": 1500, "fill": "hsl(var(--chart-3))"},
            ],
        },
        {
            "name": "Backend",
            "children": [
                {"name": "Python", "size": 2500, "fill": "hsl(var(--chart-4))"},
                {"name": "Node", "size": 2000, "fill": "hsl(var(--chart-5))"},
                {"name": "Go", "size": 1000, "fill": "hsl(var(--chart-1))"},
            ],
        },
    ]

    # Sankey Data
    data["sankey_data"] = {
        "nodes": [
            {"name": "Visit"},
            {"name": "Direct"},
            {"name": "Search"},
            {"name": "Social"},
            {"name": "Signup"},
            {"name": "Purchase"},
            {"name": "Bounce"},
        ],
        "links": [
            {"source": 0, "target": 1, "value": 3000},
            {"source": 0, "target": 2, "value": 2500},
            {"source": 0, "target": 3, "value": 1500},
            {"source": 1, "target": 4, "value": 2000},
            {"source": 1, "target": 6, "value": 1000},
            {"source": 2, "target": 4, "value": 1800},
            {"source": 2, "target": 6, "value": 700},
            {"source": 3, "target": 4, "value": 1000},
            {"source": 3, "target": 6, "value": 500},
            {"source": 4, "target": 5, "value": 3500},
            {"source": 4, "target": 6, "value": 1300},
        ],
    }
    return data


async def change_grid_columns(ctx: Context):
    ctx.state["grid_columns"] = ctx.event_data["value"]
    await ctx.refresh()

async def general_callback(ctx: Context):
    print("General callback triggered:", ctx.event_data)

async def update_chart_data(ctx: Context):
    # This function can be used to update chart data dynamically
    # For now, it just prints the event data
    new_data = get_data()
    await ctx.update_props("area-chart", {"data": new_data["area_data"]})
    await ctx.update_props("bar-chart", {"data": new_data["bar_data"]})
    await ctx.update_props("line-chart", {"data": new_data["line_data"]})
    await ctx.update_props("pie-chart", {"data": new_data["pie_data"]})
    await ctx.update_props("radar-chart", {"data": new_data["radar_data"]})
    await ctx.update_props("radial-bar-chart", {"data": new_data["radial_data"]})
    await ctx.update_props("scatter-chart", {"data": new_data["scatter_data"]})
    await ctx.update_props("composed-chart", {"data": new_data["composed_data"]})
    await ctx.show_toast("Chart data updated", variant="success")

@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="min-h-screen p-8 bg-background",
        children=[
            Container(
                class_name="flex flex-col md:flex-row justify-between "
                "items-start md:items-center mb-8 gap-4",
                children=[
                    Column(
                        children=[
                            Heading("Charts Showcase"),
                            Paragraph(
                                "A showcase of various chart types using Refast "
                                "and shadcn/ui components.",
                                class_name="mb-2 text-muted-foreground",
                            ),
                        ],
                    ),
                    Row(
                        [
                            ThemeSwitcher(),
                            Tabs(
                                [
                                    TabItem(label="1 Column", value="1"),
                                    TabItem(label="2 Column", value="2"),
                                    TabItem(label="3 Column", value="3"),
                                ],
                                on_value_change=ctx.callback(change_grid_columns),
                                value=ctx.state.get("grid_columns", "3"),
                            ),
                        ],
                        gap=4,
                    ),
                ],
            ),
            Row(
                children=[
                    Button("Update Chart Data", on_click=ctx.callback(update_chart_data)),
                ],
                class_name="mb-4",
            ),
            Container(
                # class_name="grid grid-cols-1 xl:grid-cols-3 lg:grid-cols-2 gap-8",
                class_name=f"grid grid-cols-{ctx.state.get('grid_columns', '3')} gap-8",
                children=[
                    # Area Chart Section
                    _render_area_chart_card(),
                    # Bar Chart Section
                    _render_bar_chart_card(ctx),
                    # Line Chart Section
                    _render_line_chart_card(),
                    # Pie Chart Section
                    _render_pie_chart_card(),
                    # Radar Chart Section
                    _render_radar_chart_card(),
                    # Radial Chart Section
                    _render_radial_chart_card(),
                    # Scatter Chart Section (NEW)
                    _render_scatter_chart_card(),
                    # Composed Chart Section (NEW)
                    _render_composed_chart_card(),
                    # Funnel Chart Section (NEW)
                    _render_funnel_chart_card(),
                    # NOTE: Treemap and Sankey are commented out for now
                    # as they require special handling outside ResponsiveContainer
                    # # Treemap Section (NEW)
                    # _render_treemap_card(),
                    # # Sankey Section (NEW)
                    # _render_sankey_card(),
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
                        min_height=300,
                        children=AreaChart(
                            id="area-chart",
                            data=get_data()["area_data"],
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


def _render_bar_chart_card(ctx: Context):
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
                        min_height=300,
                        children=BarChart(
                            id="bar-chart",
                            data=get_data()["bar_data"],
                            barGap=10,
                            on_click=ctx.callback(general_callback),
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
                                Bar(data_key="desktop", stack_id="a", fill="var(--color-desktop)"),
                                Bar(data_key="mobile", stack_id="a", fill="var(--color-mobile)"),
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
            CardHeader(
                children=[CardTitle("Line Chart"), CardDescription("Simple trend analysis")]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
                        },
                        min_height=300,
                        children=LineChart(
                            id="line-chart",
                            data=get_data()["line_data"],
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
                        min_height=300,
                        max_height=500,
                        class_name="mx-auto aspect-square",
                        children=PieChart(
                            children=[
                                ChartTooltip(
                                    cursor=False, content=ChartTooltipContent(hide_label=True)
                                ),
                                Pie(
                                    id="pie-chart",
                                    data=get_data()["pie_data"],
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
                children=[
                    CardTitle("Radar Chart"),
                    CardDescription("Performance metrics comparison"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
                            "mobile": ChartConfig(label="Mobile", color="hsl(var(--chart-2))"),
                        },
                        min_height=300,
                        max_height=500,
                        class_name="mx-auto aspect-square",
                        children=RadarChart(
                            id="radar-chart",
                            data=get_data()["radar_data"],
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
                children=[
                    CardTitle("Radial Bar Chart"),
                    CardDescription("Activity progress overview"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        min_height=300,
                        max_height=500,
                        class_name="mx-auto aspect-square",
                        children=RadialBarChart(
                            id="radial-bar-chart",
                            data=get_data()["radial_data"],
                            inner_radius="30%",
                            outer_radius="100%",
                            start_angle=0,
                            end_angle=250,
                            children=[
                                RadialBar(data_key="value", background=False, corner_radius=10),
                                ChartTooltip(
                                    cursor=False, content=ChartTooltipContent()
                                )
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _render_scatter_chart_card():
    """Scatter Chart - NEW chart type for 2D/3D data visualization."""
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Scatter Chart"),
                    CardDescription("Two datasets with different shapes"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "series1": ChartConfig(label="Series A", color="hsl(var(--chart-1))"),
                            "series2": ChartConfig(label="Series B", color="hsl(var(--chart-2))"),
                        },
                        min_height=300,
                        children=ScatterChart(
                            id="scatter-chart",
                            data=get_data()["scatter_data"],
                            margin={"top": 20, "right": 20, "bottom": 20, "left": 20},
                            children=[
                                CartesianGrid(stroke_dasharray="3 3"),
                                XAxis(
                                    data_key="x",
                                    type="number",
                                    name="X Value",
                                    tick_line=False,
                                ),
                                YAxis(
                                    data_key="y",
                                    type="number",
                                    name="Y Value",
                                    tick_line=False,
                                ),
                                ZAxis(data_key="z", range=[60, 400], name="Size"),
                                ChartTooltip(
                                    cursor={"strokeDasharray": "3 3"},
                                    content=ChartTooltipContent(),
                                ),
                                Scatter(
                                    name="Series A",
                                    id="scatter-series-a",
                                    data=get_data()["scatter_data"],
                                    fill="hsl(var(--chart-1))",
                                    shape="circle",
                                ),
                                Scatter(
                                    id="scatter-series-b",
                                    name="Series B",
                                    data=get_data()["scatter_data_2"],
                                    fill="hsl(var(--chart-2))",
                                    shape="diamond",
                                ),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _render_composed_chart_card():
    """Composed Chart - NEW chart type combining Bar, Line, and Area."""
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Composed Chart"),
                    CardDescription("Combining Bar, Line, and Area in one chart"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "revenue": ChartConfig(label="Revenue", color="hsl(var(--chart-1))"),
                            "profit": ChartConfig(label="Profit", color="hsl(var(--chart-2))"),
                            "orders": ChartConfig(label="Orders", color="hsl(var(--chart-3))"),
                        },
                        min_height=300,
                        children=ComposedChart(
                            id="composed-chart",
                            data=get_data()["composed_data"],
                            margin={"top": 20, "right": 20, "bottom": 20, "left": 20},
                            children=[
                                CartesianGrid(stroke_dasharray="3 3", vertical=False),
                                XAxis(
                                    data_key="month",
                                    tick_line=False,
                                    axis_line=False,
                                ),
                                YAxis(tick_line=False, axis_line=False),
                                ChartTooltip(content=ChartTooltipContent()),
                                ChartLegend(content=ChartLegendContent()),
                                Area(
                                    data_key="profit",
                                    type="monotone",
                                    fill="var(--color-profit)",
                                    fill_opacity=0.3,
                                    stroke="var(--color-profit)",
                                ),
                                Bar(
                                    data_key="revenue",
                                    fill="var(--color-revenue)",
                                    radius=[4, 4, 0, 0],
                                ),
                                Line(
                                    data_key="orders",
                                    type="monotone",
                                    stroke="var(--color-orders)",
                                    stroke_width=2,
                                    dot={"r": 4},
                                ),
                                ReferenceLine(
                                    y=200,
                                    stroke="hsl(var(--muted-foreground))",
                                    stroke_dasharray="3 3",
                                ),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _render_funnel_chart_card():
    """Funnel Chart - NEW chart type for conversion visualization."""
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Funnel Chart"),
                    CardDescription("Conversion funnel from visit to purchase"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "value": ChartConfig(label="Users"),
                            "visited": ChartConfig(label="Visited", color="hsl(var(--chart-1))"),
                            "cart": ChartConfig(label="Cart", color="hsl(var(--chart-2))"),
                            "checkout": ChartConfig(label="Checkout", color="hsl(var(--chart-3))"),
                            "purchase": ChartConfig(label="Purchase", color="hsl(var(--chart-4))"),
                        },
                        min_height=300,
                        children=FunnelChart(
                            children=[
                                ChartTooltip(content=ChartTooltipContent()),
                                Funnel(
                                    id="funnel-chart",
                                    data=get_data()["funnel_data"],
                                    data_key="value",
                                    name_key="name",
                                    label=True,
                                    is_animation_active=True,
                                    animation_duration=800,
                                ),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _render_treemap_card():
    """Treemap - NEW chart type for hierarchical data."""
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Treemap"),
                    CardDescription("Technology stack distribution by usage"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "size": ChartConfig(label="Usage"),
                        },
                        min_height=300,
                        children=Treemap(
                            id="treemap-chart",
                            data=get_data()["treemap_data"],
                            data_key="size",
                            name_key="name",
                            aspect_ratio=4 / 3,
                            stroke="#fff",
                            is_animation_active=True,
                            animation_duration=800,
                        ),
                    )
                ]
            ),
        ]
    )


def _render_sankey_card():
    """Sankey Diagram - NEW chart type for flow visualization."""
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Sankey Diagram"),
                    CardDescription("User flow from visit to conversion"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config={
                            "value": ChartConfig(label="Users"),
                        },
                        min_height=350,
                        children=Sankey(
                            id="sankey-chart",
                            data=get_data()["sankey_data"],
                            node_padding=20,
                            node_width=10,
                            link_curvature=0.5,
                            height=300,
                            margin={"top": 10, "right": 10, "bottom": 10, "left": 10},
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
