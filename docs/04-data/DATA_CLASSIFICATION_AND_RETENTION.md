---
document_id: DRL-DAT-002
title: "Data Classification, Handling, and Retention"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Data Classification, Handling, and Retention

## Classes

- **PUBLIC:** intended public content and released artifacts.
- **INTERNAL-RESEARCH:** unreleased experiments, annotations, and reports.
- **PRIVATE-USER:** authenticated user content, saved public projects.
- **LOCAL-SENSITIVE:** local files, email, voice, private memory, adapters.
- **SECRET:** credentials, tokens, private keys.
- **RESTRICTED-LICENSE:** data usable under terms but not redistributable.

## Handling summary

| Class | Training | Cloud storage | Logs | Public release |
|---|---|---|---|---|
| Public | after manifest/review | yes | content only if needed | yes |
| Internal research | approved experiments | restricted | metadata/minimized | approval required |
| Private user | no by default; donation flow only | tenant-isolated | redacted metadata | no |
| Local sensitive | local personalization only | no by default | no cloud content | no |
| Secret | never | secret manager/OS vault | never | never |
| Restricted license | per terms | restricted | metadata | generally no raw data |

## Retention defaults

- anonymous content: memory/session duration; operational metadata short-term;
- authenticated history: user-configurable with delete/export;
- public research traces: retained with release;
- donated traces: quarantine until consent and review; rejected donations deleted under policy;
- raw voice: not retained by default;
- audit records: longer retention proportionate to action risk;
- training manifests and release evidence: long-term immutable retention.

Exact durations are configuration and privacy-notice decisions before public beta.
