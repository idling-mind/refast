"""DropdownMenu — /docs/components/dropdown-menu.

Interactive reference page for the DropdownMenu component family.
"""

from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Separator,
    Text,
)
from refast.components.shadcn.overlay import (
    DropdownMenu,
    DropdownMenuCheckboxItem,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuRadioGroup,
    DropdownMenuRadioItem,
    DropdownMenuSeparator,
    DropdownMenuSub,
    DropdownMenuSubContent,
    DropdownMenuSubTrigger,
    DropdownMenuTrigger,
)

PAGE_TITLE = "Dropdown Menu"
PAGE_ROUTE = "/docs/components/dropdown-menu"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _select_item(ctx: Context, item: str):
    ctx.state.set("dm_last_action", f'Selected: "{item}"')
    await ctx.refresh()


async def _toggle_show_status_bar(ctx: Context, checked: bool):
    ctx.state.set("dm_show_status_bar", checked)
    ctx.state.set("dm_last_action", f"Status bar: {'visible' if checked else 'hidden'}")
    await ctx.refresh()


async def _toggle_show_activity(ctx: Context, checked: bool):
    ctx.state.set("dm_show_activity", checked)
    ctx.state.set("dm_last_action", f"Activity bar: {'visible' if checked else 'hidden'}")
    await ctx.refresh()


async def _set_position(ctx: Context, value: str):
    ctx.state.set("dm_position", value)
    ctx.state.set("dm_last_action", f'Panel position: "{value}"')
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    last_action = ctx.state.get("dm_last_action", "None")
    show_status_bar = ctx.state.get("dm_show_status_bar", True)
    show_activity = ctx.state.get("dm_show_activity", False)
    position = ctx.state.get("dm_position", "bottom")

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    Container(
                        class_name="border rounded-lg p-6 flex flex-col items-center gap-4 min-h-[120px] bg-muted/30 mb-4",
                        children=[
                            DropdownMenu(
                                children=[
                                    DropdownMenuTrigger(
                                        children=[
                                            Button("Open Menu", variant="outline", icon="chevron-down", icon_position="right"),
                                        ]
                                    ),
                                    DropdownMenuContent(
                                        children=[
                                            DropdownMenuLabel("My Account"),
                                            DropdownMenuSeparator(),
                                            DropdownMenuItem(
                                                "Profile",
                                                icon="user",
                                                shortcut="⇧⌘P",
                                                on_select=ctx.callback(_select_item, item="Profile"),
                                            ),
                                            DropdownMenuItem(
                                                "Billing",
                                                icon="credit-card",
                                                shortcut="⌘B",
                                                on_select=ctx.callback(_select_item, item="Billing"),
                                            ),
                                            DropdownMenuItem(
                                                "Settings",
                                                icon="settings",
                                                shortcut="⌘S",
                                                on_select=ctx.callback(_select_item, item="Settings"),
                                            ),
                                            DropdownMenuSeparator(),
                                            DropdownMenuLabel("Appearance"),
                                            DropdownMenuCheckboxItem(
                                                "Status Bar",
                                                checked=show_status_bar,
                                                on_checked_change=ctx.callback(_toggle_show_status_bar),
                                            ),
                                            DropdownMenuCheckboxItem(
                                                "Activity Bar",
                                                checked=show_activity,
                                                on_checked_change=ctx.callback(_toggle_show_activity),
                                            ),
                                            DropdownMenuSeparator(),
                                            DropdownMenuLabel("Panel Position"),
                                            DropdownMenuRadioGroup(
                                                value=position,
                                                on_value_change=ctx.callback(_set_position),
                                                children=[
                                                    DropdownMenuRadioItem("Top", value="top"),
                                                    DropdownMenuRadioItem("Bottom", value="bottom"),
                                                    DropdownMenuRadioItem("Right", value="right"),
                                                ],
                                            ),
                                            DropdownMenuSeparator(),
                                            DropdownMenuSub(
                                                children=[
                                                    DropdownMenuSubTrigger("Share", icon="share"),
                                                    DropdownMenuSubContent(
                                                        children=[
                                                            DropdownMenuItem(
                                                                "Email",
                                                                icon="mail",
                                                                on_select=ctx.callback(_select_item, item="Email"),
                                                            ),
                                                            DropdownMenuItem(
                                                                "Message",
                                                                icon="message-circle",
                                                                on_select=ctx.callback(_select_item, item="Message"),
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            DropdownMenuSeparator(),
                                            DropdownMenuItem(
                                                "Log out",
                                                icon="log-out",
                                                shortcut="⇧⌘Q",
                                                on_select=ctx.callback(_select_item, item="Log out"),
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            Text(
                                f"Last action: {last_action}",
                                class_name="text-sm text-muted-foreground",
                            ),
                        ],
                    ),
                    Markdown(
                        content=(
                            "```python\n"
                            "DropdownMenu(\n"
                            "    children=[\n"
                            '        DropdownMenuTrigger(Button("Open Menu")),\n'
                            "        DropdownMenuContent(\n"
                            '            DropdownMenuLabel("My Account"),\n'
                            "            DropdownMenuSeparator(),\n"
                            '            DropdownMenuItem("Profile", icon="user", shortcut="⇧⌘P",\n'
                            "                            on_select=ctx.callback(handle_select)),\n"
                            "            ...\n"
                            "        ),\n"
                            "    ]\n"
                            ")\n"
                            "```"
                        )
                    ),
                ]
            ),
        ]
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the DropdownMenu component reference page."""
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
A floating menu triggered by a button click. Supports labels, separators, icons,
keyboard shortcuts, checkbox items, radio groups, and nested submenus.

```python
from refast.components.shadcn.overlay import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent,
    DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator,
)
from refast.components import Button

DropdownMenu(
    children=[
        DropdownMenuTrigger(Button("Options")),
        DropdownMenuContent(
            DropdownMenuLabel("Actions"),
            DropdownMenuSeparator(),
            DropdownMenuItem("Edit", icon="edit", on_select=ctx.callback(handle_edit)),
            DropdownMenuItem("Delete", icon="trash", on_select=ctx.callback(handle_delete)),
        ),
    ]
)
```
"""

REFERENCE = """
## Component Reference

### DropdownMenu

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `bool \\| None` | `None` | Controlled open state |
| `default_open` | `bool` | `False` | Initial open state (uncontrolled) |
| `on_open_change` | `Callback \\| None` | `None` | Called when open state changes |
| `children` | `list` | *(required)* | Must contain `DropdownMenuTrigger` and `DropdownMenuContent` |

### DropdownMenuContent

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"top" \\| "right" \\| "bottom" \\| "left"` | `"bottom"` | Which side to open toward |
| `side_offset` | `int` | `4` | Pixel gap from the trigger |
| `align` | `"start" \\| "center" \\| "end"` | `"start"` | Alignment relative to trigger |

### DropdownMenuItem

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Item text |
| `icon` | `str \\| None` | `None` | Lucide icon name |
| `shortcut` | `str \\| None` | `None` | Keyboard shortcut hint (display only) |
| `disabled` | `bool` | `False` | Greys out and prevents selection |
| `on_select` | `Callback \\| None` | `None` | Called when item is selected |

### DropdownMenuLabel

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Section header text |
| `inset` | `bool` | `False` | Indent to align with items that have icons |

### DropdownMenuCheckboxItem

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Item text |
| `checked` | `bool` | `False` | Whether the checkbox is checked |
| `disabled` | `bool` | `False` | Prevents interaction |
| `on_checked_change` | `Callback \\| None` | `None` | Called with new `bool` value |

### DropdownMenuRadioGroup + DropdownMenuRadioItem

```python
DropdownMenuRadioGroup(
    value="bottom",
    on_value_change=ctx.callback(handle_position),
    children=[
        DropdownMenuRadioItem("Top", value="top"),
        DropdownMenuRadioItem("Bottom", value="bottom"),
        DropdownMenuRadioItem("Right", value="right"),
    ],
)
```

| Prop (RadioGroup) | Type | Default | Description |
|---|---|---|---|
| `value` | `str` | `""` | Currently selected value |
| `on_value_change` | `Callback \\| None` | `None` | Called with new selected value |

| Prop (RadioItem) | Type | Default | Description |
|---|---|---|---|
| `label` | `str` | *(required)* | Item text |
| `value` | `str` | `""` | Value emitted when selected |

### DropdownMenuSub (Submenu)

```python
DropdownMenuSub(
    children=[
        DropdownMenuSubTrigger("Share", icon="share"),
        DropdownMenuSubContent(
            children=[
                DropdownMenuItem("Email", icon="mail", on_select=ctx.callback(share_email)),
                DropdownMenuItem("Link", icon="link", on_select=ctx.callback(share_link)),
            ]
        ),
    ]
)
```

| Prop (SubTrigger) | Type | Default | Description |
|---|---|---|---|
| `label` | `str` | *(required)* | Trigger label |
| `icon` | `str \\| None` | `None` | Lucide icon |
| `inset` | `bool` | `False` | Align with icon-bearing items |
"""
