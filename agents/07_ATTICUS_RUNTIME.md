---
document_id: DRL-AGT-007
title: "Agent Mission 07: Atticus Control Plane and Orchestration Runtime"
version: 3.0.0
status: APPROVED EXECUTION MISSION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Agent Mission 07: Atticus Control Plane and Orchestration Runtime

## Mission objective

Implement Atticus as the open-weight operating intelligence of DRL: intent resolution, skill selection, planning, model routing, policy mediation, specialist invocation, evidence-aware synthesis, trace creation, and human approval—without allowing the model to bypass deterministic policy or trust boundaries.


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

- Missions 00–05 merged.
- DRL protocol schemas, risk tiers, identity model, policy contract, EvalForge SDK, and environment contracts stable.
- At least one approved open-weight baseline model endpoint or deterministic mock is available.

## Owned paths

- `services/atticus-control-plane/**`
- orchestration portions of `packages/drl-ai-core/**` and `packages/atticus-sdk/**`
- runtime skills and public-safe tool registry
- runtime integration tests and trace fixtures

## Protected or coordinated paths

- Specialist internals remain owned by their missions.
- Policy decisions are deterministic and external to model prose.
- No public external write tool, unrestricted shell, arbitrary URL fetch, or hidden fallback to closed models.
- Protocol schema changes require Architecture/Protocol coordination and ADR when incompatible.

## Required work packages

### WP-07-01 — Request/session lifecycle
Implement authenticated and anonymous session envelopes, idempotency, deadlines, correlation, cancellation, quotas, and explicit consent snapshots.

### WP-07-02 — Skill registry and planner
Implement versioned skill manifests, capability discovery, deterministic eligibility filters, bounded planning graph, cycle/step limits, and a plan artifact suitable for evaluation without exposing private chain-of-thought.

### WP-07-03 — Model gateway and open-weight routing
Implement Core/Edge routing, health/capability metadata, structured output validation, timeouts, retry budgets, fallback policy, and disclosure of the model path used.

### WP-07-04 — Policy, approval, and tool execution
Integrate risk tiers, permission evaluation, signed approval grants, argument constraints, replay protection, tool result validation, and immutable trace events. The model proposes; policy decides.

### WP-07-05 — Specialist orchestration and synthesis
Integrate Atlas, FedLens, BalanceLab, and EvalForge through typed clients. Preserve provenance and calculations through synthesis; fail closed on missing required evidence or policy denial.

### WP-07-06 — Recovery, observability, and public sandbox
Implement partial failure handling, compensating behavior, no-op-safe retries, user-visible status, structured telemetry, sandbox fixtures, abuse controls, and replayable reference workflows.

Every work package must name the requirements it satisfies, the evidence it produces, and its failure/rollback behavior. Create focused commits at work-package boundaries.

## ADR and director-approval triggers

- Any new authority class, approval bypass, hidden data persistence, closed-model production dependency, dynamic code execution, or cross-tenant memory.
- Any unbounded agent loop or model-generated policy rule.
- Any change in whether private content leaves a device.
- Any public tool that can mutate an external system.

## Verification matrix

- Contract tests pass against all protocol examples.
- Unit/property/integration tests cover state transitions, retries, idempotency, approval binding, denial, expiry, and cancellation.
- Security suite records zero unauthorized actions.
- EvalForge measures route/tool/argument/trajectory/grounding outcomes.
- Public sandbox survives malformed output, tool failure, specialist timeout, and prompt injection without violating policy.
- Trace contains sufficient evidence to reproduce each external action and final claim.

## Handoff requirements

Provide versioned runtime API, skill catalog, state transition table, model routing matrix, policy integration contract, trace samples, performance/cost baseline, evaluation report, known failure modes, and specialist integration checklist.

## Definition of mission complete

Atticus can execute the integrated reference workflow end-to-end using open weights and mocks/live specialists as appropriate, with bounded autonomy, auditable traces, explicit approvals, robust recovery, and release-threshold evaluation results.
