"""Code — /docs/components/code."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Checkbox,
    Code,
    Column,
    Container,
    Heading,
    Markdown,
    Paragraph,
    Row,
    Select,
    Separator,
    Text,
)

PAGE_TITLE = "Code"
PAGE_ROUTE = "/docs/components/code"


# ── Playground callbacks ──────────────────────────────────────────────────


async def _set_language(ctx: Context, value: str):
    ctx.state.set("cd_language", value)
    await ctx.refresh()


async def _set_line_numbers(ctx: Context, value: bool):
    ctx.state.set("cd_line_numbers", value)
    await ctx.refresh()


# ── Playground builder ────────────────────────────────────────────────────

_BLOCK_CODE = """def greet(name: str) -> str:
    \"\"\"Return a greeting message.\"\"\"
    return f"Hello, {name}!"


result = greet("World")
print(result)"""


def _playground(ctx: Context):
    language = ctx.state.get("cd_language", "python")
    line_numbers = ctx.state.get("cd_line_numbers", False)

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
                                    Text("language", class_name="text-sm font-medium"),
                                    Select(
                                        options=[
                                            {"value": v, "label": v}
                                            for v in [
                                                "python",
                                                "typescript",
                                                "javascript",
                                                "bash",
                                                "json",
                                                "css",
                                            ]
                                        ],
                                        value=language,
                                        on_change=ctx.callback(_set_language),
                                    ),
                                ],
                            ),
                            Column(
                                gap=2,
                                justify="end",
                                children=[
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Checkbox(
                                                checked=line_numbers,
                                                on_change=ctx.callback(_set_line_numbers),
                                                id="cd-ln-cb",
                                            ),
                                            Text("show_line_numbers", class_name="text-sm"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    Code(
                        code=_BLOCK_CODE,
                        language=language,
                        inline=False,
                        show_line_numbers=line_numbers,
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
Syntax-highlighted code display. Renders as inline `<code>` or a full code block.

```python
from refast.components import Code

# Inline code (default)
Code("print('hello')", language="python")

# Code block with line numbers
Code(
    code="def add(a, b):\\n    return a + b",
    language="python",
    inline=False,
    show_line_numbers=True,
)
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `code` | `str` | *(required)* | The code content to display |
| `language` | `str \\| None` | `None` | Language for syntax highlighting (e.g. `"python"`) |
| `inline` | `bool` | `True` | `True` = inline `<code>`, `False` = block |
| `show_line_numbers` | `bool` | `False` | Show line numbers (block mode only) |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |
| `style` | `dict \\| None` | `None` | Inline CSS overrides |

## Inline vs Block

```python
# Inline — for use in prose
Text("Call the ")
Code("render()", language="python")
Text(" function.")

# Block — for code listings
Code(
    code=source_code,
    language="typescript",
    inline=False,
    show_line_numbers=True,
)
```

## Supported Languages

Any language supported by the underlying syntax highlighter, including:
`python`, `typescript`, `javascript`, `tsx`, `jsx`, `bash`, `json`, `yaml`,
`css`, `html`, `sql`, `rust`, `go`, and many more.
"""
