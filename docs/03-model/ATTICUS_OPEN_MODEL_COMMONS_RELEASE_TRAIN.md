---
document_id: DRL-MOD-016
title: "Atticus Open Model Commons Release Train"
version: 3.2.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Atticus Open Model Commons Release Train

## Program identity

Atticus is not a single checkpoint. It is a maintained family of open agent research artifacts whose purpose is to make local, inspectable, permission-aware AI useful to ordinary people and researchers.

The Commons contains:

- **Atticus Core:** primary orchestration, research synthesis, coding assistance, and specialist routing model;
- **Atticus Edge:** compact low-latency model for intent routing, voice/local operation, simple tool selection, and constrained hardware;
- **Atticus Adapters:** task, language, safety, and research adapters when modular release is more useful than a merge;
- **AtticusBench:** public benchmark framework with governed hidden cases;
- **Atticus Data Commons:** reviewed public training/evaluation mixtures, manifests, synthetic generation recipes, and rights records;
- **Runtime Profiles:** cloud and local serving configurations;
- **Replication Archive:** community evaluations, failed reproductions, corrections, and compatible forks.

## Internal release train

The public V1 launches as one coordinated program, but internal artifacts progress through evidence gates:

1. **Candidate register:** eligible base models and rights review.
2. **Baseline freeze:** exact revisions, templates, parsers, and runtime versions.
3. **Pilot adapter:** small reviewed dataset proves the training/evaluation loop.
4. **Research candidate:** broader SFT and preference data; red-team and tool tests.
5. **Release candidate:** artifact matrix complete; quantizations and runtimes verified.
6. **Public V1:** Core and Edge release lineage, cards, recipes, evals, and local quickstart published together.
7. **Maintenance release:** corrections, runtime compatibility, safety improvements, and data lineage updates.

No stage is publicly described as stable before the corresponding maturity evidence exists.

## Base-model selection

The bakeoff evaluates current compact model families with exact card and license review at execution time. Permissively licensed candidates receive an openness advantage because they simplify redistribution, education, forks, and commercial reuse, but quality and safety remain mandatory. Custom-license open-weight models can be comparative baselines and may be selected only with precise labeling and a sustainable distribution plan.

The bakeoff records:

- tool-call and structured-output reliability;
- policy and approval behavior;
- coding and research synthesis;
- prompt-injection robustness;
- latency, memory, throughput, and context behavior;
- Transformers, vLLM/SGLang, and llama.cpp support;
- license, preferred modification materials, and redistribution rights;
- community health and upstream contribution opportunities;
- fine-tuning and quantization quality.

## Required public artifacts

For each public model role:

- exact upstream identity and terms;
- adapters and merged weights when permitted;
- selected safetensors and GGUF artifacts;
- tokenizer/chat template/tool parser;
- training code and pinned configuration;
- dataset manifest and review statistics;
- model card, safety report, evaluation report, and limitations;
- runtime profiles and smoke tests;
- checksums, release manifest, SBOM/provenance for images;
- Colab evaluation and bounded training notebook;
- local quickstart for Windows and Linux;
- citation metadata and contributor credits.

## Community submission lanes

The Commons accepts:

- independent evaluation results;
- additional runtime/quantization reports;
- rights-cleared dataset improvements;
- language/accessibility adapters;
- tool-call parsers and templates;
- adversarial and failure cases;
- teaching notebooks;
- downstream applications and compatible forks.

Submissions do not enter an official release until provenance, license, quality, privacy, and regression review pass.

## Long-term research questions

- How small can a trustworthy local orchestration model become?
- Which permission and approval behaviors survive quantization?
- When should Edge defer to Core or a specialist?
- Can tool policies be made portable across model families?
- Which synthetic-data strategies improve reliability without collapsing diversity?
- How should community failure reports influence training without overfitting the benchmark?
