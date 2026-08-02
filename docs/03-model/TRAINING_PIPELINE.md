---
document_id: DRL-MOD-005
title: "Atticus Training and Post-Training Pipeline"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Atticus Training and Post-Training Pipeline

## Pipeline stages

```text
source registration
 -> license/privacy classification
 -> normalize and deduplicate
 -> generate candidates
 -> deterministic validation
 -> human review/quarantine
 -> dataset version and split freeze
 -> base benchmarks
 -> SFT pilots
 -> mixture/recipe ablations
 -> preference or trajectory optimization
 -> safety tuning
 -> Core selection
 -> Edge distillation/tuning
 -> quantization
 -> complete evaluation
 -> release review and publication
```

## Environments

- Colab: exploration, data inspection, smoke/pilot QLoRA, educational notebooks.
- Vertex AI custom jobs: repeatable training/evaluation with pinned containers and persistent artifacts.
- Cloud Storage: immutable dataset manifests, checkpoints, reports; lifecycle policies by class.
- Experiment tracker: MLflow-compatible or selected system behind an exportable metadata schema.
- EvalForge: all benchmark execution and comparison.

## Reproducibility record

Every run records:

- run ID and purpose;
- git commit and dirty-state check;
- container digest and dependency lock;
- upstream model ID/revision/license snapshot;
- dataset IDs, manifests, filters, and split hashes;
- seed(s);
- method and full hyperparameters;
- hardware, region, runtime, and wall-clock;
- checkpoint intervals and storage URIs;
- metrics during training;
- evaluation suite versions;
- cost estimate/actual;
- final artifact hashes;
- investigator notes and anomalies.

## SFT baseline

Use Hugging Face Transformers, PEFT, and TRL or an approved equivalent. Begin with QLoRA/LoRA to establish data and evaluation behavior before considering full fine-tuning. Pilot target modules and rank are model-specific and tested rather than copied blindly.

## Data mixtures

Maintain named mixtures, for example:

- `atticus-core-balanced`;
- `atticus-core-safety-heavy`;
- `atticus-edge-route-heavy`;
- `atticus-repo-specialist`.

A mixture manifest lists category counts, weights, sources, review status, and exclusions. Report performance by category to detect improvements caused only by oversampling easy tasks.

## Preference optimization

Use only after SFT has stable structured behavior. Candidate methods include DPO and other supported approaches. Preference pairs must explain the defect: unauthorized action, unnecessary tool, unsupported certainty, bad recovery, poor style, or incorrect evidence. Avoid preference data dominated by cosmetic wording.

## Environment optimization

Reinforcement/trajectory optimization is optional and gated. It requires deterministic mock environments, reward decomposition, reward-hacking tests, held-out environments, and evidence that simpler SFT/preferences are insufficient.

## Checkpoint policy

- save outside ephemeral notebook disk;
- never overwrite release candidate;
- retain best-by-category candidates, not only training loss;
- evaluate checkpoint before promotion;
- support resume and verify data order;
- delete intermediate artifacts only under lifecycle policy after manifest retention.
