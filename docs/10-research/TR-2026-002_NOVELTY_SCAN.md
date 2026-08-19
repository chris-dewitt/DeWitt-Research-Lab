---
document_id: DRL-RES-008
title: "TR-2026-002 Preliminary Primary-Source Novelty Scan"
version: 0.1.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-19
---

# TR-2026-002 Preliminary Primary-Source Novelty Scan

## 1. Why this document exists

`TR-2026-002` has never had a novelty review. `CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md`
covered the three CFI papers and the Belief Diffusion bridge; the bake-off
harness was engineering under DIR-004 and was never in its scope. The report
therefore carries an implicit novelty position that nothing has tested.

**This is a preliminary scan, not a G1 review.** CFI-002 retained 31 records
under a stated admissibility protocol. This scan examined seven and verified
four against canonical records. It is enough to reposition the report's framing
and nowhere near enough to support a novelty claim. Every disposition below is
provisional.

Verification standard follows CFI-002 §3.2: a record counts only if title,
authorship, date, and identifier could be checked and an abstract or primary
text was inspectable. Search snippets and generated summaries were
discovery-only — two of the four verified records materially contradicted the
summary that surfaced them, which is why the rule exists. All four matrix
records were opened and verified on **2026-08-19**; that is also the
revalidation anchor, and 2025-2026 preprints should be re-opened before any G1
sign-off.

## 2. The claim under test

TR-2026-002 §1: *can the conditions under which a model-selection result is
trustworthy be expressed as executable preconditions rather than as reviewer
judgment applied after the fact?*

Decomposed, so collisions can be attributed:

| Component | Statement |
|---|---|
| C1 | Leaderboard-style reporting hides whether the measurement supports a selection |
| C2 | Trustworthiness conditions can be made executable and machine-checkable |
| C3 | A gate can *refuse* to conclude, returning structured reasons, and no score overrides it |
| C4 | The conditions include non-performance admissibility (measurement provenance, revision pinning, licence clearance) alongside statistical ones |
| C5 | The gate governs *selection among candidate models*, not release of one system |

## 3. Verified collision matrix

| Source | Establishes | Overlap | Remaining gap | Risk |
|---|---|---|---|---|
| [Falsifiable Release Gates for Self-Improving Systems (Soni, 2026), arXiv:2607.13070](https://arxiv.org/abs/2607.13070) | A methodology in which each new capability must pass a pre-declared, machine-checkable acceptance suite before shipping, with standing invariants preserved across gates; reports auto-rejecting a candidate that only inflated confidence. | **C2 and C3 directly.** Pre-declared machine-checkable preconditions that block, and a documented refusal of a candidate. | Governs a self-improving code runtime's own releases, not selection among externally benchmarked model candidates. No measurement-provenance, revision-pinning, or licence conditions. | **High for C2/C3** |
| [Automated Self-Testing as a Quality Gate (Maiorano, 2026), arXiv:2603.15676](https://arxiv.org/abs/2603.15676) | Quality gates issuing evidence-based PROMOTE/HOLD/ROLLBACK decisions over five dimensions, evaluated longitudinally across 20+ releases; evidence coverage is the primary severe-regression discriminator. | **C2 and C3 directly**, and establishes "evidence sufficiency blocks a decision" as an implemented, evaluated idea rather than a proposal. | Release management for one deployed application. Explicitly does not address selection among candidates, measurement provenance, licence clearance, or margin over a runner-up. | **High for C2/C3** |
| [Resolution Diagnostics for Paired LLM Evaluation (Kotawala, 2026), arXiv:2605.30315](https://arxiv.org/abs/2605.30315) | Frames paired LLM evaluation as hypothesis testing, inverts level-alpha power-(1-beta) tests, and reports a per-pair resolution ratio; finds many leaderboard adjacent-rank pairs unresolved, robust to multiplicity and clustering. | Occupies the **margin condition's subject matter** far more rigorously than TR-2026-002's asserted `min_margin: 0.05`. | Provides diagnostics for interpretation; stops short of a precondition that refuses a conclusion. Does not gate. | **Medium-high, and directly actionable** |
| [The Leaderboard Illusion (Singh et al., 2025), arXiv:2504.20879](https://arxiv.org/abs/2504.20879) | Documents systematic distortion in Chatbot Arena rankings from undisclosed private testing, selective score retraction, and large data-access asymmetries between proprietary and open models. | **C1 outright.** | Diagnoses the problem; proposes policy remedies rather than an executable gate. | **Contribution-collapsing for C1** |

Discovered but unverified, and therefore not load-bearing: *When Benchmarks are
Targets* (arXiv:2402.01781), *Quantifying construct validity in LLM evaluations*
(arXiv:2602.15532), and *Workflows and Smells of Leaderboard Operations*
(arXiv:2407.04065). Each appears to bear on C1 and should be opened before any
G1 sign-off.

## 4. Provisional disposition

**KEEP, NARROW, AND REFRAME.** Not contribution-collapsing, but the report's
current framing does not survive contact with this literature.

1. **C1 must stop being presented as an insight.** TR-2026-002's abstract opens
   by observing that ranking "hides the decision that actually matters." That is
   the established consensus of an active critique literature, not an
   observation the report contributes. It should be cited as background.
2. **C2 and C3 are occupied in adjacent settings.** Executable gates that refuse
   on insufficient evidence exist and have been evaluated — in release
   management and in self-improving runtimes. The report cannot claim the
   refusing-gate pattern as its own.
3. **What may remain differentiable is C4 combined with C5**: a gate over
   *selection among candidate models* whose blocking conditions mix statistical
   adequacy with non-performance admissibility — provenance, revision pinning,
   licence clearance — and which returns a structured refusal. Both verified
   gate papers explicitly lack all three of those conditions. This is a narrow
   claim, and it is a hypothesis until a proper search tests it.
4. **The null result stands regardless.** The report's only empirical claim is
   that the gate refuses under specified conditions. Nothing here touches it.

## 5. The most useful finding

Kotawala gives the correct formal object for TR-2026-002's weakest condition.
The report's `min_margin: 0.05` is asserted from judgment, and §6 already admits
the thresholds are "not derived from a power analysis." Resolution Diagnostics
supplies exactly that analysis: invert a level-alpha, power-(1-beta) paired test
and report the resolution ratio `q = N/N*`.

Replacing a hand-set margin with a power-based resolution condition would make
the margin gate principled rather than asserted, and would let the report cite
the source that motivated it. It also carries a warning worth heeding: that
paper finds the common unpaired Cohen-h shortcut off by roughly a factor of two
in exactly the close-comparison regime a margin gate operates in — which is the
regime where two candidates tie.

This is recorded as a recommendation. Changing a gate threshold is a material
change to the instrument and belongs to the Director, not to this scan.

## 6. Limitations and non-claims

- Seven records examined, four verified. CFI-002 retained 31 under a stated
  protocol. This is not comparable coverage and must not be cited as a G1 review.
- No systematic search protocol, no query-family enumeration, no screening
  ledger, no second reviewer.
- Abstract-level verification only. Theorem- or artifact-level reuse would need
  full-text reads.
- 2026 preprints are high-volatility evidence and can be revised or withdrawn.
- Absence of a collision here is evidence of a thin search, not of novelty.
- No claim is made that TR-2026-002 contains a novel contribution.

## 7. Next actions

1. Run a real nearest-neighbour search against C4+C5 before any novelty language
   enters the report.
2. Open the three unverified records in §3.
3. Director decides on the `min_margin` recommendation in §5.
4. Reframe TR-2026-002 §1 and its abstract so C1 reads as cited background.
