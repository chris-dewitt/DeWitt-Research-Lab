---
document_id: DRL-LOC-100
title: "Atticus Local Runner Project README"
version: 4.2.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-29
---


    # Atticus Local Runner

    **Role in DeWitt Research Workshop:** Installable private execution node for scoped local files, repositories, shell profiles, voice, and applications.

    Central V1 feature with a strict security bar. The current prototype provides canonical approved-root listing plus redacted `inspect_text`/`read_text`, size and binary limits, traversal/symlink denial, and exact-digest atomic text-write proposals. Writes now flow through `ApprovedWriteFlow`: an expiring, actor-identified, workspace-scoped approval grant bound to the exact proposal digest, with a redacted append-only local audit log; expired, re-bound, or changed-workspace applies are denied and audited. Pairing, voice, sandboxed commands, OS credential storage, and signed updates remain planned. The public website never pairs to the Director’s real runner.

    This directory is an independently testable part of the DRL monorepo. It inherits the laboratory constitution in [`LABORATORY_BIBLE.md`](../../LABORATORY_BIBLE.md), the agent contract in [`AGENTS.md`](../../AGENTS.md), and canonical protocol/security/data contracts under [`schemas/`](../../schemas). Project specifications below govern this component; a conflict with an approved laboratory-wide document requires an ADR rather than an improvised compromise.

    ## Scope boundary

    - Python daemon/CLI/approval UI, OS integration, tool plugins, pairing, outbound channel, local audit, and packaging.
- It is not a general remote administration service.
- Sensitive capabilities are deny-by-default.

    ## Target developer entry point

    ```bash
    uv sync --all-extras && uv run pytest -q tests/test_local_runner.py
    ```

    The baseline setup and tests must work with open or mocked providers and fixture data. Paid APIs may enhance development but cannot be mandatory for ordinary contributors or the fast CI suite.

    ## Required reading

    - [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/PROTOCOL.md`](docs/PROTOCOL.md)
- [`docs/TOOLS_AND_SANDBOX.md`](docs/TOOLS_AND_SANDBOX.md)
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
