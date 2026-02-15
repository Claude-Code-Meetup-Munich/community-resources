# Prompt: Sicher Refactoren

> Refactoring mit Sicherheitsnetz — Schritt für Schritt, testbar, rückgängig machbar.

## Prompt

```
Refactore den folgenden Code. Aber sicher:

1. **Analyse zuerst** — Was tut der Code, welche Tests gibt es?
2. **Plan** — Welche Schritte, in welcher Reihenfolge?
3. **Kleine Commits** — Jeder Schritt einzeln commitbar und testbar
4. **Verhalten beibehalten** — Keine Feature-Änderungen beim Refactoring
5. **Rückwärtskompatibel** — Bestehende Interfaces nicht brechen

Regeln:
- KEIN "while I'm at it" — nur was nötig ist
- KEINE neuen Features reinschmuggeln
- Tests müssen nach jedem Schritt grün sein
- Wenn Tests fehlen: zuerst Tests schreiben, dann refactoren
```

## Wann nutzen?

- Code ist schwer zu verstehen oder zu erweitern
- Vor dem Hinzufügen neuer Features
- Tech-Debt abbauen

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
