# drl-ai-core

Provide carefully bounded shared infrastructure used by more than one component: model-provider abstractions, structured-output validation, retries/deadlines/cancellation, tracing, provenance helpers, safe redaction, configuration, cost accounting, and deterministic IDs/digests.

Current implemented surface (prototype maturity): open-weight `ModelProvider` /
`ModelGateway`, deterministic `MockOpenWeightProvider`, and
`StructuredOutputValidator` with bounded repair and content-minimized traces.

Authoritative specification: [`docs/SPEC.md`](docs/SPEC.md).
