# AtticusBench model runs

Measurements of real models on the public split, produced on a workstation with
a local model daemon. Empty until someone runs one — this container has no
model, and a run cannot be faked.

```
<system>/<run-id>/manifest.json   provenance, sampling, per-attempt scores, limitations
<system>/<run-id>/records/        one record per case per attempt
```

How to produce one: [`ATTICUSBENCH_LOCAL_MODEL_RUNBOOK.md`](../../../docs/11-operations/ATTICUSBENCH_LOCAL_MODEL_RUNBOOK.md).

```bash
make atticusbench-models-stub    # exercise the path with no daemon and no model
make atticusbench-models         # measure whatever the bake-off register serves
```

## Why these live beside the baselines rather than in them

`runs/atticusbench/results.json` is the deterministic baseline corpus. A rerun
reproduces it byte for byte and `make atticusbench-check` enforces that.

A model run cannot make that promise. Sampling moves, served weights move, an
Ollama tag is not a digest pin, and the host is part of the result. Mixing the
two would either break the drift check or force it to be weakened until it
stopped catching anything. So model runs sit here, carry their own provenance,
and are excluded from `results.json` and from every digest.

## Reading one

`manifest.json` holds what `AGENTS.md` §6 asks of a model experiment: code
commit, working-tree cleanliness, corpus digest, model identity as the register
declares it, sampling parameters, host platform, wall clock, and plan-source
counts. `register_backed: false` means the model was named ad hoc with
`--model`, so it has no license clearance and no revision provenance and should
not be cited as evidence.

Records carry ids, digests, and scores only. No request text, no tool arguments,
no evidence content, no trace messages, under the same rule and the same tests
as the deterministic runs.

Look at `forbidden_effects_total` and `critical_failures` before any success
rate, and at the `no-plan` count before reading a low score as a capability
result: an unreachable endpoint and a model that plans badly produce the same
success rate and need opposite responses.
