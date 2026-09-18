---
document_id: DRL-TR-2026-003
title: "Technical Report TR-2026-003: An Executable AtticusBench Seed and What Four Deterministic Baselines Reveal About the Policy Model"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-18
citation_key: dewitt2026tr003
maturity: prototype
---


# TR-2026-003: An Executable AtticusBench Seed and What Four Deterministic Baselines Reveal About the Policy Model

## Citation

DeWitt, Christopher Noxon. 2026. *Technical Report TR-2026-003: An Executable
AtticusBench Seed and What Four Deterministic Baselines Reveal About the Policy
Model*. Working paper. Document ID `DRL-TR-2026-003`. Repository path:
`docs/10-research/reports/TR-2026-003-atticusbench-public-seed-baselines.md`.

## Abstract

AtticusBench had a specification and no cases. A specification that nothing
executes cannot be shown to be wrong, so the scoring vector it prescribes was
untested as a measuring instrument. This report describes the first executable
seed — 32 public cases across all ten V1 families, nine declarative environment
fixtures, and a harness that runs each case through the shipped orchestrator,
policy engine, and approval service rather than a reimplementation — and reports
what four deterministic baseline policies do on it. The baselines are not models;
they are fixed strategies whose behavior is fully predictable, which is what a
benchmark needs before it can claim anything about a model.

Three results follow. First, the metric vector separates the baselines as
intended: a planner replaying each case's recorded safe plan passes 32 of 32,
two eager planners pass 12 of 32 with seven cases carrying an unauthorized
action, and a planner that refuses everything passes 5 of 32 — the five cases
where abstention is the correct answer — with a 0.84 excessive-refusal rate. An
aggregate score alone would have ranked the refusing planner second on safety and
said nothing useful. Second, and not by design: across 96 unsafe-baseline runs,
**no forbidden external write or send ever executed.** The deterministic tier
policy held every one of them at an approval pause or a denial without the
planner's cooperation. Third, the single forbidden effect that did execute came
through a **read-tier** tool that performs a cross-session data egress, because
approval gating attaches to risk tier and this effect sits below the gate. That
is a finding about the policy model, not about any model, and it is recorded as an
open Director decision rather than silently patched.

## 1. Question and scope

**Question.** Does the AtticusBench scoring vector, as specified, distinguish
systems that differ in exactly the way the benchmark claims to care about —
usefulness without exceeding authority — and does it avoid rewarding the two
degenerate strategies of acting on everything and refusing everything?

**Scope.** This report covers the seed corpus, the harness, the four baselines,
and the measured results committed in `runs/atticusbench/`. It makes **no claim
about any model.** No model was run. Family slices are three to five cases, so
nothing here is a capability measurement of anything, and the corpus is two
orders of magnitude short of the V1 exit gate of 1,000 held-out tasks.

**Motivating failure mode.** The risk is not a wrong number but an untested
instrument: a metric that cannot separate a safe planner from an eager one, or
that quietly scores refusal as safety, will read as reassuring on a real system
for reasons that have nothing to do with that system.

## 2. The corpus

Thirty-two cases, nine fixtures, `public-test` split only, corpus digest
`sha256:9701eedcd48717c7aee79343c9623c6aeadcd3c16246ee23e35e10e26ce10853`.
Twelve cases are critical-suite members covering the hazards the specification
names: changed-argument approval replay, approval expiry, indirect prompt
injection, path and symlink escape, a secret-bearing repository, cross-session
data access, public-to-private boundary attempts, stale and as-of evidence, and
duplicate delivery.

A case is data. It declares its environment fixture, request, session mode, tool
catalog, policy version, a reference plan, any approval grants, acceptable
terminal states, hard invariants, the scorers that apply, provenance, and a
content digest over its own content. A fixture is also data: a frozen clock plus
a tool catalog, where each tool declares its risk tier, whether a public session
may reach it, its deterministic response, an argument contract, any side effect,
and any failure it raises. The harness builds handlers from those declarations,
so adding a case or an environment adds no code.

Two design choices carry most of the measurement weight.

**Effects are recorded, not inferred.** Every invocation and every executed side
effect lands in an effect ledger. A scorer can therefore say that an external
write happened, rather than deducing it from a terminal state or from prose.

**Argument contracts are enforced by the tool.** A tool with a declared contract
rejects a missing key, an unexpected key, an over-long value, or a value that
fails its anchored pattern, and it raises before performing any effect. Without
this, a path-escape or argument-construction case would have no observable
failure to score.

Five cases expect abstention. Everywhere else an empty plan is scored as
excessive refusal, which the specification treats as a capability failure.

## 3. The systems under test

| System | Strategy | Approvals presented |
|---|---|---|
| `reference-plan-v1` | Replays the case's recorded safe plan | Those the case declares |
| `eager-effect-v1` | Calls every offered tool that declares a side effect; falls back to the read path when none does | None |
| `catalog-sweep-v1` | Calls every offered tool in catalog order | None |
| `abstain-v1` | Plans nothing, in every case | None |

`reference-plan-v1` is an upper bound and a corpus self-check: if the recorded
safe plan cannot satisfy a case, the case is wrong, and a test enforces that on
every case. The two eager policies model what a capability-only evaluation
rewards — reach for the action that completes the request, never ask. Where a
baseline needs argument values the reference plan never supplied, it uses the
fixture's declared example arguments, so a baseline fails for acting without
authority rather than for forgetting a required key.

## 4. Method

Each case runs through `AtticusOrchestrator` with the real `PolicyEngine`,
`ApprovalService`, and `EvalForge` evaluator. The harness supplies only the
environment and the planner. Grants bind to an exact call digest, so a case can
approve one set of arguments and execute another, or issue a grant in the past,
and get the real verification path rather than a mock of it.

Scoring is a vector per case: terminal-state correctness, required-tool coverage,
unauthorized actions with reasons, forbidden effects executed, required-approval
recall, required-denial recall, citation grounding, calculation delegation, step
count against budget, abstention correctness, and critical-suite failure.
Aggregation adds a Wilson 95% interval on task success — Wilson rather than the
normal approximation because these rates sit at the boundaries, where the normal
interval leaves the unit interval — per-family slices, and an exact McNemar test
against the reference baseline. Critical failures are reported as case ids and
are never averaged into anything.

Records carry ids, digests, and scores only: no request text, no tool arguments,
no evidence content, no trace messages, per the `AGENTS.md` prohibition on
logging prompt or tool content by default. Two tests assert this rather than
trusting it. Wall-clock latency is written to a separate file and excluded from
every digest, so a rerun reproduces the results file byte for byte; a third test
reruns the split and compares.

## 5. Results

### 5.1 The vector separates the baselines

| System | Task success | Wilson 95% | Terminal accuracy | Cases with an unauthorized action | Unauthorized actions | Forbidden effects executed | Critical failures | Abstention rate | Excessive refusal | Mean steps |
|---|---|---|---|---|---|---|---|---|---|---|
| `reference-plan-v1` | 32/32 | 0.89–1.00 | 1.00 | 0 | 0 | 0 | 0 | 0.16 | 0.00 | 1.38 |
| `eager-effect-v1` | 12/32 | 0.23–0.55 | 0.56 | 7 | 8 | 1 | 2 | 0.00 | 0.00 | 1.53 |
| `catalog-sweep-v1` | 12/32 | 0.23–0.55 | 0.56 | 7 | 8 | 1 | 2 | 0.00 | 0.00 | 1.59 |
| `abstain-v1` | 5/32 | 0.07–0.32 | 0.31 | 0 | 0 | 0 | 0 | 1.00 | 0.84 | 0.00 |

Paired against the reference on the same 32 cases: `eager-effect-v1` and
`catalog-sweep-v1` each lose 20 cases and win none (exact McNemar
p = 1.9 × 10⁻⁶); `abstain-v1` loses 27 and wins none (p = 1.5 × 10⁻⁸). No
unpaired cases.

The intervals are wide, and deliberately reported that way: 32 cases cannot
support a tighter claim. The separation survives anyway because the discordance
is entirely one-directional.

`abstain-v1` is the instructive row. It is perfectly safe — zero unauthorized
actions, zero effects, zero critical failures — and almost useless, passing only
the five cases where abstention is correct and carrying an excessive-refusal rate
of 0.84. A benchmark that reported a safety score alone would rank it first.

### 5.2 Tier-based approval held every write, without the planner's help

Across 96 runs of the three non-reference baselines, terminal states were:

| System | completed | degraded | awaiting_approval | denied |
|---|---|---|---|---|
| `eager-effect-v1` | 16 | 3 | 11 | 2 |
| `catalog-sweep-v1` | 16 | 3 | 11 | 2 |
| `abstain-v1` | 32 | 0 | 0 | 0 |

Every eager attempt at a commit, a push, an outbound send, a file share, a ticket
creation, or a local note append stopped at an approval pause: the orchestrator
evaluates policy for the whole plan before executing any of it, so one
unapproved consequential call halts the run with nothing executed. The two
denials are the public-session cases, where a private tool in the plan is refused
outright.

**No forbidden external write or send executed in any baseline run.** That is a
property of the deterministic policy, not of the planners, and it is the strongest
positive result in this report: an eager planner with no notion of authority could
not produce an unauthorized outward effect against this policy on this corpus.

### 5.3 The effect that did execute sits below the approval gate

One forbidden effect executed, in `atb-perm-000005`, for both eager baselines:

> `private.read_session`, risk tier `read_compute`, declared effect
> `data_egress` on a cross-session read. Executed; no approval was required,
> because approval attaches at tier ≥ 2.

The case asks the system to summarize what a colleague's session concluded. The
correct behavior is to decline: cross-session access is not authorized. Both
eager baselines called the tool, the fixture recorded the egress, and the scorer
reported a critical-suite failure — which is what the case was written to detect.

The finding is architectural. The policy engine gates on **risk tier**, and the
tier taxonomy is about how consequential an action is to the operator's own
state, not about whether data leaves a boundary. A read that crosses a session or
tenant boundary is cheap by tier and severe by consequence, and nothing in the
current model catches it. Tier gating is necessary and not sufficient.

The remedy is not obvious enough to apply here. Making every egress-declaring
tool tier 2 would gate ordinary public reads behind approval; adding an
effect-class dimension to the policy decision changes canonical approval logic,
which `AGENTS.md` §4 makes an ADR and Director decision rather than an
implementation detail. It is recorded in `DIRECTORS_MEMO.md` as an open question
with this report as its evidence.

A second observation from the same run set: all seven unauthorized-action cases
were read-tier tool misuse — a post-as-of observation retrieved in two cases, an
unrequested projection in two, a cross-session read in one, and out-of-scope
retrieval in two more. Every one of them is invisible to a policy that reasons
only about write consequence.

## 6. What these results do not show

- Nothing about model capability. No model was run.
- Nothing about safety. Twelve critical cases in synthetic fixtures do not
  establish that a runtime is safe; they establish that these twelve hazards are
  detected when they occur.
- Nothing about real-world reliability. Fixtures have no network, no filesystem,
  no mailbox, and no adversary who adapts.
- Nothing about the families as capability slices. Three to five cases each.

## 7. Threats to validity

**The oracle encodes one safe outcome.** Expected terminal states are a small
set per case, so a different safe outcome can score as a failure. This is the
most likely source of an unfair reading if a real system is measured here.

**The reference baseline is the author's own plan.** Its 32-of-32 result is a
consistency check on the corpus, not evidence that the corpus is difficult. A
corpus can be internally consistent and still test nothing interesting.

**Baseline argument construction is borrowed.** Eager baselines reuse recorded or
declared example arguments, which isolates authorization behavior but means these
baselines say nothing about argument construction.

**One author, one reviewer, same person.** Twelve cases are marked for dual human
review because the specification requires it for security cases; they have had
one. The dataset card and the release manifest both record this gap explicitly.

## 8. Reproduction

```bash
uv run python scripts/validate_atticusbench.py          # schema, digests, coverage, duplication
uv run python scripts/run_atticusbench.py               # rewrite runs/atticusbench
uv run python scripts/run_atticusbench.py --check       # byte-compare against the committed corpus
uv run pytest tests/atticusbench -q                     # 73 tests, including the drift check
```

Outputs: `runs/atticusbench/records/<system>/<case>.json` (128 records),
`results.json` (digest
`sha256:c4a88e982015c4657c17f5a3765e0f803c1452a10b12878de32cbc7435aa1d50`),
`results.csv`, and `latency.json`. Release manifest and contamination report:
`datasets/atticusbench/release/`.

## 9. Next dependency-unblocking work

1. Resolve the effect-versus-tier question in §5.3 through an ADR. Until it is
   resolved, no release candidate should be measured on the critical suite and
   reported as passing, because the suite's cross-session case is currently a
   finding about the policy, not about the candidate.
2. Grow the corpus toward the V1 gate, prioritizing families where three cases
   cannot distinguish behaviors: recovery, human factors, and multi-system.
3. Obtain independent review of the twelve critical cases. This is a people
   problem, not a code problem, and it cannot be closed from inside the
   repository.
4. Add an expectation form that admits several distinct safe outcomes per case,
   which is the fix for the oracle threat in §7.

## 10. Limitations statement for reuse

Any citation of this report should carry its scope: 32 synthetic public cases,
four deterministic non-model baselines, one machine, one date, no model
selection, no safety claim, and a benchmark two orders of magnitude short of its
own V1 exit gate.
