---
document_id: DRL-WEB-009
title: "Failure Museum Product Specification"
version: 2.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-27
---


# Failure Museum Product Specification

## Purpose

Show that DRL treats failures as research evidence and regression assets.

## Record fields

- title and system;
- date/version;
- user-visible symptom;
- severity and impact;
- minimal replay or sanitized trace;
- root and contributing causes;
- detection method;
- correction;
- regression test/evaluator;
- residual limitation;
- related issue/ADR/release.

## Candidate V1 entries

- temporal retrieval selected a later source for an as-of question;
- tool description caused wrong specialist route;
- citation supported topic but not exact claim;
- narrative rounded a BalanceLab value inconsistently;
- model requested approval after proposing a side effect;
- judge model preferred confident but unsupported response;
- GPU cold start created confusing blank state.

Failures are never fabricated for atmosphere and never expose private user data.

## Current records

- [`CI-0001: Duplicate pnpm Version Sources`](../10-research/failures/CI-0001-DUPLICATE-PNPM-VERSION.md)
- [`SETUP-0001: Nonportable Python Executable Assumption`](../10-research/failures/SETUP-0001-PYTHON-EXECUTABLE-ASSUMPTION.md)
