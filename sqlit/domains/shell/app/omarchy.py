"""Omarchy theme integration for sqlit.

Provides automatic theme synchronization with Omarchy's theme system.
Only activates when Omarchy is detected on the system.

Theme matching strategy:
1. Read the current Omarchy theme from its state directory
2. Load the active colors.toml palette
3. Fall back to the default "rose-pine" theme when Omarchy is unavailable
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib

from textual.theme import Theme

# Omarchy paths. Newer Omarchy versions keep the active theme in state;
# retain the config path for older installations.
OMARCHY_CURRENT_THEME = Path.home() / ".local" / "state" / "omarchy" / "current" / "theme"
OMARCHY_CURRENT_THEME_NAME = Path.home() / ".local" / "state" / "omarchy" / "current" / "theme.name"
OMARCHY_LEGACY_CURRENT_THEME = Path.home() / ".config" / "omarchy" / "current" / "theme"

# Default theme when no Omarchy match is found
DEFAULT_THEME = "rose-pine"
OMARCHY_THEME_NAME = "omarchy-auto"

# Mapping from Omarchy theme names to Textual theme names
# Only needed when names don't match exactly
THEME_ALIASES: dict[str, str] = {
    # Omarchy "catppuccin" is the dark variant (mocha)
    "catppuccin": "catppuccin-mocha",
    # Flexoki light variant
    "flexoki-light": "flexoki",
    # Handle space/underscore variations in omarchy theme names
    "matte black": "matte-black",
    "matte_black": "matte-black",
    "osaka jade": "osaka-jade",
    "osaka_jade": "osaka-jade",
    # Ethereal doesn't have an exact match, use rose-pine as closest
    "ethereal": "rose-pine",
}


def is_omarchy_installed() -> bool:
    """Check if Omarchy exposes an active theme directory."""
    return get_current_theme_path() is not None


def get_current_theme_path() -> Path | None:
    """Get the path to the current Omarchy theme directory.

    Returns:
        Path to the current theme directory, or None if not available.
    """
    for theme_path in (OMARCHY_CURRENT_THEME, OMARCHY_LEGACY_CURRENT_THEME):
        if not theme_path.exists():
            continue
        try:
            return theme_path.resolve()
        except OSError:
            continue
    return None


def get_current_theme_name() -> str | None:
    """Get the name of the current Omarchy theme.

    Returns:
        Theme name (directory name), or None if not available.
    """
    try:
        theme_name = OMARCHY_CURRENT_THEME_NAME.read_text(encoding="utf-8").strip()
    except OSError:
        theme_name = ""
    if theme_name and "/" not in theme_name and theme_name not in {".", ".."}:
        return theme_name

    theme_path = get_current_theme_path()
    if theme_path is None:
        return None
    return theme_path.name


def load_current_theme_colors() -> dict[str, Any] | None:
    """Load the active Omarchy palette from its colors.toml file."""
    theme_path = get_current_theme_path()
    if theme_path is None:
        return None

    colors_path = theme_path / "colors.toml"
    try:
        with colors_path.open("rb") as colors_file:
            payload = tomllib.load(colors_file)
    except (OSError, tomllib.TOMLDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def build_omarchy_theme() -> Theme | None:
    """Create a Textual theme from the active Omarchy colors.toml palette."""
    colors = load_current_theme_colors()
    if not colors:
        return None

    def color(key: str, fallback: str) -> str:
        value = colors.get(key, fallback)
        return value if isinstance(value, str) and value.strip() else fallback

    dark = colors.get("mode", "dark") != "light"
    background = color("background", "#1A1B26")
    foreground = color("foreground", "#D8DEE9")
    accent = color("accent", color("blue", "#81A1C1"))
    surface = color("lighter_background", color("dark_background", background))
    panel = color("selection", color("muted", surface))

    return Theme(
        name=OMARCHY_THEME_NAME,
        primary=accent,
        secondary=color("blue", accent),
        accent=accent,
        warning=color("yellow", "#EBCB8B"),
        error=color("red", "#BF616A"),
        success=color("green", "#A3BE8C"),
        foreground=foreground,
        background=background,
        surface=surface,
        panel=panel,
        dark=dark,
        variables={
            "border": color("muted", panel),
            "footer-background": surface,
            "footer-key-foreground": accent,
            "button-color-foreground": background,
            "input-selection-background": f"{color('selection', accent)} 60%",
            "mode-normal-color": color("accent", accent),
            "mode-insert-color": color("green", accent),
        },
    )


def get_matching_textual_theme(available_themes: set[str]) -> str:
    """Get a Textual theme that matches the current Omarchy theme.

    Args:
        available_themes: Set of available Textual theme names.

    Returns:
        The matching Textual theme name, or DEFAULT_THEME if no match.
    """
    omarchy_theme = get_current_theme_name()
    if omarchy_theme is None:
        return DEFAULT_THEME

    # Prefer the active palette, even when the theme happens to share a name
    # with a built-in Textual theme. This also respects user theme overlays.
    if load_current_theme_colors() is not None:
        return OMARCHY_THEME_NAME

    # Normalize to lowercase for matching
    omarchy_lower = omarchy_theme.lower()

    # Check for exact match first
    if omarchy_lower in available_themes:
        return omarchy_lower

    # Check aliases
    if omarchy_lower in THEME_ALIASES:
        alias = THEME_ALIASES[omarchy_lower]
        if alias in available_themes:
            return alias

    return DEFAULT_THEME
