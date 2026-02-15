# Beitragen zum Community Resource Hub

Danke, dass du zur Community beitragen möchtest! Hier erfährst du, wie das geht.

---

## So funktioniert's

1. **Forke** dieses Repository
2. **Erstelle einen Branch** für deinen Beitrag
3. **Füge deine Ressource hinzu** im passenden Ordner
4. **Erstelle einen Pull Request** mit kurzer Beschreibung

Ein Organizer reviewed deinen PR und merged ihn.

---

## Ordnerstruktur

| Ordner | Was gehört rein? | Dateiformat |
|--------|------------------|-------------|
| `skills/` | Claude Code Skills (Slash-Commands) | `.md` |
| `agents/` | Custom Agent Konfigurationen | `.md` oder `.json` |
| `claude-md/` | CLAUDE.md Beispiele für verschiedene Projekttypen | `.md` |
| `prompts/` | Wiederverwendbare Prompts | `.md` |
| `tools/` | MCP Server Configs, Scripts, Guides | `.md` oder passend |

---

## Format für Beiträge

### Skills (`skills/`)

```markdown
# Skill-Name

> Kurze Beschreibung (1 Satz)

## Installation

\`\`\`bash
# Wie installiert man den Skill?
\`\`\`

## Nutzung

\`\`\`
/skill-name [argumente]
\`\`\`

## Beispiel

[Konkretes Beispiel der Nutzung]

---

*Beigetragen von: [Dein Name]*
```

### CLAUDE.md Beispiele (`claude-md/`)

```markdown
# CLAUDE.md – [Projekttyp]

> Für welche Art von Projekt ist das gedacht?

## Kontext

[Kurze Erklärung warum diese CLAUDE.md so aufgebaut ist]

---

[Die eigentliche CLAUDE.md — anonymisiert, keine echten API-Keys oder Firmennamen]

---

*Beigetragen von: [Dein Name]*
```

### Prompts (`prompts/`)

```markdown
# Prompt: [Name]

> Was macht dieser Prompt?

## Prompt

\`\`\`
[Der eigentliche Prompt-Text]
\`\`\`

## Wann nutzen?

[Beschreibung der Situation]

## Beispiel-Output

[Optional: Was kommt typischerweise raus?]

---

*Beigetragen von: [Dein Name]*
```

---

## Qualitätskriterien

Damit dein Beitrag gemerged wird:

- **Getestet**: Du hast es selbst erfolgreich benutzt
- **Dokumentiert**: Andere können es ohne Rückfragen nutzen
- **Anonymisiert**: Keine echten API-Keys, Firmennamen oder persönliche Daten
- **Eigenständig**: Falls externe Tools nötig sind, ist das dokumentiert

---

## Was wir NICHT annehmen

- Ungetestete oder kaputte Ressourcen
- Kopien aus anderen Repos ohne Quellenangabe
- Inhalte die gegen den Code of Conduct verstoßen
- Werbung oder Self-Promotion ohne echten Mehrwert

---

## Fragen?

Stell sie in unserem [Discord](https://discord.gg/wmCnKzVdHE) im `#hilfe` Channel oder erstelle ein [Issue](https://github.com/Claude-Code-Meetup-Munich/community-resources/issues).
