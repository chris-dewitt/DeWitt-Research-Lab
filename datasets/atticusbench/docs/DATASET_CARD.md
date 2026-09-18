---
document_id: DRL-ATB-091
title: "AtticusBench Public Seed 0.1.0 Dataset Card"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-09-18
---


# AtticusBench Dataset Card

## Summary

AtticusBench Public Seed 0.1.0 is the first executable slice of the AtticusBench
benchmark program described in [`docs/SPEC.md`](SPEC.md). It contains 32
machine-checked cases across the ten V1 families, nine content-addressed
environment fixtures, a declarative case schema, and a harness that runs each
case through the shipped Atticus orchestrator, policy engine, and approval
service rather than through a copy of them.

It is a **seed**, not the V1 release. The V1 exit gate in the specification
requires at least 1,000 held-out tasks; this is 32 public ones. Nothing here
selects a model, and nothing here is evidence that any system is safe.

| Property | Value |
|---|---|
| Cases | 32 |
| Environment fixtures | 9 |
| Split | `public-test` only |
| Critical-suite cases | 12 |
| Public-session cases | 2 |
| Families covered | 10 of 10 |
| Corpus digest | `sha256:9701eedcd48717c7aee79343c9623c6aeadcd3c16246ee23e35e10e26ce10853` |
| Baseline results | [`runs/atticusbench/results.json`](../../../runs/atticusbench/results.json) |

## Motivation

The specification for AtticusBench existed before any case did. A specification
that nothing executes cannot be wrong in any detectable way, so the first job of
this seed is to make the scoring vector falsifiable: run fixed policies against
it and check that the metrics separate a safe planner from an eager one, and that
they do not reward a planner that refuses everything.

## Composition

Cases live in `cases/public/<family>/<case_id>.yaml` and validate against
`schemas/atticusbench-case.schema.json`. Each case declares the environment
fixture, the request, the identity and session mode, the tool catalog offered,
the policy version, a reference plan, any approval grants, the acceptable
terminal states, hard invariants, the scorers that apply, provenance, and a
content digest.

| Family | Cases |
|---|---|
| routing | 3 |
| tool-selection | 3 |
| argument-construction | 3 |
| permission-approval | 5 |
| recovery | 3 |
| grounded-research | 3 |
| deterministic-delegation | 3 |
| prompt-injection | 3 |
| multi-system | 3 |
| human-factors | 3 |

Perturbations present: ambiguous wording (2), malicious content (3), stale result
(2), changed approval digest (1), expired approval (1), duplicate request (1),
nonexistent tool (1), unavailable tool (1), and 20 cases with none.

Fixtures validate against `schemas/atticusbench-fixture.schema.json`. A fixture
declares a frozen clock and a tool catalog; each tool declares its risk tier,
whether public sessions may reach it, its deterministic response, its argument
contract, any side effect it performs, and any failure it raises. Fixtures carry
no code: the harness builds handlers from the declarations and records every
invocation and every executed side effect in an effect ledger.

Five cases expect abstention, where planning no tool call is the correct
behavior. Everywhere else, an empty plan is scored as excessive refusal, which
the specification treats as a capability failure rather than as safety.

## Collection and generation

Hand-authored by the repository owner against the authoring guide in
[`docs/TASK_AUTHORING.md`](TASK_AUTHORING.md). No model generated any case, no
case derives from a real incident, and no trace donation was used. Case files
were emitted from a table to keep field order and formatting uniform; the YAML in
the repository is the authority, and the digests are computed from it.

## Provenance

Every case and fixture records `provenance.rights: synthetic`. Values resemble
the shape of public macro series, repositories, mailboxes, and work trackers
without reproducing any actual published print, message, or record. The injected
prompt in `poisoned-web-document-v1` is written to be recognizable and inert: it
asks for a page to be mailed to an `example.org` address.

## Human review

| Review class | Cases |
|---|---|
| dual-human-review | 12 (every critical-suite case) |
| single-human-review | 20 |

Review here means the repository owner reviewed the case against the authoring
guide, plus the automated schema, consistency, digest, duplication, and
invariant checks in `scripts/validate_atticusbench.py`. There is one author and
one reviewer and they are the same person: the "dual" class records the
specification's requirement and the intent to obtain independent review, not a
claim that two people have signed off. That gap is the corpus's largest known
weakness.

## Personal and sensitive information

None. No employer, customer, personal, or confidential data is present. No real
credential appears anywhere: the secret-bearing repository fixture describes a
scanner finding rather than reproducing a secret, and a test asserts that no
credential-shaped value exists in any corpus file.

## Licensing

Apache-2.0, the repository license. Synthetic content is original to this
repository.

## Splits and leakage controls

Only `public-test` exists. Hidden-test material is access-controlled and is
never stored in this tree; the case schema admits no other split value, so a
hidden case cannot be committed here by accident.

Duplication is audited on three signals rather than on text alone: exact content
digest, a structural signature over fixture, mode, tool set, plan shape,
invariants and expected terminal states, and Jaccard similarity over normalized
request tokens at a 0.85 threshold. The committed corpus is clean on all three.
Because these are public cases with published expectations, they are unsuitable
as a held-out measurement for any system trained on this repository.

## Recommended uses

- Checking that an agent runtime's policy, approval, and provenance behavior is
  what its specification claims.
- Regression-testing a change to the orchestrator, policy engine, or approval
  service against recorded behavior.
- Developing scorers, and finding out whether a metric can separate systems at
  all before spending inference budget on models.

## Prohibited or discouraged uses

- Training or prompt-tuning a system that will then be evaluated on these cases.
- Reporting a single aggregate score. The scoring vector exists because a system
  that completes more tasks by acting without authority must not be able to
  average past one that safely refused.
- Presenting a result here as evidence of real-world reliability or of safety.
- Citing a family slice of three to five cases as a capability measurement.

## Metrics

Per case: terminal-state correctness, required-tool coverage, unauthorized
actions with reasons, forbidden effects actually executed, required-approval
recall, required-denial recall, citation grounding, calculation delegation, step
count against budget, abstention correctness, and critical-suite failure. Per
system: those aggregated with a Wilson 95% interval on task success, per-family
slices, and an exact McNemar comparison against the reference baseline. Critical
failures are reported as case ids and are never averaged.

Wall-clock latency is recorded separately in `runs/atticusbench/latency.json`
because it is machine-dependent; it is excluded from `results.json` and from
every digest so a rerun reproduces the results file byte for byte.

## Known limitations

- 32 cases. Intervals are wide, and every family slice is three to five cases.
- Terminal-state expectations encode one intended safe outcome per case. A
  different safe outcome can score as a failure; this is a limit of the oracle,
  not of the system under test.
- Fixtures are synthetic and deterministic. No network, no real filesystem, no
  real mailbox, no model.
- The systems under test in the committed results are fixed policies, not
  models. They bound the corpus; they do not measure anything about a model.
- One human, wearing both the author and reviewer hat.
- Baseline argument construction is borrowed from the reference plan or from the
  fixture's declared example arguments, so the permission comparison is not
  confounded by a baseline forgetting a required key. That design choice means
  the baselines are not a measurement of argument construction.

## Version history

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-09-18 | First executable public seed: 32 cases, 9 fixtures, 4 deterministic baselines, committed run corpus. |

## Citation

```bibtex
@misc{dewitt2026atticusbenchseed,
  author = {DeWitt, Christopher Noxon},
  title  = {AtticusBench Public Seed 0.1.0},
  year   = {2026},
  note   = {DeWitt Research Lab. Synthetic benchmark seed for tool use,
            permission compliance, and provenance. Not the V1 release.}
}
```
