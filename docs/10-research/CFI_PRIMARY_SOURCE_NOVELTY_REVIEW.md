---
document_id: DRL-RES-006
title: "Computational Finance of Intelligence: Primary-Source Novelty Review"
version: 1.1.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-05
---

# Computational Finance of Intelligence: Primary-Source Novelty Review

## 1. Decision state

This document is the dated research record for CFI-002 and DRL-032. It is a
structured scoping review, not a systematic review, peer review, or claim that
any proposed contribution is novel. It compares the approved Belief Diffusion
bridge and three paper questions in
`COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md` with inspectable primary sources.

**G1 stop condition triggered on 2026-08-05.** Recent primary work
substantially overlaps the proposed contributions of Paper I and Paper III and
occupies part of Paper II's coherence-repair contribution. The approved
questions have not been silently renamed. The Director approved Option A in
RES-020 on 2026-08-05. DRL-032 remains blocked pending independent G1 review
and the two bounded re-scoping packets authorized by that resolution.

No dataset, participant record, model, API, experiment, simulation, cloud
resource, or publication venue was used or selected in this review.

## 2. Executive disposition

| Track | Provisional disposition | Collision level | Evidence-based reason | What remains plausible, subject to G1 approval |
|---|---|---:|---|---|
| Shared bridge: Belief Diffusion | **NARROW** | High | BayesBench directly studies multi-turn LLM belief trajectories against Bayesian posteriors; BLF implements sequential linguistic/numeric belief updating. | Use interpretable stochastic processes as falsifiable descriptive models, emphasize parameter recovery and human/model comparison, and avoid claiming that sequential belief trajectories are a new object. |
| Paper I: Option Value of Thinking | **STOP AS WORDED; REDESIGN** | Very high | LearnStop tests whether an observable-feature learned stopper beats fixed budgets and scalar confidence/stability exits under explicit cost accounting. That is the proposed primary hypothesis. | Move from passive reasoning-prefix early exit to costly **information-acquisition actions** over a calibrated belief state, with a real-options/free-boundary contribution and a human decision baseline. A fresh nearest-neighbor search is required before approval. |
| Paper II: Language, Arbitrage, and the Price of Belief | **KEEP AND NARROW; FLAGSHIP** | Medium-high | Framing effects and LLM belief coherence are established; Outcome-Free Audits provides multi-axis Dutch-book audits and formal projection repair. | The conjunction of payoff-equivalent financial claims, deterministic replication oracles, paired human/model valuation, implied-volatility distortion, and explicit calibration-versus-repair trade-offs still appears differentiable. Dutch-book repair must be a baseline, not the novelty claim. |
| Paper III: A Market of Minds | **STOP AS WORDED; REDESIGN OR REPLICATION** | Very high | Current work directly tests private-signal LLM prediction markets, correlated errors/monoculture, and incentive-compatible wagering aggregation. | Either publish a registered replication/extension or study identification and recovery of coupled stochastic belief dynamics across human and machine markets. Either route needs a new G1 search and an approved primary question. |

The recommendation is not to abandon the program. It is to make Paper II the
flagship, retain Belief Diffusion as shared instrumentation, and place Papers I
and III into bounded redesign rather than starting experiments against
occupied hypotheses.

## 3. Search protocol

### 3.1 Search date and boundary

- Search and verification date: **2026-08-05**.
- Coverage boundary: records discoverable and inspectable on that date.
- Evidence cutoff: the review includes foundational work and current records
  through 2026-08-05; it does not claim exhaustive coverage of unpublished or
  unindexed work.
- Revalidation boundary: all 2025-2026 sources must be re-opened on
  **2026-09-05** or before G1 review, whichever occurs first. Foundational
  sources must be re-opened by **2026-11-05** or before protocol freeze.

### 3.2 Interfaces and admissible records

Discovery used title-, author-, concept-, identifier-, and domain-restricted
scholarly web queries. Verification used canonical arXiv records, OpenReview
submissions, official conference proceedings, publisher/DOI pages, PubMed
Central full text, and author or institutional copies when a publisher page
identified the same work.

An evidentiary entry was included only when all of the following were true:

1. the title, authorship or issuing body, date, and persistent identifier could
   be checked;
2. an abstract, paper, proceedings record, or official metadata record was
   inspectable;
3. the source contained a method, theorem, experiment, dataset, or formal model
   relevant to a proposed claim; and
4. the overlap statement could be supported without relying on a search
   snippet, blog, news story, vendor page, or generated summary.

Secondary commentary and search snippets were discovery-only. Citation counts,
marketing claims, and unverified benchmark rankings were excluded. Preprints
and workshop submissions were retained but labeled as high-volatility evidence;
their presence can collapse a novelty claim even when their conclusions remain
subject to peer review.

### 3.3 Query families

The reproducible query families were:

```text
(LLM OR language model OR human) AND (belief trajectory OR sequential evidence
 OR Bayesian belief updating OR drift diffusion OR stochastic belief)

(reasoning model OR metareasoning OR computation) AND (optimal stopping
 OR learned stopping OR early exit OR value of computation OR compute budget)

(LLM OR human) AND (payoff equivalent OR framing OR valuation) AND
(no arbitrage OR Dutch book OR probabilistic coherence OR coherence repair)

(LLM OR AI agent OR human) AND (prediction market OR information aggregation
 OR wagering mechanism OR correlated errors OR monoculture OR herding)

exact-title and exact-identifier checks for each retained candidate
```

The evidence set below contains 31 retained primary records. The count is an
audit count of included records, not a PRISMA claim; dynamically ranked search
interfaces did not provide a stable denominator for all surfaced candidates.

### 3.4 Screening ledger

Each retained record is counted once under its primary use even when it informs
more than one track.

| Review stratum | Retained | Verification state | Principal exclusion rule |
|---|---:|---|---|
| Shared Belief Diffusion bridge | 6 | Canonical record or inspectable primary text verified | General Bayesian/decision papers without sequential belief observables excluded |
| Paper I: stopping and metareasoning | 7 | Canonical record or official proceedings text verified | Generic efficiency and chain-of-thought papers without an adaptive stopping or computation-selection method excluded |
| Paper II: framing, pricing, and coherence | 8 | Canonical record, DOI page, or inspectable primary text verified | Finance commentary without a formal pricing/behavioral object and LLM-bias surveys without payoff control excluded |
| Paper III: markets and aggregation | 10 | Canonical record, DOI page, or official proceedings text verified | Product pages, live-market commentary, and ensemble papers without an aggregation mechanism or error-dependence analysis excluded |
| **Total** | **31** | All identities verified on 2026-08-05 | Secondary material remained discovery-only |

Candidates were also excluded when the source identity could not be resolved,
the primary record could not be inspected, the apparent match was only a search
snippet, or the work shared vocabulary but not the proposed mechanism or
estimand. No inaccessible candidate is used to support a disposition.

## 4. Nearest-neighbor collision matrix

### 4.1 Shared bridge: Belief Diffusion

| Source | What the source establishes | Exact overlap | Remaining gap | Novelty risk | Next check |
|---|---|---|---|---|---|
| [BayesBench (Samanta et al., 2026), arXiv:2606.30850](https://arxiv.org/abs/2606.30850) | Evaluates multi-turn LLM belief trajectories under sequential Bayesian estimation, prediction, and latent framing. | Directly occupies sequential evidence accumulation, observable belief paths, normative Bayesian comparison, and framing-conditioned updates. | It does not appear to compare interpretable SDE families, recover continuous-time parameters, or pair model trajectories with public human trajectories. | **Very high** for any claim that belief trajectories under sequential evidence are a new benchmark object. | 2026-09-05 |
| [Agentic Forecasting using Sequential Bayesian Updating of Linguistic Beliefs (Murphy, 2026), arXiv:2604.18576](https://arxiv.org/abs/2604.18576) | Maintains a structured linguistic/numeric belief state through an iterative tool-use loop and combines trials in logit space. | Occupies explicit linguistic belief state, sequential update, logit representation, calibration, and a forecasting application. | It is an engineered forecasting system rather than a falsifiable comparison of stochastic process families across humans and models. | **High** for the shared representation; medium for the proposed descriptive SDE layer. | 2026-09-05 |
| [Do Language Models Have Beliefs? (Wall et al., 2021), arXiv:2111.13654](https://arxiv.org/abs/2111.13654) | Develops methods to detect, update, and visualize model beliefs. | Establishes that model-belief elicitation and updating predate this program. | The present program can still operationalize probability trajectories under controlled sequential evidence without making ontological claims about internal belief. | Medium | 2026-11-05 |
| [Nassar et al. (2010), Approximately Bayesian Delta-Rule Model](https://pmc.ncbi.nlm.nih.gov/articles/PMC2945906/) | Models human belief updating in a changing environment with an approximately Bayesian learning rule. | Establishes interpretable human sequential-update baselines and change-point sensitivity. | Cross-class comparison with explicitly elicited model probabilities remains possible if data rights and task alignment pass CFI-003. | Medium | 2026-11-05 |
| [A resource-rational account of sequential effects in human prediction (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10789490/) | Explains human sequential prediction effects through bounded, resource-rational inference. | Challenges an interpretation of deviations as simple stochastic noise or bias. | A model comparison could test whether diffusion parameters add predictive value beyond resource-rational baselines. | Medium-high | 2026-11-05 |
| [A Bayesian Reformulation of Extended Drift-Diffusion (2017)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5425616/) | Relates extended drift-diffusion decision dynamics to Bayesian inference. | Makes the bridge from Bayesian evidence to stochastic accumulation established background. | Parameter recovery and cross-class falsification can still be contributions if the estimands are specified before data inspection. | Medium | 2026-11-05 |

**Bridge finding:** Belief Diffusion is viable as a shared, explicitly
falsifiable measurement and model-comparison layer. It is not currently viable
as a broad novelty claim about sequential beliefs, log-odds trajectories, or
Bayesian evidence accumulation.

### 4.2 Paper I: The Option Value of Thinking

| Source | What the source establishes | Exact overlap | Remaining gap | Novelty risk | Next check |
|---|---|---|---|---|---|
| [LearnStop (Dong, Qin, and Shah, 2026), arXiv:2606.30852](https://arxiv.org/abs/2606.30852) | Tests a hidden-state-free learned stopper using observable prefix confidence, entropy, vote share, stability, and backtracking features across reasoning tasks, with cost and lost-correct-risk accounting. | This is the proposed hypothesis: an observable-feature stopping policy compared with fixed budgets and simple confidence/stability thresholds under cost. | The source studies reasoning-prefix early exit. It does not by itself occupy a policy that chooses among costly external information-acquisition actions over a calibrated belief state, nor a human comparison. | **Contribution-collapsing** | 2026-09-05 |
| [Optimal Stopping vs. Best-of-N for Inference Time Optimization (2025), arXiv:2510.01394](https://arxiv.org/abs/2510.01394) | Frames inference-time sampling as an optimal-stopping problem using Pandora's Box and reports compute savings. | Occupies adaptive inference-time stopping and theoretical comparison with fixed sampling. | Action-dependent evidence acquisition and real-options interpretation may remain distinct. | High | 2026-09-05 |
| [Horvitz (1988), Reasoning Under Varying and Uncertain Resource Constraints](https://aaai.org/Papers/AAAI/1988/AAAI88-020.pdf) | Formalizes reasoning under uncertain and varying computational resources. | Establishes resource-aware reasoning as foundational metareasoning rather than a new connection. | Modern observable belief-state estimation and empirical human/model comparison remain open implementation questions. | Medium | 2026-11-05 |
| [Hay et al. (2012), Selecting Computations, arXiv:1207.5879](https://arxiv.org/abs/1207.5879) | Develops the value of computation and metalevel decision problems. | Occupies myopic/non-myopic computation selection and formal value-of-information foundations. | A finance-derived free-boundary analysis is useful only if it proves or predicts something beyond relabeling metareasoning. | High | 2026-11-05 |
| [Callaway et al. (2017), Learning to Select Computations, arXiv:1711.06892](https://arxiv.org/abs/1711.06892) | Learns policies for selecting mental computations in resource-rational planning. | Occupies learned computation selection and human cognitive connection. | A new contribution must distinguish external evidence actions, belief observability, and task geometry. | High | 2026-11-05 |
| [Graves (2016), Adaptive Computation Time, arXiv:1603.08983](https://arxiv.org/abs/1603.08983) | Learns how many recurrent computation steps to allocate. | Establishes adaptive compute allocation as a long-standing machine-learning objective. | It does not decide among externally costly evidence sources or produce a decision-theoretic human/model comparison. | Medium | 2026-11-05 |
| [Algorithm Selection by Rational Metareasoning (2014)](https://proceedings.neurips.cc/paper_files/paper/2014/file/7fb8ceb3bd59c7956b1df66729296a4c-Paper.pdf) | Uses rational metareasoning to choose algorithms under uncertainty about performance. | Occupies decision-theoretic selection of computational actions. | State-dependent information quality and stochastic belief dynamics may offer a narrower formal problem. | High | 2026-11-05 |

**Paper I finding:** the present primary hypothesis cannot support a novelty
claim. A viable redesign must change the object from stopping a reasoning
prefix to selecting and stopping costly evidence-acquisition actions. That is a
material question change and therefore requires DIR-008 approval plus a new
nearest-neighbor review before formalization.

### 4.3 Paper II: Language, Arbitrage, and the Price of Belief

| Source | What the source establishes | Exact overlap | Remaining gap | Novelty risk | Next check |
|---|---|---|---|---|---|
| [Tversky and Kahneman (1981), The Framing of Decisions](https://doi.org/10.1126/science.7455683) | Demonstrates predictable preference shifts under alternative formulations of equivalent decision problems. | Makes human framing effects established background. | Payoff-identical derivative claims with exact replication checks and matched machine/human valuations are more specific. | Low for background; high for broad framing claims | 2026-11-05 |
| [Black and Scholes (1973), The Pricing of Options and Corporate Liabilities](https://www.journals.uchicago.edu/doi/10.1086/260062) | Derives option valuation from a no-sure-profit replication argument under stated assumptions. | Supplies a deterministic normative oracle for a restricted task family. | Using the oracle to isolate linguistic-frame distortion is a measurement design, not a new pricing theorem. | Low if represented as oracle; fatal if represented as new finance theory | 2026-11-05 |
| [Merton (1973), Theory of Rational Option Pricing](https://doi.org/10.2307/3003143) | Extends and formalizes rational option-pricing restrictions. | Establishes no-arbitrage comparative statics and boundary conditions used by the proposed audit. | The research contribution must be behavioral/computational, not a rediscovery of option restrictions. | Low if cited correctly | 2026-11-05 |
| [Breeden and Litzenberger (1978), Prices of State-Contingent Claims](https://doi.org/10.1086/296025) | Relates option prices to state-contingent claims and implied distributions. | Establishes the finance-to-belief mapping used by the track. | A new paper may study elicited inconsistent valuations, but cannot claim the mapping itself as novel. | Medium | 2026-11-05 |
| [Framing the Game (Robinson and Burden, 2025), arXiv:2503.04840](https://arxiv.org/abs/2503.04840) | Holds game structure constant while varying contextual vignettes and finds predictable framing sensitivity in LLM decisions. | Directly occupies payoff-structure-preserving linguistic framing in LLM evaluation. | It does not center derivative replication, implied volatility, explicit arbitrage portfolios, or paired human/model repair. | High for the framing claim; medium for the financial test bed | 2026-09-05 |
| [Do LLMs Act Like Rational Agents? (Yamin et al., 2026), arXiv:2602.06286](https://arxiv.org/abs/2602.06286) | Gives falsifiable conditions under which elicited probabilities and actions cannot represent a rational agent with coherent beliefs/preferences. | Occupies belief/action rationality and probabilistic decision coherence. | Payoff-equivalent financial claims and post-repair calibration effects remain outside its stated core. | High | 2026-09-05 |
| [Outcome-Free Audits and Repairs for LLM Forecasters (Li and Sreedhar, 2026)](https://openreview.net/forum?id=U27ZfUx7JE) | Audits complementary pairs, monotonicity, Frechet bounds, and entailment; provides a formal coherent projection and separates coherence from forecast quality. | Directly occupies Dutch-book audit, probability-constraint repair, and the proposition that coherence and calibration are distinct. | It does not appear to test payoff-equivalent financial narratives, implied-volatility surfaces, deterministic replication, or paired human/model frame interactions. | **Contribution-collapsing for repair alone; medium for the combined paper** | 2026-09-05 |
| [Proud to Not Own Stocks: How Identity Shapes Financial Decisions (2026)](https://academic.oup.com/rfs/advance-article/doi/10.1093/rfs/hhag034/8677631) | Uses alternative descriptions of an underlying risky choice to study identity-linked financial decisions. | Shows that economically related financial framing is an active human-behavior research area. | The proposed controlled derivative-claim design is narrower and includes machine subjects plus formal repair. | Medium-high | 2026-09-05 |

**Paper II finding:** this is the strongest track if its novelty claim is the
controlled intersection, not any component alone. The formal repair from Li
and Sreedhar should be implemented or independently reconstructed as a baseline
subject to license review, with attribution. The paper must separately report
valuation distortion, mathematical coherence, calibration, and information
loss from repair.

### 4.4 Paper III: A Market of Minds

| Source | What the source establishes | Exact overlap | Remaining gap | Novelty risk | Next check |
|---|---|---|---|---|---|
| [DeGroot (1974), Reaching a Consensus](https://www.tandfonline.com/doi/abs/10.1080/01621459.1974.10480137) | Gives an explicit iterative opinion-pooling model and consensus conditions. | Establishes coupled opinion dynamics as foundational. | The paper could estimate richer stochastic coupling rather than claim coupled beliefs as a new idea. | Medium | 2026-11-05 |
| [Bikhchandani, Hirshleifer, and Welch (1992), Informational Cascades](https://www.journals.uchicago.edu/doi/abs/10.1086/261849) | Shows how rational agents may ignore private information after observing predecessors, producing fragile conformity. | Establishes the mechanism behind minority-information loss and herding. | Human/machine parameter estimation may remain empirical work; the mechanism is not novel. | Medium | 2026-11-05 |
| [Anderson and Holt (1997), Information Cascades in the Laboratory](https://www.jstor.org/stable/2951328) | Tests information-cascade theory experimentally with human participants. | Supplies a human experimental foundation and candidate replication family. | Dataset eligibility, task reconstruction, and rights remain unreviewed until CFI-003. | Medium | 2026-11-05 |
| [Hanson (2003), Combinatorial Information Market Design](https://hanson.gmu.edu/mktscore.pdf) | Develops market scoring rules and logarithmic forms for information aggregation with bounded-loss design concerns. | Establishes the automated-market-maker and scoring-rule machinery. | A new paper must test a new empirical or identification question, not merely deploy LMSR. | Medium | 2026-11-05 |
| [Wisdom of the Silicon Crowd (2024), arXiv:2402.19379](https://arxiv.org/abs/2402.19379) | Studies aggregation of diverse LLM forecasts. | Occupies the general claim that ensembles of model forecasts may improve prediction. | Dynamic private-signal markets and coupling diagnostics are more specific, but later work below occupies much of that space. | High | 2026-09-05 |
| [Debate or Vote? (NeurIPS 2025)](https://proceedings.neurips.cc/paper_files/paper/2025/hash/934252acd87f254d5d4672fbde283bd2-Abstract-Conference.html) | Compares multi-agent debate and voting and analyzes the dynamics of iterative aggregation. | Occupies required debate/vote baselines and questions whether interaction adds much beyond voting. | Markets and explicit private evidence remain distinct mechanisms. | High | 2026-09-05 |
| [Information Aggregation with AI Agents (Galanis, 2026), arXiv:2604.20050](https://arxiv.org/abs/2604.20050) | Runs controlled prediction markets in which AI agents receive private signals and trade; varies information structure, communication, duration, prompting, and initial price. | Directly occupies the primary question of when AI-agent markets aggregate dispersed private information. | It does not appear to center recovery of continuous-time coupling parameters or matched human/model stochastic trajectories. | **Contribution-collapsing** | 2026-09-05 |
| [Preference Optimization Drives Monoculture in LLM Prediction Markets (Begin et al., 2026), arXiv:2606.26583](https://arxiv.org/abs/2606.26583) | Measures correlated LLM errors, effective crowd size, scaling behavior, causal preference-optimization ablations, and cross-model diversity mitigation. | Directly occupies hypotheses about shared error, nominal versus epistemic diversity, and aggregation reversal under correlation. | Coupled-path identification and minority-information recovery may remain, but cannot be assumed novel. | **Contribution-collapsing** | 2026-09-05 |
| [WALLA (Luo, Pennock, and Wang, 2026), arXiv:2607.04389](https://arxiv.org/abs/2607.04389) | Proposes learned-wager aggregation with incentive-compatibility properties and bounded-deficit mechanism variants. | Occupies the mechanism-design and strategic-reporting side of model aggregation. | A distinct paper would need a different formal object or a direct falsification/replication contribution. | **Very high** | 2026-09-05 |
| [Nous (Qian, 2026), arXiv:2606.13038](https://arxiv.org/abs/2606.13038) | Extracts behavioral profiles from prediction-market wallets and tests prompt-level injection as a diversity intervention, including error correlation and Brier score. | Occupies human-derived diversity injection and reports a relevant null result. | Below-prompt interventions or explicit dynamical identification may remain, but require a new rights and novelty review. | High | 2026-09-05 |

**Paper III finding:** all four proposed hypotheses have close current work.
The original paper may still be valuable as a transparent replication and
benchmark integration, but it cannot be presented as the planned novel market
aggregation result. A coupled-SDE identification paper is only a proposed pivot
until a dedicated search finds a precise unoccupied estimand.

## 5. Claim-to-source decision table

| Proposed claim | Closest work | Collision assessment | Disposition |
|---|---|---|---|
| Sequential human/model beliefs can be modeled as log-odds trajectories under evidence and framing. | BayesBench; BLF; human Bayesian-update and drift-diffusion work | The object and principal baselines are established. Comparative SDE falsification may remain. | Narrow bridge; no standalone novelty claim. |
| An observable learned stopper improves cost-sensitive utility over fixed budgets and confidence thresholds. | LearnStop; optimal stopping vs. best-of-N | Same intervention, comparison class, and cost-sensitive outcome. | Stop as worded. |
| An intelligent system should choose when to acquire another costly item of external evidence. | Value-of-computation and learned-computation-selection literature | Established formal foundation; the belief-state/action geometry may still yield a distinct, testable extension. | Candidate redesign only; repeat search. |
| Payoff-equivalent linguistic frames create paired valuation differences. | Tversky/Kahneman; Framing the Game; financial identity framing | Broad effect established; derivative-replication task family may be distinct. | Keep as a domain-specific, paired estimand; do not claim general framing novelty. |
| Projection can eliminate constructed Dutch-book portfolios. | Outcome-Free Audits and Repairs | Directly established for several probability relations. | Baseline/replication, not contribution. |
| Repair can change coherence without improving calibration. | Outcome-Free Audits and Repairs | Directly articulated and tested. | Measure as required diagnostic; do not claim concept as novel. |
| Markets aggregate independent private information from AI agents. | Galanis; Silicon Crowd | Directly tested. | Stop broad claim. |
| Shared error/correlation weakens aggregation and nominal diversity overstates epistemic diversity. | Monoculture; Nous | Directly tested, including causal and mitigation analyses. | Stop broad claim. |
| Excess coupling suppresses minority information and causes herding. | Informational-cascade theory and human experiments; Galanis | Mechanism established; AI-market case is active. | Replication or a newly specified dynamic estimand only. |
| Incentives and wagers can improve robust decentralized model aggregation. | WALLA; Hanson | Directly occupied at both foundational and current levels. | Do not claim without a materially different mechanism or falsification target. |

## 6. G1 options for the Director

**Director disposition (2026-08-05): Option A approved in RES-020.** The
alternatives remain below as institutional history. Approval selects the
research direction; it does not replace independent G1 review, establish
novelty, authorize data acquisition, or authorize an experiment.

### Option A - Recommended: preserve the program and authorize a narrow redesign

1. Make Paper II the first full paper and require its novelty statement to be
   the controlled intersection of financial payoff equivalence, exact pricing
   or replication invariants, paired human/model behavior, and measured repair
   trade-offs.
2. Retain Belief Diffusion only as a shared measurement and model-comparison
   layer with parameter-recovery and falsification gates.
3. Return Paper I to scoping around active information acquisition rather than
   reasoning-prefix early exit.
4. Return Paper III to scoping around identifiable coupled dynamics or an
   explicitly registered replication, rather than broad aggregation and
   monoculture claims.
5. Create a follow-up novelty packet before changing the approved questions or
   beginning data work.

Consequence: preserves the interdisciplinary thesis while giving up the
weakest novelty claims before they consume an academic year.

### Option B: retain all three as replication-and-extension papers

Treat direct replication, robustness, shared open infrastructure, and matched
human/model comparisons as the contributions. This is honest and potentially
useful, but the portfolio must not imply that the underlying hypotheses are
new, and publication targets should match a replication contribution.

### Option C: retain Paper II and replace Papers I and III

Open a new ideation and literature-review cycle for two different questions at
the finance, cognition, mathematics, data-science, and computer-science
intersection. This gives the largest novelty search space but breaks the
approved three-paper narrative and requires a new program decision.

## 7. Reviewer checklist

An independent G1 reviewer must answer each item with evidence:

- [ ] Each closest-work source is the same work as its canonical identifier.
- [ ] Workshop papers and preprints are labeled and not treated as settled
      empirical truth.
- [ ] LearnStop is compared against the exact Paper I hypothesis rather than a
      weaker paraphrase.
- [ ] The Paper II novelty sentence names the intersection and does not claim
      framing, Black-Scholes, Dutch books, or projection repair as new.
- [ ] Paper III does not omit Galanis, Monoculture, WALLA, or Nous.
- [ ] Any proposed pivot receives a new nearest-neighbor search before its
      question is approved.
- [ ] A statistician reviews estimands, multiplicity, parameter recovery, and
      calibration/coherence separation before preregistration.
- [ ] A finance reviewer verifies payoff equivalence, replication assumptions,
      boundary conditions, and numerical tolerances.
- [ ] A cognitive-science reviewer checks that stochastic dynamics are treated
      as falsifiable models, not explanations inferred from curve fit alone.
- [ ] CFI-003 independently verifies rights before any human dataset is
      downloaded or transformed.
- [ ] Novelty is revalidated on the dated boundary and immediately before
      protocol freeze and submission.

## 8. Limitations and non-claims

- This was a structured, reproducible scoping pass, not dual-reviewer
  systematic screening.
- Fast-moving 2026 records may be revised, withdrawn, accepted, or superseded.
- An unindexed manuscript can still defeat a novelty claim.
- Abstract-level verification was sufficient to establish several collisions;
  theorem-level or artifact-level reuse requires full-paper and license review.
- Similarity of topic does not prove identity of contribution. The stop
  decisions above are conservative because CFI-002 is a gate before expensive
  implementation.
- No empirical conclusion about humans, models, or markets is claimed by this
  review.
- No source's availability is treated as permission to copy data, code, prompts,
  or participant records.

## 9. CFI-002 closure boundary

The literature artifact, collision record, search protocol, technical-reference
update, and reviewer checklist are complete enough for review. RES-020 selects
Option A, but the research packet is not scientifically closed: independent G1
review must confirm or revise the matrix and the redesigns need fresh nearest-
neighbor searches. Until then:

- CFI-003 dataset-rights work may be planned but not used to evade G1;
- CFI-004 schema work and all experimental packets remain dependency-gated;
- the approved questions in DRL-RES-005 remain unchanged; and
- no public statement may describe any of the three proposed contributions as
  established novelty.
