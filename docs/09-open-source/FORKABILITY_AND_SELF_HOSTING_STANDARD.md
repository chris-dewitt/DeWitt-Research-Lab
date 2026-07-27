---
document_id: DRL-OSS-013
title: "Forkability, Self-Hosting, and Exit Standard"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Forkability, Self-Hosting, and Exit Standard

## Objective

A central test of DRL's public-interest mission is whether a capable person can continue using and modifying the work without depending permanently on the official hosted service. Forkability is therefore a release property with tests, not a theoretical right in a license file.

## Required profiles

### Documentation and replay profile

Runs on a normal developer laptop and includes the website, documentation, curated traces, and evaluation reports. No GPU or paid API is required.

### Local research profile

Runs Atticus Edge or a small compatible open-weight model, local PostgreSQL or simplified storage, fixture data, mock specialists, and EvalForge. It supports tool routing, approvals, trace inspection, and public demo workflows.

### Full self-hosted profile

Runs Atticus Core, specialists, storage, job queue, observability, and the integrated reference workflow on documented GPU/cloud hardware. The profile may require infrastructure expense but cannot require proprietary DRL credentials.

### Hybrid private profile

Runs public cloud components plus the outbound-only local runner. Local data boundaries and approval semantics remain identical to official DRL.

## Exit requirements

The hosted platform provides documented export for:

- account and consent state;
- user-created public research artifacts;
- approved conversation or trace data where retained;
- plugin/skill configuration;
- model and dataset references;
- project settings;
- deletion requests and evidence.

Private local memory remains locally owned and does not require cloud export.

## Substituteability

Stable interfaces allow substitution of:

- Core/Edge models;
- inference runtimes;
- storage and vector backend through supported adapters;
- observability backend through OpenTelemetry;
- authentication in self-hosted profiles;
- cloud task runner;
- specialist services;
- model/data artifact hosting.

DRL may support one official path best. It must document extension points and avoid unnecessary checks that restrict alternative implementations.

## Clean-room test

Before V1, an independent release-QA agent or contributor must:

1. start from the public archive on a clean environment;
2. follow only published documentation;
3. verify licenses and required artifacts;
4. launch documentation/replay profile;
5. launch local research profile;
6. run a specified AtticusBench subset;
7. substitute at least one compatible model endpoint;
8. export and re-import supported state;
9. record all undocumented steps and failures;
10. publish a forkability report.

Critical undocumented credentials, missing artifacts, or hidden services fail the gate.
