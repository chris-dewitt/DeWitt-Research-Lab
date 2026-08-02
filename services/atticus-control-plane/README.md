---
document_id: DRL-ATT-100
title: "Atticus Control Plane Project README"
version: 4.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-27
---


    # Atticus Control Plane

    **Role in DeWitt Research Laboratory:** Policy-governed orchestration that plans, routes, invokes specialists, manages approvals, and synthesizes results.

    Runnable local prototype with deterministic planning, risk policy, exact-call approvals, state transitions, specialist routing, evidence-preserving synthesis, EvalForge submission, CLI, HTTP adapter, tests, and container build. It is not yet a trained model runtime or production public service.

    This directory is an independently testable part of the DRL monorepo. It inherits the laboratory constitution in [`LABORATORY_BIBLE.md`](../../LABORATORY_BIBLE.md), the agent contract in [`AGENTS.md`](../../AGENTS.md), and canonical protocol/security/data contracts under [`schemas/`](../../schemas). Project specifications below govern this component; a conflict with an approved laboratory-wide document requires an ADR rather than an improvised compromise.

    ## Scope boundary

    - Python service code, API, state machine, adapters, persistence, and tests.
- No unrestricted local execution; that belongs to the paired local runner.
- No specialist domain logic; Atlas, FedLens, BalanceLab AI, and EvalForge own their domains.

    ## Target developer entry point

    ```bash
    uv sync --all-packages
    uv run --package atticus-control-plane atticus-demo --public
    uv run pytest tests/test_atticus_foundation.py
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
