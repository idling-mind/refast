"""Other Charts — /docs/components/other-charts."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Container,
    Heading,
    Markdown,
    Separator,
)
from refast.components.shadcn.charts import (
    Cell,
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
    PolarAngleAxis,
    PolarGrid,
    Radar,
    RadarChart,
    RadialBar,
    RadialBarChart,
    Scatter,
    ScatterChart,
    XAxis,
    YAxis,
)

PAGE_TITLE = "Other Charts"
PAGE_ROUTE = "/docs/components/other-charts"

# ── Sample data ───────────────────────────────────────────────────────────

RADAR_DATA = [
    {"subject": "Python",      "score": 90},
    {"subject": "TypeScript",  "score": 75},
    {"subject": "React",       "score": 80},
    {"subject": "FastAPI",     "score": 85},
    {"subject": "CSS",         "score": 60},
    {"subject": "Testing",     "score": 70},
]

RADIAL_DATA = [
    {"name": "Design",     "value": 80,  "fill": "hsl(var(--chart-1))"},
    {"name": "Development","value": 65,  "fill": "hsl(var(--chart-2))"},
    {"name": "Testing",    "value": 50,  "fill": "hsl(var(--chart-3))"},
    {"name": "Deployment", "value": 90,  "fill": "hsl(var(--chart-4))"},
]

SCATTER_DATA = [
    {"x": 10, "y": 30},
    {"x": 20, "y": 45},
    {"x": 30, "y": 25},
    {"x": 40, "y": 60},
    {"x": 50, "y": 40},
    {"x": 60, "y": 70},
    {"x": 70, "y": 55},
    {"x": 80, "y": 80},
    {"x": 90, "y": 65},
    {"x": 100,"y": 90},
]


# ── Static chart builders ─────────────────────────────────────────────────


def _radar_chart():
    config = {
        "score": ChartConfig(label="Score", color="hsl(var(--chart-1))"),
    }
    return Card(
        children=[
            CardHeader(title="Radar Chart — Skills Assessment"),
            CardContent(
                children=[
                    ChartContainer(
                        config=config,
                        class_name="h-72",
                        children=[
                            RadarChart(
                                data=RADAR_DATA,
                                children=[
                                    PolarGrid(),
                                    PolarAngleAxis(data_key="subject"),
                                    ChartTooltip(content=ChartTooltipContent()),
                                    Radar(
                                        data_key="score",
                                        fill="var(--color-score)",
                                        fill_opacity=0.5,
                                        stroke="var(--color-score)",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _radial_bar_chart():
    config = {
        "value": ChartConfig(label="Progress", color="hsl(var(--chart-1))"),
    }
    radial_cells = [
        Cell(extra_props={"fill": item["fill"]}) for item in RADIAL_DATA
    ]
    return Card(
        children=[
            CardHeader(title="Radial Bar Chart — Progress Bars"),
            CardContent(
                children=[
                    ChartContainer(
                        config=config,
                        class_name="h-72",
                        children=[
                            RadialBarChart(
                                data=RADIAL_DATA,
                                inner_radius="20%",
                                outer_radius="90%",
                                bar_size=18,
                                children=[
                                    RadialBar(
                                        data_key="value",
                                        background=True,
                                        corner_radius=4,
                                        children=radial_cells,
                                    ),
                                    ChartTooltip(content=ChartTooltipContent()),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _scatter_chart():
    config = {
        "correlation": ChartConfig(label="Correlation", color="hsl(var(--chart-2))"),
    }
    return Card(
        children=[
            CardHeader(title="Scatter Chart — Correlation Plot"),
            CardContent(
                children=[
                    ChartContainer(
                        config=config,
                        class_name="h-72",
                        children=[
                            ScatterChart(
                                children=[
                                    XAxis(data_key="x", tick_line=False, axis_line=False),
                                    YAxis(data_key="y", tick_line=False, axis_line=False),
                                    ChartTooltip(content=ChartTooltipContent()),
                                    Scatter(
                                        data=SCATTER_DATA,
                                        fill="var(--color-correlation)",
                                    ),
                                ],
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
            Markdown(content=RADAR_SECTION),
            _radar_chart(),
            Markdown(content=RADIAL_SECTION),
            _radial_bar_chart(),
            Markdown(content=SCATTER_SECTION),
            _scatter_chart(),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Content ───────────────────────────────────────────────────────────────

INTRO = """
Beyond bar, line, area, and pie charts, Refast supports several specialised chart types
for specific data visualisation needs.
"""

RADAR_SECTION = """
---

## Radar Chart

Radar charts (also called spider or web charts) show multivariate data on a 2D plane
with axes emanating from a common centre. Ideal for comparing entities across multiple
quantitative dimensions.

```python
from refast.components.shadcn.charts import (
    ChartContainer, ChartConfig,
    RadarChart, Radar, PolarGrid, PolarAngleAxis,
    ChartTooltip, ChartTooltipContent,
)

config = {"score": ChartConfig(label="Score", color="hsl(var(--chart-1))")}

data = [
    {"subject": "Python",     "score": 90},
    {"subject": "TypeScript", "score": 75},
    {"subject": "React",      "score": 80},
]

ChartContainer(config=config, class_name="h-72", children=[
    RadarChart(data=data, children=[
        PolarGrid(),
        PolarAngleAxis(data_key="subject"),
        ChartTooltip(content=ChartTooltipContent()),
        Radar(
            data_key="score",
            fill="var(--color-score)",
            fill_opacity=0.5,
            stroke="var(--color-score)",
        ),
    ]),
])
```
"""

RADIAL_SECTION = """
---

## Radial Bar Chart

Radial bar charts display values as arcs on a polar plane. They work well as
progress indicators or for comparing a small number of categories in a compact space.

```python
from refast.components.shadcn.charts import (
    ChartContainer, ChartConfig,
    RadialBarChart, RadialBar, Cell,
    ChartTooltip, ChartTooltipContent,
)

config = {"value": ChartConfig(label="Progress", color="hsl(var(--chart-1))")}

data = [
    {"name": "Design",      "value": 80,  "fill": "hsl(var(--chart-1))"},
    {"name": "Development", "value": 65,  "fill": "hsl(var(--chart-2))"},
    {"name": "Testing",     "value": 50,  "fill": "hsl(var(--chart-3))"},
]

cells = [Cell(extra_props={"fill": item["fill"]}) for item in data]

ChartContainer(config=config, class_name="h-72", children=[
    RadialBarChart(data=data, inner_radius="20%", outer_radius="90%", bar_size=18,
        children=[
            RadialBar(data_key="value", background=True, corner_radius=4, children=cells),
            ChartTooltip(content=ChartTooltipContent()),
        ],
    ),
])
```
"""

SCATTER_SECTION = """
---

## Scatter Chart

Scatter charts plot individual data points on X/Y axes, making it easy to spot
correlations, clusters, and outliers.

```python
from refast.components.shadcn.charts import (
    ChartContainer, ChartConfig,
    ScatterChart, Scatter,
    XAxis, YAxis,
    ChartTooltip, ChartTooltipContent,
)

config = {"points": ChartConfig(label="Points", color="hsl(var(--chart-2))")}

data = [
    {"x": 10, "y": 30},
    {"x": 40, "y": 60},
    {"x": 70, "y": 55},
]

ChartContainer(config=config, class_name="h-72", children=[
    ScatterChart(children=[
        XAxis(data_key="x", tick_line=False, axis_line=False),
        YAxis(data_key="y", tick_line=False, axis_line=False),
        ChartTooltip(content=ChartTooltipContent()),
        Scatter(data=data, fill="hsl(var(--chart-2))"),
    ]),
])
```
"""

REFERENCE = """
---

## Component Reference

### RadarChart Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict]` | *(required)* | Array of data objects |
| `cx` | `str \\| int` | `"50%"` | X centre position |
| `cy` | `str \\| int` | `"50%"` | Y centre position |
| `outer_radius` | `int \\| str` | `"80%"` | Outer radius |
| `start_angle` | `int` | `90` | Angle for the first axis |
| `end_angle` | `int` | `-270` | Angle sweep direction |

### Radar Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str` | *(required)* | Key from data |
| `fill` | `str` | `"hsl(var(--chart-1))"` | Fill color |
| `fill_opacity` | `float` | `0.6` | Fill opacity |
| `stroke` | `str \\| None` | *(same as fill)* | Stroke color |
| `stroke_width` | `int` | `2` | Stroke width |

### RadialBarChart Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict]` | *(required)* | Array of data objects |
| `inner_radius` | `int \\| str` | `"10%"` | Inner radius |
| `outer_radius` | `int \\| str` | `"80%"` | Outer radius |
| `bar_size` | `int \\| None` | `None` | Fixed bar thickness |
| `start_angle` | `int` | `90` | Start angle |
| `end_angle` | `int` | `-270` | End angle |

### RadialBar Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str` | *(required)* | Key for values |
| `background` | `bool \\| dict` | `False` | Show background track arc |
| `corner_radius` | `int \\| str \\| None` | `None` | Rounded bar ends |
| `min_angle` | `int` | `0` | Minimum arc angle for zero values |
| `label` | `bool \\| dict \\| None` | `None` | Value labels |
| `fill` | `str` | `"hsl(var(--chart-1))"` | Default fill (overridden by `Cell`) |

### ScatterChart Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict] \\| None` | `None` | Chart-level data (can also be set on `Scatter`) |
| `margin` | `dict` | `{top:20, right:20, left:20, bottom:20}` | Chart margins |
| `children` | `list` | `[]` | Axes, scatter series, tooltip |

### Scatter Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict] \\| None` | `None` | Series-level data points |
| `fill` | `str` | `"hsl(var(--chart-1))"` | Point fill color |
| `shape` | `str` | `"circle"` | Point shape: `"circle"`, `"cross"`, `"diamond"`, `"square"`, `"star"`, `"triangle"`, `"wye"` |
| `name` | `str \\| None` | `None` | Label for tooltip / legend |
| `line` | `bool \\| dict` | `False` | Connect points with a line |

### Other Available Chart Types

| Component | Notes |
|-----------|-------|
| `ComposedChart` + `Bar`, `Line`, `Area` | Mix multiple series types in one chart |
| `FunnelChart` + `Funnel` | Funnel / pipeline visualisation |
| `Treemap` | Hierarchical area-proportioned rectangles |
| `Sankey` | Flow diagrams between nodes |

> These chart types follow the same `ChartContainer` + `ChartConfig` wrapping pattern.
> Refer to the Recharts documentation for their full set of props.
"""
