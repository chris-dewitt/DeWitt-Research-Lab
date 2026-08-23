---
document_id: DRL-DAT-040
title: "Local public feed store"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-23
---


# Local public feed store

This directory holds **operator-refreshed** official public observations and
Fed press items. Generated JSON is gitignored. Fixtures in Atlas and FedLens
remain the default Atticus path.

```
uv run python scripts/refresh_public_feeds.py
$env:ATTICUS_LIVE_DATA="1"
$env:FRED_API_KEY="..."   # optional; yields still load from Treasury
uv run --package atticus-control-plane atticus-demo --public
```

See `docs/11-operations/PUBLIC_FEED_PIPELINE.md` and **ADR-0010** (opt-in
official public data feeds; in review). Yahoo Finance is not a source.
