---
document_id: DRL-HO-OPS-20260823-DIAG
title: "Handoff: Qwen plan bind, integrated coverage, and run records"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---


# Handoff: Qwen plan bind, integrated coverage, and run records

## 1. Branch and last commit

- Mission / issue: Director follow-up — failed CI on PR #55, diagnostic logs,
  and local runs that finish the integrated demo
- Branch: `cursor/qwen-plan-arg-bind-ad29`
- Starting commit: `f852be1` (`main` after PR #54)
- Ending commit: the commit containing this handoff
- Pull request: https://github.com/chris-dewitt/DeWitt-Research-Lab/pull/55
- Prepared UTC: `2026-08-23`

## 2. Objective completed

Unblocked foundation-ci (Ruff E501 on Atticus limitation strings). Bound
omitted Qwen plan arguments. Completed omitted Atlas / FedLens / BalanceLab
catalog tools when the objective matches the fixture integrated demo. Added
stderr progress lines and an ids-only run record so a multi-minute local run
is not silent and leaves a file. **Did not** close **DIR-004** (which
upstream models become Atticus Core and Edge). **Did not** merge to `main`.

## 3. Files and interfaces changed

- `services/atticus-control-plane/src/atticus_control_plane/model_planner.py`
  — bind `as_of` / demo scenario; append omitted catalog specialists
- `services/atticus-control-plane/src/atticus_control_plane/planner.py` —
  shared `needs_integrated_coverage` / `INTEGRATED_SPECIALISTS`
- `services/atticus-control-plane/src/atticus_control_plane/orchestrator.py`
  — optional `progress` callback; wrapped limitation strings
- `services/atticus-control-plane/src/atticus_control_plane/run_record.py` —
  new; `atticus-run-record/v1`
- `services/atticus-control-plane/src/atticus_control_plane/cli.py` —
  stderr progress, run-record path, human card
- `runs/atticus/README.md`; `.gitignore` `runs/atticus/*.json`
- `docs/11-operations/LOCAL_MODEL_RUNBOOK.md` (DRL-OPS-007 v1.3.0)
- `services/atticus-control-plane/docs/SPEC.md` (DRL-ATT-107 v3.1.0)
- Tests: `tests/test_model_planner.py`, `tests/test_atticus_foundation.py`

## 4. ADRs created or needed

None. Completing omitted catalog tools is the same reach the fixture planner
already had for the same objective. DIR-004 remains the selection gate.

## 5. Tests and results

```text
uv run ruff check scripts tests packages services apps/atticus-local-runner
# All checks passed

uv run mypy scripts packages services apps/atticus-local-runner
# Success: no issues found in 64 source files

uv run pytest -q
# 445 passed

uv run python scripts/validate_foundation.py
# VALIDATION PASSED (373 controlled documents)

uv run python scripts/validate_program.py
# PROGRAM VALIDATION PASSED

uv run python scripts/validate_open_identity.py
# OPEN IDENTITY VALIDATION PASSED

uv run python scripts/validate_domain_wix.py
# DOMAIN/WIX VALIDATION PASSED

uv run python scripts/validate_public_repository.py
# PUBLIC REPOSITORY AUDIT PASSED

uv run bandit -q -r scripts packages services apps/atticus-local-runner
# exit 0

ATTICUS_RUN_RECORD_DIR=/tmp/atticus-records \
  uv run --package atticus-control-plane atticus-demo --public
# progress lines on stderr; STATE completed; EVIDENCE 5 items;
# record lists atlas/fedlens/balancelab and evalforge_score 1.0
```

## 6. Deployment or migration notes

No cloud or schema migration. Operator-only:

```
$env:ATTICUS_MODEL="hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"
$env:ATTICUS_MODEL_NO_THINKING="1"
uv run --package atticus-control-plane atticus-demo --public
Get-Content runs\atticus\atticus-demo-*.json
```

Expect `tools_completed` to name Atlas, FedLens, and BalanceLab, five
`evidence_ids`, and `evalforge_score: 1.0`. Progress lines stay on stderr so
`--json` stdout remains a single document.

## 7. Known failures and risks

- Agents do not merge. This branch must stay green and the Director merges
  to `main`.
- Coverage fill is objective-term matching, same as `FixturePlanner`. A
  question that does not mention inflation / Federal Reserve / steepener /
  bank is not expanded.
- Run records overwrite nothing unique: each file is `{task_id}-{UTC}.json`.
- `ATTICUS_RUN_RECORD_DIR` is the test isolation hatch.

## 8. Uncommitted or generated artifacts

Run JSON under `runs/atticus/` is gitignored. Do not commit one.

## 9. Next dependency-unblocking task

Director merge of PR #55 onto `main` after green CI. Then re-run the Windows
Qwen demo and confirm the record shows five evidence ids.

## 10. Exact reading order for the next agent

1. This handoff
2. `DIRECTORS_MEMO.md` DIR-004 (still open)
3. `docs/11-operations/LOCAL_MODEL_RUNBOOK.md`
4. `services/atticus-control-plane/src/atticus_control_plane/{model_planner,run_record,cli,orchestrator}.py`
5. PR #55 CI
