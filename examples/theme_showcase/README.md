# Theme Showcase

Demonstrates Refast's theming and customization features.

## Features shown

| Feature | How it's used |
|---------|--------------|
| **Theme presets** | `rose_theme`, `green_theme`, `violet_theme`, etc. passed to `RefastApp(theme=…)` |
| **Runtime theme switching** | `await ctx.set_theme(theme)` pushes CSS variable overrides via WebSocket — no reload |
| **Custom theme** | A hand-crafted "Teal" theme built with `Theme(light=ThemeColors(…), dark=ThemeColors(…))` |
| **Custom CSS** | Inline `<style>` block with gradient background and hover effects |
| **Custom JS** | `console.log()` injected at page load (check DevTools) |
| **Favicon** | Emoji favicon via `favicon="https://fav.farm/🎨"` |
| **Head tags** | `<meta name="description">`, `<meta name="theme-color">`, and a `<link rel="preconnect">` |
| **`add_head_tag()`** | Programmatically adds a `<link>` after construction |
| **Light/dark mode** | `ThemeSwitcher` dropdown toggles `.dark` class — works with every preset |

## Run

```bash
cd examples/theme_showcase
uvicorn app:app --reload
```

Then open http://localhost:8000.

## What to try

1. Click the preset buttons to switch themes instantly.
2. Toggle light/dark mode with the sun/moon switcher.
3. Enter a custom HSL value (e.g. `280 80% 55%`) and click Apply.
4. Open DevTools → Elements → `<head>` to see the injected `<style>`, `<meta>`, and `<link>` tags.
5. Open DevTools → Console to see the custom JS log message.
