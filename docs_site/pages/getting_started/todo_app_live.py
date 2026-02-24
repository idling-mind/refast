"""Live Todo App Demo."""

from uuid import uuid4

from refast import Context
from refast import components as rc

PAGE_TITLE = "Live Todo App"
PAGE_ROUTE = "/docs/todo-live"


async def add_todo(ctx: Context, new_todo: str):
    todos = ctx.state.get("todos", [])
    if new_todo:
        unique_id = str(uuid4())
        todos.append({"id": unique_id, "text": new_todo, "completed": False})
        ctx.state["todos"] = todos
        await ctx.update_props("new-todo-input", {"value": ""})
        await ctx.replace("todo-list", render_todo_list(ctx))
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
    await ctx.replace("todo-list", render_todo_list(ctx))

def render_todo_list(ctx: Context) -> rc.Component:
    todos = ctx.state.get("todos", [])
    return rc.Column(
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
    )

def render(ctx: Context):
    """Render the live todo app page."""
    from docs_site.app import docs_layout

    
    # The actual app content
    app_content = rc.Container(
        class_name="p-8 border rounded-lg shadow-sm bg-card",
        children=[
            rc.Heading("ToDo List", level=2, class_name="mb-4"),
            rc.Row(
                children=[
                    rc.Input(
                        name="new_todo",
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
            render_todo_list(ctx),
        ],
    )

    content = rc.Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            rc.Heading(PAGE_TITLE, level=1),
            rc.Separator(class_name="my-4"),
            rc.Paragraph(
                """
                This is a live demo of the Todo App built in the Quick Tour. 
                It is running right here inside the documentation site!
                """
            ),
            rc.Flex(
                class_name="gap-4 my-8", children=[app_content]
            ),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)
