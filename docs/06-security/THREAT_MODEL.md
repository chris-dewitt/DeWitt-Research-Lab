---
document_id: DRL-SEC-002
title: "System Threat Model and Abuse Cases"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# System Threat Model and Abuse Cases

## Assets

- user identity and sessions;
- private local files, voice, memory, email, repositories;
- credentials and signing keys;
- model and dataset artifacts;
- public/source corpora and provenance;
- calculation results;
- traces and audit logs;
- cloud budgets and resources;
- DRL brand and release integrity.

## Adversaries

- malicious anonymous user;
- authenticated abusive user;
- compromised account;
- malicious or compromised data source;
- malicious plugin/dependency;
- compromised service or CI credential;
- model behaving unexpectedly;
- accidental developer/agent error;
- local malware or stolen device;
- sponsor/partner pressure on research integrity.

## Major threats and controls

### Indirect prompt injection

Untrusted document instructs Atticus to ignore policy or call tools. Controls: instruction/data separation, source labeling, reduced tool context, policy outside model, taint metadata, adversarial evals.

### Data exfiltration

User asks model to encode secret into a URL/tool argument. Controls: data-class-aware policy, destination allowlist, argument inspection, content minimization, local approval, egress restrictions.

### Approval spoofing or fatigue

Model disguises action or repeatedly requests approval. Controls: system-generated approval summary from typed operation, exact binding, rate/duplicate suppression, local display, no model-authored authoritative risk label.

### Cross-tenant access

Missing tenant filter, cache key, object path, or vector filter. Controls: tenant-aware repositories, row-level or application enforcement, scoped service APIs, automated isolation tests, no direct client database access.

### Tool command injection

Untrusted arguments reach shell/SQL. Controls: typed arguments, no shell string concatenation, parameterized queries, allowlisted commands, sandbox, path normalization.

### Supply-chain compromise

Malicious package, container, model, dataset, or plugin. Controls: lockfiles, digest pinning, SBOM, signature/provenance where available, dependency review, artifact registry, model/data hash register.

### Denial of wallet/service

Expensive prompts, GPU queue attacks, recursive agents. Controls: admission control, bounded steps/tokens/cost, per-user and global quotas, scale controls, circuit breakers, replay mode.

### Local runner compromise

Stolen device credential or malicious cloud task. Controls: OS vault, audience/nonce/expiry/signature, local policy and approval, revocation, no inbound port, minimal tool scopes.

### Evaluation manipulation

Prompt attempts to fool judge or traces omit failures. Controls: immutable trace events, deterministic critical assertions, judge blinding/calibration, separate audit channel.

## Residual risk

Language models remain vulnerable to novel manipulation and may produce unsafe proposals. DRL's core safety claim is not “the model is safe”; it is that proposals pass deterministic, least-privilege, observable controls and the residual risk is measured and disclosed.
