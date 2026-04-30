"""Area Chart — /docs/components/area-chart."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)
from refast.components.shadcn.charts import (
    Area,
    AreaChart,
    CartesianGrid,
    ChartConfig,
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
    XAxis,
)

PAGE_TITLE = "Area Chart"
PAGE_ROUTE = "/docs/components/area-chart"

SAMPLE_DATA = [
    {"month": "January",  "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March",    "desktop": 237, "mobile": 120},
    {"month": "April",    "desktop": 73,  "mobile": 190},
    {"month": "May",      "desktop": 209, "mobile": 130},
    {"month": "June",     "desktop": 214, "mobile": 140},
]

CHART_CONFIG = {
    "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
    "mobile":  ChartConfig(label="Mobile",  color="hsl(var(--chart-2))"),
}

FILL_OPTIONS = [
    {"value": "solid",    "label": "Solid"},
    {"value": "gradient", "label": "Gradient"},
]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _ac_set_fill_type(ctx: Context, value: str):
    ctx.state.set("ac_fill_type", value)
    await ctx.refresh()


async def _ac_set_stacked(ctx: Context, value: bool):
    ctx.state.set("ac_stacked", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    fill_type = ctx.state.get("ac_fill_type", "solid")
    stacked   = ctx.state.get("ac_stacked",   False)

    fill_opacity = 0.8 if fill_type == "solid" else 0.3
    stack_id_desktop = "areas" if stacked else None
    stack_id_mobile  = "areas" if stacked else None

    chart_children = [
        CartesianGrid(vertical=False),
        XAxis(data_key="month", tick_line=False, axis_line=False),
        ChartTooltip(content=ChartTooltipContent()),
        ChartLegend(content=ChartLegendContent()),
        Area(
            data_key="desktop",
            fill="var(--color-desktop)",
            stroke="var(--color-desktop)",
            fill_opacity=fill_opacity,
            stacked_id=stack_id_desktop,
            type="monotone",
        ),
        Area(
            data_key="mobile",
            fill="var(--color-mobile)",
            stroke="var(--color-mobile)",
            fill_opacity=fill_opacity,
            stacked_id=stack_id_mobile,
            type="monotone",
        ),
    ]

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    Row(gap=4, wrap=True, class_name="mb-4", children=[
                        Column(gap=1, children=[
                            Text("Fill type", class_name="text-sm font-medium"),
                            Select(
                                options=FILL_OPTIONS,
                                value=fill_type,
                                on_change=ctx.callback(_ac_set_fill_type),
                            ),
                        ]),
                        Column(gap=1, children=[
                            Text("Stacked", class_name="text-sm font-medium"),
                            Checkbox(label="stacked", checked=stacked, on_change=ctx.callback(_ac_set_stacked)),
                        ]),
                    ]),
                    ChartContainer(
                        config=CHART_CONFIG,
                        class_name="h-64",
                        children=[
                            AreaChart(
                                data=SAMPLE_DATA,
                                children=chart_children,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# ── Page render ───────────────────────────────────────────────────────────


def render(ctx: Context):
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _playground(ctx),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Content ───────────────────────────────────────────────────────────────

INTRO = """
Area charts are like line charts but with the region below the line filled in,
making them useful for showing volume, cumulative totals, or part-to-whole relationships.

```python
from refast.components.shadcn.charts import (
    ChartContainer, ChartConfig, AreaChart, Area,
    CartesianGrid, XAxis,
    ChartTooltip, ChartTooltipContent,
    ChartLegend, ChartLegendContent,
)

config = {
    "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
    "mobile":  ChartConfig(label="Mobile",  color="hsl(var(--chart-2))"),
}

data = [
    {"month": "January",  "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March",    "desktop": 237, "mobile": 120},
]

ChartContainer(config=config, class_name="h-64", children=[
    AreaChart(data=data, children=[
        CartesianGrid(vertical=False),
        XAxis(data_key="month", tick_line=False, axis_line=False),
        ChartTooltip(content=ChartTooltipContent()),
        ChartLegend(content=ChartLegendContent()),
        Area(data_key="desktop", fill="var(--color-desktop)", stroke="var(--color-desktop)",
             fill_opacity=0.4, type="monotone"),
        Area(data_key="mobile",  fill="var(--color-mobile)",  stroke="var(--color-mobile)",
             fill_opacity=0.4, type="monotone"),
    ]),
])
```

### Stacked Area Chart

Pass the same `stacked_id` to multiple `Area` components to stack them:

```python
Area(data_key="desktop", fill="var(--color-desktop)", stacked_id="areas", ...)
Area(data_key="mobile",  fill="var(--color-mobile)",  stacked_id="areas", ...)
```
"""

REFERENCE = """
## AreaChart Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict]` | *(required)* | Array of data objects |
| `layout` | `"horizontal" \\| "vertical"` | `"horizontal"` | Chart orientation |
| `margin` | `dict` | `{top:10, right:10, left:10, bottom:0}` | Chart margins |
| `stack_offset` | `str \\| None` | `None` | `"expand"`, `"wiggle"`, `"silhouette"` for stacked areas |
| `base_value` | `int \\| str \\| None` | `None` | Baseline value for areas |
| `on_click` | `Callback \\| None` | `None` | Click on the chart |
| `children` | `list` | `[]` | Axes, areas, tooltip, legend |

## Area Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str` | *(required)* | Key from data objects |
| `type` | `str` | `"natural"` | Interpolation: `"linear"`, `"monotone"`, `"step"`, `"natural"` |
| `fill` | `str` | `"hsl(var(--chart-1))"` | Area fill color |
| `fill_opacity` | `float` | `0.4` | Fill opacity (0–1). Use `0.8` for solid, `0.3` for gradient-like |
| `stroke` | `str \\| None` | *(same as fill)* | Line stroke color |
| `stroke_width` | `int` | `2` | Stroke width in pixels |
| `stacked_id` | `str \\| None` | `None` | Areas sharing the same `stacked_id` are stacked |
| `dot` | `bool \\| dict` | `False` | Show data-point dots |
| `connect_nulls` | `bool` | `False` | Connect across null values |
| `base_value` | `int \\| str \\| None` | `None` | Override baseline for this area |
| `label` | `bool \\| dict \\| None` | `None` | Show value labels |
| `hide` | `bool` | `False` | Hide this area series |
"""
