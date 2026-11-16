# sqlit-omarchy

Eine schnelle, tastaturgesteuerte SQL-TUI für Omarchy. Datenbanken verbinden,
SQL schreiben und Ergebnisse durchsuchen – direkt im Terminal.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Was ist besonders?

- Automatische Anpassung an das aktive Omarchy-Theme
- Live-Aktualisierung beim Wechsel des Themes
- SQL Server, PostgreSQL, MySQL, SQLite, MariaDB, DuckDB und viele weitere
- Connection Manager, SQL-History und Vim-artige Bedienung
- Syntax-Highlighting, Autocomplete und Filter für große Ergebnisse
- Docker-Erkennung, SSH-Tunnel und sichere Passwortablage im System-Keyring

## Installation

Für Omarchy wird direkt dieser Fork installiert:

```bash
pipx install git+https://github.com/JackyyyGames/sqlit-omarchy.git
```

Alternativ:

```bash
uv tool install git+https://github.com/JackyyyGames/sqlit-omarchy.git
```

Starten:

```bash
sqlit
```

Ohne echte Datenbank testen:

```bash
sqlit --mock=sqlite-demo
```

## Omarchy-Theme-Synchronisierung

sqlit liest die Palette aus:

```text
~/.config/omarchy/current/theme/colors.toml
```

Übernommen werden unter anderem Hintergrund, Vordergrund, Akzentfarbe,
Statusfarben, Rahmen, Auswahlfarbe und Query-Editor-Farben. Wenn du in
Omarchy das Theme wechselst, erkennt sqlit das automatisch. Es werden keine
Omarchy-Dateien verändert und kein Plugin oder Hook benötigt.

Außerhalb von Omarchy bleibt das normale sqlit-Theme-System aktiv. Bei einem
Theme ohne lesbare `colors.toml` wird ein sicherer Fallback verwendet.

## Updates aus dem Originalprojekt

Dieser Fork wird nicht automatisch aktualisiert, wenn das Originalprojekt neue
Commits erhält. Das Original ist als `origin` hinterlegt. Updates können später
so übernommen werden:

```bash
git fetch origin
git log HEAD..origin/main
git merge origin/main
```

Danach die Omarchy-Änderungen testen und in den Fork pushen:

```bash
uv run pytest tests/unit/test_omarchy.py
git push fork main
```

## Entwicklung

```bash
git clone https://github.com/JackyyyGames/sqlit-omarchy.git
cd sqlit-omarchy
uv sync --group dev
uv run pytest tests/unit/test_omarchy.py
uv run ruff check .
```

## Herkunft und Lizenz

sqlit-omarchy basiert auf [sqlit](https://github.com/Maxteabag/sqlit) und steht
unter der MIT-Lizenz. Die Omarchy-Anpassungen befinden sich in
`sqlit/domains/shell/app/omarchy.py` und `theme_manager.py`.
