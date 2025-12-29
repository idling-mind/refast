"""Data Table Example - Demonstrates DataTable with sorting, filtering, and actions.

This example demonstrates:
- DataTable component with pagination
- Column sorting and filtering
- Row selection and bulk actions
- Action buttons per row
- Badge status indicators
"""

from fastapi import FastAPI
from datetime import datetime, timedelta
import random

from refast import RefastApp, Context
from refast.components import (
    Container,
    Column,
    Row,
    Text,
    Button,
    Card,
    CardHeader,
    CardContent,
    CardTitle,
    CardDescription,
    Input,
    Select,
    Badge,
    DataTable,
    Checkbox,
    Avatar,
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    AlertDialog,
    AlertDialogTrigger,
    AlertDialogContent,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogAction,
    AlertDialogCancel,
    Separator,
    Label,
)


# Create the Refast app
ui = RefastApp(title="Data Table Example")


# Sample data
def generate_sample_users():
    """Generate sample user data."""
    statuses = ["active", "inactive", "pending"]
    roles = ["Admin", "Editor", "Viewer"]
    
    users = []
    for i in range(1, 51):
        status = random.choice(statuses)
        users.append({
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "role": random.choice(roles),
            "status": status,
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
        })
    return users


SAMPLE_USERS = generate_sample_users()


# Callback handlers
async def on_search(ctx: Context):
    """Handle search input."""
    query = ctx.event_data.get("value", "").lower()
    ctx.state.set("search_query", query)
    ctx.state.set("current_page", 1)
    await ctx.refresh()


async def on_filter_status(ctx: Context):
    """Handle status filter change."""
    status = ctx.event_data.get("value", "all")
    ctx.state.set("filter_status", status)
    ctx.state.set("current_page", 1)
    await ctx.refresh()


async def on_page_change(ctx: Context):
    """Handle page change."""
    page = ctx.event_data.get("page", 1)
    ctx.state.set("current_page", page)
    await ctx.refresh()


async def on_select_all(ctx: Context):
    """Handle select all checkbox."""
    selected = ctx.state.get("selected_ids", [])
    filtered_users = get_filtered_users(ctx)
    page_users = get_page_users(filtered_users, ctx)
    
    page_ids = [u["id"] for u in page_users]
    
    if all(id in selected for id in page_ids):
        # Deselect all on page
        selected = [id for id in selected if id not in page_ids]
    else:
        # Select all on page
        selected = list(set(selected + page_ids))
    
    ctx.state.set("selected_ids", selected)
    await ctx.refresh()


async def on_select_row(ctx: Context):
    """Handle row selection."""
    user_id = ctx.event_data.get("user_id")
    selected = ctx.state.get("selected_ids", [])
    
    if user_id in selected:
        selected.remove(user_id)
    else:
        selected.append(user_id)
    
    ctx.state.set("selected_ids", selected)
    await ctx.refresh()


async def on_edit_user(ctx: Context):
    """Handle edit user action."""
    user_id = ctx.event_data.get("user_id")
    await ctx.show_toast(f"Editing user {user_id}", variant="info")


async def on_delete_user(ctx: Context):
    """Handle delete user action."""
    user_id = ctx.event_data.get("user_id")
    # In real app, would delete from database
    await ctx.show_toast(f"Deleted user {user_id}", variant="success")
    await ctx.refresh()


async def on_bulk_delete(ctx: Context):
    """Handle bulk delete action."""
    selected = ctx.state.get("selected_ids", [])
    count = len(selected)
    ctx.state.set("selected_ids", [])
    await ctx.show_toast(f"Deleted {count} users", variant="success")
    await ctx.refresh()


async def on_export(ctx: Context):
    """Handle export action."""
    await ctx.show_toast("Exporting data...", variant="info")


def get_filtered_users(ctx: Context):
    """Get filtered users based on search and status."""
    query = ctx.state.get("search_query", "")
    status_filter = ctx.state.get("filter_status", "all")
    
    users = SAMPLE_USERS
    
    if query:
        users = [u for u in users if query in u["name"].lower() or query in u["email"].lower()]
    
    if status_filter != "all":
        users = [u for u in users if u["status"] == status_filter]
    
    return users


def get_page_users(users, ctx: Context, per_page=10):
    """Get users for current page."""
    page = ctx.state.get("current_page", 1)
    start = (page - 1) * per_page
    end = start + per_page
    return users[start:end]


def get_status_badge(status):
    """Get badge variant based on status."""
    variants = {
        "active": "success",
        "inactive": "secondary",
        "pending": "warning",
    }
    return Badge(text=status.capitalize(), variant=variants.get(status, "default"))


# Main page
@ui.page("/")
def home(ctx: Context):
    """Data table page."""
    search_query = ctx.state.get("search_query", "")
    filter_status = ctx.state.get("filter_status", "all")
    selected_ids = ctx.state.get("selected_ids", [])
    current_page = ctx.state.get("current_page", 1)
    per_page = 10
    
    filtered_users = get_filtered_users(ctx)
    page_users = get_page_users(filtered_users, ctx, per_page)
    total_pages = (len(filtered_users) + per_page - 1) // per_page
    
    page_ids = [u["id"] for u in page_users]
    all_selected = len(page_ids) > 0 and all(id in selected_ids for id in page_ids)
    
    return Container(
        class_name="max-w-7xl mx-auto p-8",
        children=[
            # Header
            Row(
                justify="between",
                align="center",
                class_name="mb-6",
                children=[
                    Column(
                        gap=1,
                        children=[
                            Text("Users", class_name="text-3xl font-bold"),
                            Text(
                                f"{len(filtered_users)} total users",
                                class_name="text-muted-foreground"
                            ),
                        ],
                    ),
                    Row(
                        gap=2,
                        children=[
                            Button(
                                label="Export",
                                variant="outline",
                                on_click=ctx.callback(on_export)
                            ),
                            Button(label="Add User", variant="default"),
                        ],
                    ),
                ],
            ),
            
            Card(
                children=[
                    CardContent(
                        class_name="p-6",
                        children=[
                            # Filters row
                            Row(
                                justify="between",
                                align="center",
                                class_name="mb-4",
                                children=[
                                    Row(
                                        gap=4,
                                        children=[
                                            Input(
                                                name="search",
                                                placeholder="Search users...",
                                                value=search_query,
                                                on_change=ctx.callback(on_search),
                                                class_name="w-64",
                                            ),
                                            Select(
                                                name="filter_status",
                                                value=filter_status,
                                                on_change=ctx.callback(on_filter_status),
                                                options=[
                                                    {"value": "all", "label": "All Status"},
                                                    {"value": "active", "label": "Active"},
                                                    {"value": "inactive", "label": "Inactive"},
                                                    {"value": "pending", "label": "Pending"},
                                                ],
                                            ),
                                        ],
                                    ),
                                    # Bulk actions
                                    Row(
                                        gap=2,
                                        children=[
                                            Text(
                                                f"{len(selected_ids)} selected",
                                                class_name="text-sm text-muted-foreground"
                                            ) if selected_ids else None,
                                            AlertDialog(
                                                children=[
                                                    AlertDialogTrigger(
                                                        children=Button(
                                                            label="Delete Selected",
                                                            variant="destructive",
                                                            size="sm",
                                                            disabled=len(selected_ids) == 0,
                                                        )
                                                    ),
                                                    AlertDialogContent(
                                                        children=[
                                                            AlertDialogHeader(
                                                                children=[
                                                                    AlertDialogTitle(title="Delete Users"),
                                                                    AlertDialogDescription(
                                                                        description=f"Are you sure you want to delete {len(selected_ids)} users? This action cannot be undone."
                                                                    ),
                                                                ]
                                                            ),
                                                            AlertDialogFooter(
                                                                children=[
                                                                    AlertDialogCancel(label="Cancel"),
                                                                    AlertDialogAction(
                                                                        label="Delete",
                                                                        on_click=ctx.callback(on_bulk_delete)
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ) if selected_ids else None,
                                        ],
                                    ),
                                ],
                            ),
                            
                            # Table
                            Container(
                                class_name="border rounded-md",
                                children=[
                                    # Table header
                                    Row(
                                        class_name="bg-muted/50 p-3 border-b",
                                        children=[
                                            Container(
                                                class_name="w-10",
                                                children=[
                                                    Checkbox(
                                                        checked=all_selected,
                                                        on_change=ctx.callback(on_select_all),
                                                    ),
                                                ],
                                            ),
                                            Text("User", class_name="flex-1 font-medium text-sm"),
                                            Text("Role", class_name="w-24 font-medium text-sm"),
                                            Text("Status", class_name="w-24 font-medium text-sm"),
                                            Text("Created", class_name="w-28 font-medium text-sm"),
                                            Text("Actions", class_name="w-20 font-medium text-sm text-right"),
                                        ],
                                    ),
                                    
                                    # Table rows
                                    Column(
                                        children=[
                                            Row(
                                                class_name=f"p-3 border-b hover:bg-muted/30 {'bg-muted/20' if user['id'] in selected_ids else ''}",
                                                align="center",
                                                children=[
                                                    Container(
                                                        class_name="w-10",
                                                        children=[
                                                            Checkbox(
                                                                checked=user["id"] in selected_ids,
                                                                on_change=ctx.callback(
                                                                    on_select_row,
                                                                    user_id=user["id"]
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                    Row(
                                                        class_name="flex-1",
                                                        gap=3,
                                                        align="center",
                                                        children=[
                                                            Avatar(
                                                                fallback=user["name"][0],
                                                                size="sm",
                                                            ),
                                                            Column(
                                                                gap=0,
                                                                children=[
                                                                    Text(user["name"], class_name="font-medium text-sm"),
                                                                    Text(user["email"], class_name="text-xs text-muted-foreground"),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    Text(user["role"], class_name="w-24 text-sm"),
                                                    Container(
                                                        class_name="w-24",
                                                        children=[get_status_badge(user["status"])],
                                                    ),
                                                    Text(user["created_at"], class_name="w-28 text-sm text-muted-foreground"),
                                                    Container(
                                                        class_name="w-20 text-right",
                                                        children=[
                                                            DropdownMenu(
                                                                children=[
                                                                    DropdownMenuTrigger(
                                                                        children=Button(
                                                                            label="•••",
                                                                            variant="ghost",
                                                                            size="sm",
                                                                        )
                                                                    ),
                                                                    DropdownMenuContent(
                                                                        children=[
                                                                            DropdownMenuItem(
                                                                                label="Edit",
                                                                                on_select=ctx.callback(
                                                                                    on_edit_user,
                                                                                    user_id=user["id"]
                                                                                ),
                                                                            ),
                                                                            DropdownMenuItem(label="View Profile"),
                                                                            DropdownMenuSeparator(),
                                                                            DropdownMenuItem(
                                                                                label="Delete",
                                                                                on_select=ctx.callback(
                                                                                    on_delete_user,
                                                                                    user_id=user["id"]
                                                                                ),
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ]
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            )
                                            for user in page_users
                                        ],
                                    ),
                                ],
                            ),
                            
                            # Pagination
                            Row(
                                justify="between",
                                align="center",
                                class_name="mt-4",
                                children=[
                                    Text(
                                        f"Showing {(current_page - 1) * per_page + 1} to {min(current_page * per_page, len(filtered_users))} of {len(filtered_users)} users",
                                        class_name="text-sm text-muted-foreground"
                                    ),
                                    Row(
                                        gap=1,
                                        children=[
                                            Button(
                                                label="Previous",
                                                variant="outline",
                                                size="sm",
                                                disabled=current_page == 1,
                                                on_click=ctx.callback(on_page_change, page=current_page - 1),
                                            ),
                                            *[
                                                Button(
                                                    label=str(p),
                                                    variant="default" if p == current_page else "outline",
                                                    size="sm",
                                                    on_click=ctx.callback(on_page_change, page=p),
                                                )
                                                for p in range(
                                                    max(1, current_page - 2),
                                                    min(total_pages + 1, current_page + 3)
                                                )
                                            ],
                                            Button(
                                                label="Next",
                                                variant="outline",
                                                size="sm",
                                                disabled=current_page >= total_pages,
                                                on_click=ctx.callback(on_page_change, page=current_page + 1),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# Create FastAPI app and include Refast
app = FastAPI()
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
