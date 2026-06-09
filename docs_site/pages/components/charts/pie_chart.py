"""Pie Chart — /docs/components/pie-chart."""

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
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
    Pie,
    PieChart,
)

PAGE_TITLE = "Pie Chart"
PAGE_ROUTE = "/docs/components/pie-chart"

BROWSER_DATA = [
    {"name": "Chrome",  "visitors": 275},
    {"name": "Firefox", "visitors": 200},
    {"name": "Safari",  "visitors": 187},
    {"name": "Edge",    "visitors": 173},
    {"name": "Other",   "visitors": 90},
]

INNER_RADIUS_OPTIONS = [
    {"value": "pie",   "label": "Pie (0)"},
    {"value": "donut", "label": "Donut (60)"},
]

_INNER_RADIUS_MAP = {"pie": 0, "donut": 60}


# ── Playground callbacks ──────────────────────────────────────────────────


async def _pc_set_inner_radius(ctx: Context, value: str):
    ctx.state.set("pc_inner_radius", value)
    await ctx.refresh()


async def _pc_set_show_labels(ctx: Context, value: bool):
    ctx.state.set("pc_labels", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    inner_radius_key = ctx.state.get("pc_inner_radius", "donut")
    show_labels      = ctx.state.get("pc_labels",       True)
    inner_radius     = _INNER_RADIUS_MAP[inner_radius_key]

    pie = Pie(
        data=BROWSER_DATA,
        data_key="visitors",
        name_key="name",
        inner_radius=inner_radius,
        outer_radius="80%",
        label=show_labels,
        padding_angle=2,
    )

    return playground_card(
        options=[
            Column(gap=1, children=[
                Text("Chart style", class_name="text-sm font-medium"),
                Select(
                    options=INNER_RADIUS_OPTIONS,
                    value=inner_radius_key,
                    on_change=ctx.callback(_pc_set_inner_radius),
                ),
            ]),
            Column(gap=1, children=[
                Text("Show labels", class_name="text-sm font-medium"),
                Checkbox(label="labels", checked=show_labels, on_change=ctx.callback(_pc_set_show_labels)),
            ]),
        ],
        preview=[
            ChartContainer(
                class_name="h-72",
                children=[
                    PieChart(
                        children=[
                            pie,
                            ChartTooltip(content=ChartTooltipContent()),
                            ChartLegend(content=ChartLegendContent()),
                        ],
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
Pie charts show part-to-whole relationships. Setting `inner_radius > 0` creates a
**donut chart**, which is often easier to read when comparing slices.

```python
from refast.components.shadcn.charts import (
    ChartContainer, PieChart, Pie,
    ChartTooltip, ChartTooltipContent,
    ChartLegend, ChartLegendContent,
)

data = [
    {"name": "Chrome",  "visitors": 275},
    {"name": "Firefox", "visitors": 200},
    {"name": "Safari",  "visitors": 187},
]

# Slice colors are auto-assigned by index (hsl(var(--chart-1)), --chart-2, ...)
ChartContainer(class_name="h-72", children=[
    PieChart(children=[
        Pie(
            data=data,
            data_key="visitors",
            name_key="name",
            inner_radius=60,   # 0 = pie, >0 = donut
            outer_radius="80%",
            padding_angle=2,
        ),
        ChartTooltip(content=ChartTooltipContent()),
        ChartLegend(content=ChartLegendContent()),
    ]),
])
```

> **Tip:** For custom per-slice colors, add a `"fill"` key to each data item
> (e.g. `{"name": "Chrome", "visitors": 275, "fill": "hsl(var(--chart-1))"}`).
> You can also use `Cell` children for fine-grained control.
"""

REFERENCE = """
## PieChart Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `Pie` components plus optional tooltip and legend |
| `margin` | `dict` | `{top:0, right:0, left:0, bottom:0}` | Chart margins |
| `on_click` | `Callback \\| None` | `None` | Click on the chart area |

## Pie Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | `list[dict]` | *(required)* | Array of data objects |
| `data_key` | `str` | *(required)* | Key holding the numeric value for each slice |
| `name_key` | `str` | *(required)* | Key holding the label for each slice |
| `inner_radius` | `int \\| str` | `0` | Inner radius; set > 0 for a donut chart |
| `outer_radius` | `int \\| str` | `"80%"` | Outer radius |
| `cx` | `str \\| int` | `"50%"` | X position of the centre |
| `cy` | `str \\| int` | `"50%"` | Y position of the centre |
| `padding_angle` | `int` | `0` | Gap between slices (degrees) |
| `corner_radius` | `int \\| str \\| None` | `None` | Rounded slice corners |
| `start_angle` | `int` | `0` | Start angle (degrees) |
| `end_angle` | `int` | `360` | End angle (degrees) |
| `label` | `bool \\| None` | `None` | Show percentage/value labels on slices |
| `label_line` | `bool \\| dict \\| None` | `None` | Leader lines from slices to labels |
| `min_angle` | `int` | `0` | Minimum sector angle so tiny slices are still visible |
| `children` | `list` | `[]` | `Cell` components for per-slice styling |

## Cell Props

Use `Cell` inside a `Pie` to set individual slice colours:

```python
Cell(extra_props={"fill": "hsl(var(--chart-1))"})
```

| Prop | Type | Description |
|------|------|-------------|
| `extra_props` | `dict` | Pass `fill` (and optionally `stroke`) for per-slice styling |
"""
