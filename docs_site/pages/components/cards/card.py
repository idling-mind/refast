"""Card — /docs/components/card.

Interactive reference page for the Card component family.
"""

from docs_site.pages.components.playground import playground_card
from refast import Context
from refast.components import (
    Button,
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
    Checkbox,
    Column,
    Container,
    Heading,
    Input,
    Markdown,
    Separator,
    Text,
)

PAGE_TITLE = "Card"
PAGE_ROUTE = "/docs/components/card"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_show_header(ctx: Context, value: bool):
    ctx.state.set("crd_show_header", value)
    await ctx.refresh()


async def _set_title(ctx: Context, value: str):
    ctx.state.set("crd_title", value)
    await ctx.refresh()


async def _set_description(ctx: Context, value: str):
    ctx.state.set("crd_description", value)
    await ctx.refresh()


async def _set_show_footer(ctx: Context, value: bool):
    ctx.state.set("crd_show_footer", value)
    await ctx.refresh()


async def _noop(ctx: Context):
    pass


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    show_header = ctx.state.get("crd_show_header", True)
    title = ctx.state.get("crd_title", "Team Members")
    description = ctx.state.get("crd_description", "Manage your team and their access levels.")
    show_footer = ctx.state.get("crd_show_footer", True)

    card_children = [
        CardContent(
            children=[
                Text("Alice — Admin", class_name="text-sm"),
                Text("Bob — Editor", class_name="text-sm"),
                Text("Carol — Viewer", class_name="text-sm"),
            ]
        )
    ]

    if show_header:
        card_children.insert(
            0,
            CardHeader(
                children=[
                    CardTitle(children=[title or "Card Title"]),
                    CardDescription(children=[description or ""]),
                ]
            ),
        )

    if show_footer:
        card_children.append(
            CardFooter(
                children=[
                    Button("Cancel", variant="outline", on_click=ctx.callback(_noop)),
                    Button("Invite Member", on_click=ctx.callback(_noop)),
                ]
            )
        )

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Show Header", class_name="text-sm font-medium"),
                    Checkbox(
                        label="show header",
                        checked=show_header,
                        on_change=ctx.callback(_set_show_header),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Title", class_name="text-sm font-medium"),
                    Input(
                        value=title,
                        placeholder="Card title…",
                        on_change=ctx.callback(_set_title),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Description", class_name="text-sm font-medium"),
                    Input(
                        value=description,
                        placeholder="Card description…",
                        on_change=ctx.callback(_set_description),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Show Footer", class_name="text-sm font-medium"),
                    Checkbox(
                        label="show footer",
                        checked=show_footer,
                        on_change=ctx.callback(_set_show_footer),
                    ),
                ],
            ),
        ],
        preview=[Card(children=card_children)],
        code=Markdown(
            content=(
                "```python\n"
                "Card(\n"
                "    children=[\n"
                + (
                    f'        CardHeader(\n'
                    f'            children=[\n'
                    f'                CardTitle(children=["{title}"]),\n'
                    f'                CardDescription(children=["{description}"]),\n'
                    f'            ]\n'
                    f'        ),\n'
                    if show_header
                    else ""
                )
                + "        CardContent(children=[...]),\n"
                + (
                    "        CardFooter(children=[Button(\"Cancel\"), Button(\"Save\")]),\n"
                    if show_footer
                    else ""
                )
                + "    ]\n"
                ")\n"
                "```"
            )
        ),
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Card component reference page."""
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
A rounded, bordered container with a subtle drop shadow for grouping related
content and actions into a visually distinct surface.

```python
from refast.components import (
    Card, CardHeader, CardTitle, CardDescription,
    CardContent, CardFooter,
)

Card(
    children=[
        CardHeader(title="Team Members", description="Manage your team."),
        CardContent(children=[Text("Alice — Admin")]),
        CardFooter(children=[Button("Invite Member")]),
    ]
)
```
"""

REFERENCE = """
## Card Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Sub-components (`CardHeader`, `CardContent`, `CardFooter`). |
| `title` | `str \\| None` | `None` | Shorthand title (rendered without `CardHeader`). |
| `description` | `str \\| None` | `None` | Shorthand description below `title`. |
| `on_click` | `Callback \\| None` | `None` | Makes the card interactive. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |
| `style` | `dict \\| None` | `None` | Inline CSS style dict. |

## CardHeader Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `str \\| None` | `None` | Shorthand heading text. |
| `description` | `str \\| None` | `None` | Shorthand subtitle text. |
| `children` | `list` | `[]` | Explicit `CardTitle` / `CardDescription` children. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## CardTitle Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Title text. Renders as `<h3>`. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## CardDescription Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Description text. Renders as muted `<p>`. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## CardContent Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Main body content. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## CardFooter Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Footer content — typically action buttons. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## Examples

### Shorthand title/description

```python
Card(title="Quick Stats", description="Last 30 days")
```

### Full composition

```python
Card(
    children=[
        CardHeader(
            children=[
                CardTitle("Dashboard"),
                CardDescription("Overview of your metrics"),
            ]
        ),
        CardContent(children=[Text("Your content here.")]),
        CardFooter(
            children=[
                Button("Cancel", variant="outline"),
                Button("Save changes"),
            ]
        ),
    ]
)
```

### Clickable card

```python
async def handle_card_click(ctx: Context):
    await ctx.show_toast("Card clicked!")

Card(
    title="Click me",
    description="This card is interactive.",
    on_click=ctx.callback(handle_card_click),
)
```
"""
