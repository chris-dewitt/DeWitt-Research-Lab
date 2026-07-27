---
document_id: DRL-PRD-004
title: "Private Atticus and Local Runner Product Requirements"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Private Atticus and Local Runner Product Requirements

## Product goal

Provide DeWitt with a local-first assistant capable of voice, file, and repository workflows while retaining explicit control over private data and consequential actions.

## V1 supported platform

- Windows is the primary supported desktop.
- Linux may be used for development and is a secondary target.
- macOS is documented as future-compatible but not required for V1 unless a contributor owns support.

## V1 capabilities

### Local voice

- push-to-talk is required; wake-word support may be experimental;
- speech-to-text adapter with local option;
- text-to-speech adapter with local option;
- visible transcript before consequential action;
- no raw audio retention by default;
- interruption/cancel support.

### Approved-directory file tools

- user grants directory scopes through local UI;
- search, metadata, read, summarize, and compare;
- write requires task-scoped approval and diff preview;
- hidden/system/credential paths denied by default;
- file content remains local unless cloud use is specifically approved.

### Repository tools

- inspect status, diff, branches, issues, and tests;
- run allowlisted commands in repository sandbox;
- prepare patches on a feature branch;
- commit only after approval;
- push only after separate approval;
- never alter unrelated changes;
- record commands, exit codes, and changed files.

### Private memory

- local encrypted store where practical;
- explicit categories and retention;
- user can inspect, correct, export, and delete memories;
- memory retrieval is cited in the interface as private memory rather than objective fact;
- private memory never enters public training.

### Device pairing

- short-lived one-time pairing code;
- device-generated key material;
- server stores public device identity and scopes, not local secrets;
- revocation and rotation;
- signed tasks with nonce, audience, expiry, and exact payload hash;
- local policy re-evaluation even after cloud approval.

## UX requirements

- local status icon and clear online/offline state;
- approval cards show action, resource, arguments, data leaving device, cost, reversibility, and expiry;
- emergency stop immediately cancels queued local actions;
- audit view can export a redacted trace;
- failures do not fall back to broader permissions.

## Privacy defaults

- raw voice: memory only, deleted after transcription unless explicitly saved;
- local file content: no cloud logging;
- local tool arguments: redacted in cloud trace when sensitive;
- private adapter and personalization data: local only;
- crash reports: opt in and scrubbed.

## V1 non-goals

- unrestricted desktop automation;
- elevated administrator actions;
- purchases or financial account operations;
- browser password or credential extraction;
- continuous ambient recording;
- autonomous email sending;
- cross-device synchronization of private memory without a separate encrypted design.
