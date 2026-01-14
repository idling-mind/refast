"""
Sidebar Showcase Example

This example demonstrates all the sidebar component features:
- SidebarProvider for state management
- Different sidebar variants (sidebar, floating, inset)
- Different collapsible modes (offcanvas, icon, none)
- Left and right side positioning
- Menu items with icons, badges, and actions
- Collapsible menu sections using Collapsible component
- Nested submenus
- Dropdown menus for menu actions
- Menu skeletons for loading states
- Header and footer sections
- Keyboard shortcuts (Ctrl/Cmd+B to toggle)
- Mobile responsiveness

Pages:
- / - Default sidebar with icon collapsible mode
- /floating - Floating variant with offcanvas collapsible
- /inset - Inset variant
- /right - Right-side sidebar
- /collapsible-menu - Collapsible menu sections demo
- /dropdown-actions - Menu with dropdown actions
- /skeleton - Loading state with skeletons
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
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
    Column,
    Container,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
    Flex,
    Heading,
    Link,
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
    SidebarMenuSkeleton,
    SidebarMenuSub,
    SidebarMenuSubButton,
    SidebarMenuSubItem,
    SidebarProvider,
    SidebarRail,
    SidebarSeparator,
    SidebarTrigger,
    Text,
)

ui = RefastApp(title="Sidebar Showcase")


async def handle_action(ctx, action: str):
    """Generic action handler."""
    await ctx.show_toast(f"Action: {action}", variant="success")


async def handle_add_project(ctx):
    await ctx.show_toast("Add Project clicked!", variant="success")


async def handle_menu_action(ctx, item: str = "", action: str = ""):
    """Handle menu action with keyword args."""
    await ctx.show_toast(f"{action} on {item}", variant="info")


# Sample menu data
MAIN_MENU = [
    {"label": "Dashboard", "icon": "home", "href": "#dashboard", "badge": None},
    {"label": "Inbox", "icon": "inbox", "href": "#inbox", "badge": "24"},
    {"label": "Calendar", "icon": "calendar", "href": "#calendar", "badge": None},
    {"label": "Search", "icon": "search", "href": "#search", "badge": None},
    {"label": "Settings", "icon": "settings", "href": "#settings", "badge": None},
]

PROJECTS = [
    {"label": "Project Alpha", "icon": "folder", "href": "#alpha"},
    {"label": "Project Beta", "icon": "folder", "href": "#beta"},
    {"label": "Project Gamma", "icon": "folder", "href": "#gamma"},
]

# Hierarchical menu data for collapsible sections
COLLAPSIBLE_MENU = [
    {
        "label": "Getting Started",
        "icon": "zap",
        "items": [
            {"label": "Introduction", "href": "#intro"},
            {"label": "Installation", "href": "#install"},
            {"label": "Quick Start", "href": "#quickstart"},
        ],
    },
    {
        "label": "Components",
        "icon": "box",
        "items": [
            {"label": "Button", "href": "#button"},
            {"label": "Card", "href": "#card"},
            {"label": "Input", "href": "#input"},
            {"label": "Dialog", "href": "#dialog"},
        ],
    },
    {
        "label": "API Reference",
        "icon": "book",
        "items": [
            {"label": "Overview", "href": "#api-overview"},
            {"label": "Context", "href": "#api-context"},
            {"label": "Events", "href": "#api-events"},
        ],
    },
]


def create_sidebar(
    ctx,
    active_item: str = "Dashboard",
    variant: str = "sidebar",
    collapsible: str = "icon",
    side: str = "left",
    show_rail: bool = True,
):
    """Create a sidebar with the given configuration.
    
    Args:
        ctx: The context
        active_item: Which menu item is active
        variant: sidebar, floating, or inset
        collapsible: icon, offcanvas, or none
        side: left or right
        show_rail: Whether to show the SidebarRail (set False for non-collapsible)
    """
    # Build children list, optionally excluding rail
    sidebar_children = [
        # Header
        SidebarHeader(
            children=[
                SidebarMenu(
                    children=[
                        SidebarMenuItem(
                                children=[
                                    SidebarMenuButton(
                                        "Acme Inc",
                                        icon="building",
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
                            SidebarGroupAction(icon="plus", title="Add Project", on_click=ctx.callback(handle_add_project)),
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
                                                        icon="more-vertical",
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
                                                        icon="settings",
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
                                        icon="user",
                                        size="lg",
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    
    # Only add rail if collapsible (not in 'none' mode)
    if show_rail:
        sidebar_children.append(SidebarRail())
    
    return Sidebar(
        side=side,
        variant=variant,
        collapsible=collapsible,
        children=sidebar_children,
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
            Column(
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
                                    Column(
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
                                    CardTitle("Demo Pages"),
                                    CardDescription("Explore different sidebar configurations"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Flex(
                                        gap="2",
                                        wrap="wrap",
                                        children=[
                                            Link(
                                                "Home (Icon Mode)",
                                                href="/",
                                            ),
                                            Link(
                                                "Floating",
                                                href="/floating",
                                            ),
                                            Link(
                                                "Inset",
                                                href="/inset",
                                            ),
                                            Link(
                                                "Right Side",
                                                href="/right",
                                            ),
                                            Link(
                                                "Collapsible Menu",
                                                href="/collapsible-menu",
                                            ),
                                            Link(
                                                "Dropdown Actions",
                                                href="/dropdown-actions",
                                            ),
                                            Link(
                                                "Skeleton Loading",
                                                href="/skeleton",
                                            ),
                                            Link(
                                                "Offcanvas Mode",
                                                href="/offcanvas",
                                            ),
                                            Link(
                                                "Non-Collapsible",
                                                href="/none",
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
                                    Column(
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
                                            Text("✅ Collapsible menu sections"),
                                            Text("✅ Dropdown menus in menu actions"),
                                            Text("✅ Button variants (default, outline)"),
                                            Text("✅ Button sizes (sm, default, lg)"),
                                            Text("✅ Group labels and actions"),
                                            Text("✅ Header and footer sections"),
                                            Text("✅ SidebarRail for edge toggling"),
                                            Text("✅ Keyboard shortcuts (Ctrl/Cmd+B)"),
                                            Text("✅ Skeleton loading states"),
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
                                    Column(
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
                                            Column(
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
                                            Column(
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
                                            Column(
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


@ui.page("/collapsible-menu")
def collapsible_menu_demo(ctx):
    """Collapsible menu sections demo using Collapsible component."""
    return SidebarProvider(
        default_open=True,
        children=[
            Sidebar(
                variant="sidebar",
                collapsible="icon",
                children=[
                    SidebarHeader(
                        children=[
                            SidebarMenu(
                                children=[
                                    SidebarMenuItem(
                                        children=[
                                            SidebarMenuButton(
                                                "Documentation",
                                                icon="file-text",
                                                size="lg",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    SidebarSeparator(),
                    SidebarContent(
                        children=[
                            # Each section is collapsible using Collapsible wrapper
                            *[
                                SidebarGroup(
                                    children=[
                                        Collapsible(
                                            default_open=(i == 0),  # First section open by default
                                            class_name="group/collapsible",
                                            children=[
                                                # Trigger wraps a menu button
                                                CollapsibleTrigger(
                                                    as_child=True,
                                                    children=[
                                                        SidebarMenuButton(
                                                            section["label"],
                                                            icon=section["icon"],
                                                        ),
                                                    ],
                                                ),
                                                CollapsibleContent(
                                                    children=[
                                                        SidebarGroupContent(
                                                            children=[
                                                                SidebarMenu(
                                                                    children=[
                                                                        SidebarMenuItem(
                                                                            children=[
                                                                                SidebarMenuButton(
                                                                                    item["label"],
                                                                                    href=item["href"],
                                                                                ),
                                                                            ]
                                                                        )
                                                                        for item in section["items"]
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ],
                                        ),
                                    ]
                                )
                                for i, section in enumerate(COLLAPSIBLE_MENU)
                            ],
                        ]
                    ),
                    SidebarRail(),
                ],
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
                                    Heading("Collapsible Menu Sections", level=1),
                                ],
                            ),
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Collapsible Menu Demo"),
                                            CardDescription(
                                                "Menu sections that can expand/collapse."
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Column(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "This example uses the Collapsible component to create expandable menu sections."
                                                    ),
                                                    Text(
                                                        "Click the arrow icon next to each section header to toggle it."
                                                    ),
                                                    Text(
                                                        "The first section is open by default using default_open=True."
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            Card(
                                class_name="mt-4",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Code Pattern"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Text(
                                                "Wrap your SidebarGroup content with Collapsible, CollapsibleTrigger, and CollapsibleContent."
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


@ui.page("/dropdown-actions")
def dropdown_actions_demo(ctx):
    """Menu items with dropdown action buttons."""
    return SidebarProvider(
        default_open=True,
        children=[
            Sidebar(
                variant="sidebar",
                collapsible="icon",
                children=[
                    SidebarHeader(
                        children=[
                            SidebarMenu(
                                children=[
                                    SidebarMenuItem(
                                        children=[
                                            SidebarMenuButton(
                                                "Workspace",
                                                icon="building",
                                                size="lg",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    SidebarSeparator(),
                    SidebarContent(
                        children=[
                            SidebarGroup(
                                children=[
                                    SidebarGroupLabel("Projects"),
                                    SidebarGroupAction(
                                        icon="plus",
                                        title="Add Project",
                                        on_click=ctx.callback(handle_add_project),
                                    ),
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
                                                            # Dropdown menu for each project
                                                            DropdownMenu(
                                                                children=[
                                                                    DropdownMenuTrigger(
                                                                        children=[
                                                                            SidebarMenuAction(
                                                                                icon="more-vertical",
                                                                                show_on_hover=True,
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    DropdownMenuContent(
                                                                        side="right",
                                                                        align="start",
                                                                        children=[
                                                                            DropdownMenuLabel(
                                                                                project["label"]
                                                                            ),
                                                                            DropdownMenuSeparator(),
                                                                            DropdownMenuItem(
                                                                                "Open",
                                                                                icon="folder-open",
                                                                                on_select=ctx.callback(
                                                                                    handle_menu_action,
                                                                                    item=project["label"],
                                                                                    action="Open",
                                                                                ),
                                                                            ),
                                                                            DropdownMenuItem(
                                                                                "Edit",
                                                                                icon="edit",
                                                                                on_select=ctx.callback(
                                                                                    handle_menu_action,
                                                                                    item=project["label"],
                                                                                    action="Edit",
                                                                                ),
                                                                            ),
                                                                            DropdownMenuItem(
                                                                                "Share",
                                                                                icon="link",
                                                                                on_select=ctx.callback(
                                                                                    handle_menu_action,
                                                                                    item=project["label"],
                                                                                    action="Share",
                                                                                ),
                                                                            ),
                                                                            DropdownMenuSeparator(),
                                                                            DropdownMenuItem(
                                                                                "Delete",
                                                                                icon="trash",
                                                                                class_name="text-red-500",
                                                                                on_select=ctx.callback(
                                                                                    handle_menu_action,
                                                                                    item=project["label"],
                                                                                    action="Delete",
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ]
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
                            SidebarGroup(
                                children=[
                                    SidebarGroupLabel("Button Variants"),
                                    SidebarGroupContent(
                                        children=[
                                            SidebarMenu(
                                                children=[
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Default Button",
                                                                icon="circle",
                                                                variant="default",
                                                            ),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Outline Button",
                                                                icon="circle-dot",
                                                                variant="outline",
                                                            ),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Active Default",
                                                                icon="check-circle",
                                                                variant="default",
                                                                is_active=True,
                                                            ),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Active Outline",
                                                                icon="check-circle-2",
                                                                variant="outline",
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
                            SidebarGroup(
                                children=[
                                    SidebarGroupLabel("Button Sizes"),
                                    SidebarGroupContent(
                                        children=[
                                            SidebarMenu(
                                                children=[
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Small Button",
                                                                icon="minus",
                                                                size="sm",
                                                            ),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Default Button",
                                                                icon="square",
                                                                size="default",
                                                            ),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Large Button",
                                                                icon="maximize",
                                                                size="lg",
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
                    SidebarRail(),
                ],
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
                                    Heading("Dropdown Actions & Variants", level=1),
                                ],
                            ),
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Dropdown Menu Actions"),
                                            CardDescription(
                                                "Menu items with dropdown action buttons."
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Column(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "Hover over project items to see the action button (⋮)."
                                                    ),
                                                    Text(
                                                        "Click the button to open a dropdown menu with options."
                                                    ),
                                                    Text(
                                                        "Each option triggers a toast notification demonstrating the callback."
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            Card(
                                class_name="mt-4",
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Button Variants & Sizes"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Column(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "SidebarMenuButton supports two variants: 'default' and 'outline'."
                                                    ),
                                                    Text(
                                                        "Three sizes are available: 'sm', 'default', and 'lg'."
                                                    ),
                                                    Text(
                                                        "The 'is_active' prop highlights the current selection."
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


@ui.page("/skeleton")
def skeleton_demo(ctx):
    """Loading state demonstration with skeleton menu items."""
    return SidebarProvider(
        default_open=True,
        children=[
            Sidebar(
                variant="sidebar",
                collapsible="icon",
                children=[
                    SidebarHeader(
                        children=[
                            SidebarMenu(
                                children=[
                                    SidebarMenuItem(
                                        children=[
                                            SidebarMenuButton(
                                                "Loading Demo",
                                                icon="loader",
                                                size="lg",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    SidebarSeparator(),
                    SidebarContent(
                        children=[
                            SidebarGroup(
                                children=[
                                    SidebarGroupLabel("Loading Items"),
                                    SidebarGroupContent(
                                        children=[
                                            SidebarMenu(
                                                children=[
                                                    # Skeleton items to show loading state
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuSkeleton(show_icon=True),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuSkeleton(show_icon=True),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuSkeleton(show_icon=True),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuSkeleton(show_icon=True),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            SidebarGroup(
                                children=[
                                    SidebarGroupLabel("Without Icons"),
                                    SidebarGroupContent(
                                        children=[
                                            SidebarMenu(
                                                children=[
                                                    # Skeleton items without icons
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuSkeleton(show_icon=False),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuSkeleton(show_icon=False),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuSkeleton(show_icon=False),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            SidebarGroup(
                                children=[
                                    SidebarGroupLabel("Loaded Items"),
                                    SidebarGroupContent(
                                        children=[
                                            SidebarMenu(
                                                children=[
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Loaded Item 1",
                                                                icon="✓",
                                                            ),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Loaded Item 2",
                                                                icon="✓",
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
                    SidebarRail(),
                ],
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
                                    Heading("Skeleton Loading States", level=1),
                                ],
                            ),
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Menu Skeletons"),
                                            CardDescription(
                                                "Placeholder loading states for menu items."
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Column(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "Use SidebarMenuSkeleton to show loading placeholders."
                                                    ),
                                                    Text(
                                                        "Set show_icon=True to include an icon placeholder."
                                                    ),
                                                    Text(
                                                        "Useful when loading dynamic menu items from an API."
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


@ui.page("/offcanvas")
def offcanvas_demo(ctx):
    """Offcanvas collapsible mode - sidebar completely hides when collapsed."""
    return SidebarProvider(
        default_open=True,
        children=[
            create_sidebar(
                ctx,
                active_item="Dashboard",
                variant="sidebar",
                collapsible="offcanvas",  # Completely hides when collapsed
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
                                    Heading("Offcanvas Mode", level=1),
                                ],
                            ),
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Offcanvas Collapsible"),
                                            CardDescription(
                                                "The sidebar completely hides when collapsed."
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Column(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "Press Ctrl+B (or Cmd+B) to toggle the sidebar."
                                                    ),
                                                    Text(
                                                        "Unlike 'icon' mode, the sidebar fully disappears."
                                                    ),
                                                    Text(
                                                        "This gives maximum space to the main content area."
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


@ui.page("/none")
def none_collapsible_demo(ctx):
    """Non-collapsible sidebar - always visible."""
    return SidebarProvider(
        default_open=True,
        children=[
            create_sidebar(
                ctx,
                active_item="Dashboard",
                variant="sidebar",
                collapsible="none",  # Cannot be collapsed
                show_rail=False,  # No rail for non-collapsible
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
                                    Heading("Non-Collapsible Sidebar", level=1),
                                ],
                            ),
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("No Collapse Mode"),
                                            CardDescription(
                                                "The sidebar is always visible and cannot be collapsed."
                                            ),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Column(
                                                gap="2",
                                                children=[
                                                    Text(
                                                        "When collapsible='none', the sidebar stays fully expanded."
                                                    ),
                                                    Text(
                                                        "The toggle button and keyboard shortcuts are disabled."
                                                    ),
                                                    Text(
                                                        "Use this for layouts where navigation must always be visible."
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


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
