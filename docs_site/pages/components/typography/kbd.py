"""Kbd — /docs/components/kbd."""

from refast import Context
from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Heading,
    Kbd,
    Markdown,
    Paragraph,
    Row,
    Separator,
    Text,
)

PAGE_TITLE = "Kbd"
PAGE_ROUTE = "/docs/components/kbd"


def render(ctx: Context):
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            _showcase(),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


def _showcase():
    shortcuts = [
        ("Open command palette", ["⌘", "K"]),
        ("Save file", ["Ctrl", "S"]),
        ("Undo", ["⌘", "Z"]),
        ("Redo", ["⌘", "Shift", "Z"]),
        ("Find", ["Ctrl", "F"]),
        ("Select all", ["⌘", "A"]),
        ("Copy", ["⌘", "C"]),
        ("Paste", ["⌘", "V"]),
    ]

    return Card(
        children=[
            CardHeader(title="Keyboard Shortcuts Showcase"),
            CardContent(
                children=[
                    Column(
                        gap=3,
                        children=[
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    Text(label, class_name="text-sm text-muted-foreground"),
                                    Row(
                                        gap=1,
                                        align="center",
                                        children=[
                                            *[Kbd(k) for k in keys[:-1]],
                                            *([Text("+", class_name="text-xs text-muted-foreground mx-0.5")] if len(keys) > 1 else []),
                                            Kbd(keys[-1]),
                                        ]
                                        if len(keys) == 1
                                        else [
                                            item
                                            for i, k in enumerate(keys)
                                            for item in (
                                                [Kbd(k)]
                                                if i == 0
                                                else [
                                                    Text(
                                                        "+",
                                                        class_name="text-xs text-muted-foreground",
                                                    ),
                                                    Kbd(k),
                                                ]
                                            )
                                        ],
                                    ),
                                ],
                            )
                            for label, keys in shortcuts
                        ],
                    ),
                ]
            ),
        ]
    )


INTRO = """
Renders a keyboard key in a styled `<kbd>` element. Use it to document
keyboard shortcuts in help text and documentation.

```python
from refast.components import Kbd, Text

# Inline in prose
Text("Press ")
Kbd("⌘")
Text(" + ")
Kbd("K")
Text(" to open the command palette.")

# Single key
Kbd("Enter")
Kbd("Escape")
Kbd("Tab")
```
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `key` | `str` | *(required)* | The key label to display |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes |

## Notes

`Kbd` is a pure display component — it renders the key label inside a styled
`<kbd>` HTML element. Combine multiple `Kbd` components with separator `Text`
(e.g. `"+"` or `"then"`) to represent key combinations.

## Common Key Symbols

| Symbol | Meaning |
|--------|---------|
| `⌘` | Command (macOS) |
| `⌃` | Control |
| `⌥` | Option / Alt |
| `⇧` | Shift |
| `⏎` | Return / Enter |
| `⌫` | Backspace |
| `⇥` | Tab |
| `⎋` | Escape |
"""
