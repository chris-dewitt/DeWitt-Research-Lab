---
document_id: DRL-ROOT-CHANGELOG
title: "Foundation Changelog"
version: 4.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-29
---

# Foundation Changelog

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

- Recorded `https://www.dwit-labs.com` as the canonical public laboratory address.
- Approved Wix as the V1 institutional/editorial website while preserving independently deployable open-source applications.
- Added domain, DNS, TLS, Wix, subdomain, consent, SEO, and cross-host operating contracts.
- Added ADR-0008, platform runbook, domain-routing configuration, release requirements, and agent work packages.
