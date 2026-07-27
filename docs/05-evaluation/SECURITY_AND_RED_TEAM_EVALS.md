---
document_id: DRL-EVA-008
title: "Security, Abuse, and Red-Team Evaluation"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Security, Abuse, and Red-Team Evaluation

## Attack surfaces

- direct user prompt;
- retrieved documents and web content;
- tool descriptions/results;
- memory;
- plugin manifests;
- file names/metadata;
- repository issues/comments;
- approval text;
- model fallback;
- cross-tenant identifiers;
- trace donation.

## Test classes

- instruction hierarchy;
- secret/PII exfiltration;
- tool scope escalation;
- malicious URL/file/path;
- command injection;
- stored prompt injection;
- approval spoofing/replay;
- denial-of-wallet;
- evaluator manipulation;
- data poisoning;
- tenant/cache confusion;
- local-runner impersonation.

Findings include severity, exploitability, affected versions, reproduction, mitigation, regression test, and residual risk. Critical findings block release.
