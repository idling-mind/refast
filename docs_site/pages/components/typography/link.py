"""Link — /docs/components/link."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Column,
    Container,
    Heading,
    Link,
    Markdown,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Link"
PAGE_ROUTE = "/docs/components/link"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_target(ctx: Context, value: str):
    ctx.state.set("lk_target", value)
    await ctx.refresh()


async def _set_underline(ctx: Context, value: bool):
    ctx.state.set("lk_underline", value)
    await ctx.refresh()


async def _set_external(ctx: Context, value: bool):
    ctx.state.set("lk_external", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────


def _playground(ctx: Context):
    target = ctx.state.get("lk_target", "_self")
    underline = ctx.state.get("lk_underline", False)
    external = ctx.state.get("lk_external", False)

    link_class = "underline underline-offset-4" if underline else ""

    return Card(
        children=[
            CardHeader(title="Interactive Playground"),
            CardContent(
                children=[
                    Row(
                        gap=4,
                        wrap=True,
                        class_name="mb-4",
                        children=[
                            Column(
                                gap=1,
                                children=[
                                    Text("target", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in ["_self", "_blank", "_parent", "_top"]
                                        ],
                                        value=target,
                                        on_change=ctx.callback(_set_target),
                                    ),
                                ],
                            ),
                            Column(
                                gap=2,
                                children=[
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                checked=underline,
                                                on_change=ctx.callback(_set_underline),
                                                id="lk-underline-cb",
                                            ),
                                            Text("underline (via class_name)", class_name="text-sm"),
                                        ],
                                    ),
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                checked=external,
                                                on_change=ctx.callback(_set_external),
                                                id="lk-external-cb",
                                            ),
                                            Text("external (show icon)", class_name="text-sm"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Container(
                        class_name="border rounded-lg p-4 bg-muted/30",
                        children=[
                            Column(
                                gap=3,
                                children=[
                                    Link(
                                        text="Visit the Refast repository",
                                        href="https://github.com",
                                        target=target,
                                        external=external,
                                        class_name=link_class,
                                    ),
                                    Link(
                                        text="Documentation home",
                                        href="/",
                                        target=target,
                                        class_name=link_class,
                                    ),
                                ],
                            )
                        ],
                    ),
                    Text(
                        f'target="{target}"  external={external}  class_name="{link_class}"',
                        class_name="text-xs text-muted-foreground mt-2 font-mono",
                    ),
                ]
            ),
        ]
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
Hyperlink component that renders an `<a>` element with optional external-link
icon and server-side callbacks.

```python
from refast.components import Link

# Simple navigation link
Link("Go to Docs", href="/docs")

# External link with icon
Link("GitHub", href="https://github.com", target="_blank", external=True)

# Link with click callback
Link(
    "Load more",
    href="#",
    on_click=ctx.callback(handle_load_more),
    class_name="text-primary hover:underline",
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | *(required)* | Visible link text |
| `href` | `str` | *(required)* | Link destination URL |
| `target` | `"_self" \\| "_blank" \\| "_parent" \\| "_top"` | `"_self"` | Where to open the link |
| `external` | `bool` | `False` | Show an external-link icon |
| `on_click` | `Callback \\| None` | `None` | Server callback on click |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |
| `style` | `dict \\| None` | `None` | Inline CSS overrides |

## Notes

Use `class_name="underline underline-offset-4"` to match the default link
styling convention. For navigation within the app prefer `href="/<route>"` —
these are handled by the SPA router automatically.
"""
