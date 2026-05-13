"""Table — /docs/components/table.

Interactive reference page for the Table component family.
"""

from refast import Context
from refast.components import (
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
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
    Text,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Table"
PAGE_ROUTE = "/docs/components/table"

# Sample data
_SAMPLE_DATA = [
    {"name": "Alice Johnson", "email": "alice@example.com", "role": "Admin"},
    {"name": "Bob Smith", "email": "bob@example.com", "role": "Editor"},
    {"name": "Carol White", "email": "carol@example.com", "role": "Viewer"},
    {"name": "David Brown", "email": "david@example.com", "role": "Editor"},
    {"name": "Eva Green", "email": "eva@example.com", "role": "Viewer"},
    {"name": "Frank Lee", "email": "frank@example.com", "role": "Admin"},
    {"name": "Grace Kim", "email": "grace@example.com", "role": "Viewer"},
    {"name": "Henry Wang", "email": "henry@example.com", "role": "Editor"},
    {"name": "Iris Chen", "email": "iris@example.com", "role": "Viewer"},
    {"name": "Jack Doe", "email": "jack@example.com", "role": "Admin"},
]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_row_count(ctx: Context, value: str):
    ctx.state.set("tbl_rows", value)
    await ctx.refresh()


async def _set_striped(ctx: Context, value: bool):
    ctx.state.set("tbl_striped", value)
    await ctx.refresh()


async def _set_hoverable(ctx: Context, value: bool):
    ctx.state.set("tbl_hoverable", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    row_count = int(ctx.state.get("tbl_rows", "5"))
    striped = ctx.state.get("tbl_striped", False)
    hoverable = ctx.state.get("tbl_hoverable", True)

    rows = _SAMPLE_DATA[:row_count]

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Row count", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "2", "label": "2"},
                            {"value": "5", "label": "5"},
                            {"value": "10", "label": "10"},
                        ],
                        value=str(row_count),
                        on_change=ctx.callback(_set_row_count),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Striped", class_name="text-sm font-medium"),
                    Checkbox(
                        label="striped rows",
                        checked=striped,
                        on_change=ctx.callback(_set_striped),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Hoverable", class_name="text-sm font-medium"),
                    Checkbox(
                        label="row hover",
                        checked=hoverable,
                        on_change=ctx.callback(_set_hoverable),
                    ),
                ],
            ),
        ],
        preview=[
            Table(
                striped=striped,
                hoverable=hoverable,
                children=[
                    TableHeader(
                        children=[
                            TableRow(
                                children=[
                                    TableHead(children=["Name"]),
                                    TableHead(children=["Email"]),
                                    TableHead(children=["Role"]),
                                ]
                            )
                        ]
                    ),
                    TableBody(
                        children=[
                            TableRow(
                                children=[
                                    TableCell(children=[row["name"]]),
                                    TableCell(children=[row["email"]]),
                                    TableCell(children=[row["role"]]),
                                ]
                            )
                            for row in rows
                        ]
                    ),
                ],
            )
        ],
        code=Markdown(
            content=(
                "```python\n"
                "Table(\n"
                f"    striped={striped},\n"
                f"    hoverable={hoverable},\n"
                "    children=[\n"
                "        TableHeader(children=[\n"
                "            TableRow(children=[\n"
                "                TableHead(children=[\"Name\"]),\n"
                "                TableHead(children=[\"Email\"]),\n"
                "                TableHead(children=[\"Role\"]),\n"
                "            ])\n"
                "        ]),\n"
                "        TableBody(children=[\n"
                "            TableRow(children=[\n"
                "                TableCell(children=[\"Alice Johnson\"]),\n"
                "                TableCell(children=[\"alice@example.com\"]),\n"
                "                TableCell(children=[\"Admin\"]),\n"
                "            ]),\n"
                "            # ... more rows\n"
                "        ]),\n"
                "    ]\n"
                ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Table component reference page."""
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
Primitive HTML table building blocks for full layout control. Use the
`Table` family when you need custom cell rendering, row selection, or
complex action columns. For a turnkey table with sorting, filtering, and
pagination see [DataTable](/docs/components/data-table).

```python
from refast.components import (
    Table, TableHeader, TableBody,
    TableRow, TableHead, TableCell,
)

Table(
    striped=True,
    children=[
        TableHeader(children=[
            TableRow(children=[
                TableHead(children=["Name"]),
                TableHead(children=["Email"]),
            ])
        ]),
        TableBody(children=[
            TableRow(children=[
                TableCell(children=["Alice"]),
                TableCell(children=["alice@example.com"]),
            ]),
        ]),
    ]
)
```
"""

REFERENCE = """
## Table Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `TableHeader` and `TableBody` components. |
| `striped` | `bool` | `False` | Enables zebra-striping for body rows. |
| `hoverable` | `bool` | `True` | Body rows show a hover highlight. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## TableHeader / TableBody Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `TableRow` components. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## TableRow Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `TableHead` or `TableCell` components. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## TableHead Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Header cell content. |
| `class_name` | `str` | `""` | Extra Tailwind classes (e.g. `"text-right"`). |

## TableCell Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Cell content. |
| `col_span` | `int \\| None` | `None` | Number of columns to span. |
| `row_span` | `int \\| None` | `None` | Number of rows to span. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## Spanning cells

```python
TableRow(children=[
    TableCell(children=["Total"], col_span=2, class_name="font-bold"),
    TableCell(children=["42"], class_name="text-right"),
])
```

## Aligned columns

```python
TableHead(children=["Amount"], class_name="text-right")
TableCell(children=["$99.00"], class_name="text-right font-mono")
```
"""
