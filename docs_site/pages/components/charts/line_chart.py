"""Line Chart — /docs/components/line-chart."""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Select,
    Separator,
    Text,
)
from refast.components.shadcn.charts import (
    CartesianGrid,
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
    Line,
    LineChart,
    XAxis,
    YAxis,
)

PAGE_TITLE = "Line Chart"
PAGE_ROUTE = "/docs/components/line-chart"

SAMPLE_DATA = [
    {"month": "January",  "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March",    "desktop": 237, "mobile": 120},
    {"month": "April",    "desktop": 73,  "mobile": 190},
    {"month": "May",      "desktop": 209, "mobile": 130},
    {"month": "June",     "desktop": 214, "mobile": 140},
]

STROKE_OPTIONS = [
    {"value": "monotone", "label": "Monotone"},
    {"value": "linear",   "label": "Linear"},
    {"value": "step",     "label": "Step"},
]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _lc_set_show_dots(ctx: Context, value: bool):
    ctx.state.set("lc_dots", value)
    await ctx.refresh()


async def _lc_set_stroke_type(ctx: Context, value: str):
    ctx.state.set("lc_type", value)
    await ctx.refresh()


async def _lc_set_show_grid(ctx: Context, value: bool):
    ctx.state.set("lc_grid", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    show_dots   = ctx.state.get("lc_dots", True)
    stroke_type = ctx.state.get("lc_type", "monotone")
    show_grid   = ctx.state.get("lc_grid", True)

    chart_children = []
    if show_grid:
        chart_children.append(CartesianGrid(vertical=False))
    chart_children.append(XAxis(data_key="month", tick_line=False, axis_line=False))
    chart_children.append(YAxis(tick_line=False, axis_line=False))
    chart_children.append(ChartTooltip(content=ChartTooltipContent()))
    chart_children.append(ChartLegend(content=ChartLegendContent()))
    chart_children.append(
        Line(
            data_key="desktop",
            label="Desktop",
            stroke_width=2,
            dot=show_dots,
            type=stroke_type,
        )
    )
    chart_children.append(
        Line(
            data_key="mobile",
            label="Mobile",
            stroke_width=2,
            dot=show_dots,
            type=stroke_type,
        )
    )

    return playground_card(
        options=[
            Column(gap=1, children=[
                Text("Show dots", class_name="text-sm font-medium"),
                Checkbox(label="dots", checked=show_dots, on_change=ctx.callback(_lc_set_show_dots)),
            ]),
            Column(gap=1, children=[
                Text("Stroke type", class_name="text-sm font-medium"),
                Select(
                    options=STROKE_OPTIONS,
                    value=stroke_type,
                    on_change=ctx.callback(_lc_set_stroke_type),
                ),
            ]),
            Column(gap=1, children=[
                Text("Show grid", class_name="text-sm font-medium"),
                Checkbox(label="grid", checked=show_grid, on_change=ctx.callback(_lc_set_show_grid)),
            ]),
        ],
        preview=[
            ChartContainer(
                class_name="h-64",
                children=[
                    LineChart(
                        data=SAMPLE_DATA,
                        children=chart_children,
                    ),
                ],
            ),
        ],
        preview_class="",
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
Line charts visualise trends over time or ordered categories by connecting data points
with a continuous line.

```python
from refast.components.shadcn.charts import (
    ChartContainer, LineChart, Line,
    CartesianGrid, XAxis, YAxis,
    ChartTooltip, ChartTooltipContent,
    ChartLegend, ChartLegendContent,
)

data = [
    {"month": "January",  "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March",    "desktop": 237, "mobile": 120},
]

ChartContainer(class_name="h-64", children=[
    LineChart(data=data, children=[
        CartesianGrid(vertical=False),
        XAxis(data_key="month", tick_line=False, axis_line=False),
        YAxis(tick_line=False, axis_line=False),
        ChartTooltip(content=ChartTooltipContent()),
        ChartLegend(content=ChartLegendContent()),
        Line(data_key="desktop", label="Desktop", type="monotone"),
        Line(data_key="mobile",  label="Mobile",  type="monotone"),
    ]),
])
```
"""

REFERENCE = """
## LineChart Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict]` | *(required)* | Array of data objects |
| `layout` | `"horizontal" \\| "vertical"` | `"horizontal"` | Chart orientation |
| `margin` | `dict` | `{top:10, right:10, left:10, bottom:0}` | Chart margins |
| `sync_id` | `str \\| None` | `None` | Sync multiple charts by the same ID |
| `on_click` | `Callback \\| None` | `None` | Click on the chart area |
| `children` | `list` | `[]` | Axes, lines, tooltip, legend |

## Line Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str` | *(required)* | Key from data objects |
| `type` | `str` | `"natural"` | Interpolation: `"linear"`, `"monotone"`, `"step"`, `"natural"`, `"basis"` |
| `stroke` | `str` | *(auto from `data_key`)* | Line color; defaults to `var(--color-{data_key})` |
| `stroke_width` | `int` | `2` | Line thickness in pixels |
| `dot` | `bool \\| dict` | `True` | Show data-point dots; pass a dict for custom dot styling |
| `active_dot` | `bool \\| dict` | `True` | Dot shown on hover |
| `connect_nulls` | `bool` | `False` | Draw a line through `null` values |
| `stroke_dasharray` | `str \\| None` | `None` | SVG dash pattern e.g. `"5 5"` for dashed lines |
| `label` | `str \\| None` | `None` | Human-readable series label shown in tooltip/legend |
| `line_label` | `bool \\| dict \\| None` | `None` | Show value labels at each data point |
| `hide` | `bool` | `False` | Hide this line series |

## XAxis / YAxis Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str \\| None` | `None` | Key for axis values |
| `tick_line` | `bool` | `True` | Show tick mark lines |
| `axis_line` | `bool` | `True` | Show the axis baseline |

## CartesianGrid Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `stroke_dasharray` | `str` | `"3 3"` | SVG dash pattern for grid lines |
| `horizontal` | `bool` | `True` | Show horizontal grid lines |
| `vertical` | `bool` | `True` | Show vertical grid lines |
"""
