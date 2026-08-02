---
document_id: DRL-OPS-005
title: "Cost Operations and Experiment Approval"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# Cost Operations and Experiment Approval

Every paid experiment or infrastructure change above configured threshold includes purpose, estimated spend, stop condition, owner, labels, cleanup plan, and expected decision. Training scripts enforce max steps/time and checkpoint before interruption.

Unexpected spend triggers:

1. disable nonessential live demos;
2. scale GPU/services to zero;
3. pause scheduled experiments;
4. inspect labels and cost breakdown;
5. rotate compromised access if abuse suspected;
6. document incident and prevention.
