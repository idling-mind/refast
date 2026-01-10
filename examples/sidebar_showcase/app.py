"""
Sidebar Showcase Example

This example demonstrates all the sidebar component features:
- SidebarProvider for state management
- Different sidebar variants (sidebar, floating, inset)
- Different collapsible modes (offcanvas, icon, none)
- Left and right side positioning
- Menu items with icons, badges, and actions
- Nested submenus
- Header and footer sections
- Keyboard shortcuts (Ctrl/Cmd+B to toggle)
- Mobile responsiveness
"""
from fastapi import FastAPI

from refast import RefastApp
from refast.components import (
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Container,
    Flex,
    Heading,
    Separator,
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupAction,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarInset,
    SidebarMenu,
    SidebarMenuAction,
    SidebarMenuBadge,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarMenuSub,
    SidebarMenuSubButton,
    SidebarMenuSubItem,
    SidebarProvider,
    SidebarRail,
    SidebarSeparator,
    SidebarTrigger,
    Stack,
    Text,
)

ui = RefastApp(title="Sidebar Showcase")

async def test_callback(ctx):
    await ctx.show_toast("Button clicked!", variant="success")

# Sample menu data
MAIN_MENU = [
    {"label": "Dashboard", "icon": "🏠", "href": "#dashboard", "badge": None},
    {"label": "Inbox", "icon": "📥", "href": "#inbox", "badge": "24"},
    {"label": "Calendar", "icon": "📅", "href": "#calendar", "badge": None},
    {"label": "Search", "icon": "🔍", "href": "#search", "badge": None},
    {"label": "Settings", "icon": "⚙️", "href": "#settings", "badge": None},
]

PROJECTS = [
    {"label": "Project Alpha", "icon": "📁", "href": "#alpha"},
    {"label": "Project Beta", "icon": "📁", "href": "#beta"},
    {"label": "Project Gamma", "icon": "📁", "href": "#gamma"},
]

SETTINGS_MENU = [
    {
        "label": "Settings",
        "icon": "⚙️",
        "submenu": [
            {"label": "General", "href": "#general"},
            {"label": "Security", "href": "#security"},
            {"label": "Notifications", "href": "#notifications"},
        ],
    },
]


def create_sidebar(
    ctx,
    active_item: str = "Dashboard",
    variant: str = "sidebar",
    collapsible: str = "icon",
    side: str = "left",
):
    """Create a sidebar with the given configuration."""
    return Sidebar(
        side=side,
        variant=variant,
        collapsible=collapsible,
        children=[
            # Header
            SidebarHeader(
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                children=[
                                    SidebarMenuButton(
                                        "Acme Inc",
                                        icon="🏢",
                                        size="lg",
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            # Separator
            SidebarSeparator(),
            # Main content
            SidebarContent(
                children=[
                    # Main navigation group
                    SidebarGroup(
                        children=[
                            SidebarGroupLabel("Navigation"),
                            SidebarGroupContent(
                                children=[
                                    SidebarMenu(
                                        children=[
                                            SidebarMenuItem(
                                                children=[
                                                    SidebarMenuButton(
                                                        item["label"],
                                                        icon=item["icon"],
                                                        href=item["href"],
                                                        is_active=(
                                                            item["label"]
                                                            == active_item
                                                        ),
                                                    ),
                                                    *(
                                                        [
                                                            SidebarMenuBadge(
                                                                item["badge"]
                                                            )
                                                        ]
                                                        if item["badge"]
                                                        else []
                                                    ),
                                                ]
                                            )
                                            for item in MAIN_MENU
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Projects group with action button
                    SidebarGroup(
                        children=[
                            SidebarGroupLabel("Projects"),
                            SidebarGroupAction(icon="➕", title="Add Project", on_click=ctx.callback(test_callback)),
                            SidebarGroupContent(
                                children=[
                                    SidebarMenu(
                                        children=[
                                            SidebarMenuItem(
                                                children=[
                                                    SidebarMenuButton(
                                                        project["label"],
                                                        icon=project["icon"],
                                                        href=project["href"],
                                                    ),
                                                    SidebarMenuAction(
                                                        icon="⋮",
                                                        show_on_hover=True,
                                                    ),
                                                ]
                                            )
                                            for project in PROJECTS
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    # Settings with submenu
                    SidebarGroup(
                        children=[
                            SidebarGroupLabel("Preferences"),
                            SidebarGroupContent(
                                children=[
                                    SidebarMenu(
                                        children=[
                                            SidebarMenuItem(
                                                children=[
                                                    SidebarMenuButton(
                                                        "Settings",
                                                        icon="⚙️",
                                                    ),
                                                    SidebarMenuSub(
                                                        children=[
                                                            SidebarMenuSubItem(
                                                                children=[
                                                                    SidebarMenuSubButton(
                                                                        "General",
                                                                        href="#general",
                                                                    ),
                                                                ]
                                                            ),
                                                            SidebarMenuSubItem(
                                                                children=[
                                                                    SidebarMenuSubButton(
                                                                        "Security",
                                                                        href="#security",
                                                                    ),
                                                                ]
                                                            ),
                                                            SidebarMenuSubItem(
                                                                children=[
                                                                    SidebarMenuSubButton(
                                                                        "Notifications",
                                                                        href="#notifications",
                                                                        is_active=True,
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            # Separator
            SidebarSeparator(),
            # Footer
            SidebarFooter(
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                children=[
                                    SidebarMenuButton(
                                        "John Doe",
                                        icon="👤",
                                        size="lg",
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            # Rail for edge toggling
            SidebarRail(),
        ],
    )


def create_main_content(ctx, variant: str):
    """Create the main content area."""
    return Container(
        class_name="p-6",
        children=[
            Flex(
                direction="row",
                align="center",
                gap="4",
                class_name="mb-6",
                children=[
                    SidebarTrigger(),
                    Heading("Sidebar Showcase", level=1),
                ],
            ),
            Stack(
                gap="6",
                children=[
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Welcome to the Sidebar Demo"),
                                    CardDescription(
                                        "This example showcases all sidebar features."
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Stack(
                                        gap="4",
                                        children=[
                                            Text(
                                                "Use Ctrl+B (or Cmd+B on Mac) to toggle the sidebar."
                                            ),
                                            Text(
                                                "Try hovering over project items to see the action buttons."
                                            ),
                                            Text(
                                                "Explore the Settings submenu for nested navigation."
                                            ),
                                            Text(
                                                "The sidebar is fully responsive - try resizing your window!"
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ]
                    ),
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Sidebar Features"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Stack(
                                        gap="2",
                                        children=[
                                            Text(
                                                "✅ SidebarProvider - Context for state management"
                                            ),
                                            Text(
                                                "✅ Collapsible modes: offcanvas, icon, none"
                                            ),
                                            Text("✅ Variants: sidebar, floating, inset"),
                                            Text("✅ Left and right positioning"),
                                            Text("✅ Menu items with icons"),
                                            Text("✅ Badges for notifications"),
                                            Text("✅ Hover actions on menu items"),
                                            Text("✅ Nested submenus"),
                                            Text("✅ Group labels and actions"),
                                            Text("✅ Header and footer sections"),
                                            Text("✅ SidebarRail for edge toggling"),
                                            Text("✅ Keyboard shortcuts (Ctrl/Cmd+B)"),
                                            Text("✅ Mobile drawer support"),
                                        ],
                                    ),
                                ]
                            ),
                        ]
                    ),
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Current Configuration"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Stack(
                                        gap="2",
                                        children=[
                                            Text(f"Variant: {variant}"),
                                            Text("Collapsible: icon"),
                                            Text("Side: left"),
                                        ],
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
            ),
        ],
    )


@ui.page("/")
def home(ctx):
    """Default sidebar demo with icon collapsible mode."""
    variant = "sidebar"
    return SidebarProvider(
        default_open=True,
        children=[
            create_sidebar(
                ctx,
                active_item="Dashboard",
                variant=variant,
                collapsible="icon",
            ),
            SidebarInset(
                children=[
                    create_main_content(ctx, variant),
                ]
            ),
        ],
    )


@ui.page("/floating")
def floating(ctx):
    """Floating sidebar variant demo."""
    variant = "floating"
    return SidebarProvider(
        default_open=True,
        children=[
            create_sidebar(
                ctx,
                active_item="Inbox",
                variant=variant,
                collapsible="offcanvas",
            ),
            SidebarInset(
                children=[
                    Container(
                        class_name="p-6",
                        children=[
                            Flex(
                                direction="row",
                                align="center",
                                gap="4",
                                class_name="mb-6",
                                children=[
                                    SidebarTrigger(),
                                    Heading("Floating Sidebar", level=1),
                                ],
                            ),
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Floating Variant"),
                                            CardDescription(
                                                "The sidebar floats above the content with rounded corners and shadow."
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Stack(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "This variant adds visual separation between the sidebar and content."
                                                    ),
                                                    Text(
                                                        "Using offcanvas collapsible mode - sidebar slides completely away."
                                                    ),
                                                ],
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
    )


@ui.page("/inset")
def inset(ctx):
    """Inset sidebar variant demo."""
    variant = "inset"
    return SidebarProvider(
        default_open=True,
        children=[
            create_sidebar(
                ctx,
                active_item="Calendar",
                variant=variant,
                collapsible="icon",
            ),
            SidebarInset(
                children=[
                    Container(
                        class_name="p-6",
                        children=[
                            Flex(
                                direction="row",
                                align="center",
                                gap="4",
                                class_name="mb-6",
                                children=[
                                    SidebarTrigger(),
                                    Heading("Inset Sidebar", level=1),
                                ],
                            ),
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Inset Variant"),
                                            CardDescription(
                                                "The content area is inset with rounded corners."
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Stack(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "This variant gives the sidebar a full-bleed appearance."
                                                    ),
                                                    Text(
                                                        "The main content appears as a card inset from the sidebar."
                                                    ),
                                                ],
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
    )


@ui.page("/right")
def right_sidebar(ctx):
    """Right-side sidebar demo."""
    return SidebarProvider(
        default_open=True,
        children=[
            SidebarInset(
                children=[
                    Container(
                        class_name="p-6",
                        children=[
                            Flex(
                                direction="row",
                                align="center",
                                gap="4",
                                justify="end",
                                class_name="mb-6",
                                children=[
                                    Heading("Right Sidebar", level=1),
                                    SidebarTrigger(),
                                ],
                            ),
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Right Side Positioning"),
                                            CardDescription(
                                                "The sidebar can be positioned on the right side."
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Stack(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "Useful for secondary navigation or contextual information."
                                                    ),
                                                    Text(
                                                        "All features work the same as the left sidebar."
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                    ),
                ]
            ),
            create_sidebar(
                ctx,
                active_item="Search",
                variant="sidebar",
                collapsible="icon",
                side="right",
            ),
        ],
    )

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
