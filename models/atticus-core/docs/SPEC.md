---
document_id: DRL-MODC-106
title: "Atticus Core Model System Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Core Model System Specification

    ## 1. Purpose and authority

    Atticus Core is an approximately 8–10B-class open-weight post-trained model specialized for DRL tool routing, structured arguments, permission-aware proposals, concise operational plans, grounded synthesis, coding and research assistance, and recovery. It remains replaceable behind the model gateway and is never the authorization system.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for Atticus Core Model. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - Atticus control plane and local runner.
- Open-source users with suitable local or cloud hardware.
- Researchers studying agent specialization, tool use, and evaluation.
- Contributors reproducing training or adding data and benchmarks.

    ## 3. V1 capabilities

    - Follow system/developer hierarchy and DRL tool protocol.
- Select skills and tools and emit valid structured calls.
- Recognize ambiguity, missing information, and unsupported requests.
- Propose permission-aware plans and approval summaries.
- Use deterministic tools for authoritative calculations.
- Synthesize evidence with support, contradiction, and citations.
- Recover from bounded tool errors and stop loops.
- Escalate when capability, context, or risk exceeds scope.
- Maintain context-adaptive Atticus voice without sacrificing precision.
- Serve through documented vLLM and llama.cpp-class runtimes.

    ## 4. Explicit non-goals

    - Serving as policy, identity, or approval authority.
- Memorizing private user data.
- Replacing retrieval or deterministic engines.
- Guaranteeing correctness or universal safety.
- Training from random initialization in V1.
- Requiring a proprietary closed model for core behavior.
- Autonomous self-modification or continuous hidden learning.

    ## 5. Logical architecture

    ```text
Open-Weight Candidate
 -> License / Tokenizer / Template Review
 -> Untuned Baseline Bake-off
 -> Curated SFT / Tool / Permission / Research Mixture
 -> Preference and Safety Post-training if justified
 -> EvalForge / Red Team / Integrated Agent Tests
 -> Merge / Quantize / Serve
 -> Signed Public Model Release
```

    ## 6. Canonical workflows

    ### Tool task
Read the messages and catalog; produce an exact call or concise clarification; consume the tool result; recover, continue, or stop.

### Grounded synthesis
Receive an EvidenceBundle with source identifiers; make supported claims, expose contradictions and limitations, and preserve citations.

### Approval proposal
Summarize the consequence and scope. The model may suggest risk, but deterministic policy decides.

### Escalation
Recognize insufficient capability, context, or confidence and request an approved route or human input instead of bluffing.

    ## 7. Interfaces and integration

    - Pinned chat template and tool-call grammar.
- Strict parser into DRL protocol; free-form text never reaches execution.
- OpenAI-compatible serving adapter plus direct Transformers and llama.cpp-class usage.
- Model release manifest declaring context, templates, stop tokens, quantizations, runtimes, and hashes.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - Release is reproducible from declared upstream weights, data, code, configuration, and environment.
- All license, attribution, acceptable-use, and redistribution obligations are preserved.
- Tool calls are validated and authorized outside the model.
- Private/local data is absent from the public training release.
- Held-out contamination is checked and reported.
- Each quantized artifact passes its own gates.
- Personality never overrides precision, refusal, or user control.

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

    - M1 upstream intake, license review, and baseline bake-off.
- M2 data mixture and small LoRA/QLoRA experiments.
- M3 selected SFT candidate and failure analysis.
- M4 preference/safety stage only if evidence justifies it.
- M5 quantization, serving, and integrated agent tests.
- M6 public weights, cards, reports, and reproduction package.

    ## 11. V1 acceptance

    - Upstream and redistribution rights approved.
- AtticusBench Core critical and quality slices pass.
- Integrated reference and local-tool workflows pass.
- Quantized artifacts meet quality, memory, and latency thresholds.
- Model, data, safety, license, and reproducibility cards are complete.
- Published weights/adapters, digests, signatures, and install examples validate.

    ## 12. Principal risks and controls

    - Benchmark overfitting: protected holdouts, rotations, and access logs.
- Synthetic artifacts: diverse generators, deterministic validation, and human review.
- Tool-template brittleness: runtime matrix and parser contracts.
- License incompatibility: upstream and data source review.
- Unsafe confidence: uncertainty and escalation training/evaluation.
- Compute limits: parameter-efficient training and explicit cloud budgets.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
