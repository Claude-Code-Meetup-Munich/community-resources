# CLAUDE.md – Fullstack Web-Anwendung

> Für Projekte mit Frontend (React/Next.js) + Backend (API) + Datenbank.

## Kontext

Diese CLAUDE.md eignet sich für typische Fullstack-Projekte mit modernem JavaScript/TypeScript-Stack. Sie definiert klare Regeln für Code-Qualität, Testing und Git-Workflow.

---

```markdown
# CLAUDE.md

## Projekt

[Projektname] ist eine Web-Anwendung für [Zweck].

**Tech-Stack:**
- Frontend: Next.js 15 mit App Router
- Backend: API Routes (Next.js)
- Datenbank: PostgreSQL mit Prisma ORM
- Auth: NextAuth.js
- Hosting: Vercel

## Architektur

```
src/
├── app/              # Next.js App Router Pages
├── components/       # React Components
│   ├── ui/          # Basis-Komponenten (Button, Input, etc.)
│   └── features/    # Feature-Komponenten
├── lib/             # Shared Utilities
│   ├── db.ts        # Prisma Client
│   └── auth.ts      # Auth Config
├── actions/         # Server Actions
└── types/           # TypeScript Types
```

## Regeln

### Code
- TypeScript strict mode — keine `any` Types
- Server Components bevorzugen, Client Components nur wenn nötig
- Server Actions für Mutations, nicht API Routes
- Prisma für alle DB-Operationen, kein Raw SQL
- Zod für Input-Validierung an Systemgrenzen

### Stil
- Funktionale Komponenten mit Arrow Functions
- Named Exports (kein `export default`)
- Tailwind CSS für Styling, keine CSS-Module
- Deutsche Kommentare nur wenn Logik nicht selbsterklärend

### Git
- Conventional Commits (feat/fix/refactor/docs/chore)
- Feature Branches von `main`
- PR mit Review vor Merge
- Keine direkten Pushes auf `main`

### Testing
- Vitest für Unit Tests
- Playwright für E2E Tests
- Tests vor PR erstellen laufen lassen: `npm test`

## Commands

| Command | Was |
|---------|-----|
| `npm run dev` | Dev Server starten |
| `npm test` | Tests laufen lassen |
| `npm run build` | Production Build |
| `npx prisma studio` | DB Browser öffnen |
| `npx prisma migrate dev` | Migration erstellen |
```

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
