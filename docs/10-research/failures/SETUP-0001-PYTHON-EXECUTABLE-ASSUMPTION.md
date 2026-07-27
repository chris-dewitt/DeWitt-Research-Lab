---
document_id: DRL-RSH-FAIL-002
title: "Failure Record SETUP-0001: Nonportable Python Executable Assumption"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---

# Failure Record SETUP-0001: Nonportable Python Executable Assumption

## System and date

- System: clean-clone `make doctor` / DRL-004 evidence procedure
- Date detected: 2026-07-27
- Affected revision: `612d201`
- Severity: medium (new-contributor bootstrap evidence blocked)

## Symptom and impact

The first clean-clone proof failed because `make doctor` invoked `python`, while
the Linux environment exposed `/usr/bin/python3` and an uv-managed interpreter,
but no `python` command. The evidence procedure also assumed `/usr/bin/time`,
which was absent.

## Root cause

Developer commands encoded executable-location assumptions instead of using the
repository's approved Python environment manager and portable shell behavior.

## Detection

DRL-004 clean-clone execution returned:

```text
make: python: No such file or directory
make: *** [Makefile:9: doctor] Error 127
/usr/bin/time: No such file or directory
```

## Correction

- `make doctor` now runs `uv run python --version`.
- `make bootstrap` installs both locked Python and frozen Node workspaces.
- Evidence instructions use the shell `time` keyword.
- A second fresh clone passed bootstrap, doctor, demo, and verify.

## Regression evidence

See
[`M1 Clean-Clone Bootstrap and Demo Evidence`](../../00-program/evidence/M1-CLEAN-CLONE-2026-07-27.md).

## Residual limitations

Linux is proven. A Windows clean-room run remains required by Mission 01.
Docker was not available locally; GitHub CI owns the container-build proof.

## Related work

- DRL-004 — clean-clone bootstrap
- DRL-006 — Failure Museum
- PR #6 — Mission 00 program bootstrap
