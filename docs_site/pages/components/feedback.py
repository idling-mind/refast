"""Feedback & Overlay — /docs/components/feedback."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Feedback & Overlay"
PAGE_ROUTE = "/docs/components/feedback"


def render(ctx):
    """Render the feedback components reference page."""
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

### Feedback
- **Alert** — Informational alert box
- **Spinner** — Loading spinner
- **Progress** — Progress bar
- **Skeleton** — Loading placeholder shape

### Dialog
- **Dialog** / **DialogTrigger** / **DialogContent** / **DialogHeader** / **DialogTitle** / **DialogDescription** / **DialogFooter** / **DialogAction** / **DialogCancel**

### Sheet
- **Sheet** / **SheetTrigger** / **SheetContent** / **SheetHeader** / **SheetTitle** / **SheetDescription** / **SheetFooter** / **SheetClose**

### Drawer
- **Drawer** / **DrawerTrigger** / **DrawerContent** / **DrawerHeader** / **DrawerTitle** / **DrawerDescription** / **DrawerFooter** / **DrawerClose**

### Popover
- **Popover** / **PopoverTrigger** / **PopoverContent**

### Tooltip
- **Tooltip** — Hover tooltip with configurable content and side

---

### Alert

```python
Alert(
    title="Heads Up!",
    description="This is an informational alert.",
    variant="default",  # default | destructive
)
```

---

### Dialog

```python
Dialog(children=[
    DialogTrigger(children=[Button("Open Dialog")]),
    DialogContent(children=[
        DialogHeader(children=[
            DialogTitle("Are you sure?"),
            DialogDescription("This action cannot be undone."),
        ]),
        DialogFooter(children=[
            DialogCancel("Cancel"),
            DialogAction("Confirm", on_click=ctx.callback(confirm)),
        ]),
    ]),
])
```

---

### Sheet

Side panel that slides in from an edge:

```python
Sheet(children=[
    SheetTrigger(children=[Button("Open Sheet")]),
    SheetContent(
        side="right",  # top | right | bottom | left
        children=[
            SheetHeader(children=[SheetTitle("Settings")]),
            Text("Sheet content"),
        ],
    ),
])
```

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
