# Refast Documentation Site

A comprehensive documentation site for the Refast framework, **built with Refast itself**.

## Quick Start

```bash
# From the project root
uvicorn docs_site.app:app --reload --port 8000
```

Open http://localhost:8000

## Structure

```
docs_site/
├── app.py                      # Main app, shared layout, route registrations
├── AGENT_INSTRUCTIONS.md       # Top-level instructions for AI agents
├── TODO.md                     # Known issues tracker
├── README.md                   # This file
└── pages/
    ├── home.py                 # Landing page (/)
    ├── getting_started/        # Installation, Architecture, Quick Tour, Examples
    ├── concepts/               # Components, Callbacks, State, Store, Updates, etc.
    ├── components/             # Full API reference for all UI components
    └── advanced/               # Component dev, Extension dev, Security, Sessions, Styling
```

## Adding a Page

1. Create `pages/<section>/<name>.py` with `PAGE_TITLE`, `PAGE_ROUTE`, and `render(ctx)`
2. Import it in `app.py`
3. Add `@ui.page(route)` handler in `app.py`
4. Add the page to `NAV_SECTIONS` in `app.py` for sidebar navigation

## Page Template

```python
"""Page Title — /docs/route."""
from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "Page Title"
PAGE_ROUTE = "/docs/route"

def render(ctx):
    from docs_site.app import docs_layout
    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(text="Your content here"),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)
```

## For AI Agents

Each section folder contains an `AGENT_INSTRUCTIONS.md` with detailed per-page content
requirements, source files to read, and examples to include. Start there.
