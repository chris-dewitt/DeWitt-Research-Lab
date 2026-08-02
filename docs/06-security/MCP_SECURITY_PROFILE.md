---
document_id: DRL-SEC-011
title: "MCP Adapter Security Profile"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# MCP Adapter Security Profile

## Position

MCP is supported as an interoperability layer for tools and resources. DRL does not delegate policy or tenant authority to an MCP server.

## Requirements

- current supported protocol version pinned/tested;
- stdio for local tools where appropriate; streamable HTTP for remote servers;
- OAuth/authorization practices for remote access;
- server identity and destination allowlist;
- tool manifest mapped into DRL risk/scopes;
- arguments validated by DRL schema;
- no token passthrough to untrusted servers;
- prevent confused-deputy and token audience errors;
- user consent for dynamic client registration where applicable;
- output treated as untrusted content;
- timeout, cancellation, and audit;
- no hidden server-initiated access beyond declared capability.

Community MCP servers are disabled in public production until reviewed and allowlisted.
