---
document_id: DRL-LOC-105
title: "Atticus Local Runner Security and Privacy Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


    # Atticus Local Runner Security and Privacy Specification

    ## Objective

    Atticus Local Runner must stay useful under hostile, malformed, ambiguous, and failure-prone inputs without giving a model authority it does not possess. Models propose. Deterministic systems authenticate, authorize, validate, constrain, execute, audit, and obtain human approval.

    ## Protected assets

    - Device and account keys.
- Local files, repositories, and shell authority.
- Microphone, transcripts, and voice data.
- Local memory, models, and adapters.
- Plugin and update trust.
- Local audit and cloud channel.

    ## Principal threats

    - Compromised cloud/model sends malicious work.
- MITM, forged message, or replay.
- Local malware steals key.
- Path or sandbox escape.
- Plugin or update compromise.
- Approval spoofing.
- Privilege escalation.
- Data exfiltration.
- Unintended microphone capture.

    ## Required controls

    - OS credential store and non-exportable key where supported.
- TLS plus signed messages with audience, nonce, expiry, device, and digest.
- Outbound-only channel.
- Local deny-by-default policy.
- Trusted local approval UI.
- Sandbox and canonical paths.
- Plugin/update signatures, explicit permission review, and rollback.
- Redacted local audit, kill switch, key rotation, and revocation.

    ## Privacy behavior

    - Default local storage and processing; no full-workspace index upload.
- Push-to-talk or explicit wake configuration and visible capture state.
- Transcripts stay local by default and are deletable.
- Users inspect capabilities, requests, transfers, devices, and audit.
- Private adapter and memory never sync without a distinct explicit feature and consent.

    ## Public abuse controls

    - Public website cannot pair to the owner's device.
- Pairing requires authenticated account and local physical action.
- Task quotas and resource limits.
- No anonymous public local tools.
- Suspicious-task lockdown and immediate revocation.

    ## Verification

    - Independent penetration review.
- Path and sandbox fuzzing.
- Forged-server and replay tests.
- Key rotation and revocation tests.
- Update-compromise drill.
- Packet inspection and local privilege review.
- Incident exercise and uninstall-residue audit.

    “Sanitize input,” “encrypt it,” and “use least privilege” are not evidence. Each control identifies the boundary, exact mechanism, negative test, telemetry signal, owner, and incident response.
