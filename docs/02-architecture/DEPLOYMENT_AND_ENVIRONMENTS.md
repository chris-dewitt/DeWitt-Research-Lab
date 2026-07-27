---
document_id: DRL-ARC-014
title: "Deployment Architecture and Environment Promotion"
version: 3.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Deployment Architecture and Environment Promotion

## Environments

- `local`: Docker Compose, fixture data, mock/open local models.
- `dev`: shared cloud development, synthetic/public data, aggressive scale-to-zero.
- `stage`: production-like identities, migrations, load/security/release tests.
- `prod`: public release, restricted admin, immutable artifacts.
- `research`: isolated Vertex/Storage projects for model/data experiments; no production credentials.

Use separate Google Cloud/Firebase projects for stage and production. Production data is not copied to dev. Research outputs are promoted through artifact review, not direct bucket sharing.

## Deployment units

- Wix for the canonical institutional site at `www.dwit-labs.com`;
- Firebase/App Hosting or approved Google-hosted frontend deployments for Atticus, specialist apps, docs, and advanced interactive workspaces;
- Cloud Run services for APIs;
- Cloud Run Jobs or Vertex custom jobs for batch work;
- Cloud Run GPU for public model inference after benchmark;
- Cloud SQL private connectivity;
- object storage buckets by data class and environment;
- Artifact Registry images pinned by digest.

## Promotion

```text
feature branch -> PR checks -> merge -> dev
release candidate tag -> stage deployment -> migration/security/eval gates
signed release approval -> prod gradual traffic -> verify -> full traffic
```

Cloud Run revisions allow traffic splitting and rollback. Database migrations use compatible expand/migrate/contract sequences. Configuration and model revisions are promoted explicitly and appear in release manifest.

## Canonical domain and cross-host promotion

Production promotion includes Wix publication and DRL subdomain validation. A release cannot be called complete merely because cloud services are healthy; the Wix launch pages, canonical links, system maturity, navigation, consent, and application host mappings must match the promoted release manifest. DNS and Wix changes use the runbook at `docs/07-platform-gcp/DOMAIN_DNS_AND_WIX_RUNBOOK.md`.

Application frontends must be deployable and testable independently of Wix. Wix embeds are optional bounded views, never the sole deployment surface for a core V1 application.
