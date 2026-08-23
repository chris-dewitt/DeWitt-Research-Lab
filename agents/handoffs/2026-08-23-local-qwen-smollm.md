---
document_id: DRL-HO-OPS-20260823
title: "Handoff: Local Atticus with Qwen3 1.7B and SmolLM3-3B"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---


# Handoff: Local Atticus with Qwen3 1.7B and SmolLM3-3B

## 1. Branch and last commit

- Mission / issue: Director request — run Atticus locally with Qwen3 1.7B and SmolLM3-3B
- Branch: `cursor/local-qwen-smollm-atticus-ad29`
- Starting commit: `c43241e` (`main`)
- Ending commit: the commit containing this handoff
- Pull request: filled after open
- Prepared UTC: `2026-08-23`

## 2. Objective completed

Documented and registered workstation serving for two small open-weight models
behind Atticus. Diagnosed why `ollama list` and `GET :11434/v1/models` disagreed
on the Director's Windows machine. **Did not** download weights (this
environment has no access to that Ollama), **did not** select Atticus Core or
Edge, **did not** close DIR-004.

## 3. Files and interfaces changed

- `models/bakeoff/candidates.yaml` — `edge-qwen3-1.7b`, `edge-smollm3-3b` with
  Ollama `serving` blocks; fixture metrics; `selection_status` remains
  `not_selected`
- `scripts/check_local_ollama.py` — reads the HTTP catalogue Atticus uses
- `scripts/windows/setup-local-models.ps1` — pins `OLLAMA_HOST` and pulls both tags
- `scripts/probe_model.py` — prints GET `/v1/models` and names the two-library fault
- `packages/drl-ai-core/src/drl_ai_core/http_provider.py` — `catalog_ids()`
- `docs/11-operations/LOCAL_MODEL_RUNBOOK.md` (DRL-OPS-007 v1.2.0)
- `.env.example`, `Makefile` `local-models-check`, README pointer
- Tests: `tests/test_check_local_ollama.py`, bake-off scaffold/harness

## 4. ADRs created or needed

None. Serving tags for an existing Edge role is operational, not a model-family
or V1-scope decision. DIR-004 remains the selection gate.

## 5. Tests and results

Filled after the verification pass on this branch.

## 6. Deployment or migration notes

No cloud, schema, or production change. Operator-only, on the Windows workstation:

1. `$env:OLLAMA_HOST="http://127.0.0.1:11434"`
2. Confirm `ollama list` matches `curl.exe http://127.0.0.1:11434/api/tags`
3. `ollama pull qwen3:1.7b`
4. `ollama pull hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M`
5. Copy the exact SmolLM3 `name` from `/api/tags` if it differs
6. `$env:ATTICUS_MODEL="qwen3:1.7b"; $env:ATTICUS_MODEL_NO_THINKING="1"`
7. `uv run python scripts/check_local_ollama.py`
8. `uv run python scripts/probe_model.py --model qwen3:1.7b --no-thinking`
9. `uv run --package atticus-control-plane atticus-demo --public`
10. Read `PLANNER:` — must say `model planner via`. Anything else is a fallback.

The daemon on `:11434` already listed `llama3.2:latest` and `gemma4:26b`. Those
can smoke-test Atticus immediately; they are not the Qwen/SmolLM pair.

## 7. Known failures and risks

- Two Ollama libraries on Windows: CLI pulls do not reach Atticus unless
  `OLLAMA_HOST` points at `:11434`.
- SmolLM3 is not in the official Ollama library; the GGUF tag must be confirmed
  after pull.
- Both models think by default; without `ATTICUS_MODEL_NO_THINKING=1` the plan
  budget can be spent inside reasoning and look like an empty completion.
- `--live` bake-off will also call `core-gemma4-26b` (26B). That is slow on CPU.
- License status remains `provisional_review_required`. Qwen3 Apache-2.0 and
  SmolLM3 Apache-2.0 still need Director confirmation before `cleared`.
- These are edge/small models, not Core-class.

## 8. Uncommitted or generated artifacts

None intended. No weights committed.

## 9. Next dependency-unblocking task

Director: pin `OLLAMA_HOST`, pull into the `:11434` daemon, probe, run the demo,
confirm `PLANNER: model planner via`. Then optionally a Path B live bake-off
without treating the result as a DIR-004 winner.

## 10. Exact reading order for the next agent

1. This handoff
2. `docs/11-operations/LOCAL_MODEL_RUNBOOK.md`
3. `models/bakeoff/candidates.yaml` (`edge-qwen3-1.7b`, `edge-smollm3-3b`)
4. `scripts/check_local_ollama.py`
5. `DIRECTORS_MEMO.md` DIR-004 (still open)
6. Do not declare a Core/Edge winner from a local demo
