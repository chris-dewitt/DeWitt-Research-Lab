---
document_id: DRL-OPS-012
title: "AtticusBench Local Model Runbook"
version: 1.0.0
status: APPROVED OPERATING PROCEDURE
owner: Christopher Noxon DeWitt
last_updated: 2026-09-18
---


# AtticusBench Local Model Runbook

How to measure a model on the AtticusBench public split on your own machine.
Nothing here needs a cloud account, an API key, or a paid endpoint.

## The short version

```powershell
# Windows, from anywhere in the repository
.\scripts\windows\run-atticusbench-models.ps1 -Stub                      # prove the setup, no model
.\scripts\windows\run-atticusbench-models.ps1                            # every model the register serves
.\scripts\windows\run-atticusbench-models.ps1 -Model qwen3:1.7b -Pull    # one model, pull it first
.\scripts\windows\run-atticusbench-models.ps1 -Model qwen3:1.7b -Repeats 3
```

```bash
# macOS or Linux
make atticusbench-models                                         # register-declared models
make atticusbench-models-stub                                    # no daemon needed
uv run python scripts/run_atticusbench_models.py --model qwen3:1.7b --repeats 3
uv run python scripts/run_atticusbench_models.py --case atb-perm-000002 --model qwen3:1.7b
```

Start with `-Stub` / `make atticusbench-models-stub`. It runs the whole path
with a built-in stub that is **not a model**, so if it works, everything except
the daemon works, and a later failure is about the model rather than the setup.

## What you need

1. **Ollama running**, answering `GET http://localhost:11434/v1/models`. On
   Windows this is the one genuinely confusing part: a tag can appear in
   `ollama list` and still be absent from that endpoint, because the pull landed
   on a different daemon. The scripts check the endpoint rather than the list,
   and say so when they disagree.
2. **The model pulled onto that daemon.** `-Pull` does it for you and then
   re-checks the endpoint rather than assuming.
3. `uv` on PATH. Nothing else: the benchmark has no external Python
   dependencies beyond the workspace.

## Choosing what to measure

**From the register (preferred).** Any candidate in
`models/bakeoff/candidates.yaml` with a `serving:` block is measured by default:

```yaml
  - id: edge-qwen3-1.7b
    # ...
    serving:
      runtime: ollama
      model: hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0
      system_prefix: "/no_think"
      quantization: Q8_0
```

Adding a model to the sweep is adding a block like that. The run then records
the register's `revision_label`, `license_label`, and `license_status`, which is
what makes the result usable as evidence.

**Ad hoc, with `--model <tag>`.** Faster for trying something, and weaker as
evidence: an unregistered tag has no license clearance and no revision
provenance, so the run records `license_label: unknown` and
`register_backed: false`. Fine for exploration; not citable in a report.

## What a run produces

```
runs/atticusbench/models/<system>/<run-id>/
  manifest.json      provenance, sampling, per-attempt scores, limitations
  records/           one JSON record per case per attempt
```

`manifest.json` carries what `AGENTS.md` §6 requires of a model experiment: code
commit, whether the working tree was dirty, corpus digest, model identity,
sampling parameters, host platform, wall clock, and the plan-source counts.

Records carry ids, digests, and scores. No request text, no tool arguments, no
evidence content, no trace messages — the same content-minimization rule that
governs the deterministic runs, enforced by the same tests.

**Model runs are never mixed into `runs/atticusbench/results.json`.** That file
is the deterministic baseline corpus and is checked byte for byte by
`make atticusbench-check`. A model run cannot be reproduced — sampling moves,
weights move, an Ollama tag is not a digest pin — so it lives beside the
baselines and never inside them.

## Reading the output

The console table puts each model next to the committed baselines:

```
system                               success  unauth  effects  critical  abstain  no-plan  seconds
baseline reference-plan-v1             33/33       0        0         0     0.15        -        -
baseline eager-effect-v1               12/33       6        0         1     0.00        -        -
baseline abstain-v1                     5/33       0        0         0     1.00        -        -
register::edge-qwen3-1.7b #1            ...
```

Read it in this order:

1. **`effects` and `critical` first.** A model that executed a forbidden effect
   or failed a critical-suite case has a finding against it, and no success rate
   compensates. These columns are never averaged into the others.
2. **`no-plan`.** How many cases produced nothing usable: unreachable endpoint,
   empty completion after reasoning was stripped, or a completion that failed
   the plan schema. A high count is a serving or prompt problem, not a
   capability result, and the per-case records say which.
3. **`success` with its interval.** 33 cases, so the interval is wide. Treat a
   gap of a few cases as noise.
4. **`abstain`.** Compare against the five cases where abstention is correct. A
   model at 1.00 is the `abstain-v1` baseline with extra steps.

`--repeats N` runs the split N times. Plans carry a digest, so differing
digests across attempts at temperature 0 mean the endpoint is not deterministic,
which is worth knowing before citing any single run.

## Known limits, before you cite anything

- **No approval grants are presented to a model.** Cases that need one are
  measured as approval pauses. This is deliberate: handing a system under test
  the approvals a human would have issued and then reporting how it behaves
  without them measures nothing.
- **A model cannot abstain through the production planner** (`DIR-012`). The
  shared plan contract requires at least one step; the benchmark relaxes that
  one keyword for measurement, and the production path is unchanged.
- **The corpus is public and publishes its expectations.** A model trained on
  this repository would be measured on its own training data.
- **33 cases** against a V1 exit gate of 1,000. Family slices are three to six
  cases. No slice supports a capability claim, and neither does the total.
- **A run is not a selection.** `DIR-004` (which upstream models become Atticus
  Core and Edge) is decided by the bake-off's evidence gate, not here.

## Sharing a run

Commit the run directory on a branch and push it. The manifest carries the
commit, the corpus digest, the model identity, and the host, which is what makes
someone else's reading of it meaningful. Do not edit a manifest by hand: rerun
instead.

## If something goes wrong

A record's `plan_outcome.source` is a code from a closed set, and
`plan_outcome.detail` is a second code classifying the immediate cause. Neither
quotes the endpoint: an endpoint controls its own error text and that text is
never persisted, so the table below maps codes rather than sentences.

| Code | Cause | Fix |
|---|---|---|
| `endpoint did not answer` (preflight) | Daemon down, or a different port | `ollama serve`; check `curl http://localhost:11434/v1/models` |
| `does not serve '<tag>'` (preflight) | Pull landed on another daemon | Pull on the host answering that port; re-check the endpoint, not `ollama list` |
| `no-plan-empty-completion` | A reasoning model spent its budget thinking | Set the register's `system_prefix: "/no_think"`, or raise `--max-output-tokens` |
| `no-plan-schema-failure` | Model is emitting prose or fenced JSON | Lower temperature; confirm the tag is instruction-tuned |
| `no-plan-unavailable-tools` | Model named tools that were not offered | Check `dropped_unknown_tools` on the record; often a prompt-following failure |
| `no-plan-provider-error` + `timeout` | Model too large for the host | Smaller quantization; the stall timeout is `--stall-timeout` |
| `no-plan-provider-error` + `connection-refused` | Daemon died mid-run | Restart it and re-run; check the host's memory |
| `no-plan-provider-error` + `not-found` | Tag is not served on that endpoint | Pull it on the daemon answering the port |
| `no-plan-provider-error` + `unclassified` | A failure this vocabulary does not name | Re-run with the endpoint's own logs open; then add the marker to `PROVIDER_FAILURES` |
| `model-empty-plan` | The model chose to call nothing | Correct on five cases; excessive refusal elsewhere |
| Scores look impossibly good | You are looking at the stub | The stub's license label is `not-a-model`; check `manifest.json` |
