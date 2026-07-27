---
document_id: DRL-RSH-FAIL-001
title: "Failure Record CI-0001: Duplicate pnpm Version Sources"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---

# Failure Record CI-0001: Duplicate pnpm Version Sources

## System and date

- System: GitHub Actions `foundation-ci` / `node-workspace`
- Date detected: 2026-07-27
- Affected revision: PR #6, head `15c713a`
- Severity: medium (merge-blocking; no production impact)

## User-visible symptom and impact

The pull request displayed a failed `node-workspace` check before dependency
installation or any JavaScript lint/test/build command ran. Python contracts,
documentation, and the Atticus container jobs passed, but the PR was not green.

## Minimal sanitized replay

The action emitted:

```text
Error: Multiple versions of pnpm specified:
- version 10 in the GitHub Action config
- version pnpm@10.0.0 in package.json#packageManager
```

No secrets or private data were present in the log.

## Root and contributing causes

Root cause: `.github/workflows/ci.yml` passed `version: 10` to
`pnpm/action-setup@v4` while `package.json` independently pinned
`pnpm@10.0.0`.

Contributing causes:

- local validation ran `pnpm` directly and did not execute the setup action;
- the foundation validator did not assert a single package-manager version
  source;
- CI was first exercised only after the planning branch was pushed.

## Detection

GitHub Actions run `30238641685`, job `89891211564`, failed in
`pnpm/action-setup@v4` before `pnpm install`.

## Correction

- Removed the action-level version so `package.json#packageManager` is the sole
  version source.
- Restored `--frozen-lockfile` for deterministic CI installation.
- Added `scripts/validate_program.py` and a regression test that reject a second
  action-level pnpm version.

## Regression evidence

```bash
uv run python scripts/validate_program.py
uv run pytest -q tests/test_program_control.py
pnpm install --frozen-lockfile
pnpm -r lint
pnpm -r typecheck
pnpm -r test
pnpm -r build
```

Follow-up GitHub Actions run
[`30239648838`](https://github.com/chris-dewitt/DeWitt-Research-Lab-Foundation/actions/runs/30239648838)
passed `node-workspace`, `contracts-and-docs`, and `atticus-container`.

## Residual limitations

Local tests cannot perfectly emulate GitHub Action runner behavior. The
repository-level regression detects this specific configuration conflict;
GitHub CI remains the authoritative end-to-end action check.

## Related work

- DRL-002 — repository CI and security features
- DRL-006 — first genuine Failure Museum entry
- PR #6 — merged Mission 00 baseline containing the failure
- PR #7 — CI/bootstrap repair and regression evidence
