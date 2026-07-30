---
document_id: DRL-PRG-091
title: "Mission 00 Current-State Baseline"
version: 1.1.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-30
---

# Mission 00 Current-State Baseline

This baseline records what exists on the inherited foundation commit so later
agents do not confuse specification density with product maturity.

## Authority snapshot

| Class | State |
|---|---|
| Laboratory Bible / AGENTS / Director's Memo | Present and binding |
| Controlled program docs | Present under `docs/00-program/` |
| Machine requirements | `requirements/requirements.yaml` — 132 APPROVED-FOUNDATION requirements |
| Work packages | `requirements/work-packages.yaml` — 122 packages, Mission 00 previously PLANNED |
| Schemas/examples | 26/26 schema-example pairs present |
| ADRs | ADR-0001–0005 and ADR-0008 approved/foundation; ADR-0006/0007 IN REVIEW |

## Implementation maturity (honest)

| Surface | Maturity | Evidence |
|---|---|---|
| Atticus control plane | `prototype` | Deterministic planner, policy, approvals, orchestration, CLI, HTTP adapter; DRL-018 linked workflow |
| Atlas / FedLens / BalanceLab / EvalForge | `prototype` | M3 adapters/corpus/citations/scenarios composed into Atticus runtime |
| Local runner safety primitives | `prototype` | Traversal/symlink rejection; approval-bound writes |
| Protocol package | `prototype` | Pydantic models + JSON Schemas |
| lab-web / atticus-console | `specified` | Placeholder package scripts only |
| Atticus Core / Edge weights | `specified` | Bake-off gate open (DIR-004 / G-001) |
| GCP / Azure deploy | `specified` | Terraform/Bicep starters; no live project |
| Wix / DNS | `specified` | Runbooks and validators; not published |

## Repository operations

| Item | Observed state | Consequence |
|---|---|---|
| Git remote | Redirects to `chris-dewitt/DeWitt-Research-Lab-Foundation` | DIR-001 still needs Director confirmation in the Memo |
| Default branch | `main` only | `integration/v1` not yet created (DRL-001) |
| CI workflow | `.github/workflows/ci.yml` present | Branch protection / required checks not yet proven on GitHub |
| Issue system | Seed backlog in `.github/ISSUE_BACKLOG.md` | GitHub issues/milestones not yet created |
| Handoffs | Foundation entry in `WORKLOG.md` | No Mission 00 reservation before this baseline |

## Distinction table for agents

| Kind | Meaning in this repo |
|---|---|
| Specified behavior | Controlled docs / schemas / acceptance criteria |
| Existing behavior | Runnable Python vertical slice and validators |
| Missing behavior | Signed replays (DRL-019), trained models, web UIs, cloud deploy, Wix publish |
| Conflicting behavior | Director Memo previously said “no GitHub remote”; remote now exists — escalate, do not silently rewrite identity |
| Tests that prove behavior | `tests/`, `make demo`, foundation/open/domain validators |
| Unverified claims | Any public “live” or “open-weight production” statement |

## Baseline commands

```bash
make doctor
make demo
make verify
uv run pytest -q
```

Baseline is not a release claim. It is the starting truth for Mission 00 and M1.
