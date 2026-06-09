"""Bar Chart — /docs/components/bar-chart."""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Separator,
    Text,
)
from refast.components.shadcn.charts import (
    Bar,
    BarChart,
    CartesianGrid,
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
    XAxis,
)

PAGE_TITLE = "Bar Chart"
PAGE_ROUTE = "/docs/components/bar-chart"

SAMPLE_DATA = [
    {"month": "January",  "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March",    "desktop": 237, "mobile": 120},
    {"month": "April",    "desktop": 73,  "mobile": 190},
    {"month": "May",      "desktop": 209, "mobile": 130},
    {"month": "June",     "desktop": 214, "mobile": 140},
]

# ── Playground callbacks ──────────────────────────────────────────────────


async def _bc_set_show_grid(ctx: Context, value: bool):
    ctx.state.set("bc_grid", value)
    await ctx.refresh()


async def _bc_set_show_legend(ctx: Context, value: bool):
    ctx.state.set("bc_legend", value)
    await ctx.refresh()


async def _bc_set_stacked(ctx: Context, value: bool):
    ctx.state.set("bc_stacked", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    show_grid   = ctx.state.get("bc_grid",    True)
    show_legend = ctx.state.get("bc_legend",  True)
    stacked     = ctx.state.get("bc_stacked", False)
    stack_id    = "a" if stacked else None

    chart_children = []
    if show_grid:
        chart_children.append(CartesianGrid(vertical=False))
    chart_children.append(XAxis(data_key="month", tick_line=False, axis_line=False))
    chart_children.append(ChartTooltip(content=ChartTooltipContent()))
    if show_legend:
        chart_children.append(ChartLegend(content=ChartLegendContent()))
    chart_children.append(Bar(data_key="desktop", label="Desktop", radius=4, stack_id=stack_id))
    chart_children.append(Bar(data_key="mobile",  label="Mobile",  radius=4, stack_id=stack_id))

    return playground_card(
        options=[
            Column(gap=1, children=[
                Text("Show grid", class_name="text-sm font-medium"),
                Checkbox(label="grid", checked=show_grid, on_change=ctx.callback(_bc_set_show_grid)),
            ]),
            Column(gap=1, children=[
                Text("Show legend", class_name="text-sm font-medium"),
                Checkbox(label="legend", checked=show_legend, on_change=ctx.callback(_bc_set_show_legend)),
            ]),
            Column(gap=1, children=[
                Text("Stacked", class_name="text-sm font-medium"),
                Checkbox(label="stacked", checked=stacked, on_change=ctx.callback(_bc_set_stacked)),
            ]),
        ],
        preview=[
            ChartContainer(
                class_name="h-64",
                children=[
                    BarChart(
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
Bar charts display data using rectangular bars proportional to the values they represent.
They are ideal for comparing values across categories.

```python
from refast.components.shadcn.charts import (
    ChartContainer, BarChart, Bar,
    CartesianGrid, XAxis, ChartTooltip, ChartTooltipContent,
)

data = [
    {"month": "January",  "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March",    "desktop": 237, "mobile": 120},
]

ChartContainer(class_name="h-64", children=[
    BarChart(data=data, children=[
        CartesianGrid(vertical=False),
        XAxis(data_key="month", tick_line=False, axis_line=False),
        ChartTooltip(content=ChartTooltipContent()),
        Bar(data_key="desktop", label="Desktop", radius=4),
        Bar(data_key="mobile",  label="Mobile",  radius=4),
    ]),
])
```
"""

REFERENCE = """
## ChartContainer Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `config` | `dict[str, ChartConfig] \\| None` | `None` | Optional override map; auto-built from series children when omitted |
| `class_name` | `str` | `""` | Container class; set height here (e.g. `"h-64"`) |
| `children` | `list` | `[]` | The chart component(s) |
| `min_height` | `int \\| str \\| None` | `200` | Minimum height |
| `aspect` | `float \\| None` | `None` | Aspect ratio (width / height) |

## ChartConfig Fields

| Field | Type | Description |
|-------|------|-------------|
| `label` | `str` | Human-readable series label |
| `color` | `str \\| None` | CSS color value (e.g. `hsl(var(--chart-1))`) |
| `icon` | `str \\| None` | Lucide icon name for the legend |

## BarChart Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict]` | *(required)* | Array of data objects |
| `layout` | `"horizontal" \\| "vertical"` | `"horizontal"` | Chart orientation |
| `margin` | `dict` | `{top:10, right:10, left:10, bottom:0}` | Chart margins |
| `bar_category_gap` | `str \\| int \\| None` | `None` | Gap between bar categories |
| `bar_gap` | `str \\| int \\| None` | `None` | Gap between bars in the same group |
| `max_bar_size` | `int \\| None` | `None` | Maximum bar width |
| `stack_offset` | `str` | `"none"` | `"expand"`, `"none"`, `"wiggle"`, `"silhouette"` |
| `on_click` | `Callback \\| None` | `None` | Click on a bar |
| `children` | `list` | `[]` | Axes, bars, tooltip, legend |

## Bar Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data_key` | `str` | *(required)* | Key from data objects |
| `fill` | `str` | *(auto from `data_key`)* | CSS color; defaults to `var(--color-{data_key})` |
| `radius` | `int \\| list[int]` | `0` | Corner radius |
| `stack_id` | `str \\| None` | `None` | Bars sharing the same `stack_id` are stacked |
| `bar_size` | `int \\| None` | `None` | Fixed bar width in pixels |
| `min_point_size` | `int \\| None` | `None` | Minimum bar height for zero values |
| `label` | `str \\| None` | `None` | Human-readable series label shown in tooltip/legend |
| `bar_label` | `bool \\| dict \\| None` | `None` | Show value labels on bars |
| `background` | `bool \\| dict` | `False` | Show background bar |
| `hide` | `bool` | `False` | Hide this bar series |
"""
