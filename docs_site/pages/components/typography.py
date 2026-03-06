"""Typography Components — /docs/components/typography."""

from refast.components import Container, Heading, Separator

from ..utils import render_markdown_with_demo_apps

PAGE_TITLE = "Typography Components"
PAGE_ROUTE = "/docs/components/typography"


def render(ctx):
    """Render the typography components reference page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            render_markdown_with_demo_apps(CONTENT, locals()),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
## Overview

Typography components render text content in various formats.
See the **Form Inputs** page for `Label`, the **Data Display** page for `Badge`,
and the **Utility** page for `Kbd`.

---

## Heading

`<h1>` through `<h6>` headings with optional styling.

```python
Heading("Page Title", level=1)
Heading("Section", level=2, class_name="text-blue-600")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | *(required)* | Heading content |
| `level` | `1 \| 2 \| 3 \| 4 \| 5 \| 6` | `1` | HTML heading level |
| `style` | `dict \| None` | `None` | Inline CSS overrides |

---

## Paragraph

Block-level `<p>` element.

```python
Paragraph("This is a paragraph of body text.", class_name="text-muted-foreground")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | *(required)* | Paragraph content |
| `style` | `dict \| None` | `None` | Inline CSS overrides |

---

## Code

Inline or block code with optional syntax highlighting.

```python
# Inline code
Code("print('hello')", language="python")

# Code block
Code(
    code="def add(a, b):\n    return a + b",
    language="python",
    inline=False,
    show_line_numbers=True,
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `code` | `str` | *(required)* | Source code string |
| `language` | `str \| None` | `None` | Language for syntax highlighting (e.g., `"python"`, `"typescript"`) |
| `inline` | `bool` | `True` | Render as `<code>` (inline) or `<pre><code>` (block) |
| `show_line_numbers` | `bool` | `False` | Show line numbers in block mode |

---

## Link

Clickable `<a>` hyperlink.

```python
Link("GitHub", href="https://github.com", target="_blank")
Link("Profile", href="/profile", on_click=ctx.callback(navigate))
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | *(required)* | Link label |
| `href` | `str` | *(required)* | Destination URL |
| `target` | `"_self" \| "_blank" \| "_parent" \| "_top"` | `"_self"` | Link target |
| `on_click` | `Callback \| None` | `None` | Click callback |

---

## Markdown

Renders a Markdown string with GitHub Flavored Markdown (GFM) support,
syntax-highlighted code blocks, and KaTeX math equations.

```python
Markdown(
    content=\"""
# Hello World

This is **bold** and `inline code`.

Inline math: $E = mc^2$
\"""
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `str` | `""` | Markdown source string |
| `allow_html` | `bool` | `False` | Allow raw HTML inside the Markdown |

> **Note**: The `allow_latex` parameter is accepted for backward compatibility but is ignored.

---

## Icon

Renders a Lucide icon by name.

```python
Icon("home")                           # default 16 px
Icon("settings", size=24)
Icon("alert-circle", color="red", stroke_width=1.5)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str` | *(required)* | Lucide icon name (e.g., `"home"`, `"settings"`) |
| `size` | `int` | `16` | Icon size in pixels |
| `color` | `str \| None` | `None` | CSS colour value; defaults to `currentColor` |
| `stroke_width` | `float` | `2` | Stroke width |

Icons can be used inline as children of other components:

```python
Button("Save", children=[Icon("save", size=14)])
SidebarMenuButton("Home", icon="home")  # also accepts icon name directly
```
"""
