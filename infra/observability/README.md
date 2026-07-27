---
document_id: DRL-SYS-023
title: "Observability Standard"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Observability

## Required signals

- traces;
- metrics;
- structured logs;
- evaluation artifacts;
- cost ledger;
- security events.

## Shared dimensions

- environment;
- service;
- version;
- task;
- session class;
- model;
- tool;
- skill;
- data classification;
- success or error class.

Sensitive content must not be used as a label or metric dimension.
