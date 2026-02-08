"""Navigation Components — /docs/components/navigation."""

from refast.components import Container, Heading, Markdown, Separator


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
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Components in this section

### Breadcrumb
- **Breadcrumb** / **BreadcrumbList** / **BreadcrumbItem** / **BreadcrumbLink** / **BreadcrumbPage** / **BreadcrumbSeparator** / **BreadcrumbEllipsis**

### NavigationMenu
- **NavigationMenu** / **NavigationMenuList** / **NavigationMenuItem** / **NavigationMenuTrigger** / **NavigationMenuContent** / **NavigationMenuLink**

### Pagination
- **Pagination** / **PaginationContent** / **PaginationItem** / **PaginationLink** / **PaginationPrevious** / **PaginationNext** / **PaginationEllipsis**

### Menubar
- **Menubar** / **MenubarMenu** / **MenubarTrigger** / **MenubarContent** / **MenubarItem** / **MenubarSeparator** / **MenubarCheckboxItem** / **MenubarRadioGroup** / **MenubarRadioItem** / **MenubarSub** / **MenubarSubTrigger** / **MenubarSubContent**

### Command
- **Command** / **CommandInput** / **CommandList** / **CommandEmpty** / **CommandGroup** / **CommandItem** / **CommandSeparator** / **CommandShortcut**

### Sidebar
- **Sidebar** / **SidebarProvider** / **SidebarContent** / **SidebarHeader** / **SidebarFooter** / **SidebarGroup** / **SidebarGroupLabel** / **SidebarGroupContent** / **SidebarGroupAction** / **SidebarMenu** / **SidebarMenuItem** / **SidebarMenuButton** / **SidebarMenuAction** / **SidebarMenuBadge** / **SidebarMenuSub** / **SidebarMenuSubItem** / **SidebarMenuSubButton** / **SidebarMenuSkeleton** / **SidebarInset** / **SidebarRail** / **SidebarSeparator** / **SidebarTrigger**

---

### Breadcrumb Example

```python
Breadcrumb(children=[
    BreadcrumbList(children=[
        BreadcrumbItem(children=[BreadcrumbLink("Home", href="/")]),
        BreadcrumbSeparator(),
        BreadcrumbItem(children=[BreadcrumbLink("Docs", href="/docs")]),
        BreadcrumbSeparator(),
        BreadcrumbItem(children=[BreadcrumbPage("Components")]),
    ]),
])
```

---

### Sidebar Example

```python
SidebarProvider(children=[
    Sidebar(collapsible="icon", children=[
        SidebarHeader(children=[...]),
        SidebarContent(children=[
            SidebarGroup(children=[
                SidebarGroupLabel("Section"),
                SidebarGroupContent(children=[
                    SidebarMenu(children=[
                        SidebarMenuItem(children=[
                            SidebarMenuButton("Item", icon="home", is_active=True),
                        ]),
                    ]),
                ]),
            ]),
        ]),
        SidebarRail(),
    ]),
    SidebarInset(children=[
        SidebarTrigger(),
        # Main content here
    ]),
])
```

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
