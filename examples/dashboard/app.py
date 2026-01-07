"""Dashboard Example - Analytics Dashboard Application.

This example demonstrates:
- Complex layout with multiple components
- Data tables
- Statistics cards
- Navigation between pages
- Responsive grid layout
"""

import random
from dataclasses import dataclass
from datetime import datetime, timedelta

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
    Grid,
    Progress,
    Row,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
    Text,
)


# Sample data
@dataclass
class User:
    id: int
    name: str
    email: str
    role: str
    status: str
    last_active: datetime


@dataclass
class Metric:
    name: str
    value: str
    change: float
    trend: str  # "up" or "down"


# Generate sample data
def generate_users():
    names = ["Alice Johnson", "Bob Smith", "Carol White", "David Brown", "Eve Davis"]
    roles = ["Admin", "Editor", "Viewer", "Editor", "Admin"]
    statuses = ["active", "active", "inactive", "active", "active"]

    users = []
    for i, name in enumerate(names):
        users.append(
            User(
                id=i + 1,
                name=name,
                email=f"{name.lower().replace(' ', '.')}@example.com",
                role=roles[i],
                status=statuses[i],
                last_active=datetime.now() - timedelta(hours=random.randint(1, 72)),
            )
        )
    return users


def generate_metrics():
    return [
        Metric("Total Users", "2,345", 12.5, "up"),
        Metric("Active Sessions", "145", -3.2, "down"),
        Metric("Page Views", "23.4K", 8.1, "up"),
        Metric("Conversion", "3.2%", 0.5, "up"),
    ]


USERS = generate_users()
METRICS = generate_metrics()


# Create the Refast app
ui = RefastApp(title="Dashboard")


def render_metric_card(metric: Metric, index: int):
    """Render a metric card."""
    trend_style = {"color": "#16a34a"} if metric.trend == "up" else {"color": "#dc2626"}
    trend_icon = "↑" if metric.trend == "up" else "↓"

    return Card(
        id=f"metric-{index}",
        children=[
            CardContent(
                class_name="pt-6",
                children=[
                    Column(
                        gap=2,
                        children=[
                            Text(
                                metric.name,
                                class_name="text-sm font-medium text-muted-foreground",
                            ),
                            Text(
                                metric.value,
                                class_name="text-3xl font-bold",
                            ),
                            Row(
                                gap=1,
                                align="center",
                                children=[
                                    Text(
                                        f"{trend_icon} {abs(metric.change)}%",
                                        class_name="text-sm font-medium",
                                        style=trend_style,
                                    ),
                                    Text(
                                        "from last week",
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            )
        ],
    )


def render_user_row(user: User):
    """Render a user table row."""
    status_variant = "success" if user.status == "active" else "secondary"

    return TableRow(
        id=f"user-row-{user.id}",
        children=[
            TableCell(
                children=[
                    Row(
                        gap=3,
                        align="center",
                        children=[
                            Avatar(name=user.name, size="sm"),
                            Column(
                                gap=0,
                                children=[
                                    Text(user.name, class_name="font-medium"),
                                    Text(
                                        user.email,
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                ],
                            ),
                        ],
                    )
                ]
            ),
            TableCell(children=[Text(user.role)]),
            TableCell(children=[Badge(user.status.capitalize(), variant=status_variant)]),
            TableCell(
                children=[
                    Text(
                        user.last_active.strftime("%Y-%m-%d %H:%M"),
                        class_name="text-sm text-muted-foreground",
                    )
                ]
            ),
            TableCell(
                children=[
                    Button("Edit", variant="ghost", size="sm"),
                ]
            ),
        ],
    )


def render_sidebar(ctx: Context, active_page: str):
    """Render the sidebar navigation."""
    nav_items = [
        ("Dashboard", "/", "📊"),
        ("Users", "/users", "👥"),
        ("Analytics", "/analytics", "📈"),
        ("Settings", "/settings", "⚙️"),
    ]

    return Container(
        id="sidebar",
        class_name="p-4 bg-card border-r",
        style={"width": "16rem", "minHeight": "100vh"},
        children=[
            Column(
                gap=6,
                children=[
                    # Logo
                    Text(
                        "Dashboard",
                        class_name="text-xl font-bold px-4",
                    ),
                    # Navigation
                    Column(
                        gap=1,
                        children=[
                            Container(
                                class_name=f"px-4 py-2 rounded-lg cursor-pointer "
                                f"{'bg-accent text-accent-foreground' if item[1] == active_page else 'hover:bg-accent/50'}",
                                children=[
                                    Row(
                                        gap=3,
                                        children=[
                                            Text(item[2]),
                                            Text(item[0]),
                                        ],
                                    )
                                ],
                            )
                            for item in nav_items
                        ],
                    ),
                ],
            )
        ],
    )


@ui.page("/")
def dashboard(ctx: Context):
    """Main dashboard page."""
    return Row(
        id="main-layout",
        class_name="bg-background",
        style={"minHeight": "100vh"},
        children=[
            # Sidebar
            render_sidebar(ctx, "/"),
            # Main content
            Container(
                id="main-content",
                class_name="flex-1 p-8",
                children=[
                    Column(
                        gap=8,
                        children=[
                            # Header
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    Column(
                                        gap=1,
                                        children=[
                                            Text(
                                                "Dashboard",
                                                class_name="text-2xl font-bold",
                                            ),
                                            Text(
                                                "Welcome back! Here's your overview.",
                                                class_name="text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                    Button(
                                        "Export Report",
                                        variant="primary",
                                    ),
                                ],
                            ),
                            # Metrics grid
                            Grid(
                                id="metrics-grid",
                                cols=4,
                                gap=6,
                                children=[
                                    render_metric_card(metric, i)
                                    for i, metric in enumerate(METRICS)
                                ],
                            ),
                            # Users section
                            Card(
                                id="users-card",
                                children=[
                                    CardHeader(
                                        children=[
                                            Row(
                                                justify="between",
                                                align="center",
                                                children=[
                                                    Column(
                                                        children=[
                                                            CardTitle("Recent Users"),
                                                            CardDescription(
                                                                "A list of users who recently logged in"
                                                            ),
                                                        ]
                                                    ),
                                                    Button(
                                                        "View All",
                                                        variant="outline",
                                                        size="sm",
                                                    ),
                                                ],
                                            )
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Table(
                                                id="users-table",
                                                children=[
                                                    TableHeader(
                                                        children=[
                                                            TableRow(
                                                                children=[
                                                                    TableHead(
                                                                        children=[Text("User")]
                                                                    ),
                                                                    TableHead(
                                                                        children=[Text("Role")]
                                                                    ),
                                                                    TableHead(
                                                                        children=[Text("Status")]
                                                                    ),
                                                                    TableHead(
                                                                        children=[
                                                                            Text("Last Active")
                                                                        ]
                                                                    ),
                                                                    TableHead(children=[Text("")]),
                                                                ],
                                                            )
                                                        ]
                                                    ),
                                                    TableBody(
                                                        children=[
                                                            render_user_row(user) for user in USERS
                                                        ]
                                                    ),
                                                ],
                                            )
                                        ]
                                    ),
                                ],
                            ),
                            # Activity section
                            Grid(
                                cols=2,
                                gap=6,
                                children=[
                                    Card(
                                        children=[
                                            CardHeader(
                                                children=[
                                                    CardTitle("System Health"),
                                                ]
                                            ),
                                            CardContent(
                                                children=[
                                                    Column(
                                                        gap=4,
                                                        children=[
                                                            Column(
                                                                gap=2,
                                                                children=[
                                                                    Row(
                                                                        justify="between",
                                                                        children=[
                                                                            Text("CPU Usage"),
                                                                            Text("45%"),
                                                                        ],
                                                                    ),
                                                                    Progress(value=45),
                                                                ],
                                                            ),
                                                            Column(
                                                                gap=2,
                                                                children=[
                                                                    Row(
                                                                        justify="between",
                                                                        children=[
                                                                            Text("Memory"),
                                                                            Text("62%"),
                                                                        ],
                                                                    ),
                                                                    Progress(value=62),
                                                                ],
                                                            ),
                                                            Column(
                                                                gap=2,
                                                                children=[
                                                                    Row(
                                                                        justify="between",
                                                                        children=[
                                                                            Text("Storage"),
                                                                            Text("78%"),
                                                                        ],
                                                                    ),
                                                                    Progress(value=78),
                                                                ],
                                                            ),
                                                        ],
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    Card(
                                        children=[
                                            CardHeader(
                                                children=[
                                                    CardTitle("Recent Activity"),
                                                ]
                                            ),
                                            CardContent(
                                                children=[
                                                    Column(
                                                        gap=3,
                                                        children=[
                                                            Row(
                                                                gap=3,
                                                                children=[
                                                                    Container(
                                                                        class_name="w-2 h-2 rounded-full bg-green-500 mt-2",
                                                                    ),
                                                                    Column(
                                                                        gap=0,
                                                                        children=[
                                                                            Text(
                                                                                "New user registered"
                                                                            ),
                                                                            Text(
                                                                                "5 minutes ago",
                                                                                class_name="text-sm text-gray-500",
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            Row(
                                                                gap=3,
                                                                children=[
                                                                    Container(
                                                                        class_name="w-2 h-2 rounded-full bg-blue-500 mt-2",
                                                                    ),
                                                                    Column(
                                                                        gap=0,
                                                                        children=[
                                                                            Text(
                                                                                "Report generated"
                                                                            ),
                                                                            Text(
                                                                                "12 minutes ago",
                                                                                class_name="text-sm text-gray-500",
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            Row(
                                                                gap=3,
                                                                children=[
                                                                    Container(
                                                                        class_name="w-2 h-2 rounded-full bg-yellow-500 mt-2",
                                                                    ),
                                                                    Column(
                                                                        gap=0,
                                                                        children=[
                                                                            Text(
                                                                                "Settings updated"
                                                                            ),
                                                                            Text(
                                                                                "1 hour ago",
                                                                                class_name="text-sm text-gray-500",
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
        ],
    )


# Create the FastAPI app and mount Refast
app = FastAPI(title="Refast Dashboard Example")
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
