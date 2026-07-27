---
document_id: DRL-PRG-EVD-001
title: "M1 Clean-Clone Bootstrap and Demo Evidence"
version: 1.0.0
status: RELEASE CANDIDATE
owner: DeWitt
last_updated: 2026-07-27
---

# M1 Clean-Clone Bootstrap and Demo Evidence

## Scope

Evidence for DRL-004 on the Mission 00 planning branch. This proves the local
fixture profile from a clean clone; it does not prove public deployment,
trained model operation, Windows support, or production readiness.

## Revision and environment

- Repository: `chris-dewitt/DeWitt-Research-Lab-Foundation`
- Branch: `cursor/mission-00-program-bootstrap-ad29`
- Commit: `0eaabd708ed1fb8ca29314d3938d551f486a7a36`
- Date: 2026-07-27 UTC
- OS: Linux 6.12.94+ x86_64
- Python: 3.12.3
- uv: 0.11.32
- Node: 22.14.0
- pnpm: 10.0.0
- Docker: unavailable; container build remains covered by GitHub CI

## Commands and exact results

```bash
git clone https://github.com/chris-dewitt/DeWitt-Research-Lab-Foundation.git
git checkout cursor/mission-00-program-bootstrap-ad29
time make bootstrap
make doctor
time make demo
time make verify
```

| Check | Result | Measured wall time / detail |
|---|---|---|
| `make bootstrap` | PASS | 1.312 s; locked uv workspace + frozen pnpm lockfile |
| `make doctor` | PASS | uv, Python, Node, pnpm detected; Docker truthfully optional |
| `make demo` | PASS | 0.087 s; 5 evidence items; EvalForge score 1.0 |
| Foundation validator | PASS | 329 controlled docs at tested revision |
| Program validator | PASS | 30 issues, 122 work packages, acyclic graph |
| Open identity validator | PASS | 26 V1 requirements, 10 stack records |
| Domain/Wix validator | PASS | canonical domain controls valid |
| Python tests | PASS | 25 passed |
| Node workspace tests | PASS | 2 placeholder workspaces; scripts explicitly report pending implementation |
| `make verify` | PASS | 2.694 s |

## Demo limitations printed by the executable

- Macro, market, and Fed inputs are synthetic fixtures for local development.
- BalanceLab uses a simplified educational repricing model, not production bank
  data.
- The deterministic planner stands in for Atticus Core until the model bake-off.

## Failure and correction discovered during proof

The first clean-clone attempt exposed two portability defects:

1. `make doctor` invoked `python`, but this environment provides `python3` and
   uv-managed Python.
2. The evidence command assumed `/usr/bin/time`, which is not present in the
   base image.

The Makefile now uses `uv run python --version`; evidence instructions use the
portable shell `time` keyword. The successful rerun above is from a new clone
after those corrections.

## Remaining acceptance work

- Repeat on supported Windows environment before M1 is declared complete.
- GitHub Actions run
  [`30239648838`](https://github.com/chris-dewitt/DeWitt-Research-Lab-Foundation/actions/runs/30239648838)
  passed the container build, frozen pnpm setup, program/docs checks, type
  checking, security scan, tests, and integrated smoke test.
- Web workspaces are honest placeholders, not implemented UIs.
