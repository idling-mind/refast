"""Refast Documentation Site.

A comprehensive documentation site for the Refast framework, built with Refast itself.

Run:
    cd <project_root>
    uvicorn docs_site.app:app --reload
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from refast import Context, RefastApp
from refast.components import (
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    Button,
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
    ConnectionStatus,
    Container,
    Dialog,
    DialogContent,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    Flex,
    IconButton,
    Row,
    Separator,
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarInset,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarMenuSub,
    SidebarMenuSubButton,
    SidebarMenuSubItem,
    SidebarProvider,
    SidebarRail,
    SidebarSeparator,
    SidebarTrigger,
    Tooltip,
)
from refast.components.shadcn import KeyboardShortcut, ThemeSwitcher
from refast.theme import (
    amber_minimal_theme,
    caffine_theme,
    catppuccin_theme,
    default_theme,
    ocean_breeze_theme,
)

from .pages import home  # noqa: E402
from .pages.advanced import (  # noqa: E402
    component_dev,
    extension_dev,
    security,
    sessions,
)
from .pages.components import (  # noqa: E402
    base,
    buttons,
    cards,
    charts,
    data_display,
    feedback,
    inputs,
    layout,
    navigation,
    typography,
    utility,
)
from .pages.components.buttons import (  # noqa: E402
    button,
    context_menu,
    dropdown_menu,
    icon_button,
    slider,
    switch,
    toggle,
)
from .pages.components.cards import (  # noqa: E402
    card as card_page,
)
from .pages.components.cards import (
    collapsible as collapsible_page,
)
from .pages.components.charts import (  # noqa: E402
    area_chart as area_chart_page,
)
from .pages.components.charts import (
    bar_chart as bar_chart_page,
)
from .pages.components.charts import (
    line_chart as line_chart_page,
)
from .pages.components.charts import (
    other_charts as other_charts_page,
)
from .pages.components.charts import (
    pie_chart as pie_chart_page,
)
from .pages.components.data_display import (  # noqa: E402
    accordion as accordion_page,
)
from .pages.components.data_display import (
    avatar as avatar_page,
)
from .pages.components.data_display import (
    data_table as data_table_page,
)
from .pages.components.data_display import (
    hover_card as hover_card_page,
)
from .pages.components.data_display import (
    list_component as list_page,
)
from .pages.components.data_display import (
    table as table_page,
)
from .pages.components.data_display import (
    tabs as tabs_page,
)
from .pages.components.data_display import (
    tooltip as tooltip_page,
)
from .pages.components.feedback import (  # noqa: E402
    alert as alert_page,
)
from .pages.components.feedback import (
    dialog as dialog_page,
)
from .pages.components.feedback import (
    popover as popover_page,
)
from .pages.components.feedback import (
    progress as progress_page,
)
from .pages.components.feedback import (
    sheet as sheet_page,
)
from .pages.components.form_inputs import (  # noqa: E402
    checkbox,
    combobox,
    date_picker,
    input_otp,
    radio,
    textarea,
)
from .pages.components.form_inputs import (
    form as form_input_page,
)
from .pages.components.form_inputs import (
    input as input_page,
)
from .pages.components.form_inputs import (
    select as select_page,
)
from .pages.components.layout import (  # noqa: E402
    column,
    container,
    flex,
    grid,
    resizable,
    row,
    scroll_area,
)
from .pages.components.navigation import (  # noqa: E402
    breadcrumb as breadcrumb_page,
)
from .pages.components.navigation import (
    navigation_menu as navigation_menu_page,
)
from .pages.components.navigation import (
    pagination as pagination_page,
)
from .pages.components.navigation import (
    sidebar_nav as sidebar_nav_page,
)
from .pages.components.typography import (
    badge as badge_page,
)
from .pages.components.typography import (
    blockquote as blockquote_page,
)
from .pages.components.typography import (
    code as code_page,
)
from .pages.components.typography import (  # noqa: E402
    heading,
)
from .pages.components.typography import (
    kbd as kbd_page,
)
from .pages.components.typography import (
    link as link_page,
)
from .pages.components.typography import (
    markdown as markdown_page,
)
from .pages.components.typography import (
    text as text_page,
)
from .pages.components.utility import (  # noqa: E402
    aspect_ratio as aspect_ratio_page,
)
from .pages.components.utility import (
    carousel as carousel_page,
)
from .pages.components.utility import (
    keyboard_shortcut as keyboard_shortcut_page,
)
from .pages.components.utility import (
    separator as separator_page,
)
from .pages.components.utility import (
    timer as timer_page,
)
from .pages.concepts import (  # noqa: E402
    background,
    bundle_splitting,
    callbacks,
    file_transfers,
    js_interop,
    routing,
    state,
    streaming,
    styling,
    theming,
    toasts,
    updates,
)
from .pages.concepts import (
    components as concepts_components,
)
from .pages.getting_started import (  # noqa: E402
    architecture,
    examples_gallery,
    installation,
    quick_tour,
    todo_app_live,
)

# ── App instance ─────────────────────────────────────────────────────────

ui = RefastApp(
    title="Refast Docs",
    theme=default_theme,
    favicon="📖",
    custom_css="/styles/main.css",
)

# ── Navigation structure ─────────────────────────────────────────────────
# Each section has a label, icon, and list of pages.
# Pages are (label, route, icon) tuples.

NAV_SECTIONS = [
    {
        "label": "Getting Started",
        "icon": "rocket",
        "pages": [
            ("Installation", "/docs/getting-started", "download"),
            ("Architecture", "/docs/architecture", "layers"),
            ("Quick Tour", "/docs/quick-tour", "zap"),
            ("Live Todo Demo", "/docs/todo-live", "check-circle"),
            ("Examples Gallery", "/docs/examples", "grid-3x3"),
        ],
    },
    {
        "label": "Core Concepts",
        "icon": "layers",
        "pages": [
            ("Components", "/docs/concepts/components", "box"),
            ("Callbacks & Events", "/docs/concepts/callbacks", "mouse-pointer-click"),
            ("State & Store", "/docs/concepts/state", "database"),
            ("DOM Updates", "/docs/concepts/updates", "refresh-cw"),
            ("Routing & Navigation", "/docs/concepts/routing", "route"),
            ("Streaming", "/docs/concepts/streaming", "radio"),
            ("Background Jobs", "/docs/concepts/background", "clock"),
            ("Theming", "/docs/concepts/theming", "palette"),
            ("Styling", "/docs/concepts/styling", "paintbrush"),
            ("Toast Notifications", "/docs/concepts/toasts", "bell"),
            ("JavaScript Interop", "/docs/concepts/js-interop", "code"),
            ("File Uploads & Downloads", "/docs/concepts/file-transfers", "upload"),
            ("Bundle Splitting", "/docs/concepts/bundle-splitting", "package"),
        ],
    },
    {
        "label": "Components",
        "icon": "component",
        "groups": [
            {
                "label": "Foundations",
                "icon": "box",
                "pages": [
                    ("Base", "/docs/components/base", "box"),
                    ("Container", "/docs/components/container", "panel-left"),
                ],
            },
            {
                "label": "Layout",
                "icon": "layout",
                "pages": [
                    ("Row", "/docs/components/row", "rows"),
                    ("Column", "/docs/components/column", "columns"),
                    ("Flex", "/docs/components/flex", "expand"),
                    ("Grid", "/docs/components/grid", "layout-grid"),
                    ("Scroll Area", "/docs/components/scroll-area", "layout-list"),
                    ("Resizable", "/docs/components/resizable", "grip-horizontal"),
                ],
            },
            {
                "label": "Typography",
                "icon": "type",
                "pages": [
                    ("Heading", "/docs/components/heading", "type"),
                    ("Text & Paragraph", "/docs/components/text", "type"),
                    ("Code", "/docs/components/code", "code"),
                    ("Link", "/docs/components/link", "link"),
                    ("Markdown", "/docs/components/markdown", "file-text"),
                    ("BlockQuote", "/docs/components/blockquote", "quote"),
                    ("Badge", "/docs/components/badge", "tag"),
                    ("Kbd", "/docs/components/kbd", "terminal"),
                ],
            },
            {
                "label": "Buttons & Actions",
                "icon": "mouse-pointer-click",
                "pages": [
                    ("Button", "/docs/components/button", "square"),
                    ("Icon Button", "/docs/components/icon-button", "circle"),
                    ("Toggle", "/docs/components/toggle", "check-square"),
                    ("Switch", "/docs/components/switch", "check-circle"),
                    ("Slider", "/docs/components/slider", "sliders"),
                    ("Dropdown Menu", "/docs/components/dropdown-menu", "chevron-down"),
                    ("Context Menu", "/docs/components/context-menu", "mouse-pointer-click"),
                ],
            },
            {
                "label": "Form Inputs",
                "icon": "text-cursor-input",
                "pages": [
                    ("Input", "/docs/components/input", "text-cursor-input"),
                    ("Textarea", "/docs/components/textarea", "edit"),
                    ("Select", "/docs/components/select", "chevrons-down"),
                    ("Checkbox", "/docs/components/checkbox", "check-square"),
                    ("Radio", "/docs/components/radio", "circle-dot"),
                    ("Combobox", "/docs/components/combobox", "search"),
                    ("Date Picker", "/docs/components/date-picker", "calendar"),
                    ("Input OTP", "/docs/components/input-otp", "shield-check"),
                    ("Form", "/docs/components/form", "clipboard"),
                ],
            },
            {
                "label": "Cards & Containers",
                "icon": "credit-card",
                "pages": [
                    ("Card", "/docs/components/card", "credit-card"),
                    ("Collapsible", "/docs/components/collapsible", "chevron-down"),
                ],
            },
            {
                "label": "Data Display",
                "icon": "table",
                "pages": [
                    ("Table", "/docs/components/table", "table"),
                    ("Data Table", "/docs/components/data-table", "table"),
                    ("Tabs", "/docs/components/tabs", "panel-top"),
                    ("Accordion", "/docs/components/accordion", "layout-list"),
                    ("Avatar", "/docs/components/avatar", "user"),
                    ("Tooltip", "/docs/components/tooltip", "info"),
                    ("Hover Card", "/docs/components/hover-card", "credit-card"),
                    ("List", "/docs/components/list", "layout-list"),
                ],
            },
            {
                "label": "Navigation",
                "icon": "compass",
                "pages": [
                    ("Breadcrumb", "/docs/components/breadcrumb", "more-horizontal"),
                    ("Sidebar", "/docs/components/sidebar-nav", "panel-left"),
                    ("Pagination", "/docs/components/pagination", "more-horizontal"),
                    ("Navigation Menu", "/docs/components/navigation-menu", "menu"),
                ],
            },
            {
                "label": "Feedback & Overlay",
                "icon": "message-square",
                "pages": [
                    ("Alert", "/docs/components/alert", "alert-triangle"),
                    ("Progress & Spinner", "/docs/components/progress", "loader"),
                    ("Dialog", "/docs/components/dialog", "x-circle"),
                    ("Sheet", "/docs/components/sheet", "panel-right"),
                    ("Popover", "/docs/components/popover", "message-square"),
                ],
            },
            {
                "label": "Charts",
                "icon": "bar-chart-3",
                "pages": [
                    ("Bar Chart", "/docs/components/bar-chart", "bar-chart"),
                    ("Line Chart", "/docs/components/line-chart", "line-chart"),
                    ("Area Chart", "/docs/components/area-chart", "activity"),
                    ("Pie Chart", "/docs/components/pie-chart", "pie-chart"),
                    ("Other Charts", "/docs/components/other-charts", "bar-chart-2"),
                ],
            },
            {
                "label": "Utility",
                "icon": "wrench",
                "pages": [
                    ("Separator", "/docs/components/separator", "minus"),
                    ("Aspect Ratio", "/docs/components/aspect-ratio", "maximize"),
                    ("Carousel", "/docs/components/carousel", "image"),
                    ("Keyboard Shortcut", "/docs/components/keyboard-shortcut", "keyboard"),
                    ("Timer", "/docs/components/timer", "timer"),
                ],
            },
        ],
    },
    {
        "label": "Advanced",
        "icon": "settings",
        "pages": [
            ("Building Components", "/docs/advanced/component-dev", "hammer"),
            ("Building Extensions", "/docs/advanced/extension-dev", "puzzle"),
            ("Security", "/docs/advanced/security", "shield"),
            ("Sessions", "/docs/advanced/sessions", "key"),
        ],
    },
]

# Build flat lookup: route -> (section_label, page_label)
_PAGE_LOOKUP: dict[str, tuple[str, str]] = {}
for _section in NAV_SECTIONS:
    if "groups" in _section:
        for _group in _section["groups"]:
            for _label, _route, _icon in _group["pages"]:
                _PAGE_LOOKUP[_route] = (_section["label"], _label)
    else:
        for _label, _route, _icon in _section["pages"]:
            _PAGE_LOOKUP[_route] = (_section["label"], _label)


# ── Navigation callback ─────────────────────────────────────────────────


async def nav(ctx: Context, path: str = "/"):
    """Navigate to a documentation page."""
    ctx.state["search_open"] = False
    await ctx.load(path)


async def open_search(ctx: Context, current_path: str = "/"):
    """Open the search dialog."""
    ctx.state["search_open"] = True
    await ctx.load(current_path)


async def close_search(ctx: Context, current_path: str = "/"):
    """Close the search dialog."""
    ctx.state["search_open"] = False
    await ctx.load(current_path)


async def search_navigate(ctx: Context, path: str = "/"):
    """Navigate from a search result and close the dialog."""
    ctx.state["search_open"] = False
    await ctx.load(path)


# ── Search helpers ───────────────────────────────────────────────────────


def _get_search_items() -> list[dict]:
    """Flatten NAV_SECTIONS into a list of searchable items grouped by section."""
    items: list[dict] = []
    for section in NAV_SECTIONS:
        group_label = section["label"]
        if "groups" in section:
            for group in section["groups"]:
                for label, route, icon in group["pages"]:
                    items.append({"label": label, "route": route, "icon": icon, "group": group_label})
        else:
            for label, route, icon in section["pages"]:
                items.append({"label": label, "route": route, "icon": icon, "group": group_label})
    return items


_SEARCH_ITEMS = _get_search_items()


def _build_search_dialog(ctx: Context, current_path: str):
    """Build the CMD+K search dialog overlay."""
    is_open = ctx.state.get("search_open", False)

    # Group items by section label
    groups: dict[str, list[dict]] = {}
    for item in _SEARCH_ITEMS:
        groups.setdefault(item["group"], []).append(item)

    command_groups = []
    for group_label, group_items in groups.items():
        command_groups.append(
            CommandGroup(
                heading=group_label,
                children=[
                    CommandItem(
                        label=item["label"],
                        value=item["label"],
                        icon=item["icon"],
                        on_select=ctx.callback(search_navigate, path=item["route"]),
                    )
                    for item in group_items
                ],
            )
        )

    return Dialog(
        open=is_open,
        on_open_change=ctx.callback(close_search, current_path=current_path),
        children=[
            DialogContent(
                class_name="p-0 overflow-hidden gap-0 max-w-lg",
                children=[
                    Command(
                        class_name="rounded-lg border-0 shadow-none",
                        children=[
                            CommandInput(placeholder="Search docs..."),
                            CommandList(
                                children=[
                                    CommandEmpty(message="No pages found."),
                                    *command_groups,
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# ── Shared layout ────────────────────────────────────────────────────────


def docs_layout(ctx: Context, content, current_path: str = "/"):
    """Wrap page content in the documentation layout with sidebar navigation.

    Args:
        ctx: The request context.
        content: The page content component tree.
        current_path: Current page route for active-state highlighting.
    """
    # Use path-specific ID for content container to force scroll reset on navigation
    safe_path = current_path.replace("/", "-").strip("-") or "home"
    content_id = f"docs-content-{safe_path}"

    return SidebarProvider(
        id="docs-sidebar-provider",
        children=[
            _build_sidebar(ctx, current_path),
            SidebarInset(
                id="docs-sidebar-inset",
                class_name="min-w-0",
                children=[
                    _build_topbar(ctx, current_path),
                    Container(
                        id=content_id,
                        class_name="flex-1 min-w-0 overflow-y-auto overflow-x-hidden",
                        children=[content],
                    ),
                    _build_footer(ctx, current_path),
                ],
            ),
            _build_search_dialog(ctx, current_path),
            KeyboardShortcut(
                shortcuts={"ctrl+k": ctx.callback(open_search, current_path=current_path)},
                priority=10,
                prevent_default=True,
            ),
            ConnectionStatus(),
        ],
    )


def _build_sidebar(ctx: Context, current_path: str):
    """Build the sidebar with all navigation sections."""
    return Sidebar(
        id="docs-sidebar",
        collapsible="icon",
        children=[
            # Header — brand
            SidebarHeader(
                id="docs-sidebar-header",
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                id="docs-brand-item",
                                children=[
                                    SidebarMenuButton(
                                        "Refast Docs",
                                        icon="layers",
                                        size="lg",
                                        is_active=(current_path == "/"),
                                        on_click=ctx.callback(nav, path="/"),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            SidebarSeparator(),
            # Navigation sections
            SidebarContent(
                id="docs-sidebar-content",
                children=[_build_nav_group(ctx, section, current_path) for section in NAV_SECTIONS],
            ),
            SidebarSeparator(),
            # Footer — version + theme
            SidebarFooter(
                id="docs-sidebar-footer",
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                id="docs-footer-item",
                                children=[
                                    Row(
                                        [
                                            SidebarMenuButton(
                                                "v0.1.0",
                                                icon="tag",
                                                size="sm",
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            SidebarRail(),
        ],
    )


def _build_nav_group(ctx: Context, section: dict, current_path: str):
    """Build a single navigation group in the sidebar."""
    section_id = section["label"].lower().replace(" ", "-")

    if "groups" in section:
        # Nested groups structure (Components section)
        menu_items = [
            _build_nav_subgroup(ctx, group, current_path)
            for group in section["groups"]
        ]
        return SidebarGroup(
            id=f"nav-group-{section_id}",
            children=[
                SidebarGroupLabel(section["label"]),
                SidebarGroupContent(
                    children=[SidebarMenu(children=menu_items)],
                ),
            ],
        )

    return SidebarGroup(
        id=f"nav-group-{section_id}",
        children=[
            SidebarGroupLabel(section["label"]),
            SidebarGroupContent(
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                id=f"nav-item-{route.strip('/').replace('/', '-')}",
                                children=[
                                    Tooltip(
                                        children=[
                                            SidebarMenuButton(
                                                label,
                                                icon=icon,
                                                is_active=(current_path == route),
                                                on_click=ctx.callback(nav, path=route),
                                            ),
                                        ],
                                        content=label,
                                        side="right",
                                    )
                                ],
                            )
                            for label, route, icon in section["pages"]
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_nav_subgroup(ctx: Context, group: dict, current_path: str):
    """Build a collapsible sub-group with SidebarMenuSub items."""
    group_id = group["label"].lower().replace(" ", "-")
    is_any_active = any(route == current_path for _, route, _ in group["pages"])

    return SidebarMenuItem(
        id=f"nav-subgroup-{group_id}",
        children=[
            SidebarMenuButton(
                group["label"],
                icon=group.get("icon"),
                is_active=is_any_active,
            ),
            SidebarMenuSub(
                children=[
                    SidebarMenuSubItem(
                        id=f"nav-sub-{route.strip('/').replace('/', '-')}",
                        children=[
                            SidebarMenuSubButton(
                                label,
                                is_active=(current_path == route),
                                on_click=ctx.callback(nav, path=route),
                            )
                        ],
                    )
                    for label, route, _ in group["pages"]
                ],
            ),
        ],
    )


async def _on_theme_change(ctx: Context, theme_name: str):
    """Handle theme change from the theme switcher."""
    theme_map = {
        "default": default_theme,
        "caffine": caffine_theme,
        "catppuccin": catppuccin_theme,
        "ocean-breeze": ocean_breeze_theme,
        "amber-minimal": amber_minimal_theme,
    }
    selected_theme = theme_map.get(theme_name, default_theme)
    await ctx.set_theme(selected_theme)


def theme_switcher(ctx: Context):
    return DropdownMenu(
        children=[
            DropdownMenuTrigger(
                IconButton(
                    icon="palette",
                    variant="ghost",
                    size="sm",
                )
            ),
            DropdownMenuContent(
                children=[
                    DropdownMenuItem(
                        theme.title(), on_select=ctx.callback(_on_theme_change, theme_name=theme)
                    )
                    for theme in [
                        "default",
                        "caffine",
                        "catppuccin",
                        "ocean-breeze",
                        "amber-minimal",
                    ]
                ]
            ),
        ]
    )


def _build_topbar(ctx: Context, current_path: str):
    """Build the top bar with breadcrumb and theme toggle."""
    # Build breadcrumb from current path
    crumbs = [("Docs", "/")]
    info = _PAGE_LOOKUP.get(current_path)
    if info:
        section_label, page_label = info
        crumbs.append((section_label, None))
        crumbs.append((page_label, current_path))

    breadcrumb_items = []
    for i, (label, route) in enumerate(crumbs):
        if i > 0:
            breadcrumb_items.append(BreadcrumbSeparator())
        if route and i < len(crumbs) - 1:
            breadcrumb_items.append(BreadcrumbItem(children=[BreadcrumbLink(label, href=route)]))
        else:
            breadcrumb_items.append(BreadcrumbItem(children=[BreadcrumbPage(label)]))

    return Container(
        id="docs-topbar",
        class_name="border-b px-4 py-3 sticky top-0 bg-background z-10",
        children=[
            Row(
                align="center",
                justify="between",
                children=[
                    Row(
                        [
                            SidebarTrigger(),
                            Separator(orientation="vertical", class_name="h-6"),
                            Breadcrumb(children=[BreadcrumbList(children=breadcrumb_items)]),
                        ],
                        align="center",
                        gap=4,
                    ),
                    Row(
                        [
                            Button(
                                "Search docs...(Ctrl+K)",
                                icon="search",
                                variant="outline",
                                size="sm",
                                class_name="text-muted-foreground justify-start font-normal",
                                style={"width": "180px"},
                                on_click=ctx.callback(open_search, current_path=current_path),
                            ),
                            ThemeSwitcher(),
                            # Text(
                            #     f"Active users: {len(ui.active_contexts)}",
                            #     class_name="text-sm text-muted-foreground",
                            # )
                            theme_switcher(ctx),
                        ],
                        align="center",
                        gap=2,
                    ),
                ],
            ),
        ],
    )


def _build_footer(ctx: Context, current_path: str):
    """Build prev/next navigation footer."""
    # Find current page index in flat list
    all_pages = []
    for section in NAV_SECTIONS:
        if "groups" in section:
            for group in section["groups"]:
                for label, route, _icon in group["pages"]:
                    all_pages.append((label, route))
        else:
            for label, route, _icon in section["pages"]:
                all_pages.append((label, route))

    current_idx = None
    for i, (label, route) in enumerate(all_pages):
        if route == current_path:
            current_idx = i
            break

    prev_btn = Container()  # empty spacer
    next_btn = Container()

    if current_idx is not None:
        if current_idx > 0:
            prev_label, prev_route = all_pages[current_idx - 1]
            prev_btn = Button(
                f"← {prev_label}",
                variant="ghost",
                on_click=ctx.callback(nav, path=prev_route),
            )
        if current_idx < len(all_pages) - 1:
            next_label, next_route = all_pages[current_idx + 1]
            next_btn = Button(
                f"{next_label} →",
                variant="ghost",
                on_click=ctx.callback(nav, path=next_route),
            )

    return Container(
        id="docs-page-footer",
        class_name="border-t px-6 py-4 mt-8",
        children=[
            Flex(
                direction="row",
                justify="between",
                children=[prev_btn, next_btn],
            ),
        ],
    )


# ── Register all pages ───────────────────────────────────────────────────


@ui.page("/")
def page_home(ctx: Context):
    return home.render(ctx)


# Getting Started
@ui.page("/docs/getting-started")
def page_getting_started(ctx: Context):
    return installation.render(ctx)


@ui.page("/docs/architecture")
def page_architecture(ctx: Context):
    return architecture.render(ctx)


@ui.page("/docs/quick-tour")
def page_quick_tour(ctx: Context):
    return quick_tour.render(ctx)


@ui.page("/docs/todo-live")
def page_todo_live(ctx: Context):
    return todo_app_live.render(ctx)


@ui.page("/docs/examples")
def page_examples(ctx: Context):
    return examples_gallery.render(ctx)


# Core Concepts
@ui.page("/docs/concepts/components")
def page_concepts_components(ctx: Context):
    return concepts_components.render(ctx)


@ui.page("/docs/concepts/callbacks")
def page_concepts_callbacks(ctx: Context):
    return callbacks.render(ctx)


@ui.page("/docs/concepts/state")
def page_concepts_state(ctx: Context):
    return state.render(ctx)


@ui.page("/docs/concepts/updates")
def page_concepts_updates(ctx: Context):
    return updates.render(ctx)


@ui.page("/docs/concepts/routing")
def page_concepts_routing(ctx: Context):
    return routing.render(ctx)


@ui.page("/docs/concepts/streaming")
def page_concepts_streaming(ctx: Context):
    return streaming.render(ctx)


@ui.page("/docs/concepts/background")
def page_concepts_background(ctx: Context):
    return background.render(ctx)


@ui.page("/docs/concepts/theming")
def page_concepts_theming(ctx: Context):
    return theming.render(ctx)


@ui.page("/docs/concepts/toasts")
def page_concepts_toasts(ctx: Context):
    return toasts.render(ctx)


@ui.page("/docs/concepts/js-interop")
def page_concepts_js_interop(ctx: Context):
    return js_interop.render(ctx)


@ui.page("/docs/concepts/file-transfers")
def page_concepts_file_transfers(ctx: Context):
    return file_transfers.render(ctx)


@ui.page("/docs/concepts/bundle-splitting")
def page_concepts_bundle_splitting(ctx: Context):
    return bundle_splitting.render(ctx)


# Component Reference
@ui.page("/docs/components/base")
def page_components_base(ctx: Context):
    return base.render(ctx)


@ui.page("/docs/components/layout")
def page_components_layout(ctx: Context):
    return layout.render(ctx)


@ui.page("/docs/components/container")
def page_components_container(ctx: Context):
    return container.render(ctx)


@ui.page("/docs/components/row")
def page_components_row(ctx: Context):
    return row.render(ctx)


@ui.page("/docs/components/column")
def page_components_column(ctx: Context):
    return column.render(ctx)


@ui.page("/docs/components/flex")
def page_components_flex(ctx: Context):
    return flex.render(ctx)


@ui.page("/docs/components/grid")
def page_components_grid(ctx: Context):
    return grid.render(ctx)


@ui.page("/docs/components/scroll-area")
def page_components_scroll_area(ctx: Context):
    return scroll_area.render(ctx)


@ui.page("/docs/components/resizable")
def page_components_resizable(ctx: Context):
    return resizable.render(ctx)


@ui.page("/docs/components/typography")
def page_components_typography(ctx: Context):
    return typography.render(ctx)


@ui.page("/docs/components/heading")
def page_components_heading(ctx: Context):
    return heading.render(ctx)


@ui.page("/docs/components/text")
def page_components_text(ctx: Context):
    return text_page.render(ctx)


@ui.page("/docs/components/code")
def page_components_code(ctx: Context):
    return code_page.render(ctx)


@ui.page("/docs/components/link")
def page_components_link(ctx: Context):
    return link_page.render(ctx)


@ui.page("/docs/components/markdown")
def page_components_markdown(ctx: Context):
    return markdown_page.render(ctx)


@ui.page("/docs/components/badge")
def page_components_badge(ctx: Context):
    return badge_page.render(ctx)


@ui.page("/docs/components/blockquote")
def page_components_blockquote(ctx: Context):
    return blockquote_page.render(ctx)


@ui.page("/docs/components/kbd")
def page_components_kbd(ctx: Context):
    return kbd_page.render(ctx)


@ui.page("/docs/components/buttons")
def page_components_buttons(ctx: Context):
    return buttons.render(ctx)


@ui.page("/docs/components/button")
def page_components_button(ctx: Context):
    return button.render(ctx)


@ui.page("/docs/components/icon-button")
def page_components_icon_button(ctx: Context):
    return icon_button.render(ctx)


@ui.page("/docs/components/toggle")
def page_components_toggle(ctx: Context):
    return toggle.render(ctx)


@ui.page("/docs/components/switch")
def page_components_switch(ctx: Context):
    return switch.render(ctx)


@ui.page("/docs/components/slider")
def page_components_slider(ctx: Context):
    return slider.render(ctx)


@ui.page("/docs/components/dropdown-menu")
def page_components_dropdown_menu(ctx: Context):
    return dropdown_menu.render(ctx)


@ui.page("/docs/components/context-menu")
def page_components_context_menu(ctx: Context):
    return context_menu.render(ctx)


@ui.page("/docs/components/inputs")
def page_components_inputs(ctx: Context):
    return inputs.render(ctx)


@ui.page("/docs/components/input")
def page_components_input(ctx: Context):
    return input_page.render(ctx)


@ui.page("/docs/components/textarea")
def page_components_textarea(ctx: Context):
    return textarea.render(ctx)


@ui.page("/docs/components/select")
def page_components_select(ctx: Context):
    return select_page.render(ctx)


@ui.page("/docs/components/checkbox")
def page_components_checkbox(ctx: Context):
    return checkbox.render(ctx)


@ui.page("/docs/components/radio")
def page_components_radio(ctx: Context):
    return radio.render(ctx)


@ui.page("/docs/components/combobox")
def page_components_combobox(ctx: Context):
    return combobox.render(ctx)


@ui.page("/docs/components/date-picker")
def page_components_date_picker(ctx: Context):
    return date_picker.render(ctx)


@ui.page("/docs/components/input-otp")
def page_components_input_otp(ctx: Context):
    return input_otp.render(ctx)


@ui.page("/docs/components/form")
def page_components_form(ctx: Context):
    return form_input_page.render(ctx)


@ui.page("/docs/components/cards")
def page_components_cards(ctx: Context):
    return cards.render(ctx)


@ui.page("/docs/components/card")
def page_components_card(ctx: Context):
    return card_page.render(ctx)


@ui.page("/docs/components/collapsible")
def page_components_collapsible(ctx: Context):
    return collapsible_page.render(ctx)


@ui.page("/docs/components/data-display")
def page_components_data_display(ctx: Context):
    return data_display.render(ctx)


@ui.page("/docs/components/table")
def page_components_table(ctx: Context):
    return table_page.render(ctx)


@ui.page("/docs/components/tabs")
def page_components_tabs(ctx: Context):
    return tabs_page.render(ctx)


@ui.page("/docs/components/accordion")
def page_components_accordion(ctx: Context):
    return accordion_page.render(ctx)


@ui.page("/docs/components/avatar")
def page_components_avatar(ctx: Context):
    return avatar_page.render(ctx)


@ui.page("/docs/components/tooltip")
def page_components_tooltip(ctx: Context):
    return tooltip_page.render(ctx)


@ui.page("/docs/components/list")
def page_components_list(ctx: Context):
    return list_page.render(ctx)


@ui.page("/docs/components/data-table")
def page_components_data_table(ctx: Context):
    return data_table_page.render(ctx)


@ui.page("/docs/components/hover-card")
def page_components_hover_card(ctx: Context):
    return hover_card_page.render(ctx)


@ui.page("/docs/components/navigation")
def page_components_navigation(ctx: Context):
    return navigation.render(ctx)


@ui.page("/docs/components/breadcrumb")
def page_components_breadcrumb(ctx: Context):
    return breadcrumb_page.render(ctx)


@ui.page("/docs/components/sidebar-nav")
def page_components_sidebar_nav(ctx: Context):
    return sidebar_nav_page.render(ctx)


@ui.page("/docs/components/pagination")
def page_components_pagination(ctx: Context):
    return pagination_page.render(ctx)


@ui.page("/docs/components/navigation-menu")
def page_components_navigation_menu(ctx: Context):
    return navigation_menu_page.render(ctx)


@ui.page("/docs/components/feedback")
def page_components_feedback(ctx: Context):
    return feedback.render(ctx)


@ui.page("/docs/components/alert")
def page_components_alert(ctx: Context):
    return alert_page.render(ctx)


@ui.page("/docs/components/progress")
def page_components_progress(ctx: Context):
    return progress_page.render(ctx)


@ui.page("/docs/components/dialog")
def page_components_dialog(ctx: Context):
    return dialog_page.render(ctx)


@ui.page("/docs/components/sheet")
def page_components_sheet(ctx: Context):
    return sheet_page.render(ctx)


@ui.page("/docs/components/popover")
def page_components_popover(ctx: Context):
    return popover_page.render(ctx)


@ui.page("/docs/components/charts")
def page_components_charts(ctx: Context):
    return charts.render(ctx)


@ui.page("/docs/components/bar-chart")
def page_components_bar_chart(ctx: Context):
    return bar_chart_page.render(ctx)


@ui.page("/docs/components/line-chart")
def page_components_line_chart(ctx: Context):
    return line_chart_page.render(ctx)


@ui.page("/docs/components/area-chart")
def page_components_area_chart(ctx: Context):
    return area_chart_page.render(ctx)


@ui.page("/docs/components/pie-chart")
def page_components_pie_chart(ctx: Context):
    return pie_chart_page.render(ctx)


@ui.page("/docs/components/other-charts")
def page_components_other_charts(ctx: Context):
    return other_charts_page.render(ctx)


@ui.page("/docs/components/utility")
def page_components_utility(ctx: Context):
    return utility.render(ctx)


@ui.page("/docs/components/separator")
def page_components_separator(ctx: Context):
    return separator_page.render(ctx)


@ui.page("/docs/components/aspect-ratio")
def page_components_aspect_ratio(ctx: Context):
    return aspect_ratio_page.render(ctx)


@ui.page("/docs/components/carousel")
def page_components_carousel(ctx: Context):
    return carousel_page.render(ctx)


@ui.page("/docs/components/keyboard-shortcut")
def page_components_keyboard_shortcut(ctx: Context):
    return keyboard_shortcut_page.render(ctx)


@ui.page("/docs/components/timer")
def page_components_timer(ctx: Context):
    return timer_page.render(ctx)


# Advanced
@ui.page("/docs/advanced/component-dev")
def page_advanced_component_dev(ctx: Context):
    return component_dev.render(ctx)


@ui.page("/docs/advanced/extension-dev")
def page_advanced_extension_dev(ctx: Context):
    return extension_dev.render(ctx)


@ui.page("/docs/advanced/security")
def page_advanced_security(ctx: Context):
    return security.render(ctx)


@ui.page("/docs/advanced/sessions")
def page_advanced_sessions(ctx: Context):
    return sessions.render(ctx)


@ui.page("/docs/concepts/styling")
def page_concepts_styling(ctx: Context):
    return styling.render(ctx)


# ── FastAPI app ──────────────────────────────────────────────────────────

app = FastAPI(title="Refast Documentation")
app.mount(
    "/styles", StaticFiles(directory=Path(__file__).parent / "styles"), name="styles"
)  # serve custom CSS and JS
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
