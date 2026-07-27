---
document_id: DRL-MOD-004
title: "Atticus Edge Model Specification"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Atticus Edge Model Specification

## Intended use

Atticus Edge provides responsive local interaction and efficient public routing. It handles bounded tasks and knows when to defer.

## Core capabilities

- classify intent and audience;
- choose simple local or public skills;
- produce one validated tool call;
- present approval requests in clear language;
- answer over a bounded offline DRL documentation index;
- manage voice turn-taking and cancellation;
- detect uncertainty, unsupported complexity, or high risk and escalate;
- preserve private-local routing.

## Escalation policy

Edge returns a typed `EscalationDecision` with reason:

- complexity;
- insufficient context;
- unsupported tool;
- low confidence;
- long synthesis;
- coding task beyond threshold;
- policy ambiguity;
- high-risk request.

Escalation does not automatically permit cloud transmission. Privacy policy chooses local Core, ask-user, or refuse.

## Training approach

- shared Atticus format and core data categories;
- oversample routing, approval, short tools, and escalation;
- distill selected teacher trajectories but preserve gold human policy labels;
- reject verbose chain-style outputs;
- optimize latency and constrained output;
- evaluate false confidence and under-escalation as major failures.

## Edge release targets

Targets are finalized after hardware profiling, but the plan measures:

- laptop memory at selected quantizations;
- first-token latency and tokens/s;
- voice round-trip;
- route/tool accuracy;
- escalation precision/recall;
- battery/CPU/GPU impact where measurable;
- offline install size.
