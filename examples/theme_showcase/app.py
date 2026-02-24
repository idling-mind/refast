"""Theme Showcase Example — Demonstrates Refast theming & customization.

This example demonstrates:
- Applying a built-in theme preset at startup
- Switching themes at runtime with ctx.set_theme()
- Custom CSS (inline snippets and external URLs)
- Custom JavaScript injection
- Extra <head> tags (meta, preconnect)
- Favicon
- The add_css() / add_js() / add_head_tag() helpers

Run:
    uvicorn examples.theme_showcase.app:app --reload
"""

from fastapi import FastAPI
from theme_util import shadcn_registry_to_theme_from_url
from themes.northern_lights import northern_lights

from refast import Context, RefastApp
from refast.components import (
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
    AspectRatio,
    Avatar,
    Badge,
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
    DatePicker,
    Dialog,
    DialogAction,
    DialogCancel,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    Drawer,
    DrawerContent,
    DrawerDescription,
    DrawerHeader,
    DrawerTitle,
    DrawerTrigger,
    Heading,
    HoverCard,
    HoverCardContent,
    HoverCardTrigger,
    Image,
    Input,
    InputWrapper,
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
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
    Row,
    ScrollArea,
    Separator,
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
    Slider,
    Switch,
    TabItem,
    Tabs,
    Text,
    ToggleGroup,
    ToggleGroupItem,
)
from refast.components.shadcn import Alert, ThemeSwitcher
from refast.components.shadcn.charts import (
    Area,
    AreaChart,
    Bar,
    BarChart,
    CartesianGrid,
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
    Line,
    LineChart,
    Pie,
    PieChart,
    XAxis,
    YAxis,
)
from refast.components.shadcn.input import Textarea
from refast.theme import (
    THEMES,
    Theme,
    ThemeColors,
    default_theme,
)

# ── A fully custom theme to show ThemeColors usage ───────────────────────

custom_teal_theme = Theme(
    light=ThemeColors(
        background="180 20% 99%",
        foreground="180 50% 5%",
        primary="174 72% 40%",
        primary_foreground="180 20% 99%",
        secondary="174 30% 92%",
        secondary_foreground="174 50% 10%",
        muted="174 20% 95%",
        muted_foreground="174 15% 45%",
        accent="174 30% 92%",
        accent_foreground="174 50% 10%",
        border="174 20% 88%",
        ring="174 72% 40%",
    ),
    dark=ThemeColors(
        background="180 30% 5%",
        foreground="174 20% 95%",
        primary="174 65% 50%",
        primary_foreground="180 30% 5%",
        secondary="174 20% 14%",
        secondary_foreground="174 20% 95%",
        muted="174 20% 14%",
        muted_foreground="174 15% 60%",
        accent="174 20% 14%",
        accent_foreground="174 20% 95%",
        border="174 20% 14%",
        ring="174 65% 50%",
        card="180 20% 5%",
    ),
    font_family="'Segoe UI', system-ui, sans-serif",
    radius="0.75rem",
)

THEMES["Custom Teal"] = custom_teal_theme
THEMES["Northern Lights"] = northern_lights
web_themes = [
    "bubblegum",
    "amethyst-haze",
    "catppuccin",
    "amber-minimal",
    "tangerine",
    "supabase",
    "clean-slate",
    "darkmatter",
    "notebook",
]
for name in web_themes:
    url = f"https://tweakcn.com/r/themes/{name}.json"
    try:
        theme = shadcn_registry_to_theme_from_url(url)
        THEMES[name.title()] = theme
    except Exception as e:
        print(f"Error fetching theme from {url}: {e}")

# ── Create the Refast app with theming + customization ───────────────────

ui = RefastApp(
    title="Theme Showcase",
    # Start with the rose preset
    theme=default_theme,
    # Favicon
    favicon="https://fav.farm/🎨",
    # Custom CSS – inline snippet to add a subtle gradient to the page
    custom_css=[
        """
        .theme-showcase-gradient {
            background: linear-gradient(
                135deg,
                hsl(var(--primary) / 0.03) 0%,
                transparent 50%
            );
        }
        .swatch {
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .swatch:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px hsl(var(--primary) / 0.2);
        }
        """,
    ],
    # Custom JS – log theme changes
    custom_js=[
        "console.log('[Theme Showcase] App loaded with custom JS injection');",
    ],
    # Extra <head> tags
    head_tags=[
        '<meta name="description" content="Refast Theme Showcase – demonstrates theming & customization">',
        '<meta name="theme-color" content="#e11d48">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">',
    ],
)

# Add more assets programmatically. Required by some of the themes showcased below.
ui.add_head_tag(
    '<link href="https://fonts.googleapis.com/css2?family=Architects+Daughter&display=swap" rel="stylesheet">'
)
ui.add_head_tag(
    '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap" rel="stylesheet">'
)
ui.add_head_tag(
    '<link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">'
)


# ── Callbacks ────────────────────────────────────────────────────────────


async def apply_preset(ctx: Context, theme: str = "", **kwargs):
    """Apply a theme preset by name."""
    print(f"Applying preset: {theme}, {kwargs}")
    theme_obj = THEMES.get(theme)
    if theme_obj is None:
        await ctx.show_toast(f"Unknown theme: {theme}", variant="error")
        return

    await ctx.set_theme(theme_obj)
    ctx.state.set("current_theme", theme)
    await ctx.refresh("/")
    await ctx.show_toast(f"Theme switched to {theme}", variant="success")


async def apply_custom_primary(ctx: Context, custom_primary: str = "", **kwargs):
    """Build a quick theme with a user-supplied primary HSL value."""
    custom_primary = custom_primary.strip()
    if not custom_primary:
        await ctx.show_toast("Enter an HSL value like  262 83% 58%", variant="warning")
        return

    theme = Theme(
        light=ThemeColors(primary=custom_primary, ring=custom_primary),
        dark=ThemeColors(primary=custom_primary, ring=custom_primary),
    )
    await ctx.set_theme(theme)
    ctx.state.set("current_theme", f"Custom ({custom_primary})")
    await ctx.refresh("/")
    await ctx.show_toast(f"Primary colour set to: {custom_primary}", variant="success")


async def on_switch_change(ctx: Context):
    """Handle switch toggle."""
    current = ctx.state.get("notifications", False)
    ctx.state.set("notifications", not current)
    await ctx.update_text("switch-status", "ON" if not current else "OFF")


async def on_slider_change(ctx: Context):
    """Handle slider change."""
    value = ctx.event_data[0]
    ctx.state.set("volume", value)
    await ctx.update_text("slider-value", f"{value}%")


async def on_toggle_change(ctx: Context):
    """Handle text formatting toggle."""
    formats = ctx.event_data
    active = [k for k, v in formats.items() if v]
    msg = f"Active formats: {', '.join(active)}" if active else "No formats active"
    await ctx.show_toast(msg, variant="info")


async def on_accordion_change(ctx: Context):
    """Handle accordion value change and update status text."""
    value = ctx.event_data.get("value", "")
    if isinstance(value, list):
        display = ", ".join(value)
    else:
        display = value or "None"
    await ctx.update_text("accordion-status", f"Open: {display}")


async def on_checkbox_group_change(ctx: Context):
    """Handle checkbox group selection change."""
    selected = ctx.event_data
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
    if "value" in ctx.event_data:
        selection = ctx.event_data.get("value", "")
    else:
        selection = ", ".join(ctx.event_data.values())
    await ctx.show_toast(f"Selected: {selection}", variant="info")


async def on_page_change(ctx: Context, page: int):
    """Handle pagination."""
    ctx.state.set("current_page", page)
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


# ── Page ─────────────────────────────────────────────────────────────────


@ui.page("/")
def home(ctx: Context):
    current = ctx.state.get("current_theme", "Rose")
    notifications = ctx.state.get("notifications", False)
    volume = ctx.state.get("volume", 50)
    current_page = ctx.state.get("current_page", 1)

    # Sample chart data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    chart_data = [
        {"month": month, "desktop": 100 + i * 50, "mobile": 80 + i * 30}
        for i, month in enumerate(months)
    ]
    pie_data = [
        {"browser": "Chrome", "visitors": 275, "fill": "hsl(var(--chart-1))"},
        {"browser": "Safari", "visitors": 200, "fill": "hsl(var(--chart-2))"},
        {"browser": "Firefox", "visitors": 187, "fill": "hsl(var(--chart-3))"},
        {"browser": "Edge", "visitors": 173, "fill": "hsl(var(--chart-4))"},
    ]

    return Container(
        class_name="theme-showcase-gradient min-h-screen",
        children=[
            Container(
                class_name="w-full py-6 px-6",
                children=[
                    # ── Header ─────────────────────────────────────
                    Row(
                        justify="between",
                        align="center",
                        class_name="mb-8",
                        children=[
                            Column(
                                children=[
                                    Heading(
                                        text="🎨 Theme Showcase",
                                        level=1,
                                        class_name="text-4xl font-bold tracking-tight",
                                    ),
                                    Text(
                                        "Demonstrates Refast theming, custom CSS, custom JS, and head tag injection.",
                                        class_name="text-muted-foreground mt-1",
                                    ),
                                ]
                            ),
                            ThemeSwitcher(mode="dropdown"),
                        ],
                    ),
                    # ── Current theme badge ────────────────────────
                    Row(
                        gap=2,
                        align="center",
                        class_name="mb-6",
                        children=[
                            Text("Active theme:", class_name="text-sm text-muted-foreground"),
                            Badge(current, variant="default"),
                        ],
                    ),
                    # ── Preset selector ────────────────────────────
                    Card(
                        class_name="mb-6",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Switch Theme Preset"),
                                    CardDescription(
                                        "Pick a built-in preset. The theme is applied at runtime "
                                        "via WebSocket — no page reload needed."
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Row(
                                        gap=2,
                                        class_name="flex-wrap",
                                        children=[
                                            Button(
                                                name,
                                                variant="outline" if name != current else "primary",
                                                size="sm",
                                                on_click=ctx.callback(apply_preset, theme=name),
                                            )
                                            for name in THEMES
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                    # ── Custom primary colour ──────────────────────
                    Card(
                        class_name="mb-6",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Custom Primary Colour"),
                                    CardDescription(
                                        "Enter an HSL triplet (e.g. 262 83% 58%) and hit Apply. "
                                        "This builds a Theme on-the-fly."
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Row(
                                        gap=2,
                                        align="end",
                                        children=[
                                            Column(
                                                class_name="flex-1",
                                                children=[
                                                    Input(
                                                        name="custom_primary",
                                                        placeholder="262 83% 58%",
                                                        on_change=ctx.save_prop("custom_primary"),
                                                    ),
                                                ],
                                            ),
                                            Button(
                                                "Apply",
                                                on_click=ctx.callback(
                                                    apply_custom_primary,
                                                    props=["custom_primary"],
                                                ),
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                    Separator(class_name="my-6"),
                    # ── Component showcase sections ────────────────
                    Heading(
                        text="Complete Component Gallery",
                        level=2,
                        class_name="text-2xl font-semibold mb-4",
                    ),
                    Text(
                        "All components rendered with the active theme.",
                        class_name="text-muted-foreground mb-6",
                    ),
                    # Grid layout for cards
                    Container(
                        class_name="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4",
                        children=[
                            # Charts Section
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Area Chart"),
                                            CardDescription("Desktop vs Mobile visitors"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            ChartContainer(
                                                config={
                                                    "desktop": ChartConfig(
                                                        label="Desktop",
                                                        color="hsl(var(--chart-1))",
                                                    ),
                                                    "mobile": ChartConfig(
                                                        label="Mobile",
                                                        color="hsl(var(--chart-2))",
                                                    ),
                                                },
                                                min_height=250,
                                                children=AreaChart(
                                                    data=chart_data,
                                                    children=[
                                                        CartesianGrid(vertical=False),
                                                        XAxis(data_key="month", tick_line=False),
                                                        ChartTooltip(
                                                            content=ChartTooltipContent(
                                                                indicator="dot"
                                                            )
                                                        ),
                                                        Area(
                                                            data_key="mobile",
                                                            fill="var(--color-mobile)",
                                                            stroke="var(--color-mobile)",
                                                        ),
                                                        Area(
                                                            data_key="desktop",
                                                            fill="var(--color-desktop)",
                                                            stroke="var(--color-desktop)",
                                                        ),
                                                    ],
                                                ),
                                            )
                                        ]
                                    ),
                                ],
                            ),
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Bar Chart"),
                                            CardDescription("Monthly comparison"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            ChartContainer(
                                                config={
                                                    "desktop": ChartConfig(
                                                        label="Desktop",
                                                        color="hsl(var(--chart-1))",
                                                    ),
                                                    "mobile": ChartConfig(
                                                        label="Mobile",
                                                        color="hsl(var(--chart-2))",
                                                    ),
                                                },
                                                min_height=250,
                                                children=BarChart(
                                                    data=chart_data,
                                                    children=[
                                                        CartesianGrid(vertical=False),
                                                        XAxis(data_key="month", tick_line=False),
                                                        ChartTooltip(
                                                            content=ChartTooltipContent(
                                                                indicator="dashed"
                                                            )
                                                        ),
                                                        Bar(
                                                            data_key="desktop",
                                                            fill="var(--color-desktop)",
                                                        ),
                                                        Bar(
                                                            data_key="mobile",
                                                            fill="var(--color-mobile)",
                                                        ),
                                                    ],
                                                ),
                                            )
                                        ]
                                    ),
                                ],
                            ),
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Line Chart"),
                                            CardDescription("Trend over time"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            ChartContainer(
                                                config={
                                                    "desktop": ChartConfig(
                                                        label="Desktop",
                                                        color="hsl(var(--chart-1))",
                                                    ),
                                                },
                                                min_height=250,
                                                children=LineChart(
                                                    data=chart_data,
                                                    children=[
                                                        CartesianGrid(vertical=False),
                                                        XAxis(data_key="month", tick_line=False),
                                                        ChartTooltip(
                                                            content=ChartTooltipContent(
                                                                indicator="line"
                                                            )
                                                        ),
                                                        Line(
                                                            data_key="desktop",
                                                            stroke="var(--color-desktop)",
                                                            stroke_width=2,
                                                        ),
                                                    ],
                                                ),
                                            )
                                        ]
                                    ),
                                ],
                            ),
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Pie Chart"),
                                            CardDescription("Browser market share"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            ChartContainer(
                                                config={
                                                    "chrome": ChartConfig(
                                                        label="Chrome",
                                                        color="hsl(var(--chart-1))",
                                                    ),
                                                    "safari": ChartConfig(
                                                        label="Safari",
                                                        color="hsl(var(--chart-2))",
                                                    ),
                                                    "firefox": ChartConfig(
                                                        label="Firefox",
                                                        color="hsl(var(--chart-3))",
                                                    ),
                                                    "edge": ChartConfig(
                                                        label="Edge",
                                                        color="hsl(var(--chart-4))",
                                                    ),
                                                },
                                                min_height=250,
                                                children=PieChart(
                                                    children=[
                                                        ChartTooltip(
                                                            content=ChartTooltipContent(
                                                                hideLabel=True
                                                            )
                                                        ),
                                                        Pie(
                                                            data=pie_data,
                                                            data_key="visitors",
                                                            name_key="browser",
                                                        ),
                                                    ],
                                                ),
                                            )
                                        ]
                                    ),
                                ],
                            ),
                            # Accordion
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Accordion"),
                                            CardDescription("Collapsible content sections"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Column(
                                                gap=4,
                                                children=[
                                                    Text(
                                                        "Open: None",
                                                        id="accordion-status",
                                                        class_name="text-sm mb-2",
                                                    ),
                                                    Accordion(
                                                        default_value=None,
                                                        type="single",
                                                        collapsible=True,
                                                        on_value_change=ctx.callback(
                                                            on_accordion_change
                                                        ),
                                                        children=[
                                                            AccordionItem(
                                                                value="item-1",
                                                                children=[
                                                                    AccordionTrigger(
                                                                        children=["Section One"]
                                                                    ),
                                                                    AccordionContent(
                                                                        children=[
                                                                            Text(
                                                                                "Content for the first section goes here."
                                                                            )
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                            AccordionItem(
                                                                value="item-2",
                                                                children=[
                                                                    AccordionTrigger(
                                                                        children=["Section Two"]
                                                                    ),
                                                                    AccordionContent(
                                                                        children=[
                                                                            Text(
                                                                                "Content for the second section goes here."
                                                                            )
                                                                        ]
                                                                    ),
                                                                ],
                                                            ),
                                                            AccordionItem(
                                                                value="item-3",
                                                                children=[
                                                                    AccordionTrigger(
                                                                        children=["Section Three"]
                                                                    ),
                                                                    AccordionContent(
                                                                        children=[
                                                                            Text(
                                                                                "Content for the third section goes here."
                                                                            )
                                                                        ]
                                                                    ),
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
                            # Breadcrumb
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Breadcrumb"),
                                            CardDescription("Navigation breadcrumbs"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Breadcrumb(
                                                children=[
                                                    BreadcrumbList(
                                                        children=[
                                                            BreadcrumbItem(
                                                                children=[
                                                                    BreadcrumbLink(
                                                                        label="Home", href="/"
                                                                    )
                                                                ]
                                                            ),
                                                            BreadcrumbSeparator(),
                                                            BreadcrumbItem(
                                                                children=[
                                                                    BreadcrumbLink(
                                                                        label="Theme", href="/theme"
                                                                    )
                                                                ]
                                                            ),
                                                            BreadcrumbSeparator(),
                                                            BreadcrumbItem(
                                                                children=[
                                                                    BreadcrumbPage(label="Showcase")
                                                                ]
                                                            ),
                                                        ]
                                                    )
                                                ],
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            # Tabs
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Tabs"),
                                            CardDescription("Tabbed content sections"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Tabs(
                                                default_value="tab1",
                                                children=[
                                                    TabItem(value="tab1", label="Overview"),
                                                    TabItem(value="tab2", label="Features"),
                                                    TabItem(value="tab3", label="Settings"),
                                                ],
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            # Form Controls
                            Card(
                                class_name="col-span-1 lg:col-span-2 xl:col-span-3",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Form Controls"),
                                            CardDescription("Interactive input elements"),
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
                                                                        "ON"
                                                                        if notifications
                                                                        else "OFF",
                                                                        id="switch-status",
                                                                        class_name="text-sm",
                                                                    ),
                                                                    Switch(
                                                                        default_checked=notifications,
                                                                        on_change=ctx.callback(
                                                                            on_switch_change
                                                                        ),
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(),
                                                    # Text Inputs
                                                    Column(
                                                        gap=4,
                                                        children=[
                                                            Input(
                                                                name="name",
                                                                label="Name",
                                                                description="Your full name",
                                                                placeholder="John Doe",
                                                                type="text",
                                                            ),
                                                            Input(
                                                                name="email",
                                                                label="Email",
                                                                description="Your email address",
                                                                placeholder="john@example.com",
                                                                type="email",
                                                            ),
                                                            InputWrapper(
                                                                label="Date of Birth",
                                                                description="Select your birth date",
                                                                children=[
                                                                    DatePicker(
                                                                        placeholder="Pick a date",
                                                                        caption_layout="dropdown",
                                                                    ),
                                                                ],
                                                            ),
                                                            Textarea(
                                                                name="message",
                                                                label="Message",
                                                                description="Enter your message",
                                                                placeholder="Type something...",
                                                                rows=3,
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
                                                                on_value_change=ctx.callback(
                                                                    on_slider_change
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(),
                                                    # Toggle Group
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Label("Text Formatting"),
                                                            Row(
                                                                gap=4,
                                                                justify="center",
                                                                children=[
                                                                    ToggleGroup(
                                                                        type="multiple",
                                                                        default_value={
                                                                            "bold": True
                                                                        },
                                                                        children=[
                                                                            ToggleGroupItem(
                                                                                name="bold",
                                                                                label="B",
                                                                            ),
                                                                            ToggleGroupItem(
                                                                                name="italic",
                                                                                label="I",
                                                                            ),
                                                                            ToggleGroupItem(
                                                                                name="underline",
                                                                                label="U",
                                                                            ),
                                                                        ],
                                                                        on_value_change=ctx.callback(
                                                                            on_toggle_change
                                                                        ),
                                                                    ),
                                                                    ToggleGroup(
                                                                        type="multiple",
                                                                        children=[
                                                                            ToggleGroupItem(
                                                                                name="back",
                                                                                icon="chevron-left",
                                                                            ),
                                                                            ToggleGroupItem(
                                                                                name="home",
                                                                                icon="home",
                                                                            ),
                                                                            ToggleGroupItem(
                                                                                name="forward",
                                                                                icon="chevron-right",
                                                                            ),
                                                                        ],
                                                                        on_value_change=ctx.callback(
                                                                            on_toggle_change
                                                                        ),
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(),
                                                    # Combobox
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Combobox(
                                                                label="Select a framework",
                                                                description="Single select combobox",
                                                                placeholder="Choose...",
                                                                options=[
                                                                    {
                                                                        "value": "react",
                                                                        "label": "React",
                                                                    },
                                                                    {
                                                                        "value": "vue",
                                                                        "label": "Vue",
                                                                    },
                                                                    {
                                                                        "value": "angular",
                                                                        "label": "Angular",
                                                                    },
                                                                    {
                                                                        "value": "svelte",
                                                                        "label": "Svelte",
                                                                    },
                                                                ],
                                                                on_select=ctx.callback(
                                                                    dropdown_select
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(),
                                                    # CheckboxGroup and RadioGroup
                                                    Row(
                                                        gap=8,
                                                        wrap=True,
                                                        children=[
                                                            Column(
                                                                gap=2,
                                                                children=[
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
                                                                        ],
                                                                        value=["cheese"],
                                                                        orientation="vertical",
                                                                        on_change=ctx.callback(
                                                                            on_checkbox_group_change
                                                                        ),
                                                                    ),
                                                                ],
                                                            ),
                                                            Column(
                                                                gap=2,
                                                                children=[
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
                                                                        ],
                                                                        value="medium",
                                                                        orientation="vertical",
                                                                        on_change=ctx.callback(
                                                                            on_radio_group_change
                                                                        ),
                                                                    ),
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
                            # Overlays
                            Card(
                                class_name="col-span-1 lg:col-span-2",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Overlays & Popups"),
                                            CardDescription("Dialogs, sheets, and popovers"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Row(
                                                gap=4,
                                                wrap=True,
                                                children=[
                                                    Dialog(
                                                        children=[
                                                            DialogTrigger(
                                                                as_child=True,
                                                                children=Button(
                                                                    label="Delete Item",
                                                                    variant="destructive",
                                                                ),
                                                            ),
                                                            DialogContent(
                                                                children=[
                                                                    DialogHeader(
                                                                        children=[
                                                                            DialogTitle(
                                                                                title="Are you sure?"
                                                                            ),
                                                                            DialogDescription(
                                                                                description="This action cannot be undone."
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    DialogFooter(
                                                                        children=[
                                                                            DialogCancel(
                                                                                label="Cancel"
                                                                            ),
                                                                            DialogAction(
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
                                                    Sheet(
                                                        children=[
                                                            SheetTrigger(
                                                                as_child=True,
                                                                children=Button(
                                                                    label="Settings",
                                                                    variant="outline",
                                                                ),
                                                            ),
                                                            SheetContent(
                                                                side="right",
                                                                children=[
                                                                    SheetHeader(
                                                                        children=[
                                                                            SheetTitle(
                                                                                title="Settings"
                                                                            ),
                                                                            SheetDescription(
                                                                                description="Configure preferences"
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    Column(
                                                                        gap=4,
                                                                        class_name="py-4",
                                                                        children=[
                                                                            Input(
                                                                                placeholder="Name",
                                                                                name="name",
                                                                            ),
                                                                            Button(
                                                                                label="Save",
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
                                                    Popover(
                                                        children=[
                                                            PopoverTrigger(
                                                                as_child=True,
                                                                children=Button(
                                                                    label="Quick Actions",
                                                                    variant="secondary",
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
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                    HoverCard(
                                                        children=[
                                                            HoverCardTrigger(
                                                                children=Text(
                                                                    "@refast",
                                                                    class_name="text-primary cursor-pointer underline",
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
                                                                                        "Refast",
                                                                                        class_name="font-semibold",
                                                                                    ),
                                                                                    Text(
                                                                                        "Python + React",
                                                                                        class_name="text-sm text-muted-foreground",
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                    Drawer(
                                                        children=[
                                                            DrawerTrigger(Button("Drawer")),
                                                            DrawerContent(
                                                                [
                                                                    DrawerHeader(
                                                                        [
                                                                            DrawerTitle(
                                                                                "Drawer Title"
                                                                            ),
                                                                            DrawerDescription(
                                                                                "Drawer content goes here"
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    Container(
                                                                        [
                                                                            Text(
                                                                                "Drawer body content"
                                                                            )
                                                                        ],
                                                                        class_name="p-4",
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            # Utility Components
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Utility Components"),
                                            CardDescription("Layout and utility elements"),
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
                                                                                        "Hidden content!"
                                                                                    ),
                                                                                ],
                                                                                class_name="p-4",
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(),
                                                    # Scroll Area
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Label("Scroll Area"),
                                                            ScrollArea(
                                                                class_name="rounded-md border p-4",
                                                                style={
                                                                    "height": "150px",
                                                                    "width": "100%",
                                                                },
                                                                children=[
                                                                    Column(
                                                                        gap=2,
                                                                        children=[
                                                                            Text(f"Item {i}")
                                                                            for i in range(1, 15)
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(),
                                                    # Aspect Ratio
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Label("Aspect Ratio (16:9)"),
                                                            AspectRatio(
                                                                ratio=16 / 9,
                                                                class_name="bg-muted rounded-md",
                                                                children=[
                                                                    Container(
                                                                        class_name="flex items-center justify-center h-full",
                                                                        children=[
                                                                            Text("16:9 Content")
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(),
                                                    # Code
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Label("Code Component"),
                                                            Code(
                                                                code='print("Hello from Refast!")',
                                                                inline=False,
                                                                show_line_numbers=True,
                                                                language="python",
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            # Image and Markdown
                            Card(
                                class_name="col-span-1 lg:col-span-2",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Media Components"),
                                            CardDescription("Images and formatted text"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Column(
                                                gap=6,
                                                children=[
                                                    # Images
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Label("Images"),
                                                            Row(
                                                                gap=4,
                                                                wrap=True,
                                                                justify="center",
                                                                children=[
                                                                    Image(
                                                                        src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200&h=150&fit=crop",
                                                                        alt="Mountain",
                                                                        width=200,
                                                                        height=150,
                                                                        object_fit="cover",
                                                                        class_name="rounded-md",
                                                                    ),
                                                                    Image(
                                                                        src="https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=200&h=150&fit=crop",
                                                                        alt="Nature",
                                                                        width=200,
                                                                        height=150,
                                                                        object_fit="cover",
                                                                        class_name="rounded-md",
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Separator(),
                                                    # Markdown
                                                    Column(
                                                        gap=2,
                                                        children=[
                                                            Label("Markdown"),
                                                            Card(
                                                                class_name="p-4",
                                                                children=[
                                                                    Markdown(
                                                                        content="""## Theme Showcase

This is **Markdown** with *full* formatting:

- ✅ Lists
- ✅ Code blocks
- ✅ Math: $E = mc^2$

```python
from refast import RefastApp
app = RefastApp()
```
""",
                                                                        allow_latex=True,
                                                                        class_name="prose-sm",
                                                                    ),
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
                            # Pagination
                            Card(
                                class_name="col-span-1",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Pagination"),
                                            CardDescription("Page navigation controls"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Row(
                                                justify="center",
                                                children=[render_pagination(ctx, current_page)],
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            # Resizable Panels
                            Card(
                                class_name="col-span-1 lg:col-span-2",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Resizable Panels"),
                                            CardDescription("Adjustable layout panels"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            ResizablePanelGroup(
                                                direction="horizontal",
                                                children=[
                                                    ResizablePanel(
                                                        min_size=20,
                                                        default_size=50,
                                                        children=[Text("Panel 1")],
                                                        class_name="bg-muted/50 p-4 rounded-l-lg",
                                                    ),
                                                    ResizableHandle(with_handle=True),
                                                    ResizablePanel(
                                                        min_size=20,
                                                        default_size=50,
                                                        children=[Text("Panel 2")],
                                                        class_name="bg-muted/50 p-4 rounded-r-lg",
                                                    ),
                                                ],
                                                class_name="border rounded-lg",
                                                style={"height": "200px", "width": "100%"},
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Separator(class_name="my-6"),
                    # ── Colour swatches ────────────────────────────
                    Heading(
                        text="Semantic Colour Tokens",
                        level=2,
                        class_name="text-2xl font-semibold mb-4",
                    ),
                    Text(
                        "These swatches update live when you switch themes.",
                        class_name="text-muted-foreground mb-4",
                    ),
                    _color_swatches(),
                    Separator(class_name="my-6"),
                    # ── Component preview ──────────────────────────
                    Heading(
                        text="Component Preview", level=2, class_name="text-2xl font-semibold mb-4"
                    ),
                    Text(
                        "Standard components styled by the active theme.",
                        class_name="text-muted-foreground mb-4",
                    ),
                    _component_preview(ctx),
                    Separator(class_name="my-6"),
                    # ── What's injected ────────────────────────────
                    Heading(
                        text="What's in the HTML", level=2, class_name="text-2xl font-semibold mb-4"
                    ),
                    _injection_info(),
                ],
            ),
        ],
    )


# ── Helpers ──────────────────────────────────────────────────────────────


def _swatch(label: str, bg_class: str, fg_class: str) -> Container:
    """A single colour swatch."""
    return Container(
        class_name=f"swatch {bg_class} {fg_class} rounded-lg p-2 border border-border flex items-center justify-center",
        style={"width": "120px"},
        children=[
            Text(label, class_name="text-xs font-mono font-semibold"),
        ],
    )


def _color_swatches() -> Row:
    """Grid of semantic colour swatches."""
    swatches = [
        ("background", "bg-background", "text-foreground"),
        ("primary", "bg-primary", "text-primary-foreground"),
        ("secondary", "bg-secondary", "text-secondary-foreground"),
        ("muted", "bg-muted", "text-muted-foreground"),
        ("accent", "bg-accent", "text-accent-foreground"),
        ("destructive", "bg-destructive", "text-destructive-foreground"),
        ("card", "bg-card", "text-card-foreground"),
        ("border", "bg-border", "text-foreground"),
    ]
    return Row(
        gap=3,
        class_name="flex-wrap mb-4",
        children=[_swatch(label, bg, fg) for label, bg, fg in swatches],
    )


def _component_preview(ctx: Context) -> Column:
    """A set of themed components for visual confirmation."""
    return Column(
        gap=4,
        children=[
            Row(
                gap=2,
                class_name="flex-wrap",
                children=[
                    Button("Primary", variant="primary"),
                    Button("Secondary", variant="secondary"),
                    Button("Outline", variant="outline"),
                    Button("Ghost", variant="ghost"),
                    Button("Destructive", variant="destructive"),
                ],
            ),
            Row(
                gap=2,
                class_name="flex-wrap",
                children=[
                    Badge("Badge", variant="default"),
                    Badge("Secondary", variant="secondary"),
                    Badge("Outline", variant="outline"),
                    Badge("Destructive", variant="destructive"),
                ],
            ),
            Row(
                gap=4,
                class_name="flex-wrap",
                children=[
                    Alert(
                        title="Heads up!",
                        description="This alert inherits the current theme colours.",
                        class_name="flex-1 min-w-[200px]",
                    ),
                    Card(
                        class_name="flex-1 min-w-[200px]",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Card Title"),
                                    CardDescription("Card description inherits muted-foreground."),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Text("Card body text uses the foreground colour."),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _injection_info() -> Column:
    """Describes what extra HTML was injected."""
    items = [
        "✅  Theme CSS variables — <style data-refast-theme> block in <head>",
        '✅  Favicon — <link rel="icon"> pointing to an emoji favicon',
        "✅  Custom CSS — inline <style> with .theme-showcase-gradient and .swatch hover effect",
        "✅  Custom JS — console.log() runs on page load (check DevTools)",
        '✅  Head tags — <meta name="description"> and <meta name="theme-color">',
        '✅  Programmatic — <link rel="preconnect"> added via ui.add_head_tag()',
    ]
    return Column(
        gap=2,
        children=[Text(item, class_name="text-sm text-muted-foreground") for item in items],
    )


# ── Mount ────────────────────────────────────────────────────────────────

app = FastAPI(title="Theme Showcase")
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
