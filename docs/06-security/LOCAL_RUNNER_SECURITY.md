---
document_id: DRL-SEC-012
title: "Local Runner Security Requirements"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Local Runner Security Requirements

## Device controls

- generated device key, non-exportable where OS supports;
- OS vault storage;
- pairing with user presence;
- fingerprint and named device;
- scope and approved roots;
- automatic update policy with signed packages;
- revocation and key rotation;
- local emergency stop.

## Task validation

- verify cloud signature/audience/expiry/nonce;
- validate schema and local tool version;
- re-run local policy;
- require local approval for data leaving device or consequential action;
- no arbitrary code from cloud;
- sandbox commands;
- redact result;
- record audit.

## Compromise modes

- cloud account compromised: local scopes and approval remain;
- device stolen: OS login/vault plus server revocation;
- local malware: outside full prevention scope; minimize privileges and clearly disclose;
- malicious update: signed release and verification;
- replayed task: nonce cache and expiry;
- paired-device enumeration: no public directory/API exposure.
