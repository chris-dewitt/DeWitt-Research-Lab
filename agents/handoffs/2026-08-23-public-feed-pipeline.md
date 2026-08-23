---
document_id: DRL-HO-OPS-20260823-FEEDS
title: "Handoff: Official public feed pipeline"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---


# Handoff: Official public feed pipeline

## 1. Branch and last commit

- Mission: Director request — actual FRED / market / Fed feeds and changing
  variables
- Branch: `cursor/live-public-feeds-ad29`
- Starting commit: `2e8a443` (`main` after PR #55)
- Ending commit: the commit containing this handoff
- Pull request: opened with this work
- Prepared UTC: `2026-08-23`

## 2. Objective completed

Isolated opt-in pipeline: ingest official public sources into a local store,
compute series deltas, optionally point Atlas/FedLens at that store.
**Did not** add Yahoo Finance. **Did not** change the default fixture demo.
**Did not** close **DIR-004**. **ADR-0010** and **DIR-010** await Director
acceptance.

## 3. Files and interfaces changed

- `scripts/public_feeds/` and `scripts/refresh_public_feeds.py`
- `services/atlas` live store adapter + `series_changes`
- `services/fedlens` live store loader
- Atticus runtime `ATTICUS_LIVE_DATA` / `DRL_FEED_ROOT`
- `configs/public-feed-sources.yaml`
- `docs/adr/ADR-0010-public-live-feeds.md`
- `docs/11-operations/PUBLIC_FEED_PIPELINE.md`
- Tests: `tests/test_public_feeds.py`

## 4. ADRs created or needed

ADR-0010 drafted, status IN REVIEW. Implementation is env-flagged.

## 5. Tests and results

```text
uv run ruff check scripts tests packages services apps/atticus-local-runner
# All checks passed

uv run mypy scripts packages services apps/atticus-local-runner
# Success: no issues found in 76 source files

uv run pytest -q
# 453 passed

uv run python scripts/validate_foundation.py
# VALIDATION PASSED (377 controlled documents)

uv run python scripts/validate_program.py
# PROGRAM VALIDATION PASSED

uv run python scripts/validate_public_repository.py
# PUBLIC REPOSITORY AUDIT PASSED

uv run bandit -q -r scripts packages services apps/atticus-local-runner
# exit 0
```

## 6. Deployment or migration notes

Operator-only. No cloud apply. Requires `FRED_API_KEY` for CPI.

## 7. Known failures and risks

- Treasury CSV column names can drift; tests pin the current header aliases.
- Fed RSS is short descriptions, not full statements.
- Live `--as-of` must be today, not the fixture pin.
- ADR unapproved: treat as experiment.

## 8. Uncommitted or generated artifacts

`data/public-feeds/*.json` is gitignored.

## 9. Next dependency-unblocking task

Director accept or reject ADR-0010. If accepted, next slice can add more
FRED series (unemployment, fed funds) the same way.

## 10. Exact reading order for the next agent

1. This handoff
2. `docs/adr/ADR-0010-public-live-feeds.md`
3. `docs/11-operations/PUBLIC_FEED_PIPELINE.md`
4. `scripts/public_feeds/refresh.py`
5. `tests/test_public_feeds.py`
