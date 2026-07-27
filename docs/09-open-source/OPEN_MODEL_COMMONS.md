---
document_id: DRL-OSS-008
title: "Atticus Open Model Commons and Community Research Program"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Atticus Open Model Commons and Community Research Program

## Identity

Atticus is not only the intelligence behind DeWitt Research Laboratory; the Atticus model family is the laboratory's primary contribution to the open-model commons. DRL's aim is to make reliable local agent behavior easier to study, reproduce, teach, and improve. The models are valuable only as part of a larger commons containing datasets, evaluation environments, training recipes, tool schemas, policy tests, runtime profiles, and public discussion of failures.

## Commons components

The V1 commons contains:

- **Atticus Core:** the principal orchestration and synthesis model;
- **Atticus Edge:** a smaller local model for routing, voice-adjacent interactions, approvals, and escalation;
- **AtticusBench:** public benchmark taxonomy, scoring code, public cases, protected cases, and community-evaluation protocol;
- **Atticus Data Commons:** public SFT/preference/tool-use records that pass rights, privacy, quality, and contamination review;
- **Atticus Recipes:** Colab notebooks, Vertex jobs, containers, configs, and exact dependency locks;
- **Atticus Runtime Profiles:** vLLM/SGLang-compatible cloud profiles and llama.cpp/GGUF-compatible local profiles where supported;
- **Atticus Skills Commons:** typed, permission-declared skills and reference specialist adapters;
- **Atticus Safety Commons:** prompt-injection tests, approval-boundary tests, policy scenarios, and failure reports;
- **Atticus Research Archive:** release papers, ablations, model cards, dataset cards, and independent replication links.

## Distribution channels

Official releases should be available through multiple open ecosystems rather than requiring the DRL website:

- GitHub for source, issues, ADRs, and release manifests;
- Hugging Face for model, dataset, benchmark, card, and community evaluation artifacts;
- OCI-compatible container registry for reproducible serving and training images;
- PyPI for Python SDKs and EvalForge/Atticus tooling;
- npm for TypeScript SDKs and terminal UI components where appropriate;
- GGUF-compatible distribution and Ollama templates for local use when licensing and runtime support permit;
- Zenodo or another archival service for DOI-bearing research snapshots when appropriate.

Each channel links back to the canonical release manifest. A release is not complete because one upload succeeds.

## Community evaluation

DRL welcomes third-party evaluations, including results that contradict official reports. Community submissions must identify model revision, quantization, runtime, hardware, prompt/template, tool parser, benchmark version, and any deviations. EvalForge should provide a standard bundle and validate the submission before displaying it.

Official and community scores remain visually distinct. DRL may reject malformed, unverifiable, contaminated, or unsafe submissions, but it must not suppress valid unfavorable results merely because they damage a headline metric.

## Community data contributions

Public contribution paths include:

- original tool-use tasks;
- adversarial permission and prompt-injection cases;
- failure recovery trajectories;
- multilingual tasks;
- accessibility-oriented interaction examples;
- specialist-system routing cases;
- high-quality corrections to synthetic examples;
- annotations and disagreement labels;
- independent benchmark slices.

Every contribution requires provenance, rights declaration, contributor attestation, and review class. Personal or employer data is not accepted. Donated user traces use a separate explicit-consent pipeline and never enter the public corpus automatically.

## Training transparency

DRL will publish enough information to understand the post-training contribution of each release:

- base model and exact revision;
- license compatibility decision;
- public/private/synthetic mixture proportions;
- record counts after filtering and deduplication;
- generation models used for synthetic data;
- human review rates by category;
- training stages and key hyperparameters;
- ablations that materially influenced architecture or data choices;
- baseline-versus-release metrics;
- quantization effects;
- safety and failure analysis;
- known non-reproducible elements, such as nondeterministic cloud hardware behavior.

Private or local-personal data may improve a private adapter, but it is excluded from official public weights unless a separate rights and consent decision is made.

## Base-model pluralism

The laboratory does not define its identity by loyalty to one vendor. Base models are selected through a license-reviewed bake-off. The candidate register should include permissively licensed models such as current Qwen and Mistral releases, and may include custom-license open-weight models such as Gemma for comparative research. The final label and redistribution plan depend on the selected upstream model.

DRL should preserve compatible runtime and protocol layers so contributors can test other open models without forking the whole platform. The official release may select one Core and one Edge base, but the evaluation harness remains pluralistic.

## Release governance

A public Atticus release requires approvals from model/data, evaluation, security, licensing, and the director. Release review verifies:

- upstream terms and notices;
- artifact checksums and signatures/attestations;
- data rights and contamination reports;
- benchmark threshold and critical-failure gates;
- model card and safety report;
- runtime compatibility;
- local installation path;
- reproducibility badge;
- public correction and withdrawal plan.

A compromised or materially misrepresented model can be withdrawn from official recommendation without attempting to erase already granted rights.

## Community recognition

Model and dataset cards should name substantive contributors. Release notes recognize evaluation, data, documentation, runtime, security, and teaching work—not only training-code authors. Research authorship follows scholarly contribution criteria rather than repository status.

The website should display a living commons map: upstream base models, core open-source dependencies, DRL derivatives, community adapters, independent evaluations, and research outputs. Atticus should be able to explain this lineage in plain language.
