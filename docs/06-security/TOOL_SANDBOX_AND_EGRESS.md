---
document_id: DRL-SEC-005
title: "Tool Sandboxing, Filesystem, Network, and Egress Controls"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Tool Sandboxing, Filesystem, Network, and Egress Controls

## Public execution

Public tools run in isolated service identities and containers with:

- no host filesystem;
- read-only root where practical;
- temporary per-task workspace;
- CPU/memory/time/process limits;
- network destination allowlist;
- no cloud metadata access beyond workload identity;
- no production admin credentials;
- sanitized output and bounded artifact size.

## Local execution

- approved roots resolved to canonical paths;
- deny traversal, symlink escape, hidden credential locations;
- commands expressed as executable plus argument list, not shell text;
- allowlisted command families and working directories;
- separate read/test/patch/commit/push permissions;
- environment variable allowlist/redaction;
- child process and timeout limits;
- diff and artifact inspection before write/commit.

## Network tools

- URL parser and DNS/IP checks;
- deny internal/cloud metadata/private network destinations unless explicitly designed;
- redirect limits;
- content type and size limits;
- TLS validation;
- source license/robots/terms considerations for collectors;
- never append secret/private content to arbitrary query strings.
