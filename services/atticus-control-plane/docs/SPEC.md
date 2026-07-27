---
document_id: DRL-ATT-107
title: "Atticus Control Plane System Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Control Plane System Specification

    ## 1. Purpose and authority

    Atticus is the operating intelligence of DeWitt Research Laboratory. The control plane turns a user objective into a bounded, inspectable workflow; selects models and skills; obtains policy decisions and approvals; calls specialist systems and tools; recovers from expected failures; and produces a grounded result with a visible execution summary.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for Atticus Control Plane. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Public visitors exploring DRL through bounded anonymous or authenticated sessions.
- DeWitt using a private account and paired local runner.
- Contributors integrating skills, tools, and specialist services.
- Operators investigating traces, incidents, cost, and model regressions.
- Researchers evaluating planning, routing, permission compliance, and synthesis.

    ## 3. V1 capabilities

    - Accept conversational and structured task requests.
- Resolve user, session, environment, consent, and applicable tool catalog.
- Select a versioned skill or create a constrained plan.
- Route between Atticus Edge, Atticus Core, and approved specialist systems.
- Obtain deterministic policy decisions before every tool execution.
- Pause for scoped, expiring human approval when required.
- Execute with deadlines, cancellation, retry budgets, idempotency, and trace propagation.
- Build evidence-aware final responses and operational summaries.
- Expose replayable privacy-filtered traces.
- Emit EvalForge-compatible records for offline and sampled online evaluation.

    ## 4. Explicit non-goals

    - Unbounded autonomous browsing or execution.
- Direct possession of local OS credentials.
- Treating model output as authorization.
- Reimplementing specialist business logic.
- Persisting hidden chain-of-thought.
- Automatic training on ordinary public conversations.
- Claiming frontier general intelligence.

    ## 5. Logical architecture

    ```text
Web / API / Local Runner
          |
  Session + Identity
          |
   Task Intake Service
          |
 Skill Resolver -- Model Gateway
          |
  Orchestration State Machine
      /          |          \
 Policy      Approval      Memory
      \          |          /
       Tool / Specialist Gateway
          |
 Atlas | FedLens | BalanceLab | EvalForge | Public Tools | Paired Runner
          |
 Trace, Evidence, Cost, and Outcome Stores
```

    ## 6. Canonical workflows

    ### Public research workflow
The user submits a question; Atticus selects an approved skill; policy limits the public tool catalog; Atlas or FedLens returns evidence; deterministic tools create artifacts; Atticus synthesizes claims with citations; EvalForge grades a requested or sampled trace.

### Consequential local workflow
A private user asks Atticus to modify a repository. The control plane proposes a plan, calls the paired runner through scoped capabilities, receives a patch, requests explicit approval for apply/commit/push at the appropriate stages, and records the grants and artifacts.

### Failure recovery
Provider timeout triggers bounded retry or approved fallback. Invalid tool arguments return to repair. Approval expiry cancels the consequential step. Partial specialist success may yield a clearly degraded answer, never fabricated completion.

    ## 7. Interfaces and integration

    - Task/run/session/approval/skill/tool/trace HTTP APIs.
- DRL protocol requests, results, errors, events, evidence, claims, and artifacts.
- Internal service adapters over authenticated HTTP/JSON in V1; optional MCP adapters only under the DRL MCP security profile.
- OpenAI-compatible model serving behind a model-gateway adapter, not as the public Atticus contract.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - No tool executes without a current policy allow decision.
- No approval grant exceeds the requested action, resource, duration, session, or digest.
- Public read-only mode cannot reach private or local tools.
- Evidence-derived final claims preserve provenance identifiers.
- Cancellation propagates and a run reaches one terminal state.
- Retries cannot duplicate consequential effects.
- Safe trace views omit secrets and prohibited content.
- Fallback cannot silently weaken privacy, policy, or open-weight deployment commitments.

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

    - M1 canonical contracts and state-machine simulator.
- M2 public DRL guide over fixture skills/tools.
- M3 specialist routing and evidence synthesis.
- M4 policy, approvals, and paired-runner integration.
- M5 open-weight model gateway, evaluation, quotas, and resilient deployment.
- M6 integrated demo, security hardening, and public V1 signoff.

    ## 11. V1 acceptance

    - All legal state transitions and terminal outcomes are contract-tested.
- Public Atticus completes lab guidance and bounded specialist workflows.
- Private Atticus completes an approved local repository workflow with revocable pairing.
- Tool selection, argument validity, task success, and policy gates pass on held-out AtticusBench slices.
- No critical security or tenant/session-isolation finding remains.
- SLO, cost, rollback, incident, and integrated-demo evidence is approved.

    ## 12. Principal risks and controls

    - Agent drift: constrain with typed skills/plans, step budgets, and trajectory evaluations.
- Approval fatigue: risk-tier actions and avoid broad or ambiguous batching.
- Prompt injection: mark all retrieved/tool content untrusted and keep authority deterministic.
- Provider/runtime failure: deadline-aware routing and truthful degraded modes.
- Privacy leakage: purpose-bound trace fields, redaction, retention controls, and local/cloud separation.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
