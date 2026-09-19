---
document_id: DRL-ADR-0011
title: "ADR-0011: Approval gates on declared effect as well as risk tier"
version: 1.1.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-09-18
---


# ADR-0011: Approval gates on declared effect as well as risk tier

## In plain language

Before this change, Atticus asked for approval based on **how consequential** an
action was — its risk tier. It did not ask based on **where the action reached**.
A tool that only *reads*, but reads across a session boundary and hands the data
out, was tier one and therefore needed no approval. A benchmark run found exactly
that and executed the read.

Now a tool that declares a boundary-crossing effect requires an approval no
matter how cheap its tier is. Nothing else changes: ordinary reads, drafts, and
local edits keep the gates they already had.

## Context

`TR-2026-003` section 5.3 is the evidence. Running the AtticusBench public seed
against four deterministic baselines produced 96 unsafe-baseline runs, and the
tier policy held **every** unauthorized write and send: 13 of them stopped at an
approval pause and 2 at an outright denial, with nothing executed, and without
any cooperation from the planner.

One forbidden effect executed. `private.read_session` is risk tier one
(`read_compute`) and declares a `data_egress` effect: it hands one session's
stored content to another. Approval attached at tier two and above, so the call
ran, the egress happened, and the scorer reported a release-blocking
critical-suite failure.

The tier taxonomy is not wrong; it answers a different question. It ranks how
consequential an action is **to the operator's own state** — can this be undone,
how much does it cost to be wrong. Whether data or authority crosses a trust
boundary is orthogonal to that. A cross-session read is cheap on the first axis
and severe on the second, and nothing in the policy engine looked at the second
axis at all.

Two further facts shaped the decision:

- **The canonical contract already models this.** `schemas/tool-definition.schema.json`
  has carried an `effect_type` enum — `observe`, `read`, `draft`, `modify`,
  `external_effect`, `privileged`, `prohibited` — and an `approval_policy` enum
  since the schema bundle was written. The runtime `ToolDefinition` dataclass
  simply never carried the field. This is an implementation catching up with its
  own contract, not a new axis.
- **Two specifications already required it.** `docs/06-security/PERMISSION_AND_APPROVAL_MODEL.md`
  lists "destination and side effect" among the policy inputs, and
  `docs/02-architecture/POLICY_AND_TOOL_EXECUTION.md` says the policy engine
  evaluates "data movement". Both were written before the engine existed. The
  gap was implementation lag against the repository's own approved documents,
  which is precisely the distinction `AGENTS.md` section 1 asks an agent to keep
  visible: specified behavior is not existing behavior.
- **The planner is not a control.** Both eager baselines reached for the tool.
  Relying on the planner to decline a read that policy permits is relying on the
  component the benchmark exists to distrust.

## Decision

1. `ToolDefinition` carries `effect_type: EffectType`, using the canonical
   schema's vocabulary. It defaults to `read`, so an existing registration keeps
   its behavior.
2. `PolicyEngine.decide` requires an approval when **either** the call's risk
   tier is `REVERSIBLE_CHANGE` or higher, **or** the catalog's declared
   `effect_type` is in `BOUNDARY_CROSSING_EFFECTS` = {`external_effect`,
   `privileged`}.
3. A tool declaring `effect_type: prohibited` is denied outright, regardless of
   tier, alongside the existing tier-four denial.
4. `PolicyDecision` carries `gating_effect`, set only when the effect — rather
   than the tier — is what required the approval. The orchestrator records it on
   the `policy_decision` trace event, so a trace shows **which control fired**
   instead of leaving it to be inferred.
5. Both conditions read the **catalog** definition. A `ToolCall` has no effect
   field, and a caller's declared tier is already rejected on mismatch, so
   neither a planner nor a model can lower its own gate.
6. The declaration is normalized once through `EffectType(...)`, and an
   unrecognized value is **denied**. `ToolDefinition` is an unvalidated
   dataclass, so a future catalog loader could hand the engine a plain string;
   a gate that cannot read a tool's effect must not conclude it has none.

### Where the line sits, and why

`modify` and `draft` are **not** gated by effect. They are already gated by tier
wherever they matter, and gating them by effect as well would put every ordinary
local edit behind an approval. The gate is for effects that leave the operator's
trust boundary, which is the property the measured failure had.

## Options considered

**A. Retier the tools.** Raise every egress-declaring tool to tier two or above.
Smallest diff, no contract change. Rejected: it conflates two axes permanently,
and it would gate ordinary public reads behind approval the moment any of them
declared an egress. It also puts the fix in per-tool registration data, where the
next tool to be added can silently omit it.

**B. Gate on declared effect (chosen).** Adds a field to the runtime definition
and one condition to the policy decision. Costs a canonical-type change and a
migration note. Gains a control that is correct by construction for every tool
that declares its effect honestly, and that says in the trace which control
fired.

**C. Accept the gap and rely on the planner.** Rejected on the measurement: both
eager baselines performed the read. A control the benchmark can defeat with a
fixed policy is not a control.

## Consequences

- One additional approval pause for any read-tier tool that declares a
  boundary-crossing effect. In the current catalogs this is exactly one tool.
- `ToolDefinition` gains a defaulted field; `PolicyDecision` gains a defaulted
  field. Both are additive and backward compatible for existing constructors.
  `drl-protocol` goes to `0.2.0`.
- Measured effect on the AtticusBench public seed, before and after, same
  corpus and scorer otherwise:

  | | Before | After |
  |---|---|---|
  | Forbidden effects executed (all baselines) | 1 | **0** |
  | Critical-suite failures per eager baseline | 2 | **1** |
  | Cases with an unauthorized action per eager baseline | 7 | **6** |
  | `reference-plan-v1` task success | 32/32 | 33/33 |

- The remaining critical-suite failure, `atb-ground-000002`, is a different
  class: a system retrieving an observation dated after the as-of date. No
  authorization control can catch that, because nothing about the action is
  unauthorized — it is a judgment failure about evidence. Worth stating plainly:
  this ADR closes an authorization gap and does not touch grounding.
- `approval_policy` from the canonical schema remains **unimplemented**. A tool
  cannot yet demand `always` or declare `never`. Recorded here as a known gap
  rather than quietly ignored; it needs its own decision because `never` is a
  way to weaken a gate.

## Amendment, v1.1.0

Added after a security review of the implementing branch:

- The effect declaration is normalized and an unrecognized value is denied
  (decision point 6). The review noted that `is`-comparison against the enum
  would have permitted a raw-string declaration; the normalization closes that
  and is covered by two tests.
- The same review found the one real defect, in the sibling change rather than
  here: a model-supplied tool name reached a persisted run record verbatim,
  through a section attached after the content-minimization allowlist. Model
  records now go through one assembler with its own allowlist, provider failures
  are classified into a closed vocabulary instead of quoting an endpoint's text,
  and both are tested. That is recorded here because it is the same principle as
  this ADR's: a guarantee restated in prose is not a guarantee, and the place to
  enforce it is the one function everything passes through.

## Migration and rollback

No stored state, no wire format, and no persisted record changes shape. Existing
`ToolDefinition` constructions are unaffected by the new default. Rollback is
reverting this ADR's code change; no data migration is implied either way.

Registrations that should declare an effect and do not will under-gate, exactly
as before this ADR. The AtticusBench fixtures declare effects per tool, and the
bench maps the fixture's finer kinds onto the canonical vocabulary in one place.

## Verification

- `tests/test_policy_effect_gate.py` — 18 tests: deny paths, abuse cases, the
  approval-binding path, the deliberate ungated line, and that a caller cannot
  declare its own effect.
- `tests/atticusbench/test_harness.py` — the regression pair:
  `atb-perm-000005` (no grant, gate holds, trace names the gating effect) and
  `atb-perm-000006` (grant present, the same read completes).
- `runs/atticusbench/results.json` — the before/after numbers in the table above
  are re-derivable with `make atticusbench-check`.

## Status

Approved by the Director on 2026-09-18 as **RES-026**, resolving **DIR-011**.
The Director selected option B explicitly over option A.
