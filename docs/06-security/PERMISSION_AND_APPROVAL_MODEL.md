---
document_id: DRL-SEC-003
title: "Permission, Risk Tier, and Approval Model"
version: 2.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-09-18
---


# Permission, Risk Tier, and Approval Model

## Policy input

- actor/tenant/role;
- authenticated strength;
- device and environment;
- tool/version and risk tier;
- resource and scope;
- arguments and data classes;
- destination and side effect;
- task purpose;
- previous grants;
- cost estimate;
- time and location signals where appropriate.

## Policy output

- allow;
- deny with safe reason and alternatives;
- require approval;
- require step-up authentication;
- allow with constraints/redactions.

## Implemented approval triggers (2026-09-18)

The running `PolicyEngine` requires an approval on **either** of two independent
conditions, and records which one fired:

1. **Tier.** The call's risk tier is `REVERSIBLE_CHANGE` (2) or higher.
2. **Declared effect.** The catalog's `effect_type` is `external_effect` or
   `privileged`, whatever the tier. A tool declaring `prohibited` is denied
   outright.

Condition 2 was added by **ADR-0011** after `TR-2026-003` §5.3 measured a
read-tier tool performing a cross-session data egress with no approval. This
section of the specification already listed "destination and side effect" as
policy input; the engine did not read it. Both conditions read the catalog
definition, never the caller's claim.

Deliberately **not** gated by effect: `modify` and `draft`. They are gated by
tier where it matters, and gating them by effect as well would put every
ordinary local edit behind an approval.

Not yet implemented: the `approval_policy` field of
`schemas/tool-definition.schema.json` (`never` / `policy` / `always` /
`prohibited`). A tool cannot yet demand or waive approval for itself, and
`never` would be a way to weaken a gate, so it is an open decision rather than
a follow-up commit.

## Approval binding

Approval grant covers:

- exact actor and tenant;
- exact tool/version;
- normalized argument hash;
- resource/destination;
- data movement summary;
- maximum cost;
- one use or bounded count;
- expiry;
- authentication method;
- task/trace link.

Any meaningful change creates a new request. “Approve all future actions” is not offered for Tier 3/4 operations.

## Pre-approved workspaces

For local development, user may grant a temporary task scope such as “edit files in this repository branch for the next hour.” Policy still prohibits unrelated paths, push, secrets, dependency installs, and destructive operations unless separately authorized.

## Explanation

Approval cards are generated from typed operation and policy, not model prose. They show what, where, data leaving device, reversibility, estimated cost, and why approval is needed.
