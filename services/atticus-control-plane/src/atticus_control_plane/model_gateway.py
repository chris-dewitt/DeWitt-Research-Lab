"""Atticus-facing model gateway factory for the local open-weight path."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from drl_ai_core import (
    ChatMessage,
    CompletionConstraints,
    MockOpenWeightProvider,
    ModelGateway,
    ModelIdentity,
    ModelProvider,
    OutputMode,
    StructuredModelResponse,
)


class ClosedWeightStubProvider:
    """Test/demo stub that advertises a closed-weight commercial path.

    Never registered as the V1 demonstration primary. Exists so policy can
    reject silent commercial substitution.
    """

    def __init__(self, provider_id: str = "commercial-stub") -> None:
        self._identity = ModelIdentity(
            provider_id=provider_id,
            model_family="commercial-stub",
            revision="denied-by-default",
            open_weight=False,
            output_mode=OutputMode.LIVE,
            license_label="proprietary",
            runtime="stub",
        )

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    def health(self) -> bool:
        return True

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        tools: Sequence[dict[str, Any]] | None = None,
        constraints: CompletionConstraints,
    ) -> StructuredModelResponse:
        raise RuntimeError("closed-weight stub must never be invoked on open path")


def build_local_model_gateway(
    *,
    primary_latency_seconds: float = 0.0,
    include_commercial_stub: bool = False,
) -> ModelGateway:
    """Build the unpaid local gateway used by foundation demos and tests."""

    primary = MockOpenWeightProvider(
        provider_id="mock-open-weight-primary",
        latency_seconds=primary_latency_seconds,
    )
    fallback = MockOpenWeightProvider(
        provider_id="mock-open-weight-fallback",
        model_family="atticus-edge",
        revision="fixture-edge-0.1.0",
        quantization="q4_0",
    )
    providers: dict[str, ModelProvider] = {
        primary.identity.provider_id: primary,
        fallback.identity.provider_id: fallback,
    }
    if include_commercial_stub:
        stub = ClosedWeightStubProvider()
        providers[stub.identity.provider_id] = stub
    return ModelGateway(
        providers,
        primary=primary.identity.provider_id,
        fallback=fallback.identity.provider_id,
    )
