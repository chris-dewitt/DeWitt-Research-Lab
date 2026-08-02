---
document_id: DRL-ARC-031
title: "DRL Contract Schema Bundle"
version: 3.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# DRL Contract Schema Bundle

## Authority

Root `schemas/*.schema.json` files are canonical JSON Schema 2020-12 contracts. Language types are generated or verified against them. Canonical `$id` values are stable identifiers; local relative paths are packaging details.

## Rules

- `additionalProperties: false` is preferred for signed, persisted, or cross-service envelopes.
- Times use RFC 3339 UTC; units and as-of semantics are explicit.
- Digests use canonical serialized content and a documented algorithm/profile.
- IDs are opaque; consumers do not parse business meaning from them.
- New optional fields are generally compatible; changed meaning, new required fields, enum removal, or type change is breaking.
- Examples validate and serve as contract-test fixtures, not merely documentation.
- API/event/storage translations preserve semantic fields and error behavior.

## Validation

Run `python scripts/validate_foundation.py`. It validates schemas, canonical IDs, references, examples, YAML configurations, OpenAPI syntax/structure, controlled documents, requirement/work-package registers, and required project/agent depth.
