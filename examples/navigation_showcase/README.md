# Navigation Showcase Example

Demonstrates all navigation-related components in Refast.

## Components Demonstrated

### Menubar
Application-style menu bar with nested menus, keyboard shortcuts, checkboxes, and radio groups.

### Breadcrumb
Navigation breadcrumbs showing location hierarchy with links and ellipsis for long paths.

### NavigationMenu
Horizontal navigation with dropdown mega-menu style content panels.

### Command Palette
Searchable command menu with groups, icons, and keyboard-accessible actions.

### Tabs
Tabbed interface for organizing content sections.

### Pagination
Page navigation controls with previous/next and page number links.

## Key Patterns

### Command Selection
```python
async def on_command_select(ctx: Context):
    command = ctx.event_data.get("command")
    await ctx.show_toast(f"Executing: {command}", variant="info")
```

### Page Navigation
```python
async def on_page_change(ctx: Context):
    page = ctx.event_data.get("page", 1)
    ctx.state.set("current_page", page)
    await ctx.refresh()
```

## Running

```bash
cd examples/navigation_showcase
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.
