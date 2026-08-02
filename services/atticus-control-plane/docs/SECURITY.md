---
document_id: DRL-ATT-106
title: "Atticus Control Plane Security and Privacy Specification"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


    # Atticus Control Plane Security and Privacy Specification

    ## Objective

    Atticus Control Plane must stay useful under hostile, malformed, ambiguous, and failure-prone inputs without giving a model authority it does not possess. Models propose. Deterministic systems authenticate, authorize, validate, constrain, execute, audit, and obtain human approval.

    ## Protected assets

    - Identity, session, consent, and account state.
- Tool authority and approval grants.
- Private/local references and bounded extracts.
- System instructions, skills, policy, and route configuration.
- Credentials, workload identity, quotas, and budgets.
- Traces, evidence, artifacts, and donation state.

    ## Principal threats

    - Instructions embedded in untrusted content.
- Forged/replayed approval or cross-session capability.
- Tool-catalog poisoning and argument smuggling.
- Cross-session/tenant data access.
- SSRF, uncontrolled egress, or credential exfiltration through tools.
- Denial of wallet/compute through loops or oversized tasks.
- Sensitive trace leakage through UI, logs, export, or evaluation.
- Compromised model/provider proposing manipulative actions.

    ## Required controls

    - Deterministic policy enforcement after proposal and before execution.
- Typed allowlisted tools, strict schema validation, canonicalization, and resource scopes.
- Nonce-bound expiring approvals tied to request digest, session, and device.
- Workload identity and Secret Manager; no shared static production keys.
- Step, time, token, cost, concurrency, and egress budgets.
- Tool-specific network allowlists and isolation.
- Explicit untrusted-content framing and provenance.
- Immutable privacy-safe audit events.
- Kill switches and revocation for tools, devices, skills, routes, and sessions.

    ## Privacy behavior

    - Public sessions have no personal memory and short retention.
- Content capture is off by default unless needed for a disclosed user feature.
- Trace donation is a separate affirmative action.
- Local runner returns only a scoped approved payload.
- Sensitive previews are redacted or shown locally where possible.
- Users can inspect history, telemetry, donated traces, devices, and deletion status.

    ## Public abuse controls

    - Per-IP/device/session quotas and concurrency caps.
- Authentication for expensive free-form workflows.
- No public write-capable external tools.
- Input/output/file size and type limits.
- GPU/provider spend circuit breakers.
- Abuse detection without building advertising profiles.

    ## Verification

    - Unit/property tests for policy and approval.
- Cross-session authorization and object-reference tests.
- Injection corpus and adversarial tool-output tests.
- Protocol/structured-output fuzzing.
- Threat review for every tool and skill.
- Independent pre-release security review.
- Tabletops for credential leak, compromised skill, public load abuse, and runner compromise.

    “Sanitize input,” “encrypt it,” and “use least privilege” are not evidence. Each control identifies the boundary, exact mechanism, negative test, telemetry signal, owner, and incident response.
