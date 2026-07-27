---
document_id: DRL-OSS-014
title: "Upstream Contribution, Attribution, and Dependency Stewardship Policy"
version: 3.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---

# Upstream Contribution, Attribution, and Dependency Stewardship Policy

## Institutional obligation

DRL's work is possible because thousands of people maintain open models, libraries, databases, standards, documentation, and infrastructure. Attribution is necessary but not sufficient. When DRL develops an improvement that is broadly useful and appropriate for an upstream project, it should attempt to contribute the improvement upstream.

## Contribution workflow

1. Confirm the issue on a supported upstream release.
2. Search existing issues, discussions, and contribution guidance.
3. Minimize the reproduction and separate DRL-specific policy.
4. Open an issue or discussion when maintainers request it.
5. Prepare a focused patch with tests and documentation.
6. Respect upstream style, governance, and review decisions.
7. Link the upstream item in the DRL work package and dependency ledger.
8. Remove temporary downstream patches after an accepted release is adopted.

## Attribution requirements

The website and release materials include an Open Stack ledger identifying major upstream projects and what DRL uses them for. Attribution must not imply sponsorship or endorsement. Generated NOTICE and SBOM artifacts supplement—but do not replace—human-readable acknowledgment.

## Maintainer respect

DRL contributors must not pressure unpaid maintainers, demand timelines, open duplicate issues across channels, or use public criticism to force acceptance. If an upstream project rejects a patch, DRL may maintain a documented extension or choose an alternative while preserving license obligations.

## Dependency stewardship

Each critical dependency has a DRL owner responsible for version tracking, advisories, compatibility tests, and exit options. The owner need not be an upstream maintainer. Ownership means DRL knows why the dependency exists and how to respond when it changes.

## Public upstream ledger

The ledger records:

- project and canonical repository;
- license;
- DRL dependency scope;
- pinned or supported version;
- criticality;
- DRL issues/PRs/contributions;
- temporary patches;
- known risks;
- review date;
- maintainer/contact link.

Accepted, pending, and rejected contributions are distinguished. Contribution counts are not used as a vanity metric.
