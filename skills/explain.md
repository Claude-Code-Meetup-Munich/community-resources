# Skill: /explain

> Erklärt eine Datei oder Funktion verständlich — ideal zum Onboarding.

## Installation

```bash
mkdir -p .claude/commands
cp explain.md .claude/commands/explain.md
```

## Skill-Inhalt

```markdown
Erkläre den Code in der angegebenen Datei oder Funktion verständlich.

Verwende $ARGUMENTS als Dateipfad oder Funktionsname.

Schritte:
1. Datei/Funktion lesen
2. Zweck in einem Satz zusammenfassen
3. Wichtige Konzepte erklären
4. Datenfluss beschreiben
5. Abhängigkeiten auflisten

Stil:
- Verständlich für Entwickler die den Code zum ersten Mal sehen
- Keine trivialen Kommentare ("diese Zeile importiert X")
- Fokus auf das WARUM, nicht das WAS
- Analogien nutzen wo hilfreich
```

## Nutzung

```
/explain src/auth/middleware.ts
/explain handleLogin
```

## Beispiel

```
> /explain src/auth/middleware.ts

## auth/middleware.ts — Authentifizierungs-Middleware

**Zweck:** Prüft bei jedem API-Request ob der User eingeloggt ist
und leitet nicht-authentifizierte Requests auf /login um.

**Wie es funktioniert:**
1. JWT-Token aus dem Cookie lesen
2. Token validieren (Signatur + Ablaufdatum)
3. User-Daten aus der DB laden und an Request hängen
4. Falls ungültig → 401 zurückgeben

**Abhängigkeiten:** jsonwebtoken, User-Model
**Genutzt von:** Alle geschützten API-Routes
```

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
