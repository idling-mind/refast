# Data Table Example

A comprehensive data table with sorting, filtering, pagination, and row actions.

## Features Demonstrated

- **DataTable** - Tabular data display with custom row rendering
- **Checkbox** - Row selection and bulk selection
- **DropdownMenu** - Per-row action menus
- **AlertDialog** - Bulk delete confirmation
- **Badge** - Status indicators
- **Avatar** - User avatars
- **Input/Select** - Search and filter controls
- **Pagination** - Page navigation with page numbers

## Key Patterns

### Row Selection
```python
async def on_select_row(ctx: Context):
    user_id = ctx.event_data.get("user_id")
    selected = ctx.state.get("selected_ids", [])
    
    if user_id in selected:
        selected.remove(user_id)
    else:
        selected.append(user_id)
    
    ctx.state.set("selected_ids", selected)
    await ctx.refresh()
```

### Filtering and Pagination
```python
def get_filtered_users(ctx: Context):
    query = ctx.state.get("search_query", "")
    status_filter = ctx.state.get("filter_status", "all")
    
    users = SAMPLE_USERS
    if query:
        users = [u for u in users if query in u["name"].lower()]
    if status_filter != "all":
        users = [u for u in users if u["status"] == status_filter]
    
    return users
```

## Running

```bash
cd examples/data_table
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.
