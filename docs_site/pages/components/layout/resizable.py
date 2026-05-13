"""Resizable — /docs/components/resizable."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Markdown,
    Paragraph,
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
    Row,
    Select,
    Separator,
    Text,
)
from docs_site.pages.components.playground import playground_card

PAGE_TITLE = "Resizable"
PAGE_ROUTE = "/docs/components/resizable"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_direction(ctx: Context, value: str):
    ctx.state.set("rs_direction", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    direction = ctx.state.get("rs_direction", "horizontal")

    if direction == "horizontal":
        panel_class = "h-32 flex items-center justify-center"
    else:
        panel_class = "h-24 flex items-center justify-center"

    return playground_card(
        options=[
            Column(
                gap=1,
                children=[
                    Text("direction", class_name="text-sm font-medium"),
                    Select(
                        options=[
                            {"value": v, "label": v}
                            for v in ["horizontal", "vertical"]
                        ],
                        value=direction,
                        on_change=ctx.callback(_set_direction),
                    ),
                ],
            ),
        ],
        preview=[
            Container(
                class_name="border rounded-lg overflow-hidden",
                style={"height": "300px"},
                children=[
                    ResizablePanelGroup(
                        direction=direction,
                        class_name="h-full",
                        children=[
                            ResizablePanel(
                                default_size=50,
                                min_size=20,
                                class_name=panel_class,
                                children=[
                                    Column(
                                        gap=1,
                                        align="center",
                                        children=[
                                            Text(
                                                "Panel A",
                                                class_name="font-medium text-sm",
                                            ),
                                            Text(
                                                "Drag the handle",
                                                class_name="text-xs text-muted-foreground",
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            ResizableHandle(with_handle=True),
                            ResizablePanel(
                                default_size=50,
                                min_size=20,
                                class_name=panel_class,
                                children=[
                                    Column(
                                        gap=1,
                                        align="center",
                                        children=[
                                            Text(
                                                "Panel B",
                                                class_name="font-medium text-sm",
                                            ),
                                            Text(
                                                "to resize",
                                                class_name="text-xs text-muted-foreground",
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),
        ],
        preview_class="",
    )


def render(ctx: Context):
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


INTRO = """
Split-pane layout built on Radix UI `ResizablePanelGroup`. Users can drag
the handle to resize panels at runtime.

```python
from refast.components import ResizablePanelGroup, ResizablePanel, ResizableHandle

ResizablePanelGroup(
    direction="horizontal",
    children=[
        ResizablePanel(default_size=30, min_size=15, children=[sidebar]),
        ResizableHandle(with_handle=True),
        ResizablePanel(default_size=70, children=[main_content]),
    ],
)
```
"""

REFERENCE = """
## ResizablePanelGroup

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `direction` | `"horizontal" \\| "vertical"` | `"horizontal"` | Split orientation |
| `children` | `list \\| Component \\| None` | `None` | Alternating panels and handles |
| `on_layout` | `Callback \\| None` | `None` | Fired with new panel size array on resize |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## ResizablePanel

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `default_size` | `float` | `50` | Initial size as % of group |
| `min_size` | `float \\| None` | `None` | Minimum size % |
| `max_size` | `float \\| None` | `None` | Maximum size % |
| `collapsible` | `bool` | `False` | Allow fully collapsing the panel |
| `collapsed_size` | `float \\| None` | `None` | Size % when fully collapsed |
| `children` | `list \\| Component \\| None` | `None` | Panel content |

## ResizableHandle

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `with_handle` | `bool` | `False` | Show a visible grip icon on the handle |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Examples

```python
# Three-column layout
ResizablePanelGroup(
    direction="horizontal",
    class_name="min-h-screen",
    children=[
        ResizablePanel(default_size=20, min_size=10, children=[nav]),
        ResizableHandle(),
        ResizablePanel(default_size=60, children=[editor]),
        ResizableHandle(),
        ResizablePanel(default_size=20, min_size=10, children=[sidebar]),
    ],
)
```
"""
