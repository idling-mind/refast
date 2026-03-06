"""Charts — /docs/components/charts."""

from refast.components import Container, Heading, Separator

from ..utils import render_markdown_with_demo_apps

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
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
## Overview

Refast includes a full charting system built on [Recharts](https://recharts.org/).
All charts are wrapped in a `ChartContainer` with a `ChartConfig` that maps data
keys to display labels and colors.

## Chart Types

| Chart | Component | Type |
|-------|-----------|------|
| Bar | `BarChart` + `Bar` | Cartesian |
| Line | `LineChart` + `Line` | Cartesian |
| Area | `AreaChart` + `Area` | Cartesian |
| Pie / Donut | `PieChart` + `Pie` | Radial |
| Radar | `RadarChart` + `Radar` | Polar |
| Radial Bar | `RadialBarChart` + `RadialBar` | Radial |
| Scatter | `ScatterChart` + `Scatter` | Cartesian |
| Composed | `ComposedChart` | Cartesian |
| Funnel | `FunnelChart` + `Funnel` | Flow |
| Treemap | `Treemap` (standalone) | Hierarchy |
| Sankey | `Sankey` (standalone) | Flow |

---

## Quick Start: Bar Chart

```python
from refast.components.shadcn.charts import (
    ChartContainer, ChartConfig,
    BarChart, Bar,
    ChartTooltip, ChartTooltipContent,
    XAxis, CartesianGrid,
)

data = [
    {"month": "Jan", "sales": 100},
    {"month": "Feb", "sales": 150},
    {"month": "Mar", "sales": 200},
]

config = {
    "sales": ChartConfig(label="Sales", color="hsl(var(--chart-1))"),
}

ChartContainer(
    config=config,
    class_name="h-64 w-full",
    children=[
        BarChart(
            data=data,
            children=[
                CartesianGrid(stroke_dasharray="3 3"),
                XAxis(data_key="month"),
                ChartTooltip(content=ChartTooltipContent()),
                Bar(data_key="sales", fill="var(--color-sales)", radius=4),
            ],
        ),
    ],
)
```

---

## ChartContainer

Responsive wrapper that provides theming context and sizing.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `config` | `dict[str, ChartConfig]` | `{}` | Map of data key → `ChartConfig` |
| `class_name` | `str` | `""` | CSS classes (e.g., `"h-64 w-full"`) |
| `width` | `str \| int` | `"100%"` | Container width |
| `height` | `str \| int` | `"100%"` | Container height |
| `min_height` | `str \| int \| None` | `200` | Minimum height |
| `aspect` | `float \| None` | `None` | Aspect ratio (width/height) |
| `on_resize` | `Callback \| None` | `None` | Fired when container is resized |

## ChartConfig (Pydantic model)

```python
ChartConfig(label="Revenue", color="hsl(var(--chart-1))")
```

| Field | Type | Description |
|-------|------|-------------|
| `label` | `str` | Human-readable series label |
| `color` | `str \| None` | CSS color value |
| `icon` | `str \| None` | Lucide icon name for the legend |

---

## Common Chart Props

All chart components (`BarChart`, `LineChart`, etc.) accept:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict]` | *(required)* | Array of data records |
| `layout` | `"horizontal" \| "vertical"` | `"horizontal"` | Chart orientation |
| `margin` | `dict[str, int] \| None` | `{top:10, right:10, left:10, bottom:0}` | Chart margins |
| `on_click` | `Callback \| None` | `None` | Click on chart element |
| `on_mouse_enter` | `Callback \| None` | `None` | Hover enter |
| `on_mouse_leave` | `Callback \| None` | `None` | Hover leave |

---

## Series Components

### Bar

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str` | *(required)* | Key in the data records for this series |
| `fill` | `str \| None` | `None` | Bar fill colour (use `var(--color-<key>)`) |
| `radius` | `int \| list[int]` | `0` | Border radius |
| `stack_id` | `str \| None` | `None` | Stack identifier for stacked bars |

### Line

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str` | *(required)* | Key in the data records |
| `stroke` | `str \| None` | `None` | Line colour |
| `stroke_width` | `int` | `2` | Line thickness |
| `dot` | `bool` | `True` | Show data-point dots |
| `type` | `"linear" \| "monotone" \| "step"` | `"linear"` | Interpolation |

### Area

Same as `Line`, plus:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `fill` | `str \| None` | `None` | Area fill colour |
| `fill_opacity` | `float` | `0.4` | Fill opacity |

### Pie

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str` | *(required)* | Key for values |
| `name_key` | `str` | `"name"` | Key for slice labels |
| `inner_radius` | `int \| str` | `0` | Inner radius (set > 0 for donut) |
| `outer_radius` | `int \| str` | `"80%"` | Outer radius |
| `on_click` | `Callback \| None` | `None` | Click a slice |

---

## Axes & Grid

### XAxis / YAxis

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str \| None` | `None` | Key for axis values |
| `tick_line` | `bool` | `True` | Show tick lines |
| `axis_line` | `bool` | `True` | Show axis line |

### CartesianGrid

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `stroke_dasharray` | `str` | `"3 3"` | SVG dash pattern |
| `horizontal` | `bool` | `True` | Show horizontal lines |
| `vertical` | `bool` | `True` | Show vertical lines |

---

## Tooltip & Legend

### ChartTooltip

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `ChartTooltipContent \| None` | `None` | Custom content component |
| `cursor` | `bool` | `True` | Show cursor highlight |

### ChartTooltipContent

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `indicator` | `"line" \| "dot" \| "dashed"` | `"dot"` | Style of series indicator |
| `name_key` | `str \| None` | `None` | Override key for series name |
| `label_key` | `str \| None` | `None` | Override key for x-axis label |

### ChartLegend / ChartLegendContent

```python
ChartLegend(content=ChartLegendContent())
```

Placed as a child of the chart component; renders the colour/label legend.
"""
