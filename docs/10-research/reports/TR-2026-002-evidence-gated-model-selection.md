---
document_id: DRL-TR-2026-002
title: "Technical Report TR-2026-002: Evidence-Gated Model Selection"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-08
citation_key: dewitt2026tr002
maturity: prototype
---


# TR-2026-002: Evidence-Gated Model Selection

## Citation

DeWitt, Christopher Noxon. 2026. *Technical Report TR-2026-002: Evidence-Gated
Model Selection*. Working paper. Document ID `DRL-TR-2026-002`. Repository path:
`docs/10-research/reports/TR-2026-002-evidence-gated-model-selection.md`.

## Abstract

Selecting a base model for an agentic system is usually reported as a ranking:
candidates are scored on a benchmark and the highest score wins. That framing
hides the decision that actually matters, which is whether the measurement was
good enough to support a selection at all. This report describes a harness that
separates those two questions. Candidates are run against a fixed task suite and
graded deterministically, producing a ranking; the ranking is then passed through
an **evidence gate** that can refuse to name a winner. The gate encodes eight
blocking conditions — measurement provenance, revision pinning, license clearance,
suite coverage, execution completeness, a quality floor, zero safety-critical
failures, and a minimum margin over the runner-up — and a failure on any one
returns "no selection" together with the reasons. No score, however favourable,
overrides a blocked gate. Running the harness on the current candidate register
returns no winner for either role, blocked by six concrete reasons. That null
result is the report's only empirical claim.

## 1. Question and scope

**Question.** Can the conditions under which a model-selection result is
trustworthy be expressed as executable preconditions rather than as reviewer
judgment applied after the fact?

**Scope.** This report describes the harness design, the grading scheme, the gate
conditions, and the result of a fixture-mode run. It does **not** select a model,
report measured hardware performance, or make any claim about the relative
capability of the registered candidates. `DIR-004` remains open by construction:
the harness produces evidence for a human decision and cannot close the gate on
its own.

**Motivating failure mode.** The risk being addressed is not a *wrong* winner but
a *premature* one — a selection that looks decisive because the suite was thin,
the hardware was simulated, the revision was unpinned, or the runner-up was inside
noise. Each of those is invisible in a leaderboard and obvious in a gate.

## 2. Methods

### 2.1 Task suite

The suite (`models/bakeoff/task_suite.yaml`, 12 tasks, content-addressed by
digest) is drawn from the behaviours the orchestration layer actually depends on:
routing to the correct specialist, invoking a tool rather than answering from
memory, emitting parseable structured output, attaching citations to claims,
declining to state an unsupported position, refusing credential disclosure,
ignoring instructions embedded in retrieved text, and edge-class latency.

Tasks carry a role (`core`, `edge`, or `both`), a weight, and a
`safety_critical` flag.

### 2.2 Grading

Every grader is a string, structural, or latency check: substring presence and
absence, tool-call assertion, JSON validity with required keys, refusal
detection, and a latency budget.

**No model grades another model.** An LLM judge would make the bake-off's own
result unfalsifiable — the artifact under evaluation would also be the instrument
of evaluation — which defeats the purpose of running a comparison at all.

Scoring is proportional across criteria, so a partially-correct response is
distinguishable from a wholly incorrect one. Safety-critical tasks are the
exception and score pass/fail only: partial credit on a boundary check would let
a candidate average its way past a boundary it actually crossed.

A provider error is recorded as a zero-scoring result rather than raised. A
candidate that crashes on a task has failed that task, and aborting the run would
bias the comparison toward fragile candidates by leaving their failures
unrecorded.

### 2.3 The evidence gate

`EvidenceGate` blocks a selection unless all of the following hold:

| Condition | Default | Rationale |
|---|---|---|
| Measurement on hardware | required | Fixture numbers are reproducible, not real |
| Revision pinned | required | "latest" is not a reproducible artifact |
| License cleared | required | An unreviewed license is not a usable model |
| Suite coverage | ≥ 8 tasks | A thin suite makes any winner a sampling artifact |
| Errored tasks | 0 | A crash is missing evidence, not a low score |
| Weighted quality | ≥ 0.80 | Floor below which ranking is uninformative |
| Safety-critical failures | 0 | Not tradeable against aggregate quality |
| Margin over runner-up | ≥ 0.05 | Two candidates inside noise means no winner |

Thresholds are configurable; the conditions are not optional. When any fails,
`select_winner` returns `selected=None`, a status of `insufficient_evidence`, and
the list of blocking reasons. A fixture-mode run therefore cannot produce a
selection under any scoring outcome.

### 2.4 Reporting

Reports emit as JSON or Markdown and carry the suite digest, the measurement
mode, the gate thresholds in force, per-candidate results, and explicit
non-claims.

## 3. Code and revision anchors

- `packages/drl-ai-core/src/drl_ai_core/bakeoff_harness.py` — tasks, grading, runs, gate, reporting
- `packages/drl-ai-core/src/drl_ai_core/scripted_provider.py` — scripted provider for fixture runs
- `models/bakeoff/task_suite.yaml` — the task suite
- `models/bakeoff/candidates.yaml` — candidate register
- `scripts/run_bakeoff.py` — CLI (`make bakeoff`)
- `tests/test_bakeoff_harness.py` — 37 tests, the majority asserting the gate refuses

## 4. Data rights and provenance

No model weights were downloaded, no inference was performed, and no network call
was made. Fixture runs use scripted providers. Closed-weight providers are
rejected before any task executes. One suite task asserts that a candidate
declines to print an API key; the task contains no real secret.

## 5. Results (fixture path)

Running `make bakeoff` against the current register in fixture mode returns
**no winner for either role**.

For the `core` role, three candidates tied at weighted quality 0.455, blocked by:

1. quality below the required 0.80;
2. safety-critical failures on citation refusal and credential refusal;
3. revision not pinned (`scaffold-unpinned`);
4. license not cleared (`provisional_review_required`);
5. metrics are fixture, not measured on hardware;
6. margin over the runner-up of 0.000 — too close to call.

For the `edge` role, coverage was below the eight-task minimum and a
safety-critical failure was recorded.

**Interpretation.** These numbers describe scripted providers, not models. The
only claim supported is that the harness runs end to end and that the gate
refuses under exactly the conditions it is specified to refuse under. The
tied 0.455 is an artifact of every scripted provider sharing one script; it is
reported because suppressing it would misrepresent what was run.

## 6. Limitations

- Fixture providers are scripted and perform no inference. They exercise the
  harness, not any model.
- The suite is 12 tasks. That is a starting instrument, not a decisive one, and
  `min_tasks: 8` is a floor rather than a target.
- Refusal detection is marker-based and will need widening against the phrasing
  real models actually produce.
- Thresholds are asserted from judgment, not derived from a power analysis. They
  should be revisited once a hardware run establishes the variance of the
  measurement.
- Deterministic grading cannot assess answer quality beyond the properties
  encoded as checks. It is a floor on correctness, not a measure of capability.
- No claim is made that the gate conditions are complete.

## 7. Reproduction

```bash
uv sync --all-packages --locked
make bakeoff          # markdown report
make bakeoff-json     # machine-readable
uv run pytest -q tests/test_bakeoff_harness.py
```

A hardware run additionally requires pinned revisions and cleared licenses in
`candidates.yaml`, live open-weight endpoints returned from `build_providers` in
`scripts/run_bakeoff.py`, and `--measurement-mode hardware`.

If the gate still refuses after a hardware run, that is the instrument reporting
that the evidence is insufficient. The correct response is to extend the suite or
correct the setup, not to lower the thresholds.

## 8. Corrections and supersession

No corrections. This report will be superseded when a hardware run produces
measured evidence.

## 9. Related requirements

- `DIR-004` — Atticus Core and Edge model selection; open by construction
- `DRL-012` — bake-off scaffold and candidate register
- `docs/01-product/PRODUCT_MATURITY_AND_SCOPE.md` — maturity vocabulary
- `models/bakeoff/README.md` — operating instructions
