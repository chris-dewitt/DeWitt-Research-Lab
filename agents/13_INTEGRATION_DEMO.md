---
document_id: DRL-AGT-013
title: "Agent Mission 13: Cross-System Integration and Reference Demonstration"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Agent Mission 13: Cross-System Integration and Reference Demonstration

## Mission objective

Integrate the laboratory into one truthful platform and deliver the signature end-to-end workflow in which Atticus gathers Atlas and FedLens evidence, constructs a documented synthetic scenario, invokes BalanceLab, sends the trace to EvalForge, and produces a cited report and replay.


## Operating contract

This mission is executed on a dedicated feature branch and ends in a reviewable pull request. Before changing files, the agent must read `LABORATORY_BIBLE.md`, root `AGENTS.md`, `docs/00-program/SPECIFICATION_MAP.md`, `docs/00-program/DECISION_REGISTER.md`, the current `WORKLOG.md`, this mission, and every listed prerequisite.

The agent must not silently reinterpret the laboratory. Missing or contradictory decisions become a documented blocker or an ADR proposal. All external factual or technical assumptions that could have changed must be revalidated against authoritative primary documentation and entered in the technical reference register.

## Branch, commit, and pull-request protocol

- Create a branch named `agent/<mission-number>-<short-scope>` from the latest approved integration branch.
- Reserve the mission in `WORKLOG.md` before modifying controlled files.
- Commit after coherent work packages; avoid one giant undifferentiated commit.
- Rebase or merge the latest integration branch before final verification.
- Open a pull request containing requirement IDs, changed contracts, ADRs, test evidence, security/privacy impact, documentation impact, known limitations, and exact handoff state.
- Never merge the pull request yourself unless the Director has explicitly delegated that authority for the specific PR.

## Universal constraints

- No credentials, personal/private content, employer material, unlicensed corpora, or generated secrets may be committed.
- Do not weaken security, privacy, evaluation, accessibility, open-weight, provenance, or deterministic-computation requirements to make a demo pass.
- Do not claim completion without verifiable evidence.
- Do not alter another component's public contract without coordination and, when material, an approved ADR.
- Public write actions and unrestricted shell execution remain outside the public Atticus trust boundary.
- LLM output never becomes an authoritative numerical financial result; BalanceLab calculations must be deterministic and auditable.

## Required artifacts in every mission PR

1. Implemented or revised artifacts owned by the mission.
2. Automated tests or executable validation for every material behavior.
3. Updated controlled documentation and requirement traceability.
4. A completed handoff ledger entry using `agents/HANDOFF_TEMPLATE.md`.
5. A list of decisions made, assumptions retained, unresolved blockers, and follow-on issues.
6. Evidence that relevant local and CI commands pass.

## Stop conditions

Stop rather than improvise when a change would expose private data, expand write authority, change a public protocol, add a new upstream model/license, materially change cloud cost, undermine reproducibility, or contradict an approved foundation decision. Draft an ADR or blocker with alternatives and impact.


## Entry prerequisites

- Missions 00–12 merged or their integration-ready release candidates approved.
- Dev/staging environments operational.
- Protocol and public demo contracts frozen for the release candidate.

## Owned paths

- cross-service integration tests and fixtures
- reference demo orchestration and replay manifests
- staging deployment composition
- `docs/01-product/INTEGRATED_REFERENCE_DEMO.md`
- integration-specific release evidence

## Protected or coordinated paths

- Component internals stay with owners; fixes are returned through focused PRs where possible.
- Do not hide failed live integration behind an unlabeled recording.
- Do not relax release thresholds to obtain a successful demo.
- Any protocol incompatibility returns to Architecture/Protocol rather than being patched with undocumented translation.

## Required work packages

### WP-13-01 — Contract compatibility and environment matrix
Pin compatible service/model/schema versions; implement consumer-driven contract tests; define live/mock/replay environment matrix and seed fixtures.

### WP-13-02 — Integrated workflow implementation
Implement the canonical request, bounded plan, evidence acquisition, scenario derivation, deterministic calculation, evaluation, report synthesis, cancellation, and partial failure behavior.

### WP-13-03 — Trace, evidence, and replay
Ensure every claim, calculation, tool event, policy decision, model route, and evaluation result is linked; create signed replay artifact and reproducibility package.

### WP-13-04 — Failure and degradation drills
Exercise model cold start, source outage, invalid evidence, policy denial, specialist timeout, queue duplication, stale schema, budget limit, and local-runner disconnect.

### WP-13-05 — User experience and narrative
Coordinate the guided tour, public workstation, failure museum entry, technical walkthrough, and role-specific paths without overstating automation or research conclusions.

### WP-13-06 — Staging endurance and release evidence
Run load/endurance/cost/security/evaluation suites in staging, collect SLOs, and create integration release dossier.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- Any last-minute public contract change.
- Any use of unapproved data/model/artifact to make the demo succeed.
- Any waiver of security/evaluation/claim-evidence gates.
- Any production data or cost exposure outside approved envelopes.

## Verification matrix

- Consumer-driven contracts pass across pinned versions.
- Integrated workflow succeeds above release threshold and fails safely in all required drills.
- Replay reproduces user-visible output or declared tolerances from immutable artifacts.
- Every claim/calculation is traceable.
- End-to-end latency/cost/SLOs are reported by stage.
- Accessibility, consent, security, and anonymous quota paths pass in staging.

## Handoff requirements

Provide compatibility matrix, integration fixtures, staging URLs/config references, signed replay, failure-drill report, SLO/cost report, integrated EvalForge report, release blockers, and exact promotion instructions.

## Definition of mission complete

The complete DRL vertical slice works as one platform in staging, can be reproduced and evaluated, degrades truthfully, and has no hidden cross-system contract or security exceptions.

### WP-13-07 — Signature open-source showcase

Build and validate the end-to-end public workflow described in `docs/09-open-source/V1_OPEN_SOURCE_SHOWCASE.md`, including reproduction bundle, local open-weight route, live/replay labeling, model identity, traces, evaluation, failure example, and contribution links.
