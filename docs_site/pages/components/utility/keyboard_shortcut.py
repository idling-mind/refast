"""KeyboardShortcut — /docs/components/keyboard-shortcut."""

from refast import Context
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Input,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)
from refast.components.shadcn import KeyboardShortcut

PAGE_TITLE = "KeyboardShortcut"
PAGE_ROUTE = "/docs/components/keyboard-shortcut"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _shortcut_fired(ctx: Context, label: str = ""):
    ctx.state.set("last_shortcut", label)
    await ctx.update_text("ks-last-fired", f'Last fired: "{label}"')
    await ctx.show_toast(f'Shortcut "{label}" triggered', variant="success")


async def _toggle_enabled(ctx: Context):
    current = ctx.state.get("ks_enabled", True)
    ctx.state.set("ks_enabled", not current)
    await ctx.refresh()


async def _toggle_bubble(ctx: Context):
    current = ctx.state.get("ks_bubble", False)
    ctx.state.set("ks_bubble", not current)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    enabled = ctx.state.get("ks_enabled", True)
    bubble = ctx.state.get("ks_bubble", False)
    last = ctx.state.get("last_shortcut", "—")

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    Column(
                        gap=6,
                        children=[
                            # Controls row
                            Row(
                                gap=4,
                                wrap=True,
                                children=[
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                label="Enabled",
                                                checked=enabled,
                                                on_change=ctx.callback(_toggle_enabled),
                                            ),
                                        ],
                                    ),
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                label="Bubble (allow multiple handlers)",
                                                checked=bubble,
                                                on_change=ctx.callback(_toggle_bubble),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            # Active shortcuts legend
                            Container(
                                class_name="border rounded-lg p-4 bg-muted/30",
                                children=[
                                    Column(
                                        gap=3,
                                        children=[
                                            Text(
                                                "Registered shortcuts on this page:",
                                                class_name="text-sm font-medium",
                                            ),
                                            Row(
                                                gap=2,
                                                wrap=True,
                                                children=[
                                                    Row(
                                                        gap=2,
                                                        align="center",
                                                        children=[
                                                            Badge(children="Ctrl + Alt + 1", variant="outline"),
                                                            Text("→ fires 'Ctrl+Alt+1'", class_name="text-sm text-muted-foreground"),
                                                        ],
                                                    ),
                                                    Row(
                                                        gap=2,
                                                        align="center",
                                                        children=[
                                                            Badge(children="Ctrl + Alt + 2", variant="outline"),
                                                            Text("→ fires 'Ctrl+Alt+2'", class_name="text-sm text-muted-foreground"),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            Text(
                                                f'Last fired: "{last}"',
                                                id="ks-last-fired",
                                                class_name="text-sm font-mono text-primary mt-1",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            # The invisible shortcut component
                            KeyboardShortcut(
                                shortcuts={
                                    "ctrl+alt+1": ctx.callback(_shortcut_fired, label="Ctrl+Alt+1"),
                                    "ctrl+alt+2": ctx.callback(_shortcut_fired, label="Ctrl+Alt+2"),
                                },
                                priority=10,
                                bubble=bubble,
                                enabled=enabled,
                            ),
                            Markdown(
                                content=(
                                    "```python\n"
                                    "KeyboardShortcut(\n"
                                    "    shortcuts={\n"
                                    '        "ctrl+alt+1": ctx.callback(handle_shortcut),\n'
                                    '        "ctrl+alt+2": ctx.callback(handle_shortcut),\n'
                                    "    },\n"
                                    f"    enabled={enabled},\n"
                                    f"    bubble={bubble},\n"
                                    ")\n"
                                    "```"
                                )
                            ),
                        ],
                    )
                ]
            ),
        ]
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the KeyboardShortcut component reference page."""
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
An invisible component that captures keyboard shortcuts globally and fires
server callbacks.  It renders nothing to the DOM — place it anywhere in the
component tree and it will listen on the `document` for the registered key
combinations.

```python
from refast.components import KeyboardShortcut

KeyboardShortcut(
    shortcuts={
        "ctrl+k": ctx.callback(open_search),
        "ctrl+shift+n": ctx.callback(new_item),
        "escape": ctx.callback(close_panel),
    }
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `shortcuts` | `dict[str, Callback]` | **required** | Mapping of shortcut string → server callback |
| `priority` | `int` | `0` | Higher values are handled first when multiple components claim the same combo |
| `bubble` | `bool` | `False` | When `True`, propagation continues to lower-priority handlers after this one fires |
| `prevent_default` | `bool` | `True` | Suppress the browser's native action for the combo (e.g. prevents Ctrl+S from opening the save dialog) |
| `enabled` | `bool` | `True` | Disable the shortcuts without removing the component from the tree |
| `id` | `str \\| None` | `None` | Unique element ID |

## Shortcut format

Shortcut strings use the form `"modifier+modifier+key"`.  Modifiers are
case-insensitive and can appear in any order:

| Modifier token | Aliases |
|----------------|---------|
| `ctrl` | `control` |
| `shift` | — |
| `alt` | — |
| `meta` | `cmd`, `command`, `win` |

The key should be a single character (`a`–`z`, `0`–`9`) or a named key
(`enter`, `escape`, `space`, `arrowup`, `arrowdown`, `arrowleft`, `arrowright`, `tab`, `f1`–`f12`, …).

```python
# Examples
"ctrl+k"
"ctrl+shift+n"
"alt+f4"
"meta+k"          # ⌘K on macOS
"escape"
"f5"
```

## Multiple shortcuts in one component

All shortcuts in a single `KeyboardShortcut` share the same `priority`,
`bubble`, and `enabled` settings.  If you need different settings per
shortcut, use multiple components:

```python
# High-priority, no bubbling — captures Ctrl+K exclusively
KeyboardShortcut(
    shortcuts={"ctrl+k": ctx.callback(open_search)},
    priority=10,
    bubble=False,
)

# Lower priority — only fires if no higher-priority handler claims the combo
KeyboardShortcut(
    shortcuts={"ctrl+k": ctx.callback(log_search_attempt)},
    priority=0,
    bubble=False,
)
```

## Priority & bubbling

When two or more `KeyboardShortcut` components register the same combo:

1. Handlers run in **descending priority** order (highest first).
2. After a handler fires, propagation **stops** unless `bubble=True` on
   that component.
3. If `bubble=True`, the next handler in priority order also runs.

```python
# Both handlers fire for Ctrl+Z because the first sets bubble=True
KeyboardShortcut(
    shortcuts={"ctrl+z": ctx.callback(analytics_undo_track)},
    priority=20,
    bubble=True,   # keep going after this
)
KeyboardShortcut(
    shortcuts={"ctrl+z": ctx.callback(do_undo)},
    priority=10,
    bubble=False,
)
```

## Input field guard

Shortcuts that have **no** `Ctrl`, `Alt`, or `Meta` modifier are silently
ignored while a text `<input>`, `<textarea>`, or `contenteditable` element is
focused — so normal typing is never intercepted.

Shortcuts *with* a global modifier (Ctrl, Alt, Meta) fire regardless of focus.

## Dynamic enable / disable

Toggle shortcuts at runtime without unmounting the component:

```python
KeyboardShortcut(
    shortcuts={"ctrl+s": ctx.callback(save)},
    enabled=ctx.state.get("editing", False),
)
```
"""
