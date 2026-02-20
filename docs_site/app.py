"""Refast Documentation Site.

A comprehensive documentation site for the Refast framework, built with Refast itself.

Run:
    cd <project_root>
    uvicorn docs_site.app:app --reload
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    Button,
    Container,
    Flex,
    Heading,
    Icon,
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
    Text,
    Tooltip,
)
from refast.components.shadcn import ThemeSwitcher
from refast.theme import default_theme

# ── App instance ─────────────────────────────────────────────────────────

ui = RefastApp(
    title="Refast Docs",
    theme=default_theme,
    favicon="📖",
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
            ("Examples Gallery", "/docs/examples", "grid-3x3"),
        ],
    },
    {
        "label": "Core Concepts",
        "icon": "book-open",
        "pages": [
            ("Components", "/docs/concepts/components", "box"),
            ("Callbacks & Events", "/docs/concepts/callbacks", "mouse-pointer-click"),
            ("State Management", "/docs/concepts/state", "database"),
            ("Store (Browser)", "/docs/concepts/store", "hard-drive"),
            ("DOM Updates", "/docs/concepts/updates", "refresh-cw"),
            ("Routing & Navigation", "/docs/concepts/routing", "route"),
            ("Streaming", "/docs/concepts/streaming", "radio"),
            ("Background Jobs", "/docs/concepts/background", "clock"),
            ("Theming", "/docs/concepts/theming", "palette"),
            ("Toast Notifications", "/docs/concepts/toasts", "bell"),
            ("JavaScript Interop", "/docs/concepts/js-interop", "code"),
        ],
    },
    {
        "label": "Components",
        "icon": "component",
        "pages": [
            ("Layout", "/docs/components/layout", "layout"),
            ("Typography", "/docs/components/typography", "type"),
            ("Buttons & Actions", "/docs/components/buttons", "square"),
            ("Form Inputs", "/docs/components/inputs", "text-cursor-input"),
            ("Cards & Containers", "/docs/components/cards", "credit-card"),
            ("Data Display", "/docs/components/data-display", "table"),
            ("Navigation", "/docs/components/navigation", "compass"),
            ("Feedback & Overlay", "/docs/components/feedback", "message-square"),
            ("Charts", "/docs/components/charts", "bar-chart-3"),
            ("Utility", "/docs/components/utility", "wrench"),
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
            ("Styling", "/docs/advanced/styling", "paintbrush"),
        ],
    },
]

# Build flat lookup: route -> (section_label, page_label)
_PAGE_LOOKUP: dict[str, tuple[str, str]] = {}
for section in NAV_SECTIONS:
    for label, route, _icon in section["pages"]:
        _PAGE_LOOKUP[route] = (section["label"], label)


# ── Navigation callback ─────────────────────────────────────────────────


async def nav(ctx: Context, path: str = "/"):
    """Navigate to a documentation page."""
    await ctx.navigate(path)


# ── Shared layout ────────────────────────────────────────────────────────


def docs_layout(ctx: Context, content, current_path: str = "/"):
    """Wrap page content in the documentation layout with sidebar navigation.

    Args:
        ctx: The request context.
        content: The page content component tree.
        current_path: Current page route for active-state highlighting.
    """
    return SidebarProvider(
        children=[
            _build_sidebar(ctx, current_path),
            SidebarInset(
                children=[
                    _build_topbar(ctx, current_path),
                    Container(
                        id="docs-content",
                        class_name="flex-1 overflow-auto",
                        children=[content],
                    ),
                    _build_footer(ctx, current_path),
                ],
            ),
        ],
    )


def _build_sidebar(ctx: Context, current_path: str):
    """Build the sidebar with all navigation sections."""
    return Sidebar(
        collapsible="icon",
        children=[
            # Header — brand
            SidebarHeader(
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                children=[
                                    SidebarMenuButton(
                                        "Refast Docs",
                                        icon="book-open",
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
                children=[_build_nav_group(ctx, section, current_path) for section in NAV_SECTIONS],
            ),
            SidebarSeparator(),
            # Footer — version + theme
            SidebarFooter(
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
                                children=[
                                    Row(
                                        [
                                            SidebarMenuButton(
                                                "v0.1.0",
                                                icon="tag",
                                                size="sm",
                                            ),
                                            ThemeSwitcher(),
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
    return SidebarGroup(
        children=[
            SidebarGroupLabel(section["label"]),
            SidebarGroupContent(
                children=[
                    SidebarMenu(
                        children=[
                            SidebarMenuItem(
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
        class_name="border-b px-4 py-3 sticky top-0 bg-background z-10",
        children=[
            Flex(
                direction="row",
                align="center",
                gap=4,
                children=[
                    SidebarTrigger(),
                    Separator(orientation="vertical", class_name="h-6"),
                    Breadcrumb(children=[BreadcrumbList(children=breadcrumb_items)]),
                ],
            ),
        ],
    )


def _build_footer(ctx: Context, current_path: str):
    """Build prev/next navigation footer."""
    # Find current page index in flat list
    all_pages = []
    for section in NAV_SECTIONS:
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
        class_name="border-t px-6 py-4 mt-8",
        children=[
            Flex(
                direction="row",
                justify="between",
                children=[prev_btn, next_btn],
            ),
        ],
    )


# ── Import all page modules ─────────────────────────────────────────────

from .pages import home  # noqa: E402
from .pages.getting_started import (  # noqa: E402
    architecture,
    examples_gallery,
    installation,
    quick_tour,
)
from .pages.concepts import (  # noqa: E402
    background,
    callbacks,
    components as concepts_components,
    js_interop,
    routing,
    state,
    store,
    streaming,
    theming,
    toasts,
    updates,
)
from .pages.components import (  # noqa: E402
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
from .pages.advanced import (  # noqa: E402
    component_dev,
    extension_dev,
    security,
    sessions,
    styling,
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


@ui.page("/docs/concepts/store")
def page_concepts_store(ctx: Context):
    return store.render(ctx)


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


# Component Reference
@ui.page("/docs/components/layout")
def page_components_layout(ctx: Context):
    return layout.render(ctx)


@ui.page("/docs/components/typography")
def page_components_typography(ctx: Context):
    return typography.render(ctx)


@ui.page("/docs/components/buttons")
def page_components_buttons(ctx: Context):
    return buttons.render(ctx)


@ui.page("/docs/components/inputs")
def page_components_inputs(ctx: Context):
    return inputs.render(ctx)


@ui.page("/docs/components/cards")
def page_components_cards(ctx: Context):
    return cards.render(ctx)


@ui.page("/docs/components/data-display")
def page_components_data_display(ctx: Context):
    return data_display.render(ctx)


@ui.page("/docs/components/navigation")
def page_components_navigation(ctx: Context):
    return navigation.render(ctx)


@ui.page("/docs/components/feedback")
def page_components_feedback(ctx: Context):
    return feedback.render(ctx)


@ui.page("/docs/components/charts")
def page_components_charts(ctx: Context):
    return charts.render(ctx)


@ui.page("/docs/components/utility")
def page_components_utility(ctx: Context):
    return utility.render(ctx)


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


@ui.page("/docs/advanced/styling")
def page_advanced_styling(ctx: Context):
    return styling.render(ctx)


# ── FastAPI app ──────────────────────────────────────────────────────────

app = FastAPI(title="Refast Documentation")
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
