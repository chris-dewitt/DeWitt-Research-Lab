---
document_id: DRL-OPS-007
title: "Local Model Runbook"
version: 1.3.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---


# Local Model Runbook

How to put an open-weight model behind the Atticus planner on a workstation, and how to tell what is wrong when it does not answer.

The deterministic fixture planner is the default everywhere, including CI. Nothing here changes that. A model is opt-in, and a model failure degrades to fixtures rather than failing the run. Running a small local model does **not** select Atticus Core or Edge. **DIR-004** (the Director decision: which upstream models become Atticus Core and Edge) stays open until a hardware bake-off with pinned revisions and cleared licenses is reviewed.

## Two Ollama libraries on Windows

Atticus talks only to the OpenAI-compatible HTTP daemon:

```
GET http://127.0.0.1:11434/v1/models
```

`ollama list` can show a different library. That is the usual failure on Windows when the Ollama app and a second `ollama` process keep separate model stores. Observed example: `ollama list` showed `hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0` while `curl.exe http://localhost:11434/api/tags` showed `llama3.2:latest` and `gemma4:26b`. Pulls that land in the CLI library never reach Atticus.

Pin the CLI to the daemon Atticus uses **before** listing or pulling:

```
$env:OLLAMA_HOST="http://127.0.0.1:11434"
ollama list
curl.exe http://127.0.0.1:11434/api/tags
```

Those two listings must name the same tags. If they do not, stop and fix the host; do not pull again into the wrong store.

## Start it

Serve an OpenAI-compatible endpoint. Ollama, vLLM, LM Studio, and `llama-server` all expose the same `/v1/chat/completions` shape, so the runtime is configuration rather than code.

Workstation default is the pair the Director asked for: **Qwen3 1.7B** and **SmolLM3-3B**.

| Role in the register | Pull tag | Size (approx.) | Notes |
|---|---|---|---|
| `edge-qwen3-1.7b` | `hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0` | 1.8 GB | The GGUF already on the Windows CLI library. Official `qwen3:1.7b` is the same family. |
| `edge-smollm3-3b` | `hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M` | 1.9 GB | Not in the Ollama library. ggml-org GGUF of HuggingFaceTB/SmolLM3-3B (Apache-2.0). Copy the exact `name` from `/api/tags` after the pull if it differs. |

Both are hybrid thinking models. Set `ATTICUS_MODEL_NO_THINKING=1` for planning so the token budget is not spent inside `<think>` blocks.

PowerShell from the repo root:

```
$env:OLLAMA_HOST="http://127.0.0.1:11434"
ollama pull hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0
ollama pull hf.co/ggml-org/SmolLM3-3B-GGUF:Q4_K_M
curl.exe http://127.0.0.1:11434/api/tags
uv run python scripts/check_local_ollama.py
```

The Qwen pull is only needed if that tag is missing from `/api/tags` on port 11434. `ollama list` showing it is not enough. SmolLM3 was not in either listing yet, so that pull is required.

Or run `scripts/windows/setup-local-models.ps1`, which sets `OLLAMA_HOST` and performs those pulls.

Then point Atticus at Qwen and run the demo:

```
$env:ATTICUS_MODEL="hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"
$env:ATTICUS_MODEL_NO_THINKING="1"
uv run python scripts/probe_model.py --model hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0 --no-thinking
uv run --package atticus-control-plane atticus-demo --public
```

Switch to SmolLM3 by setting `ATTICUS_MODEL` to the exact tag `/api/tags` reported. The first output line of the demo reports which planner actually produced the plan, not which one was configured. `model planner via ...` means the model planned. `plus catalog coverage` means the model planned, and omitted Atlas / FedLens / BalanceLab steps were filled from the live catalog because the objective matched the integrated demo. Anything else names the reason it fell back — including a missing tag on this daemon.

While the run is in progress, stderr prints `progress: <event> <detail>` lines (`planning`, `plan_created`, `tool_started`, `tool_completed`, `evaluating`, `finished`). Those lines name tools and the task id. They never print the objective or tool payloads. When the run ends, a record is written under `runs/atticus/` (override with `ATTICUS_RUN_RECORD_DIR`). The record stores ids and the EvalForge score only. `--json` still prints the full trace on stdout when you ask for it.

```
Get-Content runs\atticus\atticus-demo-*.json
```

A completed integrated demo should list `atlas.research_snapshot`, `fedlens.compare_latest`, and `balancelab.run_scenario` under `tools_completed`, five `evidence_ids`, and `evalforge_score: 1.0`. Two evidence items with only FedLens and BalanceLab means the model skipped Atlas and coverage did not run — that is a bug, not a score.

`mistral:latest`, `llama3.2:latest`, and `gemma4:26b` can also be pointed at the same way. They are not this pair, and none of them selects Atticus Core or Edge (**DIR-004**, the still-open Director decision about which models fill those roles).

Bash equivalent:

```
export OLLAMA_HOST=http://127.0.0.1:11434
export ATTICUS_MODEL=hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0
export ATTICUS_MODEL_NO_THINKING=1
uv run python -m atticus_control_plane.cli
```

## Diagnose it

`scripts/probe_model.py` walks the same path the planner takes, one stage at a time, and stops at the first stage that fails:

```
uv run python scripts/probe_model.py --model hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0 --no-thinking
```

| Stage fails | What it means | What to do |
| --- | --- | --- |
| reachability | The runtime on this base URL is not listening, or the tag is not in **its** catalogue | `curl.exe http://127.0.0.1:11434/v1/models` and `uv run python scripts/check_local_ollama.py`. Do not trust an unpinned `ollama list`. Pass `--base-url` if served elsewhere |
| generation, stalled | Nothing arrived at all for the stall window | Check the server log; the request never reached a loaded model |
| generation, total budget | The model is generating, just slowly | Raise `--timeout`, or use a smaller model |
| generation, empty completion | The whole budget went on reasoning | `--no-thinking`, or raise `--max-tokens` |
| plan schema | It generates, but will not hold the JSON contract | Try a larger model or an instruct variant |

The probe reports time to first token separately from total time. They are different faults: a long wait before the first token is a cold model load; a long steady generation is throughput.

## Measure it

Once the probe passes, the same endpoint can run the Stage-B bake-off suite for real. Declare where the candidate is served in `models/bakeoff/candidates.yaml`:

```yaml
  - id: core-gemma4-26b
    # ...
    serving:
      runtime: ollama
      model: gemma4:26b
      quantization: Q4_K_M
```

Then:

```
uv run python scripts/run_bakeoff.py --live --measurement-mode hardware
```

A candidate with a `serving` block is included; one without is skipped, because nobody having served a model is not the same as that model failing. Identity comes from the register, never from the endpoint — a local server cannot attest to the license or exact revision of the weights it loaded.

`--measurement-mode hardware` without `--live` is refused. Labelling scripted providers as hardware-measured would defeat the one gate condition fixtures can never otherwise clear.

**A live run will not name a winner, and that is correct.** Two workstation edge tags now have `serving` blocks, so a `--live` run can compare them. Licenses remain provisional, the tags are not digest pins, and DIR-004 still requires Director review. Serving is not selection. A `--live` run also includes `core-gemma4-26b` if that block is still in the register.

## Why the timeout is a stall timeout

A single blocking request with a wall-clock deadline cannot distinguish a 26B model generating steadily on CPU from a dead endpoint. Raising the deadline only makes a genuinely dead endpoint take longer to detect, and lowering it kills working runs.

The provider streams, so the two questions are asked separately:

- **stall timeout** (default 120s) — "is anything still arriving?" Fires when no byte has arrived for that long. This is what catches a dead endpoint.
- **total timeout** (default 900s) — a runaway ceiling on the whole call. It is not an estimate of how long the model ought to need.

## What the planner does not wait for

Two costs on the planning path are paid in wall clock the operator sits through, and neither buys anything.

**Tokens after the plan closes.** A plan is a JSON document, so it is finished at its closing brace. `ATTICUS_MODEL_MAX_TOKENS` has to leave headroom for a reasoning model to think before it answers, and a small local model routinely spends the rest of that headroom restating the plan in prose — text the schema validator then discards. The planner closes the stream at the closing brace instead; local runtimes cancel the generation when the client disconnects. A planning run that ended this way reports `finish_reason: client_stop` rather than `stop`, and no token counts, because the usage figures arrive on a terminal chunk that never came. This applies to the planner and to structured-output repairs, not to the probe — `probe_model.py` reads to the end on purpose, since tokens/sec is one of the numbers it exists to measure.

**Loading the model to ask whether it is up.** The health probe asks `GET /models`, which every OpenAI-compatible runtime answers from its registry without touching a weight file. Only if the route is missing, or the runtime names the loaded model differently from the tag requested, does it fall back to a one-token completion — which on a cold 26B means loading the whole model to produce a token that is thrown away. That fallback used to be the only path, and under a five-second connect timeout it reported healthy-but-cold endpoints as dead, which aborts a bake-off candidate before a single task runs.

## Environment

| Variable | Effect |
| --- | --- |
| `ATTICUS_MODEL` | Model tag. Unset means the deterministic fixture planner. |
| `ATTICUS_MODEL_BASE_URL` | Non-default endpoint. Loopback HTTP or HTTPS only. |
| `ATTICUS_MODEL_LICENSE` | License recorded in the run disclosure. |
| `ATTICUS_MODEL_TIMEOUT` | Total ceiling on one planning call, in seconds. |
| `ATTICUS_MODEL_STALL_TIMEOUT` | Silence tolerated before the endpoint is declared dead. |
| `ATTICUS_MODEL_MAX_TOKENS` | Output budget for the plan. |
| `ATTICUS_MODEL_NO_STREAM` | Fall back to one blocking request. |
| `ATTICUS_MODEL_NO_THINKING` | Ask a reasoning-capable model to answer directly. |
| `ATTICUS_RUN_RECORD_DIR` | Directory for ids-and-scores run records. Default `runs/atticus`. |

`ATTICUS_MODEL_NO_THINKING` sends both `think: false` (Ollama) and `chat_template_kwargs.enable_thinking: false` (vLLM and other template-driven servers). There is no standard for this. A server that does not recognise a key ignores it; a server that rejects unknown fields will fail the call, which is why it is opt-in rather than the default.

`ATTICUS_MODEL_LICENSE` is recorded, never probed. An endpoint cannot attest to the license of the weights it loaded, so a mislabelled register produces a wrong disclosure rather than a silent one.

## What the model is not allowed to do

The planner is contained by construction, and none of it depends on the model behaving:

- output is validated against `TOOL_CALL_PLAN_SCHEMA`; malformed structure is rejected, not coerced;
- a step naming a tool absent from the live registry is dropped — a model cannot invent a capability by naming one;
- the declared `risk_tier` is replaced with the tier the registry records, so a model cannot lower its own risk classification to slip past policy;
- an empty or wholly invalid plan falls back to the fixture planner.

Reasoning content is discarded on arrival and never enters the trace, in either the fenced `<think>` form or a `reasoning` side channel. What the model concluded is observable; how it got there is not treated as evidence.
