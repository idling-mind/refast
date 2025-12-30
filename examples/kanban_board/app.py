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
    if tasks is None:
        ctx.state.set("tasks", INITIAL_TASKS)
        return INITIAL_TASKS
    return tasks


# Callback handlers
async def create_task(ctx: Context):
    """Create a new task."""
    print(f"Creating new task... Event data: {ctx.event_data}")
    tasks = get_tasks(ctx)

    new_task = {
        "id": str(uuid.uuid4()),
        "title": ctx.state.get("new_task_title", "New Task"),
        "description": ctx.state.get("new_task_description", ""),
        "priority": ctx.state.get("new_task_priority", "medium"),
        "assignee": ctx.state.get("new_task_assignee", ""),
        "due_date": ctx.state.get("new_task_due_date", ""),
    }

    tasks["todo"].append(new_task)
    ctx.state.set("tasks", tasks)

    # Clear form
    ctx.state.set("new_task_title", "")
    ctx.state.set("new_task_description", "")
    ctx.state.set("new_task_priority", "medium")
    ctx.state.set("new_task_assignee", "")
    ctx.state.set("new_task_due_date", "")

    await ctx.show_toast("Task created successfully!", variant="success")
    await ctx.refresh()


async def move_task(ctx: Context):
    """Move task to a different column."""
    print(f"Moving task... Event data: {ctx.event_data}")
    task_id = ctx.event_data.get("task_id")
    target_column = ctx.event_data.get("target_column")
    print(f"Moving task {task_id} to column {target_column}")

    tasks = get_tasks(ctx)
    task_to_move = None
    source_column = None

    # Find and remove task from current column
    for column in ["todo", "in_progress", "done"]:
        for i, task in enumerate(tasks[column]):
            if task["id"] == task_id:
                task_to_move = tasks[column].pop(i)
                source_column = column
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


async def delete_task(ctx: Context):
    """Delete a task."""
    print(f"Deleting task... Event data: {ctx.event_data}")
    task_id = ctx.event_data.get("task_id")
    print(f"Deleting task {task_id}")
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


async def update_input(ctx: Context):
    """Update form input value."""
    print(f"Updating input... Event data: {ctx.event_data}")
    key = ctx.event_data.get("key")
    value = ctx.event_data.get("value", "")
    print(f"Updating {key} to {value}")
    ctx.state.set(key, value)


def get_priority_badge(priority: str):
    """Get badge component for priority."""
    variants = {
        "high": "destructive",
        "medium": "warning",
        "low": "secondary",
    }
    return Badge(
        text=priority.capitalize(),
        variant=variants.get(priority, "default"),
    )


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
                                                    class_name="h-6 w-6 p-0",
                                                )
                                            ),
                                            DropdownMenuContent(
                                                children=[
                                                    DropdownMenuItem(label="Edit"),
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
                                class_name="text-xs text-muted-foreground line-clamp-2",
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


def render_column(title: str, column_id: str, tasks: list, ctx: Context, color: str):
    """Render a kanban column."""
    return Container(
        class_name="w-80 flex-shrink-0",
        children=[
            Card(
                class_name="h-full",
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
                                                class_name=f"w-3 h-3 rounded-full {color}",
                                            ),
                                            Text(title, class_name="font-semibold"),
                                            Badge(
                                                text=str(len(tasks)),
                                                variant="secondary",
                                            ),
                                        ],
                                    ),
                                    Button(
                                        label="+",
                                        variant="ghost",
                                        size="sm",
                                        class_name="h-6 w-6 p-0",
                                    ),
                                ],
                            ),
                        ],
                    ),
                    CardContent(
                        class_name="pt-0",
                        children=[
                            ScrollArea(
                                class_name="h-[calc(100vh-280px)]",
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


# Main page
@ui.page("/")
def home(ctx: Context):
    """Kanban board page."""
    tasks = get_tasks(ctx)

    return Container(
        class_name="min-h-screen bg-muted/30 p-6",
        children=[
            Column(
                gap=6,
                children=[
                    # Header
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Column(
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
                                gap=2,
                                children=[
                                    Input(
                                        name="search",
                                        placeholder="Search tasks...",
                                        class_name="w-64",
                                    ),
                                    Sheet(
                                        children=[
                                            SheetTrigger(children=Button(label="+ Add Task")),
                                            SheetContent(
                                                side="right",
                                                children=[
                                                    SheetHeader(
                                                        children=[
                                                            SheetTitle(title="Create New Task"),
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
                                                                            "new_task_title", ""
                                                                        ),
                                                                        on_change=ctx.callback(
                                                                            update_input,
                                                                            key="new_task_title",
                                                                        ),
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
                                                                        on_change=ctx.callback(
                                                                            update_input,
                                                                            key="new_task_description",
                                                                        ),
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
                                                                        on_change=ctx.callback(
                                                                            update_input,
                                                                            key="new_task_priority",
                                                                        ),
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
                                                                            "new_task_assignee", ""
                                                                        ),
                                                                        on_change=ctx.callback(
                                                                            update_input,
                                                                            key="new_task_assignee",
                                                                        ),
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
                                                                            "new_task_due_date", ""
                                                                        ),
                                                                        on_change=ctx.callback(
                                                                            update_input,
                                                                            key="new_task_due_date",
                                                                        ),
                                                                    ),
                                                                ],
                                                            ),
                                                            Button(
                                                                label="Create Task",
                                                                on_click=ctx.callback(create_task),
                                                                class_name="mt-4",
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
                    # Board columns
                    Row(
                        gap=6,
                        class_name="overflow-x-auto pb-4",
                        children=[
                            render_column("To Do", "todo", tasks["todo"], ctx, "bg-slate-500"),
                            render_column(
                                "In Progress",
                                "in_progress",
                                tasks["in_progress"],
                                ctx,
                                "bg-blue-500",
                            ),
                            render_column("Done", "done", tasks["done"], ctx, "bg-green-500"),
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
