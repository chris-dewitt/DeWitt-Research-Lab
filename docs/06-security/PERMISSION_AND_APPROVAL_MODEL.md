---
document_id: DRL-SEC-003
title: "Permission, Risk Tier, and Approval Model"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
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
