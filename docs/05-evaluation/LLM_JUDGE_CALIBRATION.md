---
document_id: DRL-EVA-006
title: "LLM Judge Calibration and Governance"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# LLM Judge Calibration and Governance

## Use only when needed

Judge models may assess nuanced relevance, groundedness, style, and task completion when deterministic labels are insufficient. They are not used for permission facts that can be asserted directly.

## Calibration

- create human-labeled calibration set;
- compare multiple judge models/prompts;
- blind order and randomize pairwise position;
- test self/provider/model-family bias;
- measure agreement, false positives/negatives, and confidence;
- pin judge model and prompt versions;
- include periodic drift checks;
- route uncertain/disputed cases to human review.

## Prompt design

Judges receive rubric, relevant task/evidence, candidate, and required structured output. They do not see irrelevant brand/model names where blinding is possible.

## Reporting

Judge score is labeled model-assisted. Publish calibration statistics and known limitations. A changed judge invalidates direct historical comparisons unless overlap calibration is run.
