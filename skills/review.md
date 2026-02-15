# Skill: /review

> Führt ein Code-Review des aktuellen Branches durch.

## Installation

```bash
mkdir -p .claude/commands
cp review.md .claude/commands/review.md
```

## Skill-Inhalt

```markdown
Führe ein Code-Review aller Änderungen im aktuellen Branch durch (verglichen mit main).

Schritte:
1. `git diff main...HEAD` ausführen
2. Alle geänderten Dateien systematisch reviewen
3. Feedback in Kategorien geben

Kategorien:
🔴 Blocker — Muss gefixt werden vor Merge
🟡 Vorschlag — Sollte gefixt werden, kein Blocker
🟢 Nitpick — Stilistisch, optional
💡 Frage — Etwas das unklar ist

Format pro Finding:
**[Kategorie] Datei:Zeile**
Beschreibung des Problems + Lösungsvorschlag

Am Ende: Zusammenfassung mit Go/No-Go Empfehlung.
```

## Nutzung

```
/review
```

## Beispiel

```
> /review

Code Review für Branch `feat/login-rate-limit`:

🔴 src/middleware/rate-limit.ts:15
Rate-Limit Counter wird nie zurückgesetzt → Memory Leak
→ Fix: TTL-basierter Cache verwenden

🟢 src/routes/auth.ts:42
Magic Number 100 → als Konstante extrahieren

Zusammenfassung: 1 Blocker, 1 Nitpick
Empfehlung: 🔴 Blocker zuerst fixen
```

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
