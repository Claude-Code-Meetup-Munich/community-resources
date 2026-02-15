# Discord MCP Server für Claude Code

> Manage deinen Discord-Server direkt aus Claude Code heraus — mit 71 Tools für Channels, Rollen, Messages und mehr.

## Was ist das?

Der [discord-agent-mcp](https://github.com/aj-geddes/discord-agent-mcp) Server verbindet Claude Code mit Discord. Du kannst dann per natürlicher Sprache Channels erstellen, Nachrichten posten, Rollen verwalten und mehr.

## Voraussetzungen

- Node.js 20+
- Ein Discord-Server auf dem du Admin bist
- Ein Discord Bot Token

## Schritt 1: Discord Bot erstellen

1. Geh zu https://discord.com/developers/applications
2. "New Application" → Name vergeben
3. Links "Bot" klicken → "Reset Token" → Token kopieren und sicher speichern
4. Unter "Privileged Gateway Intents" aktivieren:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Links "OAuth2" → "URL Generator":
   - Scopes: `bot`
   - Permissions: `Administrator`
   - URL öffnen → Bot zu deinem Server einladen

## Schritt 2: MCP Server installieren

```bash
git clone https://github.com/aj-geddes/discord-agent-mcp.git
cd discord-agent-mcp
npm install
npm run build
```

## Schritt 3: Starten

```bash
# Mit Token als Umgebungsvariable
DISCORD_TOKEN=dein_token_hier npm start

# Oder mit 1Password CLI
DISCORD_TOKEN=$(op item get "mein-discord-bot" --vault "Development Keys" --fields "DISCORD_TOKEN" --reveal) npm start
```

Der Server läuft auf `http://localhost:3000/mcp`.

## Schritt 4: In Claude Code registrieren

```bash
claude mcp add --transport http discord-agent http://localhost:3000/mcp
```

## Nutzung

Jetzt kannst du in Claude Code direkt mit Discord interagieren:

```
"Erstelle einen Channel #ankündigungen in der Kategorie Events"
"Poste eine Willkommensnachricht in #general"
"Erstelle die Rolle @Moderator mit blauer Farbe"
"Liste alle Channels auf dem Server"
```

## Verfügbare Tool-Kategorien

| Kategorie | Tools | Beispiele |
|-----------|-------|-----------|
| Messaging | 10 | Nachrichten senden, bearbeiten, pinnen |
| Channels | 10 | Channels erstellen, Berechtigungen setzen |
| Threads | 3 | Forum-Threads erstellen |
| Server | 7 | Einstellungen, Webhooks, Einladungen |
| Rollen | 7 | Rollen erstellen, zuweisen, bearbeiten |
| Moderation | 6 | Kick, Ban, Timeout |
| Events | 6 | Server-Events planen |

## Tipps

- **Bot muss laufen**: Der MCP-Server muss aktiv sein während du Claude Code nutzt
- **Berechtigungen**: Der Bot braucht Admin-Rechte für die meisten Operationen
- **Rate Limits**: Discord hat Rate Limits — bei vielen Operationen kurz warten lassen

## Links

- [discord-agent-mcp auf GitHub](https://github.com/aj-geddes/discord-agent-mcp)
- [Vollständige Dokumentation](https://aj-geddes.github.io/discord-agent-mcp/)
- [Discord Developer Portal](https://discord.com/developers/applications)

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
