---
document_id: DRL-WEB-023
title: "Research Page Copy Draft"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-08
---

# Research page copy draft

Copy for `/research` on `www.dewitt-labs.com`, drawn from
`docs/10-research/COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` v1.1.0 and
`docs/10-research/CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md`.

**Status: DRAFT, not applied.** No site write is authorised.

## Honesty constraints for this page

This page is read by people who will check. Every constraint below is
load-bearing:

- **Nothing here is published, peer-reviewed, or submitted.** The program is
  proposed. Say so.
- **No results are claimed.** No experiment has been run. There is no dataset, no
  participant record, no venue.
- **Papers I and III are in bounded redesign**, not in progress, following the
  novelty review. Do not describe them as active work.
- **No degree, affiliation, advisor, grant, or lab is claimed** beyond current
  enrolment in the UNC-Chapel Hill Master of Applied Data Science program.
- The mathematical model is a **research hypothesis**, not a finding about how
  beliefs behave.

---

## Page copy

### Header

> **Research**
>
> A proposed research program, its open questions, and the review that made me
> narrow it.

### Opening

> I'm interested in whether the mathematics of finance under uncertainty can say
> something testable about intelligence under uncertainty.
>
> Thought has a price. Beliefs move stochastically as evidence arrives.
> Incoherent beliefs can be arbitraged. Multiple minds can form a market.
>
> Those four sentences are the program. They are framed as hypotheses to be
> falsified, not as claims I have established.

### The shared object: belief diffusion

> Across all three questions I represent belief in a proposition as log-odds and
> model its movement as a stochastic process with drift, diffusion, and optional
> jumps — driven by observable evidence and framing.
>
> This is a **model family and a research hypothesis**, not a claim that human or
> machine beliefs actually follow a diffusion. The work starts with interpretable
> baselines — exact Bayesian updating, bounded and asymmetric updating,
> drift-diffusion and Ornstein-Uhlenbeck processes — and only reaches for a
> neural SDE if the simpler models fail predefined criteria. A model that fits
> because it has more parameters has not taught me anything.

### Three questions

> **The option value of thinking.** When should a bounded system stop acquiring
> information or spending computation and commit to an answer? Formally this is
> optimal stopping over a belief state, with an explicit cost of thinking.
>
> **Language, arbitrage, and the price of belief.** Do payoff-equivalent
> descriptions produce different valuations, in people or in models? And can
> coherence repair remove exploitable inconsistency without destroying useful
> information? The interesting part is that repair might improve coherence while
> leaving calibration unchanged or worse — so both have to be measured separately.
>
> **A market of minds.** When does aggregating forecasts across many agents pool
> independent information, and when does it amplify shared error? I suspect
> nominal model diversity overstates epistemic diversity when the agents share a
> model family, training history, or retrieval source.

### What I require of a paper

> Every paper in this program has to carry four things: a precise mathematical or
> computational object; an empirical question with outcomes frozen in advance; a
> human-behaviour baseline or a documented reason one isn't appropriate; and a
> reproducible artifact — software, data, benchmark, or visualisation.
>
> A paper is not ready because its title is memorable.

### The review that narrowed the program

> This is the part I'd most want a reader to see.
>
> Before running any experiment, I reviewed the three proposed contributions
> against current primary sources. The review found that recent work
> substantially overlaps two of them, and occupies part of a third.
>
> - **Option value of thinking** — stop as worded, redesign. Recent work already
>   tests whether a learned stopping policy over observable features beats fixed
>   budgets and confidence thresholds under explicit cost accounting. That was my
>   proposed primary hypothesis.
> - **Market of minds** — stop as worded, redesign or convert to a registered
>   replication. Current work directly tests private-signal model prediction
>   markets, correlated error, and incentive-compatible aggregation.
> - **Language, arbitrage, and the price of belief** — keep, narrow, and make it
>   the flagship. Framing effects and coherence repair are established
>   separately; what still looks differentiable is the conjunction of
>   payoff-equivalent financial claims, deterministic replication oracles, paired
>   human and model valuation, implied-volatility distortion, and an explicit
>   calibration-versus-repair trade-off. Dutch-book repair is a baseline here,
>   not the contribution.
>
> The program is not abandoned. It is narrowed: one flagship paper, the belief
> diffusion bridge retained as shared instrumentation, and two questions in
> bounded redesign rather than experiments run against occupied hypotheses.
>
> I would rather find this out now than after collecting data. Checking whether
> the question is still open is part of the method, not a formality before
> submission.

### Where this stands

> Nothing here is published or submitted. No experiment has been run, no dataset
> collected, and no venue selected. The current state is: an approved program
> document, a dated novelty review, a decision to narrow, and instrumentation
> being built in the open.
>
> The engineering on the rest of this site — recorded runs, evidence lineage,
> evaluation harnesses — is the instrumentation this research would need. Building
> it first is deliberate.

### What I'm looking for

> I'm a Master of Applied Data Science student at UNC-Chapel Hill, working toward
> doctoral study in computer science. I'm interested in conversations with
> researchers working on belief dynamics, calibration, forecast aggregation, or
> the economics of reasoning under uncertainty — and with faculty considering
> students on these questions.
>
> If you think one of these questions is already answered, I would genuinely like
> to know. That is what the review above is for.

---

## Notes for whoever applies this

1. Do not convert "proposed" into "current research" anywhere in the copy.
2. Do not name a target venue, journal, or conference.
3. Do not add citations to specific prior work on the public page. The novelty
   review names sources internally; publishing an incomplete public bibliography
   invites the argument that the review was thin.
4. Keep the narrowing section. It is the most differentiating content on the page
   for an academic reader, and removing it to look more accomplished would make
   the page both weaker and less true.
5. The founder line stays factual: MADS student at UNC-Chapel Hill, working
   toward doctoral study. Do not imply the degree is held or the application is
   accepted.
