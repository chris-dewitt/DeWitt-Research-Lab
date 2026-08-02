---
document_id: DRL-SEC-001
title: "Security Architecture and Control Framework"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Security Architecture and Control Framework

## Security objectives

- protect user agency and data;
- prevent model-proposed actions from bypassing deterministic control;
- isolate public users, services, and local devices;
- minimize secrets and sensitive telemetry;
- maintain trustworthy release and artifact provenance;
- detect, contain, and learn from failures;
- preserve useful open access without irresponsible public capability.

## Framework mapping

DRL uses NIST AI RMF concepts—Govern, Map, Measure, Manage—as an organizing lens, plus application and agent-security guidance from OWASP-style practices, MCP security guidance for adapters, and conventional cloud least privilege. Mapping is documented but does not claim certification.

## Control layers

1. institutional policy and governance;
2. identity and tenant boundary;
3. model input/context boundary;
4. deterministic policy and approval;
5. tool registry/validation;
6. sandbox and service identity;
7. data classification/encryption;
8. observability/audit;
9. evaluation and red teaming;
10. incident response and recovery.

No single layer is trusted to compensate for all others.
