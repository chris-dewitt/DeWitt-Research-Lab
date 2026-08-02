---
document_id: DRL-DAT-001
title: "Data Governance and Stewardship"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Data Governance and Stewardship

## Principles

- purpose limitation;
- minimum necessary collection;
- documented source rights;
- provenance and transformation lineage;
- explicit public/private/local classification;
- quarantine before training eligibility;
- user control over donated and private data;
- separation of training, development, and held-out evaluation;
- deletion and correction propagation;
- reproducible released datasets.

## Roles

- **Data owner:** The Director; approves public promotion and exceptions.
- **Dataset steward:** maintains manifest, rights, quality, and version.
- **Reviewer:** validates content according to review class.
- **Security/privacy reviewer:** assesses personal or sensitive data.
- **Release reviewer:** verifies artifacts and cards.

One person may hold several roles initially, but critical safety/gold cases require a documented second pass.

## Dataset states

```text
registered -> quarantined -> normalized -> validated -> reviewed
 -> eligible_private / eligible_public / rejected
 -> split_frozen -> released -> deprecated/withdrawn
```

Records carry state and may not be copied around the workflow to bypass it.

## Deletion/correction

A source withdrawal, privacy request, or discovered rights issue creates a lineage query identifying derived records, dataset versions, adapters, and public artifacts. Feasible remediation is documented; already distributed model effects may not be perfectly reversible, which must be disclosed.
