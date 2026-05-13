"""Sheet — /docs/components/sheet."""

from refast import Context
from refast.components import (
    Button,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Sheet,
    SheetContent,
    SheetDescription,
    SheetFooter,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
    Text,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Sheet"
PAGE_ROUTE = "/docs/components/sheet"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_side(ctx: Context, value: str):
    ctx.state.set("sht_side", value)
    await ctx.refresh()


async def _open_sheet(ctx: Context):
    ctx.state.set("sht_open", True)
    await ctx.refresh()


async def _close_sheet(ctx: Context):
    ctx.state.set("sht_open", False)
    await ctx.refresh()


async def _set_sheet_open(ctx: Context, value: bool):
    ctx.state.set("sht_open", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    side = ctx.state.get("sht_side", "right")
    open_state = ctx.state.get("sht_open", False)

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Side", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["top", "right", "bottom", "left"]
                        ],
                        value=side,
                        on_change=ctx.callback(_set_side),
                    ),
                ],
            ),
        ],
        preview=[
            Sheet(
                open=open_state,
                on_open_change=ctx.callback(_set_sheet_open),
                children=[
                    SheetTrigger(
                        children=[
                            Button(
                                f"Open ({side})",
                                on_click=ctx.callback(_open_sheet),
                            )
                        ]
                    ),
                    SheetContent(
                        side=side,
                        children=[
                            SheetHeader(
                                children=[
                                    SheetTitle(title="Edit Profile"),
                                    SheetDescription(
                                        description="Make changes to your profile here. "
                                        "Click save when done."
                                    ),
                                ]
                            ),
                            Text(
                                "Profile form fields would go here.",
                                class_name="text-sm text-muted-foreground py-4",
                            ),
                            SheetFooter(
                                children=[
                                    Button(
                                        "Save changes",
                                        on_click=ctx.callback(_close_sheet),
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        ],
        code=Markdown(
            content=(
                f"```python\n"
                f"Sheet(\n"
                f"    children=[\n"
                f"        SheetTrigger(children=[Button(\"Open\")]),\n"
                f"        SheetContent(\n"
                f'            side="{side}",\n'
                f"            children=[\n"
                f"                SheetHeader(\n"
                f"                    children=[\n"
                f'                        SheetTitle(title="Edit Profile"),\n'
                f'                        SheetDescription(description="Make changes here."),\n'
                f"                    ]\n"
                f"                ),\n"
                f"                # content\n"
                f"                SheetFooter(children=[Button(\"Save\")]),\n"
                f"            ],\n"
                f"        ),\n"
                f"    ]\n"
                f")\n"
                f"```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30 flex items-center justify-center min-h-[80px]",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Sheet component reference page."""
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
A panel that slides in from an edge of the screen. Useful for side menus,
detail panels, and quick-edit forms without navigating away.

```python
from refast.components import (
    Sheet, SheetTrigger, SheetContent, SheetHeader,
    SheetTitle, SheetDescription, SheetFooter, SheetClose,
)
```
"""

REFERENCE = """
## Props

### `Sheet`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `bool \\| None` | `None` | Controlled open state |
| `default_open` | `bool` | `False` | Initial open state |
| `on_open_change` | `Callback \\| None` | `None` | Called when open state changes |

### `SheetContent`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `side` | `"top" \\| "right" \\| "bottom" \\| "left"` | `"right"` | Slide-in edge |
| `children` | `ChildrenType` | `None` | Panel content |

### `SheetTitle`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `str` | *(required)* | Panel heading |

### `SheetDescription`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `description` | `str` | *(required)* | Supporting text |

## Component Hierarchy

```
Sheet
├── SheetTrigger       ← button that opens the panel
└── SheetContent (side="right")
    ├── SheetHeader
    │   ├── SheetTitle
    │   └── SheetDescription
    ├── (custom form / content)
    └── SheetFooter
        └── SheetClose  ← or any Button with on_click=close
```

## Controlled Sheet

```python
async def open_panel(ctx: Context):
    ctx.state.set("panel_open", True)
    await ctx.refresh()

async def close_panel(ctx: Context):
    ctx.state.set("panel_open", False)
    await ctx.refresh()

# In render:
open_state = ctx.state.get("panel_open", False)

Sheet(
    open=open_state,
    on_open_change=ctx.callback(close_panel),
    children=[
        SheetContent(
            side="left",
            children=[
                SheetHeader(children=[SheetTitle(title="Filters")]),
                # filter controls
                SheetFooter(children=[Button("Apply", on_click=ctx.callback(close_panel))]),
            ]
        )
    ]
)
```
"""
