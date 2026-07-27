---
document_id: DRL-ARC-006
title: "Skills and Plugin Architecture"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Skills and Plugin Architecture

## Skill definition

A skill is a versioned, reviewable workflow contract. It is not an arbitrary prompt. It declares:

- name, purpose, owner, maturity;
- trigger examples and exclusions;
- input/output schemas;
- allowed tools and specialist systems;
- required scopes and maximum risk tier;
- preconditions;
- deterministic validation steps;
- plan template or state graph;
- retry and degraded behavior;
- evaluation suite;
- user-facing explanation;
- examples and tests.

## V1 skills

- laboratory guide;
- contributor tour;
- architecture comparison;
- Fed document comparison;
- public macro research;
- synthetic balance-sheet scenario;
- model/evaluation comparison;
- integrated macro-policy-balance-sheet report;
- local repository review;
- local file search and summary.

## Plugin types

- tool adapter;
- data connector;
- retrieval strategy;
- evaluator;
- report renderer;
- model/runtime adapter;
- teaching module;
- skill bundle.

## Plugin security

- signed or checksum-pinned package;
- declared capabilities and destinations;
- no implicit secret access;
- sandbox where feasible;
- dependency scan;
- version compatibility;
- explicit admin installation;
- per-plugin enablement;
- public allowlist independent of installation.

V1 may publish the extension interface while delaying a public registry until compatibility and moderation processes are stable.
