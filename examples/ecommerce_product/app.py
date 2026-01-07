"""E-commerce Product Page - Demonstrates a realistic product detail page.

This example demonstrates:
- Product image gallery with carousel
- Product variants selection
- Quantity selector
- Add to cart functionality
- Tabs for product details
- Reviews section with ratings
- Related products
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    AspectRatio,
    Avatar,
    Badge,
    Button,
    Card,
    CardContent,
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
    Column,
    Container,
    Grid,
    Label,
    Progress,
    Row,
    Separator,
    TabItem,
    Tabs,
    Text,
    ToggleGroup,
    ToggleGroupItem,
)

# Create the Refast app
ui = RefastApp(title="Product Page")


# Sample product data
PRODUCT = {
    "id": "prod-001",
    "name": "Premium Wireless Headphones",
    "brand": "AudioTech",
    "price": 299.99,
    "original_price": 399.99,
    "rating": 4.5,
    "reviews_count": 128,
    "description": "Experience premium audio quality with our flagship wireless headphones. Featuring active noise cancellation, 40-hour battery life, and ultra-comfortable memory foam ear cushions.",
    "images": [
        "/images/headphones-1.jpg",
        "/images/headphones-2.jpg",
        "/images/headphones-3.jpg",
        "/images/headphones-4.jpg",
    ],
    "colors": ["Black", "Silver", "Navy Blue", "Rose Gold"],
    "sizes": None,
    "in_stock": True,
    "features": [
        "Active Noise Cancellation (ANC)",
        "40-hour battery life",
        "Bluetooth 5.2",
        "USB-C fast charging",
        "Foldable design",
        "Premium carrying case included",
    ],
    "specifications": {
        "Driver Size": "40mm",
        "Frequency Response": "20Hz - 20kHz",
        "Impedance": "32 Ohms",
        "Weight": "250g",
        "Connectivity": "Bluetooth 5.2, 3.5mm aux",
        "Charging Time": "2 hours",
        "Battery Life": "40 hours (ANC on), 60 hours (ANC off)",
    },
}

REVIEWS = [
    {
        "id": 1,
        "author": "John D.",
        "avatar": "JD",
        "rating": 5,
        "date": "2024-12-10",
        "title": "Best headphones I've ever owned!",
        "content": "The sound quality is incredible and the noise cancellation is top-notch. Highly recommend!",
        "verified": True,
    },
    {
        "id": 2,
        "author": "Sarah M.",
        "avatar": "SM",
        "rating": 4,
        "date": "2024-12-08",
        "title": "Great quality, minor comfort issue",
        "content": "Excellent sound and build quality. The ear cups get a bit warm after extended use, but overall very satisfied.",
        "verified": True,
    },
    {
        "id": 3,
        "author": "Mike R.",
        "avatar": "MR",
        "rating": 5,
        "date": "2024-12-05",
        "title": "Perfect for travel",
        "content": "Used these on a long flight and they were amazing. Battery lasted the entire trip and noise cancellation blocked out engine noise completely.",
        "verified": False,
    },
]

RELATED_PRODUCTS = [
    {
        "id": "prod-002",
        "name": "Wireless Earbuds Pro",
        "price": 149.99,
        "image": "/images/earbuds.jpg",
        "rating": 4.3,
    },
    {
        "id": "prod-003",
        "name": "Premium Headphone Stand",
        "price": 49.99,
        "image": "/images/stand.jpg",
        "rating": 4.8,
    },
    {
        "id": "prod-004",
        "name": "Replacement Ear Cushions",
        "price": 29.99,
        "image": "/images/cushions.jpg",
        "rating": 4.6,
    },
]


# Callback handlers
async def add_to_cart(ctx: Context):
    """Add product to cart."""
    color = ctx.state.get("selected_color", "Black")
    quantity = ctx.state.get("quantity", 1)
    await ctx.show_toast(
        f"Added {quantity}x {PRODUCT['name']} ({color}) to cart!", variant="success"
    )


async def add_to_wishlist(ctx: Context):
    """Add product to wishlist."""
    await ctx.show_toast("Added to wishlist!", variant="info")


async def select_color(ctx: Context):
    """Handle color selection."""
    color = ctx.event_data.get("value")
    ctx.state.set("selected_color", color)


async def change_quantity(ctx: Context):
    """Handle quantity change."""
    action = ctx.event_data.get("action")
    quantity = ctx.state.get("quantity", 1)

    if action == "increment":
        quantity = min(10, quantity + 1)
    elif action == "decrement":
        quantity = max(1, quantity - 1)

    ctx.state.set("quantity", quantity)
    await ctx.refresh()


async def buy_now(ctx: Context):
    """Handle buy now action."""
    await ctx.show_toast("Redirecting to checkout...", variant="info")


def render_star_rating(rating: float, size: str = "sm"):
    """Render star rating."""
    full_stars = int(rating)
    has_half = rating - full_stars >= 0.5
    empty_stars = 5 - full_stars - (1 if has_half else 0)

    size_class = "text-sm" if size == "sm" else "text-lg"

    stars = []
    for _ in range(full_stars):
        stars.append(Text("★", class_name=f"{size_class} text-primary-500"))
    if has_half:
        stars.append(Text("★", class_name=f"{size_class} text-primary-500 opacity-50"))
    for _ in range(empty_stars):
        stars.append(Text("☆", class_name=f"{size_class} text-primary-500"))
    return Row(gap=0, children=stars)


def render_review_card(review: dict):
    """Render a review card."""
    return Card(
        class_name="mb-4",
        children=[
            CardContent(
                class_name="p-4",
                children=[
                    Column(
                        gap=3,
                        children=[
                            Row(
                                justify="between",
                                align="start",
                                children=[
                                    Row(
                                        gap=3,
                                        align="center",
                                        children=[
                                            Avatar(fallback=review["avatar"]),
                                            Column(
                                                gap=0,
                                                children=[
                                                    Row(
                                                        gap=2,
                                                        align="center",
                                                        children=[
                                                            Text(
                                                                review["author"],
                                                                class_name="font-medium",
                                                            ),
                                                            Badge(
                                                                "Verified", variant="success"
                                                            )
                                                            if review["verified"]
                                                            else "",
                                                        ],
                                                    ),
                                                    Text(
                                                        review["date"],
                                                        class_name="text-xs text-muted-foreground",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    render_star_rating(review["rating"]),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text(review["title"], class_name="font-medium"),
                                    Text(
                                        review["content"],
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def render_related_product(product: dict):
    """Render a related product card."""
    return Card(
        class_name="cursor-pointer hover:shadow-lg transition-shadow",
        children=[
            CardContent(
                class_name="p-4",
                children=[
                    Column(
                        gap=3,
                        children=[
                            AspectRatio(
                                ratio=1,
                                class_name="bg-muted rounded-md",
                                children=[
                                    Container(
                                        class_name="flex items-center justify-center h-full",
                                        children=[
                                            Text("🎧", class_name="text-4xl"),
                                        ],
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text(
                                        product["name"],
                                        class_name="font-medium text-sm line-clamp-2",
                                    ),
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            render_star_rating(product["rating"]),
                                            Text(
                                                f"({product['rating']})",
                                                class_name="text-xs text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                    Text(f"${product['price']}", class_name="font-bold"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# Main page
@ui.page("/")
def home(ctx: Context):
    """Product page."""
    selected_color = ctx.state.get("selected_color", "Black")
    quantity = ctx.state.get("quantity", 1)
    selected_tab = ctx.state.get("selected_tab", "description")

    discount_percent = int((1 - PRODUCT["price"] / PRODUCT["original_price"]) * 100)

    return Container(
        class_name="max-w-7xl mx-auto p-8",
        children=[
            Column(
                gap=8,
                children=[
                    # Breadcrumb
                    Row(
                        gap=2,
                        class_name="text-sm text-muted-foreground",
                        children=[
                            Text("Home"),
                            Text("/"),
                            Text("Electronics"),
                            Text("/"),
                            Text("Headphones"),
                            Text("/"),
                            Text(PRODUCT["name"], class_name="text-foreground"),
                        ],
                    ),
                    # Product main section
                    Row(
                        gap=12,
                        class_name="flex-col lg:flex-row",
                        children=[
                            # Product images
                            Container(
                                class_name="flex-1",
                                children=[
                                    Carousel(
                                        children=[
                                            CarouselContent(
                                                children=[
                                                    CarouselItem(
                                                        children=[
                                                            AspectRatio(
                                                                ratio=1,
                                                                class_name="bg-muted rounded-lg",
                                                                children=[
                                                                    Container(
                                                                        class_name="flex items-center justify-center h-full",
                                                                        children=[
                                                                            Text(
                                                                                "🎧",
                                                                                class_name="text-9xl",
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    )
                                                    for _ in PRODUCT["images"]
                                                ],
                                            ),
                                            CarouselPrevious(),
                                            CarouselNext(),
                                        ],
                                    ),
                                    # Thumbnail row
                                    Row(
                                        gap=2,
                                        class_name="mt-4",
                                        children=[
                                            Container(
                                                class_name="w-20 h-20 bg-muted rounded-md cursor-pointer border-2 border-primary flex items-center justify-center",
                                                children=[Text("🎧", class_name="text-2xl")],
                                            )
                                            for i in range(4)
                                        ],
                                    ),
                                ],
                            ),
                            # Product info
                            Container(
                                class_name="flex-1",
                                children=[
                                    Column(
                                        gap=6,
                                        children=[
                                            # Brand and badges
                                            Row(
                                                gap=2,
                                                children=[
                                                    Text(
                                                        PRODUCT["brand"],
                                                        class_name="text-muted-foreground",
                                                    ),
                                                    Badge(
                                                        f"{discount_percent}% OFF",
                                                        variant="destructive",
                                                    ),
                                                    Badge("Bestseller", variant="secondary"),
                                                ],
                                            ),
                                            # Title
                                            Text(PRODUCT["name"], class_name="text-3xl font-bold"),
                                            # Rating
                                            Row(
                                                gap=2,
                                                align="center",
                                                children=[
                                                    render_star_rating(PRODUCT["rating"], "lg"),
                                                    Text(
                                                        f"{PRODUCT['rating']}",
                                                        class_name="font-medium",
                                                    ),
                                                    Text(
                                                        f"({PRODUCT['reviews_count']} reviews)",
                                                        class_name="text-muted-foreground",
                                                    ),
                                                ],
                                            ),
                                            # Price
                                            Row(
                                                gap=3,
                                                align="baseline",
                                                children=[
                                                    Text(
                                                        f"${PRODUCT['price']}",
                                                        class_name="text-3xl font-bold",
                                                    ),
                                                    Text(
                                                        f"${PRODUCT['original_price']}",
                                                        class_name="text-xl text-muted-foreground line-through",
                                                    ),
                                                ],
                                            ),
                                            Separator(),
                                            # Color selection
                                            Column(
                                                gap=3,
                                                children=[
                                                    Row(
                                                        gap=2,
                                                        children=[
                                                            Label("Color:"),
                                                            Text(
                                                                selected_color,
                                                                class_name="font-medium",
                                                            ),
                                                        ],
                                                    ),
                                                    ToggleGroup(
                                                        type="single",
                                                        value=selected_color,
                                                        on_value_change=ctx.callback(select_color),
                                                        children=[
                                                            ToggleGroupItem(
                                                                value=color, label=color
                                                            )
                                                            for color in PRODUCT["colors"]
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            # Quantity selector
                                            Column(
                                                gap=3,
                                                children=[
                                                    Label("Quantity:"),
                                                    Row(
                                                        gap=0,
                                                        children=[
                                                            Button(
                                                                label="-",
                                                                variant="outline",
                                                                class_name="rounded-r-none",
                                                                on_click=ctx.callback(
                                                                    change_quantity,
                                                                    action="decrement",
                                                                ),
                                                            ),
                                                            Container(
                                                                class_name="w-16 h-10 border-y flex items-center justify-center",
                                                                children=[
                                                                    Text(
                                                                        str(quantity),
                                                                        class_name="font-medium",
                                                                    ),
                                                                ],
                                                            ),
                                                            Button(
                                                                label="+",
                                                                variant="outline",
                                                                class_name="rounded-l-none",
                                                                on_click=ctx.callback(
                                                                    change_quantity,
                                                                    action="increment",
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            # Add to cart buttons
                                            Row(
                                                gap=3,
                                                children=[
                                                    Button(
                                                        label="Add to Cart",
                                                        size="lg",
                                                        class_name="flex-1",
                                                        on_click=ctx.callback(add_to_cart),
                                                    ),
                                                    Button(
                                                        label="Buy Now",
                                                        variant="secondary",
                                                        size="lg",
                                                        class_name="flex-1",
                                                        on_click=ctx.callback(buy_now),
                                                    ),
                                                    Button(
                                                        label="♡",
                                                        variant="outline",
                                                        size="lg",
                                                        on_click=ctx.callback(add_to_wishlist),
                                                    ),
                                                ],
                                            ),
                                            # Stock status
                                            Row(
                                                gap=2,
                                                align="center",
                                                children=[
                                                    Container(
                                                        class_name="w-2 h-2 rounded-full bg-green-500",
                                                    ),
                                                    Text(
                                                        "In Stock",
                                                        class_name="text-green-600 font-medium",
                                                    ),
                                                    Text(
                                                        "- Ships within 24 hours",
                                                        class_name="text-muted-foreground",
                                                    ),
                                                ],
                                            ),
                                            Separator(),
                                            # Key features
                                            Column(
                                                gap=2,
                                                children=[
                                                    Text(
                                                        "Key Features:", class_name="font-semibold"
                                                    ),
                                                    Column(
                                                        gap=1,
                                                        children=[
                                                            Row(
                                                                gap=2,
                                                                children=[
                                                                    Text(
                                                                        "✓",
                                                                        class_name="text-green-600",
                                                                    ),
                                                                    Text(
                                                                        feature,
                                                                        class_name="text-sm",
                                                                    ),
                                                                ],
                                                            )
                                                            for feature in PRODUCT["features"][:4]
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Product details tabs
                    Card(
                        children=[
                            CardContent(
                                class_name="p-6",
                                children=[
                                    Tabs(
                                        default_value="description",
                                        children=[
                                            TabItem(value="description", label="Description"),
                                            TabItem(value="specifications", label="Specifications"),
                                            TabItem(
                                                value="reviews",
                                                label=f"Reviews ({PRODUCT['reviews_count']})",
                                            ),
                                        ],
                                    ),
                                    Container(
                                        class_name="mt-6",
                                        children=[
                                            Column(
                                                gap=4,
                                                children=[
                                                    # Description content
                                                    Text(PRODUCT["description"]),
                                                    Text(
                                                        "Features:", class_name="font-semibold mt-4"
                                                    ),
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Row(
                                                                gap=2,
                                                                children=[
                                                                    Text(
                                                                        "•",
                                                                        class_name="text-primary",
                                                                    ),
                                                                    Text(feature),
                                                                ],
                                                            )
                                                            for feature in PRODUCT["features"]
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Reviews section
                    Column(
                        gap=4,
                        children=[
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    Text("Customer Reviews", class_name="text-xl font-bold"),
                                    Button(label="Write a Review", variant="outline"),
                                ],
                            ),
                            # Rating summary
                            Card(
                                children=[
                                    CardContent(
                                        class_name="p-6",
                                        children=[
                                            Row(
                                                gap=8,
                                                children=[
                                                    Column(
                                                        gap=2,
                                                        align="center",
                                                        children=[
                                                            Text(
                                                                str(PRODUCT["rating"]),
                                                                class_name="text-5xl font-bold",
                                                            ),
                                                            render_star_rating(
                                                                PRODUCT["rating"], "lg"
                                                            ),
                                                            Text(
                                                                f"Based on {PRODUCT['reviews_count']} reviews",
                                                                class_name="text-sm text-muted-foreground",
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(
                                                        orientation="vertical", class_name="h-32"
                                                    ),
                                                    Column(
                                                        gap=2,
                                                        class_name="flex-1",
                                                        children=[
                                                            Row(
                                                                gap=2,
                                                                align="center",
                                                                children=[
                                                                    Text(
                                                                        "5★",
                                                                        class_name="w-8 text-sm",
                                                                    ),
                                                                    Progress(
                                                                        value=70,
                                                                        class_name="flex-1",
                                                                    ),
                                                                    Text(
                                                                        "70%",
                                                                        class_name="w-10 text-sm text-right",
                                                                    ),
                                                                ],
                                                            ),
                                                            Row(
                                                                gap=2,
                                                                align="center",
                                                                children=[
                                                                    Text(
                                                                        "4★",
                                                                        class_name="w-8 text-sm",
                                                                    ),
                                                                    Progress(
                                                                        value=20,
                                                                        class_name="flex-1",
                                                                    ),
                                                                    Text(
                                                                        "20%",
                                                                        class_name="w-10 text-sm text-right",
                                                                    ),
                                                                ],
                                                            ),
                                                            Row(
                                                                gap=2,
                                                                align="center",
                                                                children=[
                                                                    Text(
                                                                        "3★",
                                                                        class_name="w-8 text-sm",
                                                                    ),
                                                                    Progress(
                                                                        value=7, class_name="flex-1"
                                                                    ),
                                                                    Text(
                                                                        "7%",
                                                                        class_name="w-10 text-sm text-right",
                                                                    ),
                                                                ],
                                                            ),
                                                            Row(
                                                                gap=2,
                                                                align="center",
                                                                children=[
                                                                    Text(
                                                                        "2★",
                                                                        class_name="w-8 text-sm",
                                                                    ),
                                                                    Progress(
                                                                        value=2, class_name="flex-1"
                                                                    ),
                                                                    Text(
                                                                        "2%",
                                                                        class_name="w-10 text-sm text-right",
                                                                    ),
                                                                ],
                                                            ),
                                                            Row(
                                                                gap=2,
                                                                align="center",
                                                                children=[
                                                                    Text(
                                                                        "1★",
                                                                        class_name="w-8 text-sm",
                                                                    ),
                                                                    Progress(
                                                                        value=1, class_name="flex-1"
                                                                    ),
                                                                    Text(
                                                                        "1%",
                                                                        class_name="w-10 text-sm text-right",
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            # Individual reviews
                            Column(
                                gap=0,
                                children=[render_review_card(review) for review in REVIEWS],
                            ),
                            Row(
                                justify="center",
                                children=[
                                    Button(label="Load More Reviews", variant="outline"),
                                ],
                            ),
                        ],
                    ),
                    # Related products
                    Column(
                        gap=4,
                        children=[
                            Text("Related Products", class_name="text-xl font-bold"),
                            Grid(
                                columns=4,
                                gap=4,
                                children=[
                                    render_related_product(product) for product in RELATED_PRODUCTS
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# Create FastAPI app and include Refast
app = FastAPI()
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
