# Refast Styling Guide

This guide provides comprehensive examples and best practices for styling Refast applications. To maintain a lightweight frontend bundle (~500KB), Refast uses a **hybrid styling approach**:

1.  **Tailwind Utility Classes**: For standard layout, spacing, typography, and theming.
2.  **Style Prop**: For specific dimensions, ad-hoc positioning, and custom colors.

---

## 🏗️ Core Layout Patterns

### Flexbox Layouts

Use standard Tailwind flex utilities for structure and alignment.

```python
from refast.components import Container, Div, Text

def Header():
    return Div(
        class_name="flex flex-row items-center justify-between p-4 border-b",
        children=[
            Text("Logo", class_name="text-lg font-bold"),
            Div(
                class_name="flex gap-4",
                children=[
                    Text("Home", class_name="text-muted-foreground hover:text-foreground cursor-pointer"),
                    Text("Settings", class_name="text-muted-foreground hover:text-foreground cursor-pointer"),
                ]
            )
        ]
    )
```

### Grid Dashboard

Use `grid-cols-*` (supported: 1-6, 12) for layouts.

```python
def DashboardGrid():
    return Div(
        class_name="grid grid-cols-1 md:grid-cols-3 gap-6 p-6",
        children=[
            StatCard("Revenue", "$12,000"),
            StatCard("Users", "1,234"),
            StatCard("Growth", "+15%"),
        ]
    )

def StatCard(title, value):
    return Div(
        class_name="p-6 rounded-xl border bg-card text-card-foreground shadow-sm",
        children=[
            Text(title, class_name="text-sm font-medium text-muted-foreground"),
            Text(value, class_name="text-2xl font-bold mt-2")
        ]
    )
```

---

## 🎨 Theming & Colors

Refast enforces **Semantic Colors** to ensure your app looks great in both light and dark modes automatically. Do not use raw colors like `bg-blue-500`.

| Class Pattern | Description | usage Example |
|--------------|-------------|---------------|
| `bg-background` | Page background | Main containers |
| `text-foreground` | Main text color | Body text |
| `bg-primary` | Primary brand color | Call-to-action buttons |
| `text-muted-foreground` | Subtle text | Labels, hints, secondary info |
| `border-input` | Form borders | Input fields |
| `bg-destructive` | Error/Danger | Delete buttons |

**Example: Themed Card**
```python
Div(
    class_name="bg-card text-card-foreground border rounded-lg p-6 shadow-sm",
    children=[
        Text("Primary Action", class_name="bg-primary text-primary-foreground px-4 py-2 rounded-md")
    ]
)
```

---

## 📏 Handling Dimensions (The `style` prop)

To keep the CSS bundle small, we do **not** include every width/height utility (like `w-1/2`, `h-screen`). Instead, use the `style` prop for dimensions.

### ✅ Do This
```python
# Use style for dimensions
Div(
    class_name="bg-muted rounded-md",
    style={"width": "100%", "height": "300px"}
)

# Use style for complex positioning
Div(
    class_name="absolute bg-popover border p-2 rounded shadow-md",
    style={"top": "50px", "right": "20px", "maxWidth": "200px"}
)
```

### ❌ Instead of This
```python
# These classes might NOT be generated in the reduced bundle
Div(class_name="w-full h-[300px]") 
```

---

## 🖱️ Interactive Elements

Hover and Focus states are supported for semantic colors and standard interactions.

```python
def InteractiveButton():
    return Button(
        "Click Me",
        class_name="""
            transition-colors duration-200
            bg-secondary text-secondary-foreground
            hover:bg-primary hover:text-primary-foreground
            cursor-pointer
        """
    )
```

---

## 📱 Responsive Design

Refast supports standard Tailwind breakpoints (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`).

```python
# Stack on mobile, side-by-side on desktop
Div(
    class_name="flex flex-col md:flex-row gap-4",
    children=[
        Sidebar(class_name="w-full md:w-64"), # w-64 is NOT safelisted, use style instead!
        # Correction:
        Sidebar(style={"width": "100%"}, class_name="md:w-auto flex-1") 
    ]
)
```

**Common Responsive Pattern:**
```python
Div(
    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
)
```

---

## 📚 Technical Reference

For a complete list of exactly which Tailwind classes are included in the bundle, please refer to the [Tailwind Support Matrix](TAILWIND_SUPPORT.md).
