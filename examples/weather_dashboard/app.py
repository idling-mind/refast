"""Weather Dashboard Example.

This example demonstrates:
- Data display with Cards and Badges
- Grid layout (using Rows and Columns)
- Dynamic content updates
"""

import random
from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import (
    Container,
    Column,
    Row,
    Text,
    Button,
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    Badge,
)

ui = RefastApp(title="Weather Dashboard")

CITIES = ["New York", "London", "Tokyo", "Sydney", "Paris"]

def get_random_weather():
    return {
        "temp": random.randint(0, 35),
        "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Snowy"]),
        "humidity": random.randint(30, 90),
    }

async def refresh_data(ctx: Context):
    """Refresh weather data for all cities."""
    weather_data = {city: get_random_weather() for city in CITIES}
    ctx.state.set("weather_data", weather_data)
    await ctx.replace("dashboard-container", render_dashboard(ctx))

def weather_card(city: str, data: dict):
    temp = data["temp"]
    condition = data["condition"]
    humidity = data["humidity"]
    
    variant = "default"
    if condition == "Sunny":
        variant = "warning" # Yellow/Orange
    elif condition == "Rainy":
        variant = "default" # Blueish usually
    elif condition == "Snowy":
        variant = "secondary"
    
    return Card(
        class_name="w-full",
        children=[
            CardHeader(
                children=[
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            CardTitle(city),
                            Badge(condition, variant=variant)
                        ]
                    )
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=2,
                        children=[
                            Text(f"{temp}°C", class_name="text-4xl font-bold"),
                            Text(f"Humidity: {humidity}%", class_name="text-gray-500"),
                        ]
                    )
                ]
            )
        ]
    )

def render_dashboard(ctx: Context):
    weather_data = ctx.state.get("weather_data")
    
    return Container(
        id="dashboard-container",
        class_name="max-w-6xl mx-auto mt-10 p-4",
        children=[
            Row(
                justify="between",
                align="center",
                class_name="mb-6",
                children=[
                    Text("Weather Dashboard", class_name="text-3xl font-bold"),
                    Button("Refresh Data", on_click=ctx.callback(refresh_data)),
                ]
            ),
            # Grid layout simulation using Rows and Columns
            # We'll do a responsive grid using Tailwind classes on a Container
            Container(
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                children=[
                    weather_card(city, weather_data[city])
                    for city in CITIES
                ]
            )
        ]
    )

@ui.page("/")
def dashboard(ctx: Context):
    # Initialize data if not present
    if not ctx.state.get("weather_data"):
        ctx.state.set("weather_data", {city: get_random_weather() for city in CITIES})
    
    return render_dashboard(ctx)

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
