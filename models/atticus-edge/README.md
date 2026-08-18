---
document_id: DRL-MODE-100
title: "Atticus Edge Project README"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-17
---

# Atticus Edge

**Maturity:** `specified`

Atticus Edge is a proposed small-model research track for local routing,
bounded tool proposals, offline guidance, and escalation. No upstream model has
been selected, no DRL weights have been trained, and no quantized release
artifact exists.

## Intended contents

- Edge-specific distillation, training, and quantization recipes.
- Device-level latency, memory, energy, and quality measurements.
- Evaluation of the exact shipped quantized artifact.
- Model cards, license evidence, and signed release metadata.

## Required reading

- [`docs/SPEC.md`](docs/SPEC.md)
- [`docs/DISTILLATION_AND_TRAINING.md`](docs/DISTILLATION_AND_TRAINING.md)
- [`docs/EVALUATION.md`](docs/EVALUATION.md)
- [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)
- [`BASE_MODEL_BAKEOFF.md`](../../docs/03-model/BASE_MODEL_BAKEOFF.md)

Future local-performance and escalation claims must be earned with reproducible
device measurements and an independently evaluated release artifact.
