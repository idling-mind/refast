"""Examples Gallery — /docs/examples."""

from refast.components import (
    Badge,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Grid,
    Heading,
    Icon,
    Markdown,
    Row,
    Separator,
    Text,
)

PAGE_TITLE = "Examples Gallery"
PAGE_ROUTE = "/docs/examples"

EXAMPLES = [
    {
        "title": "Hello World",
        "desc": "Minimal Refast app — one page, one component.",
        "icon": "hand-metal",
        "file": "examples/hello.py",
    },
    {
        "title": "Basic App",
        "desc": "Counter with state management and callbacks.",
        "icon": "play",
        "file": "examples/basic/app.py",
    },
    {
        "title": "Todo App",
        "desc": "Classic todo list with add, toggle, and delete.",
        "icon": "check-square",
        "file": "examples/todo_app/app.py",
    },
    {
        "title": "Multi-Page SPA",
        "desc": "SPA navigation with shared layout and ctx.navigate().",
        "icon": "route",
        "file": "examples/multi_page/app.py",
    },
    {
        "title": "Chat App",
        "desc": "Real-time chat with broadcasting to connected clients.",
        "icon": "message-square",
        "file": "examples/chat_app/app.py",
    },
    {
        "title": "Dashboard",
        "desc": "Multi-section dashboard with cards and charts.",
        "icon": "layout-dashboard",
        "file": "examples/dashboard/app.py",
    },
    {
        "title": "Streaming",
        "desc": "Incremental text streaming with ctx.stream().",
        "icon": "radio",
        "file": "examples/streaming/app.py",
    },
    {
        "title": "Prop Store",
        "desc": "Client-side form state with store_as and prop_store.",
        "icon": "hard-drive",
        "file": "examples/prop_store/app.py",
    },
    {
        "title": "Toast Showcase",
        "desc": "All toast variants, positions, and configurations.",
        "icon": "bell",
        "file": "examples/toast_showcase/app.py",
    },
    {
        "title": "Theme Showcase",
        "desc": "Theme switching, presets, and custom themes.",
        "icon": "palette",
        "file": "examples/theme_showcase/app.py",
    },
    {
        "title": "Charts Showcase",
        "desc": "Bar, line, area, pie, radar, and radial charts.",
        "icon": "bar-chart-3",
        "file": "examples/charts_showcase/app.py",
    },
    {
        "title": "Data Table",
        "desc": "Sortable, filterable table with pagination.",
        "icon": "table",
        "file": "examples/data_table/app.py",
    },
    {
        "title": "Form Validation",
        "desc": "Input validation patterns and error display.",
        "icon": "shield-check",
        "file": "examples/form_validation/app.py",
    },
    {
        "title": "Kanban Board",
        "desc": "Drag-style column board with task management.",
        "icon": "columns",
        "file": "examples/kanban_board/app.py",
    },
    {
        "title": "Sidebar Layout",
        "desc": "Full sidebar navigation with groups and submenus.",
        "icon": "panel-left",
        "file": "examples/sidebar_showcase/app.py",
    },
    {
        "title": "Real-time Dashboard",
        "desc": "Background tasks broadcasting to all clients.",
        "icon": "activity",
        "file": "examples/realtime_dashboard/app.py",
    },
    {
        "title": "JS Callbacks",
        "desc": "Client-side JS without server roundtrip.",
        "icon": "code",
        "file": "examples/js_callbacks/app.py",
    },
    {
        "title": "File Manager",
        "desc": "Tree-style file browser with context menus.",
        "icon": "folder",
        "file": "examples/file_manager/app.py",
    },
    {
        "title": "Settings Panel",
        "desc": "Settings form with tabs, switches, and selects.",
        "icon": "settings",
        "file": "examples/settings_panel/app.py",
    },
    {
        "title": "Long Running Tasks",
        "desc": "Background job with progress and targeted DOM updates.",
        "icon": "clock",
        "file": "examples/longrunning.py",
    },
    {
        "title": "Connection Status",
        "desc": "WebSocket connection monitoring component.",
        "icon": "wifi",
        "file": "examples/connection_status/app.py",
    },
    {
        "title": "Component Showcase",
        "desc": "Kitchen sink demo of all available components.",
        "icon": "component",
        "file": "examples/component_showcase/app.py",
    },
    {
        "title": "Navigation Showcase",
        "desc": "Breadcrumbs, menus, pagination, and command palette.",
        "icon": "compass",
        "file": "examples/navigation_showcase/app.py",
    },
    {
        "title": "E-Commerce Product",
        "desc": "Product page with images, variants, and cart.",
        "icon": "shopping-cart",
        "file": "examples/ecommerce_product/app.py",
    },
    {
        "title": "Colors Showcase",
        "desc": "All semantic color tokens and their usage.",
        "icon": "paintbrush",
        "file": "examples/colors_showcase/app.py",
    },
]


def render(ctx):
    """Render the examples gallery page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-5xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Text(
                "Explore working examples that demonstrate Refast's features.",
                class_name="text-muted-foreground mb-2",
            ),
            Separator(class_name="my-4"),
            Grid(
                columns=3,
                gap=4,
                children=[
                    Card(
                        children=[
                            CardHeader(
                                class_name="pb-2",
                                children=[
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Icon(ex["icon"], size=16, class_name="text-primary"),
                                            CardTitle(ex["title"], class_name="text-base"),
                                        ],
                                    ),
                                ],
                            ),
                            CardContent(
                                children=[
                                    Text(
                                        ex["desc"],
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                    Text(
                                        ex["file"],
                                        class_name="text-xs font-mono mt-2 text-muted-foreground",
                                    ),
                                ],
                            ),
                        ],
                    )
                    for ex in EXAMPLES
                ],
            ),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)
