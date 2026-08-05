---
document_id: DRL-HO-021-20260804
title: "Handoff: DRL-021 Evidence-First Academic Positioning"
version: 1.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-04
---

# Handoff: DRL-021 Evidence-First Academic Positioning

## Handoff identity

- Mission / agent: Mission 06 Brand/Web / Codex
- Branch: `lovesong/docs/drl-021-positioning-cleanup`
- Pull request: not opened; branch is local and not pushed
- Starting commit: `37cf127`
- Implementation commit: `71d5b55`
- Started / completed UTC: `2026-08-05T03:11:02Z` / `2026-08-05T03:36:48Z`
- Environment: Windows, PowerShell, Python 3.14; Wix editor not touched

## Objective and result

- Planned objective: clean the repository documents using the Director's current
  website context, with the repository/code side in scope and Wix operation out
  of scope.
- Actual result: reconciled the controlled identity, audience, product, Wix,
  application-shell, issue, and validation documents around an evidence-first
  academic workshop. Added a regression test for the hierarchy and made existing
  document validators UTF-8 safe on Windows.
- Status: `COMPLETE` for the document cleanup; DRL-021 remains `QUEUED` because
  Wix editor implementation and visual evidence are still outstanding.
- Scope/approval: the Director's instructions in the initiating request are
  recorded as RES-015. No architecture or trust-boundary change was made.

## Work packages and requirements

| Work package | Requirement IDs | Status | Commit | Evidence |
|---|---|---|---|---|
| Academic audience and evidence hierarchy | DRL-WEB-001 | COMPLETE | `71d5b55` | Brand, PRD, personas, Bible, homepage, copy |
| Five-page Wix workshop and fallback contract | DRL-WEB-006 | COMPLETE (docs) | `71d5b55` | Wix plan, integration spec, issue criteria |
| Replay/report application-shell alignment | DRL-WEB-003, DRL-WEB-004 | COMPLETE (docs) | `71d5b55` | `apps/lab-web/docs/*` |
| Positioning regression guard | DRL-WEB-001, DRL-WEB-006 | COMPLETE | `71d5b55` | `tests/docs/test_website_positioning.py` |

## Public contracts changed

Compatible editorial clarification:

- Canonical Wix routes are Home, Projects, Writing, Open Source, and About;
  retired broad paths redirect into that tree.
- The first public actions are **Watch a recorded run** and **Read
  TR-2026-001**.
- Atticus is a documented research artifact and its public subdomain remains
  `planned`.

No API, schema, event, storage, authentication, authorization, or deployment
contract changed.

## Decisions and assumptions

- ADRs: none required; hosting and cross-host boundaries remain ADR-0008.
- Director decisions consumed: RES-013, RES-014, RES-015.
- Retained assumptions: Wix is the canonical editorial origin; the repository is
  the technical source of truth; the live editor is Director-operated.
- Invalidated assumptions: collaborator-first homepage, institute-first voice,
  public Atticus launch, standalone Status/Teaching/Failure Museum as mandatory
  Wix routes.

## Verification

| Check | Result | Notes |
|---|---|---|
| `python scripts/validate_foundation.py` | PASS | 352 docs, 132 requirements, 122 work packages, 26/26 schema examples, 16 missions |
| `python scripts/validate_program.py` | PASS | 30 issues, 122 work packages, acyclic dependencies |
| `python scripts/validate_open_identity.py` | PASS | 26 V1 requirements, 10 stack records |
| `python scripts/validate_domain_wix.py` | PASS | canonical domain/Wix contract |
| focused pytest command from DRL-021 | PASS | 31 tests |
| `python -m ruff check` on changed Python | PASS | no findings |
| full pytest excluding unsupported symlink setup | PASS | 198 test bodies; one Windows symlink test deselected |
| full unfiltered pytest | HOST LIMITATION | only failure was `WinError 1314` while the test tried to create a symlink; assertion did not run |
| Stage-B fixture JSON | PASS | `selection_status=not_selected`; six blockers for Core and six for Edge |
| `git diff --check` | PASS | no whitespace errors |

Focused pytest command:

```text
python -m pytest -q -p no:cacheprovider tests/docs/test_brand_consistency.py tests/docs/test_website_positioning.py tests/test_domain_wix.py
```

Executable full-suite command on this Windows host:

```text
python -m pytest -q -p no:cacheprovider -k "not test_workspace_rejects_symlink_escape_and_skips_symlinks_in_listing"
```

## Security, privacy, license, and cost impact

- New trust boundaries or permissions: none.
- Data classes touched: public controlled documentation and synthetic/fixture
  artifact descriptions only.
- Telemetry/content capture: none added; consent posture retained.
- Dependency change: none in the repository. The already-declared `jsonschema`
  development dependency was installed in the local user environment to execute
  validation.
- Cloud cost/capacity: none; no deployment or Wix write.
- Security evidence: existing full suite passed except the host-preconditioned
  symlink test; no security test was weakened or edited.

## Known limitations and debt

1. **High / Mission 06 / DRL-021 / blocks issue closure:** Wix pages, redirects,
   responsive captures, links, and accessibility evidence are not implemented.
2. **High / Platform / DIR-003 / blocks public contact completion:** approved
   contact/security route is still missing; copy retains an explicit gate.
3. **Medium / Mission 06 / DRL-021 / does not block docs review:**
   `atticus.dewitt-labs.com` remains planned and must not receive a launch action.
4. **Low / CI / no new issue / does not block docs review:** local Windows lacks
   symlink-creation privilege. Run the unchanged symlink-escape test in Linux CI
   or a Windows Developer Mode/admin environment.

## Dirty state and temporary resources

- Uncommitted files after the implementation commit: this handoff and final
  WORKLOG completion entry only.
- Temporary cloud resources: none.
- Pytest temporary directories created during validation: removed after exact
  path verification; they were generated and unrecoverable by design.
- Local data/checkpoints: none.
- Secrets or credentials: none created or stored.

## Next-agent start instructions

1. Check out `lovesong/docs/drl-021-positioning-cleanup` at or after `71d5b55`.
2. Read in order: `DIRECTORS_MEMO.md` RES-015 -> `BRAND_SYSTEM.md` ->
   `PORTFOLIO_V1_PRD.md` -> `HOMEPAGE_SPEC.md` -> `WIX_SITE_BUILD_PLAN.md` ->
   `SITE_COPY.md` -> `.github/ISSUE_BODIES/DRL-021.md`.
3. Run the focused pytest command and four repository validators above.
4. The Wix operator implements the page tree and collects DRL-021 acceptance
   evidence; do not deploy Atticus or create a live-service claim as part of that
   editorial task.
5. Preserve the canonical mission, research thesis, action order, negative
   results, one-person voice, and planned Atticus state.

## Attestation

I did not mark Wix implementation complete, did not claim an unrun test passed,
did not commit secrets/private/employer material, and recorded the one local host
limitation separately from repository behavior.
