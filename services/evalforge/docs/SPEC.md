---
document_id: DRL-EVL-107
title: "EvalForge System Specification"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-28
---


    # EvalForge System Specification

    ## 1. Purpose and authority

    EvalForge makes DeWitt Research Workshop claims testable. It defines versioned evaluation suites, executes local and cloud experiments, stores immutable evidence, compares candidates with accepted baselines, calibrates human and model judges, generates reports, and enforces pull-request and release gates.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for EvalForge. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Every DRL project owner defining and proving claims.
- Model researchers benchmarking Atticus Core and Edge.
- Security reviewers running adversarial suites.
- Contributors adding evaluators, adapters, datasets, or reporters.
- Public visitors inspecting truthful benchmark reports.
- CI and release automation.

    ## 3. V1 capabilities

    - Define suites, cases, targets, scorers, slices, and gates in typed manifests.
- Execute deterministic, model, RAG, tool-use, trajectory, security, latency, and cost evaluations.
- Support local functions, HTTP services, OpenAI-compatible endpoints, and trace imports.
- Record complete reproducibility metadata and immutable artifacts.
- Compare baseline and candidate using paired analysis, uncertainty, and slices.
- Calibrate LLM judges against human-reviewed samples.
- Generate JSON, Markdown, HTML, JUnit, and signed release reports.
- Gate pull requests, model promotion, and coordinated V1 release.

    ## 4. Explicit non-goals

    - One universal quality or safety score.
- Treating LLM judges as ground truth.
- Publishing private or held-out benchmark content.
- Repeatedly optimizing on hidden tests without contamination records.
- Replacing project owners' claim definitions.
- Guaranteeing real-world safety from benchmark performance.

    ## 5. Logical architecture

    ```text
Suite / Dataset Registry -> Runner / Scheduler -> Target Adapters
         |                       |
   Scorers / Judges        Traces / Artifacts
         \                       /
          Result Store -> Analysis / Comparison
                         -> Reports / Gates / Leaderboards
```

    ## 6. Canonical workflows

    ### Pull-request regression
Resolve changed components and required suites; run fast deterministic, security, and sampled model tests; compare against accepted baseline; annotate the PR; block critical regression.

### Model release
Freeze data, model, runtime, prompts, tools, and configuration; execute multi-seed and slice evaluations; calibrate judges; analyze failure clusters; generate signed model and safety reports.

### Online trace sampling
Receive consented and privacy-filtered traces; sample by declared policy; evaluate asynchronously; aggregate operational signals without silently adding traces to training.

    ## 7. Interfaces and integration

    - Python SDK and `evalforge` CLI.
- Suite and dataset manifest formats.
- Run, result, comparison, report, baseline, gate, and leaderboard APIs.
- Target, scorer, judge, reporter, and trace-adapter plugin interfaces.
- EvaluationResult and signed report schemas consumed by CI and the website.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - Every score identifies data, target, scorer, code, configuration, environment, and time.
- Held-out access and contamination events are logged.
- Critical deterministic and security failures cannot be averaged away.
- Judge scores disclose model, prompt, version, calibration, and limitations.
- Private cases and raw sensitive results remain access-controlled.
- Baseline promotion is explicit and approved.
- Website metrics derive from immutable signed reports.

    ## 8.1 Prototype held-out permission/trajectory suite

    The runnable prototype ships
    `evalforge.held_out.permission_trajectory` with separate `terminal_outcome`
    and `trajectory` metrics, allow/deny/approval/injection slices, and a hard
    `gate_decision=fail` whenever unauthorized actions appear in
    `critical_failures`. Maturity: prototype (synthetic Atticus fixtures; not a
    full AtticusBench or signed public leaderboard).

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

    - M1 manifests, schemas, deterministic local runner, and self-tests.
- M2 result store, comparison, reports, and CI output.
- M3 model, RAG, tool, trajectory, and trace adapters.
- M4 human review, judges, calibration, and statistics.
- M5 security, online trace, cost, and load suites.
- M6 signed reports, public leaderboard, and full release gating.

    ## 11. V1 acceptance

    - All V1 claims map to suites and gates.
- Local fast suites and cloud full suites reproduce.
- Paired candidate/baseline comparison handles uncertainty and slices.
- Judge calibration and held-out access controls pass review.
- CI blocks a seeded critical regression.
- Public report and integrated Atticus trace evaluation work end-to-end.

    ## 12. Principal risks and controls

    - Metric gaming: claim-specific suites, hidden/rotating sets, and failure review.
- Judge bias: human calibration, multiple methods, and limitations.
- Contamination: registry, access logs, and deduplication.
- Cost explosion: tiered suites, caching, budgets, and early stop.
- False confidence: uncertainty, slice analysis, limitations, and real incident feedback.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
