"""ContextMenu — /docs/components/context-menu.

Interactive reference page for the ContextMenu component family.
"""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Container,
    Heading,
    Markdown,
    Separator,
    Text,
)
from refast.components.shadcn.overlay import (
    ContextMenu,
    ContextMenuCheckboxItem,
    ContextMenuContent,
    ContextMenuItem,
    ContextMenuSeparator,
    ContextMenuTrigger,
)

PAGE_TITLE = "Context Menu"
PAGE_ROUTE = "/docs/components/context-menu"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _select_action(ctx: Context, action: str):
    ctx.state.set("cm_last_action", f'"{action}"')
    await ctx.refresh()


async def _toggle_bookmarks(ctx: Context, value: bool):
    ctx.state.set("cm_show_bookmarks", value)
    ctx.state.set("cm_last_action", f"Show bookmarks: {value}")
    await ctx.refresh()


async def _toggle_urls(ctx: Context, value: bool):
    ctx.state.set("cm_show_urls", value)
    ctx.state.set("cm_last_action", f"Show full URLs: {value}")
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    last_action = ctx.state.get("cm_last_action", "None")
    show_bookmarks = ctx.state.get("cm_show_bookmarks", True)
    show_urls = ctx.state.get("cm_show_urls", False)

    return playground_card(
        options=[],
        preview=[
            Text(
                "Right-click (or long-press) the area below to open the context menu.",
                class_name="text-sm text-muted-foreground mb-4",
            ),
            ContextMenu(
                children=[
                    ContextMenuTrigger(
                        children=[
                            Container(
                                class_name=(
                                    "border-2 border-dashed rounded-lg p-10 "
                                    "flex items-center justify-center "
                                    "select-none cursor-context-menu "
                                    "bg-muted/30 text-muted-foreground text-sm"
                                ),
                                children=[
                                    Text("Right-click here"),
                                ],
                            ),
                        ]
                    ),
                    ContextMenuContent(
                        children=[
                            ContextMenuItem(
                                "Back",
                                icon="arrow-left",
                                shortcut="⌘[",
                                on_select=ctx.callback(_select_action, action="Back"),
                            ),
                            ContextMenuItem(
                                "Forward",
                                icon="arrow-right",
                                shortcut="⌘]",
                                disabled=True,
                                on_select=ctx.callback(_select_action, action="Forward"),
                            ),
                            ContextMenuItem(
                                "Reload",
                                icon="refresh-cw",
                                shortcut="⌘R",
                                on_select=ctx.callback(_select_action, action="Reload"),
                            ),
                            ContextMenuSeparator(),
                            ContextMenuCheckboxItem(
                                "Show Bookmarks Bar",
                                checked=show_bookmarks,
                                on_checked_change=ctx.callback(_toggle_bookmarks),
                            ),
                            ContextMenuCheckboxItem(
                                "Show Full URLs",
                                checked=show_urls,
                                on_checked_change=ctx.callback(_toggle_urls),
                            ),
                            ContextMenuSeparator(),
                            ContextMenuItem(
                                "Save Page As…",
                                icon="save",
                                shortcut="⌘S",
                                on_select=ctx.callback(_select_action, action="Save Page As…"),
                            ),
                            ContextMenuItem(
                                "Print…",
                                icon="printer",
                                shortcut="⌘P",
                                on_select=ctx.callback(_select_action, action="Print…"),
                            ),
                        ]
                    ),
                ]
            ),
            Text(
                f"Last action: {last_action}",
                class_name="text-sm text-muted-foreground mt-4",
            ),
        ],
        code=Markdown(
            content=(
                "```python\n"
                "ContextMenu(\n"
                "    children=[\n"
                "        ContextMenuTrigger(\n"
                '            Container("Right-click here", ...)\n'
                "        ),\n"
                "        ContextMenuContent(\n"
                '            ContextMenuItem("Back", icon="arrow-left",\n'
                "                           on_select=ctx.callback(handle_back)),\n"
                '            ContextMenuItem("Reload", icon="refresh-cw",\n'
                "                           on_select=ctx.callback(handle_reload)),\n"
                "            ContextMenuSeparator(),\n"
                '            ContextMenuCheckboxItem("Show Bookmarks",\n'
                "                checked=show_bookmarks,\n"
                "                on_checked_change=ctx.callback(handle_bookmarks)),\n"
                "        ),\n"
                "    ]\n"
                ")\n"
                "```"
            )
        ),
        preview_class="",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the ContextMenu component reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _playground(ctx),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


# ── Content ───────────────────────────────────────────────────────────────

INTRO = """
Displays a floating menu when the user right-clicks (or long-presses on mobile) on
a target element. Supports items, separators, and checkbox items.

```python
from refast.components.shadcn.overlay import (
    ContextMenu, ContextMenuTrigger, ContextMenuContent,
    ContextMenuItem, ContextMenuSeparator, ContextMenuCheckboxItem,
)

ContextMenu(
    children=[
        ContextMenuTrigger(
            Container("Right-click here", class_name="border p-10 rounded-lg")
        ),
        ContextMenuContent(
            ContextMenuItem("Cut", icon="scissors", on_select=ctx.callback(handle_cut)),
            ContextMenuItem("Copy", icon="copy", on_select=ctx.callback(handle_copy)),
            ContextMenuItem("Paste", icon="clipboard", on_select=ctx.callback(handle_paste)),
        ),
    ]
)
```
"""

REFERENCE = """
## Component Reference

### ContextMenu

The root wrapper. Does not accept any interaction props directly — behaviour is
derived from its `ContextMenuTrigger` and `ContextMenuContent` children.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | *(required)* | Must contain `ContextMenuTrigger` and `ContextMenuContent` |
| `class_name` | `str` | `""` | Extra Tailwind classes on the root |

### ContextMenuTrigger

Wraps the element that will show the menu on right-click.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `Component` | *(required)* | The element the user right-clicks |
| `as_child` | `bool` | `False` | Merge props onto the child instead of wrapping |

### ContextMenuContent

The popover panel that appears after right-clicking.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | *(required)* | Menu items |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### ContextMenuItem

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Item text |
| `icon` | `str \\| None` | `None` | Lucide icon name |
| `shortcut` | `str \\| None` | `None` | Keyboard shortcut hint (display only) |
| `disabled` | `bool` | `False` | Greys out and prevents selection |
| `on_select` | `Callback \\| None` | `None` | Called when item is selected |

### ContextMenuSeparator

A horizontal rule with no configurable props (besides `class_name`).

### ContextMenuCheckboxItem

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Item text |
| `checked` | `bool` | `False` | Whether the checkbox is checked |
| `disabled` | `bool` | `False` | Prevents interaction |
| `on_checked_change` | `Callback \\| None` | `None` | Called with new `bool` value |

## Common Patterns

```python
# File manager row
ContextMenu(
    children=[
        ContextMenuTrigger(
            Row(children=[Text("document.pdf"), Text("2 MB")])
        ),
        ContextMenuContent(
            ContextMenuItem("Open", icon="folder-open",
                           on_select=ctx.callback(handle_open)),
            ContextMenuItem("Rename", icon="edit",
                           on_select=ctx.callback(handle_rename)),
            ContextMenuSeparator(),
            ContextMenuItem("Move to Trash", icon="trash",
                           on_select=ctx.callback(handle_delete)),
        ),
    ]
)

# Image with context menu
ContextMenu(
    children=[
        ContextMenuTrigger(
            Container(class_name="w-64 h-40 bg-muted rounded-lg overflow-hidden")
        ),
        ContextMenuContent(
            ContextMenuItem("Save Image As…", icon="download",
                           on_select=ctx.callback(handle_save)),
            ContextMenuItem("Copy Image", icon="copy",
                           on_select=ctx.callback(handle_copy)),
        ),
    ]
)
```
"""
