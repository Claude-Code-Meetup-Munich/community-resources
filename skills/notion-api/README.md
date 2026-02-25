# Skill: /notion-api

> Notion API Integration via curl — Seiten lesen, Blöcke bearbeiten, Kommentare verwalten, Datenbanken abfragen.

## Warum API statt Notion MCP?

Der offizielle Notion MCP-Server funktioniert für einfache Abfragen gut — aber er stößt schnell an Grenzen: Bei langen Pages liest Claude alles als Text, kann aber keine atomaren Block-Updates machen. Jede Änderung überschreibt alles. Direkte curl-Calls sind präziser, schneller und deterministisch debuggbar.

## Voraussetzungen

- `curl` und `jq` — auf macOS und Linux standardmäßig vorhanden. Windows: [Git Bash](https://git-scm.com/downloads) oder WSL.
- Für `upload.py` (optional): Python 3. Empfehlung: [`uv`](https://docs.astral.sh/uv/) — installiert Python automatisch, funktioniert auf allen Plattformen.

## Installation

```bash
cp -r notion-api/ .claude/skills/notion-api/
```

Config anlegen (`.claude/config/notion.json`):

```json
{
  "token": "ntn_...",
  "pages": {
    "my-page": { "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }
  }
}
```

> ⚠️ Add `.claude/config/notion.json` to your `.gitignore` — it contains your integration token.

Token: **notion.so → Settings → Connections → Develop or manage integrations**

## Nutzung

```
/notion-api [Aufgabe beschreiben]
```

- `/notion-api Lies die Seite "Meeting Notes" und fasse sie zusammen`
- `/notion-api Füge einen neuen Eintrag in die Tasks-Datenbank ein`
- `/notion-api Antworte auf den Kommentar in Block xyz`

---

*Beigetragen von: Jörg Müller ([@codeeater](https://github.com/codeeater))*
