"""Todo App Example - Task Management Application.

This example demonstrates:
- Form handling with inputs
- Dynamic list rendering
- CRUD operations (Create, Read, Update, Delete)
- State persistence within session
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Checkbox,
    Column,
    Container,
    IconButton,
    Input,
    Row,
    Text,
)


@dataclass
class Todo:
    """A todo item."""

    id: str
    text: str
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            text=data["text"],
            completed=data.get("completed", False),
            created_at=datetime.fromisoformat(data["created_at"]),
        )


# Create the Refast app
ui = RefastApp(title="Todo App")


def get_todos(ctx: Context) -> list[Todo]:
    """Get all todos from state."""
    todos_data = ctx.store.local.get("todos", [])
    return [Todo.from_dict(t) for t in todos_data]


async def update_new_todo_text(ctx: Context):
    """Update the new todo text in state."""
    print(ctx.event_data)
    ctx.state.set("new_todo_text", ctx.event_data.get("value", ""))


async def save_todos(ctx: Context, todos: list[Todo]) -> None:
    """Save todos to state."""
    ctx.store.local.set("todos", [t.to_dict() for t in todos])
    await ctx.refresh()


async def add_todo(ctx: Context):
    """Add a new todo item."""
    text = ctx.state.get("new_todo_text", "")
    print("Adding todo:", text)
    if not text.strip():
        return

    todos = get_todos(ctx)
    new_todo = Todo(
        id=str(uuid.uuid4()),
        text=text.strip(),
    )
    todos.append(new_todo)
    ctx.state.set("new_todo_text", "")
    await save_todos(ctx, todos)


async def toggle_todo(ctx: Context, todo_id: str = ""):
    """Toggle a todo's completed status."""
    todos = get_todos(ctx)
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = not todo.completed
            break
    await save_todos(ctx, todos)


async def delete_todo(ctx: Context, todo_id: str = ""):
    """Delete a todo item."""
    print("Deleting todo:", todo_id)
    todos = get_todos(ctx)
    todos = [t for t in todos if t.id != todo_id]
    await save_todos(ctx, todos)


async def clear_completed(ctx: Context):
    """Clear all completed todos."""
    todos = get_todos(ctx)
    todos = [t for t in todos if not t.completed]
    await save_todos(ctx, todos)


def render_todo_item(ctx: Context, todo: Todo):
    """Render a single todo item."""
    return Row(
        id=f"todo-{todo.id}",
        class_name=f"p-3 rounded-lg border {'bg-muted' if todo.completed else 'bg-card'}",
        align="center",
        gap=3,
        children=[
            Checkbox(
                id=f"checkbox-{todo.id}",
                checked=todo.completed,
                on_change=ctx.callback(toggle_todo, todo_id=todo.id),
            ),
            Container(
                class_name="flex-1",
                children=[
                    Text(
                        todo.text,
                        class_name=f"{'line-through text-muted-foreground' if todo.completed else ''}",
                    )
                ],
            ),
            IconButton(
                icon="x",
                id=f"delete-{todo.id}",
                variant="ghost",
                size="sm",
                aria_label=f"Delete {todo.text}",
                on_click=ctx.callback(delete_todo, todo_id=todo.id),
            ),
        ],
    )


@ui.page("/")
def home(ctx: Context):
    """Home page with todo list."""
    todos = get_todos(ctx)
    active_count = sum(1 for t in todos if not t.completed)
    completed_count = sum(1 for t in todos if t.completed)

    return Container(
        id="main-container",
        class_name="mt-10 px-4",
        style={"maxWidth": "32rem", "marginLeft": "auto", "marginRight": "auto"},
        children=[
            Card(
                id="todo-card",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    Column(
                                        children=[
                                            CardTitle("Todo App"),
                                            CardDescription("Manage your tasks efficiently"),
                                        ]
                                    ),
                                    Row(
                                        gap=2,
                                        children=[
                                            Badge(
                                                f"{active_count} active",
                                                variant="default",
                                            ),
                                            Badge(
                                                f"{completed_count} done",
                                                variant="success"
                                                if completed_count > 0
                                                else "secondary",
                                            ),
                                        ],
                                    ),
                                ],
                            )
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    # Add todo form
                                    Row(
                                        gap=2,
                                        children=[
                                            Container(
                                                class_name="flex-1",
                                                children=[
                                                    Input(
                                                        id="new-todo-input",
                                                        name="new_todo_text",
                                                        placeholder="What needs to be done?",
                                                        value=ctx.state.get("new_todo_text", ""),
                                                        debounce=300,
                                                        on_change=ctx.callback(
                                                            update_new_todo_text
                                                        ),
                                                    )
                                                ],
                                            ),
                                            Button(
                                                "Add",
                                                id="add-btn",
                                                variant="primary",
                                                on_click=ctx.callback(add_todo),
                                            ),
                                        ],
                                    ),
                                    # Todo list
                                    Column(
                                        id="todo-list",
                                        gap=2,
                                        children=[render_todo_item(ctx, todo) for todo in todos]
                                        if todos
                                        else [
                                            Text(
                                                "No todos yet. Add one above!",
                                                class_name="text-center text-muted-foreground py-8",
                                            )
                                        ],
                                    ),
                                    # Actions
                                    Row(
                                        justify="end",
                                        children=[
                                            Button(
                                                "Clear Completed",
                                                id="clear-btn",
                                                variant="outline",
                                                size="sm",
                                                disabled=completed_count == 0,
                                                on_click=ctx.callback(clear_completed),
                                            ),
                                        ],
                                    )
                                    if todos
                                    else Container(),
                                ],
                            )
                        ]
                    ),
                ],
            )
        ],
    )


# Create the FastAPI app and mount Refast
app = FastAPI(title="Refast Todo Example")
app.include_router(ui.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
