---
document_id: DRL-WEB-005
title: "Atticus Console, Trace, and Approval UX"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Atticus Console, Trace, and Approval UX

## Desktop layout

- conversation/report pane;
- execution pane with plan and live events;
- evidence/tool inspector;
- collapsible system map;
- command input and voice control where enabled.

## Event presentation

Human labels, not internal jargon:

- Understanding request
- Selecting research workflow
- Checking permissions
- Gathering Atlas evidence
- Comparing Federal Reserve documents
- Running deterministic scenario
- Evaluating trace
- Preparing report

Detailed view exposes exact tool/version, arguments after redaction, trace IDs, timings, and results.

## Approval card

Generated from policy operation:

```text
ATTICUS REQUESTS APPROVAL
Action: Push branch feat/123-policy-engine
Destination: github.com/.../drl
Changes: 4 commits / 11 files
Data leaving device: source diff and commit metadata
Reversible: yes, through Git
Expires: 5 minutes
[Review diff] [Approve once] [Reject]
```

No generic “Allow Atticus to continue?” prompt for consequential actions.

## Voice

- push-to-talk clearly active;
- transcript editable before dispatch;
- cancel/interrupt;
- screen equivalent;
- no autoplay public audio;
- public Atticus muted by default.

## Error/degraded states

- model waking;
- specialist unavailable;
- source stale;
- quota reached;
- approval expired;
- evaluation failed;
- replay offered.

Errors state effect and safe next step without pretending success.
