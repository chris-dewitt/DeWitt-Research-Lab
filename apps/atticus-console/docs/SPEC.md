---
document_id: DRL-CON-103
title: "Atticus Console System Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Console System Specification

    ## 1. Purpose and authority

    The Atticus Console makes agent work understandable and controllable. It renders conversation and final artifacts alongside a concise operational timeline, policy and approval prompts, evidence, failures, cost, and specialist activity without exposing private hidden reasoning or making terminal aesthetics inaccessible.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for Atticus Console. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Public DRL visitors.
- Authenticated private Atticus users.
- Operators reviewing traces and incidents.
- Developers embedding console components.
- Keyboard, screen-reader, reduced-motion, low-vision, and mobile users.

    ## 3. V1 capabilities

    - Create, resume, and cancel tasks and sessions.
- Render structured run events and one terminal state.
- Display safe plan summaries, specialist and tool activity, evidence, and artifacts.
- Present trusted approval dialogs with resource, effect, risk, duration, and expiry.
- Support conversation, guided tour, replay, architecture, compact, and multi-pane modes.
- Reconnect and resume streams while de-duplicating events.
- Export a privacy-safe trace or report.
- Surface model, live/replay/cached mode, telemetry, quota, and privacy status.

    ## 4. Explicit non-goals

    - Rendering hidden chain-of-thought.
- Acting as policy or authorization authority.
- Showing secrets or raw local content in generic logs.
- Requiring terminal syntax for ordinary users.
- Unlimited user-defined pane/plugin layouts in V1.
- Directly invoking tools around the control plane.

    ## 5. Logical architecture

    ```text
Generated API Client + Event Decoder
               |
        Deterministic UI Reducer
       /       |        |        \
Conversation Timeline Approval  Artifacts
       \       |        |        /
    Responsive Pane / Command System
```

    ## 6. Canonical workflows

    ### Live run
Create a task, subscribe to events, render ordered safe status, present approvals, recover from disconnect, and finalize.

### Replay
Load and verify a signed replay manifest, render event playback with original configuration/date, and distinguish it from live execution.

### Recovery
Resume from last acknowledged sequence, reconcile server state, ignore duplicates, identify gaps, and preserve the user's unsent draft.

### Approval
Present immutable proposal details and risk, request deliberate action, submit with current version and anti-CSRF protections, and render the resolved outcome.

    ## 7. Interfaces and integration

    - Generated TypeScript client from canonical protocol/OpenAPI.
- Deterministic event reducer and replay state machine.
- Approval submission with auth, anti-CSRF, and optimistic version.
- Signed replay verifier.
- Reusable typed component package consumed by lab-web.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - Each event sequence renders once and in order.
- A run has exactly one terminal state.
- Approval detail is bound to the exact run, action, resource, effect, digest, and expiry.
- Live, replay, cached, and illustrative modes are distinct.
- Unsafe arbitrary fields are never rendered as HTML or executable content.
- Full core operation works by keyboard and screen reader.
- Mobile use does not require horizontal terminal emulation.

    ## 9. Quality attributes

    - **Correctness:** typed inputs and verifiable artifacts, not ungrounded prose.
    - **Traceability:** operational steps can be reconstructed without storing hidden chain-of-thought.
    - **Security:** least privilege, deny by default, bounded egress, and approval for consequential actions.
    - **Privacy:** collection minimization and separation of public, DRL-private, and local-personal data.
    - **Reliability:** deadlines, cancellation, retry budgets, idempotency, and truthful degraded states.
    - **Accessibility:** public workflows support keyboard, screen readers, reduced motion, contrast, and mobile use.
    - **Portability:** Docker/open fixtures for baseline; Google Cloud is reference production, not a mandatory local dependency.
    - **Evaluability:** every headline claim maps to a versioned suite and release gate.

    ## 10. Milestones

    - M1 event reducer and protocol fixtures.
- M2 conversation, timeline, evidence, and artifact renderers.
- M3 approval, cancel, reconnect, and error states.
- M4 panes, command palette, tours, and replay.
- M5 accessibility, security, performance, and lab-web integration.

    ## 11. V1 acceptance

    - Protocol fixtures and malformed-stream tests pass.
- Approval E2E and comprehension testing pass.
- Live, replay, cold, degraded, failed, cancelled, and expired states are covered.
- Automated and manual accessibility review passes.
- No sensitive fixtures leak into snapshots or bundles.
- The lab-web integrated reference demo uses this console.

    ## 12. Principal risks and controls

    - Event drift: generated schemas and contract tests.
- Approval confusion: immutable details and digest-bound decision.
- Aesthetic overload: progressive disclosure and accessibility budgets.
- Stream loss: resumable sequence and state reconciliation.
- XSS: typed safe renderers and strict content sanitization.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
