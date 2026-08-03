---
document_id: DRL-ARC-001
title: "System Context and C4 Architecture"
version: 2.0.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-07-26
---


# System Context and C4 Architecture

## System context

DeWitt Research Workshop is a public research and software platform used by anonymous visitors, authenticated public researchers, contributors, the Director as private operator, and administrators. It integrates public data providers, model runtimes, Google Cloud services, GitHub, and optional local tools.

### External actors and systems

- anonymous visitor;
- authenticated public researcher;
- contributor/maintainer;
- The Director/private operator;
- administrator/release operator;
- public economic and Federal Reserve sources;
- GitHub and package/model registries;
- Google Cloud and Firebase identity/services;
- open model registries;
- optional commercial model providers for development or disclosed fallback;
- local operating system, file system, repositories, microphone, and speakers.

## Container view

| Container | Responsibility | Trust level | Primary technology |
|---|---|---|---|
| Lab Web | public pages, docs, console shell, replay | public edge | Next.js/TypeScript |
| Atticus Console | streaming chat, plan, trace, approval UI | public/authenticated | TypeScript |
| Atticus Control Plane | sessions, skills, routing, policy integration | restricted service | FastAPI/Python |
| Model Gateway | model identity, routing, quotas, inference adapters | restricted service | Python |
| Inference Service | open-weight model serving | isolated compute | vLLM/SGLang/llama.cpp by profile |
| Atlas | ingestion, temporal research, evidence | restricted service | Python/PostgreSQL |
| FedLens | corpus, diff, policy tools | restricted service | Python/PostgreSQL |
| BalanceLab | synthetic institutions and deterministic engine | restricted service | Python/PostgreSQL |
| EvalForge | cases, replay, scoring, reports | restricted/public report | Python |
| Local Runner | private tools and local policy | private device | Python/native adapters |
| Data Platform | SQL, object storage, queues, cache | restricted infrastructure | Cloud SQL/Storage/PubSub/Redis optional |
| Observability | traces, metrics, logs, alerts | restricted operations | OpenTelemetry/Cloud Monitoring |

## Trust zones

1. Public browser and untrusted uploads.
2. Public web edge.
3. Authenticated application services.
4. Data and model services.
5. administrative/release systems.
6. private local device.
7. third-party public sources and registries.

All crossings require identity, validation, minimum data, and trace correlation. Local/private zone does not become transitively trusted because it is paired.

## Component view: Atticus control plane

- API/session gateway;
- request normalizer;
- skill registry;
- planner/router;
- deterministic policy client;
- approval service;
- tool dispatcher;
- specialist clients;
- evidence/context assembler;
- model gateway client;
- memory interfaces;
- trace emitter;
- result synthesizer;
- quota/cost guard;
- replay recorder.

The planner has no direct network or operating-system access. It can only propose registered tool calls.
