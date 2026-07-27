---
document_id: DRL-MOD-015
title: "Open Model Ecosystem Candidate and Runtime Register"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Open Model Ecosystem Candidate and Runtime Register

## Status

This is a foundation shortlist verified against official sources on 2026-07-26. It is not the base-model selection. Mission 08 must refresh exact revisions, licenses, model cards, runtime support, and hardware requirements immediately before the bake-off.

## Core candidates

### Qwen 3.5 9B class

- official model repository indicates Apache-2.0 artifacts;
- strong candidate for tool use, structured output, multilingual work, and common serving runtimes;
- exact tool parser, chat template, context profile, and quantization support must be locked;
- official source: `https://huggingface.co/Qwen/Qwen3.5-9B`.

### Ministral 3 8B class

- Mistral announced 3B, 8B, and 14B variants under Apache 2.0;
- candidate for Core/Edge consistency, local deployment, vision, and native function calling;
- use the current model card rather than the older 2024 Ministral releases, which had different license terms;
- official source: `https://mistral.ai/news/mistral-3/` and exact Hugging Face model card at bake-off.

### Gemma 4 E4B/12B class

- Google documents Gemma 4 as open-weight and agent-oriented;
- custom Gemma terms require separate license and redistribution review and should not be described automatically as OSI open-source;
- valuable because DRL uses Google Cloud/Colab and official fine-tuning guidance;
- official sources: `https://ai.google.dev/gemma/docs/core` and `https://ai.google.dev/gemma/terms`.

## Edge candidates

- Qwen 3.5 4B class, with Apache-2.0 model card and documented tool-serving path;
- Ministral 3 3B class, subject to exact release card and runtime validation;
- Gemma 4 E2B/E4B or current compact function-calling variant, subject to terms and latency evaluation;
- a sub-billion specialist router only if it materially improves wake-to-intent latency without creating unacceptable routing risk.

## Teacher and comparison candidates

Larger open-weight models may serve as synthetic-data teachers or evaluation baselines even when they cannot be the deployed model. Teacher use must record license, provider/runtime, generated-data provenance, and review requirements. Commercial hosted teachers are allowed for synthetic generation under the data policy but are never required to run public Atticus.

## Runtime register

### Hugging Face ecosystem

Transformers, Datasets, TRL, and PEFT form the default post-training and distribution ecosystem. Exact versions are pinned. Model-card and dataset-card metadata are treated as release requirements.

### vLLM

Primary cloud-serving candidate because it provides open-weight serving, OpenAI-compatible interfaces, structured/tool-call support for many models, and benchmark tooling. The exact model parser and template must be validated; “supported model” does not guarantee Atticus-level tool reliability.

### SGLang

Secondary cloud-serving candidate for performance and model support. It receives a bake-off rather than being included solely for logo breadth.

### llama.cpp

Primary local/edge serving candidate because it supports broad hardware, quantization, an OpenAI-compatible server, schema-constrained output, and tool-use paths. Every GGUF release is evaluated separately from full precision.

### Ollama

Convenience distribution and local-development adapter. Official DRL quality claims point to the underlying model digest and runtime configuration, not only an Ollama tag.

## Selection principle

The winning model/runtime pair must satisfy the open artifact standard, not merely obtain the highest aggregate benchmark score. A slightly weaker model with permissive terms, reliable tool parsing, reproducible post-training, local deployability, and broad community support may be a better institutional choice than a marginally stronger but restrictive or opaque candidate.
