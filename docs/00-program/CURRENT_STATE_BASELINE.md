---
document_id: DRL-PRG-091
title: "Current-State Baseline"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-17
---

# Current-State Baseline

This baseline separates implemented evidence from specifications and planned
work. It is a repository truth statement, not a V1 or production-release claim.

## Identity and authority

| Item | Current state |
|---|---|
| Repository | `chris-dewitt/DeWitt-Research-Lab` |
| Public identity | Christopher Noxon DeWitt's independent academic research portfolio |
| Institutional boundary | Independent work outside UNC coursework; no employer or university representation |
| Public contact | `director@dewitt-labs.com` |
| Website | [`www.dewitt-labs.com`](https://www.dewitt-labs.com), live personal portfolio |
| Source visibility | Private through 2026-09-30 under RES-018 |
| Binding sources | `LABORATORY_BIBLE.md`, `AGENTS.md`, `DIRECTORS_MEMO.md`, approved specifications and ADRs |

## Implementation maturity

| Surface | Maturity | Evidence boundary |
|---|---|---|
| Atticus control plane | `prototype` | Deterministic planner, policy, approvals, orchestration, CLI, HTTP adapter, and public fixture demo |
| Atlas, FedLens, BalanceLab, EvalForge | `prototype` | Runnable adapters and deterministic fixture paths composed into Atticus |
| Local runner safety primitives | `prototype` | Traversal and symlink rejection plus approval-bound writes |
| DRL protocol package | `prototype` | Typed models, JSON Schemas, examples, and contract tests |
| Replay viewer and public artifact exporter | `prototype` | Signed success/degraded fixtures, static build, allowlisted release envelope |
| Technical reports and teaching lab | `prototype evidence` | Reproducible documents and linked test or replay evidence |
| lab-web and atticus-console | `specified` | Package commands declare implementation pending; no implemented UI |
| Atticus Core and Edge weights | `specified` | No upstream selection, training run, or released weight artifact |
| Cloud deployment | `specified` | Infrastructure starters only; no live DRL project or approved spend |

## Repository operations

| Item | Current state | Evidence |
|---|---|---|
| Default branch | `main` | Canonical remote branch |
| CI | Foundation workflow green on merged PR #45 | GitHub Actions run `31935774484` |
| Issue program | DRL-001 through DRL-034 recorded | `requirements/issue-register.yaml` and issue bodies |
| Public-source gate | Implemented on DRL-034 branch | `scripts/validate_public_repository.py` and tests |
| Branch protection | Deliberately not enabled | RES-018 |
| Public history gate | Blocked on Director choice | DIR-009; reachable commits contain an institutional author address |

## What is not claimed

- The repository is not V1, production-ready, or presently public.
- Placeholder Node package scripts are not application tests.
- No DRL open-weight model release exists yet.
- Fixture demonstrations are not live-user or production-system evidence.
- Infrastructure templates are not proof of a deployed cloud environment.

## Reproduce the current source checks

```bash
uv sync --all-packages --locked
make verify
make lint
make typecheck
make security
make public-check
```

`make public-release-check` additionally inspects reachable Git-author metadata
and is expected to remain blocked until DIR-009 is resolved.
