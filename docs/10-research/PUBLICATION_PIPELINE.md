---
document_id: DRL-RES-003
title: "Publication and Replication Pipeline"
version: 2.4.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-25
---


# Publication and Replication Pipeline

```text
idea -> research note -> protocol/preregistration -> experiment
 -> internal review -> replication run -> draft -> public review
 -> release with code/data/model/eval -> correction lifecycle
```

A public paper package includes document source/PDF or web version, citation metadata, code commit, environment, dataset/model manifests, outputs/figures, evaluation report, and limitations. If raw data cannot be redistributed, provide legal acquisition and transformation steps where allowed.


## Current working papers

| ID | Title | Status | Maturity | Path |
|---|---|---|---|---|
| TR-2026-001 | Local Integrated Evidence-to-Scenario Workflow | APPROVED FOUNDATION | prototype | `docs/10-research/reports/TR-2026-001-integrated-workflow.md` |
| TR-2026-002 | Evidence-Gated Model Selection | DRAFT | prototype | `docs/10-research/reports/TR-2026-002-evidence-gated-model-selection.md` |

Every report under `docs/10-research/reports/` belongs in this table, whatever
its status. A working paper that is written but unlisted is invisible to the
only index a reader is expected to trust.

## Novelty status

A report is not ready for public release until its contribution has been checked
against primary sources. Current state:

| ID | Novelty record | State |
|---|---|---|
| TR-2026-001 | None | Not required while the report claims only a reproducible workflow |
| TR-2026-002 | `TR-2026-002_NOVELTY_SCAN.md` (DRL-RES-008) | **Preliminary** — 7 records examined, 4 verified; not a G1 review |
| CFI Papers I-III | `CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md` (DRL-RES-006) + `CFI_REVALIDATION_2026-08-23.md` (DRL-RES-009) | Two strata covered; preprint re-opening outstanding. RES-025 replaced the independent-reviewer precondition with stratum coverage |

## Bridge instrumentation

The Belief Diffusion bridge is not a fourth paper (§2.1). Its foundation tasks
produce software and methods evidence, which is indexed here so that a reader
does not have to infer progress from the commit log.

| Task | Artifact | State |
|---|---|---|
| CFI-004 — observable belief-event schema | `research/cfi/src/drl_cfi/beliefs.py` | Proposal in code, with valid/invalid fixtures in `tests/cfi/test_beliefs.py`. Not gate-approved |
| CFI-005 — Bayesian, diffusion, OU, and jump baselines | `research/cfi/src/drl_cfi/baselines.py` + `CFI_BELIEF_RECOVERY_2026-08-25.md` (DRL-RES-011) | Reference package and synthetic recovery study complete; three known estimator limits recorded |
| CFI-006 — estimands and preregistration template | — | Not started |
| CFI-007 — belief-trajectory viewer | `research/cfi/src/drl_cfi/viewer.py` + `scripts/build_belief_site.py` + `CFI_BELIEF_VIEWER_2026-08-25.md` (DRL-RES-012) | Local viewer complete: seven synthetic fixtures across clean, degraded, and error states, with a diagnostic registry that reports identifiability without a verdict |
| CFI-008 — bridge methods report | — | Not started; depends on CFI-005–007 |

None of these touches G2. They use synthetic paths only, and the schema refuses
to record a belief it cannot represent rather than clamping it.
