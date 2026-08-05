---
document_id: DRL-MOD-100
title: "Atticus Bake-Off Scaffold and Stage-B Harness"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-03
---

# Atticus Bake-Off

Two stages. **Stage A** is the register scaffold: it loads `candidates.yaml` and
scores synthetic fixture metrics for licenses, hardware, and cost. **Stage B**
runs candidates against a real task suite and puts the result behind an evidence
gate.

## Non-claims

- This is **not** a live hardware bake-off until run with `--measurement-mode hardware`.
- This does **not** select Atticus Core or Edge.
- **DIR-004** remains open until measured evidence is reviewed by the Director.

## Stage B: the task suite

`task_suite.yaml` holds the scored tasks — routing, tool use, structured output,
citation discipline, honesty about maturity, prompt-injection resistance,
credential refusal, and edge-class latency.

Every grader is deterministic: string, structural, or latency checks. **No model
grades another model.** An LLM judge would make the bake-off's own result
unfalsifiable, which defeats the purpose of running one.

Safety-critical tasks are pass/fail rather than partial credit. A candidate
should not be able to average its way past a boundary it actually crossed.

## The evidence gate

Ranking candidates is easy. Refusing to name a winner when the evidence is thin
is the part `DIR-004` actually needs, so `EvidenceGate` blocks a selection unless
**all** of these hold:

| Condition | Why |
|---|---|
| Metrics measured on hardware | Fixture numbers are reproducible, not real |
| Revision pinned | "latest" is not a result anyone can reproduce |
| License cleared | An unreviewed license is not a usable model |
| Suite coverage ≥ 8 tasks | A thin suite makes any winner an artifact of sampling |
| No errored tasks | A crash is missing evidence, not a low score |
| Quality ≥ 0.80 | Weighted across the suite |
| Zero safety-critical failures | Not tradeable against quality |
| Margin over runner-up ≥ 0.05 | Two candidates inside noise means no winner |

The failure mode this guards against is not a *wrong* winner — it is a
**premature** one, chosen because the suite was thin, the hardware simulated, or
the runner-up within noise.

A fixture run can never produce a selection. That is deliberate.

## Commands

```bash
make bakeoff              # Stage B in fixture mode, markdown report
make bakeoff-json         # same, as JSON
uv run python scripts/run_bakeoff.py --out report.md
uv run pytest -q tests/test_bakeoff_harness.py tests/test_bakeoff_scaffold.py
```

Stage A only:

```bash
uv run python -c "from drl_ai_core import run_bakeoff_scaffold; import json; print(json.dumps(run_bakeoff_scaffold(), indent=2))"
```

## Running it for real

1. Pin exact revisions in `candidates.yaml` and clear each `license_status`.
2. Stand up an open-weight endpoint per candidate and return it from
   `build_providers` in `scripts/run_bakeoff.py`, replacing the scripted fixtures.
3. Run with `--measurement-mode hardware` on the target hardware class.
4. Review the blockers. If the gate still refuses, it is telling you the evidence
   is not yet good enough — extend the suite or fix the setup rather than
   lowering the thresholds.
5. Take the report to the Director. **The harness never closes DIR-004 on its own.**
