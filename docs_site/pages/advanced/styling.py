"""Styling — /docs/advanced/styling."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Styling"
PAGE_ROUTE = "/docs/advanced/styling"


def render(ctx):
    """Render the styling guide page."""
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
> Adapt from `docs/STYLING_GUIDE.md` and `docs/TAILWIND_SUPPORT.md`.

## Overview

Refast uses **Tailwind CSS** for styling, with a curated subset of utility classes
bundled with the framework. Components are styled via the `class_name` prop.

## The class_name Prop

Every component accepts `class_name`:

```python
Container(class_name="max-w-4xl mx-auto p-6 bg-card rounded-lg shadow")
Text("Hello", class_name="text-lg font-bold text-primary")
```

## Semantic Color Tokens

Use Refast's semantic colors (from the theme system) instead of raw colors:

| Token | Usage |
|-------|-------|
| `bg-background` / `text-foreground` | Page background and default text |
| `bg-primary` / `text-primary` | Primary brand color |
| `bg-secondary` / `text-secondary` | Secondary elements |
| `bg-muted` / `text-muted-foreground` | Subdued/disabled content |
| `bg-accent` / `text-accent-foreground` | Accent/highlight |
| `bg-destructive` | Error/danger |
| `bg-card` | Card backgrounds |
| `border-border` | Default borders |
| `ring-ring` | Focus rings |

## Available Tailwind Classes

Refast bundles an optimized subset of Tailwind:

- **Layout**: `flex`, `grid`, `block`, `inline`, `hidden`, `relative`, `absolute`, `fixed`
- **Spacing**: `p-{0-6,8,10,12,16}`, `m-{...}`, `gap-{...}`
- **Typography**: `text-{xs,sm,base,lg,xl,...}`, `font-{normal,medium,semibold,bold}`
- **Colors**: All semantic tokens above + `bg-white`, `bg-black`, `text-white`, etc.
- **Borders**: `rounded-{sm,md,lg,xl,full}`, `border`, `border-{t,r,b,l}`
- **Responsive**: `sm:`, `md:`, `lg:`, `xl:` prefixes

## The style Prop

For truly dynamic values that can't be expressed with Tailwind classes:

```python
Container(style={"width": f"{percentage}%"})
Progress(value=75, style={"height": "8px"})
```

> **Note**: Prefer `class_name` for static styling. Use `style` only for values
> computed at runtime (e.g., percentages, calculated positions).

## Custom CSS

Inject custom CSS globally:

```python
ui = RefastApp(title="My App", custom_css=".my-class { animation: spin 1s; }")
# or
ui.add_css(".my-class { animation: spin 1s; }")
```

## Next Steps

- [Theming](/docs/concepts/theming) — Theme configuration and presets
- [Building Components](/docs/advanced/component-dev) — Styling custom components
"""
