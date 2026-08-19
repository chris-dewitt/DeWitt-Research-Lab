---
document_id: DRL-RES-007
title: "CFI Candidate Human-Data Rights and Ethics Register"
version: 0.1.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-19
---

# CFI Candidate Human-Data Rights and Ethics Register

## 1. Decision state

This is the opening record for **CFI-003**, covering candidate human datasets
for the Paper II human baseline. It is a *preparation* artifact. Agents may
prepare rights and ethics reviews; they may not acquire, transform, or use
candidate human data before the **G2** gate, and none was.

**No dataset was downloaded. No file was retrieved. No record was transformed.**
Every finding below comes from reading a canonical landing page, and each row
records the URL and retrieval date so a reviewer can re-open the same page.

G2 remains open. Nothing here authorises acquisition.

## 2. What Paper II actually needs

The human baseline must support the *paired framing* construct: the same
economic payoff, described two ways, valued by the same person. That is a
narrower requirement than "human risky-choice data," and the distinction turns
out to matter more than licensing.

| Requirement | Why it binds |
|---|---|
| Payoff-equivalent alternative descriptions | Without a frame manipulation there is no framing effect to baseline |
| Within-subject pairing | The estimand is a paired difference; between-subject data cannot supply it |
| Elicited valuations, not just choices | Implied-volatility distortion needs a price, not a binary preference |
| Recoverable payoff structure | The replication oracle must be able to price what the subject saw |

## 3. Candidate register

Verification state is recorded per field. "Verified" means the stated value was
read on the cited page on the retrieval date; it does not mean a lawyer reviewed
it.

### 3.1 CPC18 — raw competition data

| Field | Value | State |
|---|---|---|
| Canonical source | https://zenodo.org/records/2571510 | Verified 2026-08-19 |
| Persistent identifier | `10.5281/zenodo.2571510` | Verified 2026-08-19 |
| Authors / issuing body | Plonsky, Ori; Erev, Ido; Ert, Eyal | Verified 2026-08-19 |
| Publication date | 2019-02-18 | Verified 2026-08-19 |
| Licence | Creative Commons Attribution 4.0 International | Verified 2026-08-19 |
| Redistribution permitted | Implied by CC BY 4.0, subject to attribution | **Not independently confirmed** |
| Participant and collection context | Competition entrants' choices under risk, ambiguity, and experience | **Unverified — requires full-text read** |
| Sensitive attributes | Unknown | **Unverified** |
| Re-identification risk | Unassessed | **Unverified** |
| IRB / ethics consultation needed | Undetermined | **Unverified** |

### 3.2 CPC18 — calibration data

| Field | Value | State |
|---|---|---|
| Canonical source | https://zenodo.org/records/845873 | Verified 2026-08-19 |
| Persistent identifier | `10.5281/zenodo.845873` | Verified 2026-08-19 |
| Authors / issuing body | Plonsky, Ori; Erev, Ido; Ert, Eyal | Verified 2026-08-19 |
| Publication date | 2017-09-05 | Verified 2026-08-19 |
| Licence | Creative Commons Attribution 4.0 International | Verified 2026-08-19 |
| Remaining fields | As above | **Unverified** |

### 3.3 choices13k — **blocked on licence**

| Field | Value | State |
|---|---|---|
| Canonical source | https://github.com/jcpeterson/choices13k | Verified 2026-08-19 |
| Associated publication | Peterson, Bourgin, Agrawal, Reichman & Griffiths (2021), *Science* 372(6547):1209-1214 | Verified 2026-08-19 |
| Contents | 13,006 risky-choice problems; ~243k human judgments collected via Mechanical Turk | Verified 2026-08-19 |
| Licence | **None stated on the repository page** | Verified absent 2026-08-19 |
| Disposition | **BLOCKED_RIGHTS** | — |

The absence of a licence is not a permissive default. `COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md`
§10 is explicit that public availability is not permission, and that terms
requiring written permission stay blocking until permission is documented. An
unlicensed public repository grants no redistribution or derivative rights, so
this candidate is blocked until the authors are asked in writing or a licensed
mirror with a verifiable canonical record is identified. It must not be used in
the interim on the reasoning that it is widely cited.

## 4. Construct-validity finding, which outranks the licensing question

All three candidates record **choices between gambles presented numerically**.
None of them applies a payoff-preserving *linguistic frame* manipulation, and
none elicits a valuation in currency units. Against §2 they fail the first and
third requirements outright.

That has a consequence worth stating plainly: **the two CC BY 4.0 datasets are
cleanly licensed and still probably unfit for Paper II's human baseline.** They
could support a different and weaker comparison — a risky-choice calibration
reference — but presenting that as the paired-framing human baseline would be a
construct substitution, which §5's claim discipline forbids.

Two routes remain, and both are Director decisions rather than agent work:

1. Find a public corpus that actually manipulates description while holding
   payoff fixed and elicits valuations. None has been identified yet; the search
   above was not exhaustive.
2. Document, under the contribution bar's explicit allowance, why a human
   baseline is not appropriate for the first machine-only pilot — and stage the
   human comparison into a follow-up rather than dropping it. Note that the
   novelty review named paired human *and* model valuation as part of the
   conjunction that makes Paper II differentiable, so dropping it permanently
   weakens the contribution.

## 5. Limitations and non-claims

- This is an opening scan, not a completed CFI-003 packet. Three candidates were
  examined; the space was not enumerated.
- Licence values are transcriptions of what a landing page displayed on one
  date. Pages change, and a Zenodo record can carry files under terms differing
  from the record-level licence.
- No full text was read, so participant context, consent language, sensitive
  attributes, and re-identification risk are unassessed for every candidate.
- No claim is made that any candidate is eligible. Eligibility is a G2 decision
  by the dataset steward with an ethics and rights second pass.

## 6. Next actions

1. Director or dataset steward reviews §4 and decides between the two routes.
2. If route 1: run a proper corpus search against the §2 requirements before any
   further rights work, since licensing an unfit dataset wastes the effort.
3. If route 2: record the documented reason in the protocol packet, and keep the
   staged human comparison in scope for the follow-up.
4. Either way, CFI-003 stays open and G2 stays closed until a steward signs it.
