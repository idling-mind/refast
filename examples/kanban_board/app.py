"""Kanban Board Example - Drag and drop task management.

This example demonstrates:
- Card-based layout for task boards
- Column management (To Do, In Progress, Done)
- Task creation and editing via dialogs
- Badge status indicators
- Dropdown menus for task actions
"""
import uuid

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Avatar,
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
    IconButton,
    Input,
    Label,
    Row,
    ScrollArea,
    Select,
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
    Text,
    Textarea,
    Tooltip,
)

# Create the Refast app
ui = RefastApp(title="Kanban Board")


# Sample data
INITIAL_TASKS = {
    "todo": [
        {
            "id": "1",
            "title": "Design new landing page",
            "description": "Create wireframes and mockups for the new landing page",
            "priority": "high",
            "assignee": "Alice",
            "due_date": "2024-12-20",
        },
        {
            "id": "2",
            "title": "Update documentation",
            "description": "Add API documentation for new endpoints",
            "priority": "medium",
            "assignee": "Bob",
            "due_date": "2024-12-22",
        },
    ],
    "in_progress": [
        {
            "id": "3",
            "title": "Implement user authentication",
            "description": "Add OAuth2 login with Google and GitHub",
            "priority": "high",
            "assignee": "Charlie",
            "due_date": "2024-12-18",
        },
    ],
    "done": [
        {
            "id": "4",
            "title": "Setup CI/CD pipeline",
            "description": "Configure GitHub Actions for automated testing",
            "priority": "low",
            "assignee": "David",
            "due_date": "2024-12-15",
        },
    ],
}


def get_tasks(ctx: Context) -> dict:
    """Get tasks from state or use initial data."""
    tasks = ctx.state.get("tasks")
    filtered_tasks = ctx.state.get("filtered_tasks")
    if filtered_tasks:
        return filtered_tasks
    if tasks is None:
        ctx.state.set("tasks", INITIAL_TASKS)
        return INITIAL_TASKS
    return tasks


# Callback handlers
async def create_task(ctx: Context, **kwargs):
    """Create a new task."""
    tasks = get_tasks(ctx)

    edit_task_id = ctx.state.get("edit_task_id")

    new_task = {
        "id": edit_task_id or str(uuid.uuid4()),
        "title": kwargs.get("new_task_title", "New Task"),
        "description": kwargs.get("new_task_description", ""),
        "priority": kwargs.get("new_task_priority", "medium"),
        "assignee": kwargs.get("new_task_assignee", ""),
        "due_date": kwargs.get("new_task_due_date", ""),
    }

    tasks["todo"].append(new_task)
    ctx.state.set("tasks", tasks)
    ctx.state.set("edit_task_id", None)

    await ctx.show_toast("Task created successfully!", variant="success")
    await ctx.refresh()


async def move_task(ctx: Context, task_id: str, target_column: str):
    """Move task to a different column."""
    tasks = get_tasks(ctx)
    task_to_move = None

    # Find and remove task from current column
    for column in ["todo", "in_progress", "done"]:
        for i, task in enumerate(tasks[column]):
            if task["id"] == task_id:
                task_to_move = tasks[column].pop(i)
                break
        if task_to_move:
            break

    # Add to target column
    if task_to_move and target_column:
        tasks[target_column].append(task_to_move)
        ctx.state.set("tasks", tasks)
        await ctx.show_toast(
            f"Task moved to {target_column.replace('_', ' ').title()}", variant="info"
        )
        await ctx.refresh()


async def delete_task(ctx: Context, task_id: str):
    """Delete a task."""
    tasks = get_tasks(ctx)

    # Find and remove task
    for column in ["todo", "in_progress", "done"]:
        for i, task in enumerate(tasks[column]):
            if task["id"] == task_id:
                tasks[column].pop(i)
                ctx.state.set("tasks", tasks)
                await ctx.show_toast("Task deleted", variant="success")
                await ctx.refresh()
                return


def get_priority_badge(priority: str):
    """Get badge component for priority."""
    variants = {
        "high": "destructive",
        "medium": "warning",
        "low": "secondary",
    }
    return Badge(
        priority.capitalize(),
        variant=variants.get(priority, "default"),
    )


async def search_tasks(ctx: Context, search: str):
    """Search tasks by title."""
    tasks = get_tasks(ctx)
    search = search.lower()

    if search:
        filtered_tasks = {
            "todo": [task for task in tasks["todo"] if search in task["title"].lower()],
            "in_progress": [task for task in tasks["in_progress"] if search in task["title"].lower()],
            "done": [task for task in tasks["done"] if search in task["title"].lower()],
        }
        ctx.state.set("filtered_tasks", filtered_tasks)
    else:
        ctx.state.set("filtered_tasks", None)
    await ctx.refresh()


async def open_edit(ctx: Context, task_id: str):
    """Open edit dialog for a task."""
    # For simplicity, we'll just show a toast here. In a real app, you'd open a sheet or modal with a form.
    await ctx.show_toast("Edit task functionality not implemented in this example.", variant="info")


def render_task_card(task: dict, column: str, ctx: Context):
    """Render a task card."""
    return Card(
        class_name="mb-2",
        children=[
            CardContent(
                class_name="p-4",
                children=[
                    Column(
                        gap=3,
                        children=[
                            # Header with title and menu
                            Row(
                                justify="between",
                                align="start",
                                children=[
                                    Text(task["title"], class_name="font-medium text-sm"),
                                    DropdownMenu(
                                        children=[
                                            DropdownMenuTrigger(
                                                children=Button(
                                                    label="⋮",
                                                    variant="ghost",
                                                    size="sm",
                                                    class_name="p-0",
                                                    style={"width": "1.5rem", "height": "1.5rem"},
                                                )
                                            ),
                                            DropdownMenuContent(
                                                children=[
                                                    DropdownMenuItem(
                                                        label="Edit",
                                                        on_select=ctx.callback(open_edit, task_id=task["id"])
                                                    ),
                                                    DropdownMenuSeparator(),
                                                    DropdownMenuItem(
                                                        label="Move to To Do",
                                                        on_select=ctx.callback(
                                                            move_task,
                                                            task_id=task["id"],
                                                            target_column="todo",
                                                        ),
                                                    )
                                                    if column != "todo"
                                                    else None,
                                                    DropdownMenuItem(
                                                        label="Move to In Progress",
                                                        on_select=ctx.callback(
                                                            move_task,
                                                            task_id=task["id"],
                                                            target_column="in_progress",
                                                        ),
                                                    )
                                                    if column != "in_progress"
                                                    else None,
                                                    DropdownMenuItem(
                                                        label="Move to Done",
                                                        on_select=ctx.callback(
                                                            move_task,
                                                            task_id=task["id"],
                                                            target_column="done",
                                                        ),
                                                    )
                                                    if column != "done"
                                                    else None,
                                                    DropdownMenuSeparator(),
                                                    DropdownMenuItem(
                                                        label="Delete",
                                                        on_select=ctx.callback(
                                                            delete_task, task_id=task["id"]
                                                        ),
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            # Description
                            Text(
                                task["description"],
                                class_name="text-xs text-muted-foreground",
                                style={
                                    "display": "-webkit-box",
                                    "WebkitLineClamp": "2",
                                    "WebkitBoxOrient": "vertical",
                                    "overflow": "hidden",
                                },
                            )
                            if task["description"]
                            else None,
                            # Footer with priority and assignee
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    get_priority_badge(task["priority"]),
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Avatar(
                                                fallback=task["assignee"][0]
                                                if task["assignee"]
                                                else "?",
                                                size="sm",
                                            ),
                                            Text(
                                                task["due_date"],
                                                class_name="text-xs text-muted-foreground",
                                            )
                                            if task["due_date"]
                                            else None,
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


def render_column(
    title: str, column_id: str, tasks: list, ctx: Context, color: str, color_style: dict = None
):
    """Render a kanban column."""
    return Container(
        class_name="flex-none",
        style={"width": "20rem"},
        children=[
            Card(
                style={"height": "100%"},
                children=[
                    CardHeader(
                        class_name="pb-3",
                        children=[
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Container(
                                                class_name=f"rounded-full {color}",
                                                style={
                                                    **{"width": "0.75rem", "height": "0.75rem"},
                                                    **(color_style or {}),
                                                },
                                            ),
                                            Text(title, class_name="font-semibold"),
                                            Badge(
                                                str(len(tasks)),
                                                variant="secondary",
                                            ),
                                        ],
                                    ),
                                    add_task_button_sheet(ctx) if column_id == "todo" else None,
                                ],
                            ),
                        ],
                    ),
                    CardContent(
                        class_name="pt-0",
                        children=[
                            ScrollArea(
                                style={"height": "calc(100vh - 280px)"},
                                children=[
                                    Column(
                                        gap=0,
                                        children=[
                                            render_task_card(task, column_id, ctx) for task in tasks
                                        ]
                                        if tasks
                                        else [
                                            Container(
                                                class_name="text-center py-8",
                                                children=[
                                                    Text(
                                                        "No tasks",
                                                        class_name="text-sm text-muted-foreground",
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
            ),
        ],
    )


"""Main page (kanban board) - fixed and properly defined as a ui page."""


@ui.page("/")
def board(ctx: Context):
    """Main kanban board page."""
    tasks = get_tasks(ctx)

    return Container(
        id="board-page",
        class_name="p-6 bg-background",
        style={"minHeight": "100vh"},
        children=[
            Column(
                id="board-container",
                class_name="min-h-screen bg-muted/30 p-6",
                children=[
                    Column(
                        id="board-header",
                        gap=6,
                        children=[
                            # Header
                            Row(
                                id="board-header-row",
                                justify="between",
                                align="center",
                                children=[
                                    Column(
                                        id="board-title-section",
                                        gap=1,
                                        children=[
                                            Text("Project Board", class_name="text-2xl font-bold"),
                                            Text(
                                                "Track and manage your project tasks",
                                                class_name="text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                    Row(
                                        id="board-controls",
                                        gap=2,
                                        children=[
                                            Input(
                                                id="search-input",
                                                name="search",
                                                placeholder="Search tasks...",
                                                style={"width": "16rem"},
                                                on_change=ctx.chain([
                                                    ctx.save_prop("search"),
                                                    ctx.callback(search_tasks, props=["search"], debounce=300),
                                                ])
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            # Board columns
                            Row(
                                gap=6,
                                class_name="pb-4",
                                style={"overflowX": "auto"},
                                children=[
                                    render_column(
                                        "To Do", "todo", tasks["todo"], ctx, "bg-secondary"
                                    ),
                                    render_column(
                                        "In Progress",
                                        "in_progress",
                                        tasks["in_progress"],
                                        ctx,
                                        "bg-primary",
                                    ),
                                    render_column(
                                        "Done",
                                        "done",
                                        tasks["done"],
                                        ctx,
                                        "",
                                        {"backgroundColor": "#22c55e"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

def add_task_button_sheet(ctx: Context):
    """Sheet for adding a new task."""
    return Sheet(
        id="task-sheet",
        children=[
            SheetTrigger(
                children=[
                    Tooltip(
                        content="Create New Task",
                        children=[
                            IconButton(
                                icon="plus",
                                aria_label="Create Task",
                                variant="ghost",
                                size="sm",
                            )
                        ],
                        side="bottom",
                    ),
                ],
            ),
            SheetContent(
                side="right",
                children=[
                    SheetHeader(
                        children=[
                            SheetTitle(
                                title="Create New Task"
                            ),
                            SheetDescription(
                                description="Add a new task to your board"
                            ),
                        ]
                    ),
                    Column(
                        gap=4,
                        class_name="py-6",
                        children=[
                            Column(
                                gap=2,
                                children=[
                                    Label("Title"),
                                    Input(
                                        name="new_task_title",
                                        placeholder="Task title",
                                        value=ctx.state.get(
                                            "new_task_title",
                                            "",
                                        ),
                                        on_change=ctx.save_prop("new_task_title"),
                                    ),
                                ],
                            ),
                            Column(
                                gap=2,
                                children=[
                                    Label("Description"),
                                    Textarea(
                                        name="new_task_description",
                                        placeholder="Task description",
                                        rows=3,
                                        value=ctx.state.get(
                                            "new_task_description",
                                            "",
                                        ),
                                        on_change=ctx.save_prop("new_task_description"),
                                    ),
                                ],
                            ),
                            Column(
                                gap=2,
                                children=[
                                    Label("Priority"),
                                    Select(
                                        name="new_task_priority",
                                        value=ctx.state.get(
                                            "new_task_priority",
                                            "medium",
                                        ),
                                        on_change=ctx.save_prop("new_task_priority"),
                                        options=[
                                            {
                                                "value": "high",
                                                "label": "High",
                                            },
                                            {
                                                "value": "medium",
                                                "label": "Medium",
                                            },
                                            {
                                                "value": "low",
                                                "label": "Low",
                                            },
                                        ],
                                    ),
                                ],
                            ),
                            Column(
                                gap=2,
                                children=[
                                    Label("Assignee"),
                                    Input(
                                        name="new_task_assignee",
                                        placeholder="Assignee name",
                                        value=ctx.state.get(
                                            "new_task_assignee",
                                            "",
                                        ),
                                        on_change=ctx.save_prop("new_task_assignee"),
                                    ),
                                ],
                            ),
                            Column(
                                gap=2,
                                children=[
                                    Label("Due Date"),
                                    Input(
                                        name="new_task_due_date",
                                        type="date",
                                        value=ctx.state.get(
                                            "new_task_due_date",
                                            "",
                                        ),
                                        on_change=ctx.save_prop("new_task_due_date"),
                                    ),
                                ],
                            ),
                            Button(
                                label="Create Task",
                                on_click=ctx.callback(
                                    create_task,
                                    props=[
                                        "new_task_title",
                                        "new_task_description",
                                        "new_task_priority",
                                        "new_task_assignee",
                                        "new_task_due_date",
                                    ]
                                ),
                                class_name="mt-4",
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
