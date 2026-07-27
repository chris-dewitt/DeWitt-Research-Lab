---
document_id: DRL-PRD-006
title: "Product Maturity, Scope, and Status Language"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Product Maturity, Scope, and Status Language

## Maturity labels

- **Specified:** controlled requirements exist; implementation may not.
- **Prototype:** proves a concept; interfaces and data may change; no operational claim.
- **Alpha:** usable by developers, incomplete, expected breaking changes.
- **Beta:** feature-complete for defined scope, public testing, known limitations.
- **Release candidate:** all planned V1 features present; only release-blocking fixes accepted.
- **Stable:** public compatibility and maintenance commitments apply.

Each system page and README displays actual status. A beautiful replay does not make the backend beta.

## Feature flags

Incomplete live capabilities are hidden behind explicit flags. Flags include owner, default by environment, expiry/review date, and removal issue. A flag is not a substitute for authorization.

## Scope rule

When schedule or capacity pressure appears, reduce implementation breadth inside a capability while preserving truthful, complete vertical slices. Do not keep broad menu items that lead to mocks represented as live systems.
