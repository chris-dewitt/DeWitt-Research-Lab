---
document_id: DRL-MOD-002
title: "Base Model Bake-Off and Selection Protocol"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Base Model Bake-Off and Selection Protocol

## Principle

Select upstream models by DRL evidence, not popularity. The shortlist is refreshed immediately before the bake-off because open-weight models change rapidly.

## Initial 2026 research shortlist (verified 2026-07-26)

The starting research register should include:

- Qwen 3.5 9B- and 4B-class candidates whose official model cards identify Apache-2.0 artifacts;
- Mistral 3 / Ministral 3 candidates in 8B and 3B classes, with exact current model cards and Apache-2.0 terms revalidated;
- Gemma 4 E4B/12B or other compact candidates after separate custom-terms review and precise open-weight labeling;
- specialist function-calling models as micro-router or teacher candidates;
- a strong open coding-agent model as a teacher/baseline even if too large for Core deployment.

This is a shortlist, not a selection. Candidate metadata lives in a versioned YAML register with exact revision, date, license, architecture, context, runtimes, and required parsers.

## Eligibility screen

A candidate is excluded before expensive tests if:

- release or redistribution terms are incompatible;
- exact weights/revision are unavailable;
- required runtime cannot load the model reproducibly;
- tool-call format cannot be parsed reliably;
- memory exceeds target deployment without a viable quantization;
- known restrictions conflict with intended use;
- tokenizer/template ambiguity cannot be resolved.

## Evaluation stages

### Stage A — static and runtime

- license and notice review;
- download/checksum;
- tokenizer/template test;
- JSON/schema constrained generation;
- vLLM/SGLang and llama.cpp compatibility where applicable;
- memory and startup measurements;
- context-length smoke test;
- deterministic seed behavior where supported.

### Stage B — zero/few-shot baseline

Use frozen prompts and identical tools on:

- routing;
- tool selection;
- argument validity;
- policy recognition;
- evidence synthesis;
- repository tasks;
- recovery;
- prompt injection;
- latency/cost.

### Stage C — pilot fine-tune

Train a small common LoRA/QLoRA dataset with identical mixture and budget. Evaluate improvement, stability, catastrophic regression, and data efficiency.

### Stage D — deployability

- Cloud Run GPU cold/warm latency;
- local Q4/Q5/Q8 memory and tokens/s;
- concurrent public workload;
- context/KV pressure;
- structured-output failure under load;
- model-server operational maturity.

## Weighted selection score

| Dimension | Core weight | Edge weight |
|---|---:|---:|
| Tool and schema reliability | 20 | 25 |
| Permission/safety behavior | 20 | 20 |
| Task completion and synthesis | 15 | 8 |
| Routing and escalation | 10 | 20 |
| Coding/repository ability | 10 | 5 |
| Grounding/citations | 10 | 5 |
| Local/cloud performance | 8 | 12 |
| License/ecosystem/reproducibility | 7 | 5 |

A candidate with a critical safety or license failure cannot win through weighted average.

## Statistical procedure

- evaluate paired cases;
- report bootstrap confidence intervals;
- use McNemar or paired permutation tests where appropriate;
- separate practical and statistical significance;
- inspect category-level and worst-case results;
- perform blinded human review on a stratified sample;
- publish failures, not only aggregate score.

## Decision output

The selection ADR includes winner, runner-up, rejected candidates, measurements, known weaknesses, deployment profile, planned data mixture, fallback, and conditions that trigger reselection.

## Open-ecosystem selection factor

The institutional score includes more than license permissiveness. Review the availability of preferred modification materials, post-training documentation, local quantizations, maintained runtimes, public tool parsers, community evaluation, and the feasibility of contributing fixes upstream. The selection ADR states whether the resulting Atticus release is OSI open-source AI, an open-weight derivative, or another accurately described category.

The current candidate and source register is `MODEL_ECOSYSTEM_CANDIDATE_REGISTER.md`.
