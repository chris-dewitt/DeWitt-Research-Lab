---
document_id: DRL-MODE-100
title: "Atticus Edge Project README"
version: 3.0.0
status: RELEASE CANDIDATE
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Edge

    **Role in DeWitt Research Laboratory:** Small open-weight Atticus model for local routing, constrained tool proposals, voice responsiveness, offline guidance, and escalation.

    Designed in parallel with Core; its local latency, memory, and escalation claims must be independently earned.

    This directory is an independently testable part of the DRL monorepo. It inherits the laboratory constitution in [`LABORATORY_BIBLE.md`](../../LABORATORY_BIBLE.md), the agent contract in [`AGENTS.md`](../../AGENTS.md), and canonical protocol/security/data contracts under [`schemas/`](../../schemas). Project specifications below govern this component; a conflict with an approved laboratory-wide document requires an ADR rather than an improvised compromise.

    ## Scope boundary

    - Edge-specific training, distillation, quantization, device evaluation, and release cards.
- Edge is a bounded product, not a smaller marketing copy of Core.
- The shipped quantized artifact is evaluated as the product.

    ## Target developer entry point

    ```bash
    uv sync --all-extras && uv run python -m models.atticus_edge.cli validate-config
    ```

    The baseline setup and tests must work with open or mocked providers and fixture data. Paid APIs may enhance development but cannot be mandatory for ordinary contributors or the fast CI suite.

    ## Required reading

    - [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/DISTILLATION_AND_TRAINING.md`](docs/DISTILLATION_AND_TRAINING.md)
- [`docs/EVALUATION.md`](docs/EVALUATION.md)
- [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md)
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
