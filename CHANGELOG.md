---
document_id: DRL-ROOT-CHANGELOG
title: "Foundation Changelog"
version: 4.10.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-05
---

# Foundation Changelog

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
