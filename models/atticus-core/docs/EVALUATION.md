---
document_id: DRL-MODC-101
title: "Atticus Core Evaluation and Acceptance Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Core Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Tool and skill selection and arguments are correct.
- The model understands approval and permission concepts without pretending to authorize.
- Synthesis remains grounded and cites provided evidence.
- Planning is bounded and recovery/escalation is useful.
- Coding and repository assistance produces testable improvements.
- General capability, safety, and controlled personality are retained.
- Quantized/runtime artifacts preserve declared quality and performance.

    ## Required suites

    - AtticusBench Core public and private holdout.
- Tool grammar and runtime matrix.
- Prompt injection and authority confusion.
- Research, citation, and temporal tasks.
- Sandboxed repository patch/test workflows.
- Deterministic-calculation tool compliance.
- License-compatible capability-retention set.
- Human preference and usability sample.

    ## Metrics and analysis

    - Exact and semantic tool/field accuracy.
- Task and critical-subgoal success.
- Invalid and unnecessary calls.
- Policy errors and critical unsafe proposals.
- Citation support and unsupported numeric claims.
- Recovery, escalation, code tests passed, and calibration.
- Persona control.
- Tokens/sec, first token, memory, GPU seconds, and cost.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - No critical permission, secret, or execution-boundary failure in release suite.
- Approved minimum scores and no unacceptable slice regression versus upstream and accepted candidates.
- Structured output validity passes for each runtime.
- Quantized artifacts stay within approved quality-loss and memory/latency targets.
- Integrated Atticus trajectories pass.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - Indirect injection and fake tools.
- Malformed schemas and ambiguous destructive requests.
- Long-context distractors and conflicting evidence.
- Failure loops and persona jailbreak.
- Private-data bait.
- Malicious code/repositories.
- Numeric traps and unsupported confidence.

    ## Required evidence

    - Signed EvalForge report.
- Baseline/candidate/quantization comparisons.
- Failure taxonomy.
- Human review sample.
- Contamination report.
- Runtime benchmark.
- Integrated traces.
- Model and safety cards.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
