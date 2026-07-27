---
document_id: DRL-SEC-014
title: "Security and AI Incident Response"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Security and AI Incident Response

## Incident categories

- data exposure/cross-tenant;
- credential compromise;
- unauthorized side effect;
- prompt-injection/tool abuse;
- compromised dependency/model/data artifact;
- malicious public use or cost attack;
- research integrity/benchmark issue;
- harmful or materially incorrect public output;
- local runner compromise.

## Response

1. detect and open incident record;
2. classify severity and affected assets;
3. contain: disable tool/model/service, revoke credentials, switch replay-only;
4. preserve logs/evidence with privacy controls;
5. notify DeWitt and required parties;
6. investigate root and contributing causes;
7. remediate and add regression tests;
8. restore gradually;
9. communicate appropriately;
10. conduct blameless postmortem and update risks/specs.

Critical user-data incidents prioritize containment and notification over preserving a demo.
