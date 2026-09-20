---
document_id: DRL-HO-BENCH-20260920-DIGEST
title: "Handoff: Release-manifest digests no longer depend on the checkout"
version: 1.0.0
status: IN REVIEW
owner: Christopher Noxon DeWitt
last_updated: 2026-09-20
---


# Handoff: Normalize newlines before hashing release artifacts

## 1. Branch and last commit

- Branch: `fix/manifest-digest-newline-normalization`
- Base: `main` at `7aa78ae`
- PR: not yet opened
- Independent of `fix/atticusbench-model-run-timeout`; both branch from the same
  `main` and both append to `WORKLOG.md`, so whichever merges second will need a
  trivial append-conflict resolution there.
- Environment: Windows 11, `uv` 0.12.3, project `.venv`, Python 3.13.15

## 2. Objective completed

`tests/atticusbench/test_release_manifest.py` failed on the Director's Windows
clone with two digest mismatches while CI stayed green. The release manifest now
hashes newline-normalized bytes for text artifacts, so the digest describes the
content rather than the checkout.

**Status: COMPLETE.** Full suite on Windows: 776 passed, 1 skipped, 0 failed.

## 3. Root cause

`_file_digest` hashed `path.read_bytes()`. With `core.autocrlf=true` and
`* text=auto` in `.gitattributes`, git stores LF and the Windows working tree
holds CRLF, so the same commit produced different digests on different
platforms. Every artifact the manifest names is text, so every one was affected.

Two consequences, the second more serious than the first:

1. The dataset card claims the seed reproduces byte for byte. For the manifest
   that held only on LF platforms.
2. The failing test **rewrites the tracked manifest on disk**. Any model run
   started afterwards recorded `working_tree_dirty: true` and was correctly
   rejected by `test_a_committed_model_run_carries_truthful_provenance`. This is
   how the first local Qwen3-1.7B run came to be uncitable as evidence — the
   run was fine, the tree was not.

## 4. Fix

`artifact_digest(path, *, media_type)` replaces `_file_digest`. For a text media
type — anything under `text/`, plus `application/json`, `application/schema+json`
and `application/yaml` — it normalizes CRLF and lone CR to LF before hashing. A
binary artifact is still hashed byte for byte, because normalizing one would
corrupt the digest of any file where CR or LF is data. Nothing in the manifest is
binary today; the branch exists so that adding one does not silently inherit text
handling.

`test_every_referenced_artifact_exists_with_the_recorded_digest` now imports that
function instead of recomputing the hash itself. The duplicate was the reason the
test could not see the problem: it reproduced the raw read it was meant to be
checking, so generator and test agreed on each platform separately while
disagreeing with each other.

## 5. Files changed

| File | Change |
|---|---|
| `scripts/validate_atticusbench.py` | `_file_digest` becomes `artifact_digest`, normalizing newlines for text media types |
| `tests/atticusbench/test_release_manifest.py` | Recompute with the generator's function; drop the now-unused `hashlib` import |
| `WORKLOG.md` | 4.36.0 to 4.37.0 |

## 6. Public contracts changed

**None, and no published number moves.** The committed manifest was generated on
an LF platform, so normalizing reproduces exactly the digests already published.
`datasets/atticusbench/release/` is byte-identical after this change — verified
with `git status`. The fix makes Windows agree with the existing numbers rather
than changing them.

This was expected to move digests when the work was proposed. It does not, and
that is worth stating plainly: there is nothing to re-publish, no dataset card
version to bump, and no downstream digest reference to update.

## 7. ADRs

None created or needed. No schema, policy, scoring, or release-contract change.

## 8. Verification

```text
uv run pytest
uv run ruff check scripts tests packages services apps/atticus-local-runner datasets/atticusbench/src
uv run mypy scripts packages services apps/atticus-local-runner datasets/atticusbench/src
uv run bandit -q -r scripts packages services apps/atticus-local-runner datasets/atticusbench/src
uv run python scripts/validate_foundation.py
uv run python scripts/validate_program.py
uv run python scripts/validate_open_identity.py
uv run python scripts/validate_domain_wix.py
uv run python scripts/validate_public_repository.py
uv run python scripts/validate_atticusbench.py
git status --porcelain datasets/atticusbench/release/
```

| Check | Result |
|---|---|
| pytest | 776 passed, 1 skipped, 0 failed |
| ruff | All checks passed |
| mypy (strict) | no issues in 91 source files |
| bandit | clean |
| six validators | all pass |
| `datasets/atticusbench/release/` | no change |

This is the first fully green suite on the Director's machine. Before this
change the same command reported two failures there and zero in CI.

## 9. Known limitations and debt

- The normalization is keyed on media type, which the manifest supplies. A future
  artifact added with a wrong or missing media type would be hashed as binary and
  reintroduce the platform dependence for that entry. Severity low; the media
  type is already required by the manifest schema.
- `core.autocrlf=true` remains set on this machine. This change makes the
  manifest immune to it; it does not make the repository as a whole immune. Any
  future digest taken over working-tree bytes will have the same problem, and the
  fix is the same one.
- Not addressed here: the failing-test-mutates-tracked-state pattern. With the
  digest fixed the test no longer fails, so it no longer rewrites anything, but
  `test_regeneration_is_byte_identical` still writes to the tree as part of its
  assertion. Severity low; consider a temporary directory if it recurs.

## 10. Dirty state and temporary resources

- Uncommitted files: `docs/08-web-brand/assets/` (five untracked homepage hero
  PNGs, ~11 MB, from 2026-08-24; pre-existing and unrelated to this work).
- No secrets, credentials, or cloud resources created.

## 11. Next-agent start instructions

1. `git checkout fix/manifest-digest-newline-normalization && uv sync --all-packages --locked`
2. `uv run pytest` — expect 776 passed, 1 skipped, 0 failed on any platform.
3. Confirm `git status --porcelain datasets/atticusbench/release/` is empty. If a
   digest moved, something other than line endings changed and it should be
   understood before merging.
4. Do not reintroduce a second copy of the artifact hashing in a test.
5. The sibling branch `fix/atticusbench-model-run-timeout` fixes the benchmark
   completion budget; merging both needs one append-conflict resolution in
   `WORKLOG.md`.

## 12. Attestation

No work is marked complete without the evidence in section 8. No secrets,
private, or employer material was committed. The claim that no published digest
moves is verified by `git status`, not asserted.
