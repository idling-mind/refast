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
## Overview

This section covers the `Card` family — a bordered, shadowed container
component and its structural sub-components: `CardHeader`, `CardTitle`,
`CardDescription`, `CardContent`, and `CardFooter`.

---

## Card

A rounded, bordered container with a subtle drop shadow. Use it to group
related content and actions into a visually distinct surface.

```python
from refast.components.shadcn.card import (
    Card, CardHeader, CardTitle, CardDescription,
    CardContent, CardFooter,
)
from refast.components.base import Text
from refast.components.shadcn.button import Button

Card(
    children=[
        CardHeader(
            title="Team Members",
            description="Manage your team and their access levels.",
        ),
        CardContent(children=[
            Text("Alice — Admin"),
            Text("Bob — Editor"),
        ]),
        CardFooter(children=[
            Button("Invite member", on_click=ctx.callback(invite)),
        ]),
    ]
)
```

### Card props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Card sub-components (`CardHeader`, `CardContent`, `CardFooter`, etc.). |
| `title` | `str \| None` | `None` | Shorthand title rendered by the React component directly (without `CardHeader`). |
| `description` | `str \| None` | `None` | Shorthand description rendered below `title`. |
| `on_click` | `Callback \| None` | `None` | Optional click callback — makes the card interactive. |
| `class_name` | `str` | `""` | Additional CSS class names. |
| `style` | `dict \| None` | `None` | Inline CSS style dict. |

---

## CardHeader

The top section of a card. Renders as a vertically-stacked flex container
with consistent padding. Accepts either the convenient `title`/`description`
shorthand or explicit `CardTitle` / `CardDescription` children.

```python
# Shorthand — title and description as props
CardHeader(title="Dashboard", description="Overview of your metrics")

# Explicit sub-components — use when you need custom styling
CardHeader(children=[
    CardTitle("Dashboard"),
    CardDescription("Overview of your metrics"),
])
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `str \| None` | `None` | Shorthand title text. |
| `description` | `str \| None` | `None` | Shorthand subtitle text. |
| `children` | `list` | `[]` | Explicit child components (overrides shorthand). |
| `class_name` | `str` | `""` | Additional CSS class names. |
| `style` | `dict \| None` | `None` | Inline CSS style dict. |

---

## CardTitle

Renders as a prominent `<h3>` heading. Pass the title text as `children`.

```python
CardTitle("Billing Summary")
CardTitle(children=["Billing Summary"])
CardTitle(children=["Billing Summary"], class_name="text-xl")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Title text or components. |
| `class_name` | `str` | `""` | Additional CSS class names. |
| `style` | `dict \| None` | `None` | Inline CSS style dict. |

---

## CardDescription

Renders as a muted `<p>` tag beneath the title. Pass the description text as
`children`.

```python
CardDescription("Renews monthly — cancel any time.")
CardDescription(children=["Renews monthly — cancel any time."])
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Description text or components. |
| `class_name` | `str` | `""` | Additional CSS class names. |
| `style` | `dict \| None` | `None` | Inline CSS style dict. |

---

## CardContent

The main body of the card. Rendered with appropriate padding below any
`CardHeader` (top padding is suppressed so the header and content spacing
align correctly).

```python
CardContent(children=[
    Text("Your current plan: **Pro**"),
    Text("Next payment: March 1, 2027"),
])
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Content to display in the card body. |
| `class_name` | `str` | `""` | Additional CSS class names. |
| `style` | `dict \| None` | `None` | Inline CSS style dict. |

---

## CardFooter

A flex row at the bottom of the card, typically used for action buttons.

```python
CardFooter(children=[
    Button("Cancel", variant="outline"),
    Button("Save changes", on_click=ctx.callback(save)),
])
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Footer content — typically action buttons. |
| `class_name` | `str` | `""` | Additional CSS class names. |
| `style` | `dict \| None` | `None` | Inline CSS style dict. |

---

## Full example

```python
from refast.components.shadcn.card import (
    Card, CardHeader, CardTitle, CardDescription,
    CardContent, CardFooter,
)
from refast.components.base import Container, Text
from refast.components.shadcn.button import Button
from refast.components.shadcn.data_display import Badge


async def subscribe(ctx):
    await ctx.show_toast("Subscribed!")


def pricing_card(ctx):
    return Card(
        class_name="w-80",
        children=[
            CardHeader(children=[
                CardTitle("Pro Plan"),
                CardDescription("Everything you need for a growing team."),
            ]),
            CardContent(children=[
                Container(class_name="flex items-baseline gap-1 mb-4", children=[
                    Text("$29", class_name="text-3xl font-bold"),
                    Text("/ month", class_name="text-muted-foreground"),
                ]),
                Container(children=[
                    Text("✓  Unlimited projects"),
                    Text("✓  Advanced analytics"),
                    Text("✓  Priority support"),
                ]),
            ]),
            CardFooter(children=[
                Button(
                    "Get started",
                    class_name="w-full",
                    on_click=ctx.callback(subscribe),
                ),
            ]),
        ],
    )
```
"""

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
