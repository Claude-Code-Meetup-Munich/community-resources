# Skills

Claude Code Skills (Slash-Commands) zum direkt Nutzen.

## Was sind Skills?

Skills sind wiederverwendbare Befehle für Claude Code. Du rufst sie mit `/skill-name` auf.

**Empfohlen: `.claude/skills/`** — unterstützt zusätzliche Features wie Supporting Files, Frontmatter-Steuerung und automatische Erkennung in Monorepos.

`.claude/commands/` funktioniert weiterhin (Legacy), wird aber nicht mehr empfohlen.

## Inhalt

| Skill | Beschreibung |
|-------|-------------|
| [commit.md](./commit.md) | Saubere Git-Commits mit konventioneller Message |
| [pr.md](./pr.md) | Pull Requests mit strukturierter Beschreibung |
| [review.md](./review.md) | Code-Review mit Severity-Levels |
| [explain.md](./explain.md) | Code verständlich erklärt für Onboarding |
| [notion-api/](./notion-api/) | Notion REST API Integration ohne MCP |

## Installation

```bash
# Empfohlen: als Skill (unterstützt Supporting Files)
mkdir -p .claude/skills
cp -r skill-name/ .claude/skills/skill-name/

# Einfache .md-Skills (Legacy, funktioniert weiterhin)
mkdir -p .claude/commands
cp skill-name.md .claude/commands/skill-name.md
```

## Eigene Skills beitragen

Siehe [CONTRIBUTING.md](../CONTRIBUTING.md).
