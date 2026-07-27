---
document_id: DRL-SEC-009
title: "Telemetry, Content Capture, and Retention Controls"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Telemetry, Content Capture, and Retention Controls

## Default production telemetry

Capture:

- IDs and timestamps;
- service/model/tool/version;
- status and latency;
- token/resource/cost counts;
- policy outcome/rule IDs;
- error code;
- evaluation summary;
- redacted data classification.

Do not capture full prompts, completions, tool arguments/results, local paths, email text, file content, voice, or private memory by default.

## Debug capture

Time-limited, environment-specific, operator-approved capture may be enabled for synthetic/public test accounts. It includes banner, audit, automatic expiry, access controls, and post-use deletion.

## Product analytics

Use privacy-conscious analytics such as PostHog self-hosted/cloud or equivalent only after an ADR and privacy configuration. Track page and feature events, not conversation content. Full operational telemetry belongs in restricted observability, not product analytics.
