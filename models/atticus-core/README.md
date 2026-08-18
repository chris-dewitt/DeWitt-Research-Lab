---
document_id: DRL-MODC-100
title: "Atticus Core Project README"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-17
---

# Atticus Core

**Maturity:** `specified`

Atticus Core is a proposed open-weight model research track for routing, tool
use, grounded synthesis, coding, and research. No upstream model has been
selected, no DRL weights have been trained, and no release artifact exists.
Selection remains gated by the documented bake-off, licensing, and evaluation
process.

## Intended contents

- Reproducible training and evaluation recipes.
- Data manifests and license evidence.
- Adapter, merge, and quantization tooling.
- Model cards and signed release metadata.
- Registry references by digest rather than committed weight files.

## Required reading

- [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/TRAINING_RECIPE.md`](docs/TRAINING_RECIPE.md)
- [`docs/EVALUATION.md`](docs/EVALUATION.md)
- [`docs/SAFETY_AND_LICENSE.md`](docs/SAFETY_AND_LICENSE.md)
- [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)
- [`BASE_MODEL_BAKEOFF.md`](../../docs/03-model/BASE_MODEL_BAKEOFF.md)

A future release must record the base revision, data manifest, code commit,
environment, seed, hyperparameters, hardware, cost, safety results, licenses,
and the exact released artifact digest.
