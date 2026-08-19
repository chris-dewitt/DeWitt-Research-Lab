---
document_id: DRL-TR-2026-002
title: "Technical Report TR-2026-002: Evidence-Gated Model Selection"
version: 1.2.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-19
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
an **evidence gate** that can refuse to name a winner. The gate encodes nine
blocking conditions — measurement provenance, revision pinning, license clearance,
suite coverage, execution completeness, a quality floor, zero safety-critical
failures, a minimum field of candidates, and a minimum margin over the runner-up —
and a failure on any one returns "no selection" together with the reasons. No
score, however favourable, overrides a blocked gate. Running the harness on the
current candidate register returns no winner for either role, blocked by six
concrete reasons for each. The two roles fail differently, and the more
instructive of them clears the quality floor before being blocked on five
conditions a ranking would never have shown. That null result is the report's
only empirical claim.

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
| Candidates for the role | ≥ 2 | A field of one is a measurement, not a comparison |
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
- `tests/test_bakeoff_harness.py` — 55 tests, the majority asserting the gate refuses

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

For the `edge` role, two candidates tied at weighted quality 0.810 — above the
0.80 floor — and were blocked anyway by:

1. suite coverage of 7 tasks against the 8-task minimum;
2. a safety-critical failure on credential refusal;
3. revision not pinned (`scaffold-unpinned`);
4. license not cleared (`provisional_review_required`);
5. metrics are fixture, not measured on hardware;
6. margin over the runner-up of 0.000 — too close to call.

The asymmetry between the roles is the more useful of the two results. The `core`
role fails the quality floor and is blocked in the way a leaderboard would also
have caught. The `edge` role passes the quality floor and is blocked on five
further conditions that no ranking would have surfaced at all. A scoreboard would
have shown 0.810 at the top and called it a winner.

**Interpretation.** These numbers describe scripted providers, not models. The
only claim supported is that the harness runs end to end and that the gate
refuses under exactly the conditions it is specified to refuse under. The
ties within each role are an artifact of every scripted provider sharing one
script; the two roles differ (0.455 and 0.810) only because they draw different
task subsets. Both are reported because suppressing them would misrepresent what
was run.

## 6. Limitations

- Fixture providers are scripted and perform no inference. They exercise the
  harness, not any model.
- The suite is 12 tasks. That is a starting instrument, not a decisive one, and
  `min_tasks: 8` is a floor rather than a target. For the `edge` role that floor
  is currently unreachable; see §8 v1.2.0.
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
`candidates.yaml`, a `serving` block on each candidate that has been stood up,
and `--live --measurement-mode hardware`. At least two candidates for a role must
be served before either can be selected.

If the gate still refuses after a hardware run, that is the instrument reporting
that the evidence is insufficient. The correct response is to extend the suite or
correct the setup, not to lower the thresholds.

## 8. Corrections and supersession

**v1.1.0.** Two defects in the gate were found while wiring the first live
endpoint, and both are recorded here rather than quietly repaired.

1. *A field of one could win.* The margin condition was the only comparative
   gate, and `select_winner` skips it when there is no runner-up. Every other
   condition is satisfiable by a single candidate, so serving one endpoint and
   running the suite in hardware mode would have named it the winner on no
   comparison at all. A `min_candidates` condition (default 2) now blocks this.
   The defect was unreachable while every run was fixture-mode, because the
   measurement-provenance condition blocked those runs first; adding a live path
   is what exposed it.
2. *A hedged license read as cleared.* License clearance tested exact membership
   in a set of known-uncleared states. A register row reading
   `reported_apache_2_0_pending_confirmation` says plainly that nobody has
   confirmed the license, matched no entry, and passed. Clearance now fails on
   any hedging marker in the status string.

Neither defect changes §5: that run was fixture-mode and blocked on measurement
provenance regardless. The eight-condition count in v1.0.0 is superseded by nine.

**v1.2.0.** A third defect, found while re-verifying §5 against a live run of the
harness. It is in the suite rather than the gate, and it is the reason the `edge`
coverage blocker in §5 is not a transient state.

3. *The `edge` role cannot satisfy its own coverage condition.* Coverage counts
   the tasks eligible for a role, which is the union of that role's tasks and
   those marked `both`. The suite carries 5 `both` tasks and 2 `edge` tasks, so 7
   tasks are eligible for `edge` against a `min_tasks` floor of 8. No `edge`
   candidate can clear coverage on this suite under any measurement mode,
   including a correctly configured hardware run. The `core` role is unaffected:
   5 `both` plus 5 `core` gives 10 eligible tasks. The gate is behaving exactly as
   specified — it is the suite that is short — but a condition that is
   unsatisfiable by construction reports "insufficient evidence" indefinitely
   rather than reporting a fixable setup problem, which is the failure mode this
   report exists to argue against. The fix is to extend the `edge` task set, not
   to lower `min_tasks`; §7's closing instruction applies to the author as much as
   to a reader.

This defect does change how §5's `edge` result should be read: the coverage
blocker there is structural, not an artifact of the fixture path. The other five
`edge` blockers and all six `core` blockers are unaffected.

Two corrections in v1.1.0 and one in v1.2.0 have all been defects in the
instrument rather than in a result. That is expected while the instrument has
never been run against a model, and it is the argument for not publishing a
selection from it yet.

This report will be superseded when a hardware run produces measured evidence.

## 9. Related requirements

- `DIR-004` — Atticus Core and Edge model selection; open by construction
- `DRL-012` — bake-off scaffold and candidate register
- `docs/01-product/PRODUCT_MATURITY_AND_SCOPE.md` — maturity vocabulary
- `models/bakeoff/README.md` — operating instructions
