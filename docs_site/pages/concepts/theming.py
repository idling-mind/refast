"""Theming — /docs/concepts/theming."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Theming"
PAGE_ROUTE = "/docs/concepts/theming"


def render(ctx):
    """Render the theming concept page."""
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

## Overview

Refast includes a comprehensive theming system based on **CSS custom properties** (HSL
color tokens). It supports light/dark mode, 8 built-in theme presets, custom themes,
and runtime theme switching.

## Built-in Presets

| Theme | Import |
|-------|--------|
| Blue (default) | `from refast.theme import blue_theme` |
| Rose | `rose_theme` |
| Green | `green_theme` |
| Orange | `orange_theme` |
| Violet | `violet_theme` |
| Slate | `slate_theme` |
| Zinc | `zinc_theme` |

## Applying a Theme

```python
from refast.theme import slate_theme

ui = RefastApp(title="My App", theme=slate_theme)
```

## Custom Themes

```python
from refast.theme import Theme, ThemeColors

my_theme = Theme(
    light=ThemeColors(
        background="0 0% 100%",
        foreground="222 47% 11%",
        primary="221 83% 53%",
        primary_foreground="210 40% 98%",
        # ... more HSL color tokens
    ),
    dark=ThemeColors(
        background="222 47% 11%",
        foreground="210 40% 98%",
        primary="217 91% 60%",
        primary_foreground="222 47% 11%",
        # ...
    ),
)
```

## Runtime Theme Switching

```python
# Switch theme for current client
await ctx.set_theme(rose_theme)

# Switch theme for ALL connected clients
await ctx.broadcast_theme(rose_theme)
```

## ThemeSwitcher Component

A built-in light/dark/system toggle:

```python
from refast.components.shadcn import ThemeSwitcher

ThemeSwitcher()  # Dropdown with Light, Dark, System options
```

## CSS Variables

Themes work by setting CSS custom properties on `:root` and `.dark`:

```css
:root {
    --background: 0 0% 100%;
    --foreground: 222 47% 11%;
    --primary: 221 83% 53%;
    /* ... */
}
```

Use these in `class_name` via Tailwind's semantic colors:
`bg-primary`, `text-foreground`, `border-border`, etc.

## Next Steps

- [Toast Notifications](/docs/concepts/toasts) — Visual feedback for users
- [Styling](/docs/advanced/styling) — Full styling reference
"""
