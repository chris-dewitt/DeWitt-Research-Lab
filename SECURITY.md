---
document_id: DRL-ROOT-SECURITY
title: "Security Policy"
version: 3.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# Security Policy

## Reporting a vulnerability

Do not open a public issue for exploitable vulnerabilities, private-data exposure, credential leaks, or bypasses of policy/approval boundaries. Email `director@dewitt-labs.com`, the single public contact address approved in `DIRECTORS_MEMO.md` RES-019. Do not send credentials, raw private data, or unredacted secrets with the initial report.

Include affected version/commit, environment, reproduction, impact, prerequisites, logs with secrets removed, and a safe proof of concept. Do not access data that is not yours, persist beyond the minimum demonstration, degrade service, or publicly disclose before coordination.

## Response targets

DRL aims to acknowledge credible reports promptly, triage severity, establish a remediation/disclosure plan, and credit reporters who want recognition. Small independent projects cannot promise enterprise SLAs; actual status and timelines will be communicated honestly. Active exploitation or high-risk private-data exposure may trigger immediate service restriction or shutdown.

## Scope

Especially important surfaces include:

- Atticus permissions, approvals, identity, sessions, memory, and tool execution;
- public/private/local-runner boundaries and outbound transport;
- prompt injection, indirect prompt injection, data exfiltration, SSRF, command/path injection, sandbox escape, and secret leakage;
- model/data supply chain, artifacts, deserialization, dependencies, CI/CD, and cloud IAM;
- cross-tenant access, consent, telemetry/content capture, retention, and deletion;
- BalanceLab calculation integrity and public claim provenance.

## Supported versions

Officially supported releases are listed in release notes. Development branches and research artifacts may change, but security reports are still welcome. Forks are maintained by their operators unless explicitly stated.

## Security invariants

- Deny by default; the model cannot grant authority.
- Public Atticus has no external write tools.
- Consequential local actions require explicit scoped approval.
- Cloud cannot initiate inbound access to a private device.
- Secrets are never stored in source or model prompts.
- Private content remains local unless a clearly disclosed approved workflow sends the minimum required payload.
- Every external action is attributable and auditable.

See `docs/06-security/` for architecture and test requirements. Security findings block release according to `docs/12-acceptance/V1_RELEASE_CRITERIA.md`.

## Coordinated disclosure and advisories

Fixes receive tests, affected-version analysis, release notes/advisory, and upgrade/mitigation instructions. Historical records preserve the vulnerability without publishing unnecessarily weaponized detail before users can update.
