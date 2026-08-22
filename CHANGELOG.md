---
document_id: DRL-ROOT-CHANGELOG
title: "Foundation Changelog"
version: 4.14.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-19
---

# Foundation Changelog

## 2026-08-19 — Resolution diagnostic and the research/cfi ratification

- Recorded **RES-023**, ratifying the `research/cfi` package created ahead of the
  CFI-004 layout gate. Scoped to layout only: CFI-004 still governs the
  belief-event schema work, and G2 and G3 are untouched.
- The bake-off harness now reports a **paired resolution diagnostic** with each
  decision — the tasks required to detect a `min_margin`-sized difference at
  alpha 0.05 and power 0.80, against the suite's Kish-effective task count. It is
  reported and never gating.
- It is not a gate for two stated reasons. The variance cannot be estimated from
  fixture runs, where every scripted provider shares one script and the paired
  differences are identically zero; the diagnostic reports that rather than
  inventing a number. And gating at the current `min_margin` would need roughly
  70 to 500 tasks depending on real variance, against a suite of 12 — a
  suite-expansion decision, not a threshold edit. `min_margin` stays at 0.05.
- This adopts, in diagnostic form, the recommendation in DRL-RES-008 §5 drawn
  from *Resolution Diagnostics for Paired LLM Evaluation* (arXiv:2605.30315).

## 2026-08-19 — Paper II instrument, CFI-003 opening record, TR-2026-002 novelty scan

- Added `research/cfi` (`drl-cfi`), the machine-side instrument for the Paper II
  track: piecewise-linear payoff primitives with an exact equivalence oracle, a
  Black-Scholes normative oracle with replication invariants, frame pairs that
  cannot vary the payoff they describe, and arbitrage detection with minimal
  coherence repair. Pure Python — no NumPy or SciPy dependency is added.
  63 tests; strict mypy clean.
- Coherence detection, repair, repair distance, and the exploiting portfolio all
  derive from one projection onto the closed cone `{A q : q >= 0}`, implemented
  as Lawson-Hanson NNLS over a Householder QR least-squares core. Two bounds are
  documented rather than hidden: a weak arbitrage on the cone boundary reports as
  coherent, and non-negativity is certified only across the spanned state grid.
- Recorded the opening CFI-003 candidate-data rights register (DRL-RES-007). Two
  CPC18 records verified as CC BY 4.0; choices13k carries **no stated licence**
  and is marked `BLOCKED_RIGHTS`. No dataset was downloaded and G2 stays closed.
- The register's material finding is construct validity, not licensing: all three
  candidates record numeric gamble choices with no payoff-preserving linguistic
  frame and no elicited valuation, so the cleanly licensed ones are still
  probably unfit for Paper II's human baseline.
- Recorded a preliminary novelty scan for TR-2026-002 (DRL-RES-008), which had
  never had one. Seven records examined, four verified. The leaderboard critique
  is established background, and executable refusing gates already exist in
  release management and self-improving runtimes, so the report is repositioned:
  what may remain differentiable is selection-among-candidates combined with
  non-performance admissibility conditions. The null result is untouched.
- TR-2026-002 gains a related-work section carrying those findings and a pointer
  to a better form for its weakest condition: a power-based resolution ratio in
  place of the asserted `min_margin: 0.05`.

## 2026-08-19 — DIR-009 accepted; TR-2026-002 verification pass

- Recorded **RES-022**, resolving DIR-009 as Option B against the recommendation
  in that row: the historical institutional author address in Git metadata is
  accepted rather than rewritten, commit SHAs are preserved, and new commits
  continue to use the GitHub no-reply address. Public visibility is no longer
  gated on it; the RES-018 date gate still applies.
- `validate_public_repository.py --release` now reports the affected commits as
  `ACCEPTED (RES-022)` and passes instead of failing. The check is retained, so a
  new unapproved institutional address would still surface.
- Corrected the commit count across the readiness documents: it is ref-dependent
  and drifts as branches merge, so the audit reports a measured count rather than
  the fixed "sixteen" recorded when DIR-009 was raised (15 reachable today).
- Verified TR-2026-002 against a live harness run and corrected three
  inaccuracies: a stale test count (37 → 55), an under-reported `edge` result
  that named two of six blockers, and an abstract implying six blockers in total
  rather than six per role.
- Recorded a third harness defect in TR-2026-002 §8 (v1.2.0): the `edge` role has
  only 7 eligible tasks against a `min_tasks` floor of 8, so it cannot satisfy its
  own coverage condition under any measurement mode. The suite is short, not the
  gate; the fix is to extend the `edge` tasks rather than lower the threshold.
- Added TR-2026-002 to the working-paper register in `PUBLICATION_PIPELINE.md`,
  which previously listed only TR-2026-001, and required every report under
  `docs/10-research/reports/` to appear there whatever its status.

## 2026-08-17 — Public repository source curation

- Reframed the root README as an evidence-first personal academic research
  portfolio with explicit prototype, specified, and planned boundaries.
- Added canonical citation and package metadata plus a fail-closed tracked-source
  audit for credentials, employer identifiers, private paths, binary artifacts,
  unsupported maturity claims, and unapproved public contact addresses.
- Moved the generated source manifest out of Git and into a CI artifact, archived
  stale validation snapshots, and corrected placeholder UI/model packages that
  were inaccurately labeled release candidates.
- Updated GitHub Actions to current Node 24 action generations and made the
  placeholder Node workspace status explicit in CI.
- Recorded DIR-009: public visibility remains blocked until the Director chooses
  a coordinated history rewrite or explicit acceptance of institutional
  author-address exposure. RES-018 continues to keep the repository private
  through 2026-09-30.

## 2026-08-05 — Computational Finance of Intelligence research program

- Recorded RES-017 and DRL-031 for a three-paper academic research program
  spanning optimal stopping, no-arbitrage belief repair, and market-based
  human/machine aggregation.
- Made Belief Diffusion the shared methods bridge rather than a required fourth
  paper.
- Added a sequential agent task graph with explicit novelty, data/ethics,
  protocol, confirmatory-analysis, claim, and publication gates.
- Defined a 30-day visible-foundation tranche that authorizes planning and
  synthetic methods artifacts, not data acquisition, model experiments, cloud
  spend, or empirical claims.

## 2026-08-04 — Personal academic portfolio correction

- Recorded RES-016, superseding the workshop-first public-site positioning from
  RES-015. `www.dewitt-labs.com` is Christopher Noxon DeWitt's personal academic
  portfolio.
- Centered the current Master of Applied Data Science program at the University
  of North Carolina at Chapel Hill, professional interest in complex systems,
  and intended progression toward graduate work in computer science.
- Reduced the Wix contract to Home, Research, Projects, and About. Reports,
  recorded runs, software, and Atticus are selected portfolio evidence.
- Replaced the previous positioning guard with tests for the personal identity,
  education, action order, university-claim boundary, and planned Atticus state.

## 2026-08-04 — Evidence-first academic website contract (superseded by RES-016)

- Recorded RES-015 and aligned the controlled public-site contract around the
  research thesis **Engineering complex systems for open, inspectable
  intelligence.**
- Made **Watch a recorded run** and **Read TR-2026-001** the first website
  actions; required the signed degraded replay and Stage-B no-winner evidence to
  remain visible.
- Reframed Atticus as a documented research artifact with a planned application
  address, placed teaching under Writing/Methods, and kept contributor routes
  secondary to academic evidence and serious inquiry.
- Reconciled the five-page Wix blueprint, product/persona documents,
  application-shell contracts, DRL-021 traceability, and UTF-8-safe validation.
- Added `tests/docs/test_website_positioning.py` to guard the thesis, action
  order, negative-results visibility, planned Atticus state, and contributor
  posture.

## 2026-08-02 — Canonical domain correction, live site, and founder identity

- Corrected the canonical domain spelling from `dwit-labs.com` to
  `dewitt-labs.com` across all documentation, configuration, schemas, scripts,
  and tests (RES-011). The public Wix site is live at
  `https://www.dewitt-labs.com`.
- Recorded the founder's full name as Christopher Noxon DeWitt in
  founder-identity lines, controlled-document ownership, and copyright; other
  operational references now use "the Director" (RES-012).

## 2026-08-01 — Contributor routes and good-first issues

- DRL-029: published contributor route map, five GFI seeds, Good first issue
  template, and CONTRIBUTING entry path.

## 2026-08-01 — First technical report (TR-2026-001)

- DRL-028: published prototype technical report for the local integrated
  evidence-to-scenario workflow with methods, rights, limitations, and
  reproduction commands.

## 2026-08-01 — Integrated workflow teaching lab

- DRL-020: published `docs/10-research/teaching/INTEGRATED_WORKFLOW_LAB.md` with
  exercises, instructor notes, and no private-data requirements.
- Linked from contributor first-hour path; guarded by `tests/docs/test_teaching_lab.py`.

## 2026-08-01 — Signed success and degraded replays

- DRL-019: EvalForge packages success and degraded Atticus runs as signed
  replay manifests with on-disk artifact digest verification
  (`services/evalforge/fixtures/signed_replays/`).
- Fixture HMAC key is demo-only (`drl-fixture-replay-v1`); production signing
  identity remains a later gate.

## 2026-07-30 — M3 specialists and linked integrated workflow

- DRL-014–017: Atlas public adapter, FedLens bounded corpus + passage citations,
  and BalanceLab scenario catalog landed on `main` (PRs #16–#18, #20).
- DRL-018: Atticus local runtime composes those specialists and emits one
  `linked_workflow` artifact binding Atlas, FedLens, BalanceLab, report, and
  evaluation digests (`tests/integration/test_evidence_to_scenario_trace.py`).
- Documentation: integrated demo maturity table, traceability for DRL-SYS-008,
  Director's Memo implementation truth, and issue-register evidence updated.
- Model bake-off winner remains DIR-004 (scaffold only).

## 2026-07-28 — First implementation missions merged

- Repaired Mission 00/01 CI (duplicate pnpm version configuration) and added
  portable bootstrap with Linux clean-clone evidence (PR #6, #7).
- DRL-005: added `drl_protocol.state_machine` legal/terminal transition helpers
  and orchestrator cancellation checks (PR #8).
- DRL-007: added typed open-weight `ModelProvider` interface, deterministic
  mock provider, and disclosed `ModelGateway` with open-weight enforcement
  (PR #9).
- DRL-008: added `StructuredOutputValidator` with JSON Schema 2020-12
  validation, bounded fail-closed repair, and injection-resistant trace events
  (PR #10).
- DRL-011: added held-out EvalForge permission/trajectory suite with separate
  terminal and trajectory scores and release-gating decisions (PR #11).
- DRL-009: hardened local-runner `SandboxedWorkspace` with redacted
  inspection, traversal/symlink denial, and size/binary limits (PR #12).
- Replaced the hardcoded foundation date ceiling in `validate_foundation.py`
  with a dynamic today-based check plus one day of clock skew tolerance.

## 2026-07-26 — Open-source identity iteration

- Established the Open Research and Open Technology Charter.
- Added open artifact, model commons, open stack/upstream, reproducibility badge, community, maturity, forkability, and upstream contribution standards.
- Made the Atticus Open Model Commons and Open Source portal explicit V1 release surfaces.
- Added current open-model and runtime candidate/reference registers.
- Expanded V1 requirements and sequential work packages for open identity, clean-room self-hosting, upstream stewardship, and precise terminology.
- Added OpenTofu-versus-Terraform as a documented director/ADR decision gate because open-source status differs.

All notable changes to the DRL program foundation are recorded here. Product/runtime changelogs will follow semantic versions after implementation begins.

## Unreleased

### Added

- Deep V1 Laboratory Bible and controlled specification map.
- Component-level specifications for Atticus, local runner, website, Atlas, FedLens, BalanceLab AI, EvalForge, Core, and Edge.
- Machine-readable DRL protocol schemas, environment/policy configurations, project API/data/security/evaluation/demo/roadmap documents.
- Sixteen sequential agent missions with work packages, ownership, gates, verification, and handoffs.
- Google-first cloud, model-training, security, privacy, open-source, research, brand, and release programs.
- Validation, traceability, source register, mixed-license, trademark, and commercial sustainability policies.

### Changed

- Replaced shallow/duplicate agent briefs and placeholder root policies with executable specifications and governance.
- Strengthened V1 definition from a portfolio shell to a coordinated, reproducible open research platform release.

### Removed

- Obsolete duplicate mission files that could cause agent ambiguity.

## 0.0.0 — Foundation seed

Initial documentation-first monorepo skeleton. Not a product release.

## 3.2.0 — Open-source identity deepening

- Made open models, open-source software, self-hosting, reproducibility, upstream reciprocity, and community credit explicit institutional identity pillars.
- Added Open Technology Catalog, Atticus Open Model Commons release train, sustainability boundaries, health metrics, contributor authorship, open-source visual identity, and V1 showcase specifications.
- Added three machine-readable open artifact/upstream/exception schemas and controlled configuration registries.
- Added a dedicated open-identity validator and release gate.
- Added director decision proposals for OpenTofu and Valkey rather than silently replacing approved tools.


## 2026-07-26 — Registered domain and Wix institutional site integration

- Recorded `https://www.dewitt-labs.com` as the canonical public laboratory address.
- Approved Wix as the V1 institutional/editorial website while preserving independently deployable open-source applications.
- Added domain, DNS, TLS, Wix, subdomain, consent, SEO, and cross-host operating contracts.
- Added ADR-0008, platform runbook, domain-routing configuration, release requirements, and agent work packages.
