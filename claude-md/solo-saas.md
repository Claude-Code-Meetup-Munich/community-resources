# CLAUDE.md – Solo SaaS Projekt

> Für Solopreneure die ein SaaS-Produkt mit Claude Code entwickeln.

## Kontext

Optimiert für schnelle Iteration als Einzelperson. Weniger Prozess, mehr Pragmatismus. Fokus auf shipped > perfect.

---

```markdown
# CLAUDE.md

## Projekt

[Produktname] — [Einzeiler was es tut]

**Stack:** Next.js · Supabase · Stripe · Vercel

## Prioritäten

1. **Shipping** > Perfektion
2. **Einfachheit** > Abstraktion
3. **Supabase-Features nutzen** > selbst bauen (Auth, Storage, Realtime)

## Architektur

- Supabase für Auth, DB, Storage, Edge Functions
- Stripe für Payments (Checkout + Webhooks)
- Vercel für Hosting und Preview Deployments

## Regeln

- KEIN Overengineering: 3 ähnliche Zeilen > premature Abstraction
- KEINE Tests für UI-Code (ändert sich zu oft)
- Tests NUR für: Payment-Logik, Auth-Flows, Daten-Transformationen
- Supabase RLS Policies für Security, nicht Middleware
- Stripe Webhooks sind die Single Source of Truth für Payment-Status

## Workflow

1. Feature in Supabase planen (Schema, RLS, Edge Functions)
2. Frontend bauen
3. Testen auf Preview Deployment
4. Merge wenn es auf Preview funktioniert

## Secrets

- Alle in `.env.local` (gitignored)
- Production-Secrets in Vercel Environment Variables
- Supabase Keys: `NEXT_PUBLIC_SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY`
- Stripe: `STRIPE_SECRET_KEY` + `STRIPE_WEBHOOK_SECRET`

## Commands

| Command | Was |
|---------|-----|
| `npm run dev` | Dev Server |
| `supabase start` | Lokale Supabase |
| `supabase db push` | Schema-Änderungen deployen |
| `stripe listen --forward-to localhost:3000/api/webhooks` | Webhook-Testing |
```

---

*Beigetragen von: Claude Code Munich Meetup Orga-Team*
