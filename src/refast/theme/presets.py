"""Built-in theme presets for Refast.

Each preset is a ``Theme`` instance with carefully chosen colors for both
light and dark modes. Use them directly or as starting points for custom
themes.

Example:
    ```python
    from refast import RefastApp
    from refast.theme import rose_theme

    ui = RefastApp(title="My App", theme=rose_theme)
    ```
"""

from refast.theme.theme import Theme, ThemeColors


# ---------------------------------------------------------------------------
# Default theme – the built-in shadcn/ui blue palette (matches index.css)
# No overrides needed since it matches the CSS bundle defaults.
# ---------------------------------------------------------------------------

default_theme = Theme()

# ---------------------------------------------------------------------------
# Slate theme – neutral gray palette
# ---------------------------------------------------------------------------

slate_theme = Theme(
    light=ThemeColors(
        background="0 0% 100%",
        foreground="222.2 84% 4.9%",
        primary="215.4 16.3% 46.9%",
        primary_foreground="210 40% 98%",
        secondary="210 40% 96.1%",
        secondary_foreground="222.2 47.4% 11.2%",
        muted="210 40% 96.1%",
        muted_foreground="215.4 16.3% 46.9%",
        accent="210 40% 96.1%",
        accent_foreground="222.2 47.4% 11.2%",
        border="214.3 31.8% 91.4%",
        ring="215.4 16.3% 46.9%",
    ),
    dark=ThemeColors(
        background="222.2 84% 4.9%",
        foreground="210 40% 98%",
        primary="215 20.2% 65.1%",
        primary_foreground="222.2 47.4% 11.2%",
        secondary="217.2 32.6% 17.5%",
        secondary_foreground="210 40% 98%",
        muted="217.2 32.6% 17.5%",
        muted_foreground="215 20.2% 65.1%",
        accent="217.2 32.6% 17.5%",
        accent_foreground="210 40% 98%",
        border="217.2 32.6% 17.5%",
        ring="215 20.2% 65.1%",
    ),
)

# ---------------------------------------------------------------------------
# Zinc theme – cool neutral palette
# ---------------------------------------------------------------------------

zinc_theme = Theme(
    light=ThemeColors(
        background="0 0% 100%",
        foreground="240 10% 3.9%",
        primary="240 5.9% 10%",
        primary_foreground="0 0% 98%",
        secondary="240 4.8% 95.9%",
        secondary_foreground="240 5.9% 10%",
        muted="240 4.8% 95.9%",
        muted_foreground="240 3.8% 46.1%",
        accent="240 4.8% 95.9%",
        accent_foreground="240 5.9% 10%",
        border="240 5.9% 90%",
        ring="240 5.9% 10%",
    ),
    dark=ThemeColors(
        background="240 10% 3.9%",
        foreground="0 0% 98%",
        primary="0 0% 98%",
        primary_foreground="240 5.9% 10%",
        secondary="240 3.7% 15.9%",
        secondary_foreground="0 0% 98%",
        muted="240 3.7% 15.9%",
        muted_foreground="240 5% 64.9%",
        accent="240 3.7% 15.9%",
        accent_foreground="0 0% 98%",
        border="240 3.7% 15.9%",
        ring="240 4.9% 83.9%",
    ),
)

# ---------------------------------------------------------------------------
# Rose theme – warm pink / rose accent
# ---------------------------------------------------------------------------

rose_theme = Theme(
    light=ThemeColors(
        background="0 0% 100%",
        foreground="240 10% 3.9%",
        primary="346.8 77.2% 49.8%",
        primary_foreground="355.7 100% 97.3%",
        secondary="240 4.8% 95.9%",
        secondary_foreground="240 5.9% 10%",
        muted="240 4.8% 95.9%",
        muted_foreground="240 3.8% 46.1%",
        accent="240 4.8% 95.9%",
        accent_foreground="240 5.9% 10%",
        destructive="0 84.2% 60.2%",
        border="240 5.9% 90%",
        ring="346.8 77.2% 49.8%",
    ),
    dark=ThemeColors(
        background="20 14.3% 4.1%",
        foreground="0 0% 95%",
        primary="346.8 77.2% 49.8%",
        primary_foreground="355.7 100% 97.3%",
        secondary="240 3.7% 15.9%",
        secondary_foreground="0 0% 98%",
        muted="0 0% 15%",
        muted_foreground="240 5% 64.9%",
        accent="12 6.5% 15.1%",
        accent_foreground="0 0% 98%",
        destructive="0 62.8% 30.6%",
        border="240 3.7% 15.9%",
        ring="346.8 77.2% 49.8%",
    ),
)

# ---------------------------------------------------------------------------
# Green theme – nature / success green accent
# ---------------------------------------------------------------------------

green_theme = Theme(
    light=ThemeColors(
        background="0 0% 100%",
        foreground="240 10% 3.9%",
        primary="142.1 76.2% 36.3%",
        primary_foreground="355.7 100% 97.3%",
        secondary="240 4.8% 95.9%",
        secondary_foreground="240 5.9% 10%",
        muted="240 4.8% 95.9%",
        muted_foreground="240 3.8% 46.1%",
        accent="240 4.8% 95.9%",
        accent_foreground="240 5.9% 10%",
        border="240 5.9% 90%",
        ring="142.1 76.2% 36.3%",
    ),
    dark=ThemeColors(
        background="20 14.3% 4.1%",
        foreground="0 0% 95%",
        primary="142.1 70.6% 45.3%",
        primary_foreground="144.9 80.4% 10%",
        secondary="240 3.7% 15.9%",
        secondary_foreground="0 0% 98%",
        muted="0 0% 15%",
        muted_foreground="240 5% 64.9%",
        accent="12 6.5% 15.1%",
        accent_foreground="0 0% 98%",
        border="240 3.7% 15.9%",
        ring="142.1 70.6% 45.3%",
    ),
)

# ---------------------------------------------------------------------------
# Orange theme – warm orange accent
# ---------------------------------------------------------------------------

orange_theme = Theme(
    light=ThemeColors(
        background="0 0% 100%",
        foreground="20 14.3% 4.1%",
        primary="24.6 95% 53.1%",
        primary_foreground="60 9.1% 97.8%",
        secondary="60 4.8% 95.9%",
        secondary_foreground="24 9.8% 10%",
        muted="60 4.8% 95.9%",
        muted_foreground="25 5.3% 44.7%",
        accent="60 4.8% 95.9%",
        accent_foreground="24 9.8% 10%",
        border="20 5.9% 90%",
        ring="24.6 95% 53.1%",
    ),
    dark=ThemeColors(
        background="20 14.3% 4.1%",
        foreground="60 9.1% 97.8%",
        primary="20.5 90.2% 48.2%",
        primary_foreground="60 9.1% 97.8%",
        secondary="12 6.5% 15.1%",
        secondary_foreground="60 9.1% 97.8%",
        muted="12 6.5% 15.1%",
        muted_foreground="24 5.4% 63.9%",
        accent="12 6.5% 15.1%",
        accent_foreground="60 9.1% 97.8%",
        border="12 6.5% 15.1%",
        ring="20.5 90.2% 48.2%",
    ),
)

# ---------------------------------------------------------------------------
# Blue theme – explicit blue accent (same as default but specified)
# ---------------------------------------------------------------------------

blue_theme = Theme(
    light=ThemeColors(
        primary="221.2 83.2% 53.3%",
        primary_foreground="210 40% 98%",
        ring="221.2 83.2% 53.3%",
    ),
    dark=ThemeColors(
        primary="217.2 91.2% 59.8%",
        primary_foreground="222.2 47.4% 11.2%",
        ring="224.3 76.3% 48%",
    ),
)

# ---------------------------------------------------------------------------
# Violet theme – purple / violet accent
# ---------------------------------------------------------------------------

violet_theme = Theme(
    light=ThemeColors(
        background="0 0% 100%",
        foreground="224 71.4% 4.1%",
        primary="262.1 83.3% 57.8%",
        primary_foreground="210 20% 98%",
        secondary="220 14.3% 95.9%",
        secondary_foreground="220.9 39.3% 11%",
        muted="220 14.3% 95.9%",
        muted_foreground="220 8.9% 46.1%",
        accent="220 14.3% 95.9%",
        accent_foreground="220.9 39.3% 11%",
        border="220 13% 91%",
        ring="262.1 83.3% 57.8%",
    ),
    dark=ThemeColors(
        background="224 71.4% 4.1%",
        foreground="210 20% 98%",
        primary="263.4 70% 50.4%",
        primary_foreground="210 20% 98%",
        secondary="215 27.9% 16.9%",
        secondary_foreground="210 20% 98%",
        muted="215 27.9% 16.9%",
        muted_foreground="217.9 10.6% 64.9%",
        accent="215 27.9% 16.9%",
        accent_foreground="210 20% 98%",
        border="215 27.9% 16.9%",
        ring="263.4 70% 50.4%",
    ),
)
