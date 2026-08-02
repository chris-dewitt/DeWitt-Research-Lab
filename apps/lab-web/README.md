---
document_id: DRL-WEB-100
title: "DeWitt Research Laboratory Web Project README"
version: 4.0.0
status: RELEASE CANDIDATE
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # DeWitt Research Laboratory Web

    **Role in DeWitt Research Laboratory:** Open-source interactive web platform, shared application shell, research/documentation workspace, Atticus interface, failure museum, status console, and portable open-source portal. The canonical institutional homepage is the Wix site at `https://www.dewitt-labs.com`.

    Design and content contracts are defined; public maturity requires accessibility, truthful-demo, performance, and provenance evidence.

    This directory is an independently testable part of the DRL monorepo. It inherits the laboratory constitution in [`LABORATORY_BIBLE.md`](../../LABORATORY_BIBLE.md), the agent contract in [`AGENTS.md`](../../AGENTS.md), and canonical protocol/security/data contracts under [`schemas/`](../../schemas). Project specifications below govern this component; a conflict with an approved laboratory-wide document requires an ADR rather than an improvised compromise.

    ## Scope boundary

    - Next.js/TypeScript application, content pipeline, design-system consumption, tests, and safe API/replay adapters.
- Deployable under DRL application/documentation subdomains and self-hostable by contributors.
- May generate validated content payloads or widgets for the Wix institutional site.
- It does not contain authoritative project calculations or hand-edited system metrics.
- Controlled Markdown/MDX and signed artifacts remain the source of truth.

    ## Target developer entry point

    ```bash
    pnpm install --frozen-lockfile && pnpm --filter @drl/lab-web test && pnpm --filter @drl/lab-web dev
    ```

    The baseline setup and tests must work with open or mocked providers and fixture data. Paid APIs may enhance development but cannot be mandatory for ordinary contributors or the fast CI suite.

    ## Required reading

    - [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/INFORMATION_ARCHITECTURE.md`](docs/INFORMATION_ARCHITECTURE.md)
- [`docs/DATA_AND_CONTENT.md`](docs/DATA_AND_CONTENT.md)
- [`docs/EVALUATION.md`](docs/EVALUATION.md)
- [`docs/SECURITY.md`](docs/SECURITY.md)
- [`docs/DEMO.md`](docs/DEMO.md)
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


## Wix boundary

This application does not assume it owns `www.dewitt-labs.com`. It must provide stable launch URLs, return navigation, shared tokens, release metadata, and bounded widget surfaces to the Wix site. Primary authenticated or computational flows must remain usable outside an iframe. See `../../docs/08-web-brand/DOMAIN_AND_WIX_INTEGRATION.md`.
