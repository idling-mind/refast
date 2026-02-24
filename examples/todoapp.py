from uuid import uuid4

from fastapi import FastAPI

from refast import Context, RefastApp
from refast import components as rc

app = FastAPI()
ui = RefastApp(title="Getting Started - ToDo App")


async def add_todo(ctx: Context, new_todo: str):
    todos = ctx.state.get("todos", [])
    if new_todo:
        unique_id = str(uuid4())
        todos.append({"id": unique_id, "text": new_todo, "completed": False})
        ctx.state["todos"] = todos
        await ctx.refresh(target_id="todo-list")
        await ctx.show_toast(f'Added todo: "{new_todo}"', variant="success")
    else:
        await ctx.show_toast("Please enter a todo item.", variant="error")


async def mark_todo(ctx: Context, todo_id: str):
    todos = ctx.state.get("todos", [])
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            break
    ctx.state["todos"] = todos
    await ctx.refresh(target_id="todo-list")


@ui.page("/")
def home(ctx: Context):
    todos = ctx.state.get("todos", [])
    return rc.Container(
        class_name="p-8",
        children=[
            rc.Heading("ToDo App Example", level=1, class_name="mb-4"),
            rc.Row(
                children=[
                    rc.Input(
                        placeholder="Enter a new todo",
                        id="new-todo-input",
                        class_name="flex-1 mr-2",
                        on_change=ctx.save_prop("new_todo", debounce=300),
                    ),
                    rc.Button(
                        "Add",
                        variant="primary",
                        on_click=ctx.callback(add_todo, props=["new_todo"]),
                    ),
                ]
            ),
            rc.Column(
                id="todo-list",
                gap=2,
                class_name="mt-6",
                children=[
                    rc.Row(
                        gap=2,
                        align="center",
                        children=[
                            rc.Checkbox(
                                checked=todo["completed"],
                                on_change=ctx.callback(mark_todo, todo_id=todo["id"]),
                            ),
                            rc.Text(
                                todo["text"],
                                style={"textDecoration": "line-through"}
                                if todo["completed"]
                                else {},
                            ),
                        ],
                    )
                    for i, todo in enumerate(todos)
                ],
            ),
        ],
    )


app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
