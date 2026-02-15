# Skill: /pr

> Erstellt einen Pull Request mit strukturierter Beschreibung.

## Installation

```bash
mkdir -p .claude/commands
cp pr.md .claude/commands/pr.md
```

## Skill-Inhalt

```markdown
Erstelle einen Pull Request für den aktuellen Branch.

Schritte:
1. `git log main..HEAD` für alle Commits seit main
2. `git diff main...HEAD` für alle Änderungen
3. PR-Titel erstellen (max 70 Zeichen, beschreibend)
4. PR-Body mit Summary und Test Plan erstellen
5. PR mit `gh pr create` erstellen

Format:
## Summary
- Bullet Points der wichtigsten Änderungen

## Test plan
- [ ] Schritte zum Testen

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Nutzung

```
/pr
```

## Beispiel

```
> /pr

PR erstellt: "Add login rate limiting for auth endpoints"
→ https://github.com/org/repo/pull/42
```

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
