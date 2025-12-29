# Kanban Board Example

A task management board with columns and drag-and-drop style task organization.

## Features Demonstrated

- **Card** - Task cards with metadata
- **ScrollArea** - Scrollable column content
- **DropdownMenu** - Task action menus
- **Sheet** - Slide-out task creation form
- **Badge** - Priority indicators
- **Avatar** - Assignee display
- **Input/Textarea/Select** - Form inputs
- **Label** - Form labels

## Columns

- **To Do** - Tasks not yet started
- **In Progress** - Tasks being worked on
- **Done** - Completed tasks

## Key Patterns

### Move Task Between Columns
```python
async def move_task(ctx: Context):
    task_id = ctx.event_data.get("task_id")
    target_column = ctx.event_data.get("target_column")
    
    tasks = get_tasks(ctx)
    task_to_move = None
    
    # Find and remove from current column
    for column in ["todo", "in_progress", "done"]:
        for i, task in enumerate(tasks[column]):
            if task["id"] == task_id:
                task_to_move = tasks[column].pop(i)
                break
    
    # Add to target column
    if task_to_move and target_column:
        tasks[target_column].append(task_to_move)
        ctx.state.set("tasks", tasks)
        await ctx.refresh()
```

### Create Task via Sheet
```python
async def create_task(ctx: Context):
    tasks = get_tasks(ctx)
    
    new_task = {
        "id": str(uuid.uuid4()),
        "title": ctx.state.get("new_task_title", "New Task"),
        "description": ctx.state.get("new_task_description", ""),
        "priority": ctx.state.get("new_task_priority", "medium"),
        "assignee": ctx.state.get("new_task_assignee", ""),
    }
    
    tasks["todo"].append(new_task)
    ctx.state.set("tasks", tasks)
    await ctx.refresh()
```

## Running

```bash
cd examples/kanban_board
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.
