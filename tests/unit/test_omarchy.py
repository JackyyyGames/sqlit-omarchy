from pathlib import Path

from sqlit.domains.shell.app import omarchy


def _activate_theme(monkeypatch, tmp_path: Path, colors: str) -> None:
    theme_dir = tmp_path / "my-omarchy-theme"
    theme_dir.mkdir()
    (theme_dir / "colors.toml").write_text(colors, encoding="utf-8")
    current = tmp_path / "current-theme"
    current.symlink_to(theme_dir, target_is_directory=True)
    monkeypatch.setattr(omarchy, "OMARCHY_CURRENT_THEME", current)
    monkeypatch.setattr(omarchy, "OMARCHY_CURRENT_THEME_NAME", tmp_path / "theme.name")


def test_build_omarchy_theme_uses_colors_toml(monkeypatch, tmp_path):
    _activate_theme(
        monkeypatch,
        tmp_path,
        """
mode = "light"
accent = "#123456"
background = "#fafafa"
foreground = "#111111"
selection = "#dddddd"
muted = "#999999"
red = "#aa0000"
yellow = "#bb8800"
green = "#008800"
blue = "#0000aa"
""",
    )

    theme = omarchy.build_omarchy_theme()

    assert theme is not None
    assert theme.name == "omarchy-auto"
    assert theme.dark is False
    assert theme.primary == "#123456"
    assert theme.background == "#fafafa"
    assert theme.variables["footer-key-foreground"] == "#123456"


def test_unknown_omarchy_theme_is_auto_generated(monkeypatch, tmp_path):
    _activate_theme(monkeypatch, tmp_path, 'mode = "dark"\naccent = "#abcdef"\n')

    assert omarchy.get_matching_textual_theme({"sqlit", "rose-pine", "omarchy-auto"}) == "omarchy-auto"


def test_missing_colors_falls_back_to_default(monkeypatch, tmp_path):
    theme_dir = tmp_path / "without-colors"
    theme_dir.mkdir()
    current = tmp_path / "current-theme"
    current.symlink_to(theme_dir, target_is_directory=True)
    monkeypatch.setattr(omarchy, "OMARCHY_CURRENT_THEME", current)
    monkeypatch.setattr(omarchy, "OMARCHY_CURRENT_THEME_NAME", tmp_path / "theme.name")

    assert omarchy.build_omarchy_theme() is None
    assert omarchy.get_matching_textual_theme({"rose-pine"}) == "rose-pine"
