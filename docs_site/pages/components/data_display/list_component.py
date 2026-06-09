"""List — /docs/components/list.

Interactive reference page for the List and ListItem components.
"""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Checkbox,
    Column,
    Container,
    Heading,
    List,
    Markdown,
    Separator,
    Text,
)

PAGE_TITLE = "List"
PAGE_ROUTE = "/docs/components/list"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_ordered(ctx: Context, value: bool):
    ctx.state.set("lst_ordered", value)
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

    list_children = _ITEMS[:4]

    return playground_card(
        options=[
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
        ],
        preview=[
            List(ordered=ordered, children=list_children),
        ],
        code=Markdown(
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
