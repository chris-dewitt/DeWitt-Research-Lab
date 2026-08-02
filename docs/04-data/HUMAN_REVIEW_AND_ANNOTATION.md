---
document_id: DRL-DAT-006
title: "Human Review, Annotation, and Adjudication"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Human Review, Annotation, and Adjudication

## Reviewer guidance

Reviewers evaluate correctness, completeness, ambiguity, policy, privacy, realistic tool behavior, and annotation consistency. They do not reward wording preference as if it were task correctness.

## Review levels

- **L0 automated:** schema/environment checks only; not release eligible for critical sets.
- **L1 single review:** routine training data.
- **L2 independent double review:** gold safety, policy, privacy, and research claims.
- **L3 adjudicated:** disagreements or high-impact cases reviewed by owner/adjudicator.

## Rubric labels

- valid;
- valid after edit;
- ambiguous task;
- incorrect expected behavior;
- unsafe;
- privacy issue;
- fixture defect;
- duplicate;
- rights/provenance issue;
- reject.

## Agreement

Report raw agreement and category-appropriate statistics. Low agreement triggers rubric revision, reviewer training, and possibly category exclusion. Do not hide disagreement by adjudicating everything before measurement.

## Audit

Record reviewer ID/pseudonym, timestamp, original and edited fields, reasons, and adjudication. Public datasets may release reviewer counts and process without exposing personal identity.
