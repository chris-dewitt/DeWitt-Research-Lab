---
document_id: DRL-CON-104
title: "Atticus Console State and Events"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Atticus Console State and Events

## State model

The primary flow is `idle → creating → active ↔ awaiting_approval → terminal`, with orthogonal connection states `connected`, `reconnecting`, and `offline`; and content modes `live`, `replay`, `cached`, and `illustrative`. The reducer rejects illegal regressions and records unknown additive events diagnostically without rendering arbitrary payloads.

## Required event renderers

- task and run accepted, including safe mode/model/configuration summary;
- plan summary and declared reason for revision;
- specialist/tool proposed, policy outcome, started, and completed/failed;
- approval requested, resolved, expired, or revoked;
- evidence and artifact added;
- budget, cost, and latency updates;
- degraded/warning and recovery;
- evaluation summary;
- exactly one terminal outcome.

## Pane model

Default panes are Conversation, Execution, Evidence/Artifacts, and optional System/Methods. Mobile uses tabs or a stacked layout and preserves context and focus. Execution detail may collapse; approvals interrupt visibly but not unpredictably.

## Reconnect and resume

The client stores the last contiguous acknowledged sequence. On reconnect it supplies that sequence, receives replayed events plus authoritative current state, de-duplicates by run/sequence/event ID, and reports irrecoverable gaps. It never guesses a terminal state.

## Signed replay

Replay verifies manifest digest/signature, displays execution date and pinned code/model/config, allows speed and step controls, and marks source staleness. Replay cannot submit approvals or mutate external systems.
