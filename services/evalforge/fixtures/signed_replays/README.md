# Signed reference replays (DRL-019)

**DRL-019** was the work item that packaged success and degraded Atticus runs
as signed recordings. It is merged. What exists is a **prototype**: fixture
packages for local/CI verification, published on GitHub Pages at
https://chris-dewitt.github.io/DeWitt-Research-Lab/

Signatures use a published demo HMAC key (`drl-fixture-replay-v1`),
not a production signing identity.

Captured at fixed timestamp `2026-07-30T00:00:00+00:00` for reproducibility.
`live_at_capture` is always `false`.

Verify with:

```bash
uv run pytest tests/evalforge/test_signed_replays.py -q
```

