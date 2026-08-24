---
document_id: DRL-OPS-009
title: "Official Public Feed Pipeline"
version: 1.0.0
status: DRAFT
owner: Christopher Noxon DeWitt
last_updated: 2026-08-24
---


# Official Public Feed Pipeline

Opt-in means: fixtures stay the default, including CI. Live numbers appear
only after you refresh official public sources onto this machine and set
`ATTICUS_LIVE_DATA=1`. Atticus does not scrape the web during a task.

**ADR-0010** (the written decision for this path) is in review. Using the path
does not close it. It does not select Atticus Core or Edge (**DIR-004**).

Yahoo Finance is **not** a source. Its terms do not permit unofficial bulk
retrieval or redistribution. Use FRED or Treasury for yields.

## What it fetches

| Feed | Source | Needs | Atlas / FedLens id |
|---|---|---|---|
| CPI year-over-year | FRED `CPIAUCSL` (`units=pc1`) | `FRED_API_KEY` | `CPI_YOY` |
| 2-year Treasury | FRED `DGS2`, else Treasury CSV | key optional | `UST_2Y` |
| 10-year Treasury | FRED `DGS10`, else Treasury CSV | key optional | `UST_10Y` |
| Monetary-policy press | Fed RSS | none | FedLens documents |

Get a free FRED key at https://fred.stlouisfed.org/docs/api/api_key.html.
Attribute FRED: this workshop uses the FRED API and is not endorsed by the
Federal Reserve Bank of St. Louis.

## Operator path (PowerShell)

```
$env:FRED_API_KEY="your-key"
uv run python scripts/refresh_public_feeds.py --print-changes
$env:ATTICUS_LIVE_DATA="1"
$env:ATTICUS_MODEL="hf.co/Qwen/Qwen3-1.7B-GGUF:Q8_0"
$env:ATTICUS_MODEL_NO_THINKING="1"
uv run --package atticus-control-plane atticus-demo --public
```

Without a FRED key, refresh still loads Treasury yields and Fed press items.
CPI is omitted until the key is set.

Live mode defaults `--as-of` to **today**. The fixture pin `2026-07-24` would
hide later prints.

The store is `data/public-feeds/*.json` (gitignored). Re-run refresh to see
deltas. `artifacts.series_changes` on the Atticus result is the last print
minus the previous print for each series.

## What this is not

- Not a live bank. BalanceLab stays a synthetic educational sheet.
- Not a Yahoo or broker feed.
- Not a full FOMC transcript archive. RSS titles and descriptions only.
- Not production cloud ingest. **DIR-002** (GCP project and region) is still
  open.
- Not silent. If the store is missing, live mode fails closed.
