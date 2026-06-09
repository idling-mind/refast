"""Toggle — /docs/components/toggle.

Interactive reference page for the Toggle and ToggleGroup components.
"""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Select,
    Separator,
    Text,
)
from refast.components.shadcn.controls import Toggle, ToggleGroup, ToggleGroupItem

PAGE_TITLE = "Toggle"
PAGE_ROUTE = "/docs/components/toggle"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_variant(ctx: Context, value: str):
    ctx.state.set("tgl_variant", value)
    await ctx.refresh()


async def _set_size(ctx: Context, value: str):
    ctx.state.set("tgl_size", value)
    await ctx.refresh()


async def _set_pressed(ctx: Context, value: bool):
    ctx.state.set("tgl_pressed", value)
    await ctx.refresh()


async def _toggle_pressed(ctx: Context, value: bool):
    ctx.state.set("tgl_pressed", value)
    await ctx.refresh()


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("tgl_disabled", value)
    await ctx.refresh()


async def _set_group_mode(ctx: Context, value: str):
    ctx.state.set("tgl_group_mode", value)
    ctx.state.set("tgl_group_value", [])
    await ctx.refresh()


async def _group_change(ctx: Context):
    event = ctx.event_data
    group_mode = ctx.state.get("tgl_group_mode", "single")
    if group_mode == "multiple":
        # multiple mode sends {item_value: bool, ...} — no "value" key
        ctx.state.set("tgl_group_value", event)
    else:
        ctx.state.set("tgl_group_value", event.get("value", ""))
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    variant = ctx.state.get("tgl_variant", "default")
    size = ctx.state.get("tgl_size", "md")
    pressed = ctx.state.get("tgl_pressed", False)
    disabled = ctx.state.get("tgl_disabled", False)
    group_mode = ctx.state.get("tgl_group_mode", "single")
    group_value = ctx.state.get("tgl_group_value", [])

    pressed_label = "Pressed" if pressed else "Unpressed"

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Variant", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["default", "outline"]
                        ],
                        value=variant,
                        on_change=ctx.callback(_set_variant),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Size", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["sm", "md", "lg"]
                        ],
                        value=size,
                        on_change=ctx.callback(_set_size),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Disabled", class_name="text-sm font-medium"),
                    Checkbox(
                        label="disabled",
                        checked=disabled,
                        on_change=ctx.callback(_set_disabled),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("ToggleGroup Mode", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "single", "label": "single"},
                            {"value": "multiple", "label": "multiple"},
                        ],
                        value=group_mode,
                        on_change=ctx.callback(_set_group_mode),
                    ),
                ],
            ),
        ],
        preview=[
            Text("Toggle", class_name="text-base font-semibold mb-2"),
            Container(
                class_name="border rounded-lg p-6 flex items-center gap-4 min-h-[80px] bg-muted/30",
                children=[
                    Toggle(
                        label="Bold",
                        icon="bold",
                        variant=variant,
                        size=size,
                        disabled=disabled,
                        pressed=pressed,
                        on_pressed_change=ctx.callback(_toggle_pressed),
                    ),
                    Text(
                        f"State: {pressed_label}",
                        class_name="text-sm text-muted-foreground",
                    ),
                ],
            ),
            Markdown(
                content=(
                    f"```python\n"
                    f"Toggle(\n"
                    f'    label="Bold",\n'
                    f'    icon="bold",\n'
                    f'    variant="{variant}",\n'
                    f'    size="{size}",\n'
                    f'    disabled={disabled},\n'
                    f'    pressed={pressed},\n'
                    f"    on_pressed_change=ctx.callback(handle_toggle),\n"
                    f")\n"
                    f"```"
                )
            ),
            Separator(class_name="my-6"),
            Text("ToggleGroup", class_name="text-base font-semibold mb-2"),
            Container(
                class_name="border rounded-lg p-6 flex items-center gap-4 min-h-[80px] bg-muted/30",
                children=[
                    ToggleGroup(
                        type=group_mode,
                        on_value_change=ctx.callback(_group_change),
                        children=[
                            ToggleGroupItem("Bold", icon="bold", value="bold"),
                            ToggleGroupItem("Italic", icon="italic", value="italic"),
                            ToggleGroupItem(
                                "Underline", icon="underline", value="underline"
                            ),
                        ],
                    ),
                    Text(
                        f"Selected: {group_value}",
                        class_name="text-sm text-muted-foreground",
                    ),
                ],
            ),
            Markdown(
                content=(
                    f"```python\n"
                    f'ToggleGroup(\n'
                    f'    type="{group_mode}",\n'
                    f"    on_value_change=ctx.callback(handle_change),\n"
                    f"    children=[\n"
                    f'        ToggleGroupItem("Bold", icon="bold", value="bold"),\n'
                    f'        ToggleGroupItem("Italic", icon="italic", value="italic"),\n'
                    f'        ToggleGroupItem("Underline", icon="underline", value="underline"),\n'
                    f"    ],\n"
                    f")\n"
                    f"```"
                )
            ),
        ],
        preview_class="",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Toggle component reference page."""
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
Two-state buttons that can be toggled on or off. `Toggle` is a single button;
`ToggleGroup` groups multiple toggles with single or multiple selection modes.

```python
from refast.components.shadcn.controls import Toggle, ToggleGroup, ToggleGroupItem

# Single toggle
Toggle("Bold", icon="bold", pressed=True, on_pressed_change=ctx.callback(handle_toggle))

# ToggleGroup — single selection
ToggleGroup(
    type="single",
    children=[
        ToggleGroupItem("Left", icon="align-left", value="left"),
        ToggleGroupItem("Center", icon="align-center", value="center"),
        ToggleGroupItem("Right", icon="align-right", value="right"),
    ],
    on_value_change=ctx.callback(handle_alignment),
)
```
"""

REFERENCE = """
## Toggle Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | `""` | Button text label |
| `icon` | `str \\| None` | `None` | Lucide icon name |
| `pressed` | `bool \\| None` | `None` | Controlled pressed state |
| `default_pressed` | `bool` | `False` | Initial pressed state (uncontrolled) |
| `disabled` | `bool` | `False` | Prevents interaction |
| `variant` | `"default" \\| "outline"` | `"default"` | Visual style |
| `size` | `"sm" \\| "md" \\| "lg"` | `"md"` | Button size |
| `on_pressed_change` | `Callback \\| None` | `None` | Called with new pressed state |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## ToggleGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `"single" \\| "multiple"` | `"single"` | Selection mode |
| `value` | `str \\| list[str] \\| dict[str, bool] \\| None` | `None` | Controlled value |
| `default_value` | `str \\| list[str] \\| dict[str, bool] \\| None` | `None` | Initial value (uncontrolled) |
| `disabled` | `bool` | `False` | Disables all items |
| `variant` | `"default" \\| "outline"` | `"default"` | Visual style applied to all items |
| `size` | `"sm" \\| "md" \\| "lg"` | `"md"` | Size applied to all items |
| `on_value_change` | `Callback \\| None` | `None` | Called with the new value |
| `children` | `list` | *(required)* | `ToggleGroupItem` components |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## ToggleGroupItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | `""` | Item text |
| `icon` | `str \\| None` | `None` | Lucide icon name |
| `value` | `str \\| None` | `None` | Unique value for this item |
| `name` | `str \\| None` | `None` | Alternative identifier |
| `disabled` | `bool` | `False` | Disables this specific item |

## Examples

```python
# Icon-only toolbar (alignment)
ToggleGroup(
    type="single",
    default_value="left",
    children=[
        ToggleGroupItem(icon="align-left", value="left"),
        ToggleGroupItem(icon="align-center", value="center"),
        ToggleGroupItem(icon="align-right", value="right"),
        ToggleGroupItem(icon="align-justify", value="justify"),
    ],
)

# Multiple selection (text formatting)
ToggleGroup(
    type="multiple",
    children=[
        ToggleGroupItem("B", icon="bold", value="bold"),
        ToggleGroupItem("I", icon="italic", value="italic"),
        ToggleGroupItem("U", icon="underline", value="underline"),
    ],
    on_value_change=ctx.callback(handle_format),
)

# Outline variant
Toggle("Mute", icon="volume-x", variant="outline", on_pressed_change=ctx.callback(handle_mute))
```
"""
