"""Deterministic mock open-weight provider for local development and CI."""

from __future__ import annotations

import time
from collections.abc import Sequence
from typing import Any

from .providers import (
    ChatMessage,
    CompletionConstraints,
    ModelIdentity,
    OutputMode,
    ProviderTimeoutError,
    ProviderUnavailableError,
    StructuredModelResponse,
)


class MockOpenWeightProvider:
    """A fixture model that never calls a paid API.

    Test knobs:
    - ``latency_seconds``: simulated work duration checked against timeouts
    - ``fail_closed``: raise ``ProviderUnavailableError`` on every call
    - ``healthy``: health probe result
    """

    def __init__(
        self,
        *,
        provider_id: str = "mock-open-weight",
        model_family: str = "atticus-core",
        revision: str = "fixture-0.1.0",
        latency_seconds: float = 0.0,
        fail_closed: bool = False,
        healthy: bool = True,
        quantization: str | None = "q4_k_m",
    ) -> None:
        self._identity = ModelIdentity(
            provider_id=provider_id,
            model_family=model_family,
            revision=revision,
            open_weight=True,
            output_mode=OutputMode.MOCK,
            license_label="Apache-2.0-or-upstream-pending-bakeoff",
            quantization=quantization,
            runtime="deterministic-fixture",
        )
        self.latency_seconds = latency_seconds
        self.fail_closed = fail_closed
        self.healthy = healthy

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    def health(self) -> bool:
        return self.healthy and not self.fail_closed

    def complete(
        self,
        messages: Sequence[ChatMessage],
        *,
        tools: Sequence[dict[str, Any]] | None = None,
        constraints: CompletionConstraints,
    ) -> StructuredModelResponse:
        if not messages:
            raise ValueError("messages cannot be empty")
        if constraints.require_open_weight and not self.identity.open_weight:
            raise ProviderUnavailableError("mock provider is not open-weight")
        if self.fail_closed or not self.healthy:
            raise ProviderUnavailableError(
                f"provider {self.identity.provider_id!r} is unavailable"
            )
        if self.latency_seconds > constraints.timeout_seconds:
            raise ProviderTimeoutError(
                f"provider {self.identity.provider_id!r} exceeded "
                f"{constraints.timeout_seconds:.3f}s timeout"
            )

        started = time.perf_counter()
        if self.latency_seconds > 0:
            time.sleep(self.latency_seconds)

        user_text = next(
            (message.content for message in reversed(messages) if message.role == "user"),
            messages[-1].content,
        )
        tool_names = [str(tool.get("name", "")) for tool in (tools or ()) if tool.get("name")]
        content = (
            "MOCK OPEN-WEIGHT RESPONSE\n"
            f"objective={user_text.strip()}\n"
            f"tools={','.join(tool_names) if tool_names else 'none'}\n"
            "This fixture discloses identity and does not call a paid model API."
        )
        if len(content) > constraints.max_output_tokens * 4:
            content = content[: constraints.max_output_tokens * 4]

        elapsed_ms = (time.perf_counter() - started) * 1000.0
        return StructuredModelResponse(
            content=content,
            identity=self.identity,
            finish_reason="stop",
            latency_ms=elapsed_ms,
            usage={
                "prompt_tokens": sum(len(message.content.split()) for message in messages),
                "completion_tokens": len(content.split()),
            },
            structured={
                "mock": True,
                "open_weight_required": constraints.require_open_weight,
            },
        )
