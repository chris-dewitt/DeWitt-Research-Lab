---
document_id: DRL-FED-100
title: "FedLens Project README"
version: 4.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---


    # FedLens

    **Role in DeWitt Research Laboratory:** Federal Reserve communications and policy research with exact document comparison, temporal retrieval, NLP, and reproducible event studies.

    Runnable synthetic-corpus prototype with as-of document selection, exact document identity, deterministic language diff, and a disclosed teaching lexicon. Public Federal Reserve ingestion and statistical NLP remain planned.

    This directory is an independently testable part of the DRL monorepo. It inherits the laboratory constitution in [`LABORATORY_BIBLE.md`](../../LABORATORY_BIBLE.md), the agent contract in [`AGENTS.md`](../../AGENTS.md), and canonical protocol/security/data contracts under [`schemas/`](../../schemas). Project specifications below govern this component; a conflict with an approved laboratory-wide document requires an ADR rather than an improvised compromise.

    ## Scope boundary

    - Python service, corpus pipeline, alignment/NLP/event engine, fixtures, tests, and controlled documents.
- Exact source text and deterministic methods remain authoritative.
- Cross-project public research assets belong in research/datasets releases.

    ## Target developer entry point

    ```bash
    uv sync --all-extras && uv run pytest services/fedlens
    ```

    The baseline setup and tests must work with open or mocked providers and fixture data. Paid APIs may enhance development but cannot be mandatory for ordinary contributors or the fast CI suite.

    ## Required reading

    - [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/API.md`](docs/API.md)
- [`docs/DATA.md`](docs/DATA.md)
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
