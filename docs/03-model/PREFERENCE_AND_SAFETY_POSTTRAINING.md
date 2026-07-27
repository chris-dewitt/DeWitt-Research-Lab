---
document_id: DRL-MOD-007
title: "Preference Optimization and Safety Post-Training"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Preference Optimization and Safety Post-Training

## Preference rubric

A preferred response is selected for objective reasons:

1. correct task interpretation;
2. valid and minimal tools;
3. correct permission behavior;
4. grounded claims;
5. correct handling of uncertainty;
6. efficient steps;
7. user control and understandable approval;
8. appropriate Atticus mode and clarity.

## Safety curriculum

- direct prompt injection;
- indirect injection in documents, web pages, tool results, issue text, and metadata;
- social engineering for credentials;
- encoded/obfuscated instructions;
- scope escalation;
- data exfiltration through tool arguments;
- cross-tenant requests;
- destructive-action euphemisms;
- approval fatigue and misleading summaries;
- poisoned memory;
- malicious plugin/tool descriptions;
- reward hacking and evaluator manipulation.

## Safety constraints

Safety training must not replace policy enforcement and must not make Atticus broadly refuse harmless educational or research work. Track over-refusal by category and demographic/topic slices relevant to intended use.

## Red-team loop

1. generate/adapt adversarial cases;
2. run against frozen candidate;
3. classify model, scaffold, policy, tool, or UI failure;
4. fix the correct layer;
5. add regression case;
6. rerun full category and benign controls;
7. document residual risk.
