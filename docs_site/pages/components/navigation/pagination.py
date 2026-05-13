"""Pagination — /docs/components/pagination."""

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
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Pagination"
PAGE_ROUTE = "/docs/components/pagination"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_total_pages(ctx: Context, value: str):
    ctx.state.set("pgn_total", int(value))
    current = ctx.state.get("pgn_current", 1)
    if current > int(value):
        ctx.state.set("pgn_current", int(value))
    await ctx.refresh()


async def _go_prev(ctx: Context):
    current = ctx.state.get("pgn_current", 1)
    if current > 1:
        ctx.state.set("pgn_current", current - 1)
    await ctx.refresh()


async def _go_next(ctx: Context):
    total = ctx.state.get("pgn_total", 5)
    current = ctx.state.get("pgn_current", 1)
    if current < total:
        ctx.state.set("pgn_current", current + 1)
    await ctx.refresh()


async def _go_page(ctx: Context, page: int):
    ctx.state.set("pgn_current", page)
    await ctx.refresh()


# ── Helpers ───────────────────────────────────────────────────────────────


def _build_pagination(ctx: Context, current: int, total: int) -> Pagination:
    """Build visible page items with ellipsis logic."""
    items = []

    # Previous button
    items.append(
        PaginationItem(
            children=[PaginationPrevious(on_click=ctx.callback(_go_prev))]
        )
    )

    # Show at most 5 page links centred around current
    if total <= 7:
        visible = list(range(1, total + 1))
        show_left_ellipsis = False
        show_right_ellipsis = False
    else:
        show_left_ellipsis = current > 4
        show_right_ellipsis = current < total - 3

        if not show_left_ellipsis:
            visible = list(range(1, 6))
        elif not show_right_ellipsis:
            visible = list(range(total - 4, total + 1))
        else:
            visible = [current - 1, current, current + 1]

    if total > 7 and visible[0] != 1:
        items.append(
            PaginationItem(
                children=[
                    PaginationLink(
                        "1",
                        on_click=ctx.callback(_go_page, page=1),
                        active=(current == 1),
                    )
                ]
            )
        )
        if show_left_ellipsis:
            items.append(PaginationItem(children=[PaginationEllipsis()]))

    for page in visible:
        items.append(
            PaginationItem(
                children=[
                    PaginationLink(
                        str(page),
                        on_click=ctx.callback(_go_page, page=page),
                        active=(page == current),
                    )
                ]
            )
        )

    if total > 7 and visible[-1] != total:
        if show_right_ellipsis:
            items.append(PaginationItem(children=[PaginationEllipsis()]))
        items.append(
            PaginationItem(
                children=[
                    PaginationLink(
                        str(total),
                        on_click=ctx.callback(_go_page, page=total),
                        active=(current == total),
                    )
                ]
            )
        )

    # Next button
    items.append(
        PaginationItem(
            children=[PaginationNext(on_click=ctx.callback(_go_next))]
        )
    )

    return Pagination(children=[PaginationContent(children=items)])


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    total = ctx.state.get("pgn_total", 5)
    current = ctx.state.get("pgn_current", 1)

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Total pages", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": str(n), "label": str(n)}
                            for n in [5, 10, 20]
                        ],
                        value=str(total),
                        on_change=ctx.callback(_set_total_pages),
                    ),
                ],
            ),
        ],
        preview=[
            Text(
                f"Page {current} of {total}",
                class_name="text-sm text-muted-foreground mb-3",
            ),
            _build_pagination(ctx, current, total),
        ],
        code=Markdown(
            content=(
                "```python\n"
                "Pagination(\n"
                "    children=[\n"
                "        PaginationContent(\n"
                "            children=[\n"
                "                PaginationItem(children=[PaginationPrevious(on_click=ctx.callback(go_prev))]),\n"
                "                PaginationItem(children=[PaginationLink(\"1\", active=True, on_click=ctx.callback(go_page, page=1))]),\n"
                "                PaginationItem(children=[PaginationLink(\"2\", on_click=ctx.callback(go_page, page=2))]),\n"
                "                PaginationItem(children=[PaginationEllipsis()]),\n"
                "                PaginationItem(children=[PaginationNext(on_click=ctx.callback(go_next))]),\n"
                "            ]\n"
                "        )\n"
                "    ]\n"
                ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30 flex flex-col items-center",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Pagination component reference page."""
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
Navigate through pages of content with Previous/Next and numbered page links.

```python
from refast.components import (
    Pagination, PaginationContent, PaginationItem,
    PaginationLink, PaginationPrevious, PaginationNext, PaginationEllipsis,
)
```
"""

REFERENCE = """
## Props

### `PaginationLink`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | *(required)* | Page label text |
| `href` | `str` | `"#"` | URL for the link |
| `active` | `bool` | `False` | Highlights the current page |
| `on_click` | `Callback \\| None` | `None` | Server click callback |

### `PaginationPrevious` / `PaginationNext`

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `href` | `str` | `"#"` | Navigation URL |
| `on_click` | `Callback \\| None` | `None` | Server click callback |

## Component Hierarchy

```
Pagination
└── PaginationContent
    ├── PaginationItem
    │   └── PaginationPrevious
    ├── PaginationItem
    │   └── PaginationLink (active)
    ├── PaginationItem
    │   └── PaginationLink
    ├── PaginationItem
    │   └── PaginationEllipsis
    ├── PaginationItem
    │   └── PaginationLink
    └── PaginationItem
        └── PaginationNext
```

## Server-side Controlled Example

```python
async def go_prev(ctx: Context):
    page = ctx.state.get("page", 1)
    if page > 1:
        ctx.state.set("page", page - 1)
    await ctx.refresh()

async def go_next(ctx: Context):
    page = ctx.state.get("page", 1)
    total = ctx.state.get("total_pages", 10)
    if page < total:
        ctx.state.set("page", page + 1)
    await ctx.refresh()
```
"""
