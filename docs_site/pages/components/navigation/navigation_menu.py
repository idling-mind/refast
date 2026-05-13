"""NavigationMenu — /docs/components/navigation-menu."""

from refast import Context
from docs_site.pages.components.playground import playground_card
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Navigation Menu"
PAGE_ROUTE = "/docs/components/navigation-menu"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_orientation(ctx: Context, value: str):
    ctx.state.set("nm_orientation", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    orientation = ctx.state.get("nm_orientation", "horizontal")

    nav = NavigationMenu(
        orientation=orientation,
        children=[
            NavigationMenuList(
                children=[
                    NavigationMenuItem(
                        children=[
                            NavigationMenuTrigger("Getting Started"),
                            NavigationMenuContent(
                                class_name="p-4 w-48",
                                children=[
                                    Column(
                                        gap=1,
                                        children=[
                                            NavigationMenuLink(
                                                "Installation",
                                                href="#",
                                                class_name="text-sm",
                                            ),
                                            NavigationMenuLink(
                                                "Quick Tour",
                                                href="#",
                                                class_name="text-sm",
                                            ),
                                            NavigationMenuLink(
                                                "Architecture",
                                                href="#",
                                                class_name="text-sm",
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ]
                    ),
                    NavigationMenuItem(
                        children=[
                            NavigationMenuTrigger("Components"),
                            NavigationMenuContent(
                                class_name="p-4 w-48",
                                children=[
                                    Column(
                                        gap=1,
                                        children=[
                                            NavigationMenuLink(
                                                "Button",
                                                href="#",
                                                class_name="text-sm",
                                            ),
                                            NavigationMenuLink(
                                                "Input",
                                                href="#",
                                                class_name="text-sm",
                                            ),
                                            NavigationMenuLink(
                                                "Card",
                                                href="#",
                                                class_name="text-sm",
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ]
                    ),
                    NavigationMenuItem(
                        children=[
                            NavigationMenuLink(
                                "GitHub",
                                href="https://github.com",
                                class_name="font-medium",
                            )
                        ]
                    ),
                ]
            )
        ],
    )

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Orientation", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["horizontal", "vertical"]
                        ],
                        value=orientation,
                        on_change=ctx.callback(_set_orientation),
                    ),
                ],
            ),
        ],
        preview=[nav],
        code=Markdown(
            content=(
                f"```python\n"
                f"NavigationMenu(\n"
                f'    orientation="{orientation}",\n'
                f"    children=[\n"
                f"        NavigationMenuList(\n"
                f"            children=[\n"
                f"                NavigationMenuItem(\n"
                f"                    children=[\n"
                f'                        NavigationMenuTrigger("Getting Started"),\n'
                f"                        NavigationMenuContent(\n"
                f"                            children=[...],\n"
                f"                        ),\n"
                f"                    ]\n"
                f"                ),\n"
                f"            ]\n"
                f"        )\n"
                f"    ]\n"
                f")\n"
                f"```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30 min-h-[80px]",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the NavigationMenu component reference page."""
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
A horizontal (or vertical) navigation bar with dropdown content panels.
Follows WAI-ARIA patterns for accessible navigation menus.

```python
from refast.components import (
    NavigationMenu, NavigationMenuList, NavigationMenuItem,
    NavigationMenuTrigger, NavigationMenuContent, NavigationMenuLink,
)
```
"""

REFERENCE = """
## Props

### `NavigationMenu`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `"horizontal" \\| "vertical"` | `"horizontal"` | Menu axis |
| `children` | `ChildrenType` | `None` | `NavigationMenuList` children |

### `NavigationMenuLink`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Link text |
| `href` | `str` | `"#"` | Navigation URL |
| `active` | `bool` | `False` | Mark as current page |
| `on_click` | `Callback \\| None` | `None` | Click callback |

## Component Hierarchy

```
NavigationMenu
└── NavigationMenuList
    ├── NavigationMenuItem
    │   ├── NavigationMenuTrigger  ← opens dropdown
    │   └── NavigationMenuContent  ← dropdown panel
    └── NavigationMenuItem
        └── NavigationMenuLink    ← simple link (no dropdown)
```

## Example — Link-Only Item

```python
NavigationMenuItem(
    children=[
        NavigationMenuLink("About", href="/about")
    ]
)
```

## Example — With Dropdown Panel

```python
NavigationMenuItem(
    children=[
        NavigationMenuTrigger("Products"),
        NavigationMenuContent(
            class_name="p-4 w-64",
            children=[
                NavigationMenuLink("Analytics", href="/products/analytics"),
                NavigationMenuLink("Automation", href="/products/automation"),
            ]
        ),
    ]
)
```
"""
