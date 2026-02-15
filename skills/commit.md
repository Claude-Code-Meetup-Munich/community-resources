# Skill: /commit

> Erstellt einen sauberen Git-Commit mit konventioneller Commit-Message.

## Installation

```bash
# Erstelle den Commands-Ordner falls nicht vorhanden
mkdir -p .claude/commands

# Kopiere die Skill-Datei
cp commit.md .claude/commands/commit.md
```

## Skill-Inhalt

```markdown
Analysiere die aktuellen Änderungen (staged + unstaged) und erstelle einen Git-Commit.

Schritte:
1. `git status` und `git diff` ausführen
2. Änderungen analysieren
3. Conventional Commit Message erstellen (feat/fix/refactor/docs/chore)
4. Commit erstellen mit Co-Authored-By Header

Format der Commit-Message:
- Typ: feat|fix|refactor|docs|chore|test
- Scope optional in Klammern
- Beschreibung im Imperativ, max 72 Zeichen
- Body nur wenn nötig

Beispiel:
feat(auth): Add login rate limiting

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Nutzung

```
/commit
```

Claude analysiert automatisch alle Änderungen und schlägt eine passende Commit-Message vor.

## Beispiel

```
> /commit

Ich sehe folgende Änderungen:
- Neue Datei: src/middleware/rate-limit.ts
- Geändert: src/routes/auth.ts (Rate-Limiter integriert)

Vorgeschlagener Commit:
feat(auth): Add login rate limiting

→ Soll ich committen?
```

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
