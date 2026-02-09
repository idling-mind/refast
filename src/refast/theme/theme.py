"""Theme configuration model for Refast.

Defines the Theme class and supporting types for theming Refast applications.
Theme colors are expressed as HSL triplets (e.g. "221.2 83.2% 53.3%") matching
the shadcn/ui CSS variable convention used in the frontend.

Example:
    ```python
    from refast.theme import Theme, ThemeColors

    my_theme = Theme(
        light=ThemeColors(primary="262.1 83.3% 57.8%"),
        dark=ThemeColors(primary="263.4 70% 50.4%"),
        font_family="Inter, sans-serif",
        radius="0.75rem",
    )

    ui = RefastApp(title="My App", theme=my_theme)
    ```
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ThemeMode(StrEnum):
    """Available theme modes."""

    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class ThemeColors(BaseModel):
    """
    Semantic color tokens for a single theme mode.

    Each value is an HSL triplet string like ``"221.2 83.2% 53.3%"``
    (without the ``hsl()`` wrapper) — the format consumed by
    ``hsl(var(--primary))`` in the frontend CSS.

    Only non-``None`` values will be emitted as CSS variable overrides,
    so you can override just the tokens you need.
    """

    background: str | None = None
    foreground: str | None = None
    card: str | None = None
    card_foreground: str | None = Field(None, alias="card-foreground")
    popover: str | None = None
    popover_foreground: str | None = Field(None, alias="popover-foreground")
    primary: str | None = None
    primary_foreground: str | None = Field(None, alias="primary-foreground")
    secondary: str | None = None
    secondary_foreground: str | None = Field(None, alias="secondary-foreground")
    muted: str | None = None
    muted_foreground: str | None = Field(None, alias="muted-foreground")
    accent: str | None = None
    accent_foreground: str | None = Field(None, alias="accent-foreground")
    destructive: str | None = None
    destructive_foreground: str | None = Field(None, alias="destructive-foreground")
    success: str | None = None
    success_foreground: str | None = Field(None, alias="success-foreground")
    warning: str | None = None
    warning_foreground: str | None = Field(None, alias="warning-foreground")
    info: str | None = None
    info_foreground: str | None = Field(None, alias="info-foreground")
    border: str | None = None
    input: str | None = None
    ring: str | None = None
    chart_1: str | None = Field(None, alias="chart-1")
    chart_2: str | None = Field(None, alias="chart-2")
    chart_3: str | None = Field(None, alias="chart-3")
    chart_4: str | None = Field(None, alias="chart-4")
    chart_5: str | None = Field(None, alias="chart-5")
    chart_6: str | None = Field(None, alias="chart-6")
    chart_7: str | None = Field(None, alias="chart-7")
    chart_8: str | None = Field(None, alias="chart-8")
    sidebar_background: str | None = Field(None, alias="sidebar-background")
    sidebar_foreground: str | None = Field(None, alias="sidebar-foreground")
    sidebar_primary: str | None = Field(None, alias="sidebar-primary")
    sidebar_primary_foreground: str | None = Field(None, alias="sidebar-primary-foreground")
    sidebar_accent: str | None = Field(None, alias="sidebar-accent")
    sidebar_accent_foreground: str | None = Field(None, alias="sidebar-accent-foreground")
    sidebar_border: str | None = Field(None, alias="sidebar-border")
    sidebar_ring: str | None = Field(None, alias="sidebar-ring")

    model_config = {"populate_by_name": True}

    def to_css_vars(self) -> dict[str, str]:
        """
        Return a mapping of CSS variable names to values.

        Only non-``None`` fields are included.

        Returns:
            Dict mapping ``"--primary"`` style keys to HSL triplet values.
        """
        result: dict[str, str] = {}
        for field_name, field_info in self.__class__.model_fields.items():
            value = getattr(self, field_name)
            if value is None:
                continue
            # Use the alias (with dashes) if available, otherwise convert underscores
            css_name = field_info.alias if field_info.alias else field_name.replace("_", "-")
            result[f"--{css_name}"] = value
        return result


class Theme(BaseModel):
    """
    Complete theme configuration for a Refast application.

    A theme consists of light-mode and dark-mode color palettes plus
    global design tokens (``font_family``, ``radius``).

    Example:
        ```python
        from refast.theme import Theme, ThemeColors

        theme = Theme(
            light=ThemeColors(primary="221.2 83.2% 53.3%"),
            dark=ThemeColors(primary="217.2 91.2% 59.8%"),
            font_family="Inter, sans-serif",
            radius="0.75rem",
        )
        ```
    """

    light: ThemeColors = Field(default_factory=ThemeColors)
    dark: ThemeColors = Field(default_factory=ThemeColors)
    font_family: str | None = None
    radius: str | None = None
    default_mode: ThemeMode = ThemeMode.LIGHT

    def to_css_variables(self) -> str:
        """
        Generate a ``<style>`` block containing CSS variable overrides.

        Produces ``:root { … }`` and ``.dark { … }`` blocks that layer
        on top of the defaults shipped in the client CSS bundle.

        Returns:
            A string of CSS (without ``<style>`` tags) ready for embedding.
        """
        lines: list[str] = []

        # Light mode overrides → :root
        light_vars = self.light.to_css_vars()
        if self.radius is not None:
            light_vars["--radius"] = self.radius
        if light_vars:
            lines.append(":root {")
            for var, val in light_vars.items():
                lines.append(f"  {var}: {val};")
            lines.append("}")

        # Dark mode overrides → .dark
        dark_vars = self.dark.to_css_vars()
        if self.radius is not None and "--radius" not in dark_vars:
            dark_vars["--radius"] = self.radius
        if dark_vars:
            lines.append(".dark {")
            for var, val in dark_vars.items():
                lines.append(f"  {var}: {val};")
            lines.append("}")

        # Font family → body override
        if self.font_family is not None:
            lines.append(f"body {{ font-family: {self.font_family}; }}")

        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize theme to a dict suitable for JSON transport (runtime updates).

        Returns:
            Dict with ``light``, ``dark``, ``font_family``, ``radius``, ``default_mode``.
        """
        return {
            "light": self.light.to_css_vars(),
            "dark": self.dark.to_css_vars(),
            "fontFamily": self.font_family,
            "radius": self.radius,
            "defaultMode": self.default_mode.value,
        }
