---
document_id: DRL-ADR-0006
title: "Proposed OpenTofu-First Infrastructure-as-Code Toolchain"
version: 0.1.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# ADR-0006: Proposed OpenTofu-first infrastructure-as-code toolchain

## Context

The approved foundation names Terraform as the infrastructure-as-code tool. DRL's strengthened open-source identity favors an OSI-approved, community-governed implementation where engineering fit is comparable. OpenTofu is a Linux Foundation project designed for Terraform-language compatibility. Existing module paths, providers, state, CI, and contributor expectations must be assessed before any substitution.

## Proposed decision

Evaluate and, if validation passes, use OpenTofu as the authoritative V1 CLI while retaining compatible HCL/module layout and a documented migration path. Keep `infra/terraform/` only if the naming remains clear and does not imply the HashiCorp CLI is authoritative. Pin the selected binary and provider locks.

## Alternatives

1. Continue with Terraform under its current terms.
2. Use OpenTofu for local/CI and Terraform only for an unsupported edge case.
3. Replace HCL with another open-source IaC system.
4. Delay the choice and maintain neutral configuration temporarily.

## Consequences

Potential benefits include clearer open-source alignment, community governance, and contributor accessibility. Risks include compatibility drift, provider/tooling differences, confusing documentation, and migration costs.

## Security and privacy

Whichever tool is selected must preserve state protection, least-privilege deployment identities, plan review, provider verification, and no secrets in source or avoidable state.

## Migration

Mission 05 runs a disposable-environment compatibility spike covering init, plan, apply, import, state backup, destroy, CI scanning, and documented rollback. The director approves or rejects the proposal before the toolchain is locked.

## Approval

Status: **IN REVIEW**. No agent may silently replace the approved Terraform toolchain before director approval.
