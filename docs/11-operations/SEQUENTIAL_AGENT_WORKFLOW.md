---
document_id: DRL-OPS-001
title: "Sequential Agent Development Workflow"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Sequential Agent Development Workflow

## Communication medium

Agents do not rely on hidden conversational context. They communicate through accepted repository artifacts: issues, ADRs, branch commits, PRs, worklog, test reports, and handoffs.

## Start protocol

- identify current accepted base;
- read prior handoff and verify claims;
- run doctor/tests relevant to inherited state;
- open or confirm issue;
- state intended slice and files;
- check ADR gates;
- create branch.

## During work

- commit coherent increments;
- update issue/worklog on changed scope;
- create failing test before risky logic where practical;
- preserve unrelated changes;
- record empirical findings that affect future decisions;
- do not leave secrets or huge artifacts in Git.

## End protocol

- run all required checks;
- update docs/schemas;
- write PR with evidence;
- write handoff;
- mark unresolved questions and exact next task;
- stop without self-merging.

## Context compaction

Handoffs summarize decisions and link canonical documents rather than pasting giant chat transcripts. The next agent reads source and verifies.
