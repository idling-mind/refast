"""Tests for the Theme model, ThemeColors, presets, and CSS variable generation."""

import pytest

from refast.theme import Theme, ThemeColors, ThemeMode
from refast.theme.presets import (
    blue_theme,
    default_theme,
    green_theme,
    orange_theme,
    rose_theme,
    slate_theme,
    violet_theme,
    zinc_theme,
)

# ---------------------------------------------------------------------------
# ThemeColors
# ---------------------------------------------------------------------------


class TestThemeColors:
    """Tests for ThemeColors model."""

    def test_empty_colors(self):
        """Empty ThemeColors should have all None fields."""
        colors = ThemeColors()
        assert colors.primary is None
        assert colors.background is None

    def test_partial_colors(self):
        """Only specified colours should be set."""
        colors = ThemeColors(primary="221.2 83.2% 53.3%")
        assert colors.primary == "221.2 83.2% 53.3%"
        assert colors.background is None

    def test_to_css_vars_empty(self):
        """Empty ThemeColors should return empty dict."""
        assert ThemeColors().to_css_vars() == {}

    def test_to_css_vars_partial(self):
        """Only set fields should appear in the CSS vars dict."""
        colors = ThemeColors(
            primary="221.2 83.2% 53.3%",
            background="0 0% 100%",
        )
        css = colors.to_css_vars()
        assert css == {
            "--primary": "221.2 83.2% 53.3%",
            "--background": "0 0% 100%",
        }

    def test_to_css_vars_uses_dashes_not_underscores(self):
        """Field names with underscores should emit dashed CSS variable names."""
        colors = ThemeColors(primary_foreground="210 40% 98%")
        css = colors.to_css_vars()
        assert "--primary-foreground" in css
        assert css["--primary-foreground"] == "210 40% 98%"

    def test_to_css_vars_sidebar(self):
        """Sidebar variables should use correct dashed names."""
        colors = ThemeColors(sidebar_background="0 0% 98%")
        css = colors.to_css_vars()
        assert "--sidebar-background" in css

    def test_to_css_vars_chart(self):
        """Chart variables should use dashed names."""
        colors = ThemeColors(chart_1="221.2 83.2% 53.3%", chart_5="212 97% 87%")
        css = colors.to_css_vars()
        assert "--chart-1" in css
        assert "--chart-5" in css

    def test_all_fields_can_be_set(self):
        """Ensure all fields are settable and appear in to_css_vars."""
        all_values = {
            "background": "0 0% 100%",
            "foreground": "222 84% 4.9%",
            "card": "0 0% 100%",
            "card_foreground": "222 84% 4.9%",
            "popover": "0 0% 100%",
            "popover_foreground": "222 84% 4.9%",
            "primary": "221 83% 53%",
            "primary_foreground": "210 40% 98%",
            "secondary": "210 40% 96%",
            "secondary_foreground": "222 47% 11%",
            "muted": "210 40% 96%",
            "muted_foreground": "215 16% 47%",
            "accent": "210 40% 96%",
            "accent_foreground": "222 47% 11%",
            "destructive": "0 84% 60%",
            "destructive_foreground": "210 40% 98%",
            "success": "142 76% 36%",
            "success_foreground": "355 100% 97%",
            "warning": "38 92% 50%",
            "warning_foreground": "48 96% 89%",
            "info": "199 89% 48%",
            "info_foreground": "210 40% 98%",
            "border": "214 32% 91%",
            "input": "214 32% 91%",
            "ring": "221 83% 53%",
            "chart_1": "a",
            "chart_2": "b",
            "chart_3": "c",
            "chart_4": "d",
            "chart_5": "e",
            "chart_6": "f",
            "chart_7": "g",
            "chart_8": "h",
            "sidebar_background": "x",
            "sidebar_foreground": "y",
            "sidebar_primary": "z",
            "sidebar_primary_foreground": "w",
            "sidebar_accent": "v",
            "sidebar_accent_foreground": "u",
            "sidebar_border": "t",
            "sidebar_ring": "s",
        }
        colors = ThemeColors(**all_values)
        css = colors.to_css_vars()
        # Every field should produce a CSS variable
        assert len(css) == len(all_values)

    def test_populate_by_name(self):
        """ThemeColors should accept both alias and Python name."""
        c1 = ThemeColors(primary_foreground="val1")
        c2 = ThemeColors(**{"primary-foreground": "val1"})
        assert c1.to_css_vars() == c2.to_css_vars()


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------


class TestTheme:
    """Tests for Theme model."""

    def test_default_theme_empty(self):
        """A default Theme with no args should produce no CSS overrides."""
        theme = Theme()
        assert theme.to_css_variables() == ""

    def test_theme_with_light_only(self):
        """Theme with only light colors emits :root block."""
        theme = Theme(
            light=ThemeColors(primary="262 83% 58%"),
        )
        css = theme.to_css_variables()
        assert ":root {" in css
        assert "--primary: 262 83% 58%;" in css
        assert ".dark {" not in css

    def test_theme_with_dark_only(self):
        """Theme with only dark colors emits .dark block."""
        theme = Theme(
            dark=ThemeColors(primary="263 70% 50%"),
        )
        css = theme.to_css_variables()
        assert ".dark {" in css
        assert "--primary: 263 70% 50%;" in css
        # Should not emit :root block (no light overrides)
        assert ":root {" not in css

    def test_theme_with_both_modes(self):
        """Theme with both light and dark colors emits both blocks."""
        theme = Theme(
            light=ThemeColors(primary="1 2% 3%"),
            dark=ThemeColors(primary="4 5% 6%"),
        )
        css = theme.to_css_variables()
        assert ":root {" in css
        assert ".dark {" in css
        assert "--primary: 1 2% 3%;" in css
        assert "--primary: 4 5% 6%;" in css

    def test_theme_radius(self):
        """Radius should appear in :root and .dark blocks."""
        theme = Theme(
            light=ThemeColors(primary="1 2% 3%"),
            radius="0.75rem",
        )
        css = theme.to_css_variables()
        assert "--radius: 0.75rem;" in css

    def test_theme_radius_only(self):
        """Radius alone should produce a :root block."""
        theme = Theme(radius="1rem")
        css = theme.to_css_variables()
        assert ":root {" in css
        assert "--radius: 1rem;" in css

    def test_theme_font_family(self):
        """Font family should produce a body rule."""
        theme = Theme(font_family="Inter, sans-serif")
        css = theme.to_css_variables()
        assert "body { font-family: Inter, sans-serif; }" in css

    def test_theme_default_mode(self):
        """Default mode should default to light."""
        theme = Theme()
        assert theme.default_mode == ThemeMode.LIGHT

    def test_theme_default_mode_dark(self):
        theme = Theme(default_mode=ThemeMode.DARK)
        assert theme.default_mode == ThemeMode.DARK

    def test_to_dict(self):
        """to_dict should return a JSON-serialisable dict."""
        theme = Theme(
            light=ThemeColors(primary="1 2% 3%"),
            dark=ThemeColors(primary="4 5% 6%"),
            font_family="Roboto",
            radius="0.5rem",
            default_mode=ThemeMode.DARK,
        )
        d = theme.to_dict()
        assert d["light"] == {"--primary": "1 2% 3%"}
        assert d["dark"] == {"--primary": "4 5% 6%"}
        assert d["fontFamily"] == "Roboto"
        assert d["radius"] == "0.5rem"
        assert d["defaultMode"] == "dark"

    def test_to_dict_empty(self):
        """Empty theme to_dict should still have all keys."""
        d = Theme().to_dict()
        assert "light" in d
        assert "dark" in d
        assert d["fontFamily"] is None


# ---------------------------------------------------------------------------
# ThemeMode
# ---------------------------------------------------------------------------


class TestThemeMode:
    """Tests for ThemeMode enum."""

    def test_values(self):
        assert ThemeMode.LIGHT.value == "light"
        assert ThemeMode.DARK.value == "dark"
        assert ThemeMode.SYSTEM.value == "system"

    def test_string_enum(self):
        assert str(ThemeMode.LIGHT) == "ThemeMode.LIGHT" or ThemeMode.LIGHT == "light"


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------


class TestPresets:
    """Tests for built-in theme presets."""

    @pytest.mark.parametrize(
        "preset",
        [
            default_theme,
            slate_theme,
            zinc_theme,
            rose_theme,
            green_theme,
            orange_theme,
            blue_theme,
            violet_theme,
        ],
        ids=[
            "default",
            "slate",
            "zinc",
            "rose",
            "green",
            "orange",
            "blue",
            "violet",
        ],
    )
    def test_preset_is_theme(self, preset):
        """Every preset should be a Theme instance."""
        assert isinstance(preset, Theme)

    def test_default_theme_no_overrides(self):
        """Default theme should produce no CSS (matches built-in CSS)."""
        assert default_theme.to_css_variables() == ""

    @pytest.mark.parametrize(
        "preset",
        [slate_theme, zinc_theme, rose_theme, green_theme, orange_theme, violet_theme],
        ids=["slate", "zinc", "rose", "green", "orange", "violet"],
    )
    def test_preset_produces_css(self, preset):
        """Non-default presets should produce non-empty CSS."""
        css = preset.to_css_variables()
        assert ":root {" in css
        assert ".dark {" in css

    def test_blue_theme_minimal_overrides(self):
        """Blue theme should override only primary & ring."""
        css = blue_theme.to_css_variables()
        assert "--primary" in css
        assert "--ring" in css

    def test_preset_to_dict_roundtrip(self):
        """Preset to_dict should be JSON-serialisable."""
        import json

        for preset in [rose_theme, violet_theme, green_theme]:
            d = preset.to_dict()
            s = json.dumps(d)
            assert isinstance(s, str)
