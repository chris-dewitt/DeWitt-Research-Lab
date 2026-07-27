---
document_id: DRL-PRD-005
title: "Integrated Reference Demonstration Specification"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Integrated Reference Demonstration Specification

## Objective

Demonstrate that DRL is one platform and that Atticus can coordinate specialist systems safely and transparently.

## Canonical prompt

> Using the latest available public inflation evidence and Federal Reserve communication, construct a plausible synthetic bear-steepener scenario and analyze its impact on the sample regional bank. Show sources, assumptions, calculations, limitations, and an evaluation of the workflow.

The production demo pins an `as_of_date`; “latest” is resolved and displayed to prevent nondeterministic historical replays.

## Workflow contract

1. **Normalize request.** Extract as-of date, region, requested scenario concept, synthetic institution, horizon, output depth.
2. **Policy check.** Confirm public-data and synthetic-finance scope.
3. **Atlas research.** Retrieve inflation, rates, and macro evidence with point-in-time timestamps.
4. **FedLens research.** Compare recent official communication, quote supporting passages, and distinguish decision from interpretation.
5. **Scenario proposal.** Atticus proposes curve shocks and assumptions with source links; policy validates parameter bounds.
6. **BalanceLab execution.** Deterministic engine validates institution/scenario and calculates results.
7. **Consistency check.** Narrative values must reconcile to calculation artifact IDs.
8. **EvalForge evaluation.** Score trajectory, citations, tools, policy, calculation consistency, latency, and cost.
9. **Report.** Present executive summary, evidence, assumptions, scenario, results, risks, contradictions, limitations, trace, and evaluation.

## Required artifacts

- `TaskRequest`;
- Atlas and FedLens `EvidenceBundle`s;
- proposed `ScenarioDefinition`;
- BalanceLab `CalculationArtifact` with version/hash;
- full `ExecutionTrace`;
- `EvaluationReport`;
- human-readable report;
- signed replay bundle.

## Failure behavior

- Atlas unavailable: replay or report incomplete macro evidence; do not fabricate.
- FedLens unavailable: proceed only if user accepts reduced scope, clearly labeled.
- BalanceLab validation failure: show invalid assumption and request correction.
- citation entailment failure: remove or qualify claim before final report.
- evaluation safety failure: do not present run as successful; show failure museum-compatible record.
- cost budget reached: offer replay.

## Demo acceptance

- Executes live in staging and production with open-weight Atticus.
- No manual database editing or hidden operator intervention.
- All values trace to evidence or calculation artifacts.
- Evaluation report is generated from the same trace shown to user.
- Replay can be independently verified from manifest and hashes.
- Mobile user can follow summary and expand details.
- Screen-reader user receives equivalent status and evidence.
