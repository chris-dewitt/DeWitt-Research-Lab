---
document_id: DRL-ATT-105
title: "Atticus Control Plane Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atticus Control Plane Build Roadmap

    ## Delivery philosophy

    Atticus Control Plane is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Canonical protocol and state machine.
- Skills, catalog, and policy integration.
- Open-weight model gateway and routing.
- Public sessions/API and console integration.
- Specialist adapters and evidence synthesis.
- Approvals and local-runner pairing.
- Evaluation, reliability, security, and operations.

    ## Dependency order

    Contracts and simulator → fixture tools/policy → public guide → specialist routing → approvals/local runner → Core/Edge routes → failure/load/security hardening → integrated release.

    ## Cross-project dependencies

    - DRL protocol and policy packages precede executable orchestration.
- EvalForge trace schema precedes optimization.
- Specialists can begin against contract fixtures.
- Web can ship signed replays before live APIs.
- Pairing waits for identity/approval threat-model approval.

    ## Release evidence

    - State-machine and contract report.
- AtticusBench baseline/candidate report.
- Signed integrated workflow trace.
- Approval and injection security report.
- Cloud load, cost, rollback, and incident drill.
- Operator runbook and director acceptance.

    ## Explicitly deferred

    - General browser/computer-use autonomy.
- Marketplace billing.
- Rich organization multi-tenancy.
- Self-modifying skills/models.
- Automatic learning from ordinary conversations.
- Unbounded persistent personal memory.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
