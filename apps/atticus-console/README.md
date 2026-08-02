---
document_id: DRL-CON-100
title: "Atticus Console Project README"
version: 3.0.0
status: RELEASE CANDIDATE
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atticus Console

    **Role in DeWitt Research Laboratory:** Reusable TypeScript client and component system for conversation, events, approvals, evidence, artifacts, and tmux-inspired panes.

    UI contract defined; final acceptance occurs within the integrated lab-web experience.

    This directory is an independently testable part of the DRL monorepo. It inherits the laboratory constitution in [`LABORATORY_BIBLE.md`](../../LABORATORY_BIBLE.md), the agent contract in [`AGENTS.md`](../../AGENTS.md), and canonical protocol/security/data contracts under [`schemas/`](../../schemas). Project specifications below govern this component; a conflict with an approved laboratory-wide document requires an ADR rather than an improvised compromise.

    ## Scope boundary

    - Standalone development shell and reusable state/components.
- Lab-web consumes this package rather than duplicating console behavior.
- Only safe operational summaries are displayed; hidden reasoning is out of scope.

    ## Target developer entry point

    ```bash
    pnpm install --frozen-lockfile && pnpm --filter @drl/atticus-console test
    ```

    The baseline setup and tests must work with open or mocked providers and fixture data. Paid APIs may enhance development but cannot be mandatory for ordinary contributors or the fast CI suite.

    ## Required reading

    - [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/STATE_AND_EVENTS.md`](docs/STATE_AND_EVENTS.md)
- [`docs/ACCESSIBILITY_AND_SECURITY.md`](docs/ACCESSIBILITY_AND_SECURITY.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)

    ## Health standard

    A healthy project has deterministic setup, typed interfaces, explicit configuration, structured logs, trace propagation, realistic fixtures, security-negative tests, documented failure behavior, and a public demo that does not depend on private data. “It works on my machine” is not release evidence.

    ## Contribution and change control

    Feature work occurs on a feature branch and enters through a pull request. Public API, authority boundaries, retention, permissions, model routing, deployment topology, or licensing changes require a director-approved ADR before implementation. Generated artifacts require source and reproduction instructions.

    ## V1 exit evidence

    - project acceptance criteria and cross-project contracts pass;
    - timeout, cancellation, retry, idempotency, and error paths are exercised;
    - security/privacy controls are verified by negative tests;
    - public demonstrations are bounded, accessible, and reproducible;
    - the integrated reference workflow can invoke this component and receive a traceable result;
    - release, rollback, and operator runbooks are usable by someone other than the author.
