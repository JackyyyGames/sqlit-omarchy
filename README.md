# sqlit-omarchy

A fast, keyboard-driven SQL TUI for Omarchy. Connect to databases, write SQL,
and explore results directly from your terminal.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- Automatically follows the active Omarchy theme
- Live updates when the Omarchy theme changes
- SQL Server, PostgreSQL, MySQL, SQLite, MariaDB, DuckDB, and many more
- Connection manager, query history, and Vim-style editing
- Syntax highlighting, autocomplete, and large-result filtering
- Docker discovery, SSH tunnels, and secure system-keyring storage

## Installation

Install this fork directly on Omarchy:

```bash
pipx install git+https://github.com/JackyyyGames/sqlit-omarchy.git
```

Alternatively:

```bash
uv tool install git+https://github.com/JackyyyGames/sqlit-omarchy.git
```

Start sqlit:

```bash
sqlit
```

Try it without a real database:

```bash
sqlit --mock=sqlite-demo
```

## Omarchy theme synchronization

sqlit reads the active palette from:

```text
~/.local/state/omarchy/current/theme/colors.toml
```

Background, foreground, accent, status colors, borders, selection, and query
editor colors are synchronized. When you change the theme in Omarchy, sqlit
detects it automatically. No Omarchy files are modified, and no plugin or hook
is required.

Outside Omarchy, the regular theme system remains active. Themes without a
readable `colors.toml` use a safe fallback.

## Reporting issues

If something does not work, open an
[issue](https://github.com/JackyyyGames/sqlit-omarchy/issues) with your Omarchy
version, the theme you are using, and a short description.

## License

MIT
