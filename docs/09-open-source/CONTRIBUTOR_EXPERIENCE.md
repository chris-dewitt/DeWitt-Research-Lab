---
document_id: DRL-OSS-004
title: "Contributor Experience, Issue Ladder, and Mentorship"
version: 3.2.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-08-01
---

# Contributor Experience, Issue Ladder, and Mentorship

## Design principle

Contributing to DRL should feel like entering a well-run research laboratory: the problem is legible, the safety and evidence standards are visible, the environment works, and the contribution teaches something. Contributors must not need private credentials, paid model APIs, or access to DeWitt's personal data to make meaningful progress.

## First-hour path

A clean contributor path provides:

1. `make doctor` to verify tools and print exact remediation;
2. `make dev` or a platform-specific equivalent;
3. a small open model or deterministic mock profile;
4. fixture data and a replayed Atticus workflow;
5. one test to modify safely;
6. links to the Laboratory Bible, relevant component spec, and issue ladder;
7. a contribution check that shows which gates will run in CI;
8. the integrated workflow teaching lab at
   `docs/10-research/teaching/INTEGRATED_WORKFLOW_LAB.md` (DRL-020).

Windows, Linux, and container paths are documented according to actual support, not aspirational badges.

## Issue levels

### Good first issue

Documentation, examples, typing, fixture improvement, deterministic unit test, accessibility label, error message, card metadata, source attribution, or reproduction report. Every issue includes exact files, setup, acceptance, mentor/reviewer, and a learning objective.

### Guided contributor issue

A small connector, evaluator, tool adapter, UI panel, CLI command, data-card enhancement, model-card test, or benchmark case. The issue provides architecture context and safe boundaries but leaves meaningful design work.

### Intermediate

New connector/evaluator/tool adapter, migration, integration test, runtime adapter, plugin example, data review pipeline, or evaluation slice. Requires reading the project spec and documenting evidence.

### Advanced

Policy engine, sandbox, temporal retrieval, model post-training, benchmark governance, protocol versioning, distributed execution, supply-chain hardening, security review, or statistical evaluation design.

### Research proposal

An experiment, replication, dataset study, or open-model comparison. It requires hypothesis, prior evidence, method, artifact plan, ethics/rights review, and publication criteria before expensive execution.

## Issue requirements

Every issue names:

- context and user/research value;
- requirement and work-package IDs;
- owner and likely files;
- prerequisites and protected paths;
- explicit non-goals;
- acceptance evidence and test commands;
- security, privacy, data, model, and license notes;
- upstream relationship;
- handoff expectation;
- maturity and compatibility impact.

## Pull-request evidence

A contributor PR includes:

- what changed and why;
- exact tests and evaluation run;
- documentation and card updates;
- protocol or migration impact;
- dependency/license changes;
- screenshots or trace artifacts where useful;
- failure modes and limitations;
- upstream issue/PR when applicable;
- release-note entry if user-visible.

## Mentorship and review

Mentors guide contributors without doing the entire issue. Review should explain requirements, not merely reject style. Maintainers may close stale or unsafe work, but should preserve useful research notes. Contributors are never asked to share private data or credentials for reproduction.

## Recognition

Release notes, cards, contributor lists, website profiles with consent, and research acknowledgments recognize substantive work. Paper authorship follows scholarly criteria. Official researcher or maintainer designation follows governance and sustained responsibility—not commit count.

## Support boundaries

DRL does not promise immediate review or one-on-one tutoring. Issues and discussions state expected channels. Security reports use private disclosure. Contributors should not contact personal accounts to bypass queues.
