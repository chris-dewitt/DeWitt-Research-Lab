---
document_id: DRL-DAT-008
title: "Voluntary Trace Donation Policy"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Voluntary Trace Donation Policy

## Principle

Operational use and research donation are separate. A user may use public Atticus without donating content.

## Donation flow

1. user selects “Donate this trace to research” after reviewing a plain-language summary;
2. interface shows included messages, tool metadata, evidence, and exclusions;
3. user may redact turns or withdraw before submission;
4. system creates consent receipt with policy/version and scope;
5. trace enters quarantine;
6. automated secret/PII/license/tenant checks;
7. human review;
8. eligible parts may enter research dataset with provenance;
9. donor may request withdrawal before a stated dataset freeze; limitations after model release are disclosed.

## Never donated automatically

- local files or paths beyond allowed redacted metadata;
- raw voice;
- credentials;
- emails/calendar/private repository content;
- third-party personal information without rights;
- cross-user content;
- private adapters or memory;
- administrative/security traces.

## Research separation

Donation consent does not guarantee inclusion. Rejected traces are deleted under quarantine retention policy. Dataset releases report donation counts and filtering outcomes.
