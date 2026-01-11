"""Component Showcase - Demonstrates all Stage 9 Radix UI Components.

This example demonstrates:
- Controls: Switch, Slider, Toggle, Calendar, DatePicker, Combobox
- Navigation: Breadcrumb, Tabs, Pagination, Menubar
- Overlays: AlertDialog, Sheet, Drawer, Popover, HoverCard
- Utility: Separator, AspectRatio, ScrollArea, Collapsible, Carousel
- New: Image, Markdown, CheckboxGroup, RadioGroup
"""

from textwrap import dedent

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    # Overlays
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
    AspectRatio,
    Avatar,
    # Feedback
    Badge,
    # Navigation
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    CheckboxGroup,
    Code,
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
    Column,
    Combobox,
    Container,
    HoverCard,
    HoverCardContent,
    HoverCardTrigger,
    Image,
    Input,
    Label,
    Markdown,
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
    Popover,
    PopoverContent,
    PopoverTrigger,
    RadioGroup,
    Row,
    ScrollArea,
    # Utility
    Separator,
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
    Slider,
    Spacer,
    # Controls
    Switch,
    TabItem,
    Tabs,
    Text,
    ThemeSwitcher,
    ToggleGroup,
    ToggleGroupItem,
)

# Create the Refast app
ui = RefastApp(title="Component Showcase")


# Callback handlers
async def on_switch_change(ctx: Context):
    """Handle switch toggle."""
    current = ctx.state.get("notifications", False)
    ctx.state.set("notifications", not current)
    await ctx.update_text("switch-status", "ON" if not current else "OFF")


async def on_slider_change(ctx: Context):
    """Handle slider change."""
    value = ctx.event_data.get("0", 50)
    ctx.state.set("volume", value)
    await ctx.update_text("slider-value", f"{value}%")


async def on_toggle_change(ctx: Context):
    """Handle text formatting toggle."""
    # event_data is now {"bold": True, "italic": False, ...}
    print(ctx.event_data)
    formats = ctx.event_data
    active = [k for k, v in formats.items() if v]
    msg = f"Active formats: {', '.join(active)}" if active else "No formats active"
    await ctx.show_toast(msg, variant="info")


async def on_checkbox_group_change(ctx: Context):
    """Handle checkbox group selection change."""
    selected = list(ctx.event_data.values())
    ctx.state.set("selected_toppings", selected)
    if selected:
        await ctx.show_toast(f"Selected toppings: {', '.join(selected)}", variant="info")
    else:
        await ctx.show_toast("No toppings selected", variant="info")


async def on_radio_group_change(ctx: Context):
    """Handle radio group selection change."""
    selected = ctx.event_data.get("value", "")
    ctx.state.set("selected_size", selected)
    await ctx.show_toast(f"Selected size: {selected}", variant="info")


async def dropdown_select(ctx: Context):
    """Handle dropdown selection."""
    print(ctx.event_data)
    if "value" in ctx.event_data:
        selection = ctx.event_data.get("value", "")
    else:
        selection = ", ".join(ctx.event_data.values())
    await ctx.show_toast(f"Selected: {selection}", variant="info")


async def on_page_change(ctx: Context, page: int):
    """Handle pagination."""
    print(f"Page changed to {page}")
    ctx.state.set("current_page", page)
    # Re-render pagination to update active state
    await ctx.replace("pagination", render_pagination(ctx, page))


def render_pagination(ctx: Context, current_page: int):
    """Render the pagination component."""
    return Pagination(
        id="pagination",
        children=[
            PaginationContent(
                children=[
                    PaginationItem(
                        children=[
                            PaginationPrevious(
                                href="#",
                                on_click=ctx.callback(
                                    on_page_change, page=current_page - 1 if current_page > 1 else 1
                                ),
                            )
                        ]
                    ),
                    PaginationItem(
                        children=[
                            PaginationLink(
                                label="1",
                                href="#",
                                active=(current_page == 1),
                                on_click=ctx.callback(on_page_change, page=1),
                            )
                        ]
                    ),
                    PaginationItem(
                        children=[
                            PaginationLink(
                                label="2",
                                href="#",
                                active=(current_page == 2),
                                on_click=ctx.callback(on_page_change, page=2),
                            )
                        ]
                    ),
                    PaginationItem(
                        children=[
                            PaginationLink(
                                label="3",
                                href="#",
                                active=(current_page == 3),
                                on_click=ctx.callback(on_page_change, page=3),
                            )
                        ]
                    ),
                    PaginationItem(children=[PaginationEllipsis()]),
                    PaginationItem(
                        children=[
                            PaginationNext(
                                href="#",
                                on_click=ctx.callback(on_page_change, page=current_page + 1),
                            )
                        ]
                    ),
                ],
            ),
        ],
    )


async def on_confirm_delete(ctx: Context):
    """Handle delete confirmation."""
    await ctx.show_toast("Item deleted successfully", variant="success")


async def on_sheet_save(ctx: Context):
    """Handle sheet save."""
    await ctx.show_toast("Settings saved!", variant="success")


# Main page
@ui.page("/")
def home(ctx: Context):
    """Component showcase home page."""
    notifications = ctx.state.get("notifications", False)
    volume = ctx.state.get("volume", 50)
    current_page = ctx.state.get("current_page", 1)

    return Container(
        class_name="p-6",
        style={"maxWidth": "72rem", "marginLeft": "auto", "marginRight": "auto"},
        children=[
            # Header
            Row(
                [
                    Column(
                        gap=2,
                        class_name="mb-6",
                        children=[
                            Text(
                                "Component Showcase",
                                class_name="font-bold",
                                style={"fontSize": "2.25rem", "lineHeight": "2.5rem"},
                            ),
                            Text(
                                "Explore all the Radix UI components available in Refast",
                                class_name="text-lg text-muted-foreground",
                            ),
                        ],
                    ),
                    Column([ThemeSwitcher()]),
                ],
                justify="between",
            ),
            # Breadcrumb navigation
            Breadcrumb(
                class_name="mb-4",
                children=[
                    BreadcrumbList(
                        children=[
                            BreadcrumbItem(children=[BreadcrumbLink(label="Home", href="/")]),
                            BreadcrumbSeparator(),
                            BreadcrumbItem(
                                children=[BreadcrumbLink(label="Components", href="/components")]
                            ),
                            BreadcrumbSeparator(),
                            BreadcrumbItem(children=[BreadcrumbPage(label="Showcase")]),
                        ]
                    )
                ],
            ),
            # Tabs for different component categories
            Tabs(
                default_value="new",
                children=[
                    TabItem(value="controls", label="Controls"),
                    TabItem(value="navigation", label="Navigation"),
                    TabItem(value="overlays", label="Overlays"),
                    TabItem(value="utility", label="Utility"),
                ],
            ),
            Separator(class_name="my-6"),
            # Controls Section
            Card(
                class_name="mb-6",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Form Controls"),
                            CardDescription("Interactive form elements"),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=6,
                                children=[
                                    # Switch
                                    Row(
                                        justify="between",
                                        align="center",
                                        children=[
                                            Column(
                                                gap=1,
                                                children=[
                                                    Label("Email Notifications"),
                                                    Text(
                                                        "Receive emails about your account",
                                                        class_name="text-sm text-muted-foreground",
                                                    ),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                align="center",
                                                children=[
                                                    Text(
                                                        "ON" if notifications else "OFF",
                                                        id="switch-status",
                                                        class_name="text-sm",
                                                    ),
                                                    Switch(
                                                        default_checked=notifications,
                                                        on_change=ctx.callback(on_switch_change),
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Slider
                                    Column(
                                        gap=2,
                                        children=[
                                            Row(
                                                justify="between",
                                                children=[
                                                    Label("Volume"),
                                                    Text(
                                                        f"{volume}%",
                                                        id="slider-value",
                                                        class_name="text-sm",
                                                    ),
                                                ],
                                            ),
                                            Slider(
                                                default_value=[volume],
                                                max=100,
                                                step=1,
                                                on_value_change=ctx.callback(on_slider_change),
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Toggle Group
                                    Column(
                                        gap=2,
                                        children=[
                                            Label("Text Formatting", class_name="mb-4"),
                                            Row(
                                                [
                                                    ToggleGroup(
                                                        type="multiple",
                                                        default_value={"bold": True},
                                                        children=[
                                                            ToggleGroupItem(name="bold", label="B"),
                                                            ToggleGroupItem(
                                                                name="italic", label="I"
                                                            ),
                                                            ToggleGroupItem(
                                                                name="underline", label="U"
                                                            ),
                                                        ],
                                                        on_value_change=ctx.callback(
                                                            on_toggle_change
                                                        ),
                                                    ),
                                                    Spacer(size=2),
                                                    ToggleGroup(
                                                        type="multiple",
                                                        default_value={"home": True},
                                                        children=[
                                                            ToggleGroupItem(
                                                                name="back", icon="chevron-left"
                                                            ),
                                                            ToggleGroupItem(
                                                                name="home", icon="home"
                                                            ),
                                                            ToggleGroupItem(
                                                                name="forward", icon="chevron-right"
                                                            ),
                                                        ],
                                                        on_value_change=ctx.callback(
                                                            on_toggle_change
                                                        ),
                                                    ),
                                                ],
                                                justify="center",
                                                gap=4,
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Combobox
                                    Column(
                                        gap=2,
                                        children=[
                                            Label("Select Framework"),
                                            Combobox(
                                                placeholder="Choose a framework...",
                                                options=[
                                                    {"value": "react", "label": "React"},
                                                    {"value": "vue", "label": "Vue"},
                                                    {"value": "angular", "label": "Angular"},
                                                    {"value": "svelte", "label": "Svelte"},
                                                ],
                                                on_select=ctx.callback(dropdown_select),
                                            ),
                                            Separator(class_name="mt-4 mb-4"),
                                            Label(
                                                "You can select multiple options in this combobox."
                                            ),
                                            Combobox(
                                                placeholder="Choose frameworks...",
                                                options=[
                                                    {"value": "react", "label": "React"},
                                                    {"value": "vue", "label": "Vue"},
                                                    {"value": "angular", "label": "Angular"},
                                                    {"value": "svelte", "label": "Svelte"},
                                                ],
                                                multiselect=True,
                                                on_select=ctx.callback(dropdown_select),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Overlays Section
            Card(
                class_name="mb-6",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Overlays & Popups"),
                            CardDescription("Dialogs, sheets, popovers, and more"),
                        ]
                    ),
                    CardContent(
                        children=[
                            Row(
                                gap=4,
                                wrap=True,
                                children=[
                                    # Alert Dialog
                                    AlertDialog(
                                        children=[
                                            AlertDialogTrigger(
                                                as_child=True,
                                                children=Button(
                                                    label="Delete Item", variant="destructive"
                                                ),
                                            ),
                                            AlertDialogContent(
                                                children=[
                                                    AlertDialogHeader(
                                                        children=[
                                                            AlertDialogTitle(
                                                                title="Are you absolutely sure?"
                                                            ),
                                                            AlertDialogDescription(
                                                                description="This action cannot be undone. This will permanently delete your account and remove your data from our servers."
                                                            ),
                                                        ]
                                                    ),
                                                    AlertDialogFooter(
                                                        children=[
                                                            AlertDialogCancel(label="Cancel"),
                                                            AlertDialogAction(
                                                                label="Delete",
                                                                on_click=ctx.callback(
                                                                    on_confirm_delete
                                                                ),
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    # Sheet
                                    Sheet(
                                        children=[
                                            SheetTrigger(
                                                as_child=True,
                                                children=Button(
                                                    label="Open Settings", variant="outline"
                                                ),
                                            ),
                                            SheetContent(
                                                side="right",
                                                children=[
                                                    SheetHeader(
                                                        children=[
                                                            SheetTitle(title="Settings"),
                                                            SheetDescription(
                                                                description="Configure your preferences"
                                                            ),
                                                        ]
                                                    ),
                                                    Column(
                                                        gap=4,
                                                        class_name="py-4",
                                                        children=[
                                                            Input(placeholder="Name", name="name"),
                                                            Input(
                                                                placeholder="Email", name="email"
                                                            ),
                                                            Button(
                                                                label="Save Changes",
                                                                on_click=ctx.callback(
                                                                    on_sheet_save
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                    # Popover
                                    Popover(
                                        children=[
                                            PopoverTrigger(
                                                as_child=True,
                                                children=Button(
                                                    label="Quick Actions", variant="secondary"
                                                ),
                                            ),
                                            PopoverContent(
                                                children=[
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Text(
                                                                "Quick Actions",
                                                                class_name="font-semibold",
                                                            ),
                                                            Separator(),
                                                            Button(
                                                                label="Edit",
                                                                variant="ghost",
                                                                size="sm",
                                                            ),
                                                            Button(
                                                                label="Share",
                                                                variant="ghost",
                                                                size="sm",
                                                            ),
                                                            Button(
                                                                label="Archive",
                                                                variant="ghost",
                                                                size="sm",
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                    # HoverCard
                                    HoverCard(
                                        children=[
                                            HoverCardTrigger(
                                                children=Text(
                                                    "@refast",
                                                    class_name="text-primary cursor-pointer",
                                                    style={"textDecoration": "underline"},
                                                )
                                            ),
                                            HoverCardContent(
                                                children=[
                                                    Row(
                                                        gap=4,
                                                        children=[
                                                            Avatar(
                                                                src="https://github.com/shadcn.png",
                                                                alt="@refast",
                                                            ),
                                                            Column(
                                                                gap=1,
                                                                children=[
                                                                    Text(
                                                                        "Refast Framework",
                                                                        class_name="font-semibold",
                                                                    ),
                                                                    Text(
                                                                        "Python + React UI Framework",
                                                                        class_name="text-sm text-muted-foreground",
                                                                    ),
                                                                    Badge(text="Open Source"),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Utility Section
            Card(
                class_name="mb-6",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Utility Components"),
                            CardDescription("Layout helpers and utility components"),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=6,
                                children=[
                                    # Collapsible
                                    Collapsible(
                                        children=[
                                            Row(
                                                justify="between",
                                                align="center",
                                                children=[
                                                    Text(
                                                        "Advanced Options",
                                                        class_name="font-medium",
                                                    ),
                                                    CollapsibleTrigger(
                                                        children=Button(
                                                            label="Toggle",
                                                            variant="ghost",
                                                            size="sm",
                                                        )
                                                    ),
                                                ],
                                            ),
                                            CollapsibleContent(
                                                children=[
                                                    Card(
                                                        class_name="mt-2",
                                                        children=[
                                                            CardContent(
                                                                children=[
                                                                    Text(
                                                                        "Hidden content revealed!"
                                                                    ),
                                                                ]
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    Column(
                                        gap=2,
                                        children=[
                                            Label("Scroll Area Example"),
                                            ScrollArea(
                                                class_name="rounded-md border p-4",
                                                style={"height": "12rem", "width": "100%"},
                                                children=[
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Text(f"Item {i}") for i in range(1, 21)
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Aspect Ratio
                                    AspectRatio(
                                        ratio=16 / 9,
                                        class_name="bg-muted rounded-md",
                                        children=[
                                            Container(
                                                class_name="flex items-center justify-center",
                                                style={"height": "100%"},
                                                children=[Text("16:9 Content Area")],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            Column(
                                gap=2,
                                class_name="mt-6",
                                children=[
                                    Label(
                                        "Code Component",
                                    ),
                                    Code(
                                        code=dedent("""
                                import datetime

                                now = datetime.datetime.now()
                                print("Current date and time:", now)
                            """),
                                        inline=False,
                                        language="python",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # New Components Section (Image, Markdown, CheckboxGroup, RadioGroup)
            Card(
                class_name="mb-6",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("New Components"),
                            CardDescription("Image, Markdown, CheckboxGroup, and RadioGroup"),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=6,
                                children=[
                                    # Image Component
                                    Column(
                                        gap=2,
                                        children=[
                                            Label("Image Component"),
                                            Text(
                                                "Images with loading states and fallback support",
                                                class_name="text-sm text-muted-foreground mb-2",
                                            ),
                                            Row(
                                                gap=4,
                                                wrap=True,
                                                children=[
                                                    Column(
                                                        gap=1,
                                                        children=[
                                                            Image(
                                                                src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop",
                                                                alt="Mountain landscape",
                                                                width=300,
                                                                height=200,
                                                                fit="cover",
                                                                loading=True,
                                                                class_name="rounded-md",
                                                            ),
                                                            Text(
                                                                "With loading",
                                                                class_name="text-xs text-muted-foreground",
                                                            ),
                                                        ],
                                                    ),
                                                    Column(
                                                        gap=1,
                                                        children=[
                                                            Image(
                                                                src="https://invalid-url.example/broken.jpg",
                                                                alt="Fallback demo",
                                                                width=300,
                                                                height=200,
                                                                fallback_src="https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=300&h=200&fit=crop",
                                                                class_name="rounded-md",
                                                            ),
                                                            Text(
                                                                "With fallback",
                                                                class_name="text-xs text-muted-foreground",
                                                            ),
                                                        ],
                                                    ),
                                                    Column(
                                                        gap=1,
                                                        children=[
                                                            Image(
                                                                src="https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=300&h=200&fit=crop",
                                                                alt="Lake view",
                                                                width=300,
                                                                height=200,
                                                                fit="contain",
                                                                class_name="rounded-md bg-muted",
                                                            ),
                                                            Text(
                                                                "fit=contain",
                                                                class_name="text-xs text-muted-foreground",
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Markdown Component
                                    Column(
                                        gap=2,
                                        children=[
                                            Label("Markdown Component"),
                                            Text(
                                                "Rich text with GitHub Flavored Markdown and LaTeX support",
                                                class_name="text-sm text-muted-foreground mb-2",
                                            ),
                                            Card(
                                                class_name="p-4",
                                                children=[
                                                    Markdown(
                                                        content="""## Welcome to Refast! 🚀

This is **Markdown** with *full* formatting support:

- ✅ GitHub Flavored Markdown
- ✅ Code blocks with syntax highlighting
- ✅ LaTeX math equations

### Code Example

```python
from refast import RefastApp

app = RefastApp(title="My App")
```

### Math Support

Inline math: $E = mc^2$

Display math:

$$
\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}
$$

| Feature | Status |
|---------|--------|
| GFM | ✅ |
| LaTeX | ✅ |
| Tables | ✅ |
""",
                                                        allow_latex=True,
                                                        class_name="prose-sm",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # CheckboxGroup and RadioGroup
                                    Row(
                                        gap=8,
                                        wrap=True,
                                        children=[
                                            # CheckboxGroup
                                            Column(
                                                gap=2,
                                                children=[
                                                    Label("CheckboxGroup"),
                                                    Text(
                                                        "Select multiple options",
                                                        class_name="text-sm text-muted-foreground mb-2",
                                                    ),
                                                    CheckboxGroup(
                                                        name="toppings",
                                                        label="Pizza Toppings",
                                                        options=[
                                                            {
                                                                "value": "cheese",
                                                                "label": "Extra Cheese",
                                                            },
                                                            {
                                                                "value": "pepperoni",
                                                                "label": "Pepperoni",
                                                            },
                                                            {
                                                                "value": "mushrooms",
                                                                "label": "Mushrooms",
                                                            },
                                                            {
                                                                "value": "olives",
                                                                "label": "Olives",
                                                                "disabled": True,
                                                            },
                                                        ],
                                                        value=["cheese"],
                                                        orientation="vertical",
                                                        on_change=ctx.callback(
                                                            on_checkbox_group_change
                                                        ),
                                                    ),
                                                ],
                                            ),
                                            # RadioGroup
                                            Column(
                                                gap=2,
                                                children=[
                                                    Label("RadioGroup"),
                                                    Text(
                                                        "Select a single option",
                                                        class_name="text-sm text-muted-foreground mb-2",
                                                    ),
                                                    RadioGroup(
                                                        name="size",
                                                        label="Pizza Size",
                                                        options=[
                                                            {
                                                                "value": "small",
                                                                "label": 'Small (10")',
                                                            },
                                                            {
                                                                "value": "medium",
                                                                "label": 'Medium (12")',
                                                            },
                                                            {
                                                                "value": "large",
                                                                "label": 'Large (14")',
                                                            },
                                                            {
                                                                "value": "xlarge",
                                                                "label": 'X-Large (16")',
                                                                "disabled": True,
                                                            },
                                                        ],
                                                        value="medium",
                                                        orientation="vertical",
                                                        on_change=ctx.callback(
                                                            on_radio_group_change
                                                        ),
                                                    ),
                                                ],
                                            ),
                                            # Horizontal RadioGroup
                                            Column(
                                                gap=2,
                                                children=[
                                                    Label("Horizontal RadioGroup"),
                                                    Text(
                                                        "Options in a row",
                                                        class_name="text-sm text-muted-foreground mb-2",
                                                    ),
                                                    RadioGroup(
                                                        name="priority",
                                                        label="Priority Level",
                                                        options=[
                                                            {"value": "low", "label": "Low"},
                                                            {"value": "medium", "label": "Medium"},
                                                            {"value": "high", "label": "High"},
                                                        ],
                                                        value="medium",
                                                        orientation="horizontal",
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
            # Pagination
            Row(
                justify="center",
                class_name="mt-8",
                children=[
                    render_pagination(ctx, current_page),
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
