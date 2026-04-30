"""List — /docs/components/list.

Interactive reference page for the List and ListItem components.
"""

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
    List,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "List"
PAGE_ROUTE = "/docs/components/list"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_ordered(ctx: Context, value: bool):
    ctx.state.set("lst_ordered", value)
    await ctx.refresh()


async def _set_style(ctx: Context, value: str):
    ctx.state.set("lst_style", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────

_ITEMS = [
    "First item in the list",
    "Second item with more detail",
    "Third item — nested content supported",
    "Fourth item",
    "Fifth item",
]


def _playground(ctx: Context):
    ordered = ctx.state.get("lst_ordered", False)
    style = ctx.state.get("lst_style", "plain")

    if style == "badges":
        items = [
            Row(
                align="center",
                gap=2,
                children=[
                    Badge(children=[str(i + 1)], variant="secondary"),
                    Text(item, class_name="text-sm"),
                ],
            )
            for i, item in enumerate(_ITEMS[:4])
        ]
        list_children = items
    else:
        list_children = _ITEMS[:4]

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
                                    Text("Ordered", class_name="text-sm font-medium"),
                                    Checkbox(
                                        label="numbered list",
                                        checked=ordered,
                                        on_change=ctx.callback(_set_ordered),
                                    ),
                                ],
                            ),
                            Column(
                                gap=1,
                                children=[
                                    Text("Item style", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": "plain", "label": "plain strings"},
                                            {"value": "badges", "label": "badge rows"},
                                        ],
                                        value=style,
                                        on_change=ctx.callback(_set_style),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Live preview
                    Container(
                        class_name="border rounded-lg p-6 bg-muted/30",
                        children=[
                            List(ordered=ordered, children=list_children),
                        ],
                    ),
                    Markdown(
                        content=(
                            "```python\n"
                            "List(\n"
                            f"    ordered={ordered},\n"
                            "    children=[\n"
                            + "".join(f'        "{item}",\n' for item in _ITEMS[:4])
                            + "    ],\n"
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
    """Render the List component reference page."""
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
Ordered or unordered list rendering. Children can be plain strings or
any component that renders to a list item.

```python
from refast.components import List

# Bullet list
List(children=["Apples", "Bananas", "Cherries"])

# Numbered list
List(ordered=True, children=["First step", "Second step", "Third step"])
```
"""

REFERENCE = """
## List Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | List items — strings or components. |
| `ordered` | `bool` | `False` | If `True`, renders a numbered `<ol>`; otherwise a bulleted `<ul>`. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## Unordered list

```python
List(children=[
    "Item one",
    "Item two",
    "Item three",
])
```

## Ordered list

```python
List(
    ordered=True,
    children=[
        "Install Refast: pip install refast",
        "Create your app: ui = RefastApp()",
        "Define a page: @ui.page('/')",
        "Run it: uvicorn app:app --reload",
    ],
)
```

## Rich list items with Row/Badge

Use `Column` + individual `Row` items for rich list-style layouts without
the semantic list markup:

```python
Column(
    gap=2,
    children=[
        Row(align="center", gap=2, children=[
            Badge(children=["NEW"], variant="success"),
            Text("Feature announcement", class_name="font-medium"),
        ]),
        Row(align="center", gap=2, children=[
            Badge(children=["FIX"]),
            Text("Bug fix for table sorting"),
        ]),
    ],
)
```
"""
