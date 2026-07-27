---
document_id: DRL-BAL-107
title: "BalanceLab AI System Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # BalanceLab AI System Specification

    ## 1. Purpose and authority

    BalanceLab AI is an educational and research platform for synthetic financial-institution balance sheets, interest-rate and behavioral scenarios, transparent projection methods, and inspectable explanations. It demonstrates how LLM agents should invoke deterministic quantitative tools instead of improvising authoritative financial calculations.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for BalanceLab AI. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Students and teachers learning ALM and scenario analysis.
- Researchers comparing assumptions and methods.
- Atticus constructing and explaining synthetic scenarios.
- Developers adding products, scenarios, calculations, tests, or visualizations.
- Technical reviewers inspecting deterministic-AI boundaries.

    ## 3. V1 capabilities

    - Generate and load versioned synthetic institutions.
- Validate balance-sheet, product, cash-flow, curve, and assumption schemas.
- Define yield-curve, balance, pricing, deposit, funding, and behavioral scenarios.
- Run deterministic projection, NII, duration, sensitivity, and driver calculations.
- Return calculation artifacts with assumptions, method versions, formulas, and reconciliations.
- Translate natural-language requests into proposed typed scenarios for review.
- Explain results only from calculation artifacts.
- Compare scenarios and export reproducible reports.

    ## 4. Explicit non-goals

    - Employer or proprietary bank data, code, or models.
- A regulatory-compliant production ALM platform.
- Investment, accounting, or risk-management advice.
- LLM-authored authoritative numbers.
- Claims of realism beyond the documented synthetic methods.
- Arbitrary executable user models.

    ## 5. Logical architecture

    ```text
Synthetic Institution / Validated Upload
             +
Typed Scenario Definition -> Validation / Confirmation
             |
Deterministic Projection Engine
 cash flows | balances | pricing | NII | duration | sensitivities
             |
Calculation Artifact + Reconciliation
             |
Atticus Explanation / Web Workstation / EvalForge
```

    ## 6. Canonical workflows

    ### Interactive scenario
Load a sample institution; adjust curve and behavior assumptions; validate the typed scenario; run the engine; reconcile; create an immutable artifact; explain only from that artifact.

### Natural-language scenario
Atticus converts a request into proposed scenario JSON, exposes each assumption, asks for confirmation when material or ambiguous, and then invokes the deterministic engine.

### Reproduction
Load institution, scenario, method version, dependency lock, and seed from the artifact manifest; rerun and compare exact values or declared tolerances.

    ## 7. Interfaces and integration

    - Institution, scenario, run, artifact, comparison, and report APIs.
- Python library and CLI are the numerical source of truth.
- Institution, Position, Curve, Scenario, AssumptionSet, ProjectionResult, CalculationArtifact, Reconciliation, and ExplanationInput schemas.
- Public demo uses samples; upload and persistence are authenticated or ephemeral.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - Authoritative numeric fields originate only from deterministic code.
- Inputs, assumptions, units, dates, methods, and rounding are explicit.
- Accounting and cash-flow identities reconcile or the run fails.
- Explanations cannot mutate or replace calculation artifacts.
- Synthetic/public/private status is visible.
- Same manifest, seed, method, and version reproduce within declared tolerance.
- No employer material enters the project.

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

    - M1 canonical schemas and synthetic institution generator.
- M2 curve and scenario engine with validation.
- M3 projection, NII, duration, sensitivity, and reconciliation.
- M4 artifact API, storage, and scenario comparison.
- M5 Atticus scenario translator and artifact-bound explainer.
- M6 interactive workstation, evaluation, clean-room review, and release.

    ## 11. V1 acceptance

    - Synthetic fixtures and golden calculations pass independent review.
- Reconciliation invariants hold across property tests.
- Scenario schemas and method versions are fully documented.
- Explanation faithfulness and numeric-reference gates pass.
- Public demo supports multiple sample scenarios and calculation audit.
- Integrated Atticus workflow produces a valid artifact evaluated by EvalForge.

    ## 12. Principal risks and controls

    - False authority: persistent educational/synthetic labeling and limitations.
- Numeric error: golden, property, reconciliation, and independent review.
- LLM number fabrication: artifact-only explanation contract and adversarial evaluation.
- Employer contamination: clean-room policy, contributor declarations, and source audit.
- Complexity explosion: fixed V1 product/scenario catalog with explicit extension points.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
