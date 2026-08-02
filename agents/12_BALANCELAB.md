---
document_id: DRL-AGT-012
title: "Agent Mission 12: BalanceLab AI Deterministic Scenario Laboratory"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Agent Mission 12: BalanceLab AI Deterministic Scenario Laboratory

## Mission objective

Implement BalanceLab AI as a transparent educational and research-grade synthetic balance-sheet scenario engine in which deterministic calculations are authoritative and AI provides bounded explanation, navigation, and documentation.


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

- Missions 00–07 merged.
- Project specification, DRL protocol, security policy, platform contracts, and EvalForge interfaces stable.
- Approved data/source or synthetic-data rules available.

## Owned paths

- `services/balancelab-ai/**`
- corresponding project documentation and fixtures
- project-specific public tools, SDK adapters, demos, and evaluations

## Protected or coordinated paths

- Cross-service protocol changes require Architecture/Protocol coordination.
- Public data and content must pass rights/provenance review.
- Model-generated claims cannot bypass evidence, deterministic artifacts, or uncertainty requirements.
- No project may create direct public external-write authority.

## Required work packages

### WP-12-01 — Domain model and synthetic institutions
Implement versioned product/balance/cash-flow/assumption/scenario schemas, accounting identities, synthetic institution generator, validation, and employer-separation review.

### WP-12-02 — Deterministic scenario engine
Implement approved yield-curve shocks, repricing, deposit betas/decay/runoff, balance projections, NII, duration/sensitivity, decomposition, rounding, units, and reproducible calculation artifacts.

### WP-12-03 — Explainability and audit
Expose formulas, inputs, versions, intermediate results, invariants, provenance, uncertainty, and a calculation audit; ensure LLM explanation consumes artifacts rather than inventing results.

### WP-12-04 — Atticus tool interface and public workstation
Implement validate/run/compare/explain tools, synthetic sample bank, interactive scenario controls, accessibility, and curated reference scenarios.

### WP-12-05 — Verification and model risk discipline
Add golden cases, independent calculation checks, property/metamorphic tests, edge cases, numerical tolerances, performance tests, and methodology documentation.

### WP-12-06 — Educational publication and safety
Publish tutorials, limitations, synthetic-data disclaimer, non-advice disclosure, methodology paper, and release evidence.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- New data/source license or redistribution assumptions.
- Changes to public schemas or specialist authority.
- Any claim of real-time coverage, causality, financial advice, or production-bank equivalence.
- Material cloud cost or retention changes.

## Verification matrix

- All numerical outputs derive from deterministic versioned code and pass golden/invariant/property tests.
- Units, signs, dates, rounding, and assumptions are explicit.
- AI explanations cannot alter calculations and are checked for contradiction with artifacts.
- No employer-confidential data, methods, naming, or samples appear.
- Public demo uses synthetic institutions only and is clearly educational/research oriented.
- Integrated macro/Fed/scenario workflow passes EvalForge gates.

## Handoff requirements

Provide stable API/schema version, fixture/local-mode commands, data/source manifests, evaluation and security report, performance/cost baseline, demo/replay, known limitations, publication artifacts, and exact Atticus integration examples.

## Definition of mission complete

The specialist service is independently useful, locally reproducible, publicly demonstrable, fully integrated through DRL protocol, provenance/evaluation/security complete, and meets its project-specific V1 acceptance gates.
