"""Markdown — /docs/components/markdown."""

from refast import Context
from refast.components import (
    Container,
    Heading,
    Markdown,
    Separator,
)

PAGE_TITLE = "Markdown"
PAGE_ROUTE = "/docs/components/markdown"


def render(ctx: Context):
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=INTRO),
            Markdown(content=SHOWCASE),
            Markdown(content=REFERENCE),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


INTRO = """
Rich text rendering with **GitHub Flavored Markdown** (GFM), syntax-highlighted
code blocks, tables, task lists, and KaTeX math.

```python
from refast.components import Markdown

Markdown(content=\"\"\"
# Hello World

This is **bold** and *italic* text.

```python
print("Hello!")
```
\"\"\")
```
"""

SHOWCASE = r"""
## Showcase

Below is a live render of various Markdown features:

---

### Text Formatting

Regular text, **bold**, *italic*, ~~strikethrough~~, and `inline code`.

> Blockquote: "Design is not just what it looks like and feels like. Design is how it works."
> — Steve Jobs

---

### Headings

# Heading 1
## Heading 2
### Heading 3
#### Heading 4

---

### Lists

**Unordered:**
- Item one
- Item two
  - Nested item
  - Another nested item
- Item three

**Ordered:**
1. First step
2. Second step
3. Third step

**Task list:**
- [x] Install Refast
- [x] Create your first page
- [ ] Deploy to production

---

### Code Block

```python
from refast import RefastApp, Context
from refast.components import Container, Heading, Button

ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="p-8",
        children=[
            Heading("Welcome", level=1),
            Button("Click me"),
        ],
    )
```

---

### Table

| Component | Category | Interactive |
|-----------|----------|-------------|
| `Button` | Actions | ✓ |
| `Input` | Forms | ✓ |
| `Markdown` | Typography | — |
| `Card` | Containers | — |

---

### Math (KaTeX)

Inline math: $E = mc^2$

Block math:

$$
\int_{-\infty}^{\infty} e^{-x^2}\, dx = \sqrt{\pi}
$$

The quadratic formula: $x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$

---

### Links & Images

[Refast Documentation](/) · [GitHub](https://github.com)
"""

REFERENCE = """
## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `str` | *(required)* | Markdown string to render |
| `allow_html` | `bool` | `False` | Allow raw HTML inside markdown (security risk) |
| `id` | `str \\| None` | `None` | Unique element ID |
| `class_name` | `str` | `""` | Extra Tailwind classes on the wrapper |

## Features

- **GFM** — GitHub Flavored Markdown: tables, strikethrough, task lists
- **Syntax highlighting** — fenced code blocks with language detection
- **KaTeX math** — inline `$...$` and block `$$...$$` LaTeX
- **Security** — HTML is stripped by default (`allow_html=False`)

## Notes

- `allow_latex` is deprecated (LaTeX is always rendered); it is accepted for
  backward compatibility but ignored.
- For untrusted content never set `allow_html=True`.
"""
