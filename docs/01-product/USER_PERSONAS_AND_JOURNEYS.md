---
document_id: DRL-PRD-002
title: "User Personas and End-to-End Journeys"
version: 2.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# User Personas and End-to-End Journeys

## Priority order

The public website is an evidence-first academic workshop. Its primary journey
serves people evaluating the Director's research judgment. It is mostly
read-only: contribution routes remain available, but the site does not lead
with recruitment.

1. Academic evaluator: research peer, prospective mentor or PhD adviser, or
   grant reviewer.
2. Research-oriented employer or technical leader.
3. Curious developer, tinkerer, student, or teacher.
4. Future contributor.
5. The Director using the site as a public research record.

## Persona: The academic evaluator

**Goal:** decide whether the research questions, methods, and engineering are
serious enough to merit mentorship, doctoral study, funding, or further
conversation.

**Needs:** a crisp thesis, a real run, a substantial report, methods,
limitations, provenance, negative results, code, and a direct contact route.

**Journey:** homepage -> signed recorded run -> success/degraded comparison ->
`TR-2026-001` -> methods and limitations -> source/reproduction bundle -> About
and contact.

Success means this visitor can explain what the Director investigates, what the
current prototype proves, what it does not prove, and why the next research
question matters. The visitor must not need Atticus, an account, or a live model.

## Persona: The research-oriented employer

**Goal:** judge whether the Director can engineer and evaluate complex systems,
not merely describe them.

**Needs:** fast evidence, architecture, tradeoffs, code quality, failure
handling, quantitative discipline, and a concise profile.

**Journey:** homepage -> recorded run -> trace and architecture -> degraded case
-> report -> projects -> About/contact.

Quantitative financial analysis is useful supporting context. No employer name
or confidential work appears in the public material.

## Persona: The curious developer or tinkerer

**Goal:** inspect or run a reusable component or the integrated fixture demo.

**Needs:** truthful maturity, simple commands, transparent dependencies,
architecture, licenses, and bounded examples.

**Journey:** homepage -> replay -> Projects or Open Source -> repository -> local
quickstart -> tests and artifact docs.

## Persona: The student or teacher

**Goal:** understand agent orchestration, evidence lineage, evaluation, or
deterministic quantitative modeling by seeing a real system work.

**Needs:** plain-language explanations, visible failure cases, a reproducible
exercise, glossary links, and citation/license guidance.

**Journey:** Writing -> integrated workflow lab -> recorded trace -> exercise ->
technical report and further reading.

Teaching material lives under Writing/Methods until the collection is large and
maintained enough to justify a standalone Teaching route.

## Persona: The future contributor

**Goal:** determine whether a bounded issue is worth taking on.

**Needs:** governance, architecture, local setup, issue quality, attribution,
and maintainer expectations.

**Journey:** Open Source -> contribution guide -> architecture/spec -> local mock
setup -> good-first issue -> pull request.

This route is deliberately secondary. The homepage may expose Open Source but
must not imply that the workshop is recruiting a team or that collaboration is
required to validate the work.

## Persona: The Director as public notebook keeper

**Goal:** preserve a coherent, dated public record of research questions,
experiments, decisions, results, failures, and next steps.

**Needs:** repository-authoritative sources, stable identifiers, correction
history, honest maturity labels, and low-friction publication.
**Journey:** controlled document or signed artifact -> validation -> reviewed
publication -> Wix summary/link -> later correction or supersession.

## Private operator journey

Private Atticus use remains separate from the public website. The local runner,
private files, approvals, device pairing, and local logs never become public
site content or public-site authority.

## Cross-cutting journey requirements

Every journey specifies:

- entry and exit;
- anonymous, authenticated, or local identity;
- required services and a no-service fallback;
- data collected and retained;
- errors and recovery;
- keyboard, screen-reader, reduced-motion, and mobile alternatives;
- artifact identity, maturity, and last verification;
- evaluation events and cost guardrails.
