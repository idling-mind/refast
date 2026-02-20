"""Lazy Loading Example — Refast Bundle Optimization.

This example demonstrates the ``features`` parameter on ``RefastApp``
which controls which heavy frontend chunks are downloaded by the browser.

Run the three apps side-by-side to compare load behaviour:

    # All features (default) — every chunk is loaded
    uvicorn examples.lazy_loading.app:app_all --port 8001

    # Charts only — only the charts chunk is loaded
    uvicorn examples.lazy_loading.app:app_charts --port 8002

    # Minimal — no feature chunks, core UI only
    uvicorn examples.lazy_loading.app:app_minimal --port 8003

Open the browser devtools **Network** tab to observe the difference
in the number and size of JS files loaded on each page.
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Code,
    Column,
    Container,
    Heading,
    Paragraph,
    Row,
    Separator,
    Text,
)
from refast.components.shadcn.charts import (
    Bar,
    BarChart,
    CartesianGrid,
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
    XAxis,
    YAxis,
)


# ──────────────────────────────────────────────────────────────────────────
# Shared page builders
# ──────────────────────────────────────────────────────────────────────────


def _info_section(mode: str, features: list[str] | None):
    """Build a card explaining the current mode."""
    if features is None:
        badge_text = "All Features"
        badge_variant = "default"
        description = (
            "Every lazy chunk is loaded — charts, icons, navigation, overlay, controls, markdown."
        )
    elif features == []:
        badge_text = "Minimal"
        badge_variant = "secondary"
        description = "No feature chunks. Only the core UI components (buttons, cards, inputs, etc.) are loaded."
    else:
        badge_text = ", ".join(features)
        badge_variant = "outline"
        description = f"Only the following feature chunks are loaded: {', '.join(features)}."

    return Card(
        class_name="mb-6",
        children=[
            CardHeader(
                children=[
                    Row(
                        align="center",
                        gap=3,
                        children=[
                            CardTitle(f"Lazy Loading Demo — {mode}"),
                            Badge(badge_text, variant=badge_variant),
                        ],
                    ),
                    CardDescription(description),
                ],
            ),
            CardContent(
                children=[
                    Column(
                        gap=2,
                        children=[
                            Paragraph(
                                "Open your browser's DevTools → Network tab to see "
                                "which JS chunks are requested."
                            ),
                            Paragraph(
                                "The core entry file (refast-client.js) is always loaded. "
                                "Feature chunks like refast-charts-*.js are loaded on demand."
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _chart_section():
    """Build a sample chart section to showcase the charts feature chunk."""
    chart_config = ChartConfig(
        revenue={"label": "Revenue", "color": "hsl(var(--chart-1))"},
        profit={"label": "Profit", "color": "hsl(var(--chart-2))"},
    )

    chart_data = [
        {"month": "Jan", "revenue": 4000, "profit": 2400},
        {"month": "Feb", "revenue": 3000, "profit": 1398},
        {"month": "Mar", "revenue": 2000, "profit": 4800},
        {"month": "Apr", "revenue": 2780, "profit": 3908},
        {"month": "May", "revenue": 1890, "profit": 4800},
        {"month": "Jun", "revenue": 2390, "profit": 3800},
    ]

    return Card(
        class_name="mb-6",
        children=[
            CardHeader(
                children=[
                    CardTitle("Sample Chart"),
                    CardDescription(
                        "This section triggers the charts chunk (recharts + wrappers)."
                    ),
                ],
            ),
            CardContent(
                children=[
                    ChartContainer(
                        config=chart_config,
                        class_name="h-64 w-full",
                        children=[
                            BarChart(
                                data=chart_data,
                                children=[
                                    CartesianGrid(stroke_dasharray="3 3"),
                                    XAxis(data_key="month"),
                                    YAxis(),
                                    ChartTooltip(
                                        content=ChartTooltipContent(),
                                    ),
                                    Bar(
                                        data_key="revenue",
                                        fill="var(--color-revenue)",
                                        radius=4,
                                    ),
                                    Bar(
                                        data_key="profit",
                                        fill="var(--color-profit)",
                                        radius=4,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _core_section():
    """Build a section using only core (always-loaded) components."""
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Core Components"),
                    CardDescription("These are always available — no extra chunk needed."),
                ],
            ),
            CardContent(
                children=[
                    Column(
                        gap=4,
                        children=[
                            Row(
                                gap=2,
                                children=[
                                    Button("Primary", variant="primary"),
                                    Button("Secondary", variant="secondary"),
                                    Button("Outline", variant="outline"),
                                    Button("Ghost", variant="ghost"),
                                ],
                            ),
                            Separator(),
                            Heading("Typography", level=3),
                            Paragraph(
                                "Paragraphs, headings, and inline code are part of the core bundle."
                            ),
                            Code("const features = ['charts'];"),
                        ],
                    ),
                ],
            ),
        ],
    )


# ══════════════════════════════════════════════════════════════════════════
# App 1: All features (default)
# ══════════════════════════════════════════════════════════════════════════

ui_all = RefastApp(title="Lazy Loading — All Features")


@ui_all.page("/")
def home_all(ctx: Context):
    return Container(
        class_name="max-w-3xl mx-auto py-10 px-4",
        children=[
            _info_section("All Features", None),
            _chart_section(),
            _core_section(),
        ],
    )


app_all = FastAPI(title="Lazy Loading — All")
app_all.include_router(ui_all.router)


# ══════════════════════════════════════════════════════════════════════════
# App 2: Charts only
# ══════════════════════════════════════════════════════════════════════════

ui_charts = RefastApp(title="Lazy Loading — Charts Only", features=["charts"])


@ui_charts.page("/")
def home_charts(ctx: Context):
    return Container(
        class_name="max-w-3xl mx-auto py-10 px-4",
        children=[
            _info_section("Charts Only", ["charts"]),
            _chart_section(),
            _core_section(),
        ],
    )


app_charts = FastAPI(title="Lazy Loading — Charts")
app_charts.include_router(ui_charts.router)


# ══════════════════════════════════════════════════════════════════════════
# App 3: Minimal (no feature chunks)
# ══════════════════════════════════════════════════════════════════════════

ui_minimal = RefastApp(title="Lazy Loading — Minimal", features=[])


@ui_minimal.page("/")
def home_minimal(ctx: Context):
    return Container(
        class_name="max-w-3xl mx-auto py-10 px-4",
        children=[
            _info_section("Minimal", []),
            _core_section(),
        ],
    )


app_minimal = FastAPI(title="Lazy Loading — Minimal")
app_minimal.include_router(ui_minimal.router)


# ══════════════════════════════════════════════════════════════════════════
# Default app (all features) — used by `uvicorn examples.lazy_loading.app:app`
# ══════════════════════════════════════════════════════════════════════════

app = app_all


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("examples.lazy_loading.app:app", host="0.0.0.0", port=8000, reload=True)
