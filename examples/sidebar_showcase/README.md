# Sidebar Showcase

A comprehensive example demonstrating all sidebar component features from shadcn/ui.

## Features Demonstrated

### Core Components
- **SidebarProvider** - Context provider for state management
- **Sidebar** - Main sidebar container with variants and collapsible modes
- **SidebarInset** - Main content area for inset layouts
- **SidebarTrigger** - Toggle button for opening/closing sidebar
- **SidebarRail** - Edge toggle functionality

### Layout Components
- **SidebarHeader** - Sticky header section
- **SidebarContent** - Scrollable content area
- **SidebarFooter** - Sticky footer section
- **SidebarSeparator** - Visual divider

### Menu Components
- **SidebarGroup** - Logical grouping of menu items
- **SidebarGroupLabel** - Label for groups
- **SidebarGroupAction** - Action button for groups (e.g., "Add Project")
- **SidebarGroupContent** - Container for group content
- **SidebarMenu** - Menu container
- **SidebarMenuItem** - Individual menu item
- **SidebarMenuButton** - Clickable menu button with icon support
- **SidebarMenuAction** - Action button on menu items (shows on hover)
- **SidebarMenuBadge** - Badge/notification count
- **SidebarMenuSub** - Submenu container
- **SidebarMenuSubItem** - Submenu item
- **SidebarMenuSubButton** - Submenu button
- **SidebarMenuSkeleton** - Loading placeholder

### Integration with Other Components
- **Collapsible** - For expandable/collapsible menu sections
- **DropdownMenu** - For menu item action dropdowns

## Configuration Options

### Sidebar Variants
- `sidebar` - Default bordered sidebar
- `floating` - Floating sidebar with shadow and rounded corners
- `inset` - Full-bleed sidebar with inset content area

### Collapsible Modes
- `offcanvas` - Slides completely off screen
- `icon` - Collapses to icon-only mode
- `none` - Non-collapsible

### Side
- `left` - Left side (default)
- `right` - Right side

### Button Variants
- `default` - Standard button style
- `outline` - Outlined button style

### Button Sizes
- `sm` - Small
- `default` - Default
- `lg` - Large

## Demo Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Default sidebar with icon collapsible mode |
| Floating | `/floating` | Floating variant with offcanvas mode |
| Inset | `/inset` | Inset variant (content appears as card) |
| Right | `/right` | Right-side positioned sidebar |
| Collapsible Menu | `/collapsible-menu` | Expandable/collapsible menu sections |
| Dropdown Actions | `/dropdown-actions` | Menu items with dropdown action menus |
| Skeleton | `/skeleton` | Loading state demonstration |
| Offcanvas | `/offcanvas` | Offcanvas collapsible mode (sidebar fully hides) |
| Non-Collapsible | `/none` | Sidebar that cannot be collapsed |

## Running the Example

```bash
cd examples/sidebar_showcase
uvicorn app:app --reload
```

Then visit:
- http://localhost:8000 - Home with navigation links to all demos
- http://localhost:8000/floating - Floating variant
- http://localhost:8000/inset - Inset variant
- http://localhost:8000/right - Right sidebar
- http://localhost:8000/collapsible-menu - Collapsible sections
- http://localhost:8000/dropdown-actions - Dropdown menus
- http://localhost:8000/skeleton - Loading skeletons
- http://localhost:8000/offcanvas - Offcanvas mode
- http://localhost:8000/none - Non-collapsible

## Keyboard Shortcuts

- **Ctrl+B** (Windows/Linux) or **Cmd+B** (Mac) - Toggle sidebar

## Code Example

```python
from refast.components import (
    SidebarProvider,
    Sidebar,
    SidebarInset,
    SidebarHeader,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupLabel,
    SidebarGroupContent,
    SidebarMenu,
    SidebarMenuItem,
    SidebarMenuButton,
    SidebarTrigger,
    SidebarRail,
)

@app.page("/")
def home(ctx):
    return SidebarProvider(
        default_open=True,
        children=[
            Sidebar(
                variant="sidebar",
                collapsible="icon",
                children=[
                    SidebarHeader(
                        children=[
                            SidebarMenuButton("My App", icon="🏢", size="lg"),
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
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Dashboard",
                                                                icon="🏠",
                                                                is_active=True,
                                                            ),
                                                        ]
                                                    ),
                                                    SidebarMenuItem(
                                                        children=[
                                                            SidebarMenuButton(
                                                                "Settings",
                                                                icon="⚙️",
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
                ]
            ),
            SidebarInset(
                children=[
                    SidebarTrigger(),
                    # Your main content here
                ]
            ),
        ]
    )
```
