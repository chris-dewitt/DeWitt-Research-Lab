---
document_id: DRL-PRD-005
title: "Integrated Reference Demonstration Specification"
version: 2.3.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---


# Integrated Reference Demonstration Specification

## Objective

Demonstrate that DRL is one platform and that Atticus can coordinate specialist systems safely and transparently.

## Canonical prompt

> Using the latest available public inflation evidence and Federal Reserve communication, construct a plausible synthetic bear-steepener scenario and analyze its impact on the sample regional bank. Show sources, assumptions, calculations, limitations, and an evaluation of the workflow.

The production demo pins an `as_of_date`; “latest” is resolved and displayed to prevent nondeterministic historical replays.

## Current maturity

| Claim | Maturity | Evidence |
|---|---|---|
| Local fixture orchestration Atlas → FedLens → BalanceLab → EvalForge → report | `prototype` | `atticus-demo --public`, `tests/integration/test_evidence_to_scenario_trace.py` |
| Five-way linked artifact digests on one task | `prototype` | `TaskResult.artifacts["linked_workflow"]` + `workflow_linked` trace event (DRL-018) |
| M3 specialist composition (public Atlas adapter, bounded Fed corpus + citations, scenario catalog) | `prototype` | `build_m3_specialists()` in control-plane runtime |
| Signed replay / independent verification package | `prototype` | `services/evalforge/fixtures/signed_replays/` (fixture HMAC; not production keys) |
| Opt-in official FRED/Treasury/Fed store | `prototype` | `scripts/refresh_public_feeds.py` + `ATTICUS_LIVE_DATA=1`; ADR-0010 in review |
| Live staging/production open-weight demo | `specified` | Blocked on DIR-002/DIR-004 and M4 deploy work |

## Workflow contract

1. **Normalize request.** Extract as-of date, region, requested scenario concept, synthetic institution, horizon, output depth.
2. **Policy check.** Confirm public-data and synthetic-finance scope.
3. **Atlas research.** Retrieve inflation, rates, and macro evidence with point-in-time timestamps.
4. **FedLens research.** Compare recent official communication, quote supporting passages, and distinguish decision from interpretation.
5. **Scenario proposal.** Atticus proposes curve shocks and assumptions with source links; policy validates parameter bounds.
6. **BalanceLab execution.** Deterministic engine validates institution/scenario and calculates results.
7. **Consistency check.** Narrative values must reconcile to calculation artifact IDs.
8. **EvalForge evaluation.** Score trajectory, citations, tools, policy, calculation consistency, latency, and cost.
9. **Link and report.** Emit one `linked_workflow` graph binding Atlas, FedLens, BalanceLab, report, and evaluation digests; present executive summary, evidence, assumptions, scenario, results, risks, contradictions, limitations, trace, and evaluation.

## Required artifacts

- `TaskRequest`;
- Atlas and FedLens evidence (fixture bundles today; formal `EvidenceBundle` schema remains the target);
- proposed `ScenarioDefinition` (catalog name today, e.g. `bear-steepener`);
- BalanceLab `CalculationArtifact` with version/hash;
- full `ExecutionTrace` including `workflow_linked`;
- `EvaluationReport`;
- human-readable report summary;
- signed replay bundle (**DRL-019** prototype fixtures with demo HMAC).

## Failure behavior

- Atlas unavailable: replay or report incomplete macro evidence; do not fabricate.
- FedLens unavailable: proceed only if user accepts reduced scope, clearly labeled.
- BalanceLab validation failure: show invalid assumption and request correction.
- citation entailment failure: remove or qualify claim before final report.
- evaluation safety failure: do not present run as successful; show failure museum-compatible record.
- cost budget reached: offer replay.

## Demo acceptance

- Local prototype executes without network via `make demo` / `atticus-demo --public`.
- All values in the fixture path trace to evidence or calculation artifacts.
- Evaluation report is generated from the same trace shown to the operator.
- Linked workflow digests are present for Atlas, FedLens, BalanceLab, report, and evaluation.
- Replay can be independently verified from manifest and fixture HMAC hashes (production keys later).
- Staging/production open-weight live demo remains a later gate (M4 / DIR-002 / DIR-004).
- Mobile user can follow summary and expand details (console/Wix — later).
- Screen-reader user receives equivalent status and evidence (later).
