---
document_id: DRL-SEC-008
title: "Multi-Tenancy, Privacy, and Data Subject Controls"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Multi-Tenancy, Privacy, and Data Subject Controls

## Isolation

- tenant ID derived from authenticated/session context, not request body;
- repository/data-access layer requires context;
- object paths include non-guessable tenant namespace;
- vector and full-text queries filter before scoring;
- background jobs carry signed tenant context;
- no shared mutable conversation cache;
- administration uses audited, scoped support tools.

## User controls

Authenticated users can:

- inspect stored conversations/projects;
- see retention setting;
- export eligible data;
- delete conversations/projects;
- revoke trace donation before freeze where policy allows;
- disconnect local devices;
- disable analytics categories where required.

## Privacy notices

Distinguish:

- essential operational metadata;
- product analytics;
- full operational telemetry in restricted environments;
- explicit research donation;
- local-only data.

Consent must not bundle research donation with basic service access.
