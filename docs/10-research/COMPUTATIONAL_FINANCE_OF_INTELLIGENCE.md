---
document_id: DRL-RES-005
title: "Computational Finance of Intelligence: Research Program and Agent Execution Plan"
version: 1.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-05
---

# Computational Finance of Intelligence

## 1. Authority, identity, and purpose

This document is the controlled research and execution plan for Christopher
Noxon DeWitt's Computational Finance of Intelligence program. It records the
Director's RES-017 decision and is owned by Mission 15. It does not create a
new laboratory, institute, team, degree affiliation, deployed product, or
publication claim. Public presentation remains part of Christopher's personal
academic portfolio under RES-016.

The program asks whether mathematical-finance machinery can provide useful,
testable models of intelligence under uncertainty:

> Thought has a price. Beliefs evolve stochastically. Incoherent beliefs can be
> arbitraged. Multiple minds can form markets.

The goal is three connected papers supported by one shared methods bridge,
open artifacts, reproducible experiments, and visible negative results. The
first month must produce inspectable progress without representing a pilot as a
finding or a proposed contribution as established novelty. No experiment
result is claimed by this plan.

## 2. Approved program structure

### 2.1 Shared bridge — Belief Diffusion

For subject or agent `i`, represent belief in a binary proposition by log-odds:

```text
l_i,t = log(p_i,t / (1 - p_i,t))
```

The common modeling family is:

```text
dl_i,t = mu_theta(l_i,t, e_i,t, f_i,t) dt
       + sigma_theta(l_i,t, e_i,t, f_i,t) dW_i,t
       + J_i,t dN_i,t
```

where evidence `e`, framing `f`, drift `mu`, diffusion `sigma`, and optional
jumps `J dN` are observable or estimable components. This equation is a model
family and research hypothesis, not a claim that human or machine beliefs
actually follow a diffusion.

The bridge begins with interpretable baselines:

1. exact Bayesian updating where a normative posterior is available;
2. bounded or asymmetric Bayesian updating;
3. drift-diffusion and Ornstein-Uhlenbeck processes;
4. jump-diffusion or state-space models;
5. neural SDEs only when simpler models fail predefined predictive and
   diagnostic criteria.

The bridge is expected to produce a methods report and shared software. It is
not counted as a required fourth paper. It may become a standalone paper only
if the empirical comparison supports a distinct contribution after independent
review.

### 2.2 Paper I — The Option Value of Thinking

**Working title:** *The Option Value of Thinking: Optimal Stopping Over
Stochastic Belief Dynamics*

**Primary question:** When should a bounded intelligent system stop acquiring
information or spending computation and commit to an answer?

**Formal core:** discrete-time dynamic programming and optimal stopping, with a
continuous-time HJB or free-boundary treatment as an optional extension.

```text
V(s_t) = max(
  U_commit(s_t),
  -cost(s_t, action_t) + E[V(s_t+1) | s_t, action_t]
)
```

**Proposed primary hypothesis:** A stopping policy estimated from observable
belief dynamics can improve cost-sensitive decision utility relative to fixed
reasoning budgets and simple confidence thresholds.

**Required comparisons:** fixed budget, confidence threshold, myopic value of
information, learned stopping policy, and an oracle or upper-bound policy in a
fully specified simulation.

**Human connection:** reproduce an eligible public optimal-stopping or
information-acquisition dataset before claiming a human-machine comparison.

**Portfolio artifact:** an interactive stopping-boundary simulator showing the
effect of evidence quality, error cost, compute cost, and uncertainty.

### 2.3 Paper II — Language, Arbitrage, and the Price of Belief

**Working title:** *Language, Arbitrage, and the Price of Belief: Framing
Distortions and Coherence Repair in Intelligent Systems*

This track combines the Narrative Volatility Smile and No-Arbitrage Beliefs.

**Primary question:** Do payoff-equivalent descriptions create different human
or machine valuations, and can coherence repair remove exploitable
inconsistency without destroying useful information?

**Formal core:** Black-Scholes and replication invariants where assumptions are
appropriate, state-contingent claims, probability coherence, convex
optimization, and paired experimental design.

**Proposed primary hypotheses:**

1. payoff-equivalent linguistic frames create nonzero paired valuation and
   implied-volatility differences in at least some subject/model classes;
2. a no-arbitrage projection eliminates constructed Dutch-book portfolios;
3. repair may improve coherence without necessarily improving calibration, so
   both outcomes must be measured separately.

**Required comparisons:** deterministic pricer, unassisted humans where public
data supports the comparison, conversational models, reasoning models,
tool-assisted models, and coherence-repaired outputs.

**Portfolio artifact:** a visitor prices the same economic payoff under two
descriptions, then inspects the implied-volatility difference, exploiting
portfolio, and minimum coherence repair.

### 2.4 Paper III — A Market of Minds

**Working title:** *A Market of Minds: Coupled Belief Diffusions in Human and
Machine Forecasting*

**Primary question:** When does market coupling aggregate independent
information, and when does it amplify common-mode error, herding, or strategic
misreporting?

**Formal core:** proper scoring rules, automated market makers, mechanism
design, interacting stochastic processes, and correlated-error models.

```text
dl_i,t = mu_i,t dt + sigma_i,t dW_i,t
       + kappa_i(m_t - l_i,t) dt + J_i,t dN_i,t
```

**Proposed primary hypotheses:**

1. market aggregation reduces idiosyncratic error when individual errors are
   sufficiently independent;
2. increasing shared drift or error correlation weakens or reverses that gain;
3. excessive coupling suppresses useful minority information and increases
   herding;
4. nominal model diversity overstates epistemic diversity when agents share a
   model family, training history, retrieval source, or prompt scaffold.

**Required comparisons:** unweighted and performance-weighted averaging,
majority vote, Delphi-style revision, debate where feasible, a market-scoring
rule, and at least one hybrid aggregation method.

**Portfolio artifact:** a replayable market showing private evidence, belief
paths, trades, wealth, consensus price, correlation, and resolution.

## 3. Contribution bar and non-goals

Every paper must contain all four contribution layers:

1. a precise mathematical or computational object;
2. an empirical question with frozen primary outcomes;
3. a human-behavior baseline or a documented reason it is not appropriate;
4. a reproducible software, data, benchmark, or visualization artifact.

A paper is not ready because its title is memorable. Current related work must
be reviewed from primary sources immediately before scope freeze and again
before submission. Novelty language remains provisional until that review.

The program does not aim to:

- predict or trade live securities;
- provide financial advice;
- use employer, customer, proprietary, or personal financial data;
- infer private chain-of-thought or require its disclosure;
- call public human data ethically unrestricted without review;
- train a foundation model from scratch;
- use an LLM as the authoritative financial calculator;
- force three positive results;
- submit the same empirical contribution as multiple papers;
- select a venue before contribution and evidence justify the fit.

## 4. Observable state and common data contract

Agents may use only observable experimental state. Hidden model reasoning is
not a research dependency. The common record should contain, at minimum:

| Field | Meaning |
|---|---|
| `study_id`, `run_id`, `subject_id` | Stable pseudonymous experiment identity |
| `subject_kind` | Human, model, policy, market, or simulator |
| `model_or_cohort_revision` | Exact model revision or human cohort/source |
| `task_id`, `proposition_id` | Versioned decision target |
| `step_index`, `event_time` | Ordering and time semantics |
| `evidence_id`, `frame_id` | Presented evidence and experimental frame |
| `reported_probability` | Probability report before log-odds conversion |
| `action` | Continue, stop, acquire, price, trade, defer, or abstain |
| `action_cost` | Declared compute, time, token, or experimental cost |
| `outcome` | Resolution or task outcome when lawfully available |
| `source_rights_id` | Pointer to reviewed source/rights record |
| `code_revision`, `config_digest`, `seed` | Reproduction identity |
| `maturity` | Synthetic, pilot, frozen, confirmatory, or replication |

Raw free-form human or model text is optional and content-minimized. Derived
features must preserve lineage to the source record and transformation code.

## 5. Research lifecycle and gates

Each task or paper moves through this state machine:

```text
PROPOSED
  -> NOVELTY_REVIEWED
  -> RIGHTS_AND_ETHICS_CLEARED
  -> PROTOCOL_DRAFTED
  -> PREREGISTERED
  -> PILOT
  -> DESIGN_FROZEN
  -> CONFIRMATORY
  -> INDEPENDENTLY_REPRODUCED
  -> WORKING_PAPER
  -> PUBLIC_RELEASE
```

Valid terminal or holding states include `NULL_RESULT`, `NEGATIVE_RESULT`,
`BLOCKED_RIGHTS`, `BLOCKED_VALIDITY`, `WITHDRAWN`, and `SUPERSEDED`.

### Human checkpoints

| Gate | Required approval or review | What agents must not do before it |
|---|---|---|
| G0 Program | Director | Change the three-paper structure or bridge role |
| G1 Novelty | Director, on a search covering at least two literature strata (RES-025) | Present novelty as established, or treat a single-stratum search as complete |
| G2 Data | Dataset steward plus ethics/rights second pass | Acquire, transform, or use candidate human data |
| G3 Protocol | Director/statistical reviewer | Freeze hypotheses, primary metrics, exclusions, or power plan |
| G4 Confirmatory | Director after pilot report | Inspect or run the confirmatory set |
| G5 Claim | Independent reproduction/adversarial review | Call an observed association a supported research result |
| G6 Release | Director | Publish, submit, mint a DOI, or announce a paper |

Agents may prepare decision packets for these gates. They may not approve their
own packet or treat silence as approval.

## 6. Model of agent agency

Agents are bounded research operators, not autonomous principal investigators.
The repository state, frozen protocol, and Director decisions define their
authority.

### Agents may

- build dated primary-source literature matrices;
- prepare candidate-data rights and ethics reviews;
- implement deterministic simulators, validators, baselines, and visualizers;
- write tests before running experiments;
- execute approved pilot or frozen protocols within recorded cost bounds;
- calculate predefined statistics and render figures from immutable outputs;
- identify contradictions, null results, leakage, and invalid assumptions;
- draft papers while separating proposal, observation, interpretation, and
  recommendation;
- create exact handoffs and reproduction packages.

### Agents require a gate to

- add or materially change a hypothesis, primary outcome, exclusion, or
  stopping rule;
- use a new human dataset, model family, paid API, cloud resource, or license;
- change an analysis after seeing confirmatory outcomes;
- resolve ambiguous labels or disputed human-data interpretations;
- merge related paper tracks or split one result across papers;
- communicate externally, submit, publish, or claim a result.

### Agents must never

- fabricate observations, citations, participants, sample sizes, or model runs;
- convert synthetic records into purported human observations;
- expose private or employer data;
- use an LLM judge as the sole authority for mathematical equivalence,
  coherence, or critical labels;
- optimize on the held-out confirmatory set;
- silently discard failures or outliers;
- claim authorship or assign human authorship;
- infer consent from public availability;
- weaken a test or gate to obtain a preferred conclusion.

## 7. Sequential agent roles

One agent may hold more than one role across separate tasks, but no agent may
perform the final independent review of its own experiment.

| Role | Primary output | Required independence |
|---|---|---|
| Program steward | Registry, dependency graph, decisions, scope control | Director reviews material changes |
| Literature agent | Dated novelty matrix and claim/source map | Each pass names the strata it searched; a later pass must add one the first missed |
| Data steward agent | Candidate register, rights, ethics, provenance | Human owner approves dataset eligibility |
| Methods agent | Formal model, estimands, assumptions, power plan | Statistical second pass before freeze |
| Implementation agent | Tested simulator, pipeline, schemas, baselines | Cannot certify its own scientific result |
| Experiment agent | Immutable run manifests and outputs | Runs only approved protocol/configuration |
| Evaluation agent | Predefined statistics, diagnostics, failure report | Cannot move metrics after outcome inspection |
| Reproduction agent | Clean-room rerun and discrepancy ledger | Must start from release candidate, not private context |
| Publication agent | Paper bundle, teaching note, correction path | Director approves every public claim |

## 8. Agent task graph

Task IDs below are research task packets under DRL-031, not claims of completed
work and not yet remote GitHub issues. Mission 15 files each packet as a focused
issue before execution.

### 8.1 Shared bridge and program foundation

| ID | Task | Dependencies | Exit evidence |
|---|---|---|---|
| CFI-001 | Maintain program registry and decision log | DRL-031 | Valid controlled plan and issue graph |
| CFI-002 | Build dated primary-source literature and novelty matrix | CFI-001 | Claim/source table, search protocol, gaps, reviewer notes |
| CFI-003 | Audit candidate human datasets and model/data terms | CFI-001 | Source records, rights/ethics matrix, rejected candidates |
| CFI-004 | Specify observable belief-event schema and examples | CFI-002, CFI-003 | Schema proposal, valid/invalid fixtures, privacy review |
| CFI-005 | Implement Bayesian, diffusion, OU, and jump baselines | CFI-004 | Tested reference package and synthetic recovery study |
| CFI-006 | Draft shared estimands, diagnostics, and preregistration template | CFI-002, CFI-004 | Statistical review packet; no outcomes inspected |
| CFI-007 | Build belief-trajectory viewer from synthetic fixtures | CFI-004, CFI-005 | Accessible local viewer and degraded/empty/error states |
| CFI-008 | Publish bridge methods report candidate | CFI-005, CFI-006, CFI-007 | Reproducible draft explicitly labeled methods/proposal |

### 8.2 Paper I task packets

| ID | Task | Dependencies | Exit evidence |
|---|---|---|---|
| CFI-101 | Formalize the discrete stopping problem and assumptions | CFI-002, CFI-006 | Definitions, propositions, counterexamples, review notes |
| CFI-102 | Build synthetic environment with oracle policy | CFI-005, CFI-101 | Simulator tests, oracle/regret checks, manifest |
| CFI-103 | Define observable model/human state adapters | CFI-004, CFI-102 | No hidden-CoT dependency; calibration tests |
| CFI-104 | Reproduce an eligible public human stopping dataset | CFI-003, G2 | Reproduction report and discrepancy ledger |
| CFI-105 | Run pilot and power/sensitivity analysis | CFI-102–104, G3 | Pilot report; proposed frozen design |
| CFI-106 | Run confirmatory comparison | CFI-105, G4 | Immutable outputs and predefined analysis |
| CFI-107 | Produce Paper I bundle | CFI-106, G5 | Draft, code, data manifest, figures, limitations, teaching note |

### 8.3 Paper II task packets

| ID | Task | Dependencies | Exit evidence |
|---|---|---|---|
| CFI-201 | Specify payoff-equivalence task DSL and frame taxonomy | CFI-002, CFI-006 | Canonical examples and invalid cases |
| CFI-202 | Implement deterministic pricing and replication oracle | CFI-201 | Unit, property, boundary, and independent-reference tests |
| CFI-203 | Map eligible human risky-choice data to supported constructs | CFI-003, G2 | Mapping report with exclusions and non-comparable fields |
| CFI-204 | Implement arbitrage detector and coherence projection | CFI-202 | Exploiting portfolios, convex checks, distortion measures |
| CFI-205 | Run paired framing pilot and freeze analysis | CFI-202–204, G3 | Pilot, power, leakage audit, frozen metrics |
| CFI-206 | Run confirmatory human/model comparison | CFI-205, G4 | Immutable paired results and robustness analysis |
| CFI-207 | Produce Paper II bundle | CFI-206, G5 | Draft, benchmark, solver, viewer, limitations, teaching note |

### 8.4 Paper III task packets

| ID | Task | Dependencies | Exit evidence |
|---|---|---|---|
| CFI-301 | Select and reproduce an eligible human forecasting corpus | CFI-003, G2 | Rights-cleared manifest and baseline reproduction |
| CFI-302 | Implement aggregation replay baselines | CFI-301 | Averaging, weighting, scoring, calibration tests |
| CFI-303 | Implement market mechanism and incentive tests | CFI-302 | Conservation, bounded-loss, truthfulness/strategy diagnostics |
| CFI-304 | Implement coupled-belief and correlated-error simulation | CFI-005, CFI-303 | Parameter recovery and failure-regime fixtures |
| CFI-305 | Run pilot human/model/market comparisons | CFI-304, G3 | Pilot, power, shared-error audit, frozen design |
| CFI-306 | Run confirmatory aggregation study | CFI-305, G4 | Immutable outputs, preregistered statistics, nulls/failures |
| CFI-307 | Produce Paper III bundle | CFI-306, G5 | Draft, simulator, replay viewer, limitations, teaching note |

### 8.5 Independent review and release

| ID | Task | Dependencies | Exit evidence |
|---|---|---|---|
| CFI-901 | Clean-room reproduction | Any paper bundle | Environment reconstruction, checksums, discrepancies |
| CFI-902 | Statistical and adversarial claim audit | CFI-901 | Leakage, multiplicity, robustness, alternative-explanation report |
| CFI-903 | Public release and correction package | CFI-902, G6 | Versioned bundle, citation metadata, correction path, maturity label |

## 9. Metrics to preregister, not retrofit

Final estimands and thresholds belong to each frozen protocol. The following
families must be considered before pilots become confirmatory evidence.

### Shared bridge

- held-out likelihood or predictive score;
- calibration of reported probabilities;
- parameter recovery on simulated ground truth;
- posterior predictive checks;
- stability across sequence length, evidence order, and subject/model class;
- comparison against simpler interpretable baselines.

### Paper I

- decision utility under explicit error and compute costs;
- regret relative to oracle and fixed-budget policies;
- accuracy/calibration at stopping;
- premature-stop and overthinking rates;
- compute, latency, tool calls, and failure rate.

### Paper II

- paired price and implied-volatility difference;
- no-arbitrage violation rate and exploitable portfolio value;
- put-call, monotonicity, replication, and stochastic-dominance violations;
- coherence-repair distance;
- calibration before and after repair;
- frame-by-subject/model interactions with uncertainty intervals.

### Paper III

- Brier/log score and calibration;
- aggregation gain over individual and simple-crowd baselines;
- error correlation and effective diversity;
- herding, minority-information retention, and recovery after false evidence;
- mechanism cost, bounded loss, wealth concentration, and strategic sensitivity.

Aggregate scores never hide critical mathematical invalidity, data-rights
failure, or leakage. Multiple comparisons and exploratory analyses are labeled
and corrected according to the frozen plan.

## 10. Data, ethics, security, and rights gates

Candidate human datasets remain ineligible until CFI-003 records:

- canonical source and persistent identifier;
- participant and collection context;
- license or terms snapshot and retrieval date;
- allowed research, ML evaluation, derivative, and redistribution uses;
- sensitive attributes and re-identification risk;
- acquisition and transformation method;
- whether new ethics/IRB consultation is required;
- required attribution and citation;
- release plan or lawful reconstruction instructions.

Public availability is not permission to train or evaluate models. Terms that
require written permission remain blocking until permission is documented.
Agents do not scrape around access controls or substitute a secondary mirror
for the canonical rights record.

All human identifiers are pseudonymous or removed. No employer, customer,
private correspondence, personal finance, credential, or donated trace enters
the program. Synthetic data records its generator, configuration, seed,
filters, and review class.

## 11. Reproducibility and open artifact contract

Proposed implementation layout:

```text
research/cfi/
  registry/
  shared/
    schemas/
    simulators/
    estimators/
    visualization/
  paper-01-option-value-of-thinking/
  paper-02-language-arbitrage/
  paper-03-market-of-minds/
  reports/
```

An implementation agent may create this layout in a focused issue after CFI-004
is approved. Each experiment records:

- code commit and dirty-state assertion;
- environment and lockfile;
- dataset/source manifest and rights state;
- model/provider revision and prompt/template digest;
- configuration, seed, hardware, wall time, and cost;
- raw immutable outputs and derived-table lineage;
- predefined analysis version;
- failures, exclusions, and deviations;
- reproduction command and checksum report.

Public bundles target RR-1 during methods development, RR-2 for working papers,
and independent replication before any RR-4 claim. No badge is typed manually;
evidence must generate it.

## 12. Schedule and evidence milestones

### First 30 days — visible foundation, no result claim

Complete CFI-002 through CFI-007 far enough to publish locally:

- dated literature/novelty matrix;
- candidate-data rights and ethics matrix;
- observable belief-event schema proposal;
- synthetic Bayesian/diffusion baseline with recovery tests;
- preregistration and statistical-review template;
- accessible belief-trajectory viewer using synthetic fixtures;
- methods-note landing material labeled `proposal` or `prototype`.

### Months 2–4 — first paper-sized pilot

Prioritize Paper II because deterministic payoff equivalence and pricing
invariants support fast falsifiable progress. Complete CFI-201 through CFI-205.
Release a pilot report whether the effect is positive, null, mixed, or invalid.

### Months 3–7 — redesigned active-information-acquisition study

Return Paper I to G1 scoping around costly active information acquisition over
a calibrated belief state. Do not execute the original learned-stopping
hypothesis. After the redesigned question passes its own novelty review,
complete a revised CFI-101 through CFI-106 sequence. The discrete model is
required; continuous time is optional.

### Months 6–12 — market study and integrated program

Return Paper III to G1 scoping around identifiable coupled stochastic belief
dynamics or a registered replication. Complete a revised CFI-301 through
CFI-306 only after the new question passes review and the shared bridge is
stable. End the academic year with independent reproduction attempts and a
portfolio synthesis explaining what survived contact with evidence.

## 13. Cost and compute posture

The planning stage authorizes no cloud spend, external API use, model download,
or data acquisition. Experiments begin with deterministic simulators and the
smallest adequate local/open-weight model set. Every run plan declares a hard
time, token, API, storage, and cloud-cost budget. Crossing an approved budget or
adding a paid provider requires a Director decision and cost record.

## 14. First next-agent packet after RES-020

The next research agent should execute an **independent G1 review of CFI-002**
and draft two bounded re-scoping packets. It must not begin an experiment.

**Objective:** Independently verify the collision matrix; test the narrowed
Paper II flagship novelty sentence; and search nearest neighbors for Paper I's
active-information-acquisition redesign and Paper III's identifiable coupled-
dynamics or registered-replication route.

**Read order:**

1. `LABORATORY_BIBLE.md` sections 3, 9, 10, 17, 18, 20, and 23;
2. `DIRECTORS_MEMO.md` RES-016, RES-017, and RES-020;
3. this document;
4. `RESEARCH_ETHICS_AND_INTEGRITY.md`;
5. `OPEN_RESEARCH_PUBLICATION_AND_REPLICATION.md`;
6. `docs/references/TECHNICAL_REFERENCE_REGISTER.md`;
7. `agents/15_RESEARCH_COMMUNITY.md`;
8. latest accepted handoff and `WORKLOG.md`.

**Owned output:** an independent G1 review record, a narrowed Paper II claim
packet, and separate Paper I/Paper III nearest-neighbor scoping notes, plus
updates to the technical reference register for volatile assumptions.

**Acceptance evidence:** reviewer identity or agent boundary, source-by-source
confirmation or correction, search protocol, primary sources, closest competing
work for each redesign, unresolved risks, revalidation dates, and explicit
pass/revise/stop recommendations.

**Stop conditions:** paywalled evidence with no inspectable primary source;
unclear dataset/model license; a competing paper that substantially collapses a
proposed contribution; any need to change a primary research question. Record
the issue and request direction rather than reframing silently.

## 15. Success criteria for the program

The academic year succeeds if it produces:

- one coherent mathematical and software spine used by all papers;
- at least one paper-quality result or well-formed negative result;
- three honest working-paper tracks with distinct contributions and no sliced
  duplication;
- public code, methods, manifests, and teaching artifacts sufficient for an
  informed reader to inspect and rerun eligible results;
- a portfolio experience that shows questions, methods, experiments, failures,
  and next work without overstating maturity;
- a reusable model of bounded agent contribution in which human agency,
  authorship, and research accountability remain explicit.

Success is not three acceptances, a positive result, or a flashy dashboard. It
is a credible body of work that demonstrates mathematical taste, experimental
discipline, engineering ability, and intellectual honesty.
