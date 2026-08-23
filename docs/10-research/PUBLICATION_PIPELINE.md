---
document_id: DRL-RES-003
title: "Publication and Replication Pipeline"
version: 2.2.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-19
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
