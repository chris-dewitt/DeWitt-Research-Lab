---
document_id: DRL-WEB-100
title: "DeWitt Research Lab Web Project README"
version: 4.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-17
---

# DeWitt Research Lab Web

**Maturity:** `specified`

This directory defines the planned Next.js/TypeScript research interface. It is
not currently an implemented application: its package commands explicitly
report `implementation pending`, and no user interface or web test suite exists
here yet. The live personal portfolio remains
[`www.dewitt-labs.com`](https://www.dewitt-labs.com).

## Intended scope

- Present selected research, reports, and replay evidence.
- Provide an accessible shell for Atticus and the failure museum.
- Consume signed or validated artifacts without becoming their source of truth.
- Remain self-hostable and usable with fixture or open-provider paths.

## Current developer check

```bash
pnpm install --frozen-lockfile
pnpm --filter @drl/lab-web lint
pnpm --filter @drl/lab-web typecheck
pnpm --filter @drl/lab-web test
pnpm --filter @drl/lab-web build
```

These commands verify only the declared scaffold state. They are not evidence
of an implemented web application.

## Required reading

- [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/INFORMATION_ARCHITECTURE.md`](docs/INFORMATION_ARCHITECTURE.md)
- [`docs/DATA_AND_CONTENT.md`](docs/DATA_AND_CONTENT.md)
- [`docs/EVALUATION.md`](docs/EVALUATION.md)
- [`docs/SECURITY.md`](docs/SECURITY.md)
- [`docs/DEMO.md`](docs/DEMO.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)
- [`DOMAIN_AND_WIX_INTEGRATION.md`](../../docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md)

Implementation claims require runnable code, accessibility and responsive-state
evidence, security-negative tests, and a reproducible public demonstration.
