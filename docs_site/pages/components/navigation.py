"""Navigation Components — /docs/components/navigation."""

from refast.components import Container, Heading, Separator

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "Navigation Components"
PAGE_ROUTE = "/docs/components/navigation"


def render(ctx):
    """Render the navigation components reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
## Overview

Navigation components handle routing, menus, and application structure.
Components that naturally belong together (e.g., a sidebar and all its sub-components)
are documented as a set.

---

## Breadcrumb

Shows the current page location within a hierarchy.

```python
Breadcrumb(
    children=[
        BreadcrumbList(
            children=[
                BreadcrumbItem(children=[BreadcrumbLink("Home", href="/")]),
                BreadcrumbSeparator(),
                BreadcrumbItem(children=[BreadcrumbLink("Docs", href="/docs")]),
                BreadcrumbSeparator(),
                BreadcrumbItem(children=[BreadcrumbPage("Components")]),
            ]
        )
    ]
)
```

| Component | Key Props | Notes |
|-----------|-----------|-------|
| `Breadcrumb` | `children` | Root wrapper |
| `BreadcrumbList` | `children` | `<ol>` container |
| `BreadcrumbItem` | `children` | Single item wrapper |
| `BreadcrumbLink` | `label`, `href`, `on_click` | Clickable link |
| `BreadcrumbPage` | `label` | Current page (non-clickable) |
| `BreadcrumbSeparator` | `children` | Defaults to `/`; pass custom icon as child |
| `BreadcrumbEllipsis` | — | Collapsed breadcrumbs indicator |

---

## Pagination

Controls page navigation for paginated lists.

```python
Pagination(
    children=[
        PaginationContent(
            children=[
                PaginationPrevious(on_click=ctx.callback(prev_page)),
                PaginationItem(children=[PaginationLink("1", href="?page=1", is_active=True)]),
                PaginationItem(children=[PaginationLink("2", href="?page=2")]),
                PaginationItem(children=[PaginationEllipsis()]),
                PaginationNext(on_click=ctx.callback(next_page)),
            ]
        )
    ]
)
```

### PaginationLink

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Page label text |
| `href` | `str` | `"#"` | URL for the link |
| `is_active` | `bool` | `False` | Highlights the current page |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` | Button size |
| `on_click` | `Callback \| None` | `None` | Click callback |

### PaginationPrevious / PaginationNext

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `href` | `str` | `"#"` | Navigation URL |
| `disabled` | `bool` | `False` | Disables the control |
| `on_click` | `Callback \| None` | `None` | Click callback |

---

## Sidebar

The Sidebar is a composed layout system with many sub-components. The standard pattern
wraps everything in `SidebarProvider`, then places a `Sidebar` and a `SidebarInset`
(main content area) side-by-side.

```python
SidebarProvider(
    default_open=True,
    children=[
        Sidebar(
            side="left",
            variant="sidebar",
            collapsible="icon",
            children=[
                SidebarHeader(
                    children=[Text("My App", class_name="font-bold text-lg")]
                ),
                SidebarContent(
                    children=[
                        SidebarGroup(
                            children=[
                                SidebarGroupLabel("Application"),
                                SidebarGroupContent(
                                    children=[
                                        SidebarMenu(
                                            children=[
                                                SidebarMenuItem(
                                                    children=[
                                                        SidebarMenuButton(
                                                            "Dashboard",
                                                            icon="layout-dashboard",
                                                            is_active=True,
                                                            on_click=ctx.callback(go_dashboard),
                                                        )
                                                    ]
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        )
                    ]
                ),
                SidebarFooter(
                    children=[Text("v1.0.0", class_name="text-xs text-muted-foreground")]
                ),
                SidebarRail(),
            ],
        ),
        SidebarInset(
            children=[
                SidebarTrigger(),
                # Main page content here
            ]
        ),
    ],
)
```

### SidebarProvider

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `default_open` | `bool` | `True` | Initial open/collapsed state |
| `children` | `list` | `[]` | Must contain `Sidebar` and `SidebarInset` |

### Sidebar

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"left" \| "right"` | `"left"` | Which side the sidebar appears on |
| `variant` | `"sidebar" \| "floating" \| "inset"` | `"sidebar"` | Visual style |
| `collapsible` | `"offcanvas" \| "icon" \| "none"` | `"offcanvas"` | Collapse behaviour. `"icon"` collapses to icon-only mode. `"offcanvas"` slides off screen. `"none"` is always visible. |
| `children` | `list` | `[]` | Sidebar sections |

### SidebarMenuButton

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Button text |
| `icon` | `str \| None` | `None` | Lucide icon name (e.g., `"home"`, `"settings"`) |
| `is_active` | `bool` | `False` | Highlights the button as the current selection |
| `variant` | `"default" \| "outline"` | `"default"` | Visual style |
| `size` | `"default" \| "sm" \| "lg"` | `"default"` | Button size |
| `href` | `str \| None` | `None` | If set, renders as a link |
| `on_click` | `Callback \| None` | `None` | Click callback |

### SidebarMenuAction

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `icon` | `str \| None` | `None` | Lucide icon name |
| `show_on_hover` | `bool` | `False` | Only show on hover |
| `on_click` | `Callback \| None` | `None` | Click callback |

### Other Sidebar sub-components

These are structural wrappers with only `children` and `class_name` props:
`SidebarContent`, `SidebarHeader`, `SidebarFooter`, `SidebarGroup`,
`SidebarGroupContent`, `SidebarMenu`, `SidebarMenuItem`, `SidebarMenuSub`,
`SidebarMenuSubItem`, `SidebarInset`.

| Component | Notes |
|-----------|-------|
| `SidebarGroupLabel` | Accepts `children`; renders a group heading |
| `SidebarGroupAction` | Icon button next to a group label |
| `SidebarMenuBadge` | Badge inside a menu item |
| `SidebarMenuSkeleton` | Loading skeleton for menu items |
| `SidebarMenuSubButton` | Like `SidebarMenuButton` but for nested menus |
| `SidebarSeparator` | Horizontal divider inside the sidebar |
| `SidebarRail` | Thin drag handle on the sidebar edge (no props) |
| `SidebarTrigger` | Toggle button; typically placed in `SidebarInset` |

---

## DropdownMenu

Displays a floating menu triggered by a button.

```python
DropdownMenu(
    children=[
        DropdownMenuTrigger(children=[Button("Options")]),
        DropdownMenuContent(
            side="bottom",
            align="start",
            children=[
                DropdownMenuLabel("My Account"),
                DropdownMenuSeparator(),
                DropdownMenuItem("Profile", icon="user", on_select=ctx.callback(go_profile)),
                DropdownMenuItem("Settings", icon="settings", shortcut="⌘S"),
                DropdownMenuSeparator(),
                DropdownMenuItem("Log out", icon="log-out", on_select=ctx.callback(logout)),
            ],
        ),
    ]
)
```

### DropdownMenu

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `bool \| None` | `None` | Controlled open state |
| `default_open` | `bool` | `False` | Initial open state |
| `on_open_change` | `Callback \| None` | `None` | Fired when open state changes |

### DropdownMenuContent

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"top" \| "right" \| "bottom" \| "left"` | `"bottom"` | Preferred placement side |
| `side_offset` | `int` | `4` | Pixel gap from trigger |
| `align` | `"start" \| "center" \| "end"` | `"start"` | Alignment along the side |

### DropdownMenuItem

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Item text |
| `icon` | `str \| None` | `None` | Lucide icon name |
| `shortcut` | `str \| None` | `None` | Keyboard shortcut hint text |
| `disabled` | `bool` | `False` | Disables the item |
| `on_select` | `Callback \| None` | `None` | Fired when item is selected |

### DropdownMenuCheckboxItem

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Item text |
| `checked` | `bool` | `False` | Checked state |
| `on_checked_change` | `Callback \| None` | `None` | Fires on toggle |
| `disabled` | `bool` | `False` | Disables the item |

### DropdownMenuRadioGroup / DropdownMenuRadioItem

```python
DropdownMenuRadioGroup(
    value="dark",
    on_value_change=ctx.callback(handle_theme),
    children=[
        DropdownMenuRadioItem("Light", value="light"),
        DropdownMenuRadioItem("Dark", value="dark"),
        DropdownMenuRadioItem("System", value="system"),
    ],
)
```

Other structural sub-components with only `children`/`class_name`:
`DropdownMenuSub`, `DropdownMenuSubTrigger`, `DropdownMenuSubContent`,
`DropdownMenuLabel`, `DropdownMenuSeparator`, `DropdownMenuShortcut`.

---

## Command

A searchable command palette, often used inside a `Popover` for a quick-search UI.

```python
Command(
    children=[
        CommandInput(placeholder="Search commands..."),
        CommandList(
            children=[
                CommandEmpty(children=["No results found."]),
                CommandGroup(
                    heading="Suggestions",
                    children=[
                        CommandItem("Calendar", icon="calendar", on_select=ctx.callback(open_calendar)),
                        CommandItem("Search", icon="search"),
                    ],
                ),
                CommandSeparator(),
                CommandGroup(
                    heading="Settings",
                    children=[
                        CommandItem("Profile", shortcut="⌘P"),
                        CommandItem("Settings", shortcut="⌘S"),
                    ],
                ),
            ]
        ),
    ]
)
```

### CommandInput

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `placeholder` | `str` | `""` | Input placeholder text |
| `value` | `str \| None` | `None` | Controlled input value |

### CommandItem

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Item text |
| `icon` | `str \| None` | `None` | Lucide icon name |
| `shortcut` | `str \| None` | `None` | Keyboard shortcut hint |
| `disabled` | `bool` | `False` | Disables the item |
| `on_select` | `Callback \| None` | `None` | Fired when selected |

### CommandGroup

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `heading` | `str \| None` | `None` | Group heading label |
| `children` | `list` | `[]` | `CommandItem` components |

---

## NavigationMenu

A horizontal top-level navigation with flyout panels.

```python
NavigationMenu(
    children=[
        NavigationMenuList(
            children=[
                NavigationMenuItem(
                    children=[
                        NavigationMenuTrigger(children=["Getting Started"]),
                        NavigationMenuContent(
                            children=[
                                NavigationMenuLink("Introduction", href="/docs/intro"),
                                NavigationMenuLink("Quick Start", href="/docs/quick"),
                            ]
                        ),
                    ]
                ),
                NavigationMenuItem(
                    children=[NavigationMenuLink("GitHub", href="https://github.com")]
                ),
            ]
        )
    ]
)
```

### NavigationMenuLink

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Link text |
| `href` | `str` | `"#"` | Navigation URL |
| `description` | `str \| None` | `None` | Optional sub-text shown below label |
| `active` | `bool` | `False` | Highlights the link as active |
| `on_click` | `Callback \| None` | `None` | Click callback |

---

## Menubar

An application-style menubar for desktop-like navigation.

```python
Menubar(
    children=[
        MenubarMenu(
            children=[
                MenubarTrigger(children=["File"]),
                MenubarContent(
                    children=[
                        MenubarItem("New", shortcut="⌘N", on_click=ctx.callback(new_file)),
                        MenubarItem("Open", shortcut="⌘O"),
                        MenubarSeparator(),
                        MenubarItem("Exit"),
                    ]
                ),
            ]
        ),
    ]
)
```

### MenubarItem

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Item text |
| `shortcut` | `str \| None` | `None` | Keyboard shortcut hint |
| `disabled` | `bool` | `False` | Disables the item |
| `inset` | `bool` | `False` | Indents the item |
| `on_click` | `Callback \| None` | `None` | Click callback |

Other structural sub-components: `MenubarMenu`, `MenubarTrigger`, `MenubarContent`,
`MenubarSeparator`, `MenubarSub`, `MenubarSubTrigger`, `MenubarSubContent`,
`MenubarLabel`, `MenubarShortcut`.
"""
