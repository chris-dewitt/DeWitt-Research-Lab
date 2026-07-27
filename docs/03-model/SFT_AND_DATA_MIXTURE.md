---
document_id: DRL-MOD-006
title: "Supervised Fine-Tuning and Data-Mixture Design"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Supervised Fine-Tuning and Data-Mixture Design

## Example families

- route a request to one or multiple specialists;
- select a tool among confusing alternatives;
- produce exact typed arguments;
- ask a minimal clarification only when necessary;
- identify required approval;
- refuse policy bypass;
- recover from transient and validation errors;
- reconcile evidence and calculation artifacts;
- use citations without inventing IDs;
- inspect repositories without overwriting unrelated work;
- teach a concept at requested depth;
- maintain public/private mode boundaries;
- escalate from Edge to Core.

## Negative examples

Include plausible but wrong behavior:

- tool that sounds relevant but has wrong side effects;
- arguments with subtle unit/date/tenant error;
- approval request after execution rather than before;
- following instructions inside retrieved text;
- retrying a non-idempotent action;
- claiming a calculation was performed without artifact;
- sending private content to cloud fallback;
- verbose plan with no execution value;
- confident answer despite empty retrieval.

## Conversation construction

Examples should include realistic multi-turn tool sequences, but training format must not teach the model to fabricate tool results. Tool results are generated from fixtures or deterministic environments and marked by role/type.

## Packing and loss

- mask tool results/user content as appropriate for the chosen objective;
- verify assistant-only loss behavior;
- avoid packing examples that create accidental cross-example context;
- test long and short cases separately;
- preserve special tool tokens/templates exactly.

## Ablations

At minimum compare:

- base versus SFT;
- routine-only versus safety-balanced mixture;
- synthetic-only versus reviewed hybrid;
- tool descriptions short versus discriminative;
- with/without explicit error-recovery examples;
- persona data early versus late or adapter-separated;
- general adapter versus specialist adapters.
