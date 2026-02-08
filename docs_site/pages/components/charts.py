"""Charts — /docs/components/charts."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Charts"
PAGE_ROUTE = "/docs/components/charts"


def render(ctx):
    """Render the charts reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Overview

Refast includes a full charting system built on Recharts. All charts are wrapped in
a `ChartContainer` with a `ChartConfig` that maps data keys to colors and labels.

## Chart Types

- **BarChart** — Vertical or horizontal bar charts
- **LineChart** — Line/trend charts
- **AreaChart** — Filled area charts
- **PieChart** — Pie/donut charts
- **RadarChart** — Radar/spider charts
- **RadialChart** — Radial bar charts
- **ScatterChart** — Scatter/point charts

## Basic Example

```python
from refast.components.shadcn.charts import (
    ChartContainer, ChartConfig, ChartColor,
    BarChart, Bar, ChartTooltip, ChartTooltipContent,
    XAxis, YAxis, CartesianGrid,
)

data = [
    {"month": "Jan", "sales": 100},
    {"month": "Feb", "sales": 150},
    {"month": "Mar", "sales": 200},
]

config = ChartConfig(colors={
    "sales": ChartColor(label="Sales", color="hsl(var(--primary))"),
})

ChartContainer(
    config=config,
    class_name="h-64 w-full",
    children=[
        BarChart(
            data=data,
            children=[
                CartesianGrid(stroke_dasharray="3 3"),
                XAxis(data_key="month"),
                YAxis(),
                ChartTooltip(content=ChartTooltipContent()),
                Bar(data_key="sales", fill="var(--color-sales)", radius=4),
            ],
        ),
    ],
)
```

## ChartConfig

Maps data keys to labels and colors:

```python
config = ChartConfig(colors={
    "revenue": ChartColor(label="Revenue", color="hsl(var(--chart-1))"),
    "expenses": ChartColor(label="Expenses", color="hsl(var(--chart-2))"),
})
```

## Sub-Components

| Component | Used In | Purpose |
|-----------|---------|---------|
| `Bar` | BarChart | A bar series |
| `Line` | LineChart | A line series |
| `Area` | AreaChart | An area series |
| `Pie` | PieChart | A pie series |
| `XAxis`, `YAxis` | Any cartesian | Axes |
| `CartesianGrid` | Any cartesian | Grid lines |
| `ChartTooltip` | Any | Hover tooltip |
| `ChartLegend` | Any | Color legend |
| `PolarGrid`, `PolarAngleAxis`, `PolarRadiusAxis` | Radar/Radial | Polar axes |

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements.*
"""
