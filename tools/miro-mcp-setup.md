# Miro MCP für Claude Code (inoffiziell)

> Steuere Miro-Boards direkt aus Claude Code — Sticky Notes, Shapes, Frames, Mindmaps, Diagramme und mehr. 89 Tools via REST API.

## Warum nicht der offizielle Miro MCP?

Miro hat einen offiziellen MCP Server, der aber nur einen Bruchteil der [Miro REST API](https://developers.miro.com/reference/api-reference) abdeckt. Dieser inoffizielle Server von [Olga Safonova](https://github.com/olgasafonova/miro-mcp-server) implementiert 89 Tools und gibt Claude Code vollen Zugriff auf Boards, Items, Frames, Kommentare und mehr.

## Voraussetzungen

- Ein Miro-Account mit Zugriff auf mindestens ein Board
- Ein Miro API Token (siehe unten)

## Schritt 1: Miro API Token erstellen

1. Geh zu [miro.com/app/settings/user-profile/apps](https://miro.com/app/settings/user-profile/apps)
2. „Create new app" → Name vergeben
3. Permissions aktivieren: `boards:read` und `boards:write`
4. „Install app and get OAuth token" → Token kopieren

## Schritt 2: Server installieren

```bash
# macOS (empfohlen)
brew tap olgasafonova/tap && brew install miro-mcp-server

# Alternativ: Install-Script (macOS/Linux)
curl -fsSL https://raw.githubusercontent.com/olgasafonova/miro-mcp-server/main/install.sh | sh

# Docker
docker pull ghcr.io/olgasafonova/miro-mcp-server:latest
```

Windows: Binaries unter [SETUP.md](https://github.com/olgasafonova/miro-mcp-server/blob/main/SETUP.md) im Repo.

## Schritt 3: In Claude Code registrieren

```bash
claude mcp add miro -e MIRO_ACCESS_TOKEN=dein_token -- miro-mcp-server
```

## Nutzung

```
"Erstelle ein neues Board 'Sprint Planning Q2'"
"Füge 5 Sticky Notes mit den wichtigsten Risiken hinzu"
"Erstelle ein Flowchart aus diesem Mermaid-Diagramm"
"Gruppiere alle roten Sticky Notes in einem Frame"
"Liste alle Boards in meinem Team"
```

## Verfügbare Tool-Kategorien

| Kategorie | Beispiele |
|-----------|-----------|
| Boards | Erstellen, kopieren, teilen, Mitglieder verwalten |
| Items | Sticky Notes, Shapes, Text, Cards, Bilder, Frames |
| Diagramme | Flowcharts & Sequence Diagrams aus Mermaid-Syntax |
| Mindmaps | Nodes erstellen und verbinden |
| Organisation | Tags, Gruppen, Bulk-Operationen, Exports |

## Links

- [miro-mcp-server auf GitHub](https://github.com/olgasafonova/miro-mcp-server)
- [Miro REST API Dokumentation](https://developers.miro.com/reference/api-reference)
- [Miro Developer Portal](https://developers.miro.com)

---

*Beigetragen von: Jörg Müller ([@codeeater](https://github.com/codeeater))*
