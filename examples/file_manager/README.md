# File Manager Example

A file browser interface with folder navigation, selection, and file operations.

## Features Demonstrated

- **Collapsible** - Expandable folder tree in sidebar
- **ContextMenu** - Right-click file actions
- **DropdownMenu** - Per-file action menus
- **Breadcrumb** - Path navigation
- **AlertDialog** - Delete confirmation
- **ScrollArea** - Scrollable file lists
- **Checkbox** - File selection
- **Input** - File search

## Interface Sections

1. **Sidebar** - Folder tree navigation with collapsible nodes
2. **Toolbar** - Breadcrumb path, search, view toggle
3. **Selection Bar** - Selection count, bulk actions
4. **File List** - Files with icons, size, modified date

## Key Patterns

### Folder Tree Rendering
```python
def render_sidebar_folder(folder: dict, ctx: Context, depth: int = 0):
    children_folders = [c for c in folder.get("children", []) if c["type"] == "folder"]
    
    if children_folders:
        return Collapsible(
            default_open=depth < 2,
            children=[
                Row(
                    children=[
                        CollapsibleTrigger(children=Text("▶")),
                        Row(
                            on_click=ctx.callback(navigate_to, folder_id=folder["id"]),
                            children=[Text("📁"), Text(folder["name"])],
                        ),
                    ],
                ),
                CollapsibleContent(
                    children=[
                        render_sidebar_folder(child, ctx, depth + 1)
                        for child in children_folders
                    ],
                ),
            ],
        )
```

### Context Menu for Files
```python
ContextMenu(
    children=[
        ContextMenuTrigger(children=file_row),
        ContextMenuContent(
            children=[
                ContextMenuItem(label="Open"),
                ContextMenuItem(label="Download"),
                ContextMenuSeparator(),
                ContextMenuItem(label="Rename"),
                ContextMenuItem(label="Copy"),
                ContextMenuItem(label="Delete"),
            ],
        ),
    ],
)
```

### File Type Icons
```python
def get_file_icon(item: dict) -> str:
    if item["type"] == "folder":
        return "📁"
    name = item["name"].lower()
    if name.endswith((".jpg", ".png")):
        return "🖼️"
    elif name.endswith(".pdf"):
        return "📄"
    elif name.endswith(".py"):
        return "🐍"
    # ... more types
```

## Running

```bash
cd examples/file_manager
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.
