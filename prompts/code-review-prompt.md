# Prompt: Detailliertes Code-Review

> Strukturiertes Code-Review mit Severity-Levels und konkreten Fix-Vorschlägen.

## Prompt

```
Führe ein detailliertes Code-Review durch. Prüfe auf:

1. **Bugs & Logik-Fehler** — Falsches Verhalten, Edge Cases
2. **Security** — Injection, XSS, fehlende Validierung, hardcoded Secrets
3. **Performance** — N+1 Queries, unnötige Re-Renders, Memory Leaks
4. **Lesbarkeit** — Naming, Komplexität, fehlende Typen

Für jedes Finding:
- Severity: 🔴 Blocker | 🟡 Wichtig | 🟢 Nice-to-have
- Datei und Zeile
- Problem in einem Satz
- Konkreter Fix-Vorschlag als Code

Am Ende: Zusammenfassung und Go/No-Go Empfehlung.
```

## Wann nutzen?

Vor jedem PR-Merge oder wenn du unsicher bist ob dein Code produktionsreif ist.

## Tipp

Kombiniere mit `git diff main...HEAD` damit Claude nur die relevanten Änderungen sieht.

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
