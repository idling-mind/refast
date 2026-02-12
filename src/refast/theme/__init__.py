"""Theme module for Refast theming and customization."""

from refast.theme.presets import (
    THEMES,
    amber_minimal_theme,
    amethyst_haze_theme,
    bubblegum_theme,
    caffine_theme,
    catppuccin_theme,
    default_theme,
    ocean_breeze_theme,
    twitter_theme,
)
from refast.theme.theme import Theme, ThemeColors, ThemeMode

__all__ = [
    "Theme",
    "ThemeColors",
    "ThemeMode",
    "THEMES",
    "default_theme",
    "amethyst_haze_theme",
    "amber_minimal_theme",
    "bubblegum_theme",
    "caffine_theme",
    "catppuccin_theme",
    "twitter_theme",
    "ocean_breeze_theme",
]
