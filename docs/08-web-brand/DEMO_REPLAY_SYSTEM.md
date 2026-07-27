---
document_id: DRL-WEB-015
title: "Live Demonstration and Replay System"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Live Demonstration and Replay System

## Replay bundle

A replay is a sanitized immutable execution package containing:

- task and context;
- system/model/tool versions;
- trace events and timestamps (real or normalized for playback);
- redacted tool inputs/results;
- evidence/calculation references;
- evaluation report;
- generated final report;
- manifest/hashes/signature;
- recorded-at date and maturity.

## UI

Always label `LIVE`, `REPLAY`, or `SIMULATION`. User can pause, scrub, inspect event, switch between human and technical detail, and open source/repository.

## Production use

Replays are first-class reliability assets, not fake demos. They keep the site useful during cold starts, budget limits, incidents, and future data changes while preserving the historical context.
