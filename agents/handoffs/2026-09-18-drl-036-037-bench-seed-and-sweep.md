---
document_id: DRL-HO-DATA-20260918-BENCH-SWEEP
title: "Handoff: DRL-036 AtticusBench executable seed and DRL-037 recovery sweep"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-18
---

# Handoff: DRL-036 AtticusBench executable seed and DRL-037 recovery sweep

## 1. Branch and last implementation commit

- Issues: DRL-036 (the work item that builds an executable AtticusBench public
  seed) and DRL-037 (the work item that sweeps the CFI-005 parameter-recovery
  study). Neither is filed on the remote yet; the GitHub issue register from
  Mission 00 is still unfiled, which the Director's memo already lists as a
  blocker.
- Branch: `claude/research-runs-data-ssm3ca`.
- Last implementation commit: recorded in the pull request; this handoff is the
  final commit on the branch.

## 2. Objective completed

Two specifications became data.

**DRL-036.** AtticusBench had `docs/SPEC.md`, `docs/TASK_AUTHORING.md`, and zero
cases, so the scoring vector it prescribes had never been exercised. It now has
32 executable public cases covering all ten V1 families, nine declarative
environment fixtures, a case and fixture JSON Schema, a corpus loader with
digest and duplication audits, four deterministic non-model baselines, and a
committed corpus of 128 run records that a rerun reproduces byte for byte. Cases
run through the shipped `AtticusOrchestrator`, `PolicyEngine`, and
`ApprovalService` rather than through a reimplementation.

**DRL-037.** CFI-005 reported recovery error at one design, which cannot
separate an estimator that converges from one already at an information limit
from noise in the measurement of the bias. The study is now swept on two axes —
grid refinement at fixed calendar time, and replication count at a fixed design
— across 11,850 fitted replications, with results committed and their headline
claims pinned by tests.

Neither work item runs a model, selects a model, or supports a safety claim, and
both label themselves that way in every artifact.

## 3. Files and interfaces changed

New, DRL-036:

- `datasets/atticusbench/schemas/atticusbench-case.schema.json`,
  `atticusbench-fixture.schema.json`: JSON Schema 2020-12, `additionalProperties:
  false`.
- `datasets/atticusbench/fixtures/*.yaml`: nine fixtures. Declarations only, no
  code. Each tool declares tier, public-session eligibility, deterministic
  response, argument contract, declared effect, declared failure, and example
  arguments for baselines.
- `datasets/atticusbench/cases/public/<family>/*.yaml`: 32 cases, 12 in the
  critical suite, 2 public-session, 5 expecting abstention.
- `datasets/atticusbench/src/atticusbench/`: `model.py` (typed projections),
  `corpus.py` (load, consistency, digests, duplication, coverage),
  `environment.py` (registry builder, effect ledger, argument-contract
  enforcement), `systems.py` (four baselines), `harness.py` (execution, grants,
  content-minimized records), `scoring.py` (per-case vector, Wilson interval,
  aggregate, exact McNemar).
- `datasets/atticusbench/docs/DATASET_CARD.md`,
  `datasets/atticusbench/release/{case-index.json,contamination-report.json,atticusbench-public-seed-0.1.0.manifest.json}`.
- `scripts/validate_atticusbench.py`, `scripts/run_atticusbench.py`.
- `runs/atticusbench/{records/,results.json,results.csv,latency.json,README.md}`.
- `tests/atticusbench/` (73 tests).
- `docs/10-research/reports/TR-2026-003-atticusbench-public-seed-baselines.md`.

New, DRL-037:

- `scripts/run_recovery_sweep.py`.
- `research/cfi/results/{recovery-sweep.json,recovery-sweep.csv}`.
- `tests/cfi/test_recovery_sweep.py` (18 tests).
- `docs/10-research/reports/TR-2026-004-belief-parameter-recovery-sweep.md`.

Modified:

- `Makefile`: `atticusbench`, `atticusbench-check`, `atticusbench-validate`,
  `atticusbench-manifest`, `recovery-sweep`, `recovery-sweep-check`; `verify`
  now runs the corpus validator and the run-corpus drift check; format, lint,
  typecheck, and security targets cover `datasets/atticusbench/src`.
- `pyproject.toml`: `mypy_path` for the workspace src roots.
- `tests/conftest.py`: `datasets/atticusbench/src` added to the importable roots.
- `datasets/atticusbench/README.md`: real README with layout, quickstart, and the
  case-authoring loop.
- `DIRECTORS_MEMO.md` (DIR-011, implementation truth, blocker), `CHANGELOG.md`,
  `WORKLOG.md`, root `README.md`.

No existing service, package, schema, fixture, or replay bundle changed
behavior. `services/evalforge`'s hardcoded held-out suite is untouched; the new
harness reuses its `ObservedRun`/`ObservedEvent` types and its evaluator.

## 4. ADRs created or needed

**Needed, and this is the substantive escalation: DIR-011.** The deterministic
policy gates on risk tier. Across 96 unsafe-baseline runs no unauthorized write
or send executed, but a **read-tier** tool that performs a cross-session
`data_egress` executed with no approval, because approval attaches at tier 2 and
above. `TR-2026-003` §5.3 has the measurement. An ADR is required before the
policy decision grows an effect-class dimension; raising every egress-declaring
tool to tier 2 instead would gate ordinary public reads behind approval and is
not recommended. Until this resolves, the AtticusBench critical suite must not be
cited as passed by any release candidate: its cross-session case currently
measures our policy model rather than a candidate.

No ADR was created. No existing ADR changed.

## 5. Tests and results

```
uv run pytest                                              → 717 passed
uv run pytest tests/atticusbench                           → 73 passed
uv run pytest tests/cfi/test_recovery_sweep.py             → 18 passed
uv run ruff check scripts tests packages services apps/atticus-local-runner datasets/atticusbench/src research/cfi/src
                                                           → All checks passed
uv run mypy scripts packages services apps/atticus-local-runner datasets/atticusbench/src
                                                           → Success: no issues found in 88 source files
uv run bandit -q -r scripts packages services apps/atticus-local-runner datasets/atticusbench/src
                                                           → no findings
uv run python scripts/validate_foundation.py               → VALIDATION PASSED
uv run python scripts/validate_program.py                  → PROGRAM VALIDATION PASSED
uv run python scripts/validate_open_identity.py            → OPEN IDENTITY VALIDATION PASSED
uv run python scripts/validate_public_repository.py        → PUBLIC REPOSITORY AUDIT PASSED
uv run python scripts/validate_atticusbench.py             → RESULT: valid
uv run python scripts/run_atticusbench.py --check          → Committed outputs match this run
uv run python scripts/run_recovery_sweep.py --check        → Committed sweep results match this run
```

`mypy` previously reported three `import-not-found` errors on `main`
(`scripts/run_belief_recovery.py`, `scripts/build_belief_site.py`); the
`mypy_path` addition clears them, so this branch improves that check rather than
inheriting its failure.

## 6. Deployment or migration notes

None. Nothing here is served, deployed, or reachable from the public site. The
replay viewer and Pages workflow are untouched.

## 7. Known failures and risks

- **The oracle admits one safe outcome per case.** Expected terminal states are a
  small set, so a differently-safe system can score as failing. This is the most
  likely way the corpus would misjudge a real system, and the fix — an
  expectation form admitting several distinct safe outcomes — is not built.
- **One author, one reviewer, the same person.** Twelve cases are marked
  `dual-human-review` because the specification requires it for security cases.
  They have had one review. The dataset card and the release manifest both state
  this rather than implying two sign-offs.
- **The reference baseline is the author's own plan.** Its 32/32 is a consistency
  check on the corpus, not evidence the corpus is difficult.
- **Sweep runtime.** `run_recovery_sweep.py` takes about 67 seconds at the
  committed settings. It is not wired into `make verify` for that reason; the
  drift check is available as `make recovery-sweep-check` and the committed
  artifact's claims are pinned by fast tests instead.
- The corpus is 32 cases against a V1 exit gate of 1,000. Family slices are three
  to five cases and no slice supports a capability claim.

## 8. Uncommitted or generated artifacts

None uncommitted. Generated-and-committed, by design, with the command that
regenerates each:

| Artifact | Command |
|---|---|
| `runs/atticusbench/**` | `make atticusbench` |
| `research/cfi/results/recovery-sweep.{json,csv}` | `make recovery-sweep` |
| `datasets/atticusbench/release/**` | `make atticusbench-manifest` |
| `content_digest` in every case and fixture | `scripts/validate_atticusbench.py --write-digests` |

All four are idempotent: rerunning on an unchanged input rewrites identical
bytes. `runs/atticus/*.json` remains gitignored and unaffected.

## 9. Next dependency-unblocking task

Draft the DIR-011 ADR. It blocks the meaning of the critical suite, and every
further case added to the permission family inherits the ambiguity until it is
settled.

After that, in order: grow the corpus toward the V1 gate starting with recovery,
human factors, and multi-system, where three cases cannot distinguish behaviors;
add the multi-outcome expectation form from §7; and build the bias-corrected
Ornstein-Uhlenbeck estimator that `TR-2026-004` §4.5 identifies as the only
change a protocol depending on `reversion_rate` would need.

## 10. Exact reading order for the next agent

1. `DIRECTORS_MEMO.md` — DIR-011 and the new blocker entry.
2. `docs/10-research/reports/TR-2026-003-atticusbench-public-seed-baselines.md`
   — §5.2 and §5.3 are the measurement behind DIR-011.
3. `datasets/atticusbench/docs/SPEC.md`, then `docs/TASK_AUTHORING.md` — the
   authority the corpus was written against.
4. `datasets/atticusbench/README.md` — layout and the case-authoring loop.
5. `datasets/atticusbench/schemas/atticusbench-case.schema.json` and one case,
   for example `cases/public/permission-approval/atb-perm-000003.yaml`
   (changed-argument approval replay), read together.
6. `datasets/atticusbench/src/atticusbench/scoring.py` — what "success" means
   before trusting any number in `runs/atticusbench/results.json`.
7. `docs/10-research/reports/TR-2026-004-belief-parameter-recovery-sweep.md`,
   then `docs/10-research/CFI_BELIEF_RECOVERY_2026-08-25.md` for the
   single-design study it extends.

Verify rather than trust: `make atticusbench-check` and
`make recovery-sweep-check` re-derive every number in both reports from this
commit.
