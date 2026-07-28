---
document_id: DRL-LOC-106
title: "Atticus Local Runner System Specification"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-28
---


    # Atticus Local Runner System Specification

    ## 1. Purpose and authority

    The Atticus Local Runner is a user-controlled execution node. It validates cloud identity, message signature, task freshness, local policy, resource scope, and human approval before executing explicitly registered local capabilities. It initiates outbound communication and can run Atticus Edge or Core locally for private and offline workflows.

    This document defines V1 product boundaries, behavior, interfaces, invariants, quality attributes, and evidence for Atticus Local Runner. Laboratory-wide protocol, security, privacy, data, and release policies remain controlling.

    ## 2. Users and jobs

    - DeWitt operating Atticus privately on Windows.
- Open-source users installing a personal node.
- Local tool and plugin developers.
- Security reviewers and operators.
- The control plane discovering paired device capabilities.

    ## 3. V1 capabilities

    - Short-lived secure device pairing, rotation, and revocation.
- Outbound authenticated task channel; no public inbound port.
- Local policy enforcement independent of cloud recommendation.
- Approved-directory file search/read and bounded write/diff.
- Repository inspect, test, patch, and commit-proposal tools.
- Sandboxed allowlisted shell command profiles.
- Local voice input/output and optional Edge/Core inference.
- Trusted local approval UI, audit, kill switch, and offline mode.
- Signed plugin registration with explicit capabilities.
- Return minimal approved results instead of mirroring the workspace.

    ## 4. Explicit non-goals

    - General remote desktop or unattended administration.
- Router port forwarding.
- Cloud custody of local credentials.
- Arbitrary shell access for public users.
- Silent file or microphone collection.
- Automatic plugin or package installation.
- Claims of equivalent security on every unsupported platform.

    ## 5. Logical architecture

    ```text
Local CLI / Tray / Voice / Approval UI
              |
       Local Atticus Runtime (optional)
              |
 Local Policy + Capability Registry
       /         |          \
 Files/Repo   Sandbox      Apps/Voice
       \         |          /
       Local Audit / Credential Store
              |
 Outbound Paired Channel -> Atticus Control Plane
```

    ## 6. Canonical workflows

    ### Pairing
The user authenticates in the browser and initiates pairing locally. The runner creates a device key in the OS credential store. Proof-of-possession binds the account and device. The user reviews default scopes. Both sides display fingerprint and revocation controls.

### Approved repository task
The runner validates a signed task and resource scope. Read-only inspection and tests execute under local policy. A proposed patch is shown locally. Apply, commit, and push use separate risk-appropriate approvals. Result and digest return.

### Offline mode
Edge/Core and local tools run without cloud. Cloud specialists are unavailable or use explicitly exported public snapshots. No network fallback occurs silently.

    ## 7. Interfaces and integration

    - Pairing, capability, signed task/result, heartbeat, revocation, and audit-export protocol.
- Local IPC between UI, runtime, and tools with OS permissions and authentication.
- Plugin capability manifest with schema, permissions, resources, egress, data handling, health, and tests.
- Cloud sees capability names and safe status—not a device-wide crawl.

    Cross-project requests and results use DRL protocol envelopes. Every request carries schema version, identity/session, correlation, policy context, deadline, and idempotency metadata where applicable. Internal types may be richer but cannot silently change public semantics.

    ## 8. Invariants

    - No inbound public listener.
- Local policy can be stricter and cannot be overridden remotely.
- Signature, audience, nonce, expiry, device, and request digest validate before execution.
- Canonical local resources remain within approved scopes.
- Consequential effects require an unexpired local approval.
- Secrets and full private content remain local unless explicitly approved for transfer.
- Kill switch stops new work and revokes trust.
- Offline mode makes no hidden network call.

    ## 8.1 Prototype approved-root inspection (DRL-009)

    `SandboxedWorkspace` provides deny-by-default inspection inside one approved
    canonical root: path traversal and symlink escapes raise `PermissionError`;
    oversized and binary reads fail closed; transferable `read_text` /
    `inspect_text` results apply `redact_text`. Write proposals still bind
    digests to raw content. Maturity: prototype (no pairing channel yet).

    ## 9. Quality attributes

    - **Correctness:** typed inputs and verifiable artifacts, not ungrounded prose.
    - **Traceability:** operational steps can be reconstructed without storing hidden chain-of-thought.
    - **Security:** least privilege, deny by default, bounded egress, and approval for consequential actions.
    - **Privacy:** collection minimization and separation of public, DRL-private, and local-personal data.
    - **Reliability:** deadlines, cancellation, retry budgets, idempotency, and truthful degraded states.
    - **Accessibility:** public workflows support keyboard, screen readers, reduced motion, contrast, and mobile use.
    - **Portability:** Docker/open fixtures for baseline; Google Cloud is reference production, not a mandatory local dependency.
    - **Evaluability:** every headline claim maps to a versioned suite and release gate.

    ## 10. Milestones

    - M1 capability registry, local policy, and simulator.
- M2 read-only file and repository tools with audit.
- M3 sandbox, patch/write actions, and approval UI.
- M4 pairing, outbound channel, key rotation, and revocation.
- M5 voice, local inference, and offline mode.
- M6 packaging, signed updates, security hardening, and public docs.

    ## 11. V1 acceptance

    - Windows reference installation and clean removal are tested.
- Pair, revoke, re-pair, and key rotation pass.
- File/repository workflows respect directory and action scopes.
- No inbound port is required.
- Forged, replayed, expired, and raced tasks are rejected.
- Offline packet inspection finds no unexpected egress.
- Audit, export, retention, and deletion controls work.
- Independent security review has no critical findings.

    ## 12. Principal risks and controls

    - Remote execution compromise: message signing, scoped tasks, local policy, and approval.
- Path or symlink escape: canonicalization and property/fuzz tests.
- Malicious plugin/update: signatures, explicit permissions, rollback.
- Approval spoofing: trusted local UI bound to digest.
- Voice privacy: push-to-talk/default local processing and visible capture.
- Platform complexity: Windows V1 reference with portable interfaces.

    ## 13. Change control

    An ADR is mandatory for public API changes, authority or trust-boundary changes, persistence/retention changes, rights/licensing changes, critical evaluation threshold changes, and deployment topology changes. Behavior-preserving internal refactors use ordinary review.
