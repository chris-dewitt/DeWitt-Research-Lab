# Google Cloud deployment starter

Google Cloud is DRL's reference production platform. This directory contains a
budget-conscious prototype path for the public-fixture Atticus server:

- build the root-context image with the control-plane Dockerfile;
- push it to Artifact Registry;
- deploy it to Cloud Run with scale-to-zero and a two-instance ceiling;
- keep the service authenticated until public quotas, abuse controls, privacy
  review, and Director approval are complete.

The template intentionally contains `PROJECT_ID`, `REGION`, and `IMAGE_TAG`
placeholders. Do not commit billing identifiers, credentials, service-account
keys, or production URLs.

## Prototype deployment

```bash
gcloud builds submit \
  --config infra/gcp/cloudbuild-atticus.yaml \
  --substitutions _REGION=us-central1
```

Before running it:

1. resolve `DIR-002` in `DIRECTORS_MEMO.md`;
2. enable Cloud Build, Artifact Registry, and Cloud Run;
3. create a least-privilege runtime service account;
4. configure a hard budget and alerts;
5. review the generated plan and intended public access;
6. deploy to development, never production by default.

The service currently exposes only synthetic fixture research and must retain
the maturity label `prototype`.
