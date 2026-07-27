---
document_id: DRL-ARC-008
title: "Atticus Local Runner Protocol"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Atticus Local Runner Protocol

## Pairing

1. Authenticated user requests a short-lived pairing code.
2. Local runner generates a key pair and device metadata.
3. User enters/approves code locally.
4. Runner exchanges code for device identity, server public configuration, and initial scopes.
5. Private key is stored in OS credential protection.
6. User sees device, fingerprint, scopes, last activity, and revoke control.

## Task channel

The runner initiates outbound HTTPS or approved stream connection. Tasks contain:

- task and trace IDs;
- device audience;
- exact tool and arguments;
- actor and tenant;
- nonce and issued/expiry times;
- operation hash;
- cloud policy decision;
- signature.

Runner verifies signature, audience, time, nonce/replay cache, device status, local policy, local approval, and tool schema. Cloud approval never bypasses local checks.

## Result minimization

The runner returns typed results with local redaction. Large private files are not uploaded by default. For cloud synthesis, approval names the exact excerpts or derived content transmitted.

## Offline mode

Runner can use local Atticus, local tools, and local audit without cloud. When reconnecting, it uploads only allowed operational metadata; private content sync is off by default.

## Revocation and incident behavior

- revocation terminates streams and invalidates future tasks;
- suspected compromise rotates device credentials;
- approval grants do not survive revocation;
- local emergency stop blocks dispatch immediately;
- runner keeps a tamper-evident local record of consequential operations.
