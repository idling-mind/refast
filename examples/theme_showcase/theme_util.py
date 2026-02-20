"""
Utilities to convert shadcn-style registry JSON into Refast Theme objects.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import httpx

from refast.theme import Theme, ThemeColors


def _normalize_key(key: str) -> str:
    """Convert hyphenated CSS variable names into Python attribute names."""
    return key.replace("-", "_")


def _as_theme_colors(mapping: dict[str, Any]) -> ThemeColors:
    """Convert a mapping (CSS vars section) into a ThemeColors instance."""

    def _convert_value(v: Any) -> Any:
        if isinstance(v, str):
            m = re.match(r"^oklch\(\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s*\)$", v)
            if m:
                l = float(m.group(1))
                c = float(m.group(2))
                h = float(m.group(3))
                return _oklch_to_hsl_str(l, c, h)
        return v

    normalized = {_normalize_key(k): _convert_value(v) for k, v in mapping.items()}
    return ThemeColors(**normalized)


def _oklch_to_hsl_str(l: float, c: float, h_deg: float) -> str:
    """Convert OKLCH (L, C, h) to an HSL string formatted as "h s% l%".

    L and C are expected in the same scale as in the registry (L in 0..1).
    The returned HSL uses degrees for hue and percentages for saturation/lightness
    with 4 decimal places of precision for reproducibility.
    """
    r, g, b = _oklch_to_srgb(l, c, h_deg)
    h, s, light = _rgb_to_hsl(r, g, b)
    return f"{round(h, 4)} {round(s * 100, 4)}% {round(light * 100, 4)}%"


def _oklch_to_srgb(L: float, C: float, h_deg: float) -> tuple[float, float, float]:
    """Convert OKLCH to sRGB (gamma-corrected) in range 0..1.

    Based on the OKLab/OKLCH conversion formulas by Björn Ottosson.
    """
    h_rad = math.radians(h_deg)
    a = C * math.cos(h_rad)
    b = C * math.sin(h_rad)

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_**3
    m = m_**3
    s = s_**3

    r = (+4.0767416621 * l) + (-3.3077115913 * m) + (0.2309699292 * s)
    g = (-1.2684380046 * l) + (2.6097574011 * m) + (-0.3413193965 * s)
    bb = (-0.0041960863 * l) + (-0.7034186147 * m) + (1.7076147010 * s)

    def _linear_to_srgb(c: float) -> float:
        # clamp first to avoid domain errors
        c = max(0.0, min(1.0, c))
        if c <= 0.0031308:
            return 12.92 * c
        return 1.055 * (c ** (1.0 / 2.4)) - 0.055

    return (_linear_to_srgb(r), _linear_to_srgb(g), _linear_to_srgb(bb))


def _rgb_to_hsl(r: float, g: float, b: float) -> tuple[float, float, float]:
    """Convert sRGB r,g,b in 0..1 to HSL (h in degrees, s and l in 0..1)."""
    mx = max(r, g, b)
    mn = min(r, g, b)
    l = (mx + mn) / 2.0
    if mx == mn:
        return 0.0, 0.0, l
    d = mx - mn
    s = d / (1.0 - abs(2.0 * l - 1.0))
    if mx == r:
        h = (g - b) / d % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    h_deg = (h * 60.0) % 360.0
    return h_deg, s, l


def _convert_dict_to_theme(data: dict[str, Any]) -> Theme:
    """Convert parsed registry dict into a Theme instance."""
    css_vars = data.get("cssVars")
    if not css_vars:
        raise ValueError("cssVars missing in registry data")

    theme_tokens = css_vars.get("theme", {})
    light_tokens = css_vars.get("light")
    dark_tokens = css_vars.get("dark")

    if light_tokens is None or dark_tokens is None:
        raise ValueError("Both 'light' and 'dark' sections are required in cssVars")

    light = _as_theme_colors(light_tokens)
    dark = _as_theme_colors(dark_tokens)

    font_family = theme_tokens.get("font-sans") or light_tokens.get("font-sans")
    radius = theme_tokens.get("radius") or light_tokens.get("radius")

    return Theme(light=light, dark=dark, font_family=font_family, radius=radius)


def shadcn_registry_to_theme(source: str | Path | dict[str, Any]) -> Theme:
    """
    Convert a ShadCN registry JSON (path, raw JSON string, or dict) to a Refast Theme.

    This synchronous helper will treat a string that looks like a URL (http/https)
    as raw JSON (use `shadcn_registry_to_theme_from_url` to fetch a URL).
    """
    if isinstance(source, (str, Path)):
        source_path = Path(source)
        if source_path.exists():
            data = json.loads(source_path.read_text(encoding="utf-8"))
        else:
            # treat source as raw JSON string
            data = json.loads(str(source))
    elif isinstance(source, dict):
        data = source
    else:
        raise TypeError("source must be a path, json string, or dict")

    return _convert_dict_to_theme(data)


def shadcn_registry_to_theme_from_url(
    url: str,
    timeout: float = 10.0,
    client: httpx.Client | None = None,
) -> Theme:
    """Fetch a ShadCN registry JSON from a web URL and convert it to a Theme.

    This synchronous helper uses an httpx.Client to perform a blocking GET
    request and convert the returned JSON into a :class:`Theme`.

    Args:
        url: HTTP or HTTPS URL returning the registry JSON.
        timeout: Request timeout in seconds.
        client: Optional httpx.Client for dependency injection (useful in tests).

    Returns:
        Theme instance.

    Raises:
        ValueError: For non-200 responses or missing required sections.
    """
    if not re.match(r"^https?://", url):
        raise ValueError("URL must start with http:// or https://")

    close_client = False
    if client is None:
        client = httpx.Client(timeout=timeout)
        close_client = True

    try:
        resp = client.get(url)
        if resp.status_code != 200:
            raise ValueError(f"Failed to fetch theme JSON: {resp.status_code}")
        data = resp.json()
    finally:
        if close_client:
            client.close()

    return _convert_dict_to_theme(data)
