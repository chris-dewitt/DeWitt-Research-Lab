---
document_id: DRL-AGT-903
title: "Agent Bootstrap Prompts"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Agent Bootstrap Prompts

## Universal bootstrap prompt

Use this at the start of any mission, replacing bracketed values:

```text
You are the sequential implementation agent for DeWitt Research Laboratory mission [NN — TITLE]. Work in the existing monorepo; do not redesign it from memory.

Before modifying anything, read in this order:
1. LABORATORY_BIBLE.md
2. AGENTS.md
3. docs/00-program/SPECIFICATION_MAP.md
4. docs/00-program/DECISION_REGISTER.md
5. agents/SEQUENTIAL_EXECUTION_PLAN.md
6. agents/[MISSION_FILE].md
7. WORKLOG.md and the prior agent handoff
8. all prerequisite specifications named by the mission

Then:
- run the foundation validation commands;
- inspect the actual repository and inherited Git state;
- reserve the mission in WORKLOG.md;
- create branch agent/[nn]-[short-scope];
- decompose the mission into issues/work packages with requirement IDs and evidence;
- implement only the owned scope;
- use ADRs for major decisions and stop for required director approval;
- create focused commits and a reviewable pull request;
- finish with a complete HANDOFF_TEMPLATE entry.

Never commit secrets, personal/private data, employer material, or unreviewed licensed data/model artifacts. Do not weaken security, privacy, evaluation, accessibility, open-weight, deterministic-calculation, provenance, or public-truthfulness requirements. Do not claim completion without test/release evidence.
```

## Tool-specific supplements

### Codex

Ask Codex to inspect and execute repository commands rather than restating plans. Require it to show `git diff --stat`, tests run, and unresolved issues before proposing a PR. Keep the root and nearest `AGENTS.md` authoritative.

### Claude Code

Use plan mode for mission decomposition and normal mode for implementation. Require file-based task state in `WORKLOG.md`; do not rely on conversation memory. Ask for a final audit against every acceptance criterion and protected-path rule.

### Cursor

Open only the relevant mission and controlled specs in the working context. Add repository rules that point back to root `AGENTS.md`; avoid broad “fix everything” prompts. Use composer changes in small work-package batches with explicit tests.

### GitHub Copilot

Use issue/PR descriptions generated from the DRL issue template. Treat suggestions as untrusted code: verify APIs, licenses, security, and tests. Copilot must not decide ADRs or release gates.

### Gemini CLI

Grant the minimum filesystem and command permissions required. Require confirmation for cloud-mutating commands. Use the technical reference register and authoritative Google documentation for current service behavior; record any updated assumption.

## Recovery prompt after an interrupted session

```text
Resume DRL mission [NN] from repository state, not chat memory. Read WORKLOG.md, the latest handoff, branch history, open issues, and current diff. Run validation. Summarize completed work packages, inherited failures, uncommitted state, temporary resources, and the next smallest verifiable work package. Do not repeat completed work or silently discard changes.
```

## Review-agent prompt

```text
Review this DRL pull request independently against its mission, controlling specs, requirement IDs, ADRs, and evidence. Focus on contract compatibility, security/privacy, deterministic boundaries, provenance, evaluation validity, accessibility, cost, license, rollback, and documentation. Re-run relevant checks. Report blocking defects separately from improvements. Do not approve claims that lack artifacts or reproducible commands.
```
