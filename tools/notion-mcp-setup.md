# Notion MCP für Claude Code

> Verbinde deinen Notion-Workspace mit Claude Code — Seiten lesen, Datenbanken abfragen, Inhalte erstellen, per natürlicher Sprache.

## Was ist das?

Der offizielle [Notion MCP Server](https://developers.notion.com/guides/mcp/get-started-with-mcp.md) von Notion verbindet Claude Code mit deinem Workspace. Er läuft als Remote-Server bei Notion — kein lokales Setup, keine API-Token-Verwaltung.

## Voraussetzungen

- Claude Code installiert
- Ein Notion-Account

## Installation

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

Danach in Claude Code `/mcp` aufrufen und den OAuth-Flow abschließen (Browser öffnet sich automatisch).

### Scope-Optionen

```bash
# Nur für dich, nur im aktuellen Projekt (Standard)
claude mcp add --transport http --scope local notion https://mcp.notion.com/mcp

# Für alle deine Projekte
claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp

# Für das gesamte Team (erzeugt .mcp.json im Repo)
claude mcp add --transport http --scope project notion https://mcp.notion.com/mcp
```

## Nutzung

```
"Fasse die Seite 'Meeting Notes vom 20. Feb' zusammen"
"Erstelle eine neue Seite 'Sprint Retro' im Bereich Team"
"Welche Tasks in meiner Datenbank haben Status 'In Progress'?"
"Füge einen Eintrag zur Tabelle 'Bugs' hinzu"
```

## Wann lieber den `/notion-api` Skill?

Der MCP-Server ist ideal für **lesende und einfache schreibende Operationen**. Bei komplexeren Workflows stoßt er an Grenzen:

| Szenario | MCP | [`/notion-api` Skill](../skills/notion-api/) |
|----------|-----|------|
| Seite zusammenfassen | ✅ | ✅ |
| Neue Seite erstellen | ✅ | ✅ |
| Einzelnen Block gezielt updaten | ⚠️ überschreibt alles | ✅ atomares Update |
| Kommentare lesen & beantworten | ⚠️ eingeschränkt | ✅ |
| Lange Pages mit vielen Blöcken bearbeiten | ⚠️ ineffizient | ✅ |
| Markdown-Dokument in Notion pushen | ❌ | ✅ via `upload.py` |

Der `/notion-api` Skill nutzt die REST API direkt via curl — mehr Kontrolle, kein MCP nötig.

## Links

- [Notion MCP Dokumentation](https://developers.notion.com/guides/mcp/get-started-with-mcp.md)
- [Open-Source Server (Self-Hosting)](https://github.com/makenotion/notion-mcp-server)
- [Notion Developer Portal](https://developers.notion.com)

---

*Beigetragen von: Jörg Müller ([@codeeater](https://github.com/codeeater))*
