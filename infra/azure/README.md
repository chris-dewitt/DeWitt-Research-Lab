# Azure portability profile

Azure is an approved optional deployment target, not the DRL V1 reference
production platform. The Bicep template proves that the same OCI image and HTTP
health/task contracts can run on Azure Container Apps without changing domain
logic.

Safety defaults:

- internal ingress;
- managed identity;
- scale-to-zero;
- maximum two replicas;
- no embedded credentials;
- development or staging environments only;
- 30-day prototype log retention.

## Validate

```bash
az bicep build --file infra/azure/main.bicep
az deployment group what-if \
  --resource-group YOUR_DEV_RESOURCE_GROUP \
  --template-file infra/azure/main.bicep \
  --parameters containerImage=YOUR_IMAGE
```

Do not deploy until the target subscription, resource group, cost ceiling,
identity permissions, registry access, and deletion plan are reviewed. Public
ingress remains disabled until the same authentication, quota, abuse, privacy,
and Director gates required by the GCP deployment are satisfied.
