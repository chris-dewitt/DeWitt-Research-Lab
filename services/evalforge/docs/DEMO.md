---
document_id: DRL-EVL-103
title: "EvalForge Demonstration and Portfolio Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-01
---


    # EvalForge Demonstration and Portfolio Specification

    ## Purpose

    Maturity: **prototype** signed fixture replays (DRL-019) verify digests locally.
    The demonstration proves the most important engineering claims of EvalForge. Every visible result is live, replayed from a signed real trace, cached from a dated artifact, or clearly marked illustrative.

    ## Signature story

    A visitor compares two Atticus configurations. EvalForge runs the same held-out tool-use and citation cases, displays paired quality, latency, cost, and security changes, reveals failure slices, and issues a PR-style recommendation tied to exact artifacts.

    ## Modes

    - Signed comparison replay.
- Limited live small suite.
- Failure explorer.
- Public leaderboard and method card.
- CI gate simulation.

    ## Guided sequence

    - Select baseline and candidate.
- Inspect suite and claims.
- Run or replay samples.
- View paired metrics and uncertainty.
- Inspect critical failures and slices.
- Review judge calibration.
- See gate decision and exception policy.
- Verify the report manifest and signature.

    ## Safety and boundedness

    - Public data and targets only.
- No arbitrary code execution.
- Compute caps and private holdout isolation.
- Raw harmful content is safely rendered or redacted.
- No claim that a benchmark guarantees general safety.

    ## Measurements shown

    - Task and metric deltas.
- Confidence intervals and sample counts.
- Critical failures and slices.
- Latency, cost, and run completeness.
- Tool, policy, citation, and security metrics.
- Artifact digests and signature status.

    ## Failure and fallback

    - Unavailable live target uses signed report replay.
- Failed samples remain visible and are excluded only by declared rule.
- Judge outage yields deterministic/human-required status, not invented score.
- Budget stop produces an incomplete report with partial evidence.

    The demo remains keyboard-operable, useful on mobile, compatible with reduced motion, and understandable without sound. A short visual loop, 90-second tour, and technical walkthrough all derive from the same truthful evidence.
