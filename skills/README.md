# Skills

Claude Code Skills (Slash-Commands) zum direkt Nutzen.

## Was sind Skills?

Skills sind wiederverwendbare Befehle für Claude Code. Du legst sie als `.md`-Dateien in `.claude/commands/` ab und rufst sie mit `/skill-name` auf.

## Inhalt

| Skill | Beschreibung |
|-------|-------------|
| [commit.md](./commit.md) | Saubere Git-Commits mit konventioneller Message |
| [pr.md](./pr.md) | Pull Requests mit strukturierter Beschreibung |
| [review.md](./review.md) | Code-Review mit Severity-Levels |
| [explain.md](./explain.md) | Code verständlich erklärt für Onboarding |

## Installation

```bash
# Einen Skill installieren
mkdir -p .claude/commands
cp skill-name.md ~/.claude/commands/skill-name.md

# Oder projektspezifisch
cp skill-name.md .claude/commands/skill-name.md
```

## Eigene Skills beitragen

Siehe [CONTRIBUTING.md](../CONTRIBUTING.md).
