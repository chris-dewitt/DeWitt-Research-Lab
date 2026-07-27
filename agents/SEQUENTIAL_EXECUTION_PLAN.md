---
document_id: DRL-AGT-901
title: "Sequential Agent Execution Plan"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Sequential Agent Execution Plan

## Purpose

DRL agents run sequentially, but sequential execution does not eliminate integration risk. This plan defines the authoritative order, entry gates, expected branches, handoff controls, and permitted return loops.

## Critical path

```mermaid
flowchart LR
  A00[00 Program] --> A01[01 Document Control]
  A01 --> A02[02 Architecture/Protocol]
  A02 --> A03[03 Security/Policy]
  A02 --> A04[04 EvalForge]
  A03 --> A05[05 GCP Platform]
  A04 --> A07[07 Atticus Runtime]
  A05 --> A06[06 Brand/Web]
  A03 --> A07
  A04 --> A08[08 Model/Data]
  A05 --> A08
  A07 --> A09[09 Local Runner]
  A08 --> A09
  A07 --> A10[10 Atlas]
  A07 --> A11[11 FedLens]
  A07 --> A12[12 BalanceLab]
  A06 --> A13[13 Integration]
  A09 --> A13
  A10 --> A13
  A11 --> A13
  A12 --> A13
  A13 --> A14[14 Release QA]
  A14 --> A15[15 Research/Community]
```

Where the diagram shows parallel-ready dependencies, the human operator may still run agents sequentially in any topologically valid order. The default recommended order is numeric.

## Gate before every mission

1. Previous PR merged or explicitly marked integration-ready.
2. `WORKLOG.md` contains a complete handoff.
3. Foundation validation passes on the inherited commit.
4. No unresolved blocker affects the mission’s owned contracts.
5. Required ADRs are approved.
6. Agent reserves the mission and branch in the worklog.

## Return loops

A later agent may discover an upstream defect. It must create a focused issue and either:

- fix it in a narrowly scoped coordinated PR if ownership permits and contracts do not change; or
- return it to the owning mission with a failing test and reproduction; or
- propose an ADR if the correction changes architecture or public behavior.

No compatibility shim may become permanent without documentation, tests, ownership, and a removal or support policy.

## Integration branch policy

- `main` contains only director-approved stable foundations/releases.
- `integration/v1` receives approved mission PRs and is the baseline for sequential work.
- Feature branches are cut from the latest `integration/v1`.
- Release candidates use `release/v1.0.0-rcN` and accept only reviewed defect/documentation fixes.

## Agent tool neutrality

Codex, Claude Code, Cursor, Copilot, and Gemini may all execute missions. The repository instructions, not a tool’s hidden defaults, govern behavior. Any tool-specific generated metadata must remain optional and must not become the only source of project state.

## Human checkpoints

DeWitt must review at minimum:

- base-model selection;
- public identity/brand constitution;
- security permission expansion;
- cloud cost hard-cap or topology changes;
- mixed-license decisions and model/data releases;
- V1 scope changes;
- release-gate waivers;
- production promotion and public launch.

## Open-source identity thread

Open-source identity is a cross-mission dependency rather than a final communications task. Mission 02 owns contracts; Mission 05 owns open infrastructure decision evidence; Mission 06 owns public identity surfaces; Mission 08 owns the Atticus Open Model Commons; Mission 13 owns the signature demonstration; Mission 14 independently verifies every claim; Mission 15 owns community, credit, replication, and accountability. Each handoff links the applicable DRL-OSS requirements and release evidence.
