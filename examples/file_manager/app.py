"""File Manager Example - Demonstrates a file browser interface.

This example demonstrates:
- Tree-like folder structure with Collapsible
- Context menus for file actions
- Breadcrumb navigation
- File/folder icons and types
- Selection and multi-select
- Rename and delete dialogs
"""


from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    Button,
    Checkbox,
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
    Column,
    Container,
    ContextMenu,
    ContextMenuContent,
    ContextMenuItem,
    ContextMenuSeparator,
    ContextMenuTrigger,
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
    Input,
    Row,
    ScrollArea,
    Separator,
    Text,
    ThemeSwitcher,
)

# Create the Refast app
ui = RefastApp(title="File Manager")


# Sample file system structure
FILE_SYSTEM = {
    "id": "root",
    "name": "My Files",
    "type": "folder",
    "children": [
        {
            "id": "documents",
            "name": "Documents",
            "type": "folder",
            "children": [
                {
                    "id": "doc1",
                    "name": "Resume.pdf",
                    "type": "file",
                    "size": "125 KB",
                    "modified": "2024-12-15",
                },
                {
                    "id": "doc2",
                    "name": "Cover Letter.docx",
                    "type": "file",
                    "size": "45 KB",
                    "modified": "2024-12-14",
                },
                {
                    "id": "doc3",
                    "name": "Report Q4.xlsx",
                    "type": "file",
                    "size": "2.3 MB",
                    "modified": "2024-12-10",
                },
            ],
        },
        {
            "id": "images",
            "name": "Images",
            "type": "folder",
            "children": [
                {
                    "id": "img1",
                    "name": "vacation-photo.jpg",
                    "type": "file",
                    "size": "3.5 MB",
                    "modified": "2024-12-01",
                },
                {
                    "id": "img2",
                    "name": "profile-picture.png",
                    "type": "file",
                    "size": "256 KB",
                    "modified": "2024-11-28",
                },
                {
                    "id": "img3",
                    "name": "screenshot.png",
                    "type": "file",
                    "size": "1.2 MB",
                    "modified": "2024-12-12",
                },
            ],
        },
        {
            "id": "projects",
            "name": "Projects",
            "type": "folder",
            "children": [
                {
                    "id": "project1",
                    "name": "Website Redesign",
                    "type": "folder",
                    "children": [
                        {
                            "id": "p1f1",
                            "name": "index.html",
                            "type": "file",
                            "size": "12 KB",
                            "modified": "2024-12-15",
                        },
                        {
                            "id": "p1f2",
                            "name": "styles.css",
                            "type": "file",
                            "size": "8 KB",
                            "modified": "2024-12-15",
                        },
                        {
                            "id": "p1f3",
                            "name": "app.js",
                            "type": "file",
                            "size": "25 KB",
                            "modified": "2024-12-15",
                        },
                    ],
                },
                {
                    "id": "project2",
                    "name": "Mobile App",
                    "type": "folder",
                    "children": [
                        {
                            "id": "p2f1",
                            "name": "main.py",
                            "type": "file",
                            "size": "15 KB",
                            "modified": "2024-12-14",
                        },
                        {
                            "id": "p2f2",
                            "name": "requirements.txt",
                            "type": "file",
                            "size": "1 KB",
                            "modified": "2024-12-14",
                        },
                    ],
                },
            ],
        },
        {
            "id": "notes",
            "name": "notes.txt",
            "type": "file",
            "size": "2 KB",
            "modified": "2024-12-16",
        },
        {
            "id": "readme",
            "name": "README.md",
            "type": "file",
            "size": "5 KB",
            "modified": "2024-12-15",
        },
    ],
}


def get_file_icon(item: dict) -> str:
    """Get icon for file or folder."""
    if item["type"] == "folder":
        return "📁"

    name = item["name"].lower()
    if name.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
        return "🖼️"
    elif name.endswith((".pdf",)):
        return "📄"
    elif name.endswith((".doc", ".docx")):
        return "📝"
    elif name.endswith((".xls", ".xlsx")):
        return "📊"
    elif name.endswith((".py",)):
        return "🐍"
    elif name.endswith((".js", ".ts")):
        return "📜"
    elif name.endswith((".html", ".css")):
        return "🌐"
    elif name.endswith((".md", ".txt")):
        return "📃"
    else:
        return "📄"


def find_item_by_id(root: dict, item_id: str) -> dict | None:
    """Find an item in the file system by ID."""
    if root["id"] == item_id:
        return root
    if root["type"] == "folder" and "children" in root:
        for child in root["children"]:
            result = find_item_by_id(child, item_id)
            if result:
                return result
    return None


def get_path_to_item(root: dict, item_id: str, path: list = None) -> list | None:
    """Get the path to an item."""
    if path is None:
        path = []

    if root["id"] == item_id:
        return path + [root]

    if root["type"] == "folder" and "children" in root:
        for child in root["children"]:
            result = get_path_to_item(child, item_id, path + [root])
            if result:
                return result
    return None


# Callback handlers
async def navigate_to(ctx: Context):
    """Navigate to a folder."""
    folder_id = ctx.event_data.get("folder_id")
    ctx.state.set("current_folder", folder_id)
    ctx.state.set("selected_items", [])
    await ctx.refresh()


async def toggle_selection(ctx: Context):
    """Toggle item selection."""
    item_id = ctx.event_data.get("item_id")
    selected = ctx.state.get("selected_items", [])

    if item_id in selected:
        selected.remove(item_id)
    else:
        selected.append(item_id)

    ctx.state.set("selected_items", selected)
    await ctx.refresh()


async def select_all(ctx: Context):
    """Select all items in current folder."""
    current_id = ctx.state.get("current_folder", "root")
    folder = find_item_by_id(FILE_SYSTEM, current_id)

    if folder and folder["type"] == "folder":
        all_ids = [child["id"] for child in folder.get("children", [])]
        ctx.state.set("selected_items", all_ids)
        await ctx.refresh()


async def clear_selection(ctx: Context):
    """Clear all selections."""
    ctx.state.set("selected_items", [])
    await ctx.refresh()


async def open_item(ctx: Context):
    """Open a file or folder."""
    item_id = ctx.event_data.get("item_id")
    item = find_item_by_id(FILE_SYSTEM, item_id)

    if item:
        if item["type"] == "folder":
            ctx.state.set("current_folder", item_id)
            ctx.state.set("selected_items", [])
            await ctx.refresh()
        else:
            await ctx.show_toast(f"Opening {item['name']}...", variant="info")


async def rename_item(ctx: Context):
    """Rename an item."""
    item_id = ctx.event_data.get("item_id")
    item = find_item_by_id(FILE_SYSTEM, item_id)
    if item:
        await ctx.show_toast(f"Rename dialog for {item['name']}", variant="info")


async def delete_items(ctx: Context):
    """Delete selected items."""
    selected = ctx.state.get("selected_items", [])
    count = len(selected)
    ctx.state.set("selected_items", [])
    await ctx.show_toast(f"Deleted {count} item(s)", variant="success")
    await ctx.refresh()


async def download_item(ctx: Context):
    """Download an item."""
    item_id = ctx.event_data.get("item_id")
    item = find_item_by_id(FILE_SYSTEM, item_id)
    if item:
        await ctx.show_toast(f"Downloading {item['name']}...", variant="info")


async def copy_items(ctx: Context):
    """Copy selected items."""
    selected = ctx.state.get("selected_items", [])
    ctx.state.set("clipboard", {"action": "copy", "items": selected})
    await ctx.show_toast(f"Copied {len(selected)} item(s)", variant="info")


async def cut_items(ctx: Context):
    """Cut selected items."""
    selected = ctx.state.get("selected_items", [])
    ctx.state.set("clipboard", {"action": "cut", "items": selected})
    await ctx.show_toast(f"Cut {len(selected)} item(s)", variant="info")


async def paste_items(ctx: Context):
    """Paste items from clipboard."""
    clipboard = ctx.state.get("clipboard", {})
    if clipboard:
        action = clipboard.get("action", "copy")
        items = clipboard.get("items", [])
        await ctx.show_toast(f"Pasted {len(items)} item(s)", variant="success")
        if action == "cut":
            ctx.state.set("clipboard", {})


async def create_folder(ctx: Context):
    """Create a new folder."""
    await ctx.show_toast("New folder created", variant="success")


async def upload_file(ctx: Context):
    """Upload a file."""
    await ctx.show_toast("Upload dialog opened", variant="info")


async def toggle_view(ctx: Context):
    """Toggle between grid and list view."""
    current = ctx.state.get("view_mode", "list")
    ctx.state.set("view_mode", "grid" if current == "list" else "list")
    await ctx.refresh()


def render_file_row(item: dict, ctx: Context, selected_items: list):
    """Render a file/folder row."""
    is_selected = item["id"] in selected_items
    is_folder = item["type"] == "folder"

    return ContextMenu(
        children=[
            ContextMenuTrigger(
                children=Row(
                    class_name=f"p-3 hover:bg-muted/50 cursor-pointer border-b {'bg-muted/30' if is_selected else ''}",
                    align="center",
                    on_double_click=ctx.callback(open_item, item_id=item["id"]),
                    children=[
                        Container(
                            class_name="w-8",
                            children=[
                                Checkbox(
                                    checked=is_selected,
                                    on_change=ctx.callback(toggle_selection, item_id=item["id"]),
                                ),
                            ],
                        ),
                        Row(
                            gap=3,
                            align="center",
                            class_name="flex-1",
                            children=[
                                Text(get_file_icon(item), class_name="text-xl"),
                                Text(item["name"], class_name="font-medium"),
                            ],
                        ),
                        Text(item.get("size", "-"), class_name="w-24 text-sm text-muted-foreground")
                        if not is_folder
                        else Container(class_name="w-24"),
                        Text(
                            item.get("modified", "-"),
                            class_name="w-32 text-sm text-muted-foreground",
                        ),
                        Container(
                            class_name="w-8",
                            children=[
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
                                                DropdownMenuItem(
                                                    label="Open",
                                                    on_select=ctx.callback(
                                                        open_item, item_id=item["id"]
                                                    ),
                                                ),
                                                DropdownMenuItem(
                                                    label="Download",
                                                    on_select=ctx.callback(
                                                        download_item, item_id=item["id"]
                                                    ),
                                                )
                                                if not is_folder
                                                else None,
                                                DropdownMenuSeparator(),
                                                DropdownMenuItem(
                                                    label="Rename",
                                                    on_select=ctx.callback(
                                                        rename_item, item_id=item["id"]
                                                    ),
                                                ),
                                                DropdownMenuItem(
                                                    label="Copy",
                                                    on_select=ctx.callback(copy_items),
                                                ),
                                                DropdownMenuItem(
                                                    label="Cut",
                                                    on_select=ctx.callback(cut_items),
                                                ),
                                                DropdownMenuSeparator(),
                                                DropdownMenuItem(label="Delete"),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ),
            ContextMenuContent(
                children=[
                    ContextMenuItem(
                        label="Open",
                        on_select=ctx.callback(open_item, item_id=item["id"]),
                    ),
                    ContextMenuItem(
                        label="Download",
                        on_select=ctx.callback(download_item, item_id=item["id"]),
                    )
                    if not is_folder
                    else None,
                    ContextMenuSeparator(),
                    ContextMenuItem(
                        label="Rename",
                        on_select=ctx.callback(rename_item, item_id=item["id"]),
                    ),
                    ContextMenuItem(label="Copy"),
                    ContextMenuItem(label="Cut"),
                    ContextMenuSeparator(),
                    ContextMenuItem(label="Delete"),
                ],
            ),
        ],
    )


def render_sidebar_folder(folder: dict, ctx: Context, depth: int = 0):
    """Render a folder in the sidebar."""
    current_id = ctx.state.get("current_folder", "root")
    is_active = folder["id"] == current_id

    children_folders = [c for c in folder.get("children", []) if c["type"] == "folder"]

    if children_folders:
        return Collapsible(
            default_open=depth < 2,
            children=[
                Row(
                    class_name=f"px-2 py-1 rounded hover:bg-muted cursor-pointer {'bg-muted' if is_active else ''}",
                    style={"paddingLeft": f"{depth * 12 + 8}px"},
                    children=[
                        CollapsibleTrigger(
                            children=Text("▶", class_name="text-xs mr-1"),
                        ),
                        Row(
                            gap=2,
                            class_name="flex-1",
                            on_click=ctx.callback(navigate_to, folder_id=folder["id"]),
                            children=[
                                Text("📁"),
                                Text(folder["name"], class_name="text-sm"),
                            ],
                        ),
                    ],
                ),
                CollapsibleContent(
                    children=[
                        render_sidebar_folder(child, ctx, depth + 1) for child in children_folders
                    ],
                ),
            ],
        )
    else:
        return Row(
            class_name=f"px-2 py-1 rounded hover:bg-muted cursor-pointer {'bg-muted' if is_active else ''}",
            style={"paddingLeft": f"{depth * 12 + 20}px"},
            on_click=ctx.callback(navigate_to, folder_id=folder["id"]),
            children=[
                Text("📁"),
                Text(folder["name"], class_name="text-sm ml-2"),
            ],
        )


# Main page
@ui.page("/")
def home(ctx: Context):
    """File manager page."""
    current_folder_id = ctx.state.get("current_folder", "root")
    selected_items = ctx.state.get("selected_items", [])
    view_mode = ctx.state.get("view_mode", "list")

    current_folder = find_item_by_id(FILE_SYSTEM, current_folder_id)
    path = get_path_to_item(FILE_SYSTEM, current_folder_id) or [FILE_SYSTEM]

    items = current_folder.get("children", []) if current_folder else []
    folders = [i for i in items if i["type"] == "folder"]
    files = [i for i in items if i["type"] == "file"]
    sorted_items = folders + files

    return Container(
        class_name="min-h-screen bg-background",
        children=[
            Row(
                children=[
                    # Sidebar
                    Container(
                        class_name="w-64 border-r min-h-screen p-4",
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Text("Files", class_name="text-lg font-bold px-2"),
                                    ThemeSwitcher(),
                                    # Quick actions
                                    Column(
                                        gap=1,
                                        children=[
                                            Button(
                                                label="+ New Folder",
                                                variant="outline",
                                                class_name="w-full justify-start",
                                                on_click=ctx.callback(create_folder),
                                            ),
                                            Button(
                                                label="↑ Upload File",
                                                variant="outline",
                                                class_name="w-full justify-start",
                                                on_click=ctx.callback(upload_file),
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Folder tree
                                    ScrollArea(
                                        class_name="h-[calc(100vh-200px)]",
                                        children=[
                                            Column(
                                                gap=1,
                                                children=[
                                                    render_sidebar_folder(FILE_SYSTEM, ctx),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Main content
                    Container(
                        class_name="flex-1",
                        children=[
                            Column(
                                gap=0,
                                children=[
                                    # Toolbar
                                    Row(
                                        class_name="p-4 border-b",
                                        justify="between",
                                        align="center",
                                        children=[
                                            # Breadcrumb
                                            Breadcrumb(
                                                children=[
                                                    BreadcrumbList(
                                                        children=[
                                                            item
                                                            for i, folder in enumerate(path)
                                                            for item in [
                                                                BreadcrumbItem(
                                                                    children=[
                                                                        BreadcrumbLink(
                                                                            label=folder["name"],
                                                                            href="#",
                                                                            on_click=ctx.callback(
                                                                                navigate_to,
                                                                                folder_id=folder[
                                                                                    "id"
                                                                                ],
                                                                            ),
                                                                        )
                                                                        if i < len(path) - 1
                                                                        else BreadcrumbPage(
                                                                            label=folder["name"]
                                                                        ),
                                                                    ]
                                                                ),
                                                                BreadcrumbSeparator()
                                                                if i < len(path) - 1
                                                                else None,
                                                            ]
                                                            if item is not None
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                children=[
                                                    Input(
                                                        name="search",
                                                        placeholder="Search files...",
                                                        class_name="w-64",
                                                    ),
                                                    Button(
                                                        label="≡" if view_mode == "list" else "⊞",
                                                        variant="outline",
                                                        on_click=ctx.callback(toggle_view),
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    # Selection bar
                                    Row(
                                        class_name="px-4 py-2 bg-muted/30 border-b",
                                        justify="between",
                                        align="center",
                                        children=[
                                            Row(
                                                gap=4,
                                                align="center",
                                                children=[
                                                    Checkbox(
                                                        checked=len(selected_items) > 0
                                                        and len(selected_items)
                                                        == len(sorted_items),
                                                        on_change=ctx.callback(
                                                            select_all
                                                            if len(selected_items)
                                                            < len(sorted_items)
                                                            else clear_selection
                                                        ),
                                                    ),
                                                    Text(
                                                        f"{len(selected_items)} selected"
                                                        if selected_items
                                                        else f"{len(sorted_items)} items",
                                                        class_name="text-sm text-muted-foreground",
                                                    ),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                children=[
                                                    Button(
                                                        label="Copy",
                                                        variant="outline",
                                                        size="sm",
                                                        disabled=len(selected_items) == 0,
                                                        on_click=ctx.callback(copy_items),
                                                    ),
                                                    Button(
                                                        label="Cut",
                                                        variant="outline",
                                                        size="sm",
                                                        disabled=len(selected_items) == 0,
                                                        on_click=ctx.callback(cut_items),
                                                    ),
                                                    Button(
                                                        label="Paste",
                                                        variant="outline",
                                                        size="sm",
                                                        on_click=ctx.callback(paste_items),
                                                    ),
                                                    AlertDialog(
                                                        children=[
                                                            AlertDialogTrigger(
                                                                children=Button(
                                                                    label="Delete",
                                                                    variant="destructive",
                                                                    size="sm",
                                                                    disabled=len(selected_items)
                                                                    == 0,
                                                                )
                                                            ),
                                                            AlertDialogContent(
                                                                children=[
                                                                    AlertDialogHeader(
                                                                        children=[
                                                                            AlertDialogTitle(
                                                                                title="Delete Items"
                                                                            ),
                                                                            AlertDialogDescription(
                                                                                description=f"Are you sure you want to delete {len(selected_items)} item(s)? This action cannot be undone."
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    AlertDialogFooter(
                                                                        children=[
                                                                            AlertDialogCancel(
                                                                                label="Cancel"
                                                                            ),
                                                                            AlertDialogAction(
                                                                                label="Delete",
                                                                                on_click=ctx.callback(
                                                                                    delete_items
                                                                                ),
                                                                            ),
                                                                        ]
                                                                    ),
                                                                ]
                                                            ),
                                                        ]
                                                    )
                                                    if selected_items
                                                    else "",
                                                ],
                                            ),
                                        ],
                                    ),
                                    # File list header
                                    Row(
                                        class_name="px-4 py-2 bg-muted/20 border-b text-sm font-medium text-muted-foreground",
                                        align="center",
                                        children=[
                                            Container(class_name="w-8"),
                                            Text("Name", class_name="flex-1"),
                                            Text("Size", class_name="w-24"),
                                            Text("Modified", class_name="w-32"),
                                            Container(class_name="w-8"),
                                        ],
                                    ),
                                    # File list
                                    ScrollArea(
                                        class_name="h-[calc(100vh-240px)]",
                                        children=[
                                            Column(
                                                gap=0,
                                                children=[
                                                    render_file_row(item, ctx, selected_items)
                                                    for item in sorted_items
                                                ]
                                                if sorted_items
                                                else [
                                                    Container(
                                                        class_name="flex items-center justify-center h-48",
                                                        children=[
                                                            Column(
                                                                gap=2,
                                                                align="center",
                                                                children=[
                                                                    Text(
                                                                        "📂",
                                                                        class_name="text-6xl opacity-50",
                                                                    ),
                                                                    Text(
                                                                        "This folder is empty",
                                                                        class_name="text-muted-foreground",
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
