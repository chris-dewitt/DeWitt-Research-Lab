---
document_id: DRL-OSS-029
title: "Contributor Routes and Good-First Issue Map"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-08-01
---


# Contributor Routes and Good-First Issue Map

Maturity: **prototype** contributor onboarding package.  
Sponsors do not set roadmap, review outcomes, benchmarks, or research conclusions.

## Tested setup (first hour)

```bash
make doctor
make bootstrap   # or the documented platform equivalent
make demo
make verify
```

Optional teaching companion:

- `docs/10-research/teaching/INTEGRATED_WORKFLOW_LAB.md`

Optional research companion:

- `docs/10-research/reports/TR-2026-001-integrated-workflow.md`

A contribution that needs undisclosed cloud accounts, paid APIs, private datasets, or local secret patches is not ready for review.

## Contribution map

| Route | Who it fits | Start here | Ownership |
|---|---|---|---|
| Docs / teaching | writers, learners | `CONTRIBUTING.md`, teaching lab | Research/Community |
| Fixtures / tests | new engineers | `tests/`, specialist `fixtures/` | component owners in subtree `AGENTS.md` |
| Protocol / schemas | API-minded contributors | `packages/drl-protocol/`, `schemas/` | Architecture/Protocol |
| EvalForge slices | eval researchers | `services/evalforge/` | EvalForge |
| Local runner safety | security-curious | `apps/atticus-local-runner/` | Local Runner |
| Open-source process | community stewards | `docs/09-open-source/` | Program Director / maintainers |

## Recognition

Credit follows `docs/09-open-source/CONTRIBUTOR_CREDIT_AND_AUTHORSHIP.md`. Documentation, evaluation, accessibility, teaching, and review count alongside code. Research authorship follows scholarly contribution criteria.

## Good-first issue seeds

Use the **Good first issue** GitHub template. Each seed below is intentionally local/fixture-safe.

### GFI-001 — Clarify a specialist README maturity label

- **Value:** prevent overstated “live data” claims
- **Files:** one of `services/atlas/README.md`, `services/fedlens/README.md`, `services/balancelab-ai/README.md`
- **Acceptance:** README states `prototype` / fixture maturity and points to the component `docs/SPEC.md`
- **Tests:** docs-only; run `make verify` if validators touch the file
- **Mentor route:** Atlas / FedLens / BalanceLab owner via subtree `AGENTS.md`

### GFI-002 — Add one hand-verifiable BalanceLab assertion comment

- **Value:** teach deterministic calculation literacy
- **Files:** `tests/test_balancelab_scenarios.py` or `tests/test_atticus_foundation.py`
- **Acceptance:** comment cites the `$15.81` bear-steepener identity without changing numeric expectations unless accompanied by proof
- **Tests:** `uv run pytest tests/test_balancelab_scenarios.py -q`
- **Non-goals:** new scenarios, live bank data

### GFI-003 — Improve teaching-lab exercise clarity

- **Value:** reduce first-hour friction for learners
- **Files:** `docs/10-research/teaching/INTEGRATED_WORKFLOW_LAB.md`
- **Acceptance:** one exercise instruction becomes copy-paste clearer; `tests/docs/test_teaching_lab.py` still passes
- **Tests:** `uv run pytest tests/docs/test_teaching_lab.py -q`
- **Non-goals:** adding private datasets or live API steps

### GFI-004 — Extend a failure-museum cross-link

- **Value:** keep failures discoverable
- **Files:** `docs/10-research/failures/`, `docs/08-web-brand/FAILURE_MUSEUM.md`
- **Acceptance:** one failure record gains a reciprocal link; no secrets or private logs
- **Tests:** `make verify` / foundation validators
- **Non-goals:** inventing unverified incidents

### GFI-005 — Schema example documentation tidy-up

- **Value:** help consumers read wire formats
- **Files:** `schemas/README.md` or one `schemas/examples/*.json` comment in docs
- **Acceptance:** example purpose stated in one sentence; example remains schema-valid
- **Tests:** foundation schema/example validators via `make verify`

## Issue filing checklist

Every good-first issue must include:

1. user/research value
2. exact files
3. setup commands
4. acceptance evidence
5. explicit non-goals
6. security/privacy/license notes
7. mentor/reviewer path
8. maturity impact (`NONE` / docs-only / etc.)

## Maintainer ownership

- Final merge authority: DeWitt (Director) or explicitly delegated maintainers
- Component contracts: subtree `AGENTS.md` owners
- Security-sensitive paths: require deny-path tests and cannot weaken tenant/policy invariants

## Related documents

- `CONTRIBUTING.md`
- `docs/09-open-source/CONTRIBUTOR_EXPERIENCE.md`
- `docs/09-open-source/GOVERNANCE_AND_MAINTAINERS.md`
- `.github/ISSUE_TEMPLATE/good-first.yml`
