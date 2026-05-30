"""Analytics Dashboard – Clean, modern analytics dashboard example.

Demonstrates:
- KPI metric cards with sparkline charts
- Revenue overview area chart
- Traffic sources donut (pie) chart
- Monthly orders bar chart
- Recent transactions DataTable with sorting & filtering
- Top products summary table
- Header with theme switcher and refresh action
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Avatar,
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    DataTable,
    Heading,
    Icon,
    Paragraph,
    Row,
    Separator,
    Text,
    ThemeSwitcher,
)
from refast.components.shadcn.charts import (
    Area,
    AreaChart,
    Bar,
    BarChart,
    CartesianGrid,
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
    Line,
    LineChart,
    Pie,
    PieChart,
    XAxis,
    YAxis,
)

ui = RefastApp("Analytics Dashboard", preloaded_features=["charts"])

# ── Static data ───────────────────────────────────────────────────────────────

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

_REVENUE_DATA = [
    {"month": m, "revenue": rev, "expenses": exp}
    for m, rev, exp in zip(
        _MONTHS,
        [42000, 47000, 51000, 48000, 55000, 62000, 58000, 67000, 71000, 75000, 80000, 88000],
        [28000, 30000, 32000, 29000, 35000, 38000, 36000, 40000, 42000, 44000, 48000, 52000],
    )
]

_TRAFFIC_DATA = [
    {"source": "Organic",  "visitors": 4200, "fill": "hsl(var(--chart-1))"},
    {"source": "Direct",   "visitors": 2800, "fill": "hsl(var(--chart-2))"},
    {"source": "Referral", "visitors": 1900, "fill": "hsl(var(--chart-3))"},
    {"source": "Social",   "visitors": 1400, "fill": "hsl(var(--chart-4))"},
    {"source": "Email",    "visitors":  900, "fill": "hsl(var(--chart-5))"},
]

_ORDERS_DATA = [
    {"month": m, "orders": o}
    for m, o in zip(_MONTHS[-6:], [310, 280, 350, 390, 420, 380])
]

_TRANSACTIONS = [
    {"id": "#TXN-001", "customer": "Alice Johnson",  "product": "Enterprise",    "amount": "$999", "status": "completed", "date": "2026-05-28"},
    {"id": "#TXN-002", "customer": "Bob Smith",      "product": "Pro Plan",      "amount": "$299", "status": "completed", "date": "2026-05-28"},
    {"id": "#TXN-003", "customer": "Carol White",    "product": "Starter Plan",  "amount": "$49",  "status": "pending",   "date": "2026-05-27"},
    {"id": "#TXN-004", "customer": "David Brown",    "product": "Enterprise",    "amount": "$999", "status": "completed", "date": "2026-05-27"},
    {"id": "#TXN-005", "customer": "Eve Davis",      "product": "Starter Plan",  "amount": "$49",  "status": "failed",    "date": "2026-05-26"},
    {"id": "#TXN-006", "customer": "Frank Miller",   "product": "Pro Plan",      "amount": "$299", "status": "completed", "date": "2026-05-26"},
    {"id": "#TXN-007", "customer": "Grace Wilson",   "product": "Enterprise",    "amount": "$999", "status": "pending",   "date": "2026-05-25"},
    {"id": "#TXN-008", "customer": "Henry Moore",    "product": "Pro Plan",      "amount": "$299", "status": "completed", "date": "2026-05-25"},
    {"id": "#TXN-009", "customer": "Iris Chen",      "product": "Starter Plan",  "amount": "$49",  "status": "completed", "date": "2026-05-24"},
    {"id": "#TXN-010", "customer": "Jack Turner",    "product": "Add-on: API",   "amount": "$50",  "status": "completed", "date": "2026-05-24"},
]

_TOP_PRODUCTS = [
    {"name": "Enterprise Plan",    "units": 142, "revenue": "$141,858", "change": "+18%", "trend": "up"},
    {"name": "Pro Plan",           "units": 384, "revenue": "$114,816", "change": "+12%", "trend": "up"},
    {"name": "Starter Plan",       "units": 812, "revenue": "$39,788",  "change": "+7%",  "trend": "up"},
    {"name": "Add-on: API Access", "units": 267, "revenue": "$13,350",  "change": "+24%", "trend": "up"},
    {"name": "Add-on: Analytics",  "units": 198, "revenue": "$9,900",   "change": "-5%",  "trend": "down"},
]

_PRODUCT_TRENDS = {
    "Enterprise Plan":    [85,  92,  88,  95,  110, 125, 118, 130, 142],
    "Pro Plan":           [200, 220, 210, 240, 260, 280, 300, 360, 384],
    "Starter Plan":       [620, 640, 660, 680, 700, 720, 750, 780, 812],
    "Add-on: API Access": [80,  90,  110, 130, 150, 180, 210, 240, 267],
    "Add-on: Analytics":  [230, 225, 215, 210, 205, 200, 198, 196, 198],
}

_KPI = [
    {
        "title": "Total Revenue",
        "value": "$124,592",
        "change": 12.5,
        "trend": "up",
        "sparkline_id": "spark-revenue",
        "sparkline": [420, 470, 510, 480, 550, 620, 580, 670, 710, 750, 800, 880],
    },
    {
        "title": "Active Users",
        "value": "2,845",
        "change": 8.2,
        "trend": "up",
        "sparkline_id": "spark-users",
        "sparkline": [180, 220, 200, 240, 260, 230, 280, 310, 290, 320, 350, 380],
    },
    {
        "title": "New Orders",
        "value": "1,234",
        "change": 3.1,
        "trend": "down",
        "sparkline_id": "spark-orders",
        "sparkline": [160, 140, 155, 130, 150, 135, 145, 125, 140, 120, 135, 115],
    },
    {
        "title": "Conversion Rate",
        "value": "3.24%",
        "change": 0.5,
        "trend": "up",
        "sparkline_id": "spark-conv",
        "sparkline": [2.8, 3.1, 2.9, 3.2, 3.0, 3.4, 3.1, 3.5, 3.2, 3.6, 3.3, 3.7],
    },
]


# ── Callbacks ─────────────────────────────────────────────────────────────────

async def refresh_data(ctx: Context):
    await ctx.show_toast("Dashboard refreshed", variant="success")
    await ctx.refresh()


# ── Cell component builders ──────────────────────────────────────────────────

def _status_badge(status: str):
    _variant = {"completed": "success", "pending": "warning", "failed": "destructive"}
    _icon = {"completed": "check-circle", "pending": "clock", "failed": "x-circle"}
    return Badge(
        children=[status.capitalize()],
        variant=_variant.get(status, "secondary"),
        icon=_icon.get(status),
        size="sm",
    )


def _customer_cell(name: str, txn_id: str):
    initials = "".join(p[0].upper() for p in name.split()[:2])
    return Row(
        gap=3,
        align="center",
        children=[
            Avatar(fallback=initials, alt=name, size="sm"),
            Column(
                gap=0,
                children=[
                    Text(name, class_name="text-sm font-medium leading-none"),
                    Text(txn_id, class_name="text-xs text-muted-foreground mt-0.5"),
                ],
            ),
        ],
    )


def _product_sparkline(name: str):
    values = _PRODUCT_TRENDS.get(name, [])
    data = [{"v": v} for v in values]
    return ChartContainer(
        min_height=40,
        max_height=40,
        children=LineChart(
            data=data,
            margin={"top": 4, "right": 4, "bottom": 4, "left": 4},
            children=[
                Line(
                    data_key="v",
                    type="monotone",
                    stroke_width=2,
                    dot=False,
                    is_animation_active=False,
                ),
            ],
        ),
    )


def _change_badge(change: str, trend: str):
    is_up = trend == "up"
    icon = "trending-up" if is_up else "trending-down"
    variant = "success" if is_up else "destructive"
    return Badge(children=[change], variant=variant, icon=icon, icon_position="left", size="sm")


# ── Component helpers ─────────────────────────────────────────────────────────

def _sparkline(sparkline_id: str, values: list[float]) -> ChartContainer:
    data = [{"v": v} for v in values]
    return ChartContainer(
        min_height=56,
        max_height=56,
        children=LineChart(
            data=data,
            margin={"top": 4, "right": 4, "bottom": 4, "left": 4},
            children=[
                Line(
                    data_key="v",
                    type="monotone",
                    stroke_width=2,
                    dot=False,
                    is_animation_active=False,
                    id=sparkline_id,
                ),
            ],
        ),
    )


def _kpi_card(kpi: dict) -> Card:
    is_up = kpi["trend"] == "up"
    trend_class = "text-emerald-600 dark:text-emerald-400" if is_up else "text-rose-600 dark:text-rose-400"
    trend_icon = "trending-up" if is_up else "trending-down"
    sign = "+" if is_up else "-"

    return Card(
        children=[
            CardContent(
                class_name="pt-5 pb-4",
                children=[
                    Column(
                        gap=2,
                        children=[
                            Row(
                                justify="between",
                                align="start",
                                children=[
                                    Column(
                                        gap=1,
                                        children=[
                                            Text(
                                                kpi["title"],
                                                class_name="text-sm font-medium text-muted-foreground",
                                            ),
                                            Text(
                                                kpi["value"],
                                                class_name="text-2xl font-bold tracking-tight",
                                            ),
                                        ],
                                    ),
                                    Row(
                                        gap=1,
                                        align="center",
                                        class_name=trend_class,
                                        children=[
                                            Icon(trend_icon, size=14),
                                            Text(
                                                f"{sign}{abs(kpi['change'])}%",
                                                class_name=f"text-xs font-semibold {trend_class}",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            _sparkline(kpi["sparkline_id"], kpi["sparkline"]),
                            Text(
                                "vs. last month",
                                class_name="text-xs text-muted-foreground",
                            ),
                        ],
                    )
                ],
            )
        ],
    )


def _revenue_chart() -> Card:
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Revenue Overview"),
                    CardDescription("Monthly revenue vs expenses – current year"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        min_height=300,
                        children=AreaChart(
                            id="revenue-chart",
                            data=_REVENUE_DATA,
                            margin={"top": 10, "right": 10, "left": 0, "bottom": 0},
                            children=[
                                CartesianGrid(vertical=False),
                                XAxis(
                                    data_key="month",
                                    tick_line=False,
                                    axis_line=False,
                                    tick_margin=8,
                                ),
                                YAxis(tick_line=False, axis_line=False),
                                ChartTooltip(content=ChartTooltipContent()),
                                ChartLegend(content=ChartLegendContent()),
                                Area(
                                    data_key="revenue",
                                    label="Revenue",
                                    type="natural",
                                    fill_opacity=0.25,
                                    stroke_width=2,
                                ),
                                Area(
                                    data_key="expenses",
                                    label="Expenses",
                                    type="natural",
                                    fill_opacity=0.25,
                                    stroke_width=2,
                                ),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _traffic_chart() -> Card:
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Traffic Sources"),
                    CardDescription("Visitor breakdown by acquisition channel"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        min_height=300,
                        children=PieChart(
                            children=[
                                Pie(
                                    id="traffic-pie",
                                    data=_TRAFFIC_DATA,
                                    data_key="visitors",
                                    name_key="source",
                                    inner_radius=70,
                                    label=False,
                                ),
                                ChartTooltip(content=ChartTooltipContent(hide_label=False)),
                                ChartLegend(content=ChartLegendContent()),
                            ]
                        ),
                    )
                ]
            ),
        ]
    )


def _orders_chart() -> Card:
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Monthly Orders"),
                    CardDescription("Order volume – last 6 months"),
                ]
            ),
            CardContent(
                children=[
                    ChartContainer(
                        min_height=260,
                        children=BarChart(
                            id="orders-bar",
                            data=_ORDERS_DATA,
                            children=[
                                CartesianGrid(vertical=False),
                                XAxis(
                                    data_key="month",
                                    tick_line=False,
                                    axis_line=False,
                                    tick_margin=8,
                                ),
                                ChartTooltip(content=ChartTooltipContent()),
                                Bar(data_key="orders", label="Orders", radius=4),
                            ],
                        ),
                    )
                ]
            ),
        ]
    )


def _transactions_table() -> Card:
    rows = [
        {
            "customer": _customer_cell(t["customer"], t["id"]),
            "product":  t["product"],
            "amount":   t["amount"],
            "status":   _status_badge(t["status"]),
            "date":     t["date"],
            # plain-text keywords so the filter input still works
            "keywords": [t["customer"], t["id"], t["product"], t["status"], t["date"]],
        }
        for t in _TRANSACTIONS
    ]
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Recent Transactions"),
                    CardDescription("Latest payment activity across all plans"),
                ]
            ),
            CardContent(
                children=[
                    DataTable(
                        columns=[
                            {"key": "customer", "header": "Customer"},
                            {"key": "product",  "header": "Product",  "sortable": True},
                            {"key": "amount",   "header": "Amount",   "align": "right", "width": "90px"},
                            {"key": "status",   "header": "Status",   "align": "center", "width": "120px"},
                            {"key": "date",     "header": "Date",     "sortable": True,  "width": "110px"},
                        ],
                        data=rows,
                        sortable=True,
                        filterable=True,
                        paginated=False,
                        empty_message="No transactions found.",
                    )
                ]
            ),
        ]
    )


def _top_products_table() -> Card:
    rows = [
        {
            "name":    p["name"],
            "units":   p["units"],
            "revenue": p["revenue"],
            "trend":   _product_sparkline(p["name"]),
            "change":  _change_badge(p["change"], p["trend"]),
        }
        for p in _TOP_PRODUCTS
    ]
    return Card(
        children=[
            CardHeader(
                children=[
                    CardTitle("Top Products"),
                    CardDescription("Best performers by revenue this month"),
                ]
            ),
            CardContent(
                children=[
                    DataTable(
                        columns=[
                            {"key": "name",    "header": "Product"},
                            {"key": "units",   "header": "Units",   "align": "right", "width": "70px"},
                            {"key": "revenue", "header": "Revenue", "align": "right", "width": "110px"},
                            {"key": "trend",   "header": "30-day Trend", "width": "140px"},
                            {"key": "change",  "header": "Change",  "align": "center", "width": "100px"},
                        ],
                        data=rows,
                        sortable=False,
                        filterable=False,
                        paginated=False,
                    )
                ]
            ),
        ]
    )


# ── Page ──────────────────────────────────────────────────────────────────────

@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="min-h-screen bg-background",
        children=[
            # ── Page wrapper with max-width ──────────────────────────────────
            Container(
                class_name="mx-auto max-w-screen-xl px-6 py-8 space-y-6",
                children=[

                    # ── Header ───────────────────────────────────────────────
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Column(
                                gap=1,
                                children=[
                                    Heading(
                                        "Analytics Dashboard",
                                        level=1,
                                        class_name="text-2xl font-bold tracking-tight",
                                    ),
                                    Paragraph(
                                        "Welcome back — here's what's happening across your platform.",
                                        muted=True,
                                    ),
                                ],
                            ),
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Button(
                                        "Refresh",
                                        variant="outline",
                                        size="sm",
                                        icon="refresh-cw",
                                        on_click=ctx.callback(refresh_data),
                                    ),
                                    ThemeSwitcher(),
                                ],
                            ),
                        ],
                    ),

                    Separator(),

                    # ── KPI cards ─────────────────────────────────────────────
                    Container(
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
                        children=[_kpi_card(k) for k in _KPI],
                    ),

                    # ── Revenue chart (2/3) + Traffic donut (1/3) ─────────────
                    Container(
                        class_name="grid grid-cols-1 lg:grid-cols-3 gap-4",
                        children=[
                            Container(
                                class_name="lg:col-span-2",
                                children=[_revenue_chart()],
                            ),
                            _traffic_chart(),
                        ],
                    ),

                    # ── Orders bar (1/3) + Transactions table (2/3) ───────────
                    Container(
                        class_name="grid grid-cols-1 lg:grid-cols-3 gap-4",
                        children=[
                            _orders_chart(),
                            Container(
                                class_name="lg:col-span-2",
                                children=[_transactions_table()],
                            ),
                        ],
                    ),

                    # ── Top products (full width) ─────────────────────────────
                    _top_products_table(),
                ],
            )
        ],
    )


# ── App wiring ────────────────────────────────────────────────────────────────

app = FastAPI()
app.include_router(ui.router)
