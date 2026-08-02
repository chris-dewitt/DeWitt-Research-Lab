---
document_id: DRL-TR-2026-001
title: "Technical Report TR-2026-001: Local Integrated Evidence-to-Scenario Workflow"
version: 1.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-01
citation_key: dewitt2026tr001
maturity: prototype
---


# TR-2026-001: Local Integrated Evidence-to-Scenario Workflow

## Citation

DeWitt, Christopher Noxon. 2026. *Technical Report TR-2026-001: Local Integrated Evidence-to-Scenario Workflow*. DeWitt Research Laboratory working paper. Document ID `DRL-TR-2026-001`. Repository path: `docs/10-research/reports/TR-2026-001-integrated-workflow.md`.

## Abstract

This report documents the first reproducible Atticus-integrated research vertical slice in the DeWitt Research Laboratory (DRL) monorepo. A deterministic local runtime gathers synthetic Atlas macro evidence, compares synthetic FedLens communications with passage citations, projects a BalanceLab bear-steepener on an educational bank, evaluates the trajectory with EvalForge, and links the five artifacts under one task digest. The work is **prototype** maturity: fixture data only, no trained Atticus Core/Edge weights, no production signing identity, and no live public deployment.

## 1. Question and scope

**Question.** Can DRL assemble one inspectable workflow in which Atticus coordinates Atlas, FedLens, BalanceLab, and EvalForge such that every public claim is attributable to evidence or a calculation artifact?

**In scope.** Local/CI fixture path; typed protocol envelopes; policy decisions; linked digests; signed fixture replays; teaching lab.

**Out of scope.** Live FRED/Treasury/Fed APIs; production bank data; open-weight model selection (DIR-004); GCP/Wix publication; production cryptographic signing keys.

## 2. Methods

### 2.1 Runtime composition

`atticus_control_plane.runtime.build_local_runtime()` composes:

1. Atlas via `AtlasService.from_public_adapter(PublicFixtureAdapter(...))`
2. FedLens via `FedLensService.from_bounded_corpus()`
3. BalanceLab via `ScenarioEngine` + catalog scenario `bear-steepener`
4. EvalForge trajectory checks
5. Deterministic `FixturePlanner` (stand-in for Atticus Core)

### 2.2 Linked artifact graph

On completion, `AtticusOrchestrator._link_workflow` emits `artifacts["linked_workflow"]` with presence flags and digests for:

- Atlas snapshot evidence
- FedLens cited comparison
- BalanceLab `CalculationArtifact`
- Report summary digest
- Evaluation report digest

A `workflow_linked` trace event records the graph before the terminal state.

### 2.3 Evaluation

EvalForge checks required trace events, citation presence, absence of policy bypass, and legal terminal state. Fixture success runs score `1.0` with `passed=true`.

### 2.4 Replay packaging

DRL-019 packages success and degraded runs under `services/evalforge/fixtures/signed_replays/` using a **demo** HMAC key (`drl-fixture-replay-v1`). `live_at_capture` is always `false`. This is not a production release signature.

## 3. Code and revision anchors

| Surface | Path |
|---|---|
| Orchestrator / linkage | `services/atticus-control-plane/src/atticus_control_plane/orchestrator.py` |
| Specialist tools | `services/atticus-control-plane/src/atticus_control_plane/tools.py` |
| Runtime composition | `services/atticus-control-plane/src/atticus_control_plane/runtime.py` |
| Atlas adapter | `services/atlas/src/atlas_service/adapter.py` |
| FedLens citations | `services/fedlens/src/fedlens_service/citations.py` |
| BalanceLab scenarios | `services/balancelab-ai/src/balancelab_ai/scenarios.py` |
| Replay packaging | `services/evalforge/src/evalforge_service/replay.py` |
| Integration test | `tests/integration/test_evidence_to_scenario_trace.py` |
| Product contract | `docs/01-product/INTEGRATED_REFERENCE_DEMO.md` |
| Teaching lab | `docs/10-research/teaching/INTEGRATED_WORKFLOW_LAB.md` |

Exact commit SHAs are those of the merging PRs on `main` (DRL-014…020 / PRs #16–#23). Readers should pin the commit they reproduce.

## 4. Data rights and provenance

| Dataset | Tier | Rights posture |
|---|---|---|
| Atlas fixture observations | public synthetic | Demo fixtures; not live FRED/Treasury |
| FedLens bounded corpus | public synthetic | `fixture://` citations; CC0-equivalent fixture label in corpus manifest |
| BalanceLab bank/scenario | synthetic educational | No real institution identifiers |
| Replay bundles | public synthetic | Fixture HMAC only |

No private, personal, or employer-confidential data enters these artifacts.

## 5. Results (fixture path)

Observed local demo characteristics (representative):

- Terminal state: `completed`
- Evidence count: 5 cited items
- BalanceLab bear-steepener annual NII change: `$15.81` million (hand-verifiable in unit tests)
- EvalForge score: `1.0`
- Linked keys present: `atlas`, `fedlens`, `balancelab`, `report`, `evaluation`

Degraded replay capture forces a specialist outage mid-plan, finishes `degraded`, and still verifies digests.

## 6. Limitations

1. Planner is deterministic fixture logic, not an evaluated open-weight Atticus Core/Edge model.
2. Macro and Fed inputs are synthetic; do not cite them as live market or official Fed text.
3. BalanceLab is an educational repricing toy, not a production ALM engine.
4. Replay signatures use a published demo HMAC, not a production key ceremony.
5. No staging/production Cloud Run or Wix publication is claimed.
6. Open Director gates remain: DIR-001 (repo identity), DIR-002 (GCP), DIR-003 (security contact), DIR-004 (model bake-off winner).

## 7. Reproduction

```bash
make doctor
make demo
uv run pytest tests/integration/test_evidence_to_scenario_trace.py \
  tests/evalforge/test_signed_replays.py -q
make verify
```

Expected: demo completes with EvalForge `1.0`; integration and replay tests pass; foundation validators pass.

Teaching companion: `docs/10-research/teaching/INTEGRATED_WORKFLOW_LAB.md`.

## 8. Corrections and supersession

Corrections append to this document with dated notes. A later TR that changes methods or claims must bump the document version and preserve lineage. Negative results and failure museum entries remain first-class (see `docs/10-research/failures/`).

## 9. Related requirements

- `DRL-SYS-008`, `DRL-SYS-004`, `DRL-SYS-009`
- `DRL-EVL-008`, `DRL-EVL-009`
- Issues DRL-018, DRL-019, DRL-020
