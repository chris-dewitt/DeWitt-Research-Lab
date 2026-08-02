---
document_id: DRL-GCP-012
title: "Cloud Cost Model and Budget Controls"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Cloud Cost Model and Budget Controls

## Cost centers

- web hosting/build;
- CPU services;
- GPU inference;
- Vertex training/evaluation;
- Cloud SQL;
- storage and egress;
- logging/monitoring;
- authentication/other managed services.

## Guardrails

- per-project budgets and alerts;
- global daily/monthly application budgets;
- scale-to-zero and max instances;
- request/token/step/tool quotas;
- log exclusions and retention;
- storage lifecycle and checkpoint cleanup;
- GPU job timeout and automated stop;
- label every resource/run;
- cost estimate before model experiment;
- public replay mode when budget reached.

## Reporting

Monthly report includes actual versus budget, cost per successful public task, training cost per candidate, idle cost, top services, and recommended actions. Budget is a product constraint; agents cannot raise it silently.
