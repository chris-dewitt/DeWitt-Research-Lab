---
document_id: DRL-OPS-007
title: "Local Model Runbook"
version: 1.1.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-13
---


# Local Model Runbook

How to put an open-weight model behind the Atticus planner on a workstation, and how to tell what is wrong when it does not answer.

The deterministic fixture planner is the default everywhere, including CI. Nothing here changes that. A model is opt-in, and a model failure degrades to fixtures rather than failing the run.

## Start it

Serve the model on an OpenAI-compatible endpoint. Ollama, vLLM, LM Studio, and `llama-server` all expose the same `/v1/chat/completions` shape, so the runtime is configuration rather than code.

```
ollama serve
ollama pull gemma4:26b
```

Then point Atticus at it and run the demo:

```
export ATTICUS_MODEL=gemma4:26b            # PowerShell: $env:ATTICUS_MODEL="gemma4:26b"
uv run python -m atticus_control_plane.cli
```

The first output line reports which planner actually produced the plan, not which one was configured. `model planner via ...` means the model planned. Anything else names the reason it fell back.

## Diagnose it

`scripts/probe_model.py` walks the same path the planner takes, one stage at a time, and stops at the first stage that fails:

```
uv run python scripts/probe_model.py --model gemma4:26b
```

| Stage fails | What it means | What to do |
| --- | --- | --- |
| reachability | The runtime is not listening, or the tag is not pulled | `ollama ps`, `ollama list`; pass `--base-url` if served elsewhere |
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

**A live run will not name a winner, and that is correct.** The evidence gate requires at least two candidates for a role before either can win: a field of one is a measurement, not a bake-off. Standing up a second endpoint is what makes a selection possible, and DIR-004 still requires Director review of the evidence either way.

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

`ATTICUS_MODEL_NO_THINKING` sends both `think: false` (Ollama) and `chat_template_kwargs.enable_thinking: false` (vLLM and other template-driven servers). There is no standard for this. A server that does not recognise a key ignores it; a server that rejects unknown fields will fail the call, which is why it is opt-in rather than the default.

`ATTICUS_MODEL_LICENSE` is recorded, never probed. An endpoint cannot attest to the license of the weights it loaded, so a mislabelled register produces a wrong disclosure rather than a silent one.

## What the model is not allowed to do

The planner is contained by construction, and none of it depends on the model behaving:

- output is validated against `TOOL_CALL_PLAN_SCHEMA`; malformed structure is rejected, not coerced;
- a step naming a tool absent from the live registry is dropped — a model cannot invent a capability by naming one;
- the declared `risk_tier` is replaced with the tier the registry records, so a model cannot lower its own risk classification to slip past policy;
- an empty or wholly invalid plan falls back to the fixture planner.

Reasoning content is discarded on arrival and never enters the trace, in either the fenced `<think>` form or a `reasoning` side channel. What the model concluded is observable; how it got there is not treated as evidence.
