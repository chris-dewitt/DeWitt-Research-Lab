---
document_id: DRL-HO-BENCH-20260919-VERDICT-SPLIT
title: "Handoff: DRL-040 scorer verdict split, and DIR-013 raised"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-19
---


# Handoff: DRL-040 scorer verdict split, and DIR-013 raised

## 1. Branch and last commit

Branch `claude/research-runs-data-ssm3ca`, restarted from `origin/main` after
PR #73 merged (`cce66d1`). See the pull request for the head commit.

## 2. Objective completed

DRL-040 — the work item that makes an AtticusBench failure legible as either
dangerous or merely off-route.

`success` was one conjunction over two different kinds of requirement:

- **safety** — nothing the case forbids was executed;
- **sufficiency** — `must_call` completed, terminal state in the expected set,
  step budget respected, abstention matched.

Pooling them means `12/33` cannot be read. It could be a system that took 21
dangerous actions or one that took 21 safe routes the oracle does not name. With
a real model about to be measured for the first time, that ambiguity would land
on the model.

Scorer `1.1.0` reports the two apart. It does **not** change what counts as
success, and no published number moved.

## 3. Files and interfaces changed

- `datasets/atticusbench/src/atticusbench/scoring.py` — `FAILURE_CODES` and
  `FAILURE_CLASSES` (closed vocabularies); `CaseScore.safety_ok`,
  `.failure_class`, `.failure_codes`; `SystemReport.unsafe_cases`,
  `.unmet_objective_cases`, `.failure_code_counts`; the same two counts per
  family.
- `datasets/atticusbench/src/atticusbench/__init__.py` — exports the vocabularies.
- `scripts/run_atticusbench.py` — `SCORER_VERSION` 1.0.0 → 1.1.0; two new CSV
  columns.
- `scripts/run_atticusbench_models.py` — `unsafe`/`unmet` columns in the
  comparison table; `_revived_safety_ok` / `_revived_failure_class` so a
  baseline file predating the split still revives inside the closed vocabulary.
- Regenerated: `runs/atticusbench/results.json`, `results.csv`, `latency.json`,
  all 132 records, and the 0.1.1 release manifest.
- Docs: `TR-2026-003` §5.5 (v1.2.0), dataset card, local model runbook (v1.1.0),
  `runs/atticusbench/README.md`, `DIRECTORS_MEMO.md`, `ADR_APPROVAL_QUEUE.md`,
  `CHANGELOG.md` (v4.26.0), `WORKLOG.md`.

## 4. ADRs created or needed

None created. **No ADR was judged necessary** and that judgement is worth
checking: the case schema is unchanged, no metric definition changed, no case
changed, and no existing value moved — the change is additive reporting behind a
version bump. The part that *would* be an ADR trigger, widening the oracle, was
deliberately not built.

**DIR-013 raised** (memo row and approval queue): may a case declare several
sufficient routes instead of one exact tool list? Recommend A (an optional
`sufficient_call_sets`, adopted per case as reviewed changes), because adopting
it silently would raise published scores.

## 5. Tests and results

```text
uv run pytest                                    → 776 passed in 27.95s
uv run ruff check   scripts tests packages services apps/atticus-local-runner \
                    datasets/atticusbench/src research/cfi/src   → All checks passed
uv run ruff format --check                        → formatted
uv run mypy scripts packages services apps/atticus-local-runner \
            datasets/atticusbench/src             → no issues, 91 source files
uv run bandit -q -r ...                           → no findings
scripts/validate_foundation.py                    → VALIDATION PASSED
scripts/validate_program.py                       → PROGRAM VALIDATION PASSED
scripts/validate_open_identity.py                 → OPEN IDENTITY VALIDATION PASSED
scripts/validate_domain_wix.py                    → DOMAIN/WIX VALIDATION PASSED
scripts/validate_public_repository.py             → PUBLIC REPOSITORY AUDIT PASSED
scripts/validate_atticusbench.py                  → valid (33 cases, 13 critical)
scripts/run_atticusbench.py --check               → Committed outputs match this run
scripts/run_recovery_sweep.py --check             → Committed sweep results match this run
make atticusbench-models-stub                     → model path runs, no daemon
```

New tests: five in `tests/atticusbench/test_scoring.py` (partition, over-refusal
is never unsafe, severity ordering, closed vocabulary, per-family split) and
five in `test_committed_results.py` that assert the same properties **on the
real committed runs** rather than on constructed fixtures.

## 6. Deployment or migration notes

None. No stored state, no wire format, no service. A consumer reading an old
results file sees `scorer_version: 1.0.0` and the absence of the new keys; the
model runner derives them rather than failing.

## 7. Known failures and risks

- **The oracle is still narrow.** This change measures the narrowness; it does
  not fix it. `must-call-coverage` is the most common miss code on the
  baselines. Until DIR-013 is decided, a model's success rate understates any
  system that plans differently, and the runbook now says so at the point of
  reading the table.
- `unsafe` counts *executed* forbidden actions only. A system that plans
  something forbidden and is stopped by policy is correctly not unsafe — the
  control worked — but a reader wanting "tried to do something bad" needs the
  trace, not this column.
- `atb-ground-000002` remains a critical-suite failure for both eager baselines
  and is a grounding failure, unchanged by this work.

## 8. Uncommitted or generated artifacts

None outstanding. All regenerated artifacts are committed, and both drift checks
pass against them.

## 9. Next dependency-unblocking task

**Measure a real model.** It cannot be done in a cloud container — no daemon, no
weights. The runner, the runbook and the stub proof are all in place, and the
table now reports safety and sufficiency apart, which is what makes a first
model number publishable without misattributing the oracle's narrowness.

After that: DIR-013, then re-measure.

## 10. Reading order for the next agent

1. `TR-2026-003` §5.5 — the measurement that motivates the split, with the
   miss-code table.
2. `datasets/atticusbench/src/atticusbench/scoring.py` — `score_case`, from
   `success = all(applicable)` down.
3. `tests/atticusbench/test_committed_results.py`, the last five tests — the
   properties asserted against real runs.
4. `DIRECTORS_MEMO.md` DIR-013 — what is being asked and why it was not built.
5. `docs/11-operations/ATTICUSBENCH_LOCAL_MODEL_RUNBOOK.md` — "Reading the
   output", before running anything.

Verify rather than trust: regenerate with `make atticusbench-check` and confirm
it reports no drift.
