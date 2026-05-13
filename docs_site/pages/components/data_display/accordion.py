"""Accordion — /docs/components/accordion.

Interactive reference page for the Accordion component family.
"""

from refast import Context
from refast.components import (
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Accordion"
PAGE_ROUTE = "/docs/components/accordion"

_FAQ_ITEMS = [
    ("Is it accessible?", "Yes. It adheres to the WAI-ARIA design pattern for accordions."),
    (
        "Is it styled?",
        "Yes. It comes with default styles that match the shadcn/ui design system.",
    ),
    (
        "Is it animated?",
        "Yes. It uses CSS transitions to animate the open/close state smoothly.",
    ),
    (
        "Can I use it without JavaScript?",
        "No. The accordion relies on client-side interactivity for open/close toggling.",
    ),
    (
        "How do I control it from Python?",
        "Pass a `value` prop and an `on_value_change` callback to track open items server-side.",
    ),
]


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_type(ctx: Context, value: str):
    ctx.state.set("acd_type", value)
    await ctx.refresh()


async def _set_count(ctx: Context, value: str):
    ctx.state.set("acd_count", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    accordion_type = ctx.state.get("acd_type", "single")
    item_count = int(ctx.state.get("acd_count", "3"))

    items = [
        AccordionItem(
            value=f"item-{i}",
            children=[
                AccordionTrigger(children=[_FAQ_ITEMS[i][0]]),
                AccordionContent(
                    children=[
                        Text(_FAQ_ITEMS[i][1], class_name="text-sm text-muted-foreground")
                    ]
                ),
            ],
        )
        for i in range(item_count)
    ]

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("Type", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "single", "label": "single"},
                            {"value": "multiple", "label": "multiple"},
                        ],
                        value=accordion_type,
                        on_change=ctx.callback(_set_type),
                    ),
                ],
            ),
            Column(
                gap=1,
                children=[
                    Text("Item count", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": "2", "label": "2"},
                            {"value": "3", "label": "3"},
                            {"value": "5", "label": "5"},
                        ],
                        value=str(item_count),
                        on_change=ctx.callback(_set_count),
                    ),
                ],
            ),
        ],
        preview=[
            Accordion(
                type=accordion_type,
                collapsible=True,
                children=items,
            )
        ],
        code=Markdown(
            content=(
                "```python\n"
                "Accordion(\n"
                f'    type="{accordion_type}",\n'
                "    collapsible=True,\n"
                "    children=[\n"
                + "".join(
                    f'        AccordionItem(value="item-{i}", children=[\n'
                    f'            AccordionTrigger(children=["{_FAQ_ITEMS[i][0]}"]),\n'
                    f'            AccordionContent(children=[Text("...")]),\n'
                    f"        ]),\n"
                    for i in range(item_count)
                )
                + "    ],\n"
                ")\n"
                "```"
            )
        ),
        preview_class="border rounded-lg p-4 bg-muted/30",
    )


# ── Render ────────────────────────────────────────────────────────────────


def render(ctx: Context):
    """Render the Accordion component reference page."""
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
Vertically stacked collapsible sections. Ideal for FAQs, settings panels,
and any content that benefits from progressive disclosure.

```python
from refast.components import Accordion, AccordionItem, AccordionTrigger, AccordionContent

Accordion(
    type="single",
    collapsible=True,
    children=[
        AccordionItem(
            value="q1",
            children=[
                AccordionTrigger(children=["Is it accessible?"]),
                AccordionContent(children=[Text("Yes. It adheres to WAI-ARIA.")]),
            ],
        ),
    ],
)
```
"""

REFERENCE = """
## Accordion Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | `AccordionItem` components. |
| `type` | `"single" \\| "multiple"` | `"single"` | `"single"` allows one item open; `"multiple"` allows many. |
| `collapsible` | `bool` | `True` | When `type="single"`, allows closing all items. |
| `default_value` | `str \\| list[str] \\| None` | `None` | Initially open item(s) (uncontrolled). |
| `value` | `str \\| list[str] \\| None` | `None` | Controlled open item(s). |
| `on_value_change` | `Callback \\| None` | `None` | Fired when open items change. `ctx.event_data` is `{"value": ...}`. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## AccordionItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str` | *(required)* | Unique identifier within the accordion. |
| `children` | `list` | `[]` | One `AccordionTrigger` and one `AccordionContent`. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## AccordionTrigger / AccordionContent Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list` | `[]` | Trigger label text or content to reveal. |
| `class_name` | `str` | `""` | Extra Tailwind classes. |

## Multiple open items

```python
Accordion(
    type="multiple",
    default_value=["item-1", "item-3"],
    children=[
        AccordionItem(value="item-1", children=[
            AccordionTrigger(children=["Section 1"]),
            AccordionContent(children=[Text("Content 1")]),
        ]),
        AccordionItem(value="item-2", children=[
            AccordionTrigger(children=["Section 2"]),
            AccordionContent(children=[Text("Content 2")]),
        ]),
        AccordionItem(value="item-3", children=[
            AccordionTrigger(children=["Section 3"]),
            AccordionContent(children=[Text("Content 3")]),
        ]),
    ],
)
```

## Controlled accordion

```python
async def on_change(ctx: Context):
    ctx.state.set("open_items", ctx.event_data.get("value"))
    await ctx.refresh()

def render(ctx: Context):
    open_items = ctx.state.get("open_items", [])
    return Accordion(
        type="multiple",
        value=open_items,
        on_value_change=ctx.callback(on_change),
        children=[...],
    )
```
"""
