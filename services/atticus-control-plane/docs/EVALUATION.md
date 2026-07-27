---
document_id: DRL-ATT-104
title: "Atticus Control Plane Evaluation and Acceptance Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Control Plane Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Correct specialist/tool is selected.
- Arguments satisfy schema and user intent.
- Plans are bounded, efficient, and recoverable.
- Policy and approval requirements are obeyed.
- Final results fulfill the task and remain grounded.
- Public/private/local boundaries do not cross.
- Core/Edge routing meets quality, latency, cost, and privacy objectives.

    ## Required suites

    - AtticusBench intent, skill, and specialist routing.
- Tool-call syntax and semantic argument correctness.
- Permission and approval scenarios.
- Multi-system trajectory and recovery.
- Prompt-injection and authority confusion.
- Public/private/local isolation.
- Human usability study for approvals and guided tours.
- Operational load, cold start, cancellation, and cost.

    ## Metrics and analysis

    - Task success and critical-subgoal completion.
- Tool selection precision/recall and argument validity.
- Invalid/unnecessary calls, step count, recovery success, and terminal-state correctness.
- Policy violation, missing/overbroad approval, and duplicated-effect rates.
- Citation entailment and evidence coverage.
- p50/p95 latency, first useful event, tokens, GPU seconds, and dollars per successful task.
- Slice results by model, skill, risk, session mode, language/input form, and failure condition.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - Zero known critical permission bypass, cross-mode access, duplicated consequential effect, or secret exposure.
- Deterministic state-machine and contract tests pass completely.
- Core and Edge meet approved held-out thresholds and do not materially regress from accepted baselines.
- Integrated reference workflow succeeds at the approved rate with valid citations and calculation artifacts.
- Approval comprehension and public abuse controls pass.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - Indirect prompt injection in documents and tool output.
- Unicode, encoding, JSON, and schema smuggling.
- Fake tool authority, poisoned skill descriptions, and catalog collisions.
- Approval replay, substitution, race, and stale-preview attacks.
- Cancellation and timeout at every state.
- Invalid or contradictory partial model/tool results.
- Quota evasion and cross-session trace access.

    ## Required evidence

    - Signed EvalForge baseline/candidate report.
- State-transition and contract coverage report.
- Representative failures linked to regression IDs.
- Security and unresolved-risk report.
- Cost/latency/load report.
- Approval usability notes and decisions.
- Reproduction commands and immutable config bundle.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
