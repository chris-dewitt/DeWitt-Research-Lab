---
document_id: DRL-HO-SEC-20260918-EFFECT-GATE
title: "Handoff: DRL-038 effect-class approval gate and DRL-039 local model runs"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-18
---

# Handoff: DRL-038 effect-class approval gate and DRL-039 local model runs

## 1. Branch and last implementation commit

- Issues: DRL-038 (the work item that closes the effect-gate gap DIR-011) and
  DRL-039 (the work item that adds the local model measurement path). Neither is
  filed on the remote; the Mission 00 issue register is still unfiled, which the
  Director's memo lists as a blocker, and its IDs must stay contiguous.
- Branch: `claude/research-runs-data-ssm3ca`, restarted from `main` after PR #72
  merged. Predecessor work: DRL-036 and DRL-037.
- Commits: the effect gate, then the model path and CI wiring, then this handoff.

## 2. Objective completed

**DRL-038.** The predecessor benchmark produced one finding about this
repository's own policy model: approval gated on risk tier alone, so a read-tier
tool declaring a cross-session data egress executed with no approval. The
Director approved option B as **RES-026**; **ADR-0011** implements it. The same
benchmark now shows the gap closed, and a new case shows the gate does not block
the approved path.

**DRL-039.** The benchmark could measure only fixed policies. It can now measure
a model, and the workflow for doing that is one command on a workstation,
because the measurement has to happen where the model is and this container has
no model daemon, no weights, and no API key.

## 3. Files and interfaces changed

Protocol and policy:

- `packages/drl-protocol/src/drl_protocol/models.py`: `EffectType` (the canonical
  `tool-definition` schema's vocabulary), `BOUNDARY_CROSSING_EFFECTS`,
  `ToolDefinition.effect_type` (defaults to `read`),
  `PolicyDecision.gating_effect`. Package to `0.2.0`.
- `services/atticus-control-plane/src/atticus_control_plane/policy.py`: the
  second approval condition and the prohibited-effect denial.
- `.../orchestrator.py`: `gating_effect` on the `policy_decision` trace event.

Benchmark:

- `datasets/atticusbench/src/atticusbench/environment.py`: `tool_definition`
  and `offered_catalog` — one function builds the catalog, so a model can never
  be shown a tool or a tier the registry will not enforce. `EFFECT_TYPE_BY_KIND`
  maps the fixture's finer effect kinds onto the canonical vocabulary in one
  place.
- `.../systems.py`: `BenchPlanner` protocol with `last_plan`, `StaticPlanner`,
  `static_system`, and `System.build_planner`. The harness used to call a
  planner factory twice, which for a model would have been two inferences per
  case with the recorded plan potentially from a different run than the executed
  one.
- `.../model_system.py`: `BenchModelPlanner`, `model_system`, `provenance`,
  `plan_digest`, `build_bench_plan_validator`.
- `.../stub_provider.py`: a provider that is not a model, for exercising the path
  with no daemon.
- `datasets/atticusbench/cases/public/permission-approval/atb-perm-000006.yaml`:
  the approved companion to the cross-session read. Corpus to 33 cases,
  dataset release 0.1.1.
- `scripts/run_atticusbench_models.py`, `scripts/windows/run-atticusbench-models.ps1`.
- `docs/11-operations/ATTICUSBENCH_LOCAL_MODEL_RUNBOOK.md`,
  `runs/atticusbench/models/README.md`.

Decisions and records: `docs/adr/ADR-0011-effect-class-approval-gate.md`,
`DIRECTORS_MEMO.md` (RES-026, DIR-012, blockers, implementation truth),
`docs/00-program/ADR_APPROVAL_QUEUE.md`, `docs/00-program/DECISION_REGISTER.md`
(D-035), `docs/06-security/PERMISSION_AND_APPROVAL_MODEL.md`,
`docs/02-architecture/POLICY_AND_TOOL_EXECUTION.md`, `TR-2026-003` v1.1.0,
dataset card, `runs/atticusbench/README.md`, `CHANGELOG.md`, `WORKLOG.md`.

Infrastructure: `.github/workflows/ci.yml`, `Makefile`.

## 4. ADRs created or needed

**Created: ADR-0011**, approved by the Director as RES-026 in the session that
produced this branch. Option A (retiering every egress-declaring tool) was
rejected explicitly: it conflates the two axes and puts the control in per-tool
registration data that the next tool can silently omit.

**Needed, both recorded in the approval queue rather than decided here:**

- **DIR-012.** `TOOL_CALL_PLAN_SCHEMA` sets `minItems: 1` on `steps`, so a model
  that correctly decides to call nothing produces an invalid plan and is
  indistinguishable from one emitting prose. Atticus therefore cannot abstain
  through the model path; it falls back to the rule table. The benchmark relaxes
  that one keyword in its own copy so abstention is measurable. Production needs
  an explicit abstention path with its own tests for the case where abstaining
  is wrong, which is why it is not in this change.
- **`approval_policy`.** The canonical schema allows `never` / `policy` /
  `always` / `prohibited` per tool and the engine ignores the field. `never`
  would be a way to weaken a gate, so it needs its own decision.

## 5. Tests and results

```
uv run pytest                                              → 754 passed
uv run pytest tests/test_policy_effect_gate.py             → 18 passed
uv run pytest tests/atticusbench/test_model_system.py      → 17 passed
uv run ruff check scripts tests packages services apps/atticus-local-runner datasets/atticusbench/src research/cfi/src
                                                           → All checks passed
uv run mypy scripts packages services apps/atticus-local-runner datasets/atticusbench/src
                                                           → no issues in 91 source files
uv run bandit -q -r scripts packages services apps/atticus-local-runner datasets/atticusbench/src
                                                           → no findings
uv run python scripts/validate_foundation.py               → VALIDATION PASSED
uv run python scripts/validate_program.py                  → PROGRAM VALIDATION PASSED
uv run python scripts/validate_open_identity.py            → OPEN IDENTITY VALIDATION PASSED
uv run python scripts/validate_domain_wix.py               → DOMAIN/WIX VALIDATION PASSED
uv run python scripts/validate_public_repository.py        → PUBLIC REPOSITORY AUDIT PASSED
uv run python scripts/validate_atticusbench.py             → RESULT: valid
uv run python scripts/run_atticusbench.py --check          → Committed outputs match this run
uv run python scripts/run_recovery_sweep.py --check         → Committed sweep results match this run
make atticusbench-models-stub                              → runs the model path with no daemon
```

The security-change gate in `AGENTS.md` §7 asks for deny-path, abuse-case, and
approval-binding tests: `tests/test_policy_effect_gate.py` covers the read-tier
boundary-crossing gate, every tier against every boundary-crossing effect, the
deliberately ungated line (`modify` and `draft`), prohibited denial, tier
spoofing, public-session denial ordering, the unregistered tool, a grant for the
exact call, a grant for different arguments, a grant from another session, and
that a defaulted definition keeps its old behavior.

## 6. Deployment or migration notes

No stored state, wire format, or persisted record changes shape. `ToolDefinition`
and `PolicyDecision` gained defaulted fields, so existing constructions are
unaffected. Rollback is reverting the commit; no data migration either way.

The residual risk is a registration that should declare an effect and does not:
it under-gates exactly as before the ADR. The fixtures declare effects per tool
and the mapping is in one function; the control plane's own foundation tools are
all read-only and declare nothing.

## 7. Known failures and risks

- **`atb-ground-000002` still fails for both eager baselines** and is meant to.
  It is a grounding failure, not an authorization one. Do not read the remaining
  critical-suite count as an open authorization gap.
- **No model has been measured yet.** The path is tested end to end with a stub
  labelled `not-a-model`, which proves the plumbing and nothing else.
- **A model run is not reproducible** and is excluded from `results.json` and
  every drift check. Sampling moves, weights move, an Ollama tag is not a digest
  pin, and the host is part of the result.
- **The oracle still admits one safe outcome per case** (carried over from
  DRL-036). This matters more now: the first real model measured here will be
  scored against a narrow oracle, and a differently-safe plan will read as a
  failure. Worth fixing before any model number is published.
- **The recovery-sweep CI job takes about a minute** and asserts byte equality
  of a float-bearing artifact. It has only ever been generated and verified on
  x86-64 Linux. If it ever fails on a different runner, suspect the platform
  before the code.

## 8. Uncommitted or generated artifacts

None uncommitted. Generated-and-committed, with the command that regenerates
each, in this order — the manifest digests the results file and the dataset
card, so it goes last:

| Artifact | Command |
|---|---|
| `content_digest` in every case and fixture | `scripts/validate_atticusbench.py --write-digests` |
| `runs/atticusbench/**` (excluding `models/`) | `make atticusbench` |
| `research/cfi/results/**` | `make recovery-sweep` |
| `datasets/atticusbench/release/**` | `make atticusbench-manifest` |

The superseded 0.1.0 release manifest was deleted rather than kept: a manifest
whose digests match nothing in the tree is worse than none, and a test now
asserts that exactly one manifest describes the tree. It remains in git history
at `eaf89db`.

`runs/atticusbench/models/` holds only its README until someone runs a model.

## 9. Next dependency-unblocking task

**Measure a model.** Everything else is now downstream of one number nobody has.
On a workstation: `make atticusbench-models-stub` to confirm the setup, then
`.\scripts\windows\run-atticusbench-models.ps1 -Model <tag> -Pull -Repeats 3`.
Commit the run directory and push it; the manifest carries the provenance that
makes it readable by someone else.

Before publishing any model number, fix the multi-outcome oracle (§7). A model
scored against a one-outcome oracle will be marked down for being
differently-safe, and that would be the benchmark's error reported as the
model's.

Then, in order: DIR-012's production abstention path; the `approval_policy`
decision; growing the corpus where three cases cannot distinguish behaviors
(recovery, human factors, multi-system).

## 10. Exact reading order for the next agent

1. `DIRECTORS_MEMO.md` — RES-026, then the open DIR-012 and `approval_policy`
   rows, then the blockers.
2. `docs/adr/ADR-0011-effect-class-approval-gate.md` — the decision, the
   rejected options, and the before/after table.
3. `services/atticus-control-plane/src/atticus_control_plane/policy.py` — 40
   lines, and the whole gate is in them.
4. `tests/test_policy_effect_gate.py` — what the gate is asserted to do,
   including where it deliberately does not fire.
5. `docs/10-research/reports/TR-2026-003-atticusbench-public-seed-baselines.md`
   §5.3 then §5.4 — the finding, then the re-measurement.
6. `datasets/atticusbench/src/atticusbench/model_system.py` — read the module
   docstring first; the no-fallback decision is the important part.
7. `docs/11-operations/ATTICUSBENCH_LOCAL_MODEL_RUNBOOK.md` — before touching a
   model daemon.

Verify rather than trust: `make atticusbench-check`, `make recovery-sweep-check`,
and `make atticusbench-models-stub` re-derive every claim above from this commit.
