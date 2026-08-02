---
document_id: DRL-MOD-009
title: "Quantization and Runtime Qualification"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Quantization and Runtime Qualification

## Artifacts

Evaluate:

- BF16/FP16 reference;
- runtime-supported FP8 where appropriate;
- 8-bit weight quantization;
- 6/5/4-bit GGUF variants;
- other formats only when maintained and useful.

## Qualification metrics

- AtticusBench category scores;
- schema/tool-call validity;
- permission errors;
- citation and calculation consistency;
- perplexity/general benchmark sanity where useful;
- startup and model-load time;
- memory and disk size;
- tokens/s and time to first token;
- concurrency;
- long-context degradation;
- runtime/tool-parser compatibility.

A quantization is not released solely because it loads. Safety/tool regressions can differ from broad language quality.

## Runtime targets

- vLLM or SGLang for managed GPU throughput after measured comparison;
- llama.cpp server/GGUF for local CPU/GPU portability;
- Ollama may be supported as a convenience wrapper, not the canonical protocol;
- all runtimes sit behind the model gateway and expose exact model/runtime identity.
