"""Navigation Showcase - Demonstrates all navigation components.

This example demonstrates:
- Breadcrumb navigation
- NavigationMenu with dropdowns
- Menubar with menus
- Command palette
- Sidebar navigation
- Tabs
- Pagination
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Breadcrumb,
    BreadcrumbEllipsis,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
    CommandSeparator,
    Container,
    Label,
    Menubar,
    MenubarCheckboxItem,
    MenubarContent,
    MenubarItem,
    MenubarMenu,
    MenubarSeparator,
    MenubarTrigger,
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
    Row,
    Separator,
    TabItem,
    Tabs,
    Text,
)

# Create the Refast app
ui = RefastApp(title="Navigation Showcase")


# Callback handlers
async def on_nav_click(ctx: Context):
    """Handle navigation click."""
    item = ctx.event_data.get("item", "Unknown")
    await ctx.show_toast(f"Navigating to: {item}", variant="info")


async def on_command_select(ctx: Context):
    """Handle command palette selection."""
    command = ctx.event_data.get("command", "Unknown")
    await ctx.show_toast(f"Executing: {command}", variant="info")


async def on_page_change(ctx: Context):
    """Handle page change."""
    page = ctx.event_data.get("page", 1)
    ctx.state.set("current_page", page)
    await ctx.refresh()


# Main page
@ui.page("/")
def home(ctx: Context):
    """Navigation showcase page."""
    current_page = ctx.state.get("current_page", 1)

    return Container(
        class_name="max-w-6xl mx-auto p-6",
        children=[
            Column(
                gap=8,
                children=[
                    # Header
                    Column(
                        gap=2,
                        children=[
                            Text("Navigation Components", class_name="text-3xl font-bold"),
                            Text(
                                "Explore the navigation components available in Refast",
                                class_name="text-muted-foreground",
                            ),
                        ],
                    ),
                    # Menubar Section
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Menubar"),
                                    CardDescription("Application menu bar with nested menus"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Menubar(
                                        children=[
                                            MenubarMenu(
                                                children=[
                                                    MenubarTrigger(label="File"),
                                                    MenubarContent(
                                                        children=[
                                                            MenubarItem(
                                                                label="New Tab",
                                                                shortcut="⌘T",
                                                            ),
                                                            MenubarItem(
                                                                label="New Window",
                                                                shortcut="⌘N",
                                                            ),
                                                            MenubarSeparator(),
                                                            MenubarItem(label="Share"),
                                                            MenubarSeparator(),
                                                            MenubarItem(
                                                                label="Print", shortcut="⌘P"
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            MenubarMenu(
                                                children=[
                                                    MenubarTrigger(label="Edit"),
                                                    MenubarContent(
                                                        children=[
                                                            MenubarItem(
                                                                label="Undo", shortcut="⌘Z"
                                                            ),
                                                            MenubarItem(
                                                                label="Redo", shortcut="⇧⌘Z"
                                                            ),
                                                            MenubarSeparator(),
                                                            MenubarItem(label="Cut", shortcut="⌘X"),
                                                            MenubarItem(
                                                                label="Copy", shortcut="⌘C"
                                                            ),
                                                            MenubarItem(
                                                                label="Paste", shortcut="⌘V"
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            MenubarMenu(
                                                children=[
                                                    MenubarTrigger(label="View"),
                                                    MenubarContent(
                                                        children=[
                                                            MenubarCheckboxItem(
                                                                label="Show Toolbar",
                                                                checked=True,
                                                            ),
                                                            MenubarCheckboxItem(
                                                                label="Show Sidebar",
                                                                checked=True,
                                                            ),
                                                            MenubarSeparator(),
                                                            MenubarItem(
                                                                label="Zoom In", shortcut="⌘+"
                                                            ),
                                                            MenubarItem(
                                                                label="Zoom Out", shortcut="⌘-"
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            MenubarMenu(
                                                children=[
                                                    MenubarTrigger(label="Help"),
                                                    MenubarContent(
                                                        children=[
                                                            MenubarItem(label="Documentation"),
                                                            MenubarItem(label="Keyboard Shortcuts"),
                                                            MenubarSeparator(),
                                                            MenubarItem(label="About"),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Breadcrumb Section
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Breadcrumb"),
                                    CardDescription(
                                        "Navigation breadcrumbs showing location hierarchy"
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Column(
                                        gap=6,
                                        children=[
                                            # Simple breadcrumb
                                            Column(
                                                gap=2,
                                                children=[
                                                    Label("Simple"),
                                                    Breadcrumb(
                                                        children=[
                                                            BreadcrumbList(
                                                                children=[
                                                                    BreadcrumbItem(
                                                                        children=[
                                                                            BreadcrumbLink(
                                                                                label="Home",
                                                                                href="/",
                                                                            )
                                                                        ]
                                                                    ),
                                                                    BreadcrumbSeparator(),
                                                                    BreadcrumbItem(
                                                                        children=[
                                                                            BreadcrumbLink(
                                                                                label="Products",
                                                                                href="/products",
                                                                            )
                                                                        ]
                                                                    ),
                                                                    BreadcrumbSeparator(),
                                                                    BreadcrumbItem(
                                                                        children=[
                                                                            BreadcrumbPage(
                                                                                label="Electronics"
                                                                            )
                                                                        ]
                                                                    ),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ],
                                            ),
                                            Separator(),
                                            # With ellipsis
                                            Column(
                                                gap=2,
                                                children=[
                                                    Label("With Ellipsis (collapsed)"),
                                                    Breadcrumb(
                                                        children=[
                                                            BreadcrumbList(
                                                                children=[
                                                                    BreadcrumbItem(
                                                                        children=[
                                                                            BreadcrumbLink(
                                                                                label="Home",
                                                                                href="/",
                                                                            )
                                                                        ]
                                                                    ),
                                                                    BreadcrumbSeparator(),
                                                                    BreadcrumbItem(
                                                                        children=[
                                                                            BreadcrumbEllipsis()
                                                                        ]
                                                                    ),
                                                                    BreadcrumbSeparator(),
                                                                    BreadcrumbItem(
                                                                        children=[
                                                                            BreadcrumbLink(
                                                                                label="Categories",
                                                                                href="/categories",
                                                                            )
                                                                        ]
                                                                    ),
                                                                    BreadcrumbSeparator(),
                                                                    BreadcrumbItem(
                                                                        children=[
                                                                            BreadcrumbPage(
                                                                                label="Current Page"
                                                                            )
                                                                        ]
                                                                    ),
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Navigation Menu Section
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Navigation Menu"),
                                    CardDescription("Horizontal navigation with dropdown content"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    NavigationMenu(
                                        children=[
                                            NavigationMenuList(
                                                children=[
                                                    NavigationMenuItem(
                                                        children=[
                                                            NavigationMenuTrigger(
                                                                label="Getting Started"
                                                            ),
                                                            NavigationMenuContent(
                                                                children=[
                                                                    Container(
                                                                        class_name="grid gap-3 p-4 w-[400px] md:w-[500px] md:grid-cols-2",
                                                                        children=[
                                                                            Column(
                                                                                gap=1,
                                                                                class_name="p-3 rounded-md hover:bg-muted",
                                                                                children=[
                                                                                    Text(
                                                                                        "Introduction",
                                                                                        class_name="font-medium",
                                                                                    ),
                                                                                    Text(
                                                                                        "Learn the basics of Refast and get started quickly.",
                                                                                        class_name="text-sm text-muted-foreground",
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                            Column(
                                                                                gap=1,
                                                                                class_name="p-3 rounded-md hover:bg-muted",
                                                                                children=[
                                                                                    Text(
                                                                                        "Installation",
                                                                                        class_name="font-medium",
                                                                                    ),
                                                                                    Text(
                                                                                        "Step-by-step guide to install and set up.",
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
                                                    NavigationMenuItem(
                                                        children=[
                                                            NavigationMenuTrigger(
                                                                label="Components"
                                                            ),
                                                            NavigationMenuContent(
                                                                children=[
                                                                    Container(
                                                                        class_name="grid gap-3 p-4 w-[400px] md:w-[500px] md:grid-cols-2",
                                                                        children=[
                                                                            Column(
                                                                                gap=1,
                                                                                class_name="p-3 rounded-md hover:bg-muted",
                                                                                children=[
                                                                                    Text(
                                                                                        "Button",
                                                                                        class_name="font-medium",
                                                                                    ),
                                                                                    Text(
                                                                                        "Displays a button or a component that looks like a button.",
                                                                                        class_name="text-sm text-muted-foreground",
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                            Column(
                                                                                gap=1,
                                                                                class_name="p-3 rounded-md hover:bg-muted",
                                                                                children=[
                                                                                    Text(
                                                                                        "Card",
                                                                                        class_name="font-medium",
                                                                                    ),
                                                                                    Text(
                                                                                        "Displays a card with header, content, and footer.",
                                                                                        class_name="text-sm text-muted-foreground",
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                            Column(
                                                                                gap=1,
                                                                                class_name="p-3 rounded-md hover:bg-muted",
                                                                                children=[
                                                                                    Text(
                                                                                        "Dialog",
                                                                                        class_name="font-medium",
                                                                                    ),
                                                                                    Text(
                                                                                        "A modal dialog that interrupts the user.",
                                                                                        class_name="text-sm text-muted-foreground",
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                            Column(
                                                                                gap=1,
                                                                                class_name="p-3 rounded-md hover:bg-muted",
                                                                                children=[
                                                                                    Text(
                                                                                        "Input",
                                                                                        class_name="font-medium",
                                                                                    ),
                                                                                    Text(
                                                                                        "Displays a form input field.",
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
                                                    NavigationMenuItem(
                                                        children=[
                                                            NavigationMenuLink(
                                                                label="Documentation",
                                                                href="/docs",
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Command Palette Section
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Command Palette"),
                                    CardDescription(
                                        "Searchable command menu with keyboard shortcuts"
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Command(
                                        class_name="border rounded-lg",
                                        children=[
                                            CommandInput(placeholder="Type a command or search..."),
                                            CommandList(
                                                children=[
                                                    CommandEmpty(message="No results found."),
                                                    CommandGroup(
                                                        heading="Suggestions",
                                                        children=[
                                                            CommandItem(
                                                                label="Calendar",
                                                                icon="calendar",
                                                                on_select=ctx.callback(
                                                                    on_command_select,
                                                                    command="Calendar",
                                                                ),
                                                            ),
                                                            CommandItem(
                                                                label="Search",
                                                                icon="search",
                                                                on_select=ctx.callback(
                                                                    on_command_select,
                                                                    command="Search",
                                                                ),
                                                            ),
                                                            CommandItem(
                                                                label="Settings",
                                                                icon="settings",
                                                                on_select=ctx.callback(
                                                                    on_command_select,
                                                                    command="Settings",
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                    CommandSeparator(),
                                                    CommandGroup(
                                                        heading="Actions",
                                                        children=[
                                                            CommandItem(
                                                                label="New File",
                                                                icon="file-plus",
                                                                on_select=ctx.callback(
                                                                    on_command_select,
                                                                    command="New File",
                                                                ),
                                                            ),
                                                            CommandItem(
                                                                label="New Folder",
                                                                icon="folder-plus",
                                                                on_select=ctx.callback(
                                                                    on_command_select,
                                                                    command="New Folder",
                                                                ),
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
                    # Tabs Section
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Tabs"),
                                    CardDescription("Tabbed interface for organizing content"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Tabs(
                                        default_value="overview",
                                        children=[
                                            TabItem(value="overview", label="Overview"),
                                            TabItem(value="analytics", label="Analytics"),
                                            TabItem(value="reports", label="Reports"),
                                            TabItem(value="notifications", label="Notifications"),
                                        ],
                                    ),
                                    Container(
                                        class_name="mt-4 p-4 border rounded-md",
                                        children=[
                                            Text(
                                                "Tab content goes here",
                                                class_name="text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Pagination Section
                    Card(
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Pagination"),
                                    CardDescription("Page navigation controls"),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Column(
                                        gap=6,
                                        children=[
                                            # Current page display
                                            Row(
                                                justify="center",
                                                children=[
                                                    Text(
                                                        f"Current Page: {current_page}",
                                                        class_name="text-lg font-medium",
                                                    ),
                                                ],
                                            ),
                                            # Pagination
                                            Row(
                                                justify="center",
                                                children=[
                                                    Pagination(
                                                        children=[
                                                            PaginationContent(
                                                                children=[
                                                                    PaginationItem(
                                                                        children=[
                                                                            PaginationPrevious(
                                                                                href="#",
                                                                                on_click=ctx.callback(
                                                                                    on_page_change,
                                                                                    page=max(
                                                                                        1,
                                                                                        current_page
                                                                                        - 1,
                                                                                    ),
                                                                                ),
                                                                            )
                                                                        ]
                                                                    ),
                                                                    PaginationItem(
                                                                        children=[
                                                                            PaginationLink(
                                                                                label="1",
                                                                                href="#",
                                                                                page=1,
                                                                                is_active=(
                                                                                    current_page
                                                                                    == 1
                                                                                ),
                                                                                on_click=ctx.callback(
                                                                                    on_page_change,
                                                                                    page=1,
                                                                                ),
                                                                            )
                                                                        ]
                                                                    ),
                                                                    PaginationItem(
                                                                        children=[
                                                                            PaginationLink(
                                                                                label="2",
                                                                                href="#",
                                                                                page=2,
                                                                                is_active=(
                                                                                    current_page
                                                                                    == 2
                                                                                ),
                                                                                on_click=ctx.callback(
                                                                                    on_page_change,
                                                                                    page=2,
                                                                                ),
                                                                            )
                                                                        ]
                                                                    ),
                                                                    PaginationItem(
                                                                        children=[
                                                                            PaginationLink(
                                                                                label="3",
                                                                                href="#",
                                                                                page=3,
                                                                                is_active=(
                                                                                    current_page
                                                                                    == 3
                                                                                ),
                                                                                on_click=ctx.callback(
                                                                                    on_page_change,
                                                                                    page=3,
                                                                                ),
                                                                            )
                                                                        ]
                                                                    ),
                                                                    PaginationItem(
                                                                        children=[
                                                                            PaginationEllipsis()
                                                                        ]
                                                                    ),
                                                                    PaginationItem(
                                                                        children=[
                                                                            PaginationLink(
                                                                                label="10",
                                                                                href="#",
                                                                                page=10,
                                                                                is_active=(
                                                                                    current_page
                                                                                    == 10
                                                                                ),
                                                                                on_click=ctx.callback(
                                                                                    on_page_change,
                                                                                    page=10,
                                                                                ),
                                                                            )
                                                                        ]
                                                                    ),
                                                                    PaginationItem(
                                                                        children=[
                                                                            PaginationNext(
                                                                                href="#",
                                                                                on_click=ctx.callback(
                                                                                    on_page_change,
                                                                                    page=min(
                                                                                        10,
                                                                                        current_page
                                                                                        + 1,
                                                                                    ),
                                                                                ),
                                                                            )
                                                                        ]
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
