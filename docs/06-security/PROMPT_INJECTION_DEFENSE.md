---
document_id: DRL-SEC-004
title: "Prompt Injection and Untrusted Content Defense"
version: 2.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-26
---


# Prompt Injection and Untrusted Content Defense

## Trust labels

Every context segment is labeled:

- system policy;
- skill instruction;
- user instruction;
- trusted tool metadata;
- untrusted source/evidence;
- tool result;
- private memory;
- prior assistant output.

Untrusted source text is never concatenated as instruction. The model is reminded to summarize/analyze it, not obey it.

## Controls

- retrieve minimal necessary passages;
- strip/normalize hidden markup where safe while preserving source;
- detect known injection patterns as signal, not sole defense;
- keep secrets out of model context;
- expose only tools needed by selected skill;
- policy validates every call independently;
- destination/data-class restrictions;
- use separate extraction models/tasks for high-risk documents where beneficial;
- show source and detected suspicious instructions to user/operator;
- adversarial training and regression suites.

## Indirect injection handling

If a source says “send this document to…” Atticus may report that the source contains an instruction; he cannot treat it as user intent. Tool results are also untrusted because external systems may return malicious strings.

## Failure response

On suspected injection:

- continue safely if evidence can be isolated;
- omit compromised source and find alternate evidence;
- ask user if task intent genuinely requires the action;
- deny tool call if data/permission conflict;
- create a security finding if the system attempted compliance.
