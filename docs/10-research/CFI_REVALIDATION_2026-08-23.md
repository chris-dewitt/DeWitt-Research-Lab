---
document_id: DRL-RES-009
title: "CFI Novelty Revalidation: Published-Journal Stratum"
version: 0.1.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---

# CFI Novelty Revalidation: Published-Journal Stratum

## 1. What this is, and what it is not

The 2026-08-05 review (`CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md`, DRL-RES-006) set
a revalidation boundary of **2026-09-05**. This is the first pass against it.

It is a **companion record, not an edit**. DRL-RES-006 stays as its own dated
artifact — rewriting a dated review to match later knowledge would destroy the
thing that makes it evidence. Where this pass contradicts it, the contradiction
is stated here.

Revalidation has two halves. **This document is the second half only.**

| Half | Status |
|---|---|
| Re-open the 14 dated 2025-2026 preprints for revision, withdrawal, or acceptance | **Not done** |
| Fresh nearest-neighbour search in a stratum the original did not cover | Done, this document |

## 2. The finding that matters most is about method

DRL-RES-006 retained 31 records. They are overwhelmingly **arXiv and OpenReview
preprints**: BayesBench, BLF, LearnStop, Galanis, Monoculture, WALLA, Nous. Its
search protocol (§3.2) describes scholarly web queries verified against arXiv
records, OpenReview submissions, proceedings, and DOI pages — but in practice
the retained set is dominated by machine-learning preprints.

**The published journal literature was under-searched.** Four searches of a
full-text journal corpus surfaced close neighbours on all four tracks that the
original review never saw. That is not a criticism of its rigour within its
stratum; it is a statement about coverage.

This is why **RES-025** withdrew the independent-reviewer precondition and
replaced it with a stratum-coverage rule. A reviewer was never going to be
recruited. The gap a reviewer would have caught is real, and is demonstrated
below.

## 3. Coverage of this pass

- **Stratum:** full-text journal corpus, predominantly Wiley-published titles
  across finance, economics, accounting, behavioural decision making, cognitive
  science, and risk analysis.
- **Queries:** four, one per track, phrased as full research questions.
- **Date bounds:** 2024-2025 lower bounds depending on track; no upper bound.
- **Verification level:** citation metadata and abstracts as returned by the
  corpus. **Canonical publisher pages were not individually opened.** Under
  DRL-RES-006 §3.2's own admissibility rule these are therefore *candidate*
  records, not verified ones, and must be opened before any of them is cited in
  a submission.
- **Not covered by any pass so far:** ACM and IEEE proceedings, PubMed beyond
  what DRL-RES-006 already held, SSRN, and non-Wiley economics journals.

## 4. Candidate neighbours by track

### 4.1 Paper II — the flagship

| Source | Bearing |
|---|---|
| Charles, Frydman & Kilic (2024), *Insensitive Investors*, Journal of Finance 79(4):2473-2503 | Experimentally elicits **valuations** and finds them "far too insensitive to their expectations, relative to the prediction from a frictionless model." Elicited valuation measured against a normative benchmark, in humans — the same measurement shape Paper II uses. Not the same contribution; a neighbour close enough that omitting it would look like an oversight. |
| Martin & Mandel (2024), *Calibration Feedback With the Practical Scoring Rule Does Not Improve Calibration of Confidence*, Futures & Foresight Science 7(1) | A published **null result** on calibration intervention. Supports rather than threatens Paper II's insistence on measuring coherence and calibration separately, and gives that separation precedent outside the LLM literature. |
| Kelly & Mandel (2024), Applied Cognitive Psychology 38(5) | Calibration training on analysts' judgments; background for the calibration axis. |

**No direct collision with the narrowed conjunction was found in this stratum.**
Nothing here prices payoff-equivalent linguistic frames against a deterministic
replication oracle with paired human and model valuation. Paper II's disposition
from DRL-RES-006 stands.

### 4.2 Validity threat — the most consequential item in this pass

**Levy (2026), *Caution Ahead: Numerical Reasoning and Look-Ahead Bias in AI
Models*, Journal of Accounting Research 64(3):1139-1188.**

Finds that language models "exhibit extremely poor numerical reasoning" on
accounting and finance tasks and that "application in these settings should
proceed with caution," alongside significant look-ahead bias in commercial
models.

This is **not a novelty collision. It is a design flaw in Paper II.** The paper
attributes a difference between two payoff-equivalent descriptions to the
wording. That attribution requires the subject to be able to price the claim at
all. If numerical competence is unreliable, an observed framing difference may
be arithmetic noise.

**Acted on the same day.** `drl_cfi.competence` adds an unframed-control screen:
a subject that cannot price the plain claim within tolerance is excluded before
its framed answers are counted, `PairedValuation` is inadmissible without an
attached probe, and the excluded set and its reasons are retained rather than
dropped. Screening after seeing framed results would be an exclusion rule chosen
with knowledge of the outcome, which the research plan forbids.

### 4.3 Shared bridge — Belief Diffusion

| Source | Bearing |
|---|---|
| Aydogan, Baillon, Kemel & Li (2025), *How much do we learn?*, Quantitative Economics 16(1) | Measures **symmetric and asymmetric deviations from Bayesian updating through choices**, extending Rabin & Schrag with conservatism and confirmatory bias. The bridge lists "bounded or asymmetric Bayesian updating" as its second interpretable baseline. This is that baseline, published and peer-reviewed. |
| Spiliopoulos & Hertwig (2024), Journal of Behavioral Decision Making 37(5) | Noisy retrieval of experienced probabilities underlying judgment of multiple uncertain events; bears on whether deviations are noise or bias. |

**Raises the bridge's collision level in the human-behaviour stratum.**
DRL-RES-006 already narrowed the bridge to instrumentation rather than
contribution; this reinforces that and adds baselines the bridge must compare
against rather than reinvent.

### 4.4 Paper I — the redesign is more occupied than the review suggested

RES-020 authorized re-scoping Paper I around **costly active information
acquisition over a calibrated belief state**. DRL-RES-006's Paper I row cites
only machine-learning work — LearnStop, Horvitz, Hay, Callaway, Graves,
algorithm selection by rational metareasoning. It contains **no economics or
experimental cognitive-science work at all**.

| Source | Bearing |
|---|---|
| Russek, Acosta-Kane, van Opheusden, Mattar & Griffiths (2025), *Time Spent Thinking in Online Chess Reflects the Value of Computation*, Cognitive Science | Value of computation, measured empirically in humans at scale. This is close to the human baseline the Paper I redesign wanted to establish. |
| Purohit & Srivastava (2026), *A Metacognitive Appraisal of Quitting in Chess*, Cognitive Science 50(3) | Stopping decisions and metacognition in humans, explicitly against foraging and metacognitive stopping models. |
| Brookins, Brown & Ryvkin (2026), Journal of Economics & Management Strategy | Laboratory experiment on **evidence gathering** under different reward schemes. |
| Larionov, Pham, Yamashita & Zhu (2025), Journal of Economics & Management Strategy | Mechanism design with flexible but **costly information acquisition**. |
| Laiho, Murto & Salmi (2025), Theoretical Economics 20(1):93-130 | Gradual learning from incremental actions under uncertainty. |
| Liu, Gershman & Bari (2025), Topics in Cognitive Science 18(2) | Quantifying the mental cost of context-sensitive decisions. |

**Disposition unchanged but the bar is higher.** Paper I remains stopped as
originally worded. The redesign direction needs its own dated search covering
this stratum before a question is approved — a search of the ML stratum alone
would have declared it open.

### 4.5 Paper III — an entire adjacent field was missed

DRL-RES-006's Paper III row is strong on LLM prediction markets and on
foundational aggregation theory. It contains nothing from **structured expert
judgment**, which is a mature published field addressing the same question.

| Source | Bearing |
|---|---|
| Lehmann (2025), *Mechanisms for Belief Elicitation Without Ground Truth*, Journal of Economic Surveys 40(1):505-527 | Review of 25+ years of information elicitation without verification — the mechanism-design half of Paper III, already surveyed. |
| Nane & Cooke (2024), Futures & Foresight Science 6(4) | Scoring rules and performance on expert judgment data; distinguishes rewarding honesty from rewarding quality. |
| Rongen, Nane, Morales-Napoles & Cooke (2025), Futures & Foresight Science | Evaluates five scoring rules for statistical accuracy in structured expert judgment. |
| Allen & Webber (2025), Scottish Journal of Political Economy | Consensus, diversity and wisdom of the crowd as a natural experiment with human forecasters. |
| Schultze, Stern & Schulz-Hardt (2025), Journal of Behavioral Decision Making | Learning processes in the judge-advisor system. |

**Disposition unchanged and reinforced.** Paper III stays stopped as worded. Its
proposed formal core — proper scoring rules and aggregation — is not merely
occupied by recent LLM work but by a decades-old published field.

## 5. What changed, what did not

**Changed:**
- Paper II gains a required numerical-competence screen, implemented.
- The G1 gate now requires two-stratum coverage (RES-025); the
  independent-reviewer precondition is withdrawn.
- Paper I and Paper III redesigns each require a dated search of the
  published-journal stratum before a question is approved.

**Unchanged:**
- Paper II remains the flagship, and its narrowed conjunction survived this pass.
- Papers I and III remain stopped as originally worded.
- The bridge remains instrumentation, not a contribution.

## 6. Limitations and non-claims

- **Half the revalidation is outstanding.** The 14 dated preprints have not been
  re-opened for revision, withdrawal, or acceptance. The 2026-09-05 boundary is
  not met by this document alone.
- Records here are **candidates, not verified** — abstract-level metadata from
  one corpus, without opening canonical publisher pages.
- One publisher's corpus is not the published literature. ACM, IEEE, SSRN, and
  non-Wiley economics titles remain unsearched by any pass.
- Four queries per four tracks is a thin instrument. Absence of a collision here
  is weak evidence of novelty and must not be reported as strong.
- No empirical claim about humans, models, or markets is made by this document.

## 7. Next actions

1. Re-open the 14 dated preprints from DRL-RES-006 §4 — the outstanding half.
2. Open canonical publisher pages for the Paper II and bridge candidates before
   any of them is cited.
3. Dated stratum searches for the Paper I and Paper III redesign questions
   before either is approved.
4. Extend coverage to at least one non-Wiley stratum, which RES-025 now requires
   for any public novelty claim.
