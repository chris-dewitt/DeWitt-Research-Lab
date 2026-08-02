---
document_id: DRL-EVA-007
title: "Statistical Comparison and Uncertainty"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Statistical Comparison and Uncertainty

## Paired design

Run baseline and candidate on the same cases/seeds where feasible. Use paired bootstrap confidence intervals and paired significance tests appropriate to metric type.

## Multiple comparisons

When comparing many candidates/categories, control or clearly disclose multiplicity. Predeclare primary metrics for release decisions; exploratory metrics remain exploratory.

## Practical significance

A statistically significant 0.2-point gain may not justify increased cost or risk. Release report defines minimum meaningful differences for primary metrics and shows Pareto tradeoffs.

## Variance

For stochastic models, use repeated runs on a stratified subset and report variance. Critical safety cases should be tested across multiple seeds/temperatures or deterministic constrained settings.

## Missingness

Timeouts, crashes, malformed outputs, and policy blocks are outcomes. Do not discard them from denominator.
