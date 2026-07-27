---
document_id: DRL-ARC-007
title: "Identity, Tenancy, Authentication, and Authorization"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Identity, Tenancy, Authentication, and Authorization

## Actor types

- anonymous session;
- authenticated public user;
- contributor/maintainer;
- research operator;
- administrator;
- local device;
- service workload;
- release automation.

## Tenancy

Every user-owned object carries a non-null tenant or explicit public scope. Repository methods require tenant context rather than accepting arbitrary tenant IDs from callers. Cache keys, object paths, vector filters, traces, reports, and queues include tenant boundaries.

Anonymous sessions use ephemeral tenant IDs with expiry and no discoverability. Public reference datasets are immutable shared resources, not copied into user tenancy.

## Authentication

- public web uses Firebase Authentication or an approved equivalent under ADR;
- service-to-service uses Google workload identity and audience-bound tokens;
- local devices use pairing-issued device credentials and signed tasks;
- administrative operations require stronger authentication and separate roles.

## Authorization

Role-based access controls provide broad eligibility; policy engine evaluates resource/action/context. Tool scopes are more granular than application roles.

Examples:

```text
lab.docs.read
atlas.public.research
fedlens.public.compare
balancelab.synthetic.execute
evalforge.report.read
runner.files.read:<approved-root>
runner.git.commit:<repository>
runner.email.send:<account>
```

## Session controls

- rotation and expiry;
- CSRF and secure cookie controls;
- rate and concurrency limits;
- server-side invalidation;
- local device revocation;
- no authentication tokens in model context.
