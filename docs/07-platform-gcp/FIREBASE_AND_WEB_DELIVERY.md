---
document_id: DRL-GCP-004
title: "Firebase App Hosting and Web Delivery"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Firebase App Hosting and Web Delivery

## Application

Next.js application includes static institutional content, server-rendered public data where beneficial, and a client console connecting to Atticus APIs. Repository Markdown is built into documentation pages with controlled frontmatter.

## Environments

Use separate Firebase/Google projects for stage and prod. Preview builds run from pull requests where supported without production secrets.

## Custom domain and TLS

Configure canonical domain and redirects, managed certificates, security headers, content security policy, HSTS after validation, and separate API subdomains if needed. Domain configuration lives in runbook because some DNS steps are external.

## Caching

- immutable assets long-lived;
- docs/release manifests revalidated by version;
- user/session/API responses not cached publicly;
- replay assets content-addressed;
- stale-while-revalidate only for public safe content.

## Failure behavior

Static content and signed replays remain available during API/model outage. Status strip distinguishes web, live Atticus, specialists, and replay systems.
