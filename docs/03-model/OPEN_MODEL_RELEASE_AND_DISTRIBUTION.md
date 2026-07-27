---
document_id: DRL-MOD-014
title: "Atticus Open Model Release, Packaging, and Distribution Plan"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Atticus Open Model Release, Packaging, and Distribution Plan

## Release objective

An Atticus model release should be independently useful, not an opaque weight file that only works inside DRL. The release must support researchers who want to evaluate the model, developers who want to integrate it, learners who want to understand post-training, and users who want to run it locally.

## Official artifact matrix

| Artifact | Core | Edge | Requirement |
|---|---:|---:|---|
| Safetensors weights/adapters | yes | yes | upstream terms permit redistribution |
| Merged weights | preferred | preferred | license and technical review |
| LoRA/PEFT adapter | yes | yes | published even when merged weights exist |
| GGUF quantizations | selected Q4/Q5/Q8 | selected Q4/Q5/Q8 | llama.cpp compatibility and quality evaluation |
| vLLM serving profile | yes | optional/yes | exact parser/template flags |
| llama.cpp server profile | supported if architecture permits | yes | local reference path |
| Ollama template | yes where useful | yes | generated from verified release metadata |
| Colab evaluation notebook | yes | yes | no production hosting claim |
| Colab/Vertex training recipe | yes | yes/distillation | public-data reproduction path |
| Model card | yes | yes | Hugging Face-compatible metadata |
| Safety/evaluation report | yes | yes | signed artifact reference |
| License/notice bundle | yes | yes | exact upstream and derivative obligations |

## Repository organization

Official release repositories use clear separation:

```text
model-repo/
  README.md                 # model card
  LICENSES/
  NOTICE
  release-manifest.json
  config.json
  tokenizer files
  chat_template.jinja
  tool-parser.md
  generation_config.json
  eval/
  reports/
  examples/
  checksums.txt
```

Large training code and datasets remain in the canonical DRL monorepo or dedicated dataset repositories, linked by immutable revision.

## Naming and lineage

Names include family, role, base identifier, and semantic version without claiming unsupported scale. Every artifact stores parent/base lineage. Quantizations add precision and runtime suffixes but do not receive independent quality claims without evaluation.

## Hugging Face release

The Hub model card must provide intended use, limitations, base model, license, training data summary, training procedure, evaluation, environmental/hardware notes, citation, contact, and links to source. Community evaluation submissions are welcomed through the defined process.

Dataset and benchmark repositories use dataset cards, exact license metadata, versioned files, and paper links. DRL Collections may group a release train but do not replace individual cards.

## Local packaging

The local quickstart should allow:

```text
1. download or pull a verified model;
2. launch an OpenAI-compatible local server;
3. run a tool-call smoke test;
4. run an AtticusBench mini suite;
5. connect the Atticus runtime;
6. inspect model identity and artifact digest.
```

The release documentation provides Windows, Linux, and container paths where support is actually tested.

## Supply-chain evidence

Release automation generates:

- checksums;
- SBOM for serving/training images;
- source and build provenance;
- signature/attestation where the release pipeline supports it;
- dependency and license inventory;
- reproducible command transcript;
- artifact-to-report links.

## Withdrawal and supersession

A release can be marked deprecated, withdrawn from official recommendation, or superseded. The model card remains accessible with the reason, affected use, mitigation, and replacement. DRL does not pretend already distributed weights can be recalled.
