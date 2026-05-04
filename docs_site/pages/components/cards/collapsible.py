"""Collapsible — /docs/components/collapsible.

Interactive reference page for the Collapsible component family.
"""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Separator,
    Text,
)

PAGE_TITLE = "Collapsible"
PAGE_ROUTE = "/docs/components/collapsible"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _toggle_open(ctx: Context, value: bool):
    ctx.state.set("cll_open", value)
    await ctx.refresh()


async def _set_disabled(ctx: Context, value: bool):
    ctx.state.set("cll_disabled", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    is_open = ctx.state.get("cll_open", False)
    disabled = ctx.state.get("cll_disabled", False)

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    Row(
                        gap=4,
                        wrap=True,
                        class_name="mb-6",
                        children=[
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
                        ],
                    ),
                    # Live preview — controlled via on_open_change
                    Container(
                        class_name="border rounded-lg p-6 bg-muted/30",
                        children=[
                            Text(
                                "Click the button to toggle (Python manages open state via on_open_change):",
                                class_name="text-sm text-muted-foreground mb-3",
                            ),
                            Collapsible(
                                open=is_open,
                                disabled=disabled,
                                on_open_change=ctx.callback(_toggle_open),
                                children=[
                                    CollapsibleTrigger(
                                        as_child=False,
                                        class_name="flex items-center gap-2 rounded-md border px-4 py-2 text-sm font-medium hover:bg-accent cursor-pointer",
                                        children=[
                                            Text("Toggle section \u2195"),
                                        ],
                                    ),
                                    CollapsibleContent(
                                        children=[
                                            Container(
                                                class_name="mt-3 p-3 border rounded bg-background",
                                                children=[
                                                    Text(
                                                        "This content is revealed when the collapsible is open.",
                                                        class_name="text-sm",
                                                    ),
                                                    Text(
                                                        "You can put any components here.",
                                                        class_name="text-sm text-muted-foreground",
                                                    ),
                                                ],
                                            )
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Markdown(
                        content=(
                            "```python\n"
                            "Collapsible(\n"
                            f"    open={is_open},\n"
                            f"    disabled={disabled},\n"
                            "    children=[\n"
                            "        CollapsibleTrigger(\n"
                            "            children=[Button(\"Toggle section\", on_click=ctx.callback(toggle))]\n"
                            "        ),\n"
                            "        CollapsibleContent(\n"
                            "            children=[Text(\"Hidden content\")]\n"
                            "        ),\n"
                            "    ],\n"
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
    """Render the Collapsible component reference page."""
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
An expandable section that reveals or hides content. Supports both
**uncontrolled** (browser manages state) and **controlled** (Python manages
state via a callback) usage.

```python
from refast.components import Collapsible, CollapsibleTrigger, CollapsibleContent

# Uncontrolled — browser manages open state
Collapsible(
    default_open=False,
    children=[
        CollapsibleTrigger(children=[Button("Show details")]),
        CollapsibleContent(children=[Text("The details are here.")]),
    ],
)
```
"""

REFERENCE = """
## Collapsible Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `bool \\| None` | `None` | Controlled open state. Omit for uncontrolled. |
| `default_open` | `bool` | `False` | Initial open state (uncontrolled only). |
| `on_open_change` | `Callback \\| None` | `None` | Fired when the open state changes. |
| `disabled` | `bool` | `False` | Prevents toggling. |
| `children` | `list` | `[]` | A `CollapsibleTrigger` and a `CollapsibleContent`. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## CollapsibleTrigger Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | The element that triggers open/close. |
| `as_child` | `bool` | `True` | Merges props onto the child element (Radix `asChild`). |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## CollapsibleContent Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Content revealed when open. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## Uncontrolled usage

```python
# Browser manages state — no server round-trip needed
Collapsible(
    default_open=True,
    children=[
        CollapsibleTrigger(children=[Button("Toggle")]),
        CollapsibleContent(children=[Text("Expanded by default.")]),
    ],
)
```

## Controlled usage

```python
async def toggle(ctx: Context):
    current = ctx.state.get("is_open", False)
    ctx.state.set("is_open", not current)
    await ctx.refresh()

def render(ctx: Context):
    is_open = ctx.state.get("is_open", False)
    return Collapsible(
        open=is_open,
        children=[
            CollapsibleTrigger(
                children=[Button("Toggle", on_click=ctx.callback(toggle))]
            ),
            CollapsibleContent(children=[Text("Controlled content.")]),
        ],
    )
```

## on_open_change callback

```python
async def on_open_change(ctx: Context):
    # ctx.event_data is the new boolean open state
    ctx.state.set("is_open", ctx.event_data)
    await ctx.refresh()

Collapsible(
    open=is_open,
    on_open_change=ctx.callback(on_open_change),
    children=[
        CollapsibleTrigger(children=[Button("Toggle")]),
        CollapsibleContent(children=[Text("Content.")]),
    ],
)
```
"""
