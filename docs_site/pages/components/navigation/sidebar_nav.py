"""Sidebar Nav — /docs/components/sidebar-nav.

Reference page for the Sidebar component family.
"""

from refast import Context
from refast.components import (
    Container,
    Heading,
    Markdown,
    Separator,
)

PAGE_TITLE = "Sidebar"
PAGE_ROUTE = "/docs/components/sidebar-nav"


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Sidebar component reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Content ───────────────────────────────────────────────────────────────

CONTENT = r"""
A composable, themeable sidebar navigation system. The sidebar handles
collapsible state, mobile responsiveness, and keyboard shortcuts (Ctrl/Cmd+B).

```python
from refast.components import (
    SidebarProvider, Sidebar, SidebarInset, SidebarTrigger,
    SidebarHeader, SidebarContent, SidebarFooter, SidebarRail,
    SidebarGroup, SidebarGroupLabel, SidebarGroupContent,
    SidebarMenu, SidebarMenuItem, SidebarMenuButton,
    SidebarMenuSub, SidebarMenuSubItem, SidebarMenuSubButton,
    SidebarSeparator,
)
```

---

## Basic Sidebar Structure

Wrap your entire layout in `SidebarProvider`. Place `Sidebar` and
`SidebarInset` (the main content area) as siblings inside it.

```python
SidebarProvider(
    children=[
        Sidebar(
            collapsible="icon",
            children=[
                SidebarHeader(
                    children=[
                        SidebarMenu(children=[
                            SidebarMenuItem(children=[
                                SidebarMenuButton(
                                    "My App",
                                    icon="home",
                                    size="lg",
                                )
                            ])
                        ])
                    ]
                ),
                SidebarContent(
                    children=[
                        SidebarGroup(
                            children=[
                                SidebarGroupLabel("Navigation"),
                                SidebarGroupContent(
                                    children=[
                                        SidebarMenu(
                                            children=[
                                                SidebarMenuItem(children=[
                                                    SidebarMenuButton(
                                                        "Dashboard",
                                                        icon="layout-dashboard",
                                                        is_active=True,
                                                        on_click=ctx.callback(go_dashboard),
                                                    )
                                                ]),
                                                SidebarMenuItem(children=[
                                                    SidebarMenuButton(
                                                        "Settings",
                                                        icon="settings",
                                                        on_click=ctx.callback(go_settings),
                                                    )
                                                ]),
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        )
                    ]
                ),
                SidebarFooter(
                    children=[
                        SidebarMenuButton("v1.0.0", icon="tag", size="sm")
                    ]
                ),
                SidebarRail(),
            ]
        ),
        SidebarInset(
            children=[
                SidebarTrigger(),   # hamburger toggle button
                # … main page content …
            ]
        ),
    ]
)
```

---

## Sidebar with Nested Sub-Menu

Use `SidebarMenuSub`, `SidebarMenuSubItem`, and `SidebarMenuSubButton` to
create collapsible nested navigation items.

```python
SidebarMenu(
    children=[
        SidebarMenuItem(
            children=[
                SidebarMenuButton("Components", icon="box"),
                SidebarMenuSub(
                    children=[
                        SidebarMenuSubItem(
                            children=[
                                SidebarMenuSubButton("Button", href="/docs/components/button")
                            ]
                        ),
                        SidebarMenuSubItem(
                            children=[
                                SidebarMenuSubButton("Card", href="/docs/components/card")
                            ]
                        ),
                        SidebarMenuSubItem(
                            children=[
                                SidebarMenuSubButton("Input", href="/docs/components/input")
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
)
```

---

## Collapsible Modes

Pass `collapsible` to the `Sidebar` component to control how it collapses.

| Mode | Behaviour |
|------|-----------|
| `"offcanvas"` | The sidebar slides off-screen when collapsed (default). Best for space-constrained layouts. |
| `"icon"` | The sidebar shrinks to show only icons when collapsed. Labels are hidden. Best for app dashboards. |
| `"none"` | The sidebar is always visible and cannot be collapsed. |

```python
# Slides off screen when collapsed (mobile-friendly)
Sidebar(collapsible="offcanvas", ...)

# Collapses to icon strip
Sidebar(collapsible="icon", ...)

# Always visible, no toggle
Sidebar(collapsible="none", ...)
```

---

## Props Reference

### `SidebarProvider`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `default_open` | `bool` | `True` | Initial open state |
| `children` | `ChildrenType` | `None` | `Sidebar` + `SidebarInset` |

### `Sidebar`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"left" \| "right"` | `"left"` | Placement |
| `variant` | `"sidebar" \| "floating" \| "inset"` | `"sidebar"` | Visual style |
| `collapsible` | `"offcanvas" \| "icon" \| "none"` | `"offcanvas"` | Collapse behaviour |

### `SidebarMenuButton`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Button text |
| `icon` | `str \| None` | `None` | Lucide icon name or emoji |
| `is_active` | `bool` | `False` | Highlight as current item |
| `variant` | `"default" \| "outline"` | `"default"` | Visual variant |
| `size` | `"default" \| "sm" \| "lg"` | `"default"` | Size |
| `href` | `str \| None` | `None` | Optional link URL |
| `on_click` | `Callback \| None` | `None` | Click callback |

### `SidebarMenuSubButton`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Sub-item text |
| `href` | `str \| None` | `None` | Navigation URL |
| `is_active` | `bool` | `False` | Highlight as active |
| `on_click` | `Callback \| None` | `None` | Click callback |
"""
