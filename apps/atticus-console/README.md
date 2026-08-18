---
document_id: DRL-CON-100
title: "Atticus Console Project README"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-17
---

# Atticus Console

**Maturity:** `specified`

This directory specifies a reusable TypeScript interface for conversation,
events, approvals, evidence, artifacts, and terminal-inspired panes. It is not
currently implemented: the package commands report `implementation pending`,
and no component library or UI test suite exists here yet.

## Intended scope

- Provide reusable state and components for the future lab-web application.
- Present safe operational summaries, not hidden model reasoning.
- Make permission, failure, empty, loading, and cold-start states inspectable.
- Meet keyboard, accessible-name, contrast, reduced-motion, and responsive
  layout requirements before any release claim.

## Current developer check

```bash
pnpm install --frozen-lockfile
pnpm --filter @drl/atticus-console lint
pnpm --filter @drl/atticus-console typecheck
pnpm --filter @drl/atticus-console test
pnpm --filter @drl/atticus-console build
```

These commands verify only the declared scaffold state.

## Required reading

- [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/STATE_AND_EVENTS.md`](docs/STATE_AND_EVENTS.md)
- [`docs/ACCESSIBILITY_AND_SECURITY.md`](docs/ACCESSIBILITY_AND_SECURITY.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)
