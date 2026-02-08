"""Data Display — /docs/components/data-display."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Data Display"
PAGE_ROUTE = "/docs/components/data-display"


def render(ctx):
    """Render the data display reference page."""
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

- **Table** / **TableHeader** / **TableBody** / **TableRow** / **TableHead** / **TableCell** — HTML table primitives
- **DataTable** — Higher-level data table component
- **Avatar** — User avatar with image or initials
- **Image** — Responsive image component
- **List** — Ordered or unordered list
- **Calendar** — Date display/selection calendar
- **Progress** — Progress bar
- **Skeleton** — Loading placeholder
- **Carousel** / **CarouselContent** / **CarouselItem** / **CarouselPrevious** / **CarouselNext** — Image/content carousel
- **Accordion** / **AccordionItem** / **AccordionTrigger** / **AccordionContent** — Expandable content sections
- **Tabs** / **TabItem** — Tabbed content switcher
- **HoverCard** / **HoverCardTrigger** / **HoverCardContent** — Card shown on hover
- **Tooltip** — Hover tooltip

---

### Table

```python
Table(children=[
    TableHeader(children=[
        TableRow(children=[
            TableHead("Name"),
            TableHead("Email"),
        ]),
    ]),
    TableBody(children=[
        TableRow(children=[
            TableCell("Alice"),
            TableCell("alice@example.com"),
        ]),
    ]),
])
```

---

### Tabs

```python
Tabs(
    default_value="tab1",
    children=[
        TabItem(label="Overview", value="tab1", children=[
            Text("Overview content"),
        ]),
        TabItem(label="Settings", value="tab2", children=[
            Text("Settings content"),
        ]),
    ],
)
```

---

### Accordion

```python
Accordion(
    type="single",
    collapsible=True,
    children=[
        AccordionItem(value="item1", children=[
            AccordionTrigger("Section 1"),
            AccordionContent(children=[Text("Content for section 1")]),
        ]),
    ],
)
```

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
