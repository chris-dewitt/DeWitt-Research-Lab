---
document_id: DRL-ADR-0007
title: "Proposed Valkey Default for Cache and Ephemeral Coordination"
version: 0.1.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---

# ADR-0007: Proposed Valkey default for cache and ephemeral coordination

## Context

The scaffold uses a floating `redis:7-alpine` image and generic Redis terminology. A strong open-source identity requires exact version and license control. Valkey provides a BSD-licensed open-source implementation and Google Cloud offers a managed Valkey service, creating a consistent local/cloud path.

## Proposed decision

Adopt a pinned Valkey image and Valkey terminology for new cache, rate-limit, ephemeral queue, and coordination uses, subject to compatibility and operational testing. Use protocol-compatible clients behind a DRL adapter to preserve exit options. Durable workflows must not rely solely on an ephemeral cache.

## Alternatives

1. Pin Redis 7.2 or earlier under BSD-3-Clause.
2. Use Redis 8 under an approved AGPL/commercial review.
3. Avoid an in-memory data store and use PostgreSQL/Pub/Sub only.
4. Select another open-source queue/cache.

## Consequences

Benefits include license clarity, open governance, and local/managed alignment. Costs include migration testing, terminology changes, managed-service pricing, and possible command/client incompatibilities.

## Security and privacy

The service remains private, authenticated, encrypted in transit where supported, and excluded from durable sensitive-content storage. Data classes and retention apply. Public clients never connect directly.

## Migration

Mission 05 and the control-plane mission run compatibility tests for sessions, rate limiting, queues, idempotency, and failure recovery. Update Compose, environment names, documentation, and infrastructure only after approval.

## Approval

Status: **IN REVIEW**. Director approval is required. The existing scaffold remains non-authoritative and must not ship with a floating tag.
