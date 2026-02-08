"""Typography Components — /docs/components/typography."""

from refast.components import Container, Heading, Markdown, Separator


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
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Components in this section

- **Heading** — `<h1>` through `<h6>` headings
- **Text** — Inline `<span>` text
- **Paragraph** — Block `<p>` text
- **Code** — Inline `<code>` element
- **Link** — Clickable `<a>` hyperlink
- **Markdown** — Rich text renderer with GFM, syntax highlighting, and KaTeX math
- **Label** — Form field label
- **Badge** — Small status indicator
- **Kbd** — Keyboard shortcut display

---

### Heading

```python
Heading("Page Title", level=1, class_name="text-3xl font-bold")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | (positional) | Heading text |
| `level` | `1-6` | `1` | HTML heading level (h1-h6) |

---

### Markdown

Renders Markdown with support for GitHub Flavored Markdown (tables, strikethrough),
syntax highlighting for code blocks, and KaTeX math equations.

```python
Markdown(content=\"\"\"
# Hello World

This is **bold** and `inline code`.

```python
print("syntax highlighted!")
```

Math: $E = mc^2$
\"\"\")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | `""` | Markdown content |

---

### Badge

```python
Badge("New", variant="default")
Badge("Error", variant="destructive")
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | (positional) | Badge text |
| `variant` | `"default" \| "secondary" \| "destructive" \| "outline"` | `"default"` | Visual variant |

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
