---
document_id: DRL-MODE-102
title: "Atticus Edge Evaluation and Acceptance Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Edge Evaluation and Acceptance Specification

    ## Evaluation contract

    Evaluations test actual product/research claims. Each claim has population, threat model, metric, uncertainty treatment, slices, failure examples, owner, and release threshold. A single aggregate score is never sufficient.

    ## Claims

    - Intent, skill, and simple tool choices are accurate.
- Escalation avoids both reckless autonomy and unnecessary Core use.
- Noisy short voice commands and corrections are robust.
- Quantized local latency and memory meet declared profiles.
- Offline privacy and capability honesty hold.
- Protocol behavior remains compatible with Core and control plane.

    ## Required suites

    - AtticusBench Edge public and private holdout.
- Escalation, abstention, and selective-risk cases.
- Noisy transcript, correction, and confirmation set.
- Simple file/repository/tool trajectories.
- Prompt injection and authority confusion.
- Quantization and device runtime matrix.
- General capability retention.

    ## Metrics and analysis

    - Intent and skill macro-F1.
- Tool and argument validity.
- Escalation precision, recall, coverage, and selective risk.
- Critical false-autonomy count.
- Correction success.
- First-token, tokens/sec, RAM/VRAM, startup, and energy/CPU where measured.
- Offline egress and task completion.

    Paired tests or bootstrap intervals are used where appropriate. Repeated tuning against a benchmark is tracked. Human and model judges include calibration, disagreement, and limitations; model-judge output is not objective truth.

    ## Release gates

    - Zero critical false authorization or effect caused by Edge in the gated runtime.
- Approved selective-risk and escalation threshold.
- Declared reference devices meet latency and memory budgets.
- Quantized quality loss stays within approved bounds.
- Protocol fixtures and offline privacy pass.

    A noncritical regression needs a time-bounded exception with user value, affected slices, mitigation, owner, expiry, and director approval. Security/privacy boundary and deterministic-correctness failures cannot be averaged away.

    ## Adversarial program

    - Ambiguous or deceptively simple destructive commands.
- Noisy paths, names, and entities.
- Prompt injection in local files.
- Repeated corrections and impatience.
- Unavailable Core or network.
- Overlong input and unknown tools.
- Persona pressure to bypass approval.

    ## Required evidence

    - Core/Edge comparison.
- Escalation and selective-risk curves.
- Device/quantization matrix.
- Failure taxonomy.
- Offline packet report.
- Signed local workflow.
- Model card and limits.

    Reports pin code, data, model/provider, prompt/template, tool, configuration, environment, sample counts, exclusions, costs, failures, and reproduction commands. Public metrics link to signed reports.
