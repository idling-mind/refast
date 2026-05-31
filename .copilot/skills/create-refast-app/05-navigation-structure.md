# Refast — Navigation, Multi-Page Apps & App Structure

## 1. Multi-Page Registration

Register all pages on the same `ui` instance:

```python
from fastapi import FastAPI
from refast import RefastApp, Context
from refast import components as rc

ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    return rc.Heading("Home", level=1)

@ui.page("/about")
def about(ctx: Context):
    return rc.Heading("About", level=1)

@ui.page("/users/{user_id:int}")
def user_detail(ctx: Context):
    user_id = ctx.path_params["user_id"]
    return rc.Text(f"User {user_id}")

app = FastAPI()
app.include_router(ui.router)
```

---

## 2. Navigation Methods

### `ctx.load()` — SPA Navigation (Recommended)

No page reload. WebSocket stays connected. `ctx.state` is preserved.

```python
async def go_to_dashboard(ctx: Context):
    await ctx.load("/dashboard")

# With scroll control
await ctx.load("/docs/api", scroll_to="parameters-section", scroll_behavior="smooth")
await ctx.load("/docs/api", scroll_to=None)  # keep current scroll position

# Build URL with query params dynamically
async def do_search(ctx: Context, query: str = "", page: int = 1):
    await ctx.load(f"/search?q={query}&page={page}")
```

### `ctx.redirect()` — Full Browser Redirect

Causes a full page reload. WebSocket state is lost.

```python
await ctx.redirect("/login")
await ctx.redirect("https://example.com", target="_blank")
```

### `ctx.refresh()` — Re-render Current Page

```python
await ctx.refresh()                     # re-run page function, full tree
await ctx.refresh(target_id="sidebar")  # re-render only one component subtree
await ctx.refresh(path="/settings")     # navigate + re-render (SPA, no reload)
```

### `Link` Component — Declarative Navigation

```python
from refast.components import Link

rc.Link("Go to About", href="/about")
rc.Link("Open in new tab", href="/about", target="_blank")
```

---

## 3. State-Based Navigation (No URL Change)

Useful for wizard steps, tab-like views, or transient states:

```python
async def navigate(ctx: Context, page: str = "home"):
    ctx.state.set("current_page", page)
    await ctx.replace("root-container", render_app(ctx))

def render_app(ctx: Context):
    current_page = ctx.state.get("current_page", "home")
    page_map = {"home": home_view, "about": about_view, "settings": settings_view}
    return rc.Container(
        id="root-container",
        children=[
            render_navbar(ctx, current_page),
            page_map.get(current_page, home_view)(ctx),
        ],
    )
```

---

## 4. Shared Layout Function Pattern

Factor out the shell so every page function just passes its content:

```python
# In app.py:
def app_layout(ctx: Context, content, current_path: str = "/"):
    return rc.SidebarProvider(children=[
        _build_sidebar(ctx, current_path),
        rc.SidebarInset(children=[
            _build_topbar(ctx, current_path),
            rc.Container(
                id=f"page-{current_path.replace('/', '-')}",
                class_name="flex-1 overflow-y-auto p-6",
                children=[content],
            ),
        ]),
    ])

# In each page:
@ui.page("/dashboard")
def dashboard(ctx: Context):
    content = rc.Column(children=[
        rc.Heading("Dashboard", level=1),
        rc.Text("Welcome back!"),
    ])
    return app_layout(ctx, content, "/dashboard")
```

---

## 5. Sidebar Layout (Full API)

The canonical layout for sidebar apps:

```python
from refast.components import (
    Sidebar, SidebarContent, SidebarFooter, SidebarGroup,
    SidebarGroupAction, SidebarGroupContent, SidebarGroupLabel,
    SidebarHeader, SidebarInset, SidebarMenu, SidebarMenuAction,
    SidebarMenuBadge, SidebarMenuButton, SidebarMenuItem,
    SidebarProvider, SidebarRail, SidebarSeparator, SidebarTrigger,
    SidebarMenuSub, SidebarMenuSubButton, SidebarMenuSubItem,
)

def build_sidebar_layout(ctx: Context, content, current_path: str):
    return rc.SidebarProvider(
        default_open=True,
        children=[
            rc.Sidebar(
                variant="sidebar",     # "sidebar" | "floating" | "inset"
                collapsible="icon",    # "icon" | "offcanvas" | "none"
                side="left",           # "left" | "right"
                children=[
                    rc.SidebarHeader(children=[
                        rc.SidebarMenu(children=[
                            rc.SidebarMenuItem(children=[
                                rc.SidebarMenuButton(
                                    "My App", icon="building", size="lg",
                                    on_click=ctx.callback(nav, path="/"),
                                ),
                            ]),
                        ]),
                    ]),
                    rc.SidebarSeparator(),
                    rc.SidebarContent(children=[
                        rc.SidebarGroup(children=[
                            rc.SidebarGroupLabel("Navigation"),
                            rc.SidebarGroupContent(children=[
                                rc.SidebarMenu(children=[
                                    rc.SidebarMenuItem(children=[
                                        rc.SidebarMenuButton(
                                            "Dashboard",
                                            icon="home",
                                            is_active=(current_path == "/dashboard"),
                                            on_click=ctx.callback(nav, path="/dashboard"),
                                        ),
                                        rc.SidebarMenuBadge("3"),  # optional badge
                                    ]),
                                    rc.SidebarMenuItem(children=[
                                        rc.SidebarMenuButton(
                                            "Settings",
                                            icon="settings",
                                            is_active=(current_path == "/settings"),
                                            on_click=ctx.callback(nav, path="/settings"),
                                        ),
                                    ]),
                                ]),
                            ]),
                        ]),
                    ]),
                    rc.SidebarSeparator(),
                    rc.SidebarFooter(children=[
                        rc.SidebarMenu(children=[
                            rc.SidebarMenuItem(children=[
                                rc.SidebarMenuButton("John Doe", icon="user", size="lg"),
                            ]),
                        ]),
                    ]),
                    rc.SidebarRail(),  # drag handle — omit if collapsible="none"
                ],
            ),
            rc.SidebarInset(children=[
                # Sticky topbar
                rc.Container(
                    class_name="border-b px-4 py-3 sticky top-0 bg-background z-10",
                    children=[
                        rc.Row(align="center", gap=4, children=[
                            rc.SidebarTrigger(),   # hamburger toggle button
                            rc.Separator(orientation="vertical", class_name="h-6"),
                            rc.Text("Page Title"),
                        ]),
                    ],
                ),
                # Main content
                rc.Container(class_name="p-6", children=[content]),
            ]),
        ],
    )

async def nav(ctx: Context, path: str = "/"):
    await ctx.load(path)
```

### `Sidebar` Props Summary

| Prop | Values | Notes |
|------|--------|-------|
| `variant` | `"sidebar"`, `"floating"`, `"inset"` | `floating` adds shadow/rounded; `inset` adds card effect |
| `collapsible` | `"icon"`, `"offcanvas"`, `"none"` | `icon` collapses to icon strip; `offcanvas` slides off-screen |
| `side` | `"left"`, `"right"` | For right sidebar, put `SidebarInset` **before** `Sidebar` in children |

### `SidebarMenuButton` Props

| Prop | Example | Notes |
|------|---------|-------|
| `label` (positional) | `"Dashboard"` | Menu item text |
| `icon` | `"home"` | Lucide icon name |
| `href` | `"/dashboard"` | Link (no server call) |
| `is_active` | `True` | Highlights as current page |
| `size` | `"sm"`, `"default"`, `"lg"` | `"lg"` for brand/user in header/footer |
| `on_click` | `ctx.callback(fn)` | Server callback |

---

## 6. Nested / Collapsible Sidebar Sections

```python
from refast.components import Collapsible, CollapsibleContent, CollapsibleTrigger

rc.SidebarGroup(children=[
    rc.Collapsible(
        default_open=True,
        children=[
            rc.CollapsibleTrigger(
                as_child=True,
                children=[
                    rc.SidebarMenuButton("Getting Started", icon="zap"),
                ],
            ),
            rc.CollapsibleContent(children=[
                rc.SidebarGroupContent(children=[
                    rc.SidebarMenu(children=[
                        rc.SidebarMenuItem(children=[
                            rc.SidebarMenuButton("Introduction", icon="book-open",
                                                  on_click=ctx.callback(nav, path="/docs/intro")),
                        ]),
                        rc.SidebarMenuItem(children=[
                            rc.SidebarMenuButton("Installation", icon="download",
                                                  on_click=ctx.callback(nav, path="/docs/install")),
                        ]),
                    ]),
                ]),
            ]),
        ],
    ),
])
```

---

## 7. Topbar with Breadcrumb Pattern

```python
from refast.components import (
    Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList,
    BreadcrumbPage, BreadcrumbSeparator,
)

def build_topbar(ctx: Context, current_path: str):
    # Build breadcrumb items from current path
    breadcrumb_items = [
        rc.BreadcrumbItem(children=[
            rc.BreadcrumbLink(label="Home", href="/", on_click=ctx.callback(nav, path="/")),
        ]),
        rc.BreadcrumbSeparator(),
        rc.BreadcrumbItem(children=[
            rc.BreadcrumbPage(label="Dashboard"),
        ]),
    ]
    
    return rc.Container(
        class_name="border-b px-4 py-3 sticky top-0 bg-background z-10",
        children=[
            rc.Row(align="center", justify="between", children=[
                rc.Row(align="center", gap=4, children=[
                    rc.SidebarTrigger(),
                    rc.Separator(orientation="vertical", class_name="h-6"),
                    rc.Breadcrumb(children=[
                        rc.BreadcrumbList(children=breadcrumb_items),
                    ]),
                ]),
                rc.Row(align="center", gap=2, children=[
                    rc.Button("Search", icon="search", variant="outline",
                              on_click=ctx.callback(open_search)),
                ]),
            ]),
        ],
    )
```

---

## 8. URL Parameters & Query Params

### Path Parameters

```python
@ui.page("/items/{category}/{item_id:int}")
def item_page(ctx: Context):
    category: str = ctx.path_params["category"]
    item_id: int = ctx.path_params["item_id"]
    return rc.Text(f"{category} / item {item_id}")
```

### Query Parameters

```python
@ui.page("/search")
def search_page(ctx: Context):
    query = ctx.query_params.get("q", "")
    page = int(ctx.query_params.get("page", "1"))
    sort = ctx.query_params.get("sort", "date")
    results = search(query, page=page, sort=sort)
    return render_results(ctx, results, query, page)

# Navigate with query params
async def do_search(ctx: Context, q: str = "", page: int = 1, sort: str = "date"):
    await ctx.load(f"/search?q={q}&page={page}&sort={sort}")
```

### `ctx.url` — Full Current URL

```python
ctx.url            # "/search?q=hello&page=2"
path = ctx.url.split("?")[0]        # "/search"
```

---

## 9. CMD+K Search Dialog Pattern

Used in the docs site — CMD+K opens a searchable command palette:

```python
from refast.components import (
    Command, CommandEmpty, CommandGroup, CommandInput,
    CommandItem, CommandList, CommandSeparator,
    Dialog, DialogContent,
    KeyboardShortcut,
)

def build_search_dialog(ctx: Context):
    return rc.Fragment([
        rc.Dialog(
            open=ctx.state.get("search_open", False),
            on_open_change=ctx.callback(close_search),
            children=[
                rc.DialogContent(
                    class_name="p-0 overflow-hidden max-w-lg",
                    children=[
                        rc.Command(
                            class_name="rounded-lg",
                            children=[
                                rc.CommandInput(placeholder="Search pages…"),
                                rc.CommandList(children=[
                                    rc.CommandEmpty(message="No results found."),
                                    rc.CommandGroup(heading="Pages", children=[
                                        rc.CommandItem(
                                            label="Dashboard",
                                            icon="home",
                                            on_select=ctx.callback(nav_and_close, path="/dashboard"),
                                        ),
                                        rc.CommandItem(
                                            label="Settings",
                                            icon="settings",
                                            on_select=ctx.callback(nav_and_close, path="/settings"),
                                        ),
                                    ]),
                                ]),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        rc.KeyboardShortcut(
            shortcuts={"ctrl+k": ctx.callback(open_search)},
            priority=10,
            prevent_default=True,
        ),
    ])

async def open_search(ctx: Context):
    ctx.state["search_open"] = True
    await ctx.refresh()

async def close_search(ctx: Context):
    ctx.state["search_open"] = False
    await ctx.refresh()

async def nav_and_close(ctx: Context, path: str = "/"):
    ctx.state["search_open"] = False
    await ctx.load(path)
```

---

## 10. Complete Multi-Page Docs-Style App Skeleton

```python
# app.py
from fastapi import FastAPI
from refast import RefastApp, Context
from refast import components as rc

ui = RefastApp(title="My Docs", favicon="📖", preloaded_features=["navigation"])

NAV_SECTIONS = [
    {"label": "Getting Started", "icon": "rocket", "pages": [
        ("Overview", "/docs/overview", "home"),
        ("Installation", "/docs/install", "download"),
    ]},
    {"label": "Guides", "icon": "book", "pages": [
        ("Quick Start", "/docs/quickstart", "zap"),
        ("Advanced", "/docs/advanced", "settings"),
    ]},
]

def docs_layout(ctx: Context, content, current_path: str = "/"):
    return rc.SidebarProvider(
        id="docs-sidebar-provider",
        children=[
            _build_sidebar(ctx, current_path),
            rc.SidebarInset(children=[
                _build_topbar(ctx, current_path),
                rc.Container(
                    id=f"docs-content-{current_path.replace('/', '-').strip('-') or 'home'}",
                    class_name="flex-1 overflow-y-auto p-6 max-w-4xl mx-auto",
                    children=[content],
                ),
            ]),
            rc.ConnectionStatus(),
        ],
    )

def _build_sidebar(ctx: Context, current_path: str):
    menu_items = []
    for section in NAV_SECTIONS:
        pages = [
            rc.SidebarMenuItem(children=[
                rc.SidebarMenuButton(
                    label,
                    icon=icon,
                    is_active=(current_path == path),
                    on_click=ctx.callback(nav, path=path),
                ),
            ])
            for label, path, icon in section["pages"]
        ]
        menu_items.append(rc.SidebarGroup(children=[
            rc.SidebarGroupLabel(section["label"]),
            rc.SidebarGroupContent(children=[rc.SidebarMenu(children=pages)]),
        ]))

    return rc.Sidebar(collapsible="icon", children=[
        rc.SidebarHeader(children=[
            rc.SidebarMenu(children=[
                rc.SidebarMenuItem(children=[
                    rc.SidebarMenuButton("My Docs", icon="book", size="lg",
                                         on_click=ctx.callback(nav, path="/")),
                ]),
            ]),
        ]),
        rc.SidebarContent(children=menu_items),
        rc.SidebarRail(),
    ])

def _build_topbar(ctx: Context, current_path: str):
    return rc.Container(
        class_name="border-b px-4 py-3 sticky top-0 bg-background z-10",
        children=[rc.Row(align="center", gap=4, children=[
            rc.SidebarTrigger(),
            rc.Separator(orientation="vertical", class_name="h-6"),
            rc.Text(current_path, class_name="text-muted-foreground text-sm"),
        ])],
    )

async def nav(ctx: Context, path: str = "/"):
    await ctx.load(path)

# Register pages
@ui.page("/")
def home(ctx: Context):
    return docs_layout(ctx, rc.Column(children=[
        rc.Heading("Welcome", level=1),
        rc.Paragraph("Select a topic from the sidebar."),
    ]), "/")

@ui.page("/docs/overview")
def overview(ctx: Context):
    return docs_layout(ctx, rc.Column(children=[
        rc.Heading("Overview", level=1),
        rc.Markdown("## What is this?\n\nA documentation site built with Refast."),
    ]), "/docs/overview")

@ui.page("/docs/install")
def install(ctx: Context):
    return docs_layout(ctx, rc.Column(children=[
        rc.Heading("Installation", level=1),
        rc.Code(code="pip install refast", language="bash"),
    ]), "/docs/install")

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
