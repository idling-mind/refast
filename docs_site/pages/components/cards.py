"""Cards & Containers — /docs/components/cards."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Cards & Containers"
PAGE_ROUTE = "/docs/components/cards"


def render(ctx):
    """Render the cards reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Components in this section

- **Card** — Container with border and shadow
- **CardHeader** — Card header area
- **CardTitle** — Card title text
- **CardDescription** — Card subtitle/description
- **CardContent** — Card body
- **CardFooter** — Card footer area
- **Collapsible** / **CollapsibleTrigger** / **CollapsibleContent** — Expandable/collapsible section

---

### Card

```python
Card(children=[
    CardHeader(children=[
        CardTitle("Dashboard"),
        CardDescription("Overview of your data"),
    ]),
    CardContent(children=[
        Text("Main content goes here"),
    ]),
    CardFooter(children=[
        Button("Save", on_click=ctx.callback(save)),
    ]),
])
```

---

### Collapsible

```python
Collapsible(children=[
    CollapsibleTrigger(children=[
        Button("Toggle Details", variant="ghost"),
    ]),
    CollapsibleContent(children=[
        Text("Hidden details revealed on click"),
    ]),
])
```

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
