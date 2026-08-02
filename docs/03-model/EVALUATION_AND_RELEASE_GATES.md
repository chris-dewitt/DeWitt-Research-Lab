---
document_id: DRL-MOD-011
title: "Model Evaluation and Release Gates"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Model Evaluation and Release Gates

## Gate sequence

1. license and artifact eligibility;
2. reproducible load and inference;
3. baseline evaluation;
4. pilot fine-tune quality;
5. full candidate evaluation;
6. safety and red team;
7. quantization/runtime qualification;
8. integrated staging workload;
9. model/data card review;
10. director release approval.

## Critical failure conditions

- unauthorized action proposal rate above approved threshold on gold safety suite;
- any unmitigated credential or cross-tenant exfiltration pattern;
- inability to produce valid tool calls reliably;
- merged artifact violates upstream terms;
- gold split contamination;
- integrated workflow narrative contradicts calculation artifact;
- severe quality loss in release quantization;
- lack of reproducible recipe/checkpoint chain.

## Comparative release report

Report base, previous Atticus, candidate, and quantized deployments with category metrics, confidence intervals, resource measurements, failure examples, and decision rationale. Do not publish one composite score without the category table.
