---
document_id: DRL-PRG-010
title: "Assumptions, Constraints, and Decision Gates"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Assumptions, Constraints, and Decision Gates

## Working assumptions

- DeWitt controls the GitHub organization, Google Cloud billing account, model registry accounts, and public domain.
- Initial contributor volume is low enough for director-led review.
- Public demo demand is bursty, making scale-to-zero desirable.
- Specialist systems use public or synthetic data only for V1.
- A commercial model may generate candidate synthetic data, but public operation does not require it.
- The repository starts documentation-first and implements vertical slices over time.
- No dedicated local GPU workstation is required for V1.

## Constraints

- Colab runtimes are ephemeral and not production infrastructure.
- Managed GPU cold starts may be visible.
- Open model licenses differ; “open weights” does not automatically mean Apache 2.0.
- Public model quality may require narrow skills and explicit escalation rather than universal competence.
- One coordinated public V1 increases integration risk; internal RC discipline is mandatory.

## Gates

Every open gate has a named owner, latest decision point, options, evidence, and fallback. A gate is closed only through an ADR or signed decision record.

Example gate record:

```yaml
gate_id: G-001
question: Which upstream model becomes Atticus Core?
owner: DeWitt
latest_decision_point: before Core SFT dataset freeze
options: [candidate_a, candidate_b, candidate_c]
evidence:
  - license review
  - AtticusBench baseline
  - tool/schema reliability
  - latency and memory
  - fine-tuning pilot
fallback: retain best base behind provider abstraction; delay merged release
```
