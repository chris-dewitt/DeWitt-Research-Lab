---
document_id: DRL-MODC-107
title: "Atticus Core Training Recipe"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Atticus Core Training Recipe

## Stages

1. **Candidate intake:** model card, license, weights/tokenizer/template digests, architecture, context, supported runtimes, hardware estimate, known limits.
2. **Untuned baseline:** identical AtticusBench and capability-retention suites before exposure to training data.
3. **Data freeze:** versioned mixture, rights register, deduplication/contamination report, category-specific review, and held-out separation.
4. **SFT pilot:** LoRA/QLoRA sweep over learning rate, rank, sequence length, packing, loss masking, and data mix; preserve all configs and failures.
5. **Selected training:** Colab for smoke experiments; Vertex AI or reproducible GPU job for durable candidate; checkpoints to Cloud Storage.
6. **Preference/safety stage:** only for measured failure classes; reviewed pairs; capability-retention tests; no fashionable optimizer without evidence.
7. **Merge and export:** publish adapters and/or merged weights if upstream terms permit; preserve exact scripts.
8. **Quantization:** create GGUF and any approved server format separately; evaluate each.
9. **Integrated testing:** serve through vLLM and llama.cpp-class runtimes; run control-plane trajectory, security, latency, and load suites.
10. **Release:** sign artifacts and publish model, data, safety, license, evaluation, and reproducibility cards.

## Data mixture

Tool selection and arguments; multi-turn recovery; routing and escalation; permission and approval behavior; grounded research and citations; coding/repository workflows; deterministic-calculation discipline; ambiguity and clarification; safe refusal; concise operational plans; Atticus voice; and capability retention. Mixture weights are experiment configuration and must be reported.

## Reproducibility record

Each run records repository revision, data manifest, upstream digest, environment/container and package lock, hardware, seeds, hyperparameters, checkpoint schedule, losses, throughput, memory, cost, failures, and artifact digests. External trackers may receive privacy-safe metadata; local JSON/Parquet records are canonical.

## Stop conditions

Stop on unresolved rights, held-out contamination, unexplained data corruption, numerical instability, runaway budget, critical capability collapse, or unsafe checkpoint durability. Expensive runs do not continue merely for curiosity after an integrity gate fails.
