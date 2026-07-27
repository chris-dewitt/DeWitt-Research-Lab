---
document_id: DRL-CLOUD-002
title: "Azure Optional Portability Profile"
version: 1.0.0
status: APPROVED FOUNDATION
owner: DeWitt
last_updated: 2026-07-27
---

# Azure Optional Portability Profile

Google Cloud remains DRL's reference deployment architecture. Azure is a
deliberate portability option for future collaborators, Microsoft-oriented
workflows, and deployment experiments.

| DRL capability | Google reference | Azure option |
|---|---|---|
| Container services | Cloud Run | Azure Container Apps |
| Managed training | Vertex AI | Azure Machine Learning |
| Container registry | Artifact Registry | Azure Container Registry |
| PostgreSQL | Cloud SQL | Azure Database for PostgreSQL |
| Object storage | Cloud Storage | Blob Storage |
| Secrets | Secret Manager | Key Vault |
| Queues/events | Cloud Tasks and Pub/Sub | Service Bus and Event Grid |
| Logs/metrics | Cloud Logging and Monitoring | Azure Monitor |
| Workload identity | Google service accounts | Managed identities |

## Portability rule

Domain code depends on DRL contracts, OCI images, PostgreSQL-compatible
interfaces, object-storage adapters, OpenTelemetry, and explicit provider
ports—not cloud SDK calls scattered through research logic. Cloud-specific
adapters remain at deployment and infrastructure boundaries.

Azure parity is not required for every V1 release. The minimum portability gate
is:

1. build the same Atticus image;
2. validate the Bicep template;
3. deploy privately to an approved development resource group;
4. pass `/healthz` and the synthetic integrated workflow;
5. record cost and operational differences;
6. destroy the experiment and verify cleanup.

No production dual-cloud promise may be made without measured evidence and a
new Director-approved ADR.
