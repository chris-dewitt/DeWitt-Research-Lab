# AtticusBench run corpus

Committed output of running the AtticusBench public seed against the
deterministic baseline systems. Unlike `runs/atticus/`, which holds gitignored
local demo records, everything here is checked in: the point is that a reader can
compare the numbers in a report against the records that produced them.

```
records/<system_id>/<case_id>.json   one record per case per system (132 files)
results.json                         metric vector per system, per family, paired tests
results.csv                          the same per-case scores as a flat table
latency.json                         wall-clock timings, machine-dependent
```

## Reproducing

```bash
uv run python scripts/run_atticusbench.py          # rewrite every file here
uv run python scripts/run_atticusbench.py --check  # fail if anything drifted
make atticusbench-check
```

`--check` reruns the whole split and compares byte for byte. `tests/atticusbench/test_committed_results.py`
runs the same comparison, so a change to the orchestrator, policy engine,
approval service, corpus, or scorer that moves a number cannot land without the
records moving with it.

Timing is the one thing that does not reproduce, so it lives in `latency.json`
and is excluded from `results.json` and from every digest.

## What a record contains, and what it does not

A record carries ids, digests, and scores: case id and content digest, system id,
family, terminal state, the trace as event types and states with a short list of
retained attributes, tool names started, completed, and failed, evidence ids, the
effect ledger, the EvalForge evaluation, and the case's metric vector.

A record deliberately does **not** carry the request text, tool arguments,
evidence content, or trace messages. `AGENTS.md` forbids logging prompt or tool
content by default, and a benchmark record does not need it. Two tests assert
this rather than trusting it: one checks a fresh run, one checks every committed
file.

## Current results

Corpus digest `sha256:89c0352949b0cef9ab59e00014da98fbad6aaccacf7eb60c56978821381b1fb7`,
33 cases, scorer 1.0.0.

| System | Task success | 95% interval | Cases with an unauthorized action | Forbidden effects executed | Critical-suite failures |
|---|---|---|---|---|---|
| `reference-plan-v1` | 33/33 | 0.90–1.00 | 0 | 0 | 0 |
| `eager-effect-v1` | 12/33 | 0.22–0.53 | 6 | 0 | 1 |
| `catalog-sweep-v1` | 12/33 | 0.22–0.53 | 6 | 0 | 1 |
| `abstain-v1` | 5/33 | 0.07–0.31 | 0 | 0 | 0 |

These are the post-ADR-0011 numbers. The approval gate now fires on a declared
boundary-crossing effect as well as on risk tier, so the cross-session read that
executed in the first run is held at an approval pause: forbidden effects
executed went 1 → 0 and critical-suite failures per eager baseline 2 → 1. The
pre-ADR run is preserved in `TR-2026-003` §5.1–5.3 and in git history at
`eaf89db`.

None of these systems is a model. They are fixed policies, and they are here to
show that the scoring vector separates a safe planner from an eager one and does
not reward a planner that refuses everything. The analysis is in
[`TR-2026-003`](../../docs/10-research/reports/TR-2026-003-atticusbench-public-seed-baselines.md).
