---
document_id: DRL-PLT-011
title: "Domain, DNS, TLS, and Wix Operations Runbook"
version: 1.0.0
status: APPROVED OPERATING PROCEDURE
owner: DeWitt
last_updated: 2026-07-26
---

# Domain, DNS, TLS, and Wix Operations Runbook

## Purpose

This runbook operationalizes the registered domain `dwit-labs.com`, the Wix institutional website, and DRL application subdomains without committing credentials or registrar-specific secrets.

## Pre-change inventory

Record in the private operator log, never in the public repository:

- registrar and account owner;
- renewal date and auto-renew status;
- authoritative nameservers;
- Wix plan/site identifier;
- current A, AAAA, CNAME, TXT, MX, CAA, SRV, and forwarding records;
- mail provider and verification records;
- DNSSEC status;
- existing certificate and redirect behavior;
- recovery methods and second-factor status.

Export or screenshot the pre-change zone in a secure private location. Redact account numbers, transfer codes, and verification secrets.

## Change sequence

1. Create a change ticket with objective, exact records, TTLs, validation steps, rollback, and owner.
2. Lower TTL only when necessary and far enough in advance to matter.
3. Connect the existing domain to Wix using the selected, documented connection method.
4. Confirm `www.dwit-labs.com` resolves to Wix and presents a valid certificate.
5. Configure `dwit-labs.com` to redirect permanently to `https://www.dwit-labs.com`.
6. Verify mail and unrelated records remain intact.
7. Add application subdomain records only when the target service and certificate flow exist.
8. Verify DNS from multiple resolvers and networks.
9. Test HTTP-to-HTTPS, apex-to-www, unknown-path, and rollback behavior.
10. Record actual propagation and close the ticket only after monitoring is healthy.

## Planned records

The exact record type depends on the hosting service and must come from the current provider documentation.

| Hostname | Purpose | Target ownership | V1 state |
|---|---|---|---|
| `dwit-labs.com` | apex redirect | Wix or redirect service | required |
| `www.dwit-labs.com` | canonical institutional site | Wix | required |
| `atticus.dwit-labs.com` | public Atticus console | Google/Firebase/Cloud Run frontend | required for integrated V1 |
| `docs.dwit-labs.com` | versioned docs | Google/static deployment | required or approved route alternative |
| `status.dwit-labs.com` | public status | independent status/static page | required or approved route alternative |
| specialist subdomains | public system experiences | Google-hosted applications | deploy as systems become public |
| `api.dwit-labs.com` | versioned API gateway | Google Cloud | only when gateway exists |

Do not publish dangling DNS records to unclaimed cloud resources. Remove abandoned custom-domain mappings promptly.

## Security controls

- Registrar and Wix accounts require strong unique passwords and MFA.
- Domain transfer lock remains enabled except during an approved transfer.
- DNS change access is limited to DeWitt and explicitly delegated operators.
- CAA records are evaluated before production certificate issuance.
- DNSSEC is enabled when compatible with the selected DNS operating model and tested recovery procedures.
- Staging and preview hostnames require access control or non-indexing and must not share production cookies.
- Cookies use narrow domain scope; avoid `.dwit-labs.com` unless a reviewed cross-subdomain use case requires it.
- CORS uses explicit origins and methods; wildcard credentials are prohibited.
- CSP is defined independently for Wix and external apps, with minimal frame and script allowances.

## Wix integration checks

- connected-domain status shows healthy;
- no Wix-branded temporary URL is presented as canonical;
- page canonical URLs use `www.dwit-labs.com`;
- application launch links are HTTPS and point to approved subdomains;
- external embeds have fallback links and are tested on mobile;
- custom code does not contain secrets;
- analytics and consent configuration matches DRL policy;
- Wix collaborators receive only necessary roles.

## Monitoring

Monitor:

- DNS resolution and unexpected changes;
- certificate validity and expiration;
- apex/www redirect correctness;
- Wix homepage and important route availability;
- application subdomain availability;
- broken cross-site navigation;
- unexpected indexing of preview or private routes;
- domain-renewal and billing notices.

## Incident response

For domain hijack, DNS misrouting, certificate failure, or compromised Wix access:

1. Freeze nonessential changes.
2. Revoke compromised sessions and credentials.
3. Restore known-good DNS or Wix site assignment.
4. Disable affected app links or publish a static incident notice.
5. Preserve audit and provider evidence.
6. Rotate exposed tokens and review cross-origin access.
7. Notify users when risk or policy requires.
8. Publish a factual post-incident record after containment.

## Rollback

A rollback restores the exported known-good DNS zone or prior site assignment. Rollback instructions must identify which records should not be overwritten, especially MX and provider verification records. Never perform a blind full-zone replacement without reviewing changes made since the snapshot.
