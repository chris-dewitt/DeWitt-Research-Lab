---
document_id: DRL-HO-032-20260805
title: "Handoff: DRL-032 CFI Primary-Source Novelty Review"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-05
---

# Handoff: DRL-032 CFI Primary-Source Novelty Review

## 1. Branch and commit

- Mission / packet: Mission 15 Research/Community / DRL-032 / CFI-002
- Branch: `lovesong/research/drl-032-cfi-literature-novelty`
- Work-package commit: `eaae47c`
- Research-record commit: `1797c0e`
- Pull request: none
- Handoff prepared UTC: `2026-08-05T23:33:04Z`

## 2. Objective completed

The bounded CFI-002 literature task produced a dated structured scoping review,
31-record primary-source matrix, claim-to-source mapping, revalidation boundary,
provisional dispositions, and independent-review checklist.

The issue did not pass G1. The review triggered its required stop condition:
current work substantially overlaps the original Paper I and Paper III
contributions and occupies the standalone coherence-repair component of Paper
II. DRL-032 is correctly `BLOCKED`, not `COMPLETE`. The approved questions in
DRL-RES-005 remain unchanged.

## 3. Files and interfaces changed

- `docs/10-research/CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md`
  - added search protocol and screening ledger;
  - recorded 31 retained primary records;
  - mapped each approved claim to closest work, overlap, remaining gap, risk,
    disposition, and dated revalidation;
  - recommended a narrowed Paper II flagship and bounded redesign of Papers I
    and III.
- `docs/references/TECHNICAL_REFERENCE_REGISTER.md`
  - added volatile CFI collision controls and revalidation gates.
- `DIRECTORS_MEMO.md`
  - added DIR-008 with three explicit options and the recommended G1 path.
- `.github/ISSUE_BODIES/DRL-032.md` and
  `requirements/issue-register.yaml`
  - recorded the G1 block and evidence paths.
- `WORKLOG.md`
  - changed the active reservation from in progress to G1-blocked.
- `tests/docs/test_cfi_primary_source_novelty_review.py`
  - guards the controlled review, closest collision sources, unchanged approved
    questions, block state, and revalidation controls.

No runtime, API, schema, dataset, model, prompt, participant, cloud,
publication, or public-site interface changed.

## 4. ADRs and decisions

- No ADR was created. The work is research scoping and did not change a public
  or cross-service architecture.
- DIR-008 is required before any primary question changes.
- RES-017 remains the approved program decision and has not been reinterpreted
  as approval to bypass the novelty gate.

## 5. Test and validation evidence

| Command | Exact result |
|---|---|
| `python scripts/validate_program.py` | PASS: 32 issues, 122 work packages, acyclic dependencies |
| `python scripts/validate_foundation.py` | PASS: 357 controlled documents, 132 requirements, 122 work packages, 26/26 schemas/examples, 16 missions |
| Focused pytest: CFI review, CFI program, and program controls | PASS: 17 tests |
| `python -m pytest -q -p no:cacheprovider tests/docs` | PASS: 30 tests |
| Focused Ruff check | PASS: no findings |
| `python scripts/validate_open_identity.py` | PASS: 26 V1 requirements, 10 stack records |
| `python scripts/validate_domain_wix.py` | PASS |
| Assignment-shaped secret scan | PASS: no findings |
| `git diff --check` | PASS; expected Git LF-to-CRLF workspace notices only |

One attempted combined validation command failed before execution because a
PowerShell regex string was quoted incorrectly. It produced no test result and
changed no file. The command was separated and all intended checks then passed.

## 6. Deployment and migration

None. No remote write, PR, merge, deployment, dataset acquisition, model call,
paid API, cloud resource, or publication action occurred.

## 7. Known failures and risks

1. **Paper I collision:** LearnStop directly tests the approved hypothesis's
   observable learned stopper, fixed-budget/confidence baselines, and
   cost-sensitive outcome.
2. **Paper II narrowing:** Outcome-Free Audits and Repairs occupies multi-axis
   Dutch-book auditing, formal coherent projection, and the
   coherence-versus-calibration distinction. Paper II remains plausible only
   as a carefully controlled intersection with payoff-equivalent financial
   claims, replication oracles, and paired human/model measurements.
3. **Paper III collision:** current primary work separately occupies
   private-signal AI-agent markets, shared-error monoculture, and
   incentive-compatible wagering aggregation.
4. **Volatility:** several decisive records are 2026 preprints or workshop
   papers and must be re-opened by 2026-09-05 or before G1, whichever comes
   first.
5. **Coverage:** this is a structured scoping review, not dual-reviewer
   systematic screening. Independent G1 review can add or correct sources.

## 8. Uncommitted or generated artifacts

At handoff preparation, the worktree was clean after `1797c0e`. This handoff
and its evidence references form the only subsequent intended documentation
commit. No generated data or temporary research artifact exists.

## 9. Next dependency-unblocking task

The Director must resolve DIR-008:

- recommended: preserve the three-paper program, make narrowed Paper II the
  flagship, and authorize a new bounded novelty packet for active
  information-acquisition Paper I and identifiable coupled-dynamics Paper III;
- alternative: classify all three as replication/extension work; or
- alternative: retain Paper II and replace Papers I and III.

After the Director chooses, a research agent may update DRL-RES-005 and the task
graph in a focused decision issue. No agent should start CFI-003/004 as a way to
evade G1, and no experimental packet is authorized.

## 10. Exact reading order for the next agent

1. `LABORATORY_BIBLE.md`
2. `DIRECTORS_MEMO.md`, especially DIR-008 and RES-017
3. `AGENTS.md`
4. `docs/10-research/COMPUTATIONAL_FINANCE_OF_INTELLIGENCE.md`
5. `docs/10-research/CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md`
6. `docs/references/TECHNICAL_REFERENCE_REGISTER.md`
7. `.github/ISSUE_BODIES/DRL-032.md`
8. `requirements/issue-register.yaml`, DRL-032
9. this handoff
10. the exact primary sources for the track the Director authorizes

## 11. Attestation

The review records a research-planning finding, not an empirical result. It
does not assert that any source will replicate, that the remaining Paper II
intersection is novel, or that either proposed redesign has passed G1. No
approved question was changed and no permission was inferred from source
availability.
