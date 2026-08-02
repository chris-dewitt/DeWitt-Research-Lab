---
document_id: DRL-MODE-106
title: "Atticus Edge Model System Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atticus Edge Model System Specification

    ## 1. Purpose and authority

    Atticus Edge is an approximately 2–4B-class open-weight model optimized for fast local operation: intent and skill routing, simple structured tool proposals, short voice commands, concise local assistance, and calibrated escalation to Atticus Core when complexity, risk, context, or uncertainty exceeds its scope.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for Atticus Edge Model. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Atticus Local Runner on ordinary consumer hardware.
- The public control plane as a low-cost first router where evaluation permits.
- Offline and privacy-sensitive users.
- Researchers comparing specialization, distillation, quantization, and scale.

    ## 3. V1 capabilities

    - Classify intent and skill and identify required capabilities.
- Emit simple schema-valid calls for approved low-risk tools.
- Recognize consequential, ambiguous, or complex requests and escalate.
- Handle short voice-style commands, corrections, and confirmations.
- Guide users through bundled DRL documentation offline.
- Summarize bounded local tool results.
- Operate in quantized llama.cpp/Ollama-class runtimes with low memory and latency.

    ## 4. Explicit non-goals

    - Complex multi-service research synthesis.
- Long autonomous coding or research trajectories.
- Authorization or high-risk decisions.
- Pretending success when Core or cloud is unavailable.
- Memorizing broad factual knowledge instead of retrieval.
- Requiring a discrete GPU for the baseline quantized experience.

    ## 5. Logical architecture

    ```text
Small Open-Weight Candidate or Distilled Student
 -> Edge Task/Data Subset + Reviewed Teacher Traces
 -> SFT / Distillation
 -> Escalation Calibration
 -> Quantization / Device Matrix
 -> Local Runner Integration
 -> Signed Public Release
```

    ## 6. Canonical workflows

    ### Voice and local routing
Interpret a short request, choose a local capability or clarification, execute only after deterministic policy, and summarize the result.

### Escalation
Recognize a task outside Edge's tested envelope and produce a structured escalation reason plus the minimum context references needed by Core or a human.

### Offline
Use local documentation, indexes, models, and tools; clearly name unavailable cloud specialists; never silently transmit data.

    ## 7. Interfaces and integration

    - A compatible subset of the DRL chat and tool protocol.
- Edge capability manifest listing supported tasks, skills, context, and device profiles.
- Structured escalation object validated by deterministic routing.
- Quantized local release plus optional server format and exact runtime templates.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - Edge cannot expand permissions or authorize effects.
- Unsupported or low-confidence tasks escalate rather than bluff.
- Offline mode has no hidden network call.
- Each quantized artifact passes separate evaluation.
- Training and teacher data retain rights and provenance.
- Resource use stays within declared profiles.
- Core and Edge protocol semantics cannot diverge silently.

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

    - M1 Edge task boundary and device profiles.
- M2 small-model candidate bake-off.
- M3 reviewed SFT/distillation data and pilot training.
- M4 escalation calibration and quantization.
- M5 voice, offline, and local-runner integration.
- M6 public release and comparative research report.

    ## 11. V1 acceptance

    - Intent, tool, and escalation gates pass by critical slice.
- Quantized baseline runs on declared CPU/RAM and optional GPU profiles.
- Voice/first-response latency meets approved thresholds.
- No critical consequential action occurs because of Edge output in the gated runtime.
- Offline network/privacy test passes.
- Public weights, cards, install examples, and Core comparison are available.

    ## 12. Principal risks and controls

    - Overconfidence: train out-of-scope recognition and calibrate escalation.
- Teacher-error inheritance: deterministic validation and human review.
- Device fragmentation: bounded reference matrix and community reports.
- Quantization loss: per-artifact evaluation.
- Scope creep: explicit Edge skill allowlist and capability card.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
