---
document_id: DRL-HO-BENCH-20260920-TIMEOUT
title: "Handoff: The first local model run measured the client timeout, not the model"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Handoff: AtticusBench model runs were bounded by a 30-second ceiling

## 1. Branch and last commit

- Branch: `fix/atticusbench-model-run-timeout`
- Base: `main` at `7aa78ae`
- PR: not yet opened
- Environment: Windows 11, `uv` 0.12.3, project `.venv`, Python 3.13.15

## 2. Objective completed

The Director ran AtticusBench against a real local model for the first time —
Qwen3-1.7B Q8_0 on Ollama — and it reported 6/33 with a 0.97 abstention rate.
This change establishes that the number measures the harness completion budget
rather than the model, and removes the three defects that made it look like a
model result.

**Status: COMPLETE** for the harness defects. The run itself is **not** a
measurement of Qwen3-1.7B and must not be cited as one.

## 3. What the run actually showed

| Plan outcome | Cases | Latency |
|---|---|---|
| `model` / `model-empty-plan` / `no-plan-schema-failure` | 5 | 11.8, 14.4, 17.1, 22.5, 26.0 s |
| `no-plan-provider-error`, detail `unclassified` | 28 | recorded 0 ms |

Every case that finished under 30 s produced a plan. Every case that needed more
was cut off. `CompletionConstraints.timeout_seconds` defaults to **30.0**, and
`scripts/run_atticusbench_models.py` neither set it nor exposed a flag for it.
Wall clock corroborates: 28 x 30 s plus ~92 s of real generation is 932 s
against the 936 s reported.

The harness has no fixture fallback by design, so a cut-off call produced an
empty plan, and an empty plan scores as an abstention. That is why the run landed
beside `abstain-v1` (5/33) rather than anywhere near a model behavior profile.

## 4. Root causes, each fixed rather than worked around

1. **The timeout did not classify.** `ModelGateway.complete` catches
   `ProviderTimeoutError` / `ProviderUnavailableError` and appends `str(exc)` to
   a list, so the exception class is gone by the time the bench module sees it;
   `classify_provider_failure` therefore matches substrings against a message
   this repository writes. That message was
   `no response from {url} within {n}s` — containing none of `timed out`,
   `timeout` or `stalled` — so every exhausted budget recorded `unclassified`.
   Both total-timeout raise sites in `http_provider.py` now read
   `{url} timed out: no response within {n}s`. The stall site already matched.
2. **The error path recorded no latency.** `latency_ms` was read off the
   response; a failed call has no response, so the field kept its 0.0 default.
   `BenchModelPlanner.plan` now times the call with `time.monotonic()` and
   records the elapsed time on the failure path.
3. **The manifest did not record the ceiling.** `sampling` carried
   `temperature`, `max_output_tokens` and `stop_after_json` but not the budget
   that decided 28 of 33 cases, so the manifest could not explain its own
   numbers. It now carries `timeout_seconds` and `stall_timeout_seconds`.

## 5. Files and interfaces changed

| File | Change |
|---|---|
| `packages/drl-ai-core/src/drl_ai_core/http_provider.py` | Two total-timeout messages reworded so they classify |
| `datasets/atticusbench/src/atticusbench/model_system.py` | Time the completion; record `latency_ms` on the provider-error path |
| `scripts/run_atticusbench_models.py` | New `--timeout`; `DEFAULT_BENCH_TIMEOUT_SECONDS = 600.0`; both budgets recorded in the manifest |
| `tests/atticusbench/test_model_system.py` | Two regression tests |
| `docs/11-operations/ATTICUSBENCH_LOCAL_MODEL_RUNBOOK.md` | 1.1.0 to 1.2.0: document `--timeout`; correct the `timeout` troubleshooting row, which previously blamed model size and pointed at the wrong flag |
| `WORKLOG.md` | 4.36.0 to 4.37.0 |

## 6. Public contracts changed

- **CLI:** `run_atticusbench_models.py` gains `--timeout` (default 600.0).
  Additive; existing invocations change behavior only in that they are no longer
  silently capped at 30 s.
- **Run manifest:** `sampling` gains `timeout_seconds` and
  `stall_timeout_seconds`. Additive; older manifests simply lack the fields, and
  a reader should treat their absence as bounded at the 30 s default.
- **`CompletionConstraints.timeout_seconds` default is unchanged at 30.0.** It is
  a production control-plane budget and a benchmark is not a production request.
- No schema, policy, approval, or scoring change. No published number moves.

## 7. ADRs

None created or needed. The control-plane budget is untouched; this adds a
benchmark-side flag and fixes two recording defects.

## 8. Verification

```text
uv run pytest
uv run ruff check scripts tests packages services apps/atticus-local-runner datasets/atticusbench/src
uv run mypy scripts packages services apps/atticus-local-runner datasets/atticusbench/src
uv run bandit -q -r scripts packages services apps/atticus-local-runner datasets/atticusbench/src
uv run python scripts/validate_foundation.py
uv run python scripts/validate_program.py
uv run python scripts/validate_open_identity.py
uv run python scripts/validate_domain_wix.py
uv run python scripts/validate_public_repository.py
uv run python scripts/validate_atticusbench.py
uv run python scripts/run_atticusbench.py --check
uv run python scripts/run_atticusbench_models.py --stub --timeout 450
```

| Check | Result |
|---|---|
| pytest | 781 passed, 1 skipped, 0 failed |
| ruff | All checks passed |
| mypy (strict) | no issues in 91 source files |
| bandit | clean |
| six validators | all pass |
| `run_atticusbench.py --check` | Committed outputs match this run |
| stub model path | runs end to end; manifest carries `timeout_seconds: 450.0` |

## 9. Known failures and risks

**None outstanding on this branch.** Full suite on Windows after rebasing onto
`main`: 781 passed, 1 skipped, 0 failed.

The two `tests/atticusbench/test_release_manifest.py` digest failures recorded
in earlier revisions of this handoff were a separate, pre-existing CRLF problem.
They were fixed by PR #79 (`fix/manifest-digest-newline-normalization`), which
merged to `main` as `6de4bdb` before this branch was rebased. That matters here
for one reason worth keeping: while those tests failed they **rewrote the
tracked manifest on disk**, so any model run started afterwards recorded
`working_tree_dirty: true` and was correctly rejected as evidence. That is how
the 2026-09-20 Qwen3-1.7B run came to be uncitable — the run was fine, the tree
was not. With #79 in, a run started from a clean tree stays clean.

Remaining, and not introduced here: DIR-012 (the production plan contract
forbids an empty plan, so the model path cannot abstain) and DIR-013 (the
benchmark oracle names one route per case). Neither blocks this branch.

## 10. Dirty state and temporary resources

- Uncommitted files: `docs/08-web-brand/assets/` (five untracked homepage hero
  PNGs, ~11 MB, from 2026-08-24; pre-existing and unrelated).
- The Qwen3-1.7B run was moved out of the repository to the session scratchpad,
  because it sat untracked under `runs/atticusbench/models/` and the provenance
  guard fails on any run directory in the tree that records a dirty tree. It is
  preserved, not deleted. It should not be committed: it measures the 30 s
  ceiling.
- No secrets, credentials, or cloud resources created.

## 11. Next-agent start instructions

1. `git checkout fix/atticusbench-model-run-timeout && uv sync --all-packages --locked`
2. Verify inherited state with the command block in section 8. Expect a fully
   green suite on every platform now that PR #79 is on `main`.
3. First task: re-run Qwen3-1.7B **from a clean working tree**, so the manifest
   records `working_tree_dirty: false`:
   `uv run python scripts/run_atticusbench_models.py --model hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0 --timeout 600`
   Expect it to be slow — 33 cases at up to several minutes each.
4. Do not change `CompletionConstraints.timeout_seconds`, the scorer, the case
   corpus, or `runs/atticusbench/results.json` casually. The first three move
   published numbers; the fourth is drift-checked.
5. Outstanding: the CRLF digest decision (section 9), plus the pre-existing
   DIR-012 and DIR-013, neither touched here.

## 12. Attestation

No work is marked complete without the evidence in section 8. No secrets,
private, or employer material was committed. The one result that might be
mistaken for a finding — 6/33 for Qwen3-1.7B — is recorded here and in
`WORKLOG.md` as a measurement of the harness rather than of the model, and the
run that produced it has been kept out of the repository.
