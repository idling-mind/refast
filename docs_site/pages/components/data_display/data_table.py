"""DataTable — /docs/components/data-table.

Interactive reference page for the DataTable component.
"""

from refast import Context
from refast.components import (
    Badge,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    DataTable,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "DataTable"
PAGE_ROUTE = "/docs/components/data-table"

_SAMPLE_DATA = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "role": "Admin", "status": "active"},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "role": "Editor", "status": "inactive"},
    {"id": 3, "name": "Carol White", "email": "carol@example.com", "role": "Viewer", "status": "pending"},
    {"id": 4, "name": "David Brown", "email": "david@example.com", "role": "Editor", "status": "active"},
    {"id": 5, "name": "Eva Green", "email": "eva@example.com", "role": "Viewer", "status": "active"},
    {"id": 6, "name": "Frank Lee", "email": "frank@example.com", "role": "Admin", "status": "inactive"},
    {"id": 7, "name": "Grace Kim", "email": "grace@example.com", "role": "Viewer", "status": "active"},
    {"id": 8, "name": "Henry Wang", "email": "henry@example.com", "role": "Editor", "status": "pending"},
    {"id": 9, "name": "Iris Chen", "email": "iris@example.com", "role": "Viewer", "status": "active"},
    {"id": 10, "name": "Jack Doe", "email": "jack@example.com", "role": "Admin", "status": "inactive"},
    {"id": 11, "name": "Karen Park", "email": "karen@example.com", "role": "Editor", "status": "active"},
    {"id": 12, "name": "Liam Turner", "email": "liam@example.com", "role": "Viewer", "status": "pending"},
]

_COLUMNS = [
    {"key": "id", "header": "#", "width": "60px", "align": "right"},
    {"key": "name", "header": "Name", "sortable": True},
    {"key": "email", "header": "Email", "sortable": True},
    {"key": "role", "header": "Role", "align": "center"},
    {"key": "status", "header": "Status", "sortable": True, "align": "center"},
]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_page_size(ctx: Context, value: str):
    ctx.state.set("dtb_page_size", value)
    await ctx.refresh()


async def _on_row_click(ctx: Context):
    row = ctx.event_data
    await ctx.show_toast(f"Clicked: {row.get('name', '?')} ({row.get('role', '?')})")


async def _on_sort(ctx: Context):
    ctx.state.set("dtb_sort", ctx.event_data)
    await ctx.refresh()


async def _on_page(ctx: Context):
    ctx.state.set("dtb_page", ctx.event_data.get("page", 1) if ctx.event_data else 1)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    page_size = int(ctx.state.get("dtb_page_size", "5"))
    current_page = ctx.state.get("dtb_page", 1)

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
                                    Text("Page size", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": "3", "label": "3 per page"},
                                            {"value": "5", "label": "5 per page"},
                                            {"value": "10", "label": "10 per page"},
                                        ],
                                        value=str(page_size),
                                        on_change=ctx.callback(_set_page_size),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Text(
                        "Click a row to see the row-click callback in action.",
                        class_name="text-sm text-muted-foreground mb-3",
                    ),
                    DataTable(
                        columns=_COLUMNS,
                        data=_SAMPLE_DATA,
                        sortable=True,
                        filterable=True,
                        paginated=True,
                        page_size=page_size,
                        current_page=current_page,
                        on_row_click=ctx.callback(_on_row_click),
                        on_sort_change=ctx.callback(_on_sort),
                        on_page_change=ctx.callback(_on_page),
                        empty_message="No users found.",
                    ),
                ]
            ),
        ]
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the DataTable component reference page."""
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
High-level data table with built-in sorting, filtering, and pagination.
Pass column definitions and row data — the component handles all UI concerns.
For full layout control use the primitive [Table](/docs/components/table) family instead.

```python
from refast.components import DataTable

DataTable(
    columns=[
        {"key": "name",   "header": "Name",   "sortable": True},
        {"key": "email",  "header": "Email",  "sortable": True},
        {"key": "role",   "header": "Role",   "align": "center"},
    ],
    data=[
        {"name": "Alice", "email": "alice@example.com", "role": "Admin"},
        {"name": "Bob",   "email": "bob@example.com",   "role": "Editor"},
    ],
    sortable=True,
    filterable=True,
    paginated=True,
    page_size=10,
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | `list[dict]` | *(required)* | Column definitions. Each dict needs `key` and `header`. |
| `data` | `list[dict]` | *(required)* | Row data. Each dict should have all column keys. |
| `sortable` | `bool` | `True` | Enable clicking column headers to sort. |
| `filterable` | `bool` | `True` | Show a text filter input above the table. |
| `paginated` | `bool` | `True` | Show pagination controls below the table. |
| `page_size` | `int` | `10` | Number of rows per page. |
| `loading` | `bool` | `False` | Show a loading overlay. |
| `empty_message` | `str` | `"No data available"` | Text shown when no rows match. |
| `current_page` | `int \\| None` | `None` | Controlled current page (1-based). |
| `on_row_click` | `Callback \\| None` | `None` | Fired when a row is clicked. `ctx.event_data` is the row dict. |
| `on_sort_change` | `Callback \\| None` | `None` | Fired on sort. `ctx.event_data` is `{"key": ..., "direction": "asc"/"desc"}` or `None`. |
| `on_filter_change` | `Callback \\| None` | `None` | Fired on filter input change. `ctx.event_data` is `{"value": ...}`. |
| `on_page_change` | `Callback \\| None` | `None` | Fired on page change. `ctx.event_data` is `{"page": N}`. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## Column definition keys

| Key | Required | Description |
|-----|----------|-------------|
| `key` | ✓ | Field name used to look up values in each row. |
| `header` | ✓ | Column header label. |
| `sortable` | | Per-column sortable override. |
| `width` | | CSS width (e.g. `"200px"`, `"20%"`). |
| `align` | | `"left"` (default), `"center"`, `"right"`. |

## Server-side pagination

```python
async def on_page(ctx: Context):
    page = ctx.event_data.get("page", 1)
    ctx.state.set("page", page)
    await ctx.refresh()

def render(ctx: Context):
    page = ctx.state.get("page", 1)
    page_data = fetch_page(page, size=10)
    return DataTable(
        columns=[...],
        data=page_data,
        paginated=True,
        page_size=10,
        current_page=page,
        on_page_change=ctx.callback(on_page),
    )
```
"""
