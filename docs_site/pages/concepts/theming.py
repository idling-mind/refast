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
## Overview

Refast includes a comprehensive theming system based on **CSS custom properties** (HSL
color tokens). It supports light/dark mode, 8 built-in theme presets, custom themes,
and runtime theme switching — all without a page reload.

---

## Built-in Presets

Import any preset from `refast.theme` and pass it to `RefastApp`:

| Name | Import symbol |
|------|--------------|
| Default (shadcn/ui blue) | `default_theme` |
| Amethyst Haze | `amethyst_haze_theme` |
| Amber Minimal | `amber_minimal_theme` |
| Bubblegum | `bubblegum_theme` |
| Caffine | `caffine_theme` |
| Catppuccin | `catppuccin_theme` |
| Twitter / X | `twitter_theme` |
| Ocean Breeze | `ocean_breeze_theme` |

The `THEMES` dict maps display names to `Theme` instances and can be used to build
a runtime theme picker.

```python
from refast import RefastApp
from refast.theme import amethyst_haze_theme, THEMES

# Apply a preset at startup
ui = RefastApp(title="My App", theme=amethyst_haze_theme)

# All built-in presets as a dict {name: Theme}
print(list(THEMES.keys()))
```

---

## Applying a Theme

Pass a `Theme` instance to `RefastApp`:

```python
from refast import RefastApp
from refast.theme import ocean_breeze_theme

ui = RefastApp(title="My App", theme=ocean_breeze_theme)
```

---

## Custom Themes

Create a `Theme` from `ThemeColors` objects. Every color token is an HSL triplet
string (e.g. `"221.2 83.2% 53.3%"`) — without the `hsl()` wrapper — matching the
shadcn/ui CSS variable convention.

All fields are optional; only the tokens you supply will be emitted as CSS
variable overrides.

```python
from refast.theme import Theme, ThemeColors, ThemeMode

my_theme = Theme(
    light=ThemeColors(
        background="0 0% 100%",
        foreground="222 47% 11%",
        primary="221 83% 53%",
        primary_foreground="210 40% 98%",
        secondary="210 40% 96%",
        muted="210 40% 96%",
        accent="210 40% 96%",
        border="214 32% 91%",
        ring="221 83% 53%",
    ),
    dark=ThemeColors(
        background="222 47% 11%",
        foreground="210 40% 98%",
        primary="217 91% 60%",
        primary_foreground="222 47% 11%",
        border="217 33% 17%",
        ring="217 91% 60%",
    ),
    font_family="'Inter', system-ui, sans-serif",
    radius="0.75rem",
    default_mode=ThemeMode.LIGHT,   # "light" | "dark" | "system"
)
```

### Available `ThemeColors` tokens

```
background · foreground
card · card_foreground
popover · popover_foreground
primary · primary_foreground
secondary · secondary_foreground
muted · muted_foreground
accent · accent_foreground
destructive · destructive_foreground
success · success_foreground
warning · warning_foreground
info · info_foreground
border · input · ring
chart_1 … chart_8
sidebar_background · sidebar_foreground
sidebar_primary · sidebar_primary_foreground
sidebar_accent · sidebar_accent_foreground
sidebar_border · sidebar_ring
```

---

## Light / Dark Mode Switcher

`ThemeSwitcher` is a built-in component that handles **light / dark / system** mode
switching entirely on the client side. It persists the user's choice to `localStorage`
and applies the Tailwind `dark` class to `<html>` automatically.

```python
from refast.components import ThemeSwitcher

# Toggle button (sun/moon icon, default)
ThemeSwitcher()

# Dropdown with Light, Dark, System options
ThemeSwitcher(mode="dropdown")

# Start in dark mode; hide the "System" option
ThemeSwitcher(
    default_theme="dark",
    show_system_option=False,
)

# Custom localStorage key (useful when multiple apps run on the same origin)
ThemeSwitcher(storage_key="my-app-theme")

# React to theme changes server-side
async def on_theme_change(ctx: Context, value: str):
    print(f"Client switched to: {value}")   # "light" | "dark" | "system"

ThemeSwitcher(on_change=ctx.callback(on_theme_change))
```

### `ThemeSwitcher` props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `default_theme` | `"light" \| "dark" \| "system"` | `"system"` | Initial mode if no stored preference |
| `mode` | `"toggle" \| "dropdown"` | `"toggle"` | Display as icon toggle or dropdown menu |
| `show_system_option` | `bool` | `True` | Include "System" option in dropdown mode |
| `storage_key` | `str` | `"refast-theme"` | `localStorage` key for persistence |
| `on_change` | callback | `None` | Server callback fired when user switches mode |

---

## Runtime Theme Switching (color scheme)

Switch the **active color preset** at runtime from a callback — no page reload needed.

```python
from refast import Context
from refast.theme import catppuccin_theme, ocean_breeze_theme

# Push a new theme to the current user only
async def use_catppuccin(ctx: Context):
    await ctx.set_theme(catppuccin_theme)

# Push a new theme to ALL connected clients
async def set_global_theme(ctx: Context):
    count = await ctx.broadcast_theme(ocean_breeze_theme)
    print(f"Updated {count} clients")
```

### Building a theme picker

```python
from refast.components import Button, Row
from refast.theme import THEMES

def theme_picker(ctx):
    async def switch(ctx: Context, theme_name: str):
        await ctx.set_theme(THEMES[theme_name])

    return Row(
        children=[
            Button(
                label=name,
                on_click=ctx.callback(switch, theme_name=name),
            )
            for name in THEMES
        ]
    )
```

---

## CSS Variables

Themes work by injecting a `<style>` block with CSS custom property overrides on
`:root` (light mode) and `.dark` (dark mode):

```css
:root {
    --background: 0 0% 100%;
    --foreground: 222 47% 11%;
    --primary: 221 83% 53%;
    --radius: 0.5rem;
    /* … */
}
.dark {
    --background: 222 47% 11%;
    --foreground: 210 40% 98%;
    --primary: 217 91% 60%;
    /* … */
}
```

Use these tokens in `class_name` via Tailwind's semantic color utilities:

```
bg-background    text-foreground
bg-primary       text-primary-foreground
bg-secondary     text-secondary-foreground
bg-muted         text-muted-foreground
bg-accent        text-accent-foreground
bg-card          text-card-foreground
border-border    ring-ring
```

---

## Custom & External CSS

You can inject additional CSS — either inline snippets or external URLs — via the
`custom_css` parameter on `RefastApp`, or the `add_css()` helper afterwards.

```python
from refast import RefastApp
from refast.theme import catppuccin_theme

ui = RefastApp(
    title="My App",
    theme=catppuccin_theme,
    custom_css=[
        # External URL → injected as <link rel="stylesheet">
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap",
        # Inline snippet → wrapped in <style>
        "body { font-family: 'Inter', sans-serif; }",
    ],
)

# Add more CSS any time after construction
ui.add_css("https://cdn.example.com/my-overrides.css")
ui.add_css(".hero { letter-spacing: -0.02em; }")
```

Strings starting with `http`, `https`, or `/` are treated as URLs (emitted as
`<link>` tags); everything else is treated as inline CSS (emitted inside a
`<style>` block).

### Overriding shadcn CSS variables from an external stylesheet

Because Refast sets all theme tokens as CSS custom properties on `:root` and
`.dark`, an external stylesheet can **override any of them** using the same
selectors — no Python code required:

```css
/* my-overrides.css — link it via custom_css */

:root {
    /* Override the primary color token for light mode */
    --primary: 174 72% 40%;
    --primary-foreground: 180 20% 99%;
    --radius: 0.75rem;
}

.dark {
    /* Override primary for dark mode */
    --primary: 174 65% 50%;
    --primary-foreground: 180 30% 5%;
}
```

You can also consume the tokens in your own custom rules — they always reflect
the currently active theme and update automatically when the user toggles
light/dark mode or when you call `ctx.set_theme()` at runtime:

```css
/* Consume tokens in custom component styles */
.hero-banner {
    background-color: hsl(var(--primary));
    color: hsl(var(--primary-foreground));
    border-radius: var(--radius);
}

.card-highlight {
    border: 1px solid hsl(var(--border));
    background: hsl(var(--card));
    color: hsl(var(--card-foreground));
}
```

### Full list of available CSS variables

```
--background           --foreground
--card                 --card-foreground
--popover              --popover-foreground
--primary              --primary-foreground
--secondary            --secondary-foreground
--muted                --muted-foreground
--accent               --accent-foreground
--destructive          --destructive-foreground
--success              --success-foreground
--warning              --warning-foreground
--info                 --info-foreground
--border               --input               --ring
--radius
--chart-1 … --chart-8
--sidebar-background   --sidebar-foreground
--sidebar-primary      --sidebar-primary-foreground
--sidebar-accent       --sidebar-accent-foreground
--sidebar-border       --sidebar-ring
```

---

## Next Steps

- [Toast Notifications](/docs/concepts/toasts) — Visual feedback for users
- [Styling](/docs/advanced/styling) — Full styling reference
"""
