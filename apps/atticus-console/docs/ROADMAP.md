---
document_id: DRL-CON-102
title: "Atticus Console Build Roadmap"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atticus Console Build Roadmap

    ## Delivery philosophy

    Atticus Console is built as thin verified vertical slices. Each slice includes contracts, implementation, tests, telemetry, documentation, demo evidence, and rollback—not an isolated subsystem no user can exercise.

    ## Workstreams

    - Protocol client and event reducer.
- Conversation, timeline, evidence, and artifacts.
- Approval UX.
- Reconnect, resume, cancel, and terminal states.
- Pane system, command palette, tours, and replay.
- Accessibility, security, performance, and integration.

    ## Dependency order

    Event fixtures → reducer → core renderers → approval → reconnect/replay → responsive workspace → exhaustive integration audit.

    ## Cross-project dependencies

    - Canonical DRL schemas and OpenAPI.
- Atticus task/run/event API.
- Design system and tokens.
- Signed replay format.
- Lab-web authentication and consent.

    ## Release evidence

    - Reducer and property tests.
- Visual and accessibility snapshots.
- Approval E2E and comprehension findings.
- Malformed-content security tests.
- Replay verification.
- Integrated demo report.

    ## Explicitly deferred

    - Collaborative multi-user consoles.
- Arbitrary plugin panes.
- Native desktop shell.
- Advanced trace-query language.
- Direct terminal command execution.

    Deferred work may appear on the public roadmap but cannot be implied by V1 marketing. Agents must not widen authority or scope “helpfully.”
