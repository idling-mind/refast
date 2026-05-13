"""Breadcrumb — /docs/components/breadcrumb."""

from refast import Context
from docs_site.pages.components.playground import playground_card
from refast.components import (
    Breadcrumb,
    BreadcrumbEllipsis,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Breadcrumb"
PAGE_ROUTE = "/docs/components/breadcrumb"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_item_count(ctx: Context, value: str):
    ctx.state.set("brd_item_count", int(value))
    await ctx.refresh()


async def _set_show_ellipsis(ctx: Context, value: bool):
    ctx.state.set("brd_show_ellipsis", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    item_count = ctx.state.get("brd_item_count", 3)
    show_ellipsis = ctx.state.get("brd_show_ellipsis", False)

    all_crumbs = [
        ("Home", "/"),
        ("Docs", "/docs"),
        ("Components", "/docs/components"),
        ("Navigation", "/docs/components/navigation"),
        ("Breadcrumb", "/docs/components/breadcrumb"),
    ]
    selected = all_crumbs[:item_count]

    # Build breadcrumb items
    items = []
    if show_ellipsis and item_count >= 4:
        # Show first, ellipsis, then last two
        items.append(BreadcrumbItem(children=[BreadcrumbLink(selected[0][0], href=selected[0][1])]))
        items.append(BreadcrumbSeparator())
        items.append(BreadcrumbItem(children=[BreadcrumbEllipsis()]))
        for label, href in selected[-2:-1]:
            items.append(BreadcrumbSeparator())
            items.append(BreadcrumbItem(children=[BreadcrumbLink(label, href=href)]))
        items.append(BreadcrumbSeparator())
        last_label, _ = selected[-1]
        items.append(BreadcrumbItem(children=[BreadcrumbPage(last_label)]))
    else:
        for i, (label, href) in enumerate(selected):
            if i > 0:
                items.append(BreadcrumbSeparator())
            if i < len(selected) - 1:
                items.append(BreadcrumbItem(children=[BreadcrumbLink(label, href=href)]))
            else:
                items.append(BreadcrumbItem(children=[BreadcrumbPage(label)]))

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Number of items", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": str(n), "label": str(n)}
                            for n in [2, 3, 4, 5]
                        ],
                        value=str(item_count),
                        on_change=ctx.callback(_set_item_count),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Show ellipsis", class_name="text-sm font-medium"),
                    Checkbox(
                        label="collapse middle items",
                        checked=show_ellipsis,
                        on_change=ctx.callback(_set_show_ellipsis),
                    ),
                ],
            ),
        ],
        preview=[
            Breadcrumb(children=[BreadcrumbList(children=items)]),
        ],
        code=Markdown(
            content=(
                "```python\n"
                "Breadcrumb(\n"
                "    children=[\n"
                "        BreadcrumbList(\n"
                "            children=[\n"
                "                BreadcrumbItem(children=[BreadcrumbLink(\"Home\", href=\"/\")]),\n"
                "                BreadcrumbSeparator(),\n"
                "                BreadcrumbItem(children=[BreadcrumbLink(\"Docs\", href=\"/docs\")]),\n"
                "                BreadcrumbSeparator(),\n"
                "                BreadcrumbItem(children=[BreadcrumbPage(\"Components\")]),\n"
                "            ]\n"
                "        )\n"
                "    ]\n"
                ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Breadcrumb component reference page."""
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
A navigation trail showing the current page location in a hierarchy.

```python
from refast.components import (
    Breadcrumb, BreadcrumbList, BreadcrumbItem,
    BreadcrumbLink, BreadcrumbPage, BreadcrumbSeparator, BreadcrumbEllipsis,
)
```
"""

REFERENCE = """
## Props

### `Breadcrumb`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ChildrenType` | `None` | `BreadcrumbList` child |
| `separator` | `str \\| None` | `None` | Custom separator character |
| `class_name` | `str` | `""` | Extra Tailwind classes |

### `BreadcrumbLink`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Link text |
| `href` | `str` | `"#"` | Navigation URL |
| `current` | `bool` | `False` | Mark as current location |
| `on_click` | `Callback \\| None` | `None` | Click callback (alternative to href) |

### `BreadcrumbPage`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Text for the current (non-clickable) page |

## Component Hierarchy

```
Breadcrumb
└── BreadcrumbList
    ├── BreadcrumbItem
    │   └── BreadcrumbLink  ← clickable crumb
    ├── BreadcrumbSeparator
    ├── BreadcrumbItem
    │   └── BreadcrumbEllipsis  ← collapsed indicator
    ├── BreadcrumbSeparator
    └── BreadcrumbItem
        └── BreadcrumbPage  ← current page (non-clickable)
```

## With Ellipsis

```python
Breadcrumb(
    children=[
        BreadcrumbList(
            children=[
                BreadcrumbItem(children=[BreadcrumbLink("Home", href="/")]),
                BreadcrumbSeparator(),
                BreadcrumbItem(children=[BreadcrumbEllipsis()]),
                BreadcrumbSeparator(),
                BreadcrumbItem(children=[BreadcrumbLink("Components", href="/docs/components")]),
                BreadcrumbSeparator(),
                BreadcrumbItem(children=[BreadcrumbPage("Breadcrumb")]),
            ]
        )
    ]
)
```

## With Custom Separator

```python
Breadcrumb(separator=">")
```
"""
