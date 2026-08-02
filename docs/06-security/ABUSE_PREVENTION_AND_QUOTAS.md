---
document_id: DRL-SEC-010
title: "Public Abuse Prevention, Quotas, and Kill Switches"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Public Abuse Prevention, Quotas, and Kill Switches

## Controls

- request and token limits;
- concurrent-session limits;
- per-tool daily quotas;
- aggregate dollar/GPU budgets;
- content/file size limits;
- anonymous lower limits;
- abuse signals and cooldown;
- tool allowlists;
- model context and output caps;
- bounded agent steps/retries;
- queue max age;
- operator feature kill switches;
- replay-only degradation mode.

## Denial of wallet

Admission controller estimates cost and reserves budget before work. Long workflows show remaining budget. Model cannot request unlimited steps. External-source fan-out is capped.

## Response

When limits hit, explain the limit and offer static/replay material. Do not expose enough quota internals to enable evasion.
