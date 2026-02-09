"""Theme Showcase Example — Demonstrates Refast theming & customization.

This example demonstrates:
- Applying a built-in theme preset at startup
- Switching themes at runtime with ctx.set_theme()
- Custom CSS (inline snippets and external URLs)
- Custom JavaScript injection
- Extra <head> tags (meta, preconnect)
- Favicon
- The add_css() / add_js() / add_head_tag() helpers

Run:
    uvicorn examples.theme_showcase.app:app --reload
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Input,
    Row,
    Separator,
    Text,
)
from refast.components.shadcn import Alert, ThemeSwitcher
from refast.theme import (
    Theme,
    ThemeColors,
    blue_theme,
    green_theme,
    orange_theme,
    rose_theme,
    slate_theme,
    violet_theme,
    zinc_theme,
)

# ── Available presets keyed by display name ──────────────────────────────

PRESETS: dict[str, Theme] = {
    "Default (Blue)": blue_theme,
    "Rose": rose_theme,
    "Green": green_theme,
    "Orange": orange_theme,
    "Violet": violet_theme,
    "Slate": slate_theme,
    "Zinc": zinc_theme,
}

# ── A fully custom theme to show ThemeColors usage ───────────────────────

custom_teal_theme = Theme(
    light=ThemeColors(
        background="180 20% 99%",
        foreground="180 50% 5%",
        primary="174 72% 40%",
        primary_foreground="180 20% 99%",
        secondary="174 30% 92%",
        secondary_foreground="174 50% 10%",
        muted="174 20% 95%",
        muted_foreground="174 15% 45%",
        accent="174 30% 92%",
        accent_foreground="174 50% 10%",
        border="174 20% 88%",
        ring="174 72% 40%",
    ),
    dark=ThemeColors(
        background="180 30% 5%",
        foreground="174 20% 95%",
        primary="174 65% 50%",
        primary_foreground="180 30% 5%",
        secondary="174 20% 14%",
        secondary_foreground="174 20% 95%",
        muted="174 20% 14%",
        muted_foreground="174 15% 60%",
        accent="174 20% 14%",
        accent_foreground="174 20% 95%",
        border="174 20% 14%",
        ring="174 65% 50%",
    ),
    font_family="'Segoe UI', system-ui, sans-serif",
    radius="0.75rem",
)

PRESETS["Custom Teal"] = custom_teal_theme

# ── Create the Refast app with theming + customization ───────────────────

ui = RefastApp(
    title="Theme Showcase",
    # Start with the rose preset
    theme=rose_theme,
    # Favicon
    favicon="https://fav.farm/🎨",
    # Custom CSS – inline snippet to add a subtle gradient to the page
    custom_css=[
        """
        .theme-showcase-gradient {
            background: linear-gradient(
                135deg,
                hsl(var(--primary) / 0.03) 0%,
                transparent 50%
            );
        }
        .swatch {
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .swatch:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px hsl(var(--primary) / 0.2);
        }
        """,
    ],
    # Custom JS – log theme changes
    custom_js=[
        "console.log('[Theme Showcase] App loaded with custom JS injection');",
    ],
    # Extra <head> tags
    head_tags=[
        '<meta name="description" content="Refast Theme Showcase – demonstrates theming & customization">',
        '<meta name="theme-color" content="#e11d48">',
    ],
)

# Add more assets programmatically
ui.add_head_tag('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')


# ── Callbacks ────────────────────────────────────────────────────────────


async def apply_preset(ctx: Context, theme: str = "", **kwargs):
    """Apply a theme preset by name."""
    print(f"Applying preset: {theme}, {kwargs}")
    theme_obj = PRESETS.get(theme)
    if theme_obj is None:
        await ctx.show_toast(f"Unknown theme: {theme}", variant="error")
        return

    await ctx.set_theme(theme_obj)
    ctx.state.set("current_theme", theme)
    await ctx.refresh("/")
    await ctx.show_toast(f"Theme switched to {theme}", variant="success")


async def apply_custom_primary(ctx: Context, custom_primary: str = "", **kwargs):
    """Build a quick theme with a user-supplied primary HSL value."""
    custom_primary = custom_primary.strip()
    if not custom_primary:
        await ctx.show_toast("Enter an HSL value like  262 83% 58%", variant="warning")
        return

    theme = Theme(
        light=ThemeColors(primary=custom_primary, ring=custom_primary),
        dark=ThemeColors(primary=custom_primary, ring=custom_primary),
    )
    await ctx.set_theme(theme)
    ctx.state.set("current_theme", f"Custom ({custom_primary})")
    await ctx.refresh("/")
    await ctx.show_toast(f"Primary colour set to: {custom_primary}", variant="success")


# ── Page ─────────────────────────────────────────────────────────────────


@ui.page("/")
def home(ctx: Context):
    current = ctx.state.get("current_theme", "Rose")

    return Container(
        class_name="theme-showcase-gradient min-h-screen",
        children=[
            Container(
                class_name="max-w-4xl mx-auto py-10 px-4",
                children=[
                    # ── Header ─────────────────────────────────────
                    Row(
                        justify="between",
                        align="center",
                        class_name="mb-8",
                        children=[
                            Column(
                                children=[
                                    Heading(
                                        text="🎨 Theme Showcase",
                                        level=1,
                                        class_name="text-4xl font-bold tracking-tight",
                                    ),
                                    Text(
                                        "Demonstrates Refast theming, custom CSS, custom JS, and head tag injection.",
                                        class_name="text-muted-foreground mt-1",
                                    ),
                                ]
                            ),
                            ThemeSwitcher(mode="dropdown"),
                        ],
                    ),
                    # ── Current theme badge ────────────────────────
                    Row(
                        gap=2,
                        align="center",
                        class_name="mb-6",
                        children=[
                            Text("Active theme:", class_name="text-sm text-muted-foreground"),
                            Badge(current, variant="default"),
                        ],
                    ),
                    # ── Preset selector ────────────────────────────
                    Card(
                        class_name="mb-6",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Switch Theme Preset"),
                                    CardDescription(
                                        "Pick a built-in preset. The theme is applied at runtime "
                                        "via WebSocket — no page reload needed."
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Row(
                                        gap=2,
                                        class_name="flex-wrap",
                                        children=[
                                            Button(
                                                name,
                                                variant="outline" if name != current else "primary",
                                                size="sm",
                                                on_click=ctx.callback(apply_preset, theme=name),
                                            )
                                            for name in PRESETS
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                    # ── Custom primary colour ──────────────────────
                    Card(
                        class_name="mb-6",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Custom Primary Colour"),
                                    CardDescription(
                                        "Enter an HSL triplet (e.g. 262 83% 58%) and hit Apply. "
                                        "This builds a Theme on-the-fly."
                                    ),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Row(
                                        gap=2,
                                        align="end",
                                        children=[
                                            Column(
                                                class_name="flex-1",
                                                children=[
                                                    Input(
                                                        name="custom_primary",
                                                        placeholder="262 83% 58%",
                                                        on_change=ctx.callback(
                                                            store_as="custom_primary"
                                                        ),
                                                    ),
                                                ],
                                            ),
                                            Button(
                                                "Apply",
                                                on_click=ctx.callback(
                                                    apply_custom_primary,
                                                    props=["custom_primary"],
                                                ),
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                    ),
                    Separator(class_name="my-6"),
                    # ── Colour swatches ────────────────────────────
                    Heading(
                        text="Semantic Colour Tokens",
                        level=2,
                        class_name="text-2xl font-semibold mb-4",
                    ),
                    Text(
                        "These swatches update live when you switch themes.",
                        class_name="text-muted-foreground mb-4",
                    ),
                    _color_swatches(),
                    Separator(class_name="my-6"),
                    # ── Component preview ──────────────────────────
                    Heading(
                        text="Component Preview", level=2, class_name="text-2xl font-semibold mb-4"
                    ),
                    Text(
                        "Standard components styled by the active theme.",
                        class_name="text-muted-foreground mb-4",
                    ),
                    _component_preview(ctx),
                    Separator(class_name="my-6"),
                    # ── What's injected ────────────────────────────
                    Heading(
                        text="What's in the HTML", level=2, class_name="text-2xl font-semibold mb-4"
                    ),
                    _injection_info(),
                ],
            ),
        ],
    )


# ── Helpers ──────────────────────────────────────────────────────────────


def _swatch(label: str, bg_class: str, fg_class: str) -> Column:
    """A single colour swatch."""
    return Column(
        class_name=f"swatch {bg_class} {fg_class} rounded-lg p-3 border border-border",
        children=[
            Text(label, class_name="text-xs font-mono font-semibold"),
        ],
    )


def _color_swatches() -> Row:
    """Grid of semantic colour swatches."""
    swatches = [
        ("background", "bg-background", "text-foreground"),
        ("primary", "bg-primary", "text-primary-foreground"),
        ("secondary", "bg-secondary", "text-secondary-foreground"),
        ("muted", "bg-muted", "text-muted-foreground"),
        ("accent", "bg-accent", "text-accent-foreground"),
        ("destructive", "bg-destructive", "text-destructive-foreground"),
        ("card", "bg-card", "text-card-foreground"),
        ("border", "bg-border", "text-foreground"),
    ]
    return Row(
        gap=3,
        class_name="flex-wrap mb-4",
        children=[_swatch(label, bg, fg) for label, bg, fg in swatches],
    )


def _component_preview(ctx: Context) -> Column:
    """A set of themed components for visual confirmation."""
    return Column(
        gap=4,
        children=[
            Row(
                gap=2,
                class_name="flex-wrap",
                children=[
                    Button("Primary", variant="primary"),
                    Button("Secondary", variant="secondary"),
                    Button("Outline", variant="outline"),
                    Button("Ghost", variant="ghost"),
                    Button("Destructive", variant="destructive"),
                ],
            ),
            Row(
                gap=2,
                class_name="flex-wrap",
                children=[
                    Badge("Badge", variant="default"),
                    Badge("Secondary", variant="secondary"),
                    Badge("Outline", variant="outline"),
                    Badge("Destructive", variant="destructive"),
                ],
            ),
            Row(
                gap=4,
                class_name="flex-wrap",
                children=[
                    Alert(
                        title="Heads up!",
                        description="This alert inherits the current theme colours.",
                        class_name="flex-1 min-w-[200px]",
                    ),
                    Card(
                        class_name="flex-1 min-w-[200px]",
                        children=[
                            CardHeader(
                                children=[
                                    CardTitle("Card Title"),
                                    CardDescription("Card description inherits muted-foreground."),
                                ]
                            ),
                            CardContent(
                                children=[
                                    Text("Card body text uses the foreground colour."),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _injection_info() -> Column:
    """Describes what extra HTML was injected."""
    items = [
        "✅  Theme CSS variables — <style data-refast-theme> block in <head>",
        '✅  Favicon — <link rel="icon"> pointing to an emoji favicon',
        "✅  Custom CSS — inline <style> with .theme-showcase-gradient and .swatch hover effect",
        "✅  Custom JS — console.log() runs on page load (check DevTools)",
        '✅  Head tags — <meta name="description"> and <meta name="theme-color">',
        '✅  Programmatic — <link rel="preconnect"> added via ui.add_head_tag()',
    ]
    return Column(
        gap=2,
        children=[Text(item, class_name="text-sm text-muted-foreground") for item in items],
    )


# ── Mount ────────────────────────────────────────────────────────────────

app = FastAPI(title="Theme Showcase")
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
