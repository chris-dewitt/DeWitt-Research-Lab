---
document_id: DRL-REF-001
title: "Technical Reference Register"
version: 4.1.0
status: APPROVED FOUNDATION
owner: Christopher Noxon DeWitt
last_updated: 2026-08-05
---

# Technical Reference Register

## Purpose and update rule

This register records primary technical sources that underpin volatile implementation assumptions. It is not a substitute for revalidation. The agent owning a feature must re-open the authoritative source near implementation and release, record the exact version/revision and reviewed date, and create an ADR when current behavior materially changes the plan.

## Open AI terminology and licensing

| Topic | Primary source | Foundation use | Revalidate before |
|---|---|---|---|
| Open Source AI Definition 1.0 | `https://opensource.org/ai` | precise distinction among Open Source AI, open weights, and public artifacts | every model/public-identity release |
| Open Source Definition and approved licenses | `https://opensource.org/osd`, `https://opensource.org/licenses` | software licensing vocabulary | dependency and release review |
| Apache License 2.0 | OSI/Apache canonical license text | DRL-authored software default | legal/release review |
| Gemma terms | `https://ai.google.dev/gemma/terms` | separate custom-license review; never assume OSI status | bakeoff and release |

## Current open-weight model candidates (verified 2026-07-26)

| Topic | Primary source | Foundation use | Revalidate before |
|---|---|---|---|
| Qwen 3.5 9B/4B | `https://huggingface.co/Qwen/Qwen3.5-9B`, `https://huggingface.co/Qwen/Qwen3.5-4B` | Apache-2.0 Core/Edge bakeoff candidates; tool-serving flags documented in cards | bakeoff, training, release |
| Qwen tool/coding models | official Qwen organization model cards | teacher, coding, and agent baseline candidates | synthetic-data and benchmark runs |
| Mistral 3 / Ministral 3 | `https://mistral.ai/news/mistral-3/`, current exact model cards | Apache-2.0 3B/8B/14B candidates; distinguish older Ministral licenses | bakeoff and release |
| Gemma 4 | `https://ai.google.dev/gemma/docs/core`, `https://ai.google.dev/gemma/docs/core/model_card_4` | E-class/12B open-weight candidates and Google-native research path | bakeoff, terms, training |
| Gemma function calling | `https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4` | agent/tool experiments with application safeguards | template/parser lock |

## Open model training, distribution, and serving

| Topic | Primary source | Foundation use | Revalidate before |
|---|---|---|---|
| Hugging Face Hub | `https://huggingface.co/docs/hub/index` | Git-based model/dataset/demo release and community surface | org/release setup |
| Model cards | `https://huggingface.co/docs/hub/model-cards` | model transparency and release metadata | every model release |
| Dataset cards | `https://huggingface.co/docs/hub/datasets-cards` | data transparency and discoverability | every dataset release |
| Model release checklist | `https://huggingface.co/docs/hub/model-release-checklist` | official release process and community evaluations | release candidate |
| TRL | `https://huggingface.co/docs/trl/index` | SFT, DPO/GRPO and other post-training surfaces | training container lock |
| PEFT | `https://huggingface.co/docs/peft/en/index` | LoRA/parameter-efficient adaptation | training container lock |
| Google QLoRA/Colab guide | `https://ai.google.dev/gemma/docs/core/huggingface_text_finetune_qlora` | Colab/Vertex reproducibility pattern | notebook/job implementation |
| vLLM serving and tool calling | `https://docs.vllm.ai/en/latest/serving/online_serving/`, `https://docs.vllm.ai/en/stable/features/tool_calling/` | cloud open-weight serving and tool parser validation | inference lock |
| llama.cpp | `https://github.com/ggml-org/llama.cpp`, server README | local quantized serving, OpenAI-compatible API, tool/schema paths | local runner and GGUF release |
| MLflow | `https://github.com/mlflow/mlflow` | optional open experiment tracking/model registry/evaluation integration | experiment platform ADR |

## Open data, observability, and infrastructure

| Topic | Primary source | Foundation use | Revalidate before |
|---|---|---|---|
| PostgreSQL/pgvector | `https://github.com/pgvector/pgvector` | open relational/vector store | database implementation |
| OpenTelemetry | `https://opentelemetry.io/docs/`, `https://opentelemetry.io/docs/what-is-opentelemetry/` | vendor-neutral traces, metrics, logs | observability lock |
| OpenTofu | `https://opentofu.org/` | Linux Foundation open-source IaC candidate and Terraform-language compatibility | IaC ADR and CI lock |
| Terraform terms | official HashiCorp license/product docs | source-available comparison and compatibility risk | IaC ADR |
| SLSA 1.2 | `https://slsa.dev/spec/v1.2/` | build provenance and supply-chain maturity | release pipeline |
| OpenSSF Scorecard | `https://scorecard.dev/` | repository security-practice assessment | public repo setup |
| SPDX | `https://spdx.dev/`, `https://spdx.dev/learn/areas-of-interest/ai/` | software/AI SBOM and license information | artifact release |
| REUSE 3.3 | `https://reuse.software/spec/` | machine/human-readable file licensing | repository compliance setup |

## Google platform

| Topic | Primary source | Foundation use | Revalidate before |
|---|---|---|---|
| Firebase App Hosting | official Firebase documentation | website delivery default | first deploy and promotion |
| Cloud Run GPU | official Cloud Run GPU documentation | public open-weight inference | service creation/capacity plan |
| Cloud SQL PostgreSQL/pgvector | official Cloud SQL documentation | managed production storage | schema/performance implementation |
| Vertex AI custom training | official Vertex AI documentation | durable repeatable training | first job |
| Colab FAQ and limits | official Colab documentation | interactive research only | notebook guidance |
| Artifact Registry | official Google Cloud documentation | OCI images and build artifacts | CI/CD implementation |
| Secret Manager/IAM/WIF | official Google Cloud documentation | secrets and deployment identity | infrastructure implementation |

## Security and interoperability

| Topic | Primary source | Foundation use | Revalidate before |
|---|---|---|---|
| NIST AI RMF and Generative AI Profile | official NIST publications | Govern/Map/Measure/Manage framing | release review |
| Model Context Protocol | official MCP specification/security guidance | optional interoperability with explicit trust boundaries | MCP implementation |
| JSON Schema 2020-12 | official JSON Schema specification | canonical DRL contracts | schema tooling lock |
| OpenAPI 3.1 | official OpenAPI specification | HTTP contracts | API generation/validation |

## Computational Finance of Intelligence novelty boundary (verified 2026-08-05)

These records are research-boundary controls, not evidence that a DRL proposal
is novel or that a reported result will replicate. The current synthesis and
source-by-source overlap assessment live in
`docs/10-research/CFI_PRIMARY_SOURCE_NOVELTY_REVIEW.md`. Preprints and workshop
records are volatile and must be re-opened before G1 review and protocol freeze.

| Topic | Primary source | Foundation use | Revalidate before |
|---|---|---|---|
| Sequential model-belief trajectories | `https://arxiv.org/abs/2606.30850` (BayesBench) | Direct collision control for sequential evidence, Bayesian comparison, and latent framing | 2026-09-05 and G1 |
| Linguistic/numeric sequential belief state | `https://arxiv.org/abs/2604.18576` (BLF) | Direct collision control for logit-space linguistic belief updating and calibration | 2026-09-05 and G1 |
| Observable learned reasoning stopper | `https://arxiv.org/abs/2606.30852` (LearnStop) | Contribution-collapsing control for the original Paper I hypothesis | 2026-09-05 and any Paper I redesign |
| Metareasoning and value of computation | `https://arxiv.org/abs/1207.5879`, `https://arxiv.org/abs/1711.06892` | Foundational control for computation selection and resource-rational planning | Paper I question freeze |
| Outcome-free coherence audit and repair | `https://openreview.net/forum?id=U27ZfUx7JE` | Contribution-collapsing control for Dutch-book auditing, coherent projection, and coherence/calibration separation | 2026-09-05 and G1 |
| Payoff-preserving LLM framing | `https://arxiv.org/abs/2503.04840` | Direct collision control for context framing with fixed game structure | 2026-09-05 and Paper II protocol freeze |
| Option replication and no-arbitrage oracle | `https://www.journals.uchicago.edu/doi/10.1086/260062`, `https://doi.org/10.2307/3003143` | Established finance baseline; never represent the pricing restrictions as a new contribution | Paper II protocol freeze |
| Private-signal AI-agent prediction markets | `https://arxiv.org/abs/2604.20050` | Contribution-collapsing control for Paper III's broad aggregation question | 2026-09-05 and any Paper III redesign |
| Correlated LLM errors and market monoculture | `https://arxiv.org/abs/2606.26583`, `https://arxiv.org/abs/2606.13038` | Contribution-collapsing control for shared-error, effective-diversity, and prompt-diversity claims | 2026-09-05 and any Paper III redesign |
| Incentive-compatible LLM wagering aggregation | `https://arxiv.org/abs/2607.04389` (WALLA) | Direct mechanism-design collision control | 2026-09-05 and any Paper III redesign |
| Consensus, cascades, and market scoring rules | `https://doi.org/10.1080/01621459.1974.10480137`, `https://doi.org/10.1086/261849`, `https://hanson.gmu.edu/mktscore.pdf` | Foundational coupled-belief and information-market baselines | Paper III question freeze |

## Recording current assumptions

Every implementation PR relying on a volatile source adds a note with source title, canonical URL, version/tag or retrieval date, relevant claim, exact license where material, and whether it confirms or changes the foundation. Avoid copying benchmark marketing claims into DRL specifications; record only behavior and terms necessary to the laboratory.

| Valkey | `https://valkey.io/`, `https://github.com/valkey-io/valkey` | BSD open-source cache/coordination candidate | ADR-0007 and platform spike |
| Google Memorystore for Valkey | `https://cloud.google.com/memorystore/docs/valkey` | managed Google Cloud Valkey path; distinguish service from upstream software | platform architecture |


## Wix, domain, and public-site integration

| Topic | Primary source | Foundation use | Revalidate before |
|---|---|---|---|
| Connect an existing domain to Wix | `https://support.wix.com/en/article/connecting-a-domain-you-own-to-your-wix-site` | existing `dewitt-labs.com` connection workflow and ownership choices | initial domain connection and any host migration |
| Wix nameserver connection | `https://support.wix.com/en/article/connecting-a-domain-to-the-wix-name-servers` | option where Wix manages authoritative DNS | connection-method decision |
| Wix pointing connection | `https://support.wix.com/en/article/connecting-a-domain-to-wix-using-the-pointing-method` | option where DNS remains with current host; useful to evaluate for multi-subdomain architecture | connection-method decision |
| Wix custom elements | `https://support.wix.com/en/article/studio-editor-adding-a-custom-element`, `https://dev.wix.com/docs/velo/velo-only-apis/%24w/custom-element/introduction` | bounded public widgets and externally hosted custom elements | widget implementation |
| Wix embeds and iframe limitations | `https://support.wix.com/en/article/studio-editor-adding-an-html-iframe-element` | fallback, sandbox, responsiveness, and no-primary-app-iframe policy | every embed |
| Wix Headless | `https://dev.wix.com/docs/go-headless/get-started/about-headless/about-wix-headless` | later option for shared CMS/membership/business data across custom frontends | any headless/SSO ADR |
| Wix custom site APIs | `https://dev.wix.com/docs/develop-websites/articles/coding-with-velo/integrations/exposing-services/about-custom-site-apis` | optional controlled Wix-to-DRL integration | API bridge implementation |
