---
document_id: DRL-DAT-011
title: "Data Quality Metrics and Lineage Operations"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Data Quality Metrics and Lineage Operations

## Quality dimensions

- completeness;
- validity;
- uniqueness;
- consistency;
- timeliness;
- provenance completeness;
- license completeness;
- annotation agreement;
- contamination risk;
- class/category balance;
- drift from previous release.

Quality checks produce artifacts, not only console output. Critical thresholds block promotion.

## Lineage queries

The system must answer:

- Which source and transformation produced this evidence chunk?
- Which dataset versions contain this record?
- Which model runs used this dataset?
- Which public reports or model artifacts depend on a withdrawn source?
- Which claims cite this source version?

Lineage identifiers survive storage moves and use content hashes plus semantic IDs.
