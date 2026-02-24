"""Quick Tour — /docs/quick-tour."""

from refast.components import (
    Container,
    Heading,
    Markdown,
    Separator,
)


PAGE_TITLE = "Quick Tour"
PAGE_ROUTE = "/docs/quick-tour"


def render(ctx):
    """Render the quick tour page."""
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


# ---------------------------------------------------------------------------
# PAGE CONTENT — To be expanded by an agent.
# See getting_started/AGENT_INSTRUCTIONS.md for full requirements.
# ---------------------------------------------------------------------------

CONTENT = r"""
## Build a Todo App in 5 Minutes

Let's build a functional Todo application. We'll cover **creating an app**, **state management**, **handling user input**, and **updating the UI**.

> **Live Demo**: Check out the [working Todo App](/docs/todo-live) running right inside these docs!

### Step 1: Create the App

First, we need the basic scaffolding. Create a file named `todo_app.py`:

```python
from uuid import uuid4
from fastapi import FastAPI
from refast import RefastApp, Context
from refast import components as rc

app = FastAPI()
ui = RefastApp(title="Getting Started - ToDo App")

# We'll define our page handler here next...

app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 2: Define State & Page

We need a way to store our todos. We'll use `ctx.state`, which persists data for the active user connection.

```python
@ui.page("/")
def home(ctx: Context):
    # Initialize or retrieve existing todos
    todos = ctx.state.get("todos", [])
    
    return rc.Container(
        class_name="p-8 max-w-md mx-auto mt-10 border rounded-lg shadow-sm",
        children=[
            rc.Heading("ToDo App Example", level=1, class_name="mb-4"),
            # We will add the UI components here next...
        ],
    )
```

### Step 3: Build the UI

Now let's assemble the components in the `home` function. We'll reference two callback functions (`add_todo` and `mark_todo`) that we haven't defined yet—don't worry, we'll implement those in the next steps!

```python
@ui.page("/")
def home(ctx: Context):
    todos = ctx.state.get("todos", [])
    
    return rc.Container(
        class_name="p-8 max-w-md mx-auto mt-10 border rounded-lg shadow-sm",
        children=[
            rc.Heading("ToDo App Example", level=1, class_name="mb-4"),
            
            # Input Row
            rc.Row(
                children=[
                    rc.Input(
                        name="new_todo",
                        placeholder="Enter a new todo",
                        id="new-todo-input",
                        class_name="flex-1 mr-2",
                        # Bind the input value to a prop named "new_todo"
                        # This is stored in a global prop store that can be accessed
                        # in other callbacks like the on_click callback of the Add button.
                        on_change=ctx.save_prop("new_todo", debounce=300),
                    ),
                    rc.Button(
                        "Add",
                        variant="primary",
                        # Pass the "new_todo" prop to the callback
                        on_click=ctx.callback(add_todo, props=["new_todo"]),
                    ),
                ]
            ),
            
            # Todo List
            rc.Column(
                id="todo-list",
                gap=2,
                class_name="mt-6",
                children=[
                    rc.Row( # Each todo item is a row with a checkbox and text
                        gap=2,
                        align="center",
                        children=[
                            rc.Checkbox(
                                checked=todo["completed"],
                                on_change=ctx.callback(mark_todo, todo_id=todo["id"]),
                            ),
                            rc.Text(
                                todo["text"],
                                # If the todo is completed, apply a line-through style
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
```

### Step 4: Add Todo Logic

Now let's create the `add_todo` callback function to handle adding new items.

```python
async def add_todo(ctx: Context, new_todo: str):
    todos = ctx.state.get("todos", [])
    
    if new_todo:
        unique_id = str(uuid4())
        todos.append({"id": unique_id, "text": new_todo, "completed": False})
        ctx.state["todos"] = todos
        
        # Refresh just the list part of the page
        await ctx.refresh(target_id="todo-list")
        await ctx.show_toast(f'Added todo: "{new_todo}"', variant="success")
    else:
        await ctx.show_toast("Please enter a todo item.", variant="error")
```

### Step 5: Toggle Completion Logic

Finally, implement the `mark_todo` function to mark items as done.

```python
async def mark_todo(ctx: Context, todo_id: str):
    todos = ctx.state.get("todos", [])
    for todo in todos:
        if todo["id"] == todo_id:
            # Toggle the completed status
            todo["completed"] = not todo["completed"]
            break
    ctx.state["todos"] = todos
    await ctx.refresh(target_id="todo-list")
```

### Step 6: Run It

Run the app using Python directly or via `uvicorn`:

```bash
python todo_app.py
# or
uvicorn todo_app:app --reload
```

Visit [http://localhost:8000](http://localhost:8000) to inspect your new Todo app!

## Summary

In this quick tour, you learned:

- **`@ui.page`**: To route requests to UI handlers.
- **`ctx.save_prop`**: To bind input values to props accessible in callbacks.
- **`ctx.callback`**: To trigger Python functions from UI events, passing props like `new_todo`.
- **`ctx.refresh(target_id=...)`**: To re-render specific parts of the page for better performance.
- **`ctx.show_toast`**: To display notifications.
"""
