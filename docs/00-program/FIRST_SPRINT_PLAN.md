---
document_id: DRL-PRG-093
title: "First Sprint Execution Plan — M1 Bootstrap"
version: 1.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-27
---

# First Sprint Execution Plan — M1 Bootstrap

## Sprint objective

Make the repository a trusted execution system: protected branches, issue
program, Director decision cadence, clean-clone proof, and hardened contract
tests — without implementing later-mission product features.

**Milestone:** M1 Repository Online and Trusted  
**Owning mission:** 00 (program) → hands off DRL-004/005/006 evidence work to
Mission 01 / foundation maintainers as noted per issue  
**Duration target:** first 14 days of `docs/00-program/90_DAY_EXECUTION_PLAN.md`  
**Branch for this planning PR:** `cursor/mission-00-program-bootstrap-ad29`

## Definition of sprint done

1. GitHub milestones M1–M4 exist; labels from `.github/labels.yml` applied.
2. Issues DRL-001–030 filed from `.github/ISSUE_BODIES/` (or equivalent register).
3. `integration/v1` exists; `main` protected; CI required.
4. Clean-clone bootstrap + `make demo` transcript attached to DRL-004.
5. Director's Memo weekly review cadence active (DRL-003).
6. First Failure Museum entry filed from real friction (DRL-006).
7. No production credentials introduced.

## Issue sequence (execute in order)

| Order | Issue | Title | Owner mission | Blocks |
|---:|---|---|---:|---|
| 1 | DRL-001 | Initialize repository and protected branches | 00 | all remote work |
| 2 | DRL-002 | Enable Actions and repository security features | 00/01 | merge safety |
| 3 | DRL-003 | Activate Director's Memo review | 00 | material decisions |
| 4 | DRL-004 | Prove clean-clone bootstrap and demo | 01 | contributor trust |
| 5 | DRL-005 | Expand protocol and state-machine contract tests | 02 | Atticus expansion |
| 6 | DRL-006 | Publish first real failure record | 00/15 | honesty culture |

Issues DRL-007–030 remain queued; do not start them until DRL-001–006 close or
are explicitly deferred with Director approval.

## Exact acceptance commands

### Repository trust (DRL-001 / DRL-002)

```bash
gh repo view chris-dewitt/DeWitt-Research-Lab-Foundation --json name,isPrivate,viewerPermission
gh api repos/chris-dewitt/DeWitt-Research-Lab-Foundation/branches/main/protection || true
gh api repos/chris-dewitt/DeWitt-Research-Lab-Foundation/branches/integration%2Fv1/protection || true
gh workflow list
```

Record screenshots or JSON of branch protection requiring `foundation-ci`. Confirm DIR-001 slug/casing first.

### Local proof (DRL-004)

```bash
git clone <canonical-url> drl-clean && cd drl-clean
make bootstrap
make doctor
make demo
make verify
uv run pytest -q
```

Attach timed transcript and OS/toolchain versions.

### Contract hardening (DRL-005)

```bash
uv run pytest -q tests/test_atticus_foundation.py tests/test_foundation.py
uv run python scripts/validate_foundation.py
uv run --package atticus-control-plane atticus-demo --public
```

Must cover success, denial, invalid input, cancellation, and legal terminal states
(add tests where gaps remain).

### Failure museum (DRL-006)

Publish under the controlled Failure Museum path named by Mission 15 docs once
the first real CI/setup failure is captured. Link issue, commit, and regression
test.

## Director decisions required this sprint

| ID | Action this sprint |
|---|---|
| DIR-001 | Confirm GitHub owner/slug matches the live remote or record transfer intent |
| DIR-003 | Confirm or create `security@dewitt-labs.com` (or interim contact in SECURITY.md) |
| DIR-002 | Not required to *code*; required before any `terraform apply` |

Do not invent resolutions. Update `DIRECTORS_MEMO.md` when the Director decides.

## Out of scope for this sprint

- Selecting Atticus Core/Edge upstream models
- Public Fed/Atlas adapters
- Wix publication or DNS changes
- GCP project creation/apply
- Web UI implementation beyond placeholders
- Training runs

## Next sprint preview (after M1 exit)

Start M2 with **DRL-007** (typed open-weight provider interface) on a branch cut
from `integration/v1`. See `.github/ISSUE_BODIES/DRL-007.md`.
