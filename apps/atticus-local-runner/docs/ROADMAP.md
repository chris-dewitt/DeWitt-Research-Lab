---
document_id: DRL-LOC-104
title: "Atticus Local Runner Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atticus Local Runner Build Roadmap

    ## Delivery philosophy

    Atticus Local Runner is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Capability registry and local policy.
- Filesystem and repository tools.
- Process sandbox.
- Pairing, channel, rotation, and revocation.
- Approval UI and audit.
- Voice, local models, and offline mode.
- Packaging, signed update, and security hardening.

    ## Dependency order

    Simulator and policy → read-only files/Git → sandbox tests → patch/write approval → pairing/channel → local inference/voice → packaging and independent security review.

    ## Cross-project dependencies

    - Atticus control-plane identity and approval protocol.
- Atticus Edge/Core runtimes.
- Shared protocol and policy SDKs.
- EvalForge local trajectory and security suites.
- Signed installer/release infrastructure.

    ## Release evidence

    - Protocol and sandbox reports.
- Windows install/update/rollback/uninstall matrix.
- Paired and offline signed workflows.
- Packet/privacy report.
- Security review.
- User and operator runbooks.

    ## Explicitly deferred

    - Polished macOS/Linux distribution beyond portable core.
- Broad application automation.
- Remote desktop.
- Unreviewed plugin marketplace.
- Automatic privilege elevation.
- Mobile local runner.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
