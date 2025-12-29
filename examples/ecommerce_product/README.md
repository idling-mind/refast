# E-commerce Product Page Example

A realistic product detail page with all the features you'd expect from a modern e-commerce site.

## Features Demonstrated

- **Carousel** - Product image gallery with navigation
- **AspectRatio** - Consistent image dimensions
- **ToggleGroup** - Color variant selection
- **Tabs** - Product details sections
- **Badge** - Discount and bestseller labels
- **Progress** - Rating distribution bars
- **HoverCard** - Additional info on hover
- **Avatar** - Reviewer avatars
- **Card** - Review cards and related products
- **Grid** - Related products layout

## Product Page Sections

1. **Image Gallery** - Carousel with thumbnails
2. **Product Info** - Name, price, rating, description
3. **Variant Selection** - Color picker with ToggleGroup
4. **Quantity Selector** - Increment/decrement buttons
5. **Add to Cart** - Primary actions
6. **Product Details Tabs** - Description, specs, reviews
7. **Reviews Section** - Rating summary and individual reviews
8. **Related Products** - Grid of similar items

## Key Patterns

### Quantity Management
```python
async def change_quantity(ctx: Context):
    action = ctx.event_data.get("action")
    quantity = ctx.state.get("quantity", 1)
    
    if action == "increment":
        quantity = min(10, quantity + 1)
    elif action == "decrement":
        quantity = max(1, quantity - 1)
    
    ctx.state.set("quantity", quantity)
    await ctx.refresh()
```

### Add to Cart
```python
async def add_to_cart(ctx: Context):
    color = ctx.state.get("selected_color", "Black")
    quantity = ctx.state.get("quantity", 1)
    await ctx.show_toast(
        f"Added {quantity}x {PRODUCT['name']} ({color}) to cart!",
        variant="success"
    )
```

### Star Rating Rendering
```python
def render_star_rating(rating: float, size: str = "sm"):
    full_stars = int(rating)
    has_half = rating - full_stars >= 0.5
    # ... render stars
```

## Running

```bash
cd examples/ecommerce_product
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.
