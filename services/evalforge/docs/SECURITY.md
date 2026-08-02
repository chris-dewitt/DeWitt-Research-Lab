---
document_id: DRL-EVL-106
title: "EvalForge Security and Privacy Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # EvalForge Security and Privacy Specification

    ## Objective

    EvalForge must stay useful under hostile, malformed, ambiguous, and failure-prone inputs without giving a model authority it does not possess. Models propose. Deterministic systems authenticate, authorize, validate, constrain, execute, audit, and obtain human approval.

    ## Protected assets

    - Private and held-out datasets.
- Benchmark integrity and labels.
- Target outputs and traces.
- Baseline and gate decisions.
- Report signatures.
- Provider credentials and budgets.
- Scientific credibility.

    ## Principal threats

    - Target or output attacking runner/judge.
- Untrusted plugin code execution.
- Held-out label leakage.
- Unauthorized dataset access.
- Result or baseline tampering.
- Metric gaming and selective publication.
- Denial of wallet.
- Private content in public reports.

    ## Required controls

    - Isolated target and plugin execution.
- Typed bounded artifacts and output limits.
- Dataset ACLs, canaries, and access logs.
- Immutable versioned results and separate public/private stores.
- Signed manifests and reports.
- Budget, concurrency, and early-stop controls.
- Review for baseline promotion and report publication.
- Redaction and publication validation.

    ## Privacy behavior

    - Online evaluation uses purpose-limited consented fields.
- Public reports aggregate or redact.
- Human reviewers see only necessary content.
- Evaluation is not permission for model training.
- Users can inspect and revoke future trace donation where feasible.

    ## Public abuse controls

    - Authentication for expensive runs.
- Per-suite and per-target quotas.
- No arbitrary public plugin execution.
- Public leaderboard submissions are scanned, sandboxed, and reviewed.
- Circuit breakers protect provider and GPU spend.

    ## Verification

    - Sandbox and plugin escape tests.
- Dataset ACL and canary tests.
- Forged result/signature tests.
- Judge prompt-injection tests.
- Budget and early-stop tests.
- Cross-project isolation.
- Redaction snapshots.
- Incident exercise for leaked holdout.

    “Sanitize input,” “encrypt it,” and “use least privilege” are not evidence. Each control identifies the boundary, exact mechanism, negative test, telemetry signal, owner, and incident response.
