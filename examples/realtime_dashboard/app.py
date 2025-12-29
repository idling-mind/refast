"""Real-time Dashboard Example.

This example demonstrates:
- Server-side background updates (Server-Sent Events style)
- Updating the UI without user interaction
- Shared state across all clients
"""

import asyncio
import random
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Row,
    Text,
)

# Global state for the dashboard
dashboard_data = {
    "cpu_usage": 0,
    "memory_usage": 0,
    "active_users": 0,
    "requests_per_sec": 0,
    "system_status": "Operational",
    "last_updated": datetime.now().strftime("%H:%M:%S"),
    "logs": [],
}

ui = RefastApp(title="Real-time Monitor")


def get_status_color(usage: int) -> str:
    if usage > 80:
        return "destructive"
    if usage > 50:
        return "warning"
    return "success"


def render_metric_card(title: str, value: str, status: str = "default"):
    return Card(
        children=[
            CardHeader(
                children=[CardTitle(title, class_name="text-sm font-medium text-muted-foreground")]
            ),
            CardContent(
                children=[
                    Text(value, class_name="text-2xl font-bold"),
                    Badge(
                        status,
                        variant=status
                        if status in ["default", "secondary", "destructive", "outline"]
                        else "default",
                    )
                    if status != "default"
                    else None,
                ]
            ),
        ]
    )


def render_dashboard(ctx: Context):
    """Render the dashboard based on global data and client-specific state."""
    cpu_color = get_status_color(dashboard_data["cpu_usage"])
    mem_color = get_status_color(dashboard_data["memory_usage"])

    # Client-specific data
    client_id = ctx.state.get("client_id", "Connecting...")
    personal_counter = ctx.state.get("personal_counter", 0)

    return Container(
        id="dashboard-root",
        class_name="p-8 max-w-7xl mx-auto",
        children=[
            Row(
                justify="between",
                align="center",
                class_name="mb-8",
                children=[
                    Column(
                        children=[
                            Text("System Monitor", class_name="text-3xl font-bold tracking-tight"),
                            Text("Real-time server metrics", class_name="text-muted-foreground"),
                        ]
                    ),
                    Row(
                        gap=2,
                        children=[
                            Badge(f"Client: {client_id}", variant="secondary"),
                            Badge(f"Updates: {personal_counter}", variant="outline"),
                            Badge(
                                f"Last updated: {dashboard_data['last_updated']}", variant="outline"
                            ),
                        ],
                    ),
                ],
            ),
            # Metrics Grid
            Container(
                class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8",
                children=[
                    render_metric_card("CPU Usage", f"{dashboard_data['cpu_usage']}%", cpu_color),
                    render_metric_card(
                        "Memory Usage", f"{dashboard_data['memory_usage']}%", mem_color
                    ),
                    render_metric_card(
                        "Active Users", str(dashboard_data["active_users"]), "secondary"
                    ),
                    render_metric_card(
                        "Requests/sec", str(dashboard_data["requests_per_sec"]), "default"
                    ),
                ],
            ),
            # Recent Logs
            Card(
                class_name="col-span-4",
                children=[
                    CardHeader(children=[CardTitle("Recent System Logs")]),
                    CardContent(
                        children=[
                            Column(
                                gap=2,
                                children=[
                                    Text(log, class_name="font-mono text-sm")
                                    for log in dashboard_data["logs"][-5:]
                                ],
                            )
                        ]
                    ),
                ],
            ),
        ],
    )


@ui.page("/")
def home(ctx: Context):
    return render_dashboard(ctx)


async def update_dashboard_task():
    """Background task to update dashboard data."""
    while True:
        # Simulate changing data
        dashboard_data["cpu_usage"] = random.randint(10, 95)
        dashboard_data["memory_usage"] = random.randint(20, 85)
        dashboard_data["active_users"] = max(
            0, dashboard_data["active_users"] + random.randint(-5, 10)
        )
        dashboard_data["requests_per_sec"] = random.randint(50, 200)
        dashboard_data["last_updated"] = datetime.now().strftime("%H:%M:%S")

        # Add a log entry occasionally
        if random.random() < 0.3:
            log_types = ["INFO", "WARN", "ERROR"]
            log_msgs = [
                "Cache cleared",
                "High latency detected",
                "User login failed",
                "Backup started",
                "Service restarted",
            ]
            log_type = random.choice(log_types)
            msg = f"[{datetime.now().strftime('%H:%M:%S')}] [{log_type}] {random.choice(log_msgs)}"
            dashboard_data["logs"].append(msg)
            if len(dashboard_data["logs"]) > 10:
                dashboard_data["logs"].pop(0)

        # Push updates to all connected clients
        for ctx in ui.active_contexts:
            try:
                # Initialize client ID if not present
                if not ctx.state.get("client_id"):
                    ctx.state.set("client_id", f"#{random.randint(1000, 9999)}")

                # Update personal counter
                count = ctx.state.get("personal_counter", 0)
                ctx.state.set("personal_counter", count + 1)

                await ctx.replace("dashboard-root", render_dashboard(ctx))
            except Exception as e:
                print(f"Error updating client: {e}")
        await asyncio.sleep(2)  # Update every 2 seconds


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create background task
    task = asyncio.create_task(update_dashboard_task())
    yield
    # Shutdown: cancel background task
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


# Create FastAPI app
app = FastAPI(lifespan=lifespan)
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
